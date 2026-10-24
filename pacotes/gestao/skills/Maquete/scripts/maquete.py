#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Maquete — motor de design de produto: fluxos, wireframes e protótipo navegável.

Transforma um pedido de software ("quero um app/site/SaaS que faça X") no DESENHO
do produto ANTES de escrever código: as personas, os fluxos de uso (a jornada
tela-a-tela), os wireframes lo-fi de cada tela e — a joia — um PROTÓTIPO HTML
navegável e clicável que o dono abre no navegador, mostra pro cliente e valida com
usuário. No fim, gera um brief de handoff pronto pro build (Gabarito/Estaleiro/
Claude Code) construir a coisa CERTA.

Princípios (travas embutidas):
  - Começa pela TAREFA/fluxo do usuário, não pela tela solta. Toda tela nasce de
    um fluxo; toda ação leva a algum lugar.
  - Fidelidade LO-FI de propósito: wireframe cinza, sem cor/marca, para discutir
    ESTRUTURA e navegação — não "a cor do botão".
  - Nunca inventa conteúdo real: usa rótulos genéricos/placeholder; dado real que
    o dono não deu fica [A CONFERIR], nunca um chute.
  - Sinaliza defeito: tela ÓRFÃ (nenhum fluxo/ação chega nela) e ação QUEBRADA
    (aponta para tela inexistente).
  - A IA desenha e propõe; o DONO valida cada tela. Dados 100% locais (offline).

