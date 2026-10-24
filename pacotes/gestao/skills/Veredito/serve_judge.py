#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""veredito · serve_judge.py
Servidor local minimo (stdlib) para o MODO AO VIVO do painel. Serve UM painel
html em 127.0.0.1 numa porta EFEMERA e recebe POST /verdict, gravando o veredito
em _run/<batch>/verdict.json a cada acao.

Uso:
  python3 serve_judge.py --html <painel.html> --batch <id> [--watchdog <segundos>]

Regras:
 - WATCHDOG padrao = 180 MIN (10800s): sem requisicao por 180 min -> se mata.
 - pending==0 -> grava verdict.FINAL.json e CONTINUA VIVO (comentarios escritos depois do
   ultimo voto se perdiam). Cada POST posterior regrava o FINAL. Depois de completo, morre com
   30 min sem requisicao (--after-final), ou pelo watchdog geral.
 - SWEEP na largada: mata servidores orfaos de rodadas anteriores.
 - A porta escolhida fica em _run/<batch>/server.port; o pid em server.pid.
"""
import argparse, glob, json, os, re, signal, threading, time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

BASE = os.path.dirname(os.path.abspath(__file__))
RUN = os.path.join(BASE, "_run")
WATCHDOG_DEFAULT = 180 * 60  # 180 minutos


def log(msg):
    print(f"[{time.strftime('%H:%M:%S')}] {msg}", flush=True)


def safe_batch(b):
    return re.sub(r"[^A-Za-z0-9._-]", "_", b)[:64] or "batch"


def alive(pid):
    # No Windows, os.kill(pid, 0) ENCERRA o processo (TerminateProcess); consulta pela API.
    if os.name == "nt":
        import ctypes
        k = ctypes.windll.kernel32
        h = k.OpenProcess(0x1000, False, int(pid))  # PROCESS_QUERY_LIMITED_INFORMATION
        if not h:
            return False
        code = ctypes.c_ulong()
        ok = k.GetExitCodeProcess(h, ctypes.byref(code))
        k.CloseHandle(h)
        return bool(ok) and code.value == 259  # STILL_ACTIVE
    try:
        os.kill(pid, 0)
    except ProcessLookupError:
        return False
    except PermissionError:
        return True
    return True


def sweep(my_pid):
    """Le pids de rodadas anteriores, mata os que ainda estiverem vivos e limpa os arquivos."""
    killed = []
    for pf in glob.glob(os.path.join(RUN, "*", "server.pid")):
        pid = None
        try:
            pid = int(open(pf).read().strip())
        except Exception:
            pid = None
        if pid and pid != my_pid and os.name != "nt" and alive(pid):
            try:
                os.kill(pid, signal.SIGKILL)
                killed.append(pid)
                log(f"SWEEP: matou orfao vivo pid={pid} ({pf})")
            except Exception as e:
                log(f"SWEEP: falha ao matar pid={pid}: {e}")
        elif pid and pid != my_pid:
            log(f"SWEEP: pid={pid} ja estava morto (stale) ({pf})")
        for name in ("server.pid", "server.port"):
            p = os.path.join(os.path.dirname(pf), name)
            try:
                os.remove(p)
            except FileNotFoundError:
                pass
    if not killed:
        log("SWEEP: nenhum orfao vivo para matar")
    return killed


class State:
    last_req = time.time()
    final_at = None


def make_handler(html_path, run_dir):
    html_bytes = open(html_path, "rb").read()
    verdict_path = os.path.join(run_dir, "verdict.json")
    final_path = os.path.join(run_dir, "verdict.FINAL.json")

    def atomic_write(path, text):
        tmp = path + ".tmp"
        with open(tmp, "w", encoding="utf-8") as f:
            f.write(text)
        os.replace(tmp, path)

    def selfkill():
        for name in ("server.pid", "server.port"):
            try:
                os.remove(os.path.join(run_dir, name))
            except FileNotFoundError:
                pass
        log("SELF-KILL: lote completo, encerrando processo")
        os._exit(0)

    class H(BaseHTTPRequestHandler):
        def log_message(self, fmt, *args):
            log("HTTP " + (fmt % args))

        def _touch(self):
            State.last_req = time.time()

        def do_GET(self):
            self._touch()
            if self.path in ("/", "/index.html"):
                self.send_response(200)
                self.send_header("Content-Type", "text/html; charset=utf-8")
                self.send_header("Content-Length", str(len(html_bytes)))
                self.end_headers()
                self.wfile.write(html_bytes)
            elif self.path == "/favicon.ico":
                self.send_response(204)
                self.end_headers()
            else:
                self.send_response(404)
                self.end_headers()

        def do_POST(self):
            self._touch()
            if self.path != "/verdict":
                self.send_response(404)
                self.end_headers()
                return
            n = int(self.headers.get("Content-Length", "0") or 0)
            raw = self.rfile.read(n) if n else b"{}"
            try:
                payload = json.loads(raw.decode("utf-8"))
            except Exception:
                self.send_response(400)
                self.end_headers()
                self.wfile.write(b'{"ok":false}')
                return
            atomic_write(verdict_path, json.dumps(payload, ensure_ascii=False, indent=2))
            pending = (payload.get("counts") or {}).get("pending", None)
            final = (pending == 0)
            if final:
                atomic_write(final_path, json.dumps(payload, ensure_ascii=False, indent=2))
                log("LOTE COMPLETO: verdict.FINAL.json gravado (pending==0)")
            body = json.dumps({"ok": True, "final": final}).encode()
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)
            if final:
                State.final_at = State.final_at or time.time()

    return H


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--html", required=True)
    ap.add_argument("--batch", required=True)
    ap.add_argument("--watchdog", type=int, default=WATCHDOG_DEFAULT,
                    help="segundos sem requisicao ate se matar (padrao 10800 = 180 min)")
    # Padrao seguro: so nesta maquina. Use --host 0.0.0.0 para abrir no celular/outro
    # computador da MESMA rede (qualquer pessoa na rede local tambem consegue abrir).
    ap.add_argument("--host", default="127.0.0.1",
                    help="interface de escuta (padrao 127.0.0.1 = so nesta maquina; 0.0.0.0 = rede local)")
    ap.add_argument("--after-final", type=int, default=30 * 60,
                    help="segundos sem requisicao DEPOIS do lote completo ate se matar (padrao 30 min)")
    a = ap.parse_args()

    os.makedirs(RUN, exist_ok=True)
    my_pid = os.getpid()
    log(f"START pid={my_pid} batch={a.batch} watchdog={a.watchdog}s")
    sweep(my_pid)

    batch = safe_batch(a.batch)
    run_dir = os.path.join(RUN, batch)
    os.makedirs(run_dir, exist_ok=True)

    handler = make_handler(os.path.abspath(a.html), run_dir)
    httpd = ThreadingHTTPServer((a.host, 0), handler)  # porta 0 = efemera, SO escolhe
    port = httpd.server_address[1]
    with open(os.path.join(run_dir, "server.pid"), "w") as f:
        f.write(str(my_pid))
    with open(os.path.join(run_dir, "server.port"), "w") as f:
        f.write(str(port))
    log(f"LISTEN http://127.0.0.1:{port}/  host={a.host}  run_dir={run_dir}")

    def watchdog():
        while True:
            time.sleep(2)
            idle = time.time() - State.last_req
            limit = a.after_final if getattr(State, "final_at", None) else a.watchdog
            if idle > limit:
                log(f"WATCHDOG: {idle:.0f}s sem requisicao (> {a.watchdog}s) -> encerrando")
                for name in ("server.pid", "server.port"):
                    try:
                        os.remove(os.path.join(run_dir, name))
                    except FileNotFoundError:
                        pass
                os._exit(0)
    threading.Thread(target=watchdog, daemon=True).start()

    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    main()
