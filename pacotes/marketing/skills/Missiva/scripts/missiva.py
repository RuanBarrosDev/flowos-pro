#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Missiva — motor local do canal de e-mail marketing & newsletter.
100% biblioteca padrao do Python. Nao conecta em lugar nenhum: le e escreve
arquivos locais dentro de .missiva/ na raiz do seu projeto.

Regra de ouro embutida: nunca inventa contato, metrica nem resultado. O que
falta vira [A PREENCHER] ou "faltou dado" visivel. Consentimento e obrigatorio.
"""

import argparse
import csv
import os
import re
import sys
from pathlib import Path

# ----------------------------------------------------------------------------
# Ancoragem: onde fica a pasta .missiva/
# ----------------------------------------------------------------------------

def achar_raiz():
    """Descobre a raiz do projeto de forma robusta (independe do diretorio atual).
    Ordem: CLAUDE_PROJECT_DIR -> sobe procurando .missiva/.git/.claude -> cwd."""
    env = os.environ.get("CLAUDE_PROJECT_DIR")
    if env and Path(env).is_dir():
        return Path(env)
    atual = Path.cwd().resolve()
    for base in [atual, *atual.parents]:
        for marca in (".missiva", ".git", ".claude"):
            if (base / marca).exists():
                return base
    return atual


RAIZ = achar_raiz()
DIR = RAIZ / ".missiva"
CONFIG = DIR / "config.md"
CONTATOS = DIR / "contatos.csv"
CAMPANHAS = DIR / "campanhas.csv"
SEQ_DIR = DIR / "sequencias"

VAZIO = "[A PREENCHER]"

# ----------------------------------------------------------------------------
# Utilidades
# ----------------------------------------------------------------------------

def sem_acento(s):
    tab = str.maketrans("aaaaaeeeiooooouuc", "aaaaaeeeiooooouuc")
    s = s.lower().strip()
    for a, b in [("á","a"),("à","a"),("ã","a"),("â","a"),("é","e"),("ê","e"),
                 ("í","i"),("ó","o"),("ô","o"),("õ","o"),("ú","u"),("ç","c")]:
        s = s.replace(a, b)
    return s.translate(tab)


def garantir_dir():
    DIR.mkdir(parents=True, exist_ok=True)
    SEQ_DIR.mkdir(parents=True, exist_ok=True)


def ler_config():
    """Le config.md no formato '- **Rotulo:** valor' (insensivel a acento)."""
    dados = {}
    if not CONFIG.exists():
        return dados
    for linha in CONFIG.read_text(encoding="utf-8").splitlines():
        m = re.match(r"\s*[-*]\s*\*\*(.+?):\*\*\s*(.*)", linha)
        if m:
            dados[sem_acento(m.group(1))] = m.group(2).strip()
    return dados


def cfg(dados, *chaves, padrao=VAZIO):
    for c in chaves:
        v = dados.get(sem_acento(c), "")
        if v and v != VAZIO:
            return v
    return padrao


RE_EMAIL = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


def email_valido(e):
    return bool(RE_EMAIL.match((e or "").strip()))


CONSENT_OK = {"confirmado", "sim", "optin", "opt-in", "duplo optin", "double optin", "s"}
CONSENT_NAO = {"negado", "nao", "n", "descadastrou", "revogado"}


def canon_consent(v):
    s = sem_acento(v or "").replace(" ", "")
    if s in {sem_acento(x).replace(" ", "") for x in CONSENT_OK}:
        return "confirmado"
    if s in {sem_acento(x).replace(" ", "") for x in CONSENT_NAO}:
        return "negado"
    return "desconhecido"


STATUS_SUPRIMIDO = {"descadastrado", "bounce", "reclamacao", "reclamou", "invalido"}


def status_canon(v):
    s = sem_acento(v or "")
    if s in STATUS_SUPRIMIDO:
        return "descadastrado" if s == "descadastrado" else s
    return s or "ativo"


def suprimido(status, consent):
    return status_canon(status) in STATUS_SUPRIMIDO or canon_consent(consent) == "negado"


def pct(n, d):
    return (100.0 * n / d) if d else 0.0


def ler_contatos():
    if not CONTATOS.exists():
        return []
    with CONTATOS.open(encoding="utf-8") as f:
        return list(csv.DictReader(f))


CAB_CONTATOS = ["email", "nome", "empresa", "segmento", "consentimento", "status", "origem", "data_entrada"]


def salvar_contatos(linhas):
    garantir_dir()
    with CONTATOS.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=CAB_CONTATOS)
        w.writeheader()
        for l in linhas:
            w.writerow({k: l.get(k, "") for k in CAB_CONTATOS})


def exigir_config(dados):
    if not dados:
        print("⚠️  Ainda nao existe .missiva/config.md. Rode o modo Preparar (primeira vez).")
        sys.exit(2)


# ----------------------------------------------------------------------------
# setup / config
# ----------------------------------------------------------------------------

def cmd_setup(a):
    garantir_dir()
    linhas = [
        "# Configuracao da Missiva",
        "",
        "> Preenchido na primeira conversa. Fica so no seu computador (.missiva/, git-ignored).",
        "",
        f"- **Nome do negocio:** {a.negocio or VAZIO}",
        f"- **Responsavel:** {a.responsavel or VAZIO}",
        f"- **Nicho/area:** {a.nicho or VAZIO}",
        f"- **Nome do remetente (from-name):** {a.remetente or VAZIO}",
        f"- **E-mail de resposta (reply-to):** {a.reply_to or VAZIO}",
        f"- **Endereco fisico (rodape/CAN-SPAM/LGPD):** {a.endereco or VAZIO}",
        f"- **Ferramenta de envio (ESP):** {a.esp or VAZIO}",
        f"- **Tom de voz:** {a.tom or VAZIO}",
        f"- **Link de descadastro disponivel:** {a.descadastro or VAZIO}",
        "",
    ]
    CONFIG.write_text("\n".join(linhas), encoding="utf-8")
    # garante .missiva/ no .gitignore da raiz
    gi = RAIZ / ".gitignore"
    marca = ".missiva/"
    atual = gi.read_text(encoding="utf-8") if gi.exists() else ""
    if marca not in atual:
        with gi.open("a", encoding="utf-8") as f:
            if atual and not atual.endswith("\n"):
                f.write("\n")
            f.write(marca + "\n")
    print(f"✅ Config gravada em {CONFIG}")
    print("✅ .missiva/ garantido no .gitignore")


def cmd_autodestruir_setup(a):
    """Remove a pasta setup/ ao lado do script (independe do diretorio atual)."""
    aqui = Path(__file__).resolve().parent
    for cand in (aqui / "setup", aqui.parent / "setup"):
        if cand.is_dir():
            for p in sorted(cand.rglob("*"), reverse=True):
                p.unlink() if p.is_file() else p.rmdir()
            cand.rmdir()
            print(f"✅ Pasta de setup removida: {cand}")
            return
    print("ℹ️  Nenhuma pasta setup/ encontrada (ja limpa).")


def cmd_config(a):
    dados = ler_config()
    exigir_config(dados)
    print("# Configuracao atual\n")
    print(CONFIG.read_text(encoding="utf-8"))


# ----------------------------------------------------------------------------
# base — lista & segmentos
# ----------------------------------------------------------------------------

def _mapear_colunas(linha):
    m = {}
    for k in linha:
        kk = sem_acento(k)
        if kk in ("email", "e-mail", "mail"):
            m["email"] = k
        elif kk in ("nome", "name", "primeiro nome"):
            m["nome"] = k
        elif kk in ("empresa", "company", "negocio"):
            m["empresa"] = k
        elif kk in ("segmento", "segment", "tag", "grupo", "interesse"):
            m["segmento"] = k
        elif kk in ("consentimento", "consent", "optin", "opt-in", "permissao"):
            m["consentimento"] = k
        elif kk in ("status", "situacao"):
            m["status"] = k
        elif kk in ("origem", "source", "fonte"):
            m["origem"] = k
        elif kk in ("data_entrada", "data", "entrada", "date"):
            m["data_entrada"] = k
    return m


def cmd_base_importar(a):
    caminho = Path(a.arquivo)
    if not caminho.exists():
        print(f"⚠️  Arquivo nao encontrado: {caminho}")
        sys.exit(1)
    with caminho.open(encoding="utf-8-sig") as f:
        entrada = list(csv.DictReader(f))
    if not entrada:
        print("⚠️  CSV vazio ou sem cabecalho.")
        sys.exit(1)
    mapa = _mapear_colunas(entrada[0])
    if "email" not in mapa:
        print("⚠️  Nao achei uma coluna de e-mail no CSV (esperado: email / e-mail / mail).")
        sys.exit(1)

    existentes = {l["email"].strip().lower(): l for l in ler_contatos()}
    novos = 0
    invalidos = 0
    dup = 0
    for r in entrada:
        email = (r.get(mapa["email"], "") or "").strip().lower()
        if not email_valido(email):
            invalidos += 1
            continue
        if email in existentes:
            dup += 1
            continue
        existentes[email] = {
            "email": email,
            "nome": r.get(mapa.get("nome", ""), ""),
            "empresa": r.get(mapa.get("empresa", ""), ""),
            "segmento": (r.get(mapa.get("segmento", ""), "") or a.segmento or ""),
            "consentimento": canon_consent(r.get(mapa.get("consentimento", ""), "") or a.consentimento or ""),
            "status": status_canon(r.get(mapa.get("status", ""), "")),
            "origem": (r.get(mapa.get("origem", ""), "") or a.origem or ""),
            "data_entrada": r.get(mapa.get("data_entrada", ""), ""),
        }
        novos += 1
    salvar_contatos(list(existentes.values()))
    print(f"✅ Importados {novos} novos contato(s). Duplicados ignorados: {dup}. E-mails invalidos descartados: {invalidos}.")
    desconhecidos = sum(1 for l in existentes.values() if canon_consent(l.get("consentimento")) == "desconhecido")
    if desconhecidos:
        print(f"⚠️  {desconhecidos} contato(s) sem consentimento confirmado. Antes de disparar, confirme o opt-in ou nao envie (LGPD).")


def cmd_base_higiene(a):
    linhas = ler_contatos()
    if not linhas:
        print("ℹ️  Sua lista ainda esta vazia. Importe um CSV com o modo Base.")
        return
    total = len(linhas)
    vistos = {}
    dedup = []
    invalidos = 0
    for l in linhas:
        e = l["email"].strip().lower()
        if not email_valido(e):
            invalidos += 1
            continue
        if e in vistos:
            continue
        vistos[e] = True
        dedup.append(l)
    suprimidos = sum(1 for l in dedup if suprimido(l.get("status"), l.get("consentimento")))
    desconhecidos = sum(1 for l in dedup if canon_consent(l.get("consentimento")) == "desconhecido")
    ativos = sum(1 for l in dedup if not suprimido(l.get("status"), l.get("consentimento")) and canon_consent(l.get("consentimento")) == "confirmado")
    if a.aplicar:
        salvar_contatos(dedup)
    print("# Higiene da lista\n")
    print(f"- Total no arquivo: {total}")
    print(f"- E-mails invalidos: {invalidos}")
    print(f"- Duplicados removidos: {total - len(dedup) - invalidos}")
    print(f"- Suprimidos (descadastro/bounce/reclamacao/consent negado): {suprimidos}")
    print(f"- Sem consentimento confirmado (NAO enviar ate confirmar): {desconhecidos}")
    print(f"- Enviaveis hoje (ativos + opt-in confirmado): {ativos}")
    if not a.aplicar:
        print("\n(Isso foi so um diagnostico. Rode com --aplicar para gravar a lista limpa/deduplicada.)")
    else:
        print("\n✅ Lista limpa e deduplicada gravada.")


def cmd_base_segmentos(a):
    linhas = ler_contatos()
    if not linhas:
        print("ℹ️  Lista vazia.")
        return
    por_seg = {}
    for l in linhas:
        seg = (l.get("segmento") or "(sem segmento)").strip() or "(sem segmento)"
        d = por_seg.setdefault(seg, {"total": 0, "enviaveis": 0})
        d["total"] += 1
        if not suprimido(l.get("status"), l.get("consentimento")) and canon_consent(l.get("consentimento")) == "confirmado":
            d["enviaveis"] += 1
    print("# Segmentos\n")
    print(f"{'Segmento':<28}{'Total':>8}{'Enviaveis':>12}")
    print("-" * 48)
    for seg, d in sorted(por_seg.items(), key=lambda kv: -kv[1]["total"]):
        print(f"{seg[:27]:<28}{d['total']:>8}{d['enviaveis']:>12}")
    peq = [s for s, d in por_seg.items() if d["enviaveis"] < 200 and s != "(sem segmento)"]
    if peq:
        print("\nℹ️  Dica: segmento com menos de ~200 pessoas raramente compensa o custo de segmentar.")
        print("   Qualidade > tamanho, mas nao super-segmente lista pequena.")


# ----------------------------------------------------------------------------
# sequencia — automacoes de ciclo de vida
# ----------------------------------------------------------------------------

RECEITAS = {
    "boas-vindas": {
        "nome": "Sequencia de boas-vindas",
        "gatilho": "Novo contato entra na lista (formulario, isca digital, indicacao)",
        "objetivo_ex": "Ativar o novo inscrito e levar a primeira acao em ate 30 dias",
        "saida": "Comprou / respondeu / passou para a nutricao recorrente",
        "emails": [
            "Dia 0 — Entrega o que foi prometido (a isca) + boas-vindas + o que esperar",
            "Dia 2 — Sua historia / por que voce faz isso (conexao) + 1 recurso util",
            "Dia 4 — Prova: caso real, depoimento ou resultado (sem vender ainda)",
            "Dia 6 — A oferta certa para quem acabou de chegar + 1 CTA claro",
            "Dia 9 — Quebra de objecao + reforco da oferta com prazo/limite honesto",
        ],
    },
    "nutricao": {
        "nome": "Sequencia de nutricao (relacionamento)",
        "gatilho": "Terminou as boas-vindas e nao comprou / lead morno",
        "objetivo_ex": "Manter presenca e educar ate a pessoa estar pronta para comprar",
        "saida": "Comprou / clicou numa oferta / ficou inativo (vai para reengajamento)",
        "emails": [
            "Semana 1 — Dica pratica que resolve uma dor pequena (valor puro)",
            "Semana 2 — Erro comum do nicho + como evitar",
            "Semana 3 — Caso de cliente (antes/depois) com prova",
            "Semana 4 — Oferta suave conectada ao conteudo das semanas anteriores",
        ],
    },
    "carrinho": {
        "nome": "Recuperacao de carrinho / proposta abandonada",
        "gatilho": "Iniciou compra/checkout/proposta e nao concluiu",
        "objetivo_ex": "Recuperar a venda que estava a um passo de fechar",
        "saida": "Concluiu a compra ou pediu para sair",
        "emails": [
            "1h depois — 'Esqueceu algo?' + link direto para concluir",
            "24h depois — Quebra da objecao provavel (frete, duvida, confianca) + prova",
            "48h depois — Ultimo lembrete honesto (sem falsa escassez)",
        ],
    },
    "pos-compra": {
        "nome": "Sequencia pos-compra (retencao / LTV)",
        "gatilho": "Cliente comprou / fechou o servico",
        "objetivo_ex": "Garantir sucesso no uso, reduzir arrependimento e abrir recompra",
        "saida": "Passa para a base de clientes ativos (handoff para o Ancora)",
        "emails": [
            "Dia 0 — Confirmacao + proximos passos claros (o que acontece agora)",
            "Dia 3 — Como extrair o maximo / primeiro resultado rapido",
            "Dia 10 — Pedido de feedback ou avaliacao (handoff para o Aplauso)",
            "Dia 20 — Oferta de recompra / upgrade / produto complementar",
        ],
    },
    "reengajamento": {
        "nome": "Reengajamento / win-back",
        "gatilho": "Contato sem abrir/clicar ha 60-90 dias",
        "objetivo_ex": "Recuperar quem esfriou OU limpar a lista com dignidade",
        "saida": "Reengajou (volta a ativa) OU vai para supressao (sunset)",
        "emails": [
            "E-mail 1 — 'Ainda quer receber?' + melhor conteudo recente",
            "E-mail 2 — Incentivo/novidade para reativar o clique",
            "E-mail 3 — Despedida honesta: 'vou parar de te enviar' + botao de ficar",
        ],
    },
    "aniversario": {
        "nome": "Data comemorativa / aniversario",
        "gatilho": "Data do contato (aniversario, aniversario de cliente)",
        "objetivo_ex": "Gerar carinho e uma venda leve numa data pessoal",
        "saida": "Envio unico anual",
        "emails": [
            "No dia — Mensagem pessoal + mimo/beneficio exclusivo com validade",
        ],
    },
}


def cmd_sequencia_nova(a):
    tipo = sem_acento(a.tipo)
    chave = None
    for k in RECEITAS:
        if sem_acento(k) == tipo or tipo in sem_acento(k):
            chave = k
            break
    if not chave:
        print("Tipos disponiveis: " + ", ".join(RECEITAS))
        sys.exit(1)
    garantir_dir()
    r = RECEITAS[chave]
    slug = a.slug or chave
    caminho = SEQ_DIR / f"{slug}.md"
    linhas = [
        f"# {r['nome']}",
        "",
        f"- **Gatilho:** {r['gatilho']}",
        f"- **Objetivo (edite para ficar mensuravel):** {a.objetivo or r['objetivo_ex']} {VAZIO if not a.objetivo else ''}".strip(),
        f"- **Condicao de saida:** {r['saida']}",
        f"- **Segmento-alvo:** {a.segmento or VAZIO}",
        "",
        "## Roteiro (esqueleto — a copy fina de cada e-mail voce escreve no modo Escrita ou delega ao Verbo)",
        "",
    ]
    for i, e in enumerate(r["emails"], 1):
        linhas += [f"### E-mail {i} — {e}",
                   f"- Assunto: {VAZIO}",
                   f"- Preview: {VAZIO}",
                   f"- CTA unico: {VAZIO}",
                   ""]
    linhas += [
        "## Antes de ligar no ESP",
        "- Todo e-mail precisa de descadastro em 1 clique + endereco fisico no rodape.",
        "- Defina a condicao de saida no ESP (senao a pessoa recebe fora de hora).",
        "- Rode o modo Disparo (pre-voo) antes de publicar.",
        "",
    ]
    caminho.write_text("\n".join(linhas), encoding="utf-8")
    print(f"✅ Sequencia '{r['nome']}' criada em {caminho}")
    print("   Preencha os campos [A PREENCHER] com a ajuda do modo Escrita.")


def cmd_sequencia_listar(a):
    if not SEQ_DIR.exists() or not any(SEQ_DIR.glob("*.md")):
        print("ℹ️  Nenhuma sequencia criada ainda. Use: sequencia nova <tipo>")
        print("   Tipos: " + ", ".join(RECEITAS))
        return
    print("# Sequencias desenhadas\n")
    for p in sorted(SEQ_DIR.glob("*.md")):
        txt = p.read_text(encoding="utf-8")
        pend = txt.count(VAZIO)
        titulo = txt.splitlines()[0].lstrip("# ").strip()
        marca = "🟢 pronta" if pend == 0 else f"🟡 {pend} campo(s) [A PREENCHER]"
        print(f"- {p.stem}: {titulo}  ({marca})")


# ----------------------------------------------------------------------------
# newsletter — calendario editorial
# ----------------------------------------------------------------------------

def cmd_newsletter(a):
    freq = sem_acento(a.frequencia)
    n = max(1, a.edicoes)
    mapa = {"semanal": 7, "quinzenal": 14, "mensal": 30, "bissemanal": 3}
    passo = mapa.get(freq, 7)
    temas_base = [
        "Ensino: um passo pratico que o leitor aplica hoje",
        "Bastidor: como voce/ um cliente resolveu um problema real",
        "Curadoria: 3 coisas uteis que voce viu na semana",
        "Historia + licao: um caso com comeco, meio e aprendizado",
        "Pergunta da audiencia respondida a fundo",
        "Mito x verdade do seu nicho",
        "Oferta com contexto (a cada ~5 edicoes, nao toda vez)",
    ]
    print(f"# Calendario de newsletter — {a.frequencia}, {n} edicoes\n")
    print("Proporcao saudavel: ~80% valor / conteudo, ~20% oferta. Nunca so venda.\n")
    dia = 0
    for i in range(n):
        tema = temas_base[i % len(temas_base)]
        eh_oferta = (i + 1) % 5 == 0
        rotulo = "  [pode ter oferta]" if eh_oferta else ""
        print(f"Edicao {i+1} (dia +{dia}): {tema}{rotulo}")
        print(f"   Assunto: {VAZIO}   |   Seção principal: {VAZIO}   |   CTA: {VAZIO}")
        dia += passo
    print("\nDica de constancia: escolha a MENOR frequencia que voce sustenta por 6 meses.")
    print("Newsletter irregular perde mais do que newsletter menos frequente.")


# ----------------------------------------------------------------------------
# campanha — registrar metricas coladas do ESP
# ----------------------------------------------------------------------------

CAB_CAMP = ["data", "nome", "tipo", "enviados", "aberturas", "cliques", "descadastros", "bounces", "reclamacoes"]


def _num(v):
    try:
        return int(str(v).strip().replace(".", "").replace(",", ""))
    except (ValueError, AttributeError):
        return None


def cmd_campanha_registrar(a):
    garantir_dir()
    existe = CAMPANHAS.exists()
    with CAMPANHAS.open("a", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=CAB_CAMP)
        if not existe:
            w.writeheader()
        w.writerow({
            "data": a.data or "", "nome": a.nome, "tipo": a.tipo or "campanha",
            "enviados": a.enviados if a.enviados is not None else "",
            "aberturas": a.aberturas if a.aberturas is not None else "",
            "cliques": a.cliques if a.cliques is not None else "",
            "descadastros": a.descadastros if a.descadastros is not None else "",
            "bounces": a.bounces if a.bounces is not None else "",
            "reclamacoes": a.reclamacoes if a.reclamacoes is not None else "",
        })
    print(f"✅ Metricas de '{a.nome}' registradas. Rode o modo Painel para o diagnostico.")


def _diagnostico(row):
    env = _num(row.get("enviados"))
    if not env:
        return "⚠️  FALTOU DADO", "Sem numero de enviados nao da para calcular nada. Cole os enviados."
    ab = _num(row.get("aberturas"))
    cl = _num(row.get("cliques"))
    de = _num(row.get("descadastros"))
    bo = _num(row.get("bounces"))
    re_ = _num(row.get("reclamacoes"))
    if re_ is not None and pct(re_, env) >= 0.1:
        return "🔴 ENTREGABILIDADE EM RISCO", (
            f"Reclamacao de spam em {pct(re_, env):.2f}% (limite saudavel < 0,1%). "
            "Pare de enviar para inativos, revise consentimento e reduza frequencia AGORA.")
    if bo is not None and pct(bo, env) >= 2:
        return "🔴 HIGIENE URGENTE", (
            f"Bounce em {pct(bo, env):.1f}% (acima de 2% queima sua reputacao). "
            "Limpe a lista (modo Base > higiene) e nunca use lista comprada.")
    if de is not None and pct(de, env) >= 0.5:
        return "🟡 FADIGA / RELEVANCIA", (
            f"Descadastro em {pct(de, env):.2f}% (acima de ~0,5%). "
            "Segmente melhor, reduza frequencia ou aumente o valor por e-mail.")
    if ab is not None and pct(ab, env) < 15:
        return "🟡 ASSUNTO / CAIXA DE SPAM", (
            f"Abertura em {pct(ab, env):.1f}% (baixa). Teste assuntos (modo Escrita) "
            "e cheque entregabilidade/autenticacao.")
    if cl is not None and pct(cl, env) < 1:
        return "🟡 OFERTA / CTA FRACO", (
            f"Clique em {pct(cl, env):.2f}% (baixo). Reveja se a oferta bate com o segmento e "
            "deixe UM CTA claro.")
    return "🟢 SAUDAVEL", "Metricas dentro do esperado. Documente o que funcionou e repita."


def cmd_painel(a):
    dados = ler_config()
    exigir_config(dados)
    linhas = []
    if CAMPANHAS.exists():
        with CAMPANHAS.open(encoding="utf-8") as f:
            linhas = list(csv.DictReader(f))
    print("# Painel Missiva — metricas viram decisao\n")
    print(f"Negocio: {cfg(dados, 'Nome do negocio')}   |   Remetente: {cfg(dados, 'Nome do remetente (from-name)', 'Nome do remetente')}\n")
    contatos = ler_contatos()
    if contatos:
        enviaveis = sum(1 for l in contatos if not suprimido(l.get("status"), l.get("consentimento")) and canon_consent(l.get("consentimento")) == "confirmado")
        print(f"Lista: {len(contatos)} contato(s) | {enviaveis} enviaveis (opt-in confirmado)\n")
    if not linhas:
        print("ℹ️  Nenhuma campanha registrada ainda. Cole as metricas com 'campanha registrar'.")
        return
    for row in linhas:
        semaforo, acao = _diagnostico(row)
        env = _num(row.get("enviados")) or 0
        ab = _num(row.get("aberturas"))
        cl = _num(row.get("cliques"))
        print(f"## {row.get('nome','(sem nome)')}  [{row.get('tipo','')}]  {semaforo}")
        if env:
            taxa_ab = f"{pct(ab, env):.1f}%" if ab is not None else "faltou dado"
            taxa_cl = f"{pct(cl, env):.1f}%" if cl is not None else "faltou dado"
            print(f"   Enviados {env} | Abertura {taxa_ab} | Clique {taxa_cl}")
        print(f"   → {acao}\n")
    print("Lembrete: metrica de abertura e diretriz, nao verdade absoluta (Apple MPP infla).")
    print("Falha silenciosa: se um fluxo automatico parou de disparar, o painel nao avisa sozinho —")
    print("revise seus fluxos no ESP toda semana.")


# ----------------------------------------------------------------------------
# preflight — pacote de aprovacao + gate de seguranca antes do disparo
# ----------------------------------------------------------------------------

def cmd_preflight(a):
    dados = ler_config()
    exigir_config(dados)
    contatos = ler_contatos()
    seg = a.segmento
    if seg:
        alvo = [l for l in contatos if sem_acento(l.get("segmento", "")) == sem_acento(seg)]
    else:
        alvo = contatos
    total = len(alvo)
    suprimidos = [l for l in alvo if suprimido(l.get("status"), l.get("consentimento"))]
    desconhecidos = [l for l in alvo if canon_consent(l.get("consentimento")) == "desconhecido"]
    enviaveis = total - len(suprimidos) - len(desconhecidos)

    remetente = cfg(dados, "Nome do remetente (from-name)", "Nome do remetente")
    reply = cfg(dados, "E-mail de resposta (reply-to)", "E-mail de resposta")
    endereco = cfg(dados, "Endereco fisico (rodape/CAN-SPAM/LGPD)", "Endereco fisico")
    descad = cfg(dados, "Link de descadastro disponivel", "Link de descadastro")

    print("# Pre-voo do disparo — pacote de aprovacao\n")
    print(f"Segmento-alvo: {seg or '(lista inteira)'}")
    print(f"- Tamanho total: {total}")
    print(f"- Suprimidos (nao entram): {len(suprimidos)}")
    print(f"- Sem consentimento confirmado (NAO enviar): {len(desconhecidos)}")
    print(f"- Enviaveis de fato: {enviaveis}")
    print(f"- Remetente (from-name): {remetente}")
    print(f"- Reply-to: {reply}")
    print(f"- Endereco fisico no rodape: {endereco}")
    print(f"- Descadastro em 1 clique: {descad}")
    print("- Assunto / preview / corpo: confira no rascunho antes de aprovar")
    print()

    bloqueios = []
    alertas = []
    if enviaveis <= 0:
        bloqueios.append("Nenhum contato enviavel (sem opt-in confirmado). NAO dispare.")
    if desconhecidos:
        bloqueios.append(f"{len(desconhecidos)} contato(s) sem consentimento confirmado no alvo — remova ou confirme o opt-in (LGPD).")
    if endereco == VAZIO:
        bloqueios.append("Falta o endereco fisico do rodape (exigido por lei anti-spam / LGPD).")
    if descad == VAZIO or sem_acento(descad) in ("nao", "n"):
        bloqueios.append("Descadastro em 1 clique nao confirmado — todo e-mail marketing precisa dele.")
    if remetente == VAZIO:
        alertas.append("Defina um from-name reconhecivel (nunca 'noreply').")
    if reply == VAZIO:
        alertas.append("Defina um reply-to monitorado (respostas ajudam a entregabilidade).")
    if suprimidos:
        alertas.append(f"{len(suprimidos)} suprimido(s) serao excluidos automaticamente — confirme que seu ESP tambem exclui.")

    if bloqueios:
        print("🔴 BLOQUEADO — resolva antes de enviar:")
        for b in bloqueios:
            print(f"   - {b}")
    elif alertas:
        print("🟡 LIBERADO COM RESSALVAS:")
        for al in alertas:
            print(f"   - {al}")
    else:
        print("🟢 PRONTO PARA APROVACAO.")
    print("\nA Missiva NAO dispara. Leve este pacote + o rascunho aprovado ao seu ESP,")
    print("cole a audiencia enviavel e agende. O botao de enviar e sempre seu.")


# ----------------------------------------------------------------------------
# stats
# ----------------------------------------------------------------------------

def cmd_stats(a):
    dados = ler_config()
    contatos = ler_contatos()
    seqs = list(SEQ_DIR.glob("*.md")) if SEQ_DIR.exists() else []
    camp = 0
    if CAMPANHAS.exists():
        with CAMPANHAS.open(encoding="utf-8") as f:
            camp = sum(1 for _ in csv.DictReader(f))
    enviaveis = sum(1 for l in contatos if not suprimido(l.get("status"), l.get("consentimento")) and canon_consent(l.get("consentimento")) == "confirmado")
    print("# Missiva — visao geral\n")
    print(f"- Config: {'ok' if dados else 'FALTA (rode Preparar)'}")
    print(f"- Contatos na lista: {len(contatos)} ({enviaveis} enviaveis com opt-in)")
    print(f"- Sequencias desenhadas: {len(seqs)}")
    print(f"- Campanhas com metricas: {camp}")
    print(f"- Pasta de dados: {DIR}")


# ----------------------------------------------------------------------------
# CLI
# ----------------------------------------------------------------------------

def build_parser():
    p = argparse.ArgumentParser(
        prog="missiva",
        description="Motor local do canal de e-mail marketing & newsletter (offline, nunca dispara).")
    sub = p.add_subparsers(dest="cmd")

    s = sub.add_parser("setup", help="Grava a config inicial")
    for flag in ["negocio", "responsavel", "nicho", "remetente", "reply-to", "endereco", "esp", "tom", "descadastro"]:
        s.add_argument(f"--{flag}", default="")
    s.set_defaults(func=cmd_setup)

    sub.add_parser("autodestruir-setup", help="Remove a pasta setup/ apos a 1a vez").set_defaults(func=cmd_autodestruir_setup)
    sub.add_parser("config", help="Mostra a config atual").set_defaults(func=cmd_config)
    sub.add_parser("stats", help="Visao geral").set_defaults(func=cmd_stats)

    b = sub.add_parser("base", help="Lista & segmentos")
    bs = b.add_subparsers(dest="sub")
    bi = bs.add_parser("importar", help="Importa contatos de um CSV")
    bi.add_argument("arquivo")
    bi.add_argument("--segmento", default="")
    bi.add_argument("--consentimento", default="")
    bi.add_argument("--origem", default="")
    bi.set_defaults(func=cmd_base_importar)
    bh = bs.add_parser("higiene", help="Diagnostica/limpa a lista")
    bh.add_argument("--aplicar", action="store_true", help="Grava a lista limpa/deduplicada")
    bh.set_defaults(func=cmd_base_higiene)
    bs.add_parser("segmentos", help="Tamanho por segmento").set_defaults(func=cmd_base_segmentos)

    q = sub.add_parser("sequencia", help="Automacoes de ciclo de vida")
    qs = q.add_subparsers(dest="sub")
    qn = qs.add_parser("nova", help="Cria uma sequencia a partir de uma receita")
    qn.add_argument("tipo", help="boas-vindas|nutricao|carrinho|pos-compra|reengajamento|aniversario")
    qn.add_argument("--slug", default="")
    qn.add_argument("--segmento", default="")
    qn.add_argument("--objetivo", default="")
    qn.set_defaults(func=cmd_sequencia_nova)
    qs.add_parser("listar", help="Lista sequencias criadas").set_defaults(func=cmd_sequencia_listar)

    nw = sub.add_parser("newsletter", help="Calendario editorial recorrente")
    nw.add_argument("--frequencia", default="semanal", help="semanal|quinzenal|mensal")
    nw.add_argument("--edicoes", type=int, default=6)
    nw.set_defaults(func=cmd_newsletter)

    cr = sub.add_parser("campanha", help="Registra metricas coladas do ESP")
    crs = cr.add_subparsers(dest="sub")
    crr = crs.add_parser("registrar")
    crr.add_argument("nome")
    crr.add_argument("--data", default="")
    crr.add_argument("--tipo", default="campanha")
    for m in ["enviados", "aberturas", "cliques", "descadastros", "bounces", "reclamacoes"]:
        crr.add_argument(f"--{m}", type=int, default=None)
    crr.set_defaults(func=cmd_campanha_registrar)

    sub.add_parser("painel", help="Metricas viram decisao + entregabilidade").set_defaults(func=cmd_painel)

    pf = sub.add_parser("preflight", help="Pacote de aprovacao + gate antes do disparo")
    pf.add_argument("--segmento", default="")
    pf.set_defaults(func=cmd_preflight)

    return p


def main():
    parser = build_parser()
    args = parser.parse_args()
    if not getattr(args, "func", None):
        parser.print_help()
        return
    # sub-comandos sem acao escolhida
    if args.cmd in ("base", "sequencia", "campanha") and not getattr(args, "sub", None):
        parser.parse_args([args.cmd, "--help"])
        return
    args.func(args)


if __name__ == "__main__":
    main()