Sem dependências externas. Só biblioteca padrão. NUNCA acessa a rede.
"""

import sys
import os
import csv
import argparse
import html as _html
import unicodedata
from datetime import datetime, timezone

# ----------------------------------------------------------------------------
# Ancoragem: onde fica a pasta .maquete/ (raiz do projeto)
# ----------------------------------------------------------------------------

def _strip_accents(s):
    if not s:
        return ""
    nfkd = unicodedata.normalize("NFKD", str(s))
    return "".join(c for c in nfkd if not unicodedata.combining(c))

def _norm(s):
    """minúsculo, sem acento, bordas aparadas — para comparação robusta."""
    return _strip_accents(str(s or "")).strip().lower()

def find_project_root():
    """Sobe a árvore procurando um marcador de raiz.
    Preferência: CLAUDE_PROJECT_DIR > pasta que já tem .maquete/ > .git/.claude > cwd."""
    env = os.environ.get("CLAUDE_PROJECT_DIR")
    if env and os.path.isdir(env):
        return os.path.abspath(env)
    cur = os.path.abspath(os.getcwd())
    walk = cur
    while True:
        if os.path.isdir(os.path.join(walk, ".maquete")):
            return walk
        parent = os.path.dirname(walk)
        if parent == walk:
            break
        walk = parent
    walk = cur
    while True:
        if os.path.isdir(os.path.join(walk, ".git")) or os.path.isdir(os.path.join(walk, ".claude")):
            return walk
        parent = os.path.dirname(walk)
        if parent == walk:
            break
        walk = parent
    return cur

ROOT = find_project_root()
MDIR = os.path.join(ROOT, ".maquete")

def mpath(*parts):
    return os.path.join(MDIR, *parts)

def ensure_dir():
    os.makedirs(MDIR, exist_ok=True)

def now_stamp():
    return datetime.now(timezone.utc).astimezone().strftime("%Y-%m-%d %H:%M")

# ----------------------------------------------------------------------------
# Armazenamento CSV (tudo local, sem nuvem)
# ----------------------------------------------------------------------------

FILES = {
    "projeto":    ("projeto.csv",    ["chave", "valor"]),
    "personas":   ("personas.csv",   ["id", "nome", "papel", "objetivo", "contexto"]),
    "fluxos":     ("fluxos.csv",     ["id", "nome", "persona", "objetivo", "telas", "gatilho"]),
    "telas":      ("telas.csv",      ["id", "nome", "tipo", "objetivo", "blocos", "estado", "observacao"]),
}

def _fpath(tabela):
    return mpath(FILES[tabela][0])

def _cols(tabela):
    return FILES[tabela][1]

def read_rows(tabela):
    p = _fpath(tabela)
    if not os.path.exists(p):
        return []
    with open(p, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))

def write_rows(tabela, rows):
    ensure_dir()
    cols = _cols(tabela)
    with open(_fpath(tabela), "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=cols)
        w.writeheader()
        for r in rows:
            w.writerow({c: r.get(c, "") for c in cols})

def append_row(tabela, row):
    rows = read_rows(tabela)
    rows.append(row)
    write_rows(tabela, rows)

def next_id(tabela, prefixo):
    rows = read_rows(tabela)
    n = 0
    for r in rows:
        rid = r.get("id", "")
        if rid.startswith(prefixo + "."):
            try:
                n = max(n, int(rid.split(".")[1]))
            except (ValueError, IndexError):
                pass
    return "%s.%02d" % (prefixo, n + 1)

# projeto.csv é um dicionário chave/valor
def read_projeto():
    d = {}
    for r in read_rows("projeto"):
        d[r.get("chave", "")] = r.get("valor", "")
    return d

def write_projeto(d):
    write_rows("projeto", [{"chave": k, "valor": v} for k, v in d.items()])

# ----------------------------------------------------------------------------
# DSL de blocos — o vocabulário lo-fi que descreve uma tela
# ----------------------------------------------------------------------------
# Cada bloco fica numa linha. Formato:  tipo: conteúdo   (ação usa  -> T.xx)
# Tipos: titulo, subtitulo, texto, campo, area, selecao, botao, link, lista,
#        tabela, card, imagem, abas, nav, metrica, aviso, espaco
# Ações (botao/link/nav/abas) podem apontar destino com  -> T.xx
# Ex.:  botao: Entrar -> T.02        link: Esqueci a senha -> T.09
#       nav: Início -> T.02, Perfil -> T.05
BLOCOS_VALIDOS = {
    "titulo", "subtitulo", "texto", "campo", "area", "selecao", "botao",
    "link", "lista", "tabela", "card", "imagem", "abas", "nav", "metrica",
    "aviso", "espaco",
}

def _split_blocos(raw):
    """Divide o campo de blocos em linhas (aceita quebra real ou ' || ')."""
    if not raw:
        return []
    raw = raw.replace(" || ", "\n").replace("||", "\n")
    linhas = [ln.strip() for ln in raw.splitlines()]
    return [ln for ln in linhas if ln]

def parse_bloco(linha):
    """Retorna (tipo, conteudo, destino_ou_None). Blocos desconhecidos viram texto."""
    if ":" in linha:
        tipo, conteudo = linha.split(":", 1)
        tipo = _norm(tipo)
        conteudo = conteudo.strip()
    else:
        tipo, conteudo = "texto", linha.strip()
    if tipo not in BLOCOS_VALIDOS:
        # tolerante: trata como texto para não quebrar o desenho
        conteudo = linha.strip()
        tipo = "texto"
    destino = None
    if "->" in conteudo:
        conteudo, destino = conteudo.rsplit("->", 1)
        conteudo = conteudo.strip()
        destino = destino.strip().upper()
    return tipo, conteudo, destino

def blocos_da_tela(tela):
    return [parse_bloco(ln) for ln in _split_blocos(tela.get("blocos", ""))]

def destinos_da_tela(tela):
    """Todos os T.xx que os botões/links/nav/abas desta tela apontam."""
    dests = []
    for _, conteudo, destino in blocos_da_tela(tela):
        if destino:
            dests.append(destino)
        # nav/abas podem ter múltiplos "item -> T.xx" separados por vírgula
    # varre também itens de nav/abas com vírgulas
    for tipo, conteudo, destino in blocos_da_tela(tela):
        if tipo in ("nav", "abas"):
            for item in conteudo.split(","):
                if "->" in item:
                    dests.append(item.rsplit("->", 1)[1].strip().upper())
    return [d for d in dests if d]

# ----------------------------------------------------------------------------
# Diagnóstico: telas órfãs, ações quebradas, becos-sem-saída
# ----------------------------------------------------------------------------

def _ids_telas():
    return [t["id"] for t in read_rows("telas")]

def diagnostico():
    telas = read_rows("telas")
    fluxos = read_rows("fluxos")
    ids = set(t["id"] for t in telas)

    # telas que são início de algum fluxo
    inicios = set()
    for f in fluxos:
        seq = [s.strip().upper() for s in (f.get("telas", "") or "").split(",") if s.strip()]
        if seq:
            inicios.add(seq[0])

    # telas alcançadas por ação de outra tela OU citadas em algum fluxo
    alcancadas = set(inicios)
    quebradas = []   # (tela_origem, destino_inexistente)
    for t in telas:
        for tipo, conteudo, destino in [(a, b, c) for (a, b, c) in _acoes_expandidas(t)]:
            if destino:
                if destino in ids:
                    alcancadas.add(destino)
                else:
                    quebradas.append((t["id"], destino, conteudo))
    for f in fluxos:
        for s in (f.get("telas", "") or "").split(","):
            s = s.strip().upper()
            if s:
                alcancadas.add(s)

    orfas = [t for t in telas if t["id"] not in alcancadas]
    # beco-sem-saída: tela sem nenhuma ação de navegação para fora
    becos = []
    for t in telas:
        tem_saida = any(d for (_, _, d) in _acoes_expandidas(t))
        if not tem_saida:
            becos.append(t)
    return {"orfas": orfas, "quebradas": quebradas, "becos": becos,
            "telas": telas, "fluxos": fluxos}

def _acoes_expandidas(tela):
    """Lista (tipo, rótulo, destino) de toda ação navegável da tela (inclui itens de nav/abas)."""
    out = []
    for tipo, conteudo, destino in blocos_da_tela(tela):
        if tipo in ("botao", "link") and destino:
            out.append((tipo, conteudo, destino))
        elif tipo in ("nav", "abas"):
            for item in conteudo.split(","):
                item = item.strip()
                if "->" in item:
                    rot, dst = item.rsplit("->", 1)
                    out.append((tipo, rot.strip(), dst.strip().upper()))
                elif item:
                    out.append((tipo, item, None))
    return out

# ----------------------------------------------------------------------------
# Utilidades de saída
# ----------------------------------------------------------------------------

def esc(t):
    return _html.escape(str(t or ""))

def _proximo_arquivo(prefixo, ext):
    ensure_dir()
    n = 1
    while os.path.exists(mpath("%s-%d.%s" % (prefixo, n, ext))):
        n += 1
    return mpath("%s-%d.%s" % (prefixo, n, ext))

def _tela_por_id(tid):
    for t in read_rows("telas"):
        if t["id"].upper() == tid.upper():
            return t
    return None

# ============================================================================
# COMANDOS
# ============================================================================

def cmd_init(args):
    ensure_dir()
    for tabela in FILES:
        if not os.path.exists(_fpath(tabela)):
            write_rows(tabela, [])
    if not read_projeto():
        write_projeto({
            "nome": "[A CONFERIR]", "para_quem": "[A CONFERIR]",
            "plataforma": "web", "problema": "[A CONFERIR]",
            "tom_visual": "limpo e simples", "criado_em": now_stamp(),
        })
    print("✓ Maquete iniciada em .maquete/")

def cmd_novo(args):
    ensure_dir()
    cmd_init(args)
    d = read_projeto()
    if args.nome:      d["nome"] = args.nome
    if args.para:      d["para_quem"] = args.para
    if args.plataforma: d["plataforma"] = _norm(args.plataforma) or "web"
    if args.problema:  d["problema"] = args.problema
    if args.tom:       d["tom_visual"] = args.tom
    write_projeto(d)
    print("✓ Produto enquadrado.")
    _print_projeto(d)

def _print_projeto(d):
    print("  Produto:    %s" % d.get("nome", ""))
    print("  Para quem:  %s" % d.get("para_quem", ""))
    print("  Plataforma: %s" % d.get("plataforma", ""))
    print("  Problema:   %s" % d.get("problema", ""))

def cmd_projeto(args):
    d = read_projeto()
    if not d:
        print("Nenhum produto enquadrado ainda. Use: novo --nome ...")
        return
    _print_projeto(d)

# --- personas ---
def cmd_persona_add(args):
    pid = next_id("personas", "P")
    append_row("personas", {
        "id": pid, "nome": args.nome or "[A CONFERIR]",
        "papel": args.papel or "", "objetivo": args.objetivo or "",
        "contexto": args.contexto or "",
    })
    print("✓ Persona %s: %s" % (pid, args.nome or "[A CONFERIR]"))

def cmd_personas(args):
    rows = read_rows("personas")
    if not rows:
        print("Nenhuma persona ainda. Quem vai USAR o produto?")
        return
    for r in rows:
        print("  %s  %s — %s" % (r["id"], r["nome"], r.get("objetivo", "")))

# --- fluxos ---
def cmd_fluxo_add(args):
    fid = next_id("fluxos", "F")
    telas = ",".join(s.strip().upper() for s in (args.telas or "").split(",") if s.strip())
    append_row("fluxos", {
        "id": fid, "nome": args.nome or "[A CONFERIR]",
        "persona": (args.persona or "").upper(), "objetivo": args.objetivo or "",
        "telas": telas, "gatilho": args.gatilho or "",
    })
    print("✓ Fluxo %s: %s" % (fid, args.nome or "[A CONFERIR]"))
    if telas:
        print("  Jornada: %s" % " → ".join(telas.split(",")))

def cmd_fluxo_set(args):
    rows = read_rows("fluxos")
    for r in rows:
        if r["id"].upper() == (args.id or "").upper():
            if args.telas is not None:
                r["telas"] = ",".join(s.strip().upper() for s in args.telas.split(",") if s.strip())
            if args.nome:     r["nome"] = args.nome
            if args.objetivo: r["objetivo"] = args.objetivo
            if args.gatilho:  r["gatilho"] = args.gatilho
            if args.persona:  r["persona"] = args.persona.upper()
            write_rows("fluxos", rows)
            print("✓ Fluxo %s atualizado." % r["id"])
            return
    print("Fluxo %s não encontrado." % args.id)

def cmd_fluxos(args):
    rows = read_rows("fluxos")
    if not rows:
        print("Nenhum fluxo ainda. Qual a primeira TAREFA que o usuário quer cumprir?")
        return
    telas = {t["id"]: t["nome"] for t in read_rows("telas")}
    for r in rows:
        seq = [s for s in (r.get("telas", "") or "").split(",") if s]
        jornada = " → ".join("%s(%s)" % (s, telas.get(s, "?")) for s in seq) if seq else "(sem telas)"
        print("  %s  %s" % (r["id"], r["nome"]))
        print("       %s" % jornada)

# --- telas ---
def cmd_tela_add(args):
    tid = next_id("telas", "T")
    blocos = args.blocos or ""
    append_row("telas", {
        "id": tid, "nome": args.nome or "[A CONFERIR]",
        "tipo": _norm(args.tipo) or "", "objetivo": args.objetivo or "",
        "blocos": blocos, "estado": args.estado or "normal",
        "observacao": args.observacao or "",
    })
    print("✓ Tela %s: %s (%s)" % (tid, args.nome or "[A CONFERIR]", args.tipo or "—"))

def cmd_tela_set(args):
    rows = read_rows("telas")
    for r in rows:
        if r["id"].upper() == (args.id or "").upper():
            if args.nome:      r["nome"] = args.nome
            if args.tipo:      r["tipo"] = _norm(args.tipo)
            if args.objetivo:  r["objetivo"] = args.objetivo
            if args.blocos is not None: r["blocos"] = args.blocos
            if args.estado:    r["estado"] = args.estado
            if args.observacao: r["observacao"] = args.observacao
            write_rows("telas", rows)
            print("✓ Tela %s atualizada." % r["id"])
            return
    print("Tela %s não encontrada." % args.id)

def cmd_telas(args):
    rows = read_rows("telas")
    if not rows:
        print("Nenhuma tela ainda. Desenhe o fluxo primeiro, depois as telas dele.")
        return
    diag = diagnostico()
    orfas = set(t["id"] for t in diag["orfas"])
    for r in rows:
        marca = "  ⚠ órfã" if r["id"] in orfas else ""
        print("  %s  %s [%s]%s" % (r["id"], r["nome"], r.get("tipo", "—"), marca))

def cmd_tela(args):
    t = _tela_por_id(args.id or "")
    if not t:
        print("Tela %s não encontrada." % args.id)
        return
    print("%s — %s [%s]" % (t["id"], t["nome"], t.get("tipo", "—")))
    print("Objetivo: %s" % t.get("objetivo", ""))
    print("Estado:   %s" % t.get("estado", "normal"))
    print("Blocos:")
    for tipo, conteudo, destino in blocos_da_tela(t):
        seta = "  → %s" % destino if destino else ""
        print("  • %-9s %s%s" % (tipo, conteudo, seta))

# --- mapa de navegação ---
def cmd_mapa(args):
    diag = diagnostico()
    telas = diag["telas"]
    if not telas:
        print("Sem telas para mapear.")
        return
    nomes = {t["id"]: t["nome"] for t in telas}
    print("MAPA DE NAVEGAÇÃO")
    print("=================")
    for t in telas:
        acoes = _acoes_expandidas(t)
        saidas = [d for (_, _, d) in acoes if d]
        if saidas:
            for tipo, rot, dst in acoes:
                if dst:
                    alvo = "%s(%s)" % (dst, nomes.get(dst, "?"))
                    print("  %s(%s) --[%s]--> %s" % (t["id"], t["nome"], rot, alvo))
        else:
            print("  %s(%s)  (sem saída)" % (t["id"], t["nome"]))
    print()
    _print_alertas(diag)

def _print_alertas(diag):
    if diag["orfas"]:
        print("⚠ TELAS ÓRFÃS (ninguém chega nelas — falta um fluxo ou uma ação):")
        for t in diag["orfas"]:
            print("   %s %s" % (t["id"], t["nome"]))
    if diag["quebradas"]:
        print("⚠ AÇÕES QUEBRADAS (o botão aponta para uma tela que não existe):")
        for origem, destino, rot in diag["quebradas"]:
            print("   %s '%s' → %s (inexistente)" % (origem, rot, destino))
    if diag["becos"]:
        print("• Becos-sem-saída (tela sem nenhum botão de navegação — ok se for tela final):")
        for t in diag["becos"]:
            print("   %s %s" % (t["id"], t["nome"]))
    if not (diag["orfas"] or diag["quebradas"]):
        print("✓ Navegação íntegra: nenhuma tela órfã, nenhuma ação quebrada.")

# --- painel ---
def cmd_painel(args):
    d = read_projeto()
    diag = diagnostico()
    print("PAINEL DA MAQUETE — %s" % d.get("nome", "(produto sem nome)"))
    print("=" * 46)
    print("Plataforma: %s   |   Problema: %s" % (d.get("plataforma", "?"), d.get("problema", "?")))
    print("Personas:   %d" % len(read_rows("personas")))
    print("Fluxos:     %d" % len(diag["fluxos"]))
    print("Telas:      %d" % len(diag["telas"]))
    print("-" * 46)
    _print_alertas(diag)
    print("-" * 46)
    print("Prontidão:", _veredito(d, diag))

def _veredito(d, diag):
    faltas = []
    if _norm(d.get("nome")) in ("", "[a conferir]"): faltas.append("nome do produto")
    if _norm(d.get("problema")) in ("", "[a conferir]"): faltas.append("problema central")
    if not diag["fluxos"]: faltas.append("nenhum fluxo desenhado")
    if not diag["telas"]:  faltas.append("nenhuma tela")
    if diag["quebradas"]:  faltas.append("%d ação(ões) quebrada(s)" % len(diag["quebradas"]))
    if diag["orfas"]:      faltas.append("%d tela(s) órfã(s)" % len(diag["orfas"]))
    if not faltas:
        return "🟢 pronta para virar protótipo e ir pro build"
    graves = [f for f in faltas if "quebrada" in f or "nenhum" in f or "central" in f]
    cor = "🔴" if graves else "🟡"
    return "%s falta: %s" % (cor, "; ".join(faltas))

def cmd_plano(args):
    d = read_projeto()
    diag = diagnostico()
    print("O QUE FECHAR ANTES DE CONSIDERAR O DESIGN PRONTO")
    print("================================================")
    itens = []
    if _norm(d.get("problema")) in ("", "[a conferir]"):
        itens.append(("🔴", "Definir o problema central que o produto resolve"))
    if not diag["fluxos"]:
        itens.append(("🔴", "Desenhar ao menos o fluxo principal (a tarefa nº 1 do usuário)"))
    for origem, destino, rot in diag["quebradas"]:
        itens.append(("🔴", "Corrigir ação quebrada em %s ('%s' → %s inexistente)" % (origem, rot, destino)))
    for t in diag["orfas"]:
        itens.append(("🟡", "Ligar a tela órfã %s (%s) a um fluxo ou a uma ação" % (t["id"], t["nome"])))
    if not read_rows("personas"):
        itens.append(("🟡", "Registrar ao menos uma persona (quem usa e para quê)"))
    # ordena 🔴 antes de 🟡
    itens.sort(key=lambda x: 0 if x[0] == "🔴" else 1)
    if not itens:
        print("✓ Nada pendente — gere o protótipo (prototipo) e o brief (entregar).")
        return
    for cor, txt in itens:
        print("  %s %s" % (cor, txt))

# ----------------------------------------------------------------------------
# WIREFRAMES (documento lo-fi tela-a-tela em Markdown)
# ----------------------------------------------------------------------------

def _wire_ascii(tela):
    """Desenho lo-fi em texto de uma tela (honesto: só estrutura)."""
    L = []
    W = 44
    L.append("┌" + "─" * W + "┐")
    def linha(txt=""):
        txt = str(txt)[:W]
        L.append("│" + txt.ljust(W) + "│")
    for tipo, conteudo, destino in blocos_da_tela(tela):
        seta = " →%s" % destino if destino else ""
        if tipo == "titulo":
            linha(" ▛ %s" % conteudo)
            linha(" " + "─" * (W - 2))
        elif tipo == "subtitulo":
            linha(" %s" % conteudo)
        elif tipo == "texto":
            linha(" %s" % conteudo)
        elif tipo == "campo":
            linha(" %s:" % conteudo)
            linha(" [____________________________]")
        elif tipo == "area":
            linha(" %s:" % conteudo)
            linha(" [                            ]")
            linha(" [____________________________]")
        elif tipo == "selecao":
            linha(" %s: [ selecione ▾ ]" % conteudo)
        elif tipo == "botao":
            linha(" ( %s )%s" % (conteudo, seta))
        elif tipo == "link":
            linha(" _%s_%s" % (conteudo, seta))
        elif tipo == "lista":
            for it in conteudo.split(","):
                linha("  • %s" % it.strip())
        elif tipo == "tabela":
            cols = " | ".join(c.strip() for c in conteudo.split(","))
            linha(" ┆ %s" % cols)
            linha(" ┆ ---------------------------")
            linha(" ┆ ...")
        elif tipo == "card":
            linha(" ┏━ %s" % conteudo.replace("|", "—"))
        elif tipo == "imagem":
            linha(" [ ▨ imagem: %s ]" % conteudo)
        elif tipo == "abas":
            linha(" | %s |" % " | ".join(a.split("->")[0].strip() for a in conteudo.split(",")))
        elif tipo == "nav":
            itens = [a.split("->")[0].strip() for a in conteudo.split(",")]
            linha(" " + "  ".join(itens))
        elif tipo == "metrica":
            partes = conteudo.split("|")
            rot = partes[0].strip()
            val = partes[1].strip() if len(partes) > 1 else "[valor]"
            linha(" ▮ %s: %s" % (rot, val))
        elif tipo == "aviso":
            linha(" ⚠ %s" % conteudo)
        elif tipo == "espaco":
            linha("")
    L.append("└" + "─" * W + "┘")
    return "\n".join(L)

def cmd_wireframes(args):
    telas = read_rows("telas")
    d = read_projeto()
    if not telas:
        print("Sem telas para desenhar. Crie telas primeiro.")
        return
    out = _proximo_arquivo("wireframes", "md")
    diag = diagnostico()
    orfas = set(t["id"] for t in diag["orfas"])
    with open(out, "w", encoding="utf-8") as f:
        f.write("# Wireframes — %s\n\n" % d.get("nome", "produto"))
        f.write("_Fidelidade lo-fi (só estrutura). Gerado em %s._\n\n" % now_stamp())
        for t in telas:
            marca = " ⚠ (órfã)" if t["id"] in orfas else ""
            f.write("## %s — %s%s\n" % (t["id"], t["nome"], marca))
            f.write("**Tipo:** %s  |  **Objetivo:** %s  |  **Estado:** %s\n\n"
                    % (t.get("tipo", "—"), t.get("objetivo", "—"), t.get("estado", "normal")))
            f.write("```\n" + _wire_ascii(t) + "\n```\n\n")
            acoes = [(rot, dst) for (_, rot, dst) in _acoes_expandidas(t) if dst]
            if acoes:
                f.write("**Vai para:** " + ", ".join("%s → %s" % (r, dst) for r, dst in acoes) + "\n\n")
    print("✓ Wireframes gerados: %s" % out)

# ----------------------------------------------------------------------------
# PROTÓTIPO HTML NAVEGÁVEL (o coração)
# ----------------------------------------------------------------------------

def _bloco_html(tipo, conteudo, destino):
    c = esc(conteudo)
    if tipo == "titulo":
        return '<div class="wf-titulo">%s</div>' % c
    if tipo == "subtitulo":
        return '<div class="wf-subtitulo">%s</div>' % c
    if tipo == "texto":
        return '<p class="wf-texto">%s</p>' % (c or "&nbsp;")
    if tipo == "campo":
        return '<label class="wf-label">%s</label><div class="wf-input"></div>' % c
    if tipo == "area":
        return '<label class="wf-label">%s</label><div class="wf-input wf-area"></div>' % c
    if tipo == "selecao":
        return '<label class="wf-label">%s</label><div class="wf-input wf-select">selecione ▾</div>' % c
    if tipo == "botao":
        attr = ' data-goto="%s"' % esc(destino) if destino else ""
        cls = "wf-botao" + ("" if destino else " wf-botao-morto")
        return '<button class="%s"%s>%s</button>' % (cls, attr, c or "Botão")
    if tipo == "link":
        attr = ' data-goto="%s"' % esc(destino) if destino else ""
        return '<a class="wf-link" href="#"%s>%s</a>' % (attr, c or "link")
    if tipo == "lista":
        itens = "".join("<li>%s</li>" % esc(i.strip()) for i in conteudo.split(",") if i.strip())
        return '<ul class="wf-lista">%s</ul>' % itens
    if tipo == "tabela":
        cols = [esc(x.strip()) for x in conteudo.split(",") if x.strip()]
        th = "".join("<th>%s</th>" % x for x in cols)
        linhas = ""
        for _ in range(3):
            linhas += "<tr>" + "".join('<td><span class="wf-skel"></span></td>' for _ in cols) + "</tr>"
        return '<table class="wf-tabela"><thead><tr>%s</tr></thead><tbody>%s</tbody></table>' % (th, linhas)
    if tipo == "card":
        partes = conteudo.split("|")
        titulo = esc(partes[0].strip())
        corpo = esc(partes[1].strip()) if len(partes) > 1 else ""
        return '<div class="wf-card"><div class="wf-card-t">%s</div><div class="wf-card-b">%s</div></div>' % (titulo, corpo)
    if tipo == "imagem":
        return '<div class="wf-img"><span>▨ %s</span></div>' % (c or "imagem")
    if tipo == "abas":
        abas = []
        for a in conteudo.split(","):
            rot = a.split("->")[0].strip()
            dst = a.rsplit("->", 1)[1].strip().upper() if "->" in a else ""
            attr = ' data-goto="%s"' % esc(dst) if dst else ""
            abas.append('<span class="wf-aba"%s>%s</span>' % (attr, esc(rot)))
        return '<div class="wf-abas">%s</div>' % "".join(abas)
    if tipo == "nav":
        itens = []
        for a in conteudo.split(","):
            rot = a.split("->")[0].strip()
            dst = a.rsplit("->", 1)[1].strip().upper() if "->" in a else ""
            attr = ' data-goto="%s"' % esc(dst) if dst else ""
            itens.append('<span class="wf-navitem"%s>%s</span>' % (attr, esc(rot)))
        return '<nav class="wf-nav">%s</nav>' % "".join(itens)
    if tipo == "metrica":
        partes = conteudo.split("|")
        rot = esc(partes[0].strip())
        val = esc(partes[1].strip()) if len(partes) > 1 else "[valor]"
        return '<div class="wf-metrica"><div class="wf-metrica-v">%s</div><div class="wf-metrica-r">%s</div></div>' % (val, rot)
    if tipo == "aviso":
        return '<div class="wf-aviso">⚠ %s</div>' % c
    if tipo == "espaco":
        return '<div class="wf-espaco"></div>'
    return '<p class="wf-texto">%s</p>' % c

def _tela_frame_html(tela, plataforma, is_start):
    corpo = "".join(_bloco_html(tp, ct, ds) for (tp, ct, ds) in blocos_da_tela(tela))
    if not corpo:
        corpo = '<p class="wf-texto wf-vazio">[tela ainda sem blocos — descreva o que aparece aqui]</p>'
    estado = tela.get("estado", "normal")
    badge_estado = "" if estado in ("", "normal") else '<div class="wf-estado">estado: %s</div>' % esc(estado)
    hidden = "" if is_start else ' hidden'
    return ('<section class="tela" data-id="%s" data-nome="%s"%s>'
            '<div class="tela-head"><span class="tela-id">%s</span>'
            '<span class="tela-nome">%s</span>'
            '<span class="tela-tipo">%s</span></div>'
            '%s<div class="tela-corpo">%s</div></section>') % (
        esc(tela["id"]), esc(tela["nome"]), hidden,
        esc(tela["id"]), esc(tela["nome"]), esc(tela.get("tipo", "")),
        badge_estado, corpo)

def cmd_prototipo(args):
    d = read_projeto()
    telas = read_rows("telas")
    fluxos = read_rows("fluxos")
    if not telas:
        print("Sem telas — não há o que prototipar. Desenhe as telas dos fluxos primeiro.")
        return
    plataforma = _norm(d.get("plataforma", "web")) or "web"

    # tela inicial: início do primeiro fluxo, senão a primeira tela
    start = telas[0]["id"]
    if fluxos:
        seq = [s.strip().upper() for s in (fluxos[0].get("telas", "") or "").split(",") if s.strip()]
        if seq:
            start = seq[0]

    frames = "\n".join(_tela_frame_html(t, plataforma, t["id"].upper() == start.upper()) for t in telas)

    # lista lateral de telas
    itens_telas = "".join(
        '<li data-goto="%s"><b>%s</b> %s</li>' % (esc(t["id"]), esc(t["id"]), esc(t["nome"]))
        for t in telas)

    # fluxos (para o modo passo-a-passo)
    fluxos_js = []
    itens_fluxos = ""
    for f in fluxos:
        seq = [s.strip().upper() for s in (f.get("telas", "") or "").split(",") if s.strip()]
        seq = [s for s in seq if _tela_por_id(s)]  # só telas que existem
        if not seq:
            continue
        fluxos_js.append("{nome:%s, telas:%s}" % (_js_str(f["nome"]), _js_list(seq)))
        itens_fluxos += '<li data-fluxo="%d">▸ %s <span class="pass">%d telas</span></li>' % (
            len(fluxos_js) - 1, esc(f["nome"]), len(seq))
    if not itens_fluxos:
        itens_fluxos = '<li class="vazio">nenhum fluxo desenhado ainda</li>'

    diag = diagnostico()
    n_alertas = len(diag["orfas"]) + len(diag["quebradas"])
    aviso_qualidade = ""
    if n_alertas:
        partes = []
        if diag["orfas"]:
            partes.append("%d tela(s) órfã(s)" % len(diag["orfas"]))
        if diag["quebradas"]:
            partes.append("%d ação(ões) sem destino" % len(diag["quebradas"]))
        aviso_qualidade = " · ⚠ " + ", ".join(partes)

    html_out = PROTOTIPO_TEMPLATE
    html_out = html_out.replace("{{PRODUTO}}", esc(d.get("nome", "Produto")))
    html_out = html_out.replace("{{PARAQUEM}}", esc(d.get("para_quem", "")))
    html_out = html_out.replace("{{PLATAFORMA}}", esc(plataforma))
    html_out = html_out.replace("{{FRAME_CLASS}}", "frame-" + (plataforma if plataforma in ("web", "mobile", "desktop") else "web"))
    html_out = html_out.replace("{{TELA_INICIAL}}", esc(start))
    html_out = html_out.replace("{{ITENS_TELAS}}", itens_telas)
    html_out = html_out.replace("{{ITENS_FLUXOS}}", itens_fluxos)
    html_out = html_out.replace("{{FRAMES}}", frames)
    html_out = html_out.replace("{{FLUXOS_JS}}", "[" + ",".join(fluxos_js) + "]")
    html_out = html_out.replace("{{AVISO_QUALIDADE}}", aviso_qualidade)
    html_out = html_out.replace("{{GERADO}}", esc(now_stamp()))

    out = _proximo_arquivo("prototipo", "html")
    with open(out, "w", encoding="utf-8") as f:
        f.write(html_out)
    print("✓ Protótipo navegável gerado: %s" % out)
    print("  Abra esse arquivo no navegador (duplo-clique) para clicar pelas telas.")
    if n_alertas:
        print("  Atenção%s — rode 'mapa' para ver os detalhes." % aviso_qualidade)

def _js_str(s):
    return '"' + str(s or "").replace("\\", "\\\\").replace('"', '\\"') + '"'

def _js_list(lst):
    return "[" + ",".join(_js_str(x) for x in lst) + "]"

# ----------------------------------------------------------------------------
# BRIEF DE CONSTRUÇÃO (handoff pro build)
# ----------------------------------------------------------------------------

def cmd_entregar(args):
    d = read_projeto()
    telas = read_rows("telas")
    fluxos = read_rows("fluxos")
    personas = read_rows("personas")
    if not telas:
        print("Sem telas — desenhe o produto antes de gerar o brief.")
        return
    out = _proximo_arquivo("brief-de-construcao", "md")
    diag = diagnostico()
    with open(out, "w", encoding="utf-8") as f:
        f.write("# Brief de construção — %s\n\n" % d.get("nome", "produto"))
        f.write("_Handoff do design para o build (Gabarito/Estaleiro/Claude Code). Gerado em %s._\n\n" % now_stamp())
        f.write("## O produto\n")
        f.write("- **Nome:** %s\n- **Para quem:** %s\n- **Plataforma:** %s\n- **Problema que resolve:** %s\n- **Tom visual:** %s\n\n"
                % (d.get("nome", ""), d.get("para_quem", ""), d.get("plataforma", ""),
                   d.get("problema", ""), d.get("tom_visual", "")))
        if personas:
            f.write("## Quem usa\n")
            for p in personas:
                f.write("- **%s** (%s) — quer: %s%s\n" % (
                    p["nome"], p.get("papel", ""), p.get("objetivo", ""),
                    ("  · contexto: " + p["contexto"]) if p.get("contexto") else ""))
            f.write("\n")
        if fluxos:
            f.write("## Fluxos (a ordem em que as telas acontecem)\n")
            nomes = {t["id"]: t["nome"] for t in telas}
            for fl in fluxos:
                seq = [s for s in (fl.get("telas", "") or "").split(",") if s]
                jornada = " → ".join("%s (%s)" % (s, nomes.get(s, "?")) for s in seq)
                f.write("- **%s** — %s\n  - Gatilho: %s\n  - Jornada: %s\n" % (
                    fl["nome"], fl.get("objetivo", ""), fl.get("gatilho", "—"), jornada or "—"))
            f.write("\n")
        f.write("## Telas (o que cada uma precisa)\n")
        for t in telas:
            f.write("### %s — %s [%s]\n" % (t["id"], t["nome"], t.get("tipo", "—")))
            f.write("- **Objetivo:** %s\n" % t.get("objetivo", "—"))
            if t.get("estado") and t["estado"] != "normal":
                f.write("- **Estado especial:** %s\n" % t["estado"])
            blocos = blocos_da_tela(t)
            campos = [c for (tp, c, _) in blocos if tp in ("campo", "area", "selecao")]
            if campos:
                f.write("- **Dados que entram:** %s\n" % ", ".join(campos))
            acoes = [(rot, dst) for (_, rot, dst) in _acoes_expandidas(t) if dst]
            if acoes:
                f.write("- **Ações:** %s\n" % "; ".join("'%s' leva a %s" % (r, dst) for r, dst in acoes))
            f.write("\n")
        f.write("## Pendências do design (fechar no build)\n")
        pend = []
        for origem, destino, rot in diag["quebradas"]:
            pend.append("Ação quebrada: %s '%s' → %s inexistente" % (origem, rot, destino))
        for t in diag["orfas"]:
            pend.append("Tela órfã: %s (%s) — decidir por onde se chega nela" % (t["id"], t["nome"]))
        # [A CONFERIR] espalhados
        conferir = [t["id"] for t in telas if "[A CONFERIR]" in (t.get("nome", "") + t.get("objetivo", ""))]
        if conferir:
            pend.append("Telas com [A CONFERIR]: %s" % ", ".join(conferir))
        if not pend:
            f.write("- Nenhuma — design íntegro e pronto para construir.\n")
        else:
            for p in pend:
                f.write("- %s\n" % p)
    print("✓ Brief de construção gerado: %s" % out)

# ----------------------------------------------------------------------------
# Roteador de comandos
# ----------------------------------------------------------------------------

def build_parser():
    ap = argparse.ArgumentParser(description="Maquete — design de produto: fluxos, wireframes e protótipo navegável.")
    sub = ap.add_subparsers(dest="cmd")

    sub.add_parser("init")

    p = sub.add_parser("novo")
    p.add_argument("--nome"); p.add_argument("--para"); p.add_argument("--plataforma")
    p.add_argument("--problema"); p.add_argument("--tom")

    sub.add_parser("projeto")

    p = sub.add_parser("persona-add")
    p.add_argument("--nome"); p.add_argument("--papel"); p.add_argument("--objetivo"); p.add_argument("--contexto")
    sub.add_parser("personas")

    p = sub.add_parser("fluxo-add")
    p.add_argument("--nome"); p.add_argument("--persona"); p.add_argument("--objetivo")
    p.add_argument("--telas"); p.add_argument("--gatilho")
    p = sub.add_parser("fluxo-set")
    p.add_argument("--id", required=True); p.add_argument("--nome"); p.add_argument("--persona")
    p.add_argument("--objetivo"); p.add_argument("--telas"); p.add_argument("--gatilho")
    sub.add_parser("fluxos")

    p = sub.add_parser("tela-add")
    p.add_argument("--nome"); p.add_argument("--tipo"); p.add_argument("--objetivo")
    p.add_argument("--blocos"); p.add_argument("--estado"); p.add_argument("--observacao")
    p = sub.add_parser("tela-set")
    p.add_argument("--id", required=True); p.add_argument("--nome"); p.add_argument("--tipo")
    p.add_argument("--objetivo"); p.add_argument("--blocos"); p.add_argument("--estado"); p.add_argument("--observacao")
    sub.add_parser("telas")
    p = sub.add_parser("tela"); p.add_argument("--id", required=True)

    sub.add_parser("mapa")
    sub.add_parser("wireframes")
    sub.add_parser("prototipo")
    sub.add_parser("entregar")
    sub.add_parser("painel")
    sub.add_parser("plano")
    return ap

DISPATCH = {
    "init": cmd_init, "novo": cmd_novo, "projeto": cmd_projeto,
    "persona-add": cmd_persona_add, "personas": cmd_personas,
    "fluxo-add": cmd_fluxo_add, "fluxo-set": cmd_fluxo_set, "fluxos": cmd_fluxos,
    "tela-add": cmd_tela_add, "tela-set": cmd_tela_set, "telas": cmd_telas, "tela": cmd_tela,
    "mapa": cmd_mapa, "wireframes": cmd_wireframes, "prototipo": cmd_prototipo,
    "entregar": cmd_entregar, "painel": cmd_painel, "plano": cmd_plano,
}

def main():
    ap = build_parser()
    args = ap.parse_args()
    if not args.cmd:
        ap.print_help()
        return
    DISPATCH[args.cmd](args)

# ----------------------------------------------------------------------------
# Template do protótipo (self-contained, offline, lo-fi, navegável)
# ----------------------------------------------------------------------------

PROTOTIPO_TEMPLATE = r"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Maquete — {{PRODUTO}}</title>
<style>
  :root{
    --tinta:#2b2b2b; --papel:#f4f4f2; --linha:#c9c9c6; --linha2:#dededb;
    --skel:#d9d9d6; --skel2:#e6e6e3; --acao:#6b6b6b; --barra:#1f1f1f; --nota:#8a8a86;
  }
  *{box-sizing:border-box}
  body{margin:0;font:14px/1.5 -apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Helvetica,Arial,sans-serif;
       color:var(--tinta);background:#e8e8e5;display:flex;height:100vh;overflow:hidden}
  /* ---- Painel lateral ---- */
  aside{width:250px;min-width:250px;background:var(--barra);color:#e7e7e4;display:flex;flex-direction:column;height:100vh}
  aside .marca{padding:16px 16px 12px;border-bottom:1px solid #3a3a3a}
  aside .marca b{font-size:15px;letter-spacing:.2px}
  aside .marca small{display:block;color:#9a9a96;margin-top:3px;font-size:11px}
  aside h4{margin:14px 16px 6px;font-size:10.5px;text-transform:uppercase;letter-spacing:1px;color:#8a8a86;font-weight:700}
  aside ul{list-style:none;margin:0;padding:0 8px;overflow-y:auto}
  aside li{padding:7px 10px;border-radius:6px;cursor:pointer;font-size:12.5px;color:#d3d3cf;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
  aside li:hover{background:#2c2c2c}
  aside li.ativo{background:#3a3a37;color:#fff}
  aside li b{color:#bdbdb8;font-weight:600;margin-right:4px}
  aside li .pass{color:#7d7d78;font-size:10.5px;margin-left:4px}
  aside li.vazio{color:#6d6d68;font-style:italic;cursor:default}
  aside .telas-wrap{flex:1;overflow-y:auto;min-height:60px}
  aside .rodape{padding:10px 16px;border-top:1px solid #3a3a3a;font-size:10.5px;color:#79796f}
  /* ---- Palco ---- */
  main{flex:1;display:flex;flex-direction:column;height:100vh;overflow:hidden}
  .topo{background:#fff;border-bottom:1px solid #d7d7d3;padding:10px 18px;display:flex;align-items:center;gap:14px}
  .topo .t-prod{font-weight:700}
  .topo .t-tag{font-size:11px;color:#fff;background:#b45; padding:2px 8px;border-radius:10px;background:#9a6b2f}
  .topo .t-nota{font-size:11.5px;color:var(--nota);margin-left:auto}
  .palco{flex:1;overflow:auto;display:flex;align-items:flex-start;justify-content:center;padding:26px}
  /* ---- Frames de dispositivo ---- */
  .frame{background:#fff;border:1px solid var(--linha);border-radius:10px;box-shadow:0 10px 30px rgba(0,0,0,.10),0 2px 6px rgba(0,0,0,.06)}
  .frame-web{width:860px;max-width:100%}
  .frame-web .chrome{background:#ececea;border-bottom:1px solid var(--linha);border-radius:10px 10px 0 0;padding:8px 12px;display:flex;align-items:center;gap:8px}
  .frame-web .dot{width:11px;height:11px;border-radius:50%;background:#cdcdc9}
  .frame-web .url{flex:1;background:#fff;border:1px solid var(--linha);border-radius:6px;padding:3px 10px;font-size:11.5px;color:#9a9a95;margin-left:8px}
  .frame-mobile{width:390px}
  .frame-mobile .chrome{background:#111;border-radius:10px 10px 0 0;height:26px;position:relative}
  .frame-mobile .chrome::after{content:"";position:absolute;left:50%;top:7px;transform:translateX(-50%);width:120px;height:12px;background:#000;border-radius:8px}
  .frame-desktop{width:820px;max-width:100%}
  .frame-desktop .chrome{background:#e4e4e1;border-bottom:1px solid var(--linha);border-radius:10px 10px 0 0;padding:7px 12px;display:flex;gap:7px}
  .frame-desktop .dot{width:11px;height:11px;border-radius:50%;background:#cdcdc9}
  .tela-viewport{padding:0}
  /* ---- Uma tela ---- */
  .tela{padding:0}
  .tela-head{display:flex;align-items:center;gap:8px;padding:9px 16px;border-bottom:1px dashed var(--linha);background:#fafaf8;font-size:11.5px;color:#8a8a86}
  .tela-head .tela-id{font-weight:700;color:#a09a90}
  .tela-head .tela-nome{font-weight:700;color:#555}
  .tela-head .tela-tipo{margin-left:auto;background:#ececea;border-radius:8px;padding:1px 8px;color:#8a8a86}
  .wf-estado{margin:10px 16px 0;font-size:11px;color:#9a6b2f;background:#f6efe2;border:1px solid #e6d8bf;border-radius:6px;padding:4px 9px;display:inline-block}
  .tela-corpo{padding:20px 22px 30px;min-height:380px}
  /* ---- Blocos lo-fi (cinza, honesto) ---- */
  .wf-titulo{font-size:20px;font-weight:800;color:#3a3a38;letter-spacing:-.2px;margin:4px 0 12px}
  .wf-subtitulo{font-size:14px;font-weight:700;color:#5a5a57;margin:16px 0 8px}
  .wf-texto{color:#77776f;margin:8px 0}
  .wf-texto.wf-vazio{color:#b0b0aa;font-style:italic}
  .wf-label{display:block;font-size:12px;color:#8a8a84;margin:12px 0 4px}
  .wf-input{height:36px;border:1px solid var(--linha);border-radius:6px;background:repeating-linear-gradient(135deg,#f7f7f5,#f7f7f5 6px,#f1f1ef 6px,#f1f1ef 12px)}
  .wf-input.wf-area{height:74px}
  .wf-input.wf-select{height:36px;display:flex;align-items:center;padding:0 10px;color:#a0a09a;background:#f7f7f5}
  .wf-botao{display:inline-block;margin:14px 8px 4px 0;padding:10px 20px;border:none;border-radius:7px;background:#4a4a47;color:#fff;font-weight:700;font-size:13px;cursor:pointer}
  .wf-botao:hover{background:#333}
  .wf-botao-morto{background:#c4c4bf;cursor:not-allowed}
  .wf-link{display:inline-block;margin:8px 0;color:#5a7a9a;text-decoration:underline;font-size:12.5px;cursor:pointer}
  .wf-lista{list-style:none;margin:10px 0;padding:0;border:1px solid var(--linha);border-radius:8px;overflow:hidden}
  .wf-lista li{padding:11px 14px;border-bottom:1px solid var(--linha2);color:#66665f}
  .wf-lista li:last-child{border-bottom:none}
  .wf-tabela{width:100%;border-collapse:collapse;margin:10px 0;font-size:12.5px}
  .wf-tabela th{text-align:left;padding:9px 12px;background:#f1f1ef;border:1px solid var(--linha);color:#77776f;font-weight:700}
  .wf-tabela td{padding:11px 12px;border:1px solid var(--linha2)}
  .wf-skel{display:block;height:9px;border-radius:5px;background:var(--skel);width:80%}
  .wf-card{border:1px solid var(--linha);border-radius:9px;padding:14px;margin:10px 0;background:#fbfbf9}
  .wf-card-t{font-weight:700;color:#55554f;margin-bottom:5px}
  .wf-card-b{color:#88887f;font-size:12.5px}
  .wf-img{height:150px;border:1px dashed var(--linha);border-radius:8px;display:flex;align-items:center;justify-content:center;color:#adada6;background:repeating-linear-gradient(135deg,#f5f5f3,#f5f5f3 10px,#efefec 10px,#efefec 20px);margin:10px 0}
  .wf-img span{color:#a8a8a0;font-size:12.5px}
  .wf-abas{display:flex;gap:2px;border-bottom:2px solid var(--linha);margin:10px 0 14px}
  .wf-aba{padding:8px 16px;font-size:12.5px;color:#7a7a73;cursor:pointer;border-bottom:2px solid transparent;margin-bottom:-2px}
  .wf-aba:hover{color:#333;border-bottom-color:#9a9a93}
  .wf-nav{display:flex;gap:6px;justify-content:space-around;border-top:1px solid var(--linha);padding:10px 0;margin-top:18px;background:#fafaf8}
  .wf-navitem{font-size:11.5px;color:#7a7a73;cursor:pointer;padding:4px 10px;border-radius:6px}
  .wf-navitem:hover{background:#eee;color:#333}
  .wf-metrica{display:inline-block;min-width:130px;border:1px solid var(--linha);border-radius:9px;padding:14px 16px;margin:6px 10px 6px 0;background:#fbfbf9;vertical-align:top}
  .wf-metrica-v{font-size:24px;font-weight:800;color:#4a4a45}
  .wf-metrica-r{font-size:11.5px;color:#8a8a82;margin-top:2px}
  .wf-aviso{background:#f6efe2;border:1px solid #e6d8bf;color:#8a6a2f;border-radius:7px;padding:9px 12px;margin:10px 0;font-size:12.5px}
  .wf-espaco{height:18px}
  /* ---- Stepper de fluxo ---- */
  .stepper{background:#fff;border-top:1px solid #d7d7d3;padding:9px 18px;display:none;align-items:center;gap:12px;font-size:12.5px}
  .stepper.on{display:flex}
  .stepper b{color:#555}
  .stepper .sp-nome{font-weight:700}
  .stepper .sp-pos{color:var(--nota)}
  .stepper button{border:1px solid var(--linha);background:#f4f4f2;border-radius:6px;padding:5px 12px;cursor:pointer;font-weight:700;color:#555}
  .stepper button:disabled{opacity:.4;cursor:default}
  .stepper .sp-x{margin-left:auto;cursor:pointer;color:#a0a09a;font-size:16px;line-height:1}
  @media(max-width:760px){aside{display:none}.frame-web,.frame-desktop{width:100%}}
</style>
</head>
<body>
  <aside>
    <div class="marca">
      <b>{{PRODUTO}}</b>
      <small>maquete lo-fi{{AVISO_QUALIDADE}}</small>
    </div>
    <h4>Fluxos</h4>
    <ul id="lista-fluxos">{{ITENS_FLUXOS}}</ul>
    <h4>Telas</h4>
    <div class="telas-wrap"><ul id="lista-telas">{{ITENS_TELAS}}</ul></div>
    <div class="rodape">Protótipo para VALIDAR e discutir — não é a arte final.<br>Gerado em {{GERADO}}.</div>
  </aside>
  <main>
    <div class="topo">
      <span class="t-prod">{{PRODUTO}}</span>
      <span class="t-tag">rascunho navegável</span>
      <span class="t-nota">clique nos botões para andar pelas telas · para quem: {{PARAQUEM}}</span>
    </div>
    <div class="palco">
      <div class="frame {{FRAME_CLASS}}">
        <div class="chrome"><span class="dot"></span><span class="dot"></span><span class="dot"></span><span class="url">maquete://{{PLATAFORMA}}</span></div>
        <div class="tela-viewport" id="viewport">
          {{FRAMES}}
        </div>
      </div>
    </div>
    <div class="stepper" id="stepper">
      <b>Fluxo:</b> <span class="sp-nome" id="sp-nome"></span>
      <span class="sp-pos" id="sp-pos"></span>
      <button id="sp-prev">← anterior</button>
      <button id="sp-next">próximo →</button>
      <span class="sp-x" id="sp-x" title="sair do fluxo">✕</span>
    </div>
  </main>
<script>
(function(){
  var FLUXOS = {{FLUXOS_JS}};
  var atual = "{{TELA_INICIAL}}";
  var fluxoAtivo = -1, passo = 0;

  function todasTelas(){ return Array.prototype.slice.call(document.querySelectorAll('.tela')); }
  function mostrar(id){
    if(!id) return;
    var achou=false;
    todasTelas().forEach(function(s){
      var on = s.getAttribute('data-id').toUpperCase() === id.toUpperCase();
      s.hidden = !on; if(on) achou=true;
    });
    if(!achou) return;
    atual = id;
    document.querySelectorAll('#lista-telas li').forEach(function(li){
      li.classList.toggle('ativo', li.getAttribute('data-goto') && li.getAttribute('data-goto').toUpperCase()===id.toUpperCase());
    });
    var vp = document.getElementById('viewport'); if(vp) vp.scrollTop = 0;
  }
  // navegação por qualquer elemento com data-goto
  document.addEventListener('click', function(e){
    var el = e.target.closest('[data-goto]');
    if(el){ e.preventDefault(); var d = el.getAttribute('data-goto'); if(d){ sairFluxoSilencioso(); mostrar(d);} }
  });
  // fluxos
  var listaFluxos = document.getElementById('lista-fluxos');
  if(listaFluxos){
    listaFluxos.addEventListener('click', function(e){
      var li = e.target.closest('li[data-fluxo]'); if(!li) return;
      iniciarFluxo(parseInt(li.getAttribute('data-fluxo'),10));
    });
  }
  function iniciarFluxo(i){
    if(!FLUXOS[i]) return;
    fluxoAtivo=i; passo=0;
    document.querySelectorAll('#lista-fluxos li').forEach(function(li){
      li.classList.toggle('ativo', parseInt(li.getAttribute('data-fluxo'),10)===i);
    });
    document.getElementById('sp-nome').textContent = FLUXOS[i].nome;
    document.getElementById('stepper').classList.add('on');
    irPasso(0);
  }
  function irPasso(p){
    var fl = FLUXOS[fluxoAtivo]; if(!fl) return;
    passo = Math.max(0, Math.min(p, fl.telas.length-1));
    mostrar(fl.telas[passo]);
    document.getElementById('sp-pos').textContent = 'passo '+(passo+1)+' de '+fl.telas.length;
    document.getElementById('sp-prev').disabled = passo===0;
    document.getElementById('sp-next').disabled = passo===fl.telas.length-1;
  }
  function sairFluxoSilencioso(){
    fluxoAtivo=-1;
    document.getElementById('stepper').classList.remove('on');
    document.querySelectorAll('#lista-fluxos li').forEach(function(li){li.classList.remove('ativo');});
  }
  var b;
  if(b=document.getElementById('sp-prev')) b.onclick=function(){irPasso(passo-1);};
  if(b=document.getElementById('sp-next')) b.onclick=function(){irPasso(passo+1);};
  if(b=document.getElementById('sp-x'))    b.onclick=sairFluxoSilencioso;
  // teclado: setas andam no fluxo se ativo
  document.addEventListener('keydown', function(e){
    if(fluxoAtivo<0) return;
    if(e.key==='ArrowRight'){ irPasso(passo+1); }
    else if(e.key==='ArrowLeft'){ irPasso(passo-1); }
    else if(e.key==='Escape'){ sairFluxoSilencioso(); }
  });
  mostrar(atual);
})();
</script>
</body>
</html>
"""

if __name__ == "__main__":
    main()
