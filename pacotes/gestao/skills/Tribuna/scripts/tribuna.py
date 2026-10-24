#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Tribuna — motor de Autoridade de Especialista (thought leadership) em PT-BR.
Só biblioteca padrão (offline, sem rede, sem instalação). A IA conversa e
raciocina; este motor apenas GUARDA o material da autoridade do dono e CALCULA
a parte exata (força de cada pilar de tema, funil de palcos e a nota honesta de
autoridade). Nunca inventa credencial, número, cliente nem case.

Dados ficam 100% locais em .tribuna/ na RAIZ do projeto:
  .tribuna/config.md    (identidade — gravado no setup de 1ª execução)
  .tribuna/tese.md      (o ângulo autoral + a bandeira/manifesto)
  .tribuna/metodo.md    (o framework autoral COM NOME + os passos)
  .tribuna/pilares.csv  (os temas que você quer "dominar" + posse × demanda)
  .tribuna/alvos.csv    (palcos-alvo: podcast/evento/mídia/comunidade + status)
"""
import sys, os, csv, argparse, unicodedata, re

# ------------------------------------------------------------------ raiz/paths
def _sem_acento(s):
    if not s:
        return ""
    return "".join(c for c in unicodedata.normalize("NFD", str(s))
                   if unicodedata.category(c) != "Mn").lower().strip()

def achar_raiz():
    """Ancora .tribuna/ na raiz do projeto (não dentro da pasta da skill)."""
    env = os.environ.get("CLAUDE_PROJECT_DIR")
    if env and os.path.isdir(env):
        return env
    d = os.getcwd()
    while True:
        for marca in (".tribuna", ".git", ".claude"):
            if os.path.isdir(os.path.join(d, marca)):
                return d
        pai = os.path.dirname(d)
        if pai == d:
            return os.getcwd()
        d = pai

RAIZ = achar_raiz()
DIR = os.path.join(RAIZ, ".tribuna")
TESE = os.path.join(DIR, "tese.md")
METODO = os.path.join(DIR, "metodo.md")
PILARES = os.path.join(DIR, "pilares.csv")
ALVOS = os.path.join(DIR, "alvos.csv")
CONFIG = os.path.join(DIR, "config.md")

def garantir_dir():
    os.makedirs(DIR, exist_ok=True)

# ------------------------------------------------------------------ config
def ler_config():
    """Lê '- **Rótulo:** valor' do config.md, chave sem acento/minúscula."""
    cfg = {}
    if not os.path.exists(CONFIG):
        return cfg
    with open(CONFIG, encoding="utf-8") as f:
        for linha in f:
            m = re.match(r"\s*[-*]\s*\*\*(.+?):\*\*\s*(.*)", linha)
            if m:
                cfg[_sem_acento(m.group(1))] = m.group(2).strip()
    return cfg

def cfg_get(cfg, *chaves, padrao=""):
    for c in chaves:
        k = _sem_acento(c)
        if k in cfg and cfg[k]:
            return cfg[k]
    return padrao

# ------------------------------------------------------------------ csv util
def ler_csv(caminho):
    if not os.path.exists(caminho):
        return []
    with open(caminho, encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))

def escrever_csv(caminho, linhas, campos):
    garantir_dir()
    with open(caminho, "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=campos)
        w.writeheader()
        for l in linhas:
            w.writerow({c: l.get(c, "") for c in campos})

def prox_id(linhas):
    m = 0
    for l in linhas:
        try:
            m = max(m, int(l.get("id", 0)))
        except (ValueError, TypeError):
            pass
    return str(m + 1)

CAMPOS_PILAR = ["id", "texto", "posse", "demanda"]
CAMPOS_ALVO = ["id", "nome", "tipo", "publico", "status"]

# ------------------------------------------------------------------ escalas
def _n03(v):
    try:
        return max(0, min(3, int(v)))
    except (ValueError, TypeError):
        return None

# temas genéricos demais para virar pilar de autoridade (nicho de ninguém)
GENERICOS = [
    "inteligencia artificial", "ia", "tecnologia", "inovacao", "produtividade",
    "marketing", "vendas", "negocios", "empreendedorismo", "futuro", "transformacao digital",
    "automacao", "gestao", "lideranca", "sucesso", "mindset", "digital",
]
def eh_generico(texto):
    t = _sem_acento(texto)
    # genérico só se for EXATAMENTE o termo amplo (não se for uma fatia de nicho dele)
    return t in GENERICOS

STATUS_ORDEM = ["alvo", "contatado", "agendado", "feito"]
STATUS_LABEL = {"alvo": "🎯 alvo", "contatado": "✉️ contatado",
                "agendado": "📅 agendado", "feito": "✅ feito"}
def norm_status(s):
    n = _sem_acento(s)
    mapa = {"alvo": "alvo", "lista": "alvo", "contatado": "contatado", "contato": "contatado",
            "pitchado": "contatado", "agendado": "agendado", "marcado": "agendado",
            "feito": "feito", "publicado": "feito", "feita": "feito", "ok": "feito"}
    return mapa.get(n)

TIPOS_ALVO = ["podcast", "evento", "midia", "comunidade", "artigo", "canal"]

# ------------------------------------------------------------------ comandos
def cmd_config(args):
    cfg = ler_config()
    if not cfg:
        print("Config ainda não criado. Rode o setup de 1ª execução (setup/SETUP.md).")
        return
    print("=== Sua identidade (config.md) ===")
    for rot in ("Nome", "Campo/Nicho", "Para quem", "Credencial real", "Tom"):
        v = cfg_get(cfg, rot)
        if v:
            print(f"  {rot}: {v}")

# ---- Tese (ângulo + bandeira/manifesto) ----
def _tem_tese():
    return os.path.exists(TESE) and os.path.getsize(TESE) > 0

def cmd_tese_set(args):
    garantir_dir()
    campos = {
        "angulo": (args.angulo or "[o seu ponto de vista contrário]").strip(),
        "inimigo": (args.inimigo or "[a crença comum que você contraria]").strip(),
        "mudanca": (args.mudanca or "[a mudança que você prega]").strip(),
        "frase": (args.frase or "[a sua grande ideia em uma frase]").strip(),
    }
    faltando = [k for k, v in campos.items() if v.startswith("[")]
    linhas = [
        "# Tese & Bandeira — Tribuna\n\n",
        "## Ângulo autoral (o que só VOCÊ defende)\n", campos["angulo"] + "\n\n",
        "## O inimigo comum (a crença que você contraria)\n", campos["inimigo"] + "\n\n",
        "## A mudança que você prega\n", campos["mudanca"] + "\n\n",
        "## A grande ideia em uma frase (o manifesto)\n", "> " + campos["frase"] + "\n",
    ]
    if faltando:
        linhas.append("\n## ⚠ Ainda falta preencher\n")
        for k in faltando:
            linhas.append(f"- {k}\n")
    with open(TESE, "w", encoding="utf-8") as f:
        f.writelines(linhas)
    print("=== TESE GRAVADA ===\n")
    print(f"Ângulo:  {campos['angulo']}")
    print(f"Inimigo: {campos['inimigo']}")
    print(f"Mudança: {campos['mudanca']}")
    print(f"Frase:   “{campos['frase']}”")
    # aviso anti-morno
    if _sem_acento(campos["inimigo"]).startswith("["):
        print("\n⚠ Sem um INIMIGO claro (a crença comum que você contraria), isso ainda é")
        print("  opinião morna, não tese. Toda autoridade defende algo que alguém discorda.")
    if faltando:
        print(f"\n⚠ Ainda falta preencher: {', '.join(faltando)}")

def cmd_tese_show(args):
    if not _tem_tese():
        print("Sem tese ainda. Monte com: tese-set --angulo ... --inimigo ... --mudanca ... --frase ...")
        return
    print(open(TESE, encoding="utf-8").read())

# ---- Método autoral ----
def _tem_metodo():
    return os.path.exists(METODO) and os.path.getsize(METODO) > 0

def cmd_metodo_set(args):
    garantir_dir()
    nome = (args.nome or "[NOME DO SEU MÉTODO]").strip()
    promessa = (args.promessa or "[o que o método entrega]").strip()
    passos = [p.strip() for p in (args.passos or "").split(";") if p.strip()]
    linhas = [f"# Método autoral: {nome} — Tribuna\n\n",
              f"**Promessa:** {promessa}\n\n", "## Os passos\n"]
    if passos:
        for i, p in enumerate(passos, 1):
            linhas.append(f"{i}. {p}\n")
    else:
        linhas.append("[defina 3 a 7 passos com --passos \"passo 1; passo 2; passo 3\"]\n")
    with open(METODO, "w", encoding="utf-8") as f:
        f.writelines(linhas)
    print(f"=== MÉTODO GRAVADO: {nome} ===")
    print(f"Promessa: {promessa}")
    for i, p in enumerate(passos, 1):
        print(f"  {i}. {p}")
    avisos = []
    if nome.startswith("[") or _sem_acento(nome) in ("", "meu metodo", "metodo"):
        avisos.append("Dê um NOME próprio e memorável ao método — é ele que vira sua assinatura.")
    if len(passos) < 3:
        avisos.append("Um método repetível costuma ter de 3 a 7 passos. Você tem menos que isso.")
    if len(passos) > 7:
        avisos.append("Mais de 7 passos ninguém lembra. Agrupe até caber em 3–7.")
    for a in avisos:
        print(f"  ⚠ {a}")

def cmd_metodo_show(args):
    if not _tem_metodo():
        print("Sem método ainda. Monte com: metodo-set --nome ... --promessa ... --passos \"a; b; c\"")
        return
    print(open(METODO, encoding="utf-8").read())

# ---- Pilares de tema ----
def cmd_pilar_add(args):
    pil = ler_csv(PILARES)
    novo = {"id": prox_id(pil), "texto": args.texto.strip(), "posse": "", "demanda": ""}
    pil.append(novo)
    escrever_csv(PILARES, pil, CAMPOS_PILAR)
    aviso = ("  ⚠ tema amplo demais (autoridade de todo mundo = de ninguém). Afunile para uma "
             "fatia sua." if eh_generico(args.texto) else "")
    print(f"OK — pilar de tema #{novo['id']}: {novo['texto']}{aviso}")
    print(f"Agora pontue: pilar-nota --id {novo['id']} --posse 0-3 --demanda 0-3")

def cmd_pilar_nota(args):
    pil = ler_csv(PILARES)
    alvo = next((p for p in pil if p["id"] == str(args.id)), None)
    if not alvo:
        print(f"Nada com id {args.id}. Liste com: pilares")
        return
    for campo, val in (("posse", args.posse), ("demanda", args.demanda)):
        if val is not None:
            n = _n03(val)
            if n is None:
                print(f"Valor de --{campo} inválido (use 0 a 3).")
                return
            alvo[campo] = str(n)
    escrever_csv(PILARES, pil, CAMPOS_PILAR)
    print(f"OK — pilar #{alvo['id']} atualizado.")
    cmd_pilares(args)

def _forca_pilar(p):
    """Força 0-100 de um pilar de tema a partir de posse × demanda (0-3 cada).
    Posse é porta: se você não tem NADA de próprio a dizer ali (posse 0), força 0 —
    não dá para ser autoridade em tema que você não vive."""
    po = _n03(p.get("posse")); de = _n03(p.get("demanda"))
    if po is None or de is None:
        return None
    if po == 0:
        return 0
    # posse (o que é SEU) pesa mais que demanda; ambos 3 -> 100
    return round((po * 4 + de * 2) / 18 * 100)

def cmd_pilares(args):
    pil = ler_csv(PILARES)
    if not pil:
        print("Nenhum pilar de tema ainda. Cadastre com: pilar-add --texto \"...\"")
        return
    print("=== PILARES DE TEMA (os assuntos que você quer DOMINAR) ===")
    print("Crivos: [P]osse (o quanto é SEU, da sua vivência) · [D]emanda (o quanto o público liga) — 0 a 3\n")
    avaliados = []
    for p in pil:
        f = _forca_pilar(p)
        if f is None:
            print(f"  [{p['id']}] {p['texto']}")
            print(f"        ⏳ falta pontuar — pilar-nota --id {p['id']} --posse _ --demanda _")
            continue
        sem = "🟢" if f >= 70 else ("🟡" if f >= 45 else "🔴")
        avaliados.append((f, p))
        pt = p.get("posse", "·"); dt = p.get("demanda", "·")
        print(f"  [{p['id']}] {sem} força {f}/100   (P{pt} D{dt})   {p['texto']}")
        obs = []
        if _n03(p.get("posse")) == 0:
            obs.append("você não tem vivência própria aqui → não é seu pilar")
        if (_n03(p.get("demanda")) or 0) <= 1:
            obs.append("o público quase não procura por isso")
        if eh_generico(p["texto"]):
            obs.append("tema amplo demais — afunile para a sua fatia")
        if obs:
            print(f"        ⚠ {'; '.join(obs)}")
    if avaliados:
        avaliados.sort(reverse=True, key=lambda x: x[0])
        fortes = [p for f, p in avaliados if f >= 70]
        print(f"\n➜ Você tem {len(fortes)} pilar(es) forte(s) (≥70).")
        if len(fortes) < 3:
            print("  ⚠ Autoridade sólida costuma ter 3–5 pilares fortes que você repete sempre.")
            print("    Afine os crivos com honestidade ou troque temas que você não vive de verdade.")
        else:
            print("  🟢 Base boa: gire TODO o seu conteúdo em torno destes pilares — sempre os mesmos.")

# ---- Palcos-alvo (colocar-se no radar) ----
def cmd_alvo_add(args):
    al = ler_csv(ALVOS)
    tipo = _sem_acento(args.tipo) if args.tipo else "podcast"
    if tipo not in TIPOS_ALVO:
        tipo = "podcast"
    novo = {"id": prox_id(al), "nome": args.nome.strip(), "tipo": tipo,
            "publico": (args.publico or "").strip(), "status": "alvo"}
    al.append(novo)
    escrever_csv(ALVOS, al, CAMPOS_ALVO)
    print(f"OK — palco-alvo #{novo['id']} ({tipo}): {novo['nome']}  [🎯 alvo]")

def cmd_alvo_status(args):
    al = ler_csv(ALVOS)
    alvo = next((a for a in al if a["id"] == str(args.id)), None)
    if not alvo:
        print(f"Nada com id {args.id}. Liste com: alvos")
        return
    st = norm_status(args.status)
    if not st:
        print("Status inválido. Use: alvo | contatado | agendado | feito")
        return
    alvo["status"] = st
    escrever_csv(ALVOS, al, CAMPOS_ALVO)
    print(f"OK — palco #{alvo['id']} ({alvo['nome']}): {STATUS_LABEL[st]}")

def cmd_alvos(args):
    al = ler_csv(ALVOS)
    if not al:
        print("Nenhum palco-alvo ainda. Cadastre com: alvo-add --nome \"...\" --tipo podcast|evento|midia|comunidade|artigo")
        return
    print("=== FUNIL DE PALCOS (onde você aparece para virar referência) ===\n")
    for st in STATUS_ORDEM:
        grupo = [a for a in al if a.get("status") == st]
        if grupo:
            print(f"-- {STATUS_LABEL[st]} ({len(grupo)}) --")
            for a in grupo:
                pub = f"  · público: {a['publico']}" if a.get("publico") else ""
                print(f"   [{a['id']}] {a['nome']}  ({a.get('tipo','')}){pub}")
            print()
    feitos = sum(1 for a in al if a.get("status") == "feito")
    agendados = sum(1 for a in al if a.get("status") == "agendado")
    print(f"Resumo: {len(al)} alvos • {agendados} agendado(s) • {feitos} feito(s).")
    if feitos + agendados == 0:
        print("⚠ Autoridade não é só o que você publica no seu quintal — é onde OUTROS te chamam.")
        print("  Mire 1 palco externo (podcast/evento/artigo convidado) e mova-o até 'feito'.")

# ---- Painel + nota de autoridade ----
def cmd_painel(args):
    cfg = ler_config()
    pil = ler_csv(PILARES)
    al = ler_csv(ALVOS)
    print("=== PAINEL DA TRIBUNA ===")
    nome = cfg_get(cfg, "Nome")
    nicho = cfg_get(cfg, "Campo/Nicho")
    if nome:
        print(f"Autoridade: {nome}" + (f" — {nicho}" if nicho else ""))

    # portões da nota honesta de autoridade
    tem_tese = _tem_tese()
    tese_com_inimigo = False
    if tem_tese:
        txt = open(TESE, encoding="utf-8").read()
        tese_com_inimigo = ("[A PREENCHER]" not in txt and "[a crença comum" not in txt
                             and "⚠ Ainda falta" not in txt)
    nicho_ok = bool(nicho) and _sem_acento(nicho) not in (
        "", "ia", "inteligencia artificial", "tecnologia", "geral", "tudo", "todos")
    tem_metodo_batizado = False
    if _tem_metodo():
        mt = open(METODO, encoding="utf-8").read()
        tem_metodo_batizado = "[NOME DO SEU MÉTODO]" not in mt
    fortes = [p for p in pil if (_forca_pilar(p) or 0) >= 70]
    pilares_ok = len(fortes) >= 3
    palco_ok = any(a.get("status") in ("agendado", "feito") for a in al)

    portoes = [
        ("Tese com inimigo claro (não morna)", tese_com_inimigo),
        ("Nicho específico (não 'IA/tecnologia' em geral)", nicho_ok),
        ("Método autoral batizado", tem_metodo_batizado),
        ("3+ pilares de tema fortes", pilares_ok),
        ("1+ palco externo agendado/feito", palco_ok),
    ]
    pontos = sum(1 for _, ok in portoes if ok)
    print("\n-- Nota honesta de autoridade --")
    for rot, ok in portoes:
        print(f"  {'✓' if ok else '✗'} {rot}")
    if pontos >= 5:
        print("\n  🟢 REFERÊNCIA — tese, método, pilares e palco no lugar. Você já tem tribuna própria.")
    elif pontos >= 3:
        print("\n  🟡 EM CONSTRUÇÃO — a base está de pé; ataque os ✗ acima na ordem em que aparecem.")
    else:
        print("\n  🔴 AINDA INVISÍVEL — falta o essencial. Comece pela TESE (o que só você defende).")

    print("\n-- A ordem de construção (se estiver perdido) --")
    print("  1) Ângulo/Tese  →  2) Método com nome  →  3) 3–5 pilares  →  4) palcos externos")
    print("\n-- Passar o bastão --")
    print("  → Holofote: transforma a tese + pilares em conteúdo recorrente nas redes")
    print("  → Verbo: escreve a copy (bio de autoridade, pitch de convidado, página do método)")
    print("  → Baliza: usa a autoridade como diferencial de posicionamento da oferta")
    print("  → Alavanca: empacota o método autoral num produto digital que vende sozinho")

# ------------------------------------------------------------------ CLI
def main():
    p = argparse.ArgumentParser(prog="tribuna", description="Motor de Autoridade de Especialista — Tribuna")
    sub = p.add_subparsers(dest="cmd")

    sub.add_parser("config", help="mostra sua identidade do config.md").set_defaults(func=cmd_config)

    ts = sub.add_parser("tese-set", help="grava o ângulo autoral + a bandeira/manifesto")
    for c in ("angulo", "inimigo", "mudanca", "frase"):
        ts.add_argument("--" + c)
    ts.set_defaults(func=cmd_tese_set)
    sub.add_parser("tese", help="mostra a tese gravada").set_defaults(func=cmd_tese_show)

    ms = sub.add_parser("metodo-set", help="grava o método autoral com nome e passos")
    ms.add_argument("--nome"); ms.add_argument("--promessa")
    ms.add_argument("--passos", help="passos separados por ; (ex.: \"a; b; c\")")
    ms.set_defaults(func=cmd_metodo_set)
    sub.add_parser("metodo", help="mostra o método gravado").set_defaults(func=cmd_metodo_show)

    pa = sub.add_parser("pilar-add", help="cadastra um pilar de tema candidato")
    pa.add_argument("--texto", required=True); pa.set_defaults(func=cmd_pilar_add)
    pn = sub.add_parser("pilar-nota", help="pontua um pilar (posse × demanda, 0-3 cada)")
    pn.add_argument("--id", required=True)
    pn.add_argument("--posse"); pn.add_argument("--demanda")
    pn.set_defaults(func=cmd_pilar_nota)
    sub.add_parser("pilares", help="lista pilares com força e semáforo").set_defaults(func=cmd_pilares)

    aa = sub.add_parser("alvo-add", help="cadastra um palco-alvo (podcast/evento/mídia/...)")
    aa.add_argument("--nome", required=True)
    aa.add_argument("--tipo", help="podcast|evento|midia|comunidade|artigo|canal")
    aa.add_argument("--publico")
    aa.set_defaults(func=cmd_alvo_add)
    ast = sub.add_parser("alvo-status", help="move um palco no funil")
    ast.add_argument("--id", required=True); ast.add_argument("--status", required=True)
    ast.set_defaults(func=cmd_alvo_status)
    sub.add_parser("alvos", help="mostra o funil de palcos").set_defaults(func=cmd_alvos)

    sub.add_parser("painel", help="resumo + nota honesta de autoridade + passar o bastão").set_defaults(func=cmd_painel)
    sub.add_parser("nota", help="atalho para o painel").set_defaults(func=cmd_painel)

    args = p.parse_args()
    if not getattr(args, "cmd", None):
        p.print_help()
        return
    args.func(args)

if __name__ == "__main__":
    main()
