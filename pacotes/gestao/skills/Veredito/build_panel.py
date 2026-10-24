#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""veredito · build_panel.py
Gera o HTML autossuficiente do painel a partir de um manifesto JSON, usando o
motor unico em template/panel.html. Toda imagem local e embutida em base64
(comprimida com PIL ~1100px / JPEG q70 por padrao), para o HTML ser 100%
autocontido e offline.

Uso:
  python3 build_panel.py manifesto.json [--out saida.html]

Manifesto (ver reference/manifest-schema.md):
  {"title":..., "subtitle":..., "batch":"meu-lote", "round":1,
   "items":[{"id":"a1","kind":"image","src":"/caminho/img.png"}, ...]}

Campos de imagem processados (caminho local -> base64): src, img, image, screenshot.
Se ja for data: URI ou http(s), fica como esta (a menos de --refetch, nao implementado).
Saida padrao: _run/<batch>/panel.html
"""
import argparse, base64, io, json, mimetypes, os, re, sys

BASE = os.path.dirname(os.path.abspath(__file__))
TEMPLATE = os.path.join(BASE, "template", "panel.html")
RUN = os.path.join(BASE, "_run")
IMG_FIELDS = ("src", "img", "image", "screenshot")


def safe_batch(b):
    return re.sub(r"[^A-Za-z0-9._-]", "_", str(b))[:64] or "batch"


def is_embedded(v):
    return isinstance(v, str) and (v.startswith("data:") or v.startswith("http://") or v.startswith("https://"))


def raw_datauri(path):
    mime = mimetypes.guess_type(path)[0] or "application/octet-stream"
    with open(path, "rb") as f:
        b = f.read()
    return "data:%s;base64,%s" % (mime, base64.b64encode(b).decode())


def compress_datauri(path, max_w=1100, quality=70):
    """Redimensiona para <=max_w e salva JPEG q70. Cai para embed cru se PIL falhar."""
    ext = os.path.splitext(path)[1].lower()
    if ext == ".svg":
        return raw_datauri(path)  # SVG e vetorial: embute cru
    try:
        from PIL import Image
    except Exception:
        return raw_datauri(path)
    try:
        im = Image.open(path)
        if im.mode in ("RGBA", "LA", "P"):
            bg = Image.new("RGB", im.size, (255, 255, 255))
            im = im.convert("RGBA")
            bg.paste(im, mask=im.split()[-1])
            im = bg
        else:
            im = im.convert("RGB")
        if im.width > max_w:
            h = int(round(im.height * max_w / im.width))
            im = im.resize((max_w, h), Image.LANCZOS)
        buf = io.BytesIO()
        im.save(buf, format="JPEG", quality=quality, optimize=True)
        return "data:image/jpeg;base64," + base64.b64encode(buf.getvalue()).decode()
    except Exception as e:
        sys.stderr.write("[build_panel] aviso: falha ao comprimir %s (%s); embutindo cru\n" % (path, e))
        return raw_datauri(path)


def process_items(items, base_dir, no_compress):
    n_embed = 0
    for it in items:
        if not isinstance(it, dict):
            continue
        for fld in IMG_FIELDS:
            v = it.get(fld)
            if not v or not isinstance(v, str) or is_embedded(v):
                continue
            path = v if os.path.isabs(v) else os.path.join(base_dir, v)
            if not os.path.exists(path):
                sys.stderr.write("[build_panel] aviso: imagem nao encontrada: %s\n" % path)
                continue
            uri = raw_datauri(path) if (no_compress or it.get("no_compress")) else compress_datauri(path)
            # url usa 'img' no motor; image usa 'src'; normaliza screenshot/image -> destino certo
            dest = "src" if it.get("kind") == "image" else ("img" if it.get("kind") == "url" else fld)
            it[dest] = uri
            if dest != fld:
                it.pop(fld, None)
            n_embed += 1
    return n_embed


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("manifest")
    ap.add_argument("--out", default=None)
    ap.add_argument("--no-compress", action="store_true", help="embute imagens cruas (sem PIL/JPEG)")
    a = ap.parse_args()

    with open(a.manifest, encoding="utf-8") as f:
        man = json.load(f)

    man.setdefault("items", [])
    man["batch"] = man.get("batch") or os.path.splitext(os.path.basename(a.manifest))[0]
    batch = safe_batch(man["batch"])
    man["batch"] = batch

    base_dir = os.path.dirname(os.path.abspath(a.manifest))
    n = process_items(man["items"], base_dir, a.no_compress)

    with open(TEMPLATE, encoding="utf-8") as f:
        tpl = f.read()
    if "__AR_BOARD_MANIFEST__" not in tpl:
        raise SystemExit("ERRO: placeholder __AR_BOARD_MANIFEST__ ausente no template")
    data = json.dumps(man, ensure_ascii=False)
    html = tpl.replace("__AR_BOARD_MANIFEST__", data)

    out = a.out
    if not out:
        run_dir = os.path.join(RUN, batch)
        os.makedirs(run_dir, exist_ok=True)
        out = os.path.join(run_dir, "panel.html")
    with open(out, "w", encoding="utf-8") as f:
        f.write(html)

    size_mb = os.path.getsize(out) / 1024 / 1024
    print(json.dumps({
        "ok": True, "batch": batch, "html": out,
        "items": len(man["items"]), "images_embedded": n,
        "size_mb": round(size_mb, 2)
    }, ensure_ascii=False))


if __name__ == "__main__":
    main()
