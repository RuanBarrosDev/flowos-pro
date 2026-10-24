#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Mostruário — motor do otimizador de anúncio/ficha de produto para marketplaces e loja.

Só biblioteca padrão. Offline. Nunca acessa a internet e nunca publica nada.
Guarda tudo em ./.mostruario/ na raiz do projeto do membro.

O motor cuida da PARTE MECÂNICA e VERIFICÁVEL: catálogo de produtos, as regras e
limites de cada marketplace, a montagem do título no formato certo, a nota (scorecard)
do anúncio contra um checklist de conversão, e a exportação do anúncio pronto pra colar.
A COPY persuasiva (título, bullets, descrição) quem escreve é a IA, no tom do dono —
o motor valida, pontua e guarda. Nunca inventa especificação de produto.
"""

import argparse
import csv
import json
import os
import sys
import unicodedata
from datetime import datetime

# --------------------------------------------------------------------------- #
# Localização dos dados
# --------------------------------------------------------------------------- #
DATA_DIR = os.path.join(os.getcwd(), ".mostruario")
PRODUTOS = os.path.join(DATA_DIR, "produtos.csv")
ANUNCIOS = os.path.join(DATA_DIR, "anuncios.csv")
ANUNCIOS_DIR = os.path.join(DATA_DIR, "anuncios")
CONFIG = os.path.join(DATA_DIR, "config.md")

PRODUTO_COLS = [
    "id", "nome", "categoria", "marca", "modelo", "publico",
    "marketplace", "custo", "preco", "atributos", "diferenciais",
    "palavras", "notas", "criado",
]
ANUNCIO_COLS = ["id", "produto_id", "marketplace", "titulo", "nota", "arquivo", "atualizado"]

# --------------------------------------------------------------------------- #
# Regras por marketplace (limites oficiais conhecidos — SEMPRE confira, pois
# as plataformas mudam). Título em CARACTERES.
# --------------------------------------------------------------------------- #
MARKETPLACES = {
    "mercadolivre": {
        "nome": "Mercado Livre",
        "titulo_max": 60,
        "titulo_formula": "Produto + Marca + Modelo + Especificação principal",
        "usa_bullets": False,
        "descricao_max": 60000,
        "fotos_max": 12,
        "fotos_rec": 8,
        "palavras_slot": 0,          # ML não tem campo de palavra-chave; a busca lê título + ficha
        "atributos": "Ficha técnica é OBRIGATÓRIA e pesa no ranking (preencha o máximo).",
        "proibido": "Sem '(oferta)', emoji, telefone, link externo ou 'melhor/o nº1' no título.",
    },
    "shopee": {
        "nome": "Shopee",
        "titulo_max": 256,
        "titulo_formula": "Produto + Especificação/Tipo + Marca + Modelo (material, cor, tamanho, quantidade)",
        "usa_bullets": False,
        "descricao_max": 5000,
        "fotos_max": 9,
        "fotos_rec": 6,
        "palavras_slot": 0,          # Shopee lê título + descrição; sem espaço no início/fim
        "atributos": "Preencha TODOS os atributos do formulário da categoria (alimentam filtro e ranking).",
        "proibido": "Sem contato/redireciono pra fora da Shopee; sem espaço sobrando no título.",
    },
    "amazon": {
        "nome": "Amazon",
        "titulo_max": 200,           # regra prática 75 (mobile trunca ~70-80); keyword nos 1os ~50
        "titulo_rec": 75,
        "titulo_formula": "Marca + Modelo + Produto + Atributo-chave + Tamanho/Cor (keyword nos 1os 50)",
        "usa_bullets": True,
        "bullets_qtd": 5,
        "bullet_max": 255,           # 10-255 caracteres cada; só os 1os 1000 bytes somados indexam
        "descricao_max": 2000,
        "fotos_max": 9,
        "fotos_rec": 7,
        "palavras_slot": 249,        # backend search terms: 249 BYTES (estourar de-indexa TUDO)
        "atributos": "5 bullets (BENEFÍCIO em CAIXA ALTA) + termos de busca no backend (249 bytes, sem repetir o título).",
        "proibido": "Sem preço/promoção/frete/nome de vendedor no título; sem ! $ ? _ { } ^; sem repetir palavra >2x.",
    },
    "loja": {
        "nome": "Loja própria / Nuvemshop / Site",
        "titulo_max": 70,            # bom para SEO da aba do navegador
        "titulo_formula": "Produto + Atributo + Marca (pensando no Google)",
        "usa_bullets": True,
        "bullets_qtd": 5,
        "bullet_max": 200,
        "descricao_max": 5000,
        "fotos_max": 12,
        "fotos_rec": 6,
        "palavras_slot": 0,
        "atributos": "Título e descrição pensando também no Google (SEO). Veja a skill Alcance.",
        "proibido": "Evite copiar a descrição do fabricante (conteúdo duplicado derruba no Google).",
    },
}

ALIASES = {
    "ml": "mercadolivre", "mercado-livre": "mercadolivre", "mercado livre": "mercadolivre",
    "meli": "mercadolivre", "amz": "amazon", "site": "loja", "nuvemshop": "loja",
    "loja-propria": "loja", "própria": "loja",
}

# --------------------------------------------------------------------------- #
# Utilidades
# --------------------------------------------------------------------------- #
def _ensure_dir():
    os.makedirs(DATA_DIR, exist_ok=True)
    os.makedirs(ANUNCIOS_DIR, exist_ok=True)


def _read(path, cols):
    if not os.path.exists(path):
        return []
    with open(path, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def _write(path, cols, rows):
    _ensure_dir()
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=cols)
        w.writeheader()
        for r in rows:
            w.writerow({c: r.get(c, "") for c in cols})


def _now():
    return datetime.now().strftime("%Y-%m-%d %H:%M")


def _next_id(rows, prefix):
    n = 0
    for r in rows:
        rid = r.get("id", "")
        if rid.startswith(prefix) and rid[len(prefix):].isdigit():
            n = max(n, int(rid[len(prefix):]))
    return f"{prefix}{n+1:03d}"


def _norm_mkt(m):
    if not m:
        return ""
    key = m.strip().lower()
    key = ALIASES.get(key, key)
    return key if key in MARKETPLACES else key


def _mkt_or_die(m):
    key = _norm_mkt(m)
    if key not in MARKETPLACES:
        opts = ", ".join(MARKETPLACES.keys())
        print(f"⚠️  Marketplace '{m}' não reconhecido. Use um destes: {opts}")
        sys.exit(2)
    return key


def _split_list(s):
    if not s:
        return []
    return [x.strip() for x in s.split("||") if x.strip()]


def _parse_attrs(s):
    """'cor=azul||material=algodão' -> [(cor,azul),(material,algodão)]"""
    out = []
    for item in _split_list(s):
        if "=" in item:
            k, v = item.split("=", 1)
            out.append((k.strip(), v.strip()))
        else:
            out.append((item.strip(), ""))
    return out


def _bytes_len(s):
    return len(s.encode("utf-8"))


def _find_produto(pid_or_name):
    rows = _read(PRODUTOS, PRODUTO_COLS)
    for r in rows:
        if r["id"].lower() == pid_or_name.lower():
            return r, rows
    # busca por nome parcial
    hits = [r for r in rows if pid_or_name.lower() in r["nome"].lower()]
    if len(hits) == 1:
        return hits[0], rows
    return None, rows


# --------------------------------------------------------------------------- #
# Comandos
# --------------------------------------------------------------------------- #
def cmd_init(_):
    _ensure_dir()
    if not os.path.exists(PRODUTOS):
        _write(PRODUTOS, PRODUTO_COLS, [])
    if not os.path.exists(ANUNCIOS):
        _write(ANUNCIOS, ANUNCIO_COLS, [])
    print("✅ Mostruário pronto. Dados em ./.mostruario/ (produtos.csv, anuncios.csv, anuncios/).")


def cmd_produto_add(a):
    rows = _read(PRODUTOS, PRODUTO_COLS)
    pid = _next_id(rows, "P")
    row = {
        "id": pid,
        "nome": a.nome or "",
        "categoria": a.categoria or "",
        "marca": a.marca or "",
        "modelo": a.modelo or "",
        "publico": a.publico or "",
        "marketplace": _norm_mkt(a.marketplace) if a.marketplace else "",
        "custo": (a.custo or "").replace(",", "."),
        "preco": (a.preco or "").replace(",", "."),
        "atributos": a.atributos or "",
        "diferenciais": a.diferenciais or "",
        "palavras": a.palavras or "",
        "notas": a.notas or "",
        "criado": _now(),
    }
    rows.append(row)
    _write(PRODUTOS, PRODUTO_COLS, rows)
    print(f"✅ Produto {pid} cadastrado: {row['nome'] or '[SEM NOME — A CONFERIR]'}")
    faltando = [c for c in ("categoria", "marca", "atributos") if not row[c]]
    if faltando:
        print("   ⚠️  Faltou: " + ", ".join(faltando) + " → marque [A CONFERIR] com o dono.")


def cmd_definir(a):
    row, rows = _find_produto(a.id)
    if not row:
        print(f"⚠️  Produto '{a.id}' não encontrado.")
        sys.exit(2)
    campo = a.campo
    if campo not in PRODUTO_COLS or campo in ("id", "criado"):
        print(f"⚠️  Campo '{campo}' inválido. Editáveis: "
              + ", ".join(c for c in PRODUTO_COLS if c not in ("id", "criado")))
        sys.exit(2)
    valor = a.valor
    if campo in ("custo", "preco"):
        valor = valor.replace(",", ".")
    if campo == "marketplace":
        valor = _norm_mkt(valor)
    row[campo] = valor
    _write(PRODUTOS, PRODUTO_COLS, rows)
    print(f"✅ {row['id']}: {campo} = {valor}")


def cmd_catalogo(_):
    rows = _read(PRODUTOS, PRODUTO_COLS)
    if not rows:
        print("Catálogo vazio. Cadastre com produto-add ou peça pra IA cadastrar conversando.")
        return
    print(f"📦 CATÁLOGO — {len(rows)} produto(s)\n")
    for r in rows:
        mkt = MARKETPLACES.get(r["marketplace"], {}).get("nome", r["marketplace"] or "—")
        print(f"  {r['id']}  {r['nome'] or '[SEM NOME]'}")
        print(f"       categoria: {r['categoria'] or '[A CONFERIR]'} · marca: {r['marca'] or '[A CONFERIR]'} · alvo: {mkt}")
        if r["preco"]:
            print(f"       preço: R$ {r['preco']}")
    print("\nAnúncios já montados: veja `painel` ou `exportar --produto <id> --marketplace <mkt>`.")


def cmd_produto(a):
    row, _ = _find_produto(a.id)
    if not row:
        print(f"⚠️  Produto '{a.id}' não encontrado.")
        sys.exit(2)
    print(f"📦 {row['id']} — {row['nome'] or '[SEM NOME — A CONFERIR]'}\n")
    print(f"  Categoria .... {row['categoria'] or '[A CONFERIR]'}")
    print(f"  Marca ........ {row['marca'] or '[A CONFERIR]'}")
    print(f"  Modelo ....... {row['modelo'] or '—'}")
    print(f"  Público ...... {row['publico'] or '—'}")
    mkt = row["marketplace"]
    print(f"  Marketplace .. {MARKETPLACES.get(mkt, {}).get('nome', mkt or '—')}")
    if row["custo"] or row["preco"]:
        print(f"  Custo/Preço .. R$ {row['custo'] or '?'} / R$ {row['preco'] or '?'}")
    attrs = _parse_attrs(row["atributos"])
    print("\n  Ficha técnica / atributos:")
    if attrs:
        for k, v in attrs:
            print(f"    • {k}: {v or '[A CONFERIR]'}")
    else:
        print("    (nenhum — a ficha técnica é o que mais pesa na busca; peça ao dono)")
    dif = _split_list(row["diferenciais"])
    print("\n  Diferenciais:")
    for d in (dif or ["(nenhum informado)"]):
        print(f"    • {d}")
    kw = _split_list(row["palavras"])
    print("\n  Palavras que o cliente busca:")
    print("    " + (", ".join(kw) if kw else "(nenhuma — peça ao dono como o cliente chama o produto)"))


def cmd_limites(a):
    key = _mkt_or_die(a.marketplace)
    m = MARKETPLACES[key]
    print(f"📐 REGRAS — {m['nome']}\n")
    print(f"  Título ........ máx {m['titulo_max']} caracteres"
          + (f" (recomendado ≤ {m['titulo_rec']})" if m.get("titulo_rec") else ""))
    print(f"  Fórmula ....... {m['titulo_formula']}")
    if m["usa_bullets"]:
        print(f"  Bullets ....... {m['bullets_qtd']} itens, cada um ≤ {m['bullet_max']} caracteres")
    print(f"  Descrição ..... máx {m['descricao_max']} caracteres")
    print(f"  Fotos ......... máx {m['fotos_max']} (recomendado {m['fotos_rec']}+)")
    if m["palavras_slot"]:
        print(f"  Palavras-chave  campo de busca: {m['palavras_slot']} bytes (backend)")
    print(f"  Atributos ..... {m['atributos']}")
    print(f"  ❌ Proibido ... {m['proibido']}")
    print("\n  ⚠️  Plataformas mudam as regras. Confirme sempre na central de ajuda do marketplace.")


def cmd_titulo_check(a):
    key = _mkt_or_die(a.marketplace)
    m = MARKETPLACES[key]
    t = a.texto.strip()
    n = len(t)
    limite = m["titulo_max"]
    print(f"🔎 TÍTULO para {m['nome']} — {n}/{limite} caracteres")
    bar_ok = n <= limite
    print("   " + ("✅ dentro do limite" if bar_ok else f"❌ passou {n - limite} caractere(s) — corte"))
    if m.get("titulo_rec") and n > m["titulo_rec"]:
        print(f"   🟡 acima do recomendado ({m['titulo_rec']}) — o começo do título é o que aparece na busca")
    # heurísticas de qualidade (sem inventar nada)
    avisos = []
    low = _strip_accents(t.lower())
    for bad in ("melhor", "o numero 1", "promocao", "oferta", "frete gratis", "imperdivel", "barato"):
        if bad in low:
            avisos.append(f"remova '{bad}' (marketplaces penalizam / proíbem no título)")
    if any(ch in t for ch in "!*_#") or _has_emoji(t):
        avisos.append("tire emoji e pontuação de efeito (!, *, #) — poluem e podem ser barrados")
    if "  " in t:
        avisos.append("há espaço duplo")
    if avisos:
        print("   Ajustes:")
        for w in avisos:
            print(f"     • {w}")
    print(f"   Fórmula ideal: {m['titulo_formula']}")


def _strip_accents(s):
    return "".join(c for c in unicodedata.normalize("NFD", s)
                   if unicodedata.category(c) != "Mn")


def _has_emoji(s):
    for ch in s:
        if ord(ch) > 0x2600:
            return True
    return False


def cmd_salvar(a):
    """Registra o anúncio pronto que a IA escreveu (arquivo .md) e recalcula a nota."""
    row, _ = _find_produto(a.produto)
    if not row:
        print(f"⚠️  Produto '{a.produto}' não encontrado.")
        sys.exit(2)
    key = _mkt_or_die(a.marketplace)
    if not os.path.exists(a.arquivo):
        print(f"⚠️  Arquivo do anúncio não encontrado: {a.arquivo}")
        sys.exit(2)
    _ensure_dir()
    dest = os.path.join(ANUNCIOS_DIR, f"{row['id']}-{key}.md")
    with open(a.arquivo, encoding="utf-8") as f:
        conteudo = f.read()
    with open(dest, "w", encoding="utf-8") as f:
        f.write(conteudo)
    nota, _det = _scorecard(row, key, conteudo)
    anrows = _read(ANUNCIOS, ANUNCIO_COLS)
    titulo = _extrai_titulo(conteudo)
    existing = next((x for x in anrows if x["produto_id"] == row["id"] and x["marketplace"] == key), None)
    if existing:
        existing.update(titulo=titulo, nota=str(nota), arquivo=dest, atualizado=_now())
    else:
        anrows.append({
            "id": _next_id(anrows, "A"), "produto_id": row["id"], "marketplace": key,
            "titulo": titulo, "nota": str(nota), "arquivo": dest, "atualizado": _now(),
        })
    _write(ANUNCIOS, ANUNCIO_COLS, anrows)
    print(f"✅ Anúncio salvo para {row['nome']} em {MARKETPLACES[key]['nome']} — nota {nota}/100.")
    print(f"   Arquivo: {dest}")
    print("   Rode `nota` para ver o que ainda dá pra melhorar.")


def _extrai_titulo(txt):
    for line in txt.splitlines():
        s = line.strip().lstrip("#").strip()
        low = _strip_accents(s.lower())
        if low.startswith("titulo"):
            return s.split(":", 1)[-1].strip() if ":" in s else s
    for line in txt.splitlines():
        if line.strip():
            return line.strip().lstrip("#").strip()
    return ""


def _scorecard(row, key, conteudo):
    """Checklist de conversão -> nota 0-100. Não julga a qualidade da prosa,
    verifica a ESTRUTURA e as regras do marketplace."""
    m = MARKETPLACES[key]
    low = _strip_accents(conteudo.lower())
    itens = []

    titulo = _extrai_titulo(conteudo)
    itens.append(("Título presente", 15, bool(titulo)))
    itens.append(("Título dentro do limite de caracteres", 15,
                  bool(titulo) and len(titulo) <= m["titulo_max"]))
    itens.append(("Marca no anúncio", 8, bool(row["marca"])))
    itens.append(("Ficha técnica / atributos preenchidos", 15, len(_parse_attrs(row["atributos"])) >= 3))
    if m["usa_bullets"]:
        n_bul = low.count("\n- ") + low.count("\n* ") + low.count("\n• ")
        itens.append((f"{m['bullets_qtd']} bullets de benefício", 12, n_bul >= m["bullets_qtd"]))
    else:
        itens.append(("Descrição com benefícios (não só specs)", 12,
                      any(w in low for w in ("voce", "para voce", "ideal", "perfeito", "ajuda", "beneficio"))))
    itens.append(("Palavras de busca do cliente definidas", 10, len(_split_list(row["palavras"])) >= 3))
    itens.append(("Chamada final / próximo passo (CTA)", 5,
                  any(w in low for w in ("compre", "leve", "garanta", "adicione", "aproveite"))))
    itens.append(("Nada de termo proibido no título", 10,
                  not any(b in _strip_accents(titulo.lower())
                          for b in ("melhor", "promocao", "oferta", "frete gratis", "barato"))))

    total = sum(p for _, p, _ in itens)
    got = sum(p for _, p, ok in itens if ok)
    nota = round(got / total * 100)
    return nota, itens


def cmd_nota(a):
    row, _ = _find_produto(a.produto)
    if not row:
        print(f"⚠️  Produto '{a.produto}' não encontrado.")
        sys.exit(2)
    key = _mkt_or_die(a.marketplace)
    dest = os.path.join(ANUNCIOS_DIR, f"{row['id']}-{key}.md")
    if not os.path.exists(dest):
        print(f"⚠️  Ainda não há anúncio salvo para {row['nome']} em {MARKETPLACES[key]['nome']}.")
        print("   A IA escreve o anúncio, salva com `salvar`, e aí a nota aparece.")
        sys.exit(2)
    conteudo = open(dest, encoding="utf-8").read()
    nota, itens = _scorecard(row, key, conteudo)
    print(f"🏅 NOTA DO ANÚNCIO — {row['nome']} · {MARKETPLACES[key]['nome']}: {nota}/100\n")
    for nome, peso, ok in itens:
        print(f"  {'✅' if ok else '⬜'} {nome}  ({peso} pts)")
    faltas = [n for n, _, ok in itens if not ok]
    if faltas:
        print("\n  Pra subir a nota, resolva: " + "; ".join(faltas) + ".")
    else:
        print("\n  🎉 Anúncio completo pelo checklist. Confira as informações com o dono e publique.")


def cmd_exportar(a):
    row, _ = _find_produto(a.produto)
    if not row:
        print(f"⚠️  Produto '{a.produto}' não encontrado.")
        sys.exit(2)
    key = _mkt_or_die(a.marketplace)
    dest = os.path.join(ANUNCIOS_DIR, f"{row['id']}-{key}.md")
    if not os.path.exists(dest):
        print(f"⚠️  Não há anúncio salvo para {row['nome']} em {MARKETPLACES[key]['nome']}.")
        sys.exit(2)
    print(f"===== ANÚNCIO PRONTO PARA COLAR — {MARKETPLACES[key]['nome']} =====\n")
    print(open(dest, encoding="utf-8").read())
    print("\n===== FIM — confira tudo e publique você mesmo no marketplace =====")


def cmd_painel(_):
    prod = _read(PRODUTOS, PRODUTO_COLS)
    an = _read(ANUNCIOS, ANUNCIO_COLS)
    print("📊 PAINEL DO MOSTRUÁRIO\n")
    print(f"  Produtos no catálogo ... {len(prod)}")
    print(f"  Anúncios montados ...... {len(an)}")
    if an:
        print("\n  Anúncios:")
        for x in sorted(an, key=lambda r: int(r.get("nota") or 0), reverse=True):
            p = next((r for r in prod if r["id"] == x["produto_id"]), {})
            print(f"    {x['produto_id']}  {p.get('nome','?')[:34]:34}  "
                  f"{MARKETPLACES.get(x['marketplace'],{}).get('nome',x['marketplace']):14}  "
                  f"nota {x['nota']}/100")
    faltam = [p["id"] for p in prod if not any(x["produto_id"] == p["id"] for x in an)]
    if faltam:
        print("\n  Sem anúncio ainda: " + ", ".join(faltam))
    print("\n  Ordem sugerida: monte primeiro os produtos que mais vendem / têm mais concorrência.")


# --------------------------------------------------------------------------- #
# CLI
# --------------------------------------------------------------------------- #
def build_parser():
    p = argparse.ArgumentParser(description="Mostruário — anúncios de produto que vendem.")
    sub = p.add_subparsers(dest="cmd", required=True)

    sub.add_parser("init").set_defaults(func=cmd_init)

    a = sub.add_parser("produto-add")
    for opt in ("nome", "categoria", "marca", "modelo", "publico", "marketplace",
                "custo", "preco", "atributos", "diferenciais", "palavras", "notas"):
        a.add_argument(f"--{opt}")
    a.set_defaults(func=cmd_produto_add)

    d = sub.add_parser("definir")
    d.add_argument("--id", required=True)
    d.add_argument("--campo", required=True)
    d.add_argument("--valor", required=True)
    d.set_defaults(func=cmd_definir)

    sub.add_parser("catalogo").set_defaults(func=cmd_catalogo)

    pr = sub.add_parser("produto")
    pr.add_argument("--id", required=True)
    pr.set_defaults(func=cmd_produto)

    li = sub.add_parser("limites")
    li.add_argument("--marketplace", required=True)
    li.set_defaults(func=cmd_limites)

    tc = sub.add_parser("titulo-check")
    tc.add_argument("--texto", required=True)
    tc.add_argument("--marketplace", required=True)
    tc.set_defaults(func=cmd_titulo_check)

    sv = sub.add_parser("salvar")
    sv.add_argument("--produto", required=True)
    sv.add_argument("--marketplace", required=True)
    sv.add_argument("--arquivo", required=True)
    sv.set_defaults(func=cmd_salvar)

    nt = sub.add_parser("nota")
    nt.add_argument("--produto", required=True)
    nt.add_argument("--marketplace", required=True)
    nt.set_defaults(func=cmd_nota)

    ex = sub.add_parser("exportar")
    ex.add_argument("--produto", required=True)
    ex.add_argument("--marketplace", required=True)
    ex.set_defaults(func=cmd_exportar)

    sub.add_parser("painel").set_defaults(func=cmd_painel)
    return p


def main():
    parser = build_parser()
    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
