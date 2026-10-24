#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""veredito · read_verdict.py
Le o veredito de um lote e devolve o resultado NORMALIZADO em JSON no stdout.
Prefere verdict.FINAL.json (lote completo); se nao existir, usa verdict.json
(parcial, ainda em andamento). Reporta o status para o agente saber como agir.

Uso:
  python3 read_verdict.py <batch> [--run-dir <dir>] [--raw]

Saida:
  {
    "status": "complete" | "partial" | "none",
    "server_alive": true/false,
    "batch": "...", "round": 1, "batch_note": "...",
    "counts": {"approved":..,"rejected":..,"maybe":..,"pending":..},
    "approved":[...], "rejected":[{id,label,comment}], "maybe":[...], "pending":[...],
    "reviewed_at": "...", "source": "verdict.FINAL.json" | "verdict.json" | null
  }
"""
import argparse, json, os, re, sys

BASE = os.path.dirname(os.path.abspath(__file__))
RUN = os.path.join(BASE, "_run")


def safe_batch(b):
    return re.sub(r"[^A-Za-z0-9._-]", "_", str(b))[:64] or "batch"


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
    except Exception:
        return False
    return True


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("batch")
    ap.add_argument("--run-dir", default=None)
    ap.add_argument("--raw", action="store_true", help="imprime o payload cru, sem normalizar")
    a = ap.parse_args()

    run_dir = a.run_dir or os.path.join(RUN, safe_batch(a.batch))
    final_p = os.path.join(run_dir, "verdict.FINAL.json")
    part_p = os.path.join(run_dir, "verdict.json")
    pid_p = os.path.join(run_dir, "server.pid")

    server_alive = False
    if os.path.exists(pid_p):
        try:
            server_alive = alive(int(open(pid_p).read().strip()))
        except Exception:
            server_alive = False

    src, path = None, None
    if os.path.exists(final_p):
        src, path = "verdict.FINAL.json", final_p
    elif os.path.exists(part_p):
        src, path = "verdict.json", part_p

    if not path:
        print(json.dumps({
            "status": "none", "server_alive": server_alive, "batch": safe_batch(a.batch),
            "counts": {}, "approved": [], "rejected": [], "maybe": [], "pending": [],
            "source": None, "run_dir": run_dir,
            "note": "Nenhum veredito no disco ainda. O painel pode nao ter sido tocado."
        }, ensure_ascii=False, indent=2))
        return

    with open(path, encoding="utf-8") as f:
        p = json.load(f)

    if a.raw:
        print(json.dumps(p, ensure_ascii=False, indent=2))
        return

    counts = p.get("counts") or {}
    status = "complete" if (src == "verdict.FINAL.json" or counts.get("pending", 1) == 0) else "partial"
    items = p.get("items") or []
    pending = [{"id": it.get("id"), "label": it.get("label", "")}
               for it in items if (it.get("verdict") or "pending") == "pending"]

    out = {
        "status": status,
        "server_alive": server_alive,
        "batch": p.get("batch", safe_batch(a.batch)),
        "round": p.get("round", 1),
        "batch_note": p.get("batch_note", ""),
        "counts": counts,
        "approved": p.get("approved", []),
        "rejected": p.get("rejected", []),
        "maybe": p.get("maybe", []),
        "pending": pending,
        "reviewed_at": p.get("reviewed_at"),
        "source": src,
        "run_dir": run_dir,
    }
    print(json.dumps(out, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
