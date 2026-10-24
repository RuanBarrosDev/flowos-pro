#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Gabarito — motor de elicitação de requisitos e especificação.

Transforma um pedido vago ("quero um sistema/app/automação/site que faça X" —
seu ou de um cliente) numa ESPECIFICAÇÃO escrita, priorizada e com critério de
aceite, ANTES de construir. Assim você (ou seu desenvolvedor, ou o Claude Code)
constrói a coisa CERTA.

Princípios (travas de segurança embutidas):
  - NUNCA inventa problema, requisito, número ou critério → marca [A CONFERIR].
  - Toda funcionalidade traça a um problema real (Problema → Necessidade → Requisito).
    Requisito sem problema por trás é órfão = candidato a cortar (anti-desperdício).
  - Todo requisito precisa de critério de aceite testável. Adjetivo vago
    ("rápido/fácil/intuitivo") sem número não é requisito — é opinião.
  - Prioriza por MoSCoW (Obrigatório / Importante / Desejável / Fora-por-ora) e
    confere dependências: o obrigatório não pode depender do opcional.
  - Separa fatos, suposições, riscos, restrições e perguntas em aberto — nunca mistura.
  - A IA pergunta e REDIGE; o DONO decide e valida. Dados 100% locais (offline).

Sem dependências externas. Só biblioteca padrão. NUNCA acessa a rede.
"""

import sys
import os
import csv
import argparse
import unicodedata
from datetime import datetime, timezone

# ----------------------------------------------------------------------------
# Ancoragem: onde fica a pasta .gabarito/  (raiz do projeto)
# ----------------------------------------------------------------------------

def _strip_accents(s):
    if not s:
        return ""
    nfkd = unicodedata.normalize("NFKD", str(s))
    return "".join(c for c in nfkd if not unicodedata.combining(c))

def _norm(s):
    """minúsculo, sem acento, sem espaços nas bordas — para comparação robusta."""
    return _strip_accents(str(s or "")).strip().lower()

def find_project_root():
    """Sobe a árvore procurando um marcador de raiz de projeto.
    Preferência: CLAUDE_PROJECT_DIR > pasta que já tem .gabarito/ > .git/.claude > cwd."""
    env = os.environ.get("CLAUDE_PROJECT_DIR")
    if env and os.path.isdir(env):
        return os.path.abspath(env)
    cur = os.path.abspath(os.getcwd())
    # 1) se já existe um .gabarito na árvore, use-o
    walk = cur
    while True:
        if os.path.isdir(os.path.join(walk, ".gabarito")):
            return walk
        parent = os.path.dirname(walk)
        if parent == walk:
            break
        walk = parent
    # 2) senão, o primeiro .git/.claude que aparecer
    walk = cur
    while True:
        if os.path.isdir(os.path.join(walk, ".git")) or os.path.isdir(os.path.join(walk, ".claude")):
            return walk
        parent = os.path.dirname(walk)
        if parent == walk:
            break
        walk = parent
    # 3) fallback: diretório atual
    return cur

ROOT = find_project_root()
GDIR = os.path.join(ROOT, ".gabarito")

def gpath(*parts):
    return os.path.join(GDIR, *parts)

def ensure_dir():
    os.makedirs(GDIR, exist_ok=True)

def now_stamp():
    return datetime.now(timezone.utc).astimezone().strftime("%Y-%m-%d %H:%M")

# ----------------------------------------------------------------------------
# CSV helpers
# ----------------------------------------------------------------------------

FILES = {
    "problemas":    ["id", "codigo", "titulo", "descricao", "criado"],
    "necessidades": ["id", "codigo", "problema", "descricao", "criado"],
    "requisitos":   ["id", "codigo", "necessidade", "enunciado", "tipo",
                     "porque", "criterio", "validar", "prioridade", "depende", "criado"],
    "respostas":    ["id", "dimensao", "pergunta", "resposta", "criado"],
    "escopo":       ["id", "tipo", "texto", "criado"],
}

def _fpath(name):
    return gpath(name + ".csv")

def read_rows(name):
    p = _fpath(name)
    if not os.path.exists(p):
        return []
    with open(p, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))

def write_rows(name, rows):
    ensure_dir()
    cols = FILES[name]
    with open(_fpath(name), "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=cols)
        w.writeheader()
        for r in rows:
            w.writerow({c: r.get(c, "") for c in cols})

def next_id(rows):
    mx = 0
    for r in rows:
        try:
            mx = max(mx, int(r.get("id", 0)))
        except (ValueError, TypeError):
            pass
    return mx + 1

def next_codigo(rows, prefix):
    """Gera CP.01 / CN.01 / RF.01 / RNF.01 a partir do maior número existente do prefixo."""
    mx = 0
    for r in rows:
        cod = r.get("codigo", "")
        if cod.startswith(prefix + "."):
            try:
                mx = max(mx, int(cod.split(".", 1)[1]))
            except (ValueError, IndexError):
                pass
    return "%s.%02d" % (prefix, mx + 1)

# ----------------------------------------------------------------------------
# Config (.gabarito/config.md) — formato "- **Rótulo:** valor", acento-insensível
# ----------------------------------------------------------------------------

def read_config():
    p = gpath("config.md")
    cfg = {}
    if not os.path.exists(p):
        return cfg
    import re
    pat = re.compile(r"^\s*-\s*\*\*(.+?)\*\*\s*:?\s*(.*)$")
    with open(p, encoding="utf-8") as f:
        for line in f:
            m = pat.match(line)
            if m:
                cfg[_norm(m.group(1)).rstrip(":").strip()] = m.group(2).strip()
    return cfg

def cfg_get(cfg, *labels, default=""):
    for lab in labels:
        v = cfg.get(_norm(lab))
        if v:
            return v
    return default

# ----------------------------------------------------------------------------
# Vocabulário / normalização de prioridade e tipo
# ----------------------------------------------------------------------------

PRIOS = {  # aliases → chave canônica
    "must": "Must", "obrigatorio": "Must", "obrigatoria": "Must", "essencial": "Must",
    "should": "Should", "importante": "Should", "deveria": "Should",
    "could": "Could", "desejavel": "Could", "opcional": "Could", "poderia": "Could",
    "wont": "Wont", "wont-have": "Wont", "fora": "Wont", "fora-por-ora": "Wont",
    "nao-agora": "Wont", "depois": "Wont",
}
PRIO_LABEL = {
    "Must":  "Obrigatório (Must)",
    "Should":"Importante (Should)",
    "Could": "Desejável (Could)",
    "Wont":  "Fora por ora (Won't)",
}
PRIO_VALUE = {"Must": 4, "Should": 3, "Could": 2, "Wont": 1}
PRIO_ORDER = ["Must", "Should", "Could", "Wont"]

def norm_prio(s):
    if not s:
        return ""
    return PRIOS.get(_norm(s).replace("_", "-").replace(" ", "-"), "")

def norm_tipo(s):
    n = _norm(s)
    if n in ("nao-funcional", "naofuncional", "nfr", "rnf", "nao funcional", "qualidade"):
        return "nao-funcional"
    if n in ("funcional", "fr", "rf", ""):
        return "funcional"
    return "funcional"

# dimensões da entrevista
DIMENSOES = ["problema", "usuarios", "jornada", "dados", "integracoes",
             "restricoes", "prazo", "orcamento", "sucesso"]

def norm_dimensao(s):
    n = _norm(s)
    alias = {
        "usuario": "usuarios", "publico": "usuarios", "quem": "usuarios",
        "integracao": "integracoes", "sistemas": "integracoes",
        "restricao": "restricoes", "limite": "restricoes", "limites": "restricoes",
        "prazos": "prazo", "orcamentos": "orcamento", "budget": "orcamento",
        "metrica": "sucesso", "metricas": "sucesso", "resultado": "sucesso",
    }
    n = alias.get(n, n)
    return n if n in DIMENSOES else n

# adjetivos vagos que, sozinhos, não são requisito testável
VAGOS = ["rapido", "rapida", "facil", "intuitivo", "intuitiva", "amigavel",
         "moderno", "moderna", "bonito", "bonita", "robusto", "robusta",
         "escalavel", "seguro", "segura", "simples", "leve", "eficiente",
         "otimizado", "otimizada", "flexivel", "confiavel", "estavel",
         "profissional", "agradavel", "fluido", "fluida", "responsivo", "responsiva"]

# ----------------------------------------------------------------------------
# Saída
# ----------------------------------------------------------------------------

def out(s=""):
    print(s)

def hr():
    out("─" * 60)

def title(s):
    out()
    out(s)
    hr()

def para_conferir(v, marca="[A CONFERIR]"):
    v = (v or "").strip()
    return v if v else marca

# ----------------------------------------------------------------------------
# Comandos
# ----------------------------------------------------------------------------

def cmd_init(args):
    ensure_dir()
    # cria os CSVs vazios (com cabeçalho) se não existirem
    for name in FILES:
        if not os.path.exists(_fpath(name)):
            write_rows(name, [])
    # projeto.md base, se não houver
    pj = gpath("projeto.md")
    if not os.path.exists(pj):
        with open(pj, "w", encoding="utf-8") as f:
            f.write("# Projeto (a especificar)\n\n"
                    "- **Nome:** [A CONFERIR]\n"
                    "- **Para quem:** [A CONFERIR]\n"
                    "- **Problema central:** [A CONFERIR]\n"
                    "- **Domínio:** [A CONFERIR]\n")
    out("✓ Gabarito iniciado em: " + GDIR)
    out("  Pastas e arquivos de trabalho prontos. Nada é enviado para a internet.")

def _read_projeto():
    p = gpath("projeto.md")
    d = {}
    if not os.path.exists(p):
        return d
    import re
    pat = re.compile(r"^\s*-\s*\*\*(.+?)\*\*\s*:?\s*(.*)$")
    with open(p, encoding="utf-8") as f:
        for line in f:
            m = pat.match(line)
            if m:
                d[_norm(m.group(1)).rstrip(":").strip()] = m.group(2).strip()
    return d

def cmd_novo(args):
    ensure_dir()
    nome = args.nome or ""
    para = args.para or ""
    problema = args.problema or ""
    dominio = args.dominio or ""
    with open(gpath("projeto.md"), "w", encoding="utf-8") as f:
        f.write("# Projeto\n\n")
        f.write("- **Nome:** %s\n" % para_conferir(nome))
        f.write("- **Para quem:** %s\n" % para_conferir(para))
        f.write("- **Problema central:** %s\n" % para_conferir(problema))
        f.write("- **Domínio:** %s\n" % para_conferir(dominio, "[A CONFERIR]"))
    title("PROJETO ENQUADRADO")
    out("Nome ............ " + para_conferir(nome))
    out("Para quem ....... " + para_conferir(para))
    out("Problema central  " + para_conferir(problema))
    out("Domínio ......... " + para_conferir(dominio))
    faltando = [k for k, v in [("nome", nome), ("para quem", para),
                               ("problema central", problema)] if not v.strip()]
    out()
    if faltando:
        out("⚠ Ainda falta definir: " + ", ".join(faltando) +
            ". Não invente — pergunte ao dono e registre com `responder`.")
    else:
        out("Comece a entrevista: use `perguntas` para ver o que perguntar,")
        out("e `responder` para registrar cada resposta NAS PALAVRAS do dono.")

def cmd_projeto(args):
    d = _read_projeto()
    if not d:
        out("Nenhum projeto enquadrado ainda. Rode `novo --nome ... --para ... --problema ...`.")
        return
    title("PROJETO")
    out("Nome ............ " + para_conferir(d.get(_norm("Nome"))))
    out("Para quem ....... " + para_conferir(d.get(_norm("Para quem"))))
    out("Problema central  " + para_conferir(d.get(_norm("Problema central"))))
    out("Domínio ......... " + para_conferir(d.get(_norm("Domínio"))))

# ---------- entrevista ----------

PERGUNTAS = {
    "problema": [
        "Qual é a dor concreta que isso resolve? O que acontece hoje SEM essa solução?",
        "Quem sente essa dor, e com que frequência?",
        "Como o problema é 'resolvido na marra' hoje (planilha, papel, no braço)?",
    ],
    "usuarios": [
        "Quem vai USAR a solução no dia a dia? (perfis/papéis)",
        "Quantas pessoas, mais ou menos? É o dono, a equipe, o cliente final?",
        "Qual o nível técnico de quem vai usar?",
    ],
    "jornada": [
        "Descreva o passo a passo IDEAL: a pessoa abre e... até terminar a tarefa.",
        "Qual é a tarefa PRINCIPAL que precisa funcionar bem? (o coração)",
        "O que seria um 'deu certo' numa única sessão de uso?",
    ],
    "dados": [
        "Que informações a solução guarda? (ex.: clientes, pedidos, agendamentos)",
        "De onde vêm esses dados? Digitados à mão, importados de planilha, de outro sistema?",
        "Algum dado é sensível (dados pessoais/LGPD, financeiro, saúde)?",
    ],
    "integracoes": [
        "Precisa conversar com algum sistema que você já usa? (planilha, ERP, WhatsApp, e-mail, pagamento)",
        "Precisa de login? De quem? (cliente, equipe)",
        "Precisa enviar algo automático (mensagem, e-mail, cobrança)?",
    ],
    "restricoes": [
        "Tem que rodar em quê? (celular, computador, os dois)",
        "Alguma regra do seu mercado que não pode furar? (norma, contrato, prazo legal)",
        "O que definitivamente NÃO faz parte disso? (para proteger o escopo)",
    ],
    "prazo": [
        "Para quando você precisa de uma primeira versão útil?",
        "Existe uma data que não pode passar? Por quê?",
    ],
    "orcamento": [
        "Quanto dá para investir nisso (tempo/dinheiro)?",
        "Prefere o mais barato que resolve, ou o mais completo?",
    ],
    "sucesso": [
        "Daqui a 3 meses, o que precisa ter mudado para você dizer 'valeu a pena'?",
        "Que número você olharia para saber se funcionou? (tempo economizado, vendas, erros a menos)",
    ],
}

def cmd_perguntas(args):
    dim = norm_dimensao(args.dimensao) if args.dimensao else None
    respostas = read_rows("respostas")
    respondidas = set(_norm(r.get("dimensao")) for r in respostas)
    title("O QUE PERGUNTAR AO DONO")
    dims = [dim] if dim else DIMENSOES
    for d in dims:
        if d not in PERGUNTAS:
            out("Dimensão desconhecida: %s. Use uma de: %s" % (d, ", ".join(DIMENSOES)))
            continue
        marca = "✓" if d in respondidas else "·"
        out("%s %s" % (marca, d.upper()))
        for q in PERGUNTAS[d]:
            out("    – " + q)
        out()
    out("Regra de ouro: a IA LIDERA a conversa, o DONO DECIDE. Traduza todo termo")
    out("técnico para o dia a dia (veja references/traducao_de_termos.md) e registre")
    out("cada resposta com `responder --dimensao ... --pergunta ... --resposta '...'`.")
    out("O que o dono não souber fica [A CONFERIR] — nunca invente por ele.")

def cmd_responder(args):
    rows = read_rows("respostas")
    dim = norm_dimensao(args.dimensao or "")
    rows.append({
        "id": next_id(rows),
        "dimensao": dim,
        "pergunta": (args.pergunta or "").strip(),
        "resposta": (args.resposta or "").strip(),
        "criado": now_stamp(),
    })
    write_rows("respostas", rows)
    out("✓ Resposta registrada em [%s]." % (dim or "geral"))
    if dim and dim not in DIMENSOES:
        out("  (dimensão fora da lista padrão — ok, mas confira: %s)" % ", ".join(DIMENSOES))

def cmd_entrevista(args):
    rows = read_rows("respostas")
    title("ENTREVISTA — O QUE JÁ SABEMOS (fatos nas palavras do dono)")
    if not rows:
        out("Nada registrado ainda. Rode `perguntas` e depois `responder`.")
    else:
        for d in DIMENSOES:
            ans = [r for r in rows if _norm(r.get("dimensao")) == d]
            if ans:
                out("● " + d.upper())
                for r in ans:
                    out("   – " + (r.get("resposta") or "[A CONFERIR]"))
        extra = [r for r in rows if _norm(r.get("dimensao")) not in DIMENSOES]
        if extra:
            out("● OUTRAS")
            for r in extra:
                out("   – " + (r.get("resposta") or "[A CONFERIR]"))
    faltam = [d for d in DIMENSOES
              if not any(_norm(r.get("dimensao")) == d for r in rows)]
    out()
    if faltam:
        out("Dimensões ainda EM BRANCO ([A CONFERIR]): " + ", ".join(faltam))
    else:
        out("Todas as dimensões têm ao menos uma resposta. Pode traçar os requisitos.")

# ---------- cadeia problema → necessidade → requisito ----------

def cmd_problema_add(args):
    rows = read_rows("problemas")
    cod = next_codigo(rows, "CP")
    rows.append({
        "id": next_id(rows), "codigo": cod,
        "titulo": (args.titulo or "").strip(),
        "descricao": (args.descricao or "").strip(),
        "criado": now_stamp(),
    })
    write_rows("problemas", rows)
    out("✓ Problema %s cadastrado: %s" % (cod, para_conferir(args.titulo)))

def cmd_necessidade_add(args):
    probs = read_rows("problemas")
    codes = {p.get("codigo") for p in probs}
    alvo = (args.problema or "").strip().upper()
    rows = read_rows("necessidades")
    cod = next_codigo(rows, "CN")
    warn = ""
    if alvo and alvo not in codes:
        warn = "  ⚠ Problema %s não existe ainda — a cadeia ficará quebrada até você criá-lo." % alvo
    rows.append({
        "id": next_id(rows), "codigo": cod,
        "problema": alvo,
        "descricao": (args.descricao or "").strip(),
        "criado": now_stamp(),
    })
    write_rows("necessidades", rows)
    out("✓ Necessidade %s (do problema %s): %s" %
        (cod, para_conferir(alvo, "[SEM PROBLEMA]"), para_conferir(args.descricao)))
    if warn:
        out(warn)

def cmd_requisito_add(args):
    necs = read_rows("necessidades")
    ncodes = {n.get("codigo") for n in necs}
    tipo = norm_tipo(args.tipo)
    prefix = "RF" if tipo == "funcional" else "RNF"
    rows = read_rows("requisitos")
    cod = next_codigo(rows, prefix)
    alvo = (args.necessidade or "").strip().upper()
    prio = norm_prio(args.prioridade) or ""
    rows.append({
        "id": next_id(rows), "codigo": cod,
        "necessidade": alvo,
        "enunciado": (args.enunciado or "").strip(),
        "tipo": tipo,
        "porque": (args.porque or "").strip(),
        "criterio": (args.criterio or "").strip(),
        "validar": (args.validar or "").strip(),
        "prioridade": prio,
        "depende": (args.depende or "").strip().upper(),
        "criado": now_stamp(),
    })
    write_rows("requisitos", rows)
    out("✓ Requisito %s (%s): %s" % (cod, tipo, para_conferir(args.enunciado)))
    if alvo and alvo not in ncodes:
        out("  ⚠ Necessidade %s não existe — requisito ficará ÓRFÃO (candidato a cortar)." % alvo)
    if not alvo:
        out("  ⚠ Sem necessidade ligada — todo requisito deve traçar a um problema real.")
    if not (args.criterio or "").strip():
        out("  ⚠ Sem critério de aceite. Rode `detalhar --id %s --criterio '...'`." % (next_id(rows) - 1))

def _find_req(rows, ident):
    ident = (ident or "").strip()
    for r in rows:
        if str(r.get("id")) == ident or _norm(r.get("codigo")) == _norm(ident):
            return r
    return None

def cmd_detalhar(args):
    rows = read_rows("requisitos")
    r = _find_req(rows, args.id)
    if not r:
        out("Requisito não encontrado: %s" % args.id)
        return
    if args.enunciado is not None:
        r["enunciado"] = args.enunciado.strip()
    if args.porque is not None:
        r["porque"] = args.porque.strip()
    if args.criterio is not None:
        r["criterio"] = args.criterio.strip()
    if args.validar is not None:
        r["validar"] = args.validar.strip()
    if args.necessidade is not None:
        r["necessidade"] = args.necessidade.strip().upper()
    if args.depende is not None:
        r["depende"] = args.depende.strip().upper()
    if args.tipo is not None:
        r["tipo"] = norm_tipo(args.tipo)
    write_rows("requisitos", rows)
    out("✓ Requisito %s atualizado." % r.get("codigo"))
    _print_requisito(r, read_rows("problemas"), read_rows("necessidades"), rows)

def _nebuloso(r):
    """True se o enunciado usa termo vago e não há critério de aceite."""
    if (r.get("criterio") or "").strip():
        return False
    enun = _norm(r.get("enunciado"))
    return any((" " + v + " ") in (" " + enun + " ") or enun == v for v in VAGOS)

def _orfao(r, ncodes, pcodes, necs_by_code):
    """True se o requisito não traça até um problema existente."""
    nec = (r.get("necessidade") or "").strip().upper()
    if not nec or nec not in ncodes:
        return True
    prob = (necs_by_code.get(nec, {}) or {}).get("problema", "").strip().upper()
    return (not prob) or (prob not in pcodes)

def _print_requisito(r, probs, necs, reqs):
    pcodes = {p.get("codigo"): p for p in probs}
    ncodes = {n.get("codigo"): n for n in necs}
    out()
    out("%s  [%s]  %s" % (r.get("codigo"), r.get("tipo"),
                          PRIO_LABEL.get(r.get("prioridade"), "sem prioridade")))
    out("  Enunciado ...... " + para_conferir(r.get("enunciado")))
    out("  Porquê ......... " + para_conferir(r.get("porque")))
    out("  Critério aceite  " + para_conferir(r.get("criterio")))
    out("  Como validar ... " + para_conferir(r.get("validar")))
    nec = (r.get("necessidade") or "").strip().upper()
    if nec and nec in ncodes:
        prob = (ncodes[nec].get("problema") or "").strip().upper()
        cadeia = "%s ← %s" % (nec, prob if prob else "[SEM PROBLEMA]")
        out("  Traça para ..... " + cadeia)
    else:
        out("  Traça para ..... ⚠ ÓRFÃO (nenhum problema por trás — candidato a cortar)")
    if r.get("depende"):
        out("  Depende de ..... " + r.get("depende"))
    flags = []
    if _nebuloso(r):
        flags.append("NEBULOSO (termo vago sem critério — não é testável)")
    if flags:
        out("  ⚠ " + "; ".join(flags))

def cmd_requisito(args):
    reqs = read_rows("requisitos")
    probs = read_rows("problemas")
    necs = read_rows("necessidades")
    if args.id:
        r = _find_req(reqs, args.id)
        if not r:
            out("Requisito não encontrado: %s" % args.id)
            return
        _print_requisito(r, probs, necs, reqs)
        return
    if not reqs:
        out("Nenhum requisito ainda. Rode `requisito-add --necessidade CN.01 --enunciado '...'`.")
        return
    ncodes = {n.get("codigo") for n in necs}
    pcodes = {p.get("codigo") for p in probs}
    necs_by_code = {n.get("codigo"): n for n in necs}
    title("REQUISITOS (%d)" % len(reqs))
    for r in reqs:
        flags = []
        if _nebuloso(r):
            flags.append("nebuloso")
        if _orfao(r, ncodes, pcodes, necs_by_code):
            flags.append("órfão")
        if not (r.get("criterio") or "").strip():
            flags.append("sem critério")
        mark = ("  ⚠ " + ", ".join(flags)) if flags else ""
        out("  %-6s %-10s %s%s" % (
            r.get("codigo"),
            {"Must": "OBRIG.", "Should": "IMPORT.", "Could": "DESEJ.", "Wont": "FORA"}.get(r.get("prioridade"), "—"),
            para_conferir(r.get("enunciado")), mark))

# ---------- MoSCoW ----------

def cmd_prioridade(args):
    rows = read_rows("requisitos")
    r = _find_req(rows, args.id)
    if not r:
        out("Requisito não encontrado: %s" % args.id)
        return
    prio = norm_prio(args.nivel)
    if not prio:
        out("Nível inválido: %s. Use Obrigatório/Importante/Desejável/Fora "
            "(Must/Should/Could/Won't)." % args.nivel)
        return
    r["prioridade"] = prio
    write_rows("requisitos", rows)
    out("✓ %s → %s" % (r.get("codigo"), PRIO_LABEL[prio]))

def cmd_moscow(args):
    reqs = read_rows("requisitos")
    if not reqs:
        out("Nenhum requisito para priorizar ainda.")
        return
    by = {k: [] for k in PRIO_ORDER}
    sem = []
    for r in reqs:
        p = r.get("prioridade")
        (by[p] if p in by else sem).append(r) if p in by else sem.append(r)
    title("PRIORIZAÇÃO MoSCoW")
    for k in PRIO_ORDER:
        out("%s — %d" % (PRIO_LABEL[k], len(by[k])))
        for r in by[k]:
            out("   %-6s %s" % (r.get("codigo"), para_conferir(r.get("enunciado"))))
    if sem:
        out("SEM PRIORIDADE — %d (defina com `prioridade --id N --nivel ...`)" % len(sem))
        for r in sem:
            out("   %-6s %s" % (r.get("codigo"), para_conferir(r.get("enunciado"))))
    # MVP = os Obrigatórios
    musts = by["Must"]
    out()
    if musts:
        out("👉 O MVP (primeira versão útil) = os %d obrigatórios acima." % len(musts))
        semcrit = [r for r in musts if not (r.get("criterio") or "").strip()]
        if semcrit:
            out("   ⚠ %d obrigatório(s) SEM critério de aceite: %s"
                % (len(semcrit), ", ".join(r.get("codigo") for r in semcrit)))
    else:
        out("⚠ Nenhum requisito Obrigatório ainda — sem MVP definido. "
            "Marque os essenciais como Obrigatório.")
    # validador de dependência
    codes = {r.get("codigo"): r for r in reqs}
    problemas = []
    for r in reqs:
        dep = (r.get("depende") or "").strip().upper()
        if not dep:
            continue
        d = codes.get(dep)
        if not d:
            problemas.append("%s depende de %s, que NÃO existe." % (r.get("codigo"), dep))
            continue
        pv = PRIO_VALUE.get(r.get("prioridade"), 0)
        dv = PRIO_VALUE.get(d.get("prioridade"), 0)
        if pv and dv and dv < pv:
            problemas.append(
                "%s (%s) depende de %s (%s) — o mais importante não pode depender do menos importante."
                % (r.get("codigo"), PRIO_LABEL[r.get("prioridade")],
                   d.get("codigo"), PRIO_LABEL[d.get("prioridade")]))
    out()
    if problemas:
        out("⚠ DEPENDÊNCIAS A CORRIGIR:")
        for p in problemas:
            out("   – " + p)
    else:
        out("✓ Nenhuma dependência inválida entre requisitos.")

# ---------- escopo / contexto ----------

ESCOPO_TIPOS = {
    "dentro": "Dentro do escopo",
    "fora": "Fora do escopo",
    "depende": "Depende de terceiro",
    "bloqueado": "Bloqueado por decisão",
    "suposicao": "Suposição",
    "risco": "Risco",
    "restricao": "Restrição",
    "pergunta": "Pergunta em aberto",
}
def norm_escopo_tipo(s):
    n = _norm(s)
    alias = {"dependencia": "depende", "terceiro": "depende", "bloqueio": "bloqueado",
             "premissa": "suposicao", "assuncao": "suposicao", "duvida": "pergunta",
             "aberto": "pergunta", "limite": "restricao", "in": "dentro", "out": "fora"}
    n = alias.get(n, n)
    return n if n in ESCOPO_TIPOS else ""

def cmd_escopo_add(args):
    tipo = norm_escopo_tipo(args.tipo)
    if not tipo:
        out("Tipo inválido: %s. Use: %s" % (args.tipo, ", ".join(ESCOPO_TIPOS)))
        return
    rows = read_rows("escopo")
    rows.append({"id": next_id(rows), "tipo": tipo,
                 "texto": (args.texto or "").strip(), "criado": now_stamp()})
    write_rows("escopo", rows)
    out("✓ [%s] %s" % (ESCOPO_TIPOS[tipo], para_conferir(args.texto)))

def cmd_escopo(args):
    rows = read_rows("escopo")
    title("FRONTEIRA DE ESCOPO E CONTEXTO")
    if not rows:
        out("Nada registrado. Proteja o escopo: registre o que fica FORA com")
        out("`escopo-add --tipo fora --texto '...'` — é a defesa nº 1 contra retrabalho.")
        return
    ordem = ["dentro", "fora", "depende", "bloqueado", "restricao",
             "suposicao", "risco", "pergunta"]
    for t in ordem:
        items = [r for r in rows if r.get("tipo") == t]
        if items:
            out("● " + ESCOPO_TIPOS[t])
            for r in items:
                out("   – " + para_conferir(r.get("texto")))
    fora = [r for r in rows if r.get("tipo") == "fora"]
    if not fora:
        out()
        out("⚠ Nenhuma fronteira 'fora do escopo' definida. Sem ela, o projeto incha "
            "(escopo-creep). Diga explicitamente o que NÃO faz parte.")

# ---------- especificação: o documento ----------

def _gate(reqs, probs, necs, escopo, projeto):
    """Devolve lista de (nome, status 🟢/🟡/🔴, detalhe)."""
    ncodes = {n.get("codigo") for n in necs}
    pcodes = {p.get("codigo") for p in probs}
    necs_by_code = {n.get("codigo"): n for n in necs}
    g = []

    prob_central = (projeto.get(_norm("Problema central")) or "").strip()
    g.append(("Problema central definido",
              "🟢" if prob_central and "[A CONFERIR]" not in prob_central else "🔴",
              prob_central or "—"))

    completos = [r for r in reqs
                 if not _orfao(r, ncodes, pcodes, necs_by_code)
                 and (r.get("criterio") or "").strip()]
    g.append(("Cadeia problema→necessidade→requisito completa",
              "🟢" if completos else ("🟡" if reqs else "🔴"),
              "%d requisito(s) completo(s)" % len(completos)))

    sem_crit = [r for r in reqs if not (r.get("criterio") or "").strip()]
    g.append(("Todo requisito tem critério de aceite",
              "🟢" if reqs and not sem_crit else ("🔴" if sem_crit else "🟡"),
              ("faltam: " + ", ".join(r.get("codigo") for r in sem_crit)) if sem_crit else "ok"))

    nebul = [r for r in reqs if _nebuloso(r)]
    g.append(("Nenhum requisito nebuloso",
              "🟢" if not nebul else "🔴",
              ("nebulosos: " + ", ".join(r.get("codigo") for r in nebul)) if nebul else "ok"))

    orfaos = [r for r in reqs if _orfao(r, ncodes, pcodes, necs_by_code)]
    g.append(("Nenhum requisito órfão",
              "🟢" if reqs and not orfaos else ("🔴" if orfaos else "🟡"),
              ("órfãos: " + ", ".join(r.get("codigo") for r in orfaos)) if orfaos else "ok"))

    # dependências inválidas
    codes = {r.get("codigo"): r for r in reqs}
    dep_bad = []
    for r in reqs:
        dep = (r.get("depende") or "").strip().upper()
        if dep and dep in codes:
            pv = PRIO_VALUE.get(r.get("prioridade"), 0)
            dv = PRIO_VALUE.get(codes[dep].get("prioridade"), 0)
            if pv and dv and dv < pv:
                dep_bad.append(r.get("codigo"))
        elif dep and dep not in codes:
            dep_bad.append(r.get("codigo"))
    g.append(("Dependências coerentes",
              "🟢" if not dep_bad else "🔴",
              ("corrigir: " + ", ".join(dep_bad)) if dep_bad else "ok"))

    fora = [r for r in escopo if r.get("tipo") == "fora"]
    g.append(("Escopo tem fronteira (o que fica de fora)",
              "🟢" if fora else "🔴",
              "%d item(ns) fora do escopo" % len(fora)))

    musts = [r for r in reqs if r.get("prioridade") == "Must"]
    g.append(("MVP definido (há obrigatórios)",
              "🟢" if musts else "🔴",
              "%d obrigatório(s)" % len(musts)))

    perguntas = [r for r in escopo if r.get("tipo") == "pergunta"]
    g.append(("Perguntas em aberto resolvidas",
              "🟢" if not perguntas else "🟡",
              "%d em aberto" % len(perguntas)))
    return g

def cmd_especificacao(args):
    reqs = read_rows("requisitos")
    probs = read_rows("problemas")
    necs = read_rows("necessidades")
    escopo = read_rows("escopo")
    respostas = read_rows("respostas")
    projeto = _read_projeto()
    ncodes = {n.get("codigo"): n for n in necs}

    # próximo número de documento
    n = 1
    while os.path.exists(gpath("especificacao-%d.md" % n)):
        n += 1
    docpath = gpath("especificacao-%d.md" % n)

    L = []
    nome = para_conferir(projeto.get(_norm("Nome")))
    L.append("# Especificação — %s" % nome)
    L.append("")
    L.append("_Gerado pelo Gabarito em %s. Rascunho para o dono revisar, ajustar e aprovar._" % now_stamp())
    L.append("")
    L.append("## 1. Resumo")
    L.append("- **Para quem:** %s" % para_conferir(projeto.get(_norm("Para quem"))))
    L.append("- **Problema central:** %s" % para_conferir(projeto.get(_norm("Problema central"))))
    L.append("- **Domínio:** %s" % para_conferir(projeto.get(_norm("Domínio"))))
    L.append("")

    L.append("## 2. Problemas e necessidades")
    if probs:
        for p in probs:
            L.append("- **%s — %s**  \n  %s" % (
                p.get("codigo"), para_conferir(p.get("titulo")), para_conferir(p.get("descricao"))))
            for ne in [x for x in necs if (x.get("problema") or "").upper() == p.get("codigo")]:
                L.append("  - _%s_: %s" % (ne.get("codigo"), para_conferir(ne.get("descricao"))))
    else:
        L.append("- [A CONFERIR] — nenhum problema cadastrado.")
    L.append("")

    L.append("## 3. Requisitos")
    def bloco(tipo, titulo_sec):
        rs = [r for r in reqs if r.get("tipo") == tipo]
        if not rs:
            return
        L.append("### %s" % titulo_sec)
        for r in rs:
            nec = (r.get("necessidade") or "").upper()
            prob = (ncodes.get(nec, {}) or {}).get("problema", "")
            L.append("- **%s** — %s _(%s)_" % (
                r.get("codigo"), para_conferir(r.get("enunciado")),
                PRIO_LABEL.get(r.get("prioridade"), "sem prioridade")))
            L.append("  - Porquê: %s" % para_conferir(r.get("porque")))
            L.append("  - Critério de aceite: %s" % para_conferir(r.get("criterio")))
            L.append("  - Como validar: %s" % para_conferir(r.get("validar")))
            L.append("  - Traça para: %s ← %s" % (nec or "[SEM NECESSIDADE]", prob or "[SEM PROBLEMA]"))
        L.append("")
    bloco("funcional", "Funcionais (o que faz)")
    bloco("nao-funcional", "Não-funcionais (qualidade: desempenho, segurança, privacidade, disponibilidade)")
    if not reqs:
        L.append("- [A CONFERIR] — nenhum requisito cadastrado.")
        L.append("")

    L.append("## 4. Prioridade (MoSCoW) e MVP")
    for k in PRIO_ORDER:
        rs = [r for r in reqs if r.get("prioridade") == k]
        if rs:
            L.append("- **%s:** %s" % (PRIO_LABEL[k], ", ".join(r.get("codigo") for r in rs)))
    musts = [r for r in reqs if r.get("prioridade") == "Must"]
    L.append("- **MVP (primeira versão útil):** %s" %
             (", ".join(r.get("codigo") for r in musts) if musts else "[A CONFERIR]"))
    L.append("")

    L.append("## 5. Fronteira de escopo")
    for t, lab in [("fora", "Fora do escopo"), ("depende", "Depende de terceiro"),
                   ("bloqueado", "Bloqueado por decisão"), ("restricao", "Restrições")]:
        items = [r for r in escopo if r.get("tipo") == t]
        if items:
            L.append("**%s:**" % lab)
            for r in items:
                L.append("- %s" % para_conferir(r.get("texto")))
    if not any(r.get("tipo") == "fora" for r in escopo):
        L.append("- [A CONFERIR] — defina o que fica FORA do escopo.")
    L.append("")

    L.append("## 6. Suposições, riscos e perguntas em aberto")
    for t, lab in [("suposicao", "Suposições"), ("risco", "Riscos"), ("pergunta", "Perguntas em aberto")]:
        items = [r for r in escopo if r.get("tipo") == t]
        if items:
            L.append("**%s:**" % lab)
            for r in items:
                L.append("- %s" % para_conferir(r.get("texto")))
    L.append("")

    L.append("## 7. Critérios de sucesso")
    suc = [r for r in respostas if _norm(r.get("dimensao")) == "sucesso"]
    if suc:
        for r in suc:
            L.append("- %s" % para_conferir(r.get("resposta")))
    else:
        L.append("- [A CONFERIR] — como saberemos que deu certo? (número/meta)")
    L.append("")

    L.append("## 8. Aceite")
    L.append("- [ ] O dono revisou e concorda que esta especificação descreve o que precisa ser construído.")
    L.append("- [ ] Os itens [A CONFERIR] foram preenchidos ou marcados como pergunta em aberto.")
    L.append("- **Data / responsável:** ______________________")
    L.append("")

    with open(docpath, "w", encoding="utf-8") as f:
        f.write("\n".join(L) + "\n")

    title("ESPECIFICAÇÃO GERADA")
    out("Documento salvo em: " + docpath)
    out()
    out("PRONTO PARA CONSTRUIR? (portões de qualidade)")
    g = _gate(reqs, probs, necs, escopo, projeto)
    verdes = sum(1 for _, s, _ in g if s == "🟢")
    for nome_g, status, det in g:
        out("  %s %-46s %s" % (status, nome_g, det))
    out()
    if verdes == len(g):
        out("🟢 Tudo verde — especificação sólida. Próximo passo: leve ao Prumo (planejar")
        out("   o build) ou ao seu desenvolvedor. Nada aqui foi inventado — o que está")
        out("   [A CONFERIR] precisa do dono.")
    else:
        vermelhos = [n for n, s, _ in g if s == "🔴"]
        out("🟡 Ainda há pontos a fechar antes de construir: " +
            (", ".join(vermelhos) if vermelhos else "veja os 🟡 acima") + ".")
        out("   Use `plano` para a ordem de ataque. Construir com estes furos = retrabalho.")

def cmd_painel(args):
    reqs = read_rows("requisitos")
    probs = read_rows("problemas")
    necs = read_rows("necessidades")
    escopo = read_rows("escopo")
    respostas = read_rows("respostas")
    projeto = _read_projeto()
    ncodes = {n.get("codigo") for n in necs}
    pcodes = {p.get("codigo") for p in probs}
    necs_by_code = {n.get("codigo"): n for n in necs}
    title("PAINEL — RAIO-X DA ESPECIFICAÇÃO")
    out("Projeto ............ " + para_conferir(projeto.get(_norm("Nome"))))
    out("Problemas .......... %d" % len(probs))
    out("Necessidades ....... %d" % len(necs))
    out("Requisitos ......... %d  (funcionais %d / não-funcionais %d)" % (
        len(reqs),
        sum(1 for r in reqs if r.get("tipo") == "funcional"),
        sum(1 for r in reqs if r.get("tipo") == "nao-funcional")))
    musts = sum(1 for r in reqs if r.get("prioridade") == "Must")
    out("MVP (obrigatórios) . %d" % musts)
    sem_crit = sum(1 for r in reqs if not (r.get("criterio") or "").strip())
    nebul = sum(1 for r in reqs if _nebuloso(r))
    orf = sum(1 for r in reqs if _orfao(r, ncodes, pcodes, necs_by_code))
    out("Sem critério ....... %d" % sem_crit)
    out("Nebulosos .......... %d" % nebul)
    out("Órfãos ............. %d" % orf)
    out("Fora do escopo ..... %d" % sum(1 for r in escopo if r.get("tipo") == "fora"))
    out("Perguntas em aberto  %d" % sum(1 for r in escopo if r.get("tipo") == "pergunta"))
    dims_resp = set(_norm(r.get("dimensao")) for r in respostas)
    faltam = [d for d in DIMENSOES if d not in dims_resp]
    out("Entrevista ......... %d/%d dimensões" % (len(DIMENSOES) - len(faltam), len(DIMENSOES)))

def cmd_plano(args):
    reqs = read_rows("requisitos")
    probs = read_rows("problemas")
    necs = read_rows("necessidades")
    escopo = read_rows("escopo")
    projeto = _read_projeto()
    respostas = read_rows("respostas")
    ncodes = {n.get("codigo") for n in necs}
    pcodes = {p.get("codigo") for p in probs}
    necs_by_code = {n.get("codigo"): n for n in necs}
    acoes = []

    prob_central = (projeto.get(_norm("Problema central")) or "").strip()
    if not prob_central or "[A CONFERIR]" in prob_central:
        acoes.append(("🔴", "Defina o problema central do projeto (rode `novo` ou entreviste o dono)."))

    dims_resp = set(_norm(r.get("dimensao")) for r in respostas)
    faltam = [d for d in DIMENSOES if d not in dims_resp]
    if faltam:
        acoes.append(("🟡", "Complete a entrevista nas dimensões: " + ", ".join(faltam) + "."))

    perguntas = [r for r in escopo if r.get("tipo") == "pergunta"]
    for r in perguntas:
        acoes.append(("🔴", "Resolva a pergunta em aberto: " + para_conferir(r.get("texto"))))

    for r in reqs:
        if not (r.get("criterio") or "").strip():
            acoes.append(("🔴", "%s sem critério de aceite — rode `detalhar --id %s --criterio '...'`."
                          % (r.get("codigo"), r.get("id"))))
    for r in reqs:
        if _nebuloso(r):
            acoes.append(("🔴", "%s é nebuloso — troque o adjetivo vago por um número/critério testável."
                          % r.get("codigo")))
    for r in reqs:
        if _orfao(r, ncodes, pcodes, necs_by_code):
            acoes.append(("🟡", "%s é órfão — ligue-o a uma necessidade/problema, ou corte-o." % r.get("codigo")))

    if not any(r.get("tipo") == "fora" for r in escopo):
        acoes.append(("🔴", "Defina o que fica FORA do escopo (`escopo-add --tipo fora --texto '...'`)."))

    if not any(r.get("prioridade") == "Must" for r in reqs):
        acoes.append(("🟡", "Marque os requisitos essenciais como Obrigatório para desenhar o MVP."))

    title("PLANO — O QUE FECHAR ANTES DE CONSTRUIR")
    if not acoes:
        out("🟢 Nada pendente. A especificação está pronta para virar build.")
        out("   Gere/atualize o documento com `especificacao` e leve ao Prumo ou ao dev.")
        return
    # 🔴 antes de 🟡
    for sev in ("🔴", "🟡"):
        for s, txt in acoes:
            if s == sev:
                out("%s %s" % (s, txt))

# ----------------------------------------------------------------------------
# CLI
# ----------------------------------------------------------------------------

def build_parser():
    p = argparse.ArgumentParser(
        prog="gabarito",
        description="Elicitação de requisitos e especificação — construa a coisa certa.")
    sub = p.add_subparsers(dest="cmd")

    sub.add_parser("init")

    s = sub.add_parser("novo")
    s.add_argument("--nome"); s.add_argument("--para"); s.add_argument("--problema"); s.add_argument("--dominio")

    sub.add_parser("projeto")

    s = sub.add_parser("perguntas"); s.add_argument("--dimensao")

    s = sub.add_parser("responder")
    s.add_argument("--dimensao", required=True); s.add_argument("--pergunta", default="")
    s.add_argument("--resposta", required=True)

    sub.add_parser("entrevista")

    s = sub.add_parser("problema-add")
    s.add_argument("--titulo", required=True); s.add_argument("--descricao", default="")

    s = sub.add_parser("necessidade-add")
    s.add_argument("--problema", required=True); s.add_argument("--descricao", required=True)

    s = sub.add_parser("requisito-add")
    s.add_argument("--necessidade", default=""); s.add_argument("--enunciado", required=True)
    s.add_argument("--tipo", default="funcional"); s.add_argument("--porque", default="")
    s.add_argument("--criterio", default=""); s.add_argument("--validar", default="")
    s.add_argument("--prioridade", default=""); s.add_argument("--depende", default="")

    s = sub.add_parser("detalhar")
    s.add_argument("--id", required=True)
    s.add_argument("--enunciado"); s.add_argument("--porque"); s.add_argument("--criterio")
    s.add_argument("--validar"); s.add_argument("--necessidade"); s.add_argument("--depende")
    s.add_argument("--tipo")

    s = sub.add_parser("requisito"); s.add_argument("--id")

    s = sub.add_parser("prioridade")
    s.add_argument("--id", required=True); s.add_argument("--nivel", required=True)

    sub.add_parser("moscow")

    s = sub.add_parser("escopo-add")
    s.add_argument("--tipo", required=True); s.add_argument("--texto", required=True)

    sub.add_parser("escopo")
    sub.add_parser("especificacao")
    sub.add_parser("documento")
    sub.add_parser("painel")
    sub.add_parser("plano")
    return p

DISPATCH = {
    "init": cmd_init, "novo": cmd_novo, "projeto": cmd_projeto,
    "perguntas": cmd_perguntas, "responder": cmd_responder, "entrevista": cmd_entrevista,
    "problema-add": cmd_problema_add, "necessidade-add": cmd_necessidade_add,
    "requisito-add": cmd_requisito_add, "detalhar": cmd_detalhar, "requisito": cmd_requisito,
    "prioridade": cmd_prioridade, "moscow": cmd_moscow,
    "escopo-add": cmd_escopo_add, "escopo": cmd_escopo,
    "especificacao": cmd_especificacao, "documento": cmd_especificacao,
    "painel": cmd_painel, "plano": cmd_plano,
}

def main(argv=None):
    parser = build_parser()
    args = parser.parse_args(argv)
    if not args.cmd:
        parser.print_help()
        return 0
    fn = DISPATCH.get(args.cmd)
    if not fn:
        parser.print_help()
        return 1
    fn(args)
    return 0

if __name__ == "__main__":
    sys.exit(main())
