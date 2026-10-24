#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Cais — motor local de onboarding/intake de cliente novo.

Cuida da parte EXATA do onboarding (o que precisa de contagem e memória):
cadastro de clientes novos, os 5 marcos do onboarding, a checklist de
documentos & acessos, o questionário de intake, o cálculo de prontidão e o
painel de quem está travado.

Princípios:
- Só biblioteca padrão do Python. Sem rede, sem API, sem instalar nada.
- Offline e 100% local: grava tudo em .cais/ na raiz do projeto.
- Nunca inventa dado. Campo em branco fica visível como [A PREENCHER]/[PENDENTE].
- O motor conta e organiza; QUEM decide e QUEM envia as mensagens é o dono.

Uso rápido:
    python3 cais.py cliente-add --nome "Ana Costa" --empresa "Studio Ana" \\
        --servico "Gestão de tráfego" --valor "R$ 1.500/mês" --inicio 05/08/2026 \\
        --contato "ana@studio.com" --canal WhatsApp
    python3 cais.py painel
    python3 cais.py prontidao --slug ana-costa
"""

import argparse
import csv
import os
import re
import sys
from datetime import datetime, date

# --------------------------------------------------------------------------- #
# Localização da pasta de dados (.cais/) — âncora na raiz do projeto
# --------------------------------------------------------------------------- #

def achar_raiz():
    """Sobe a partir do diretório atual procurando .cais/ , .git/ ou .claude/.
    Respeita CLAUDE_PROJECT_DIR quando definido. Cai no cwd se não achar nada."""
    env = os.environ.get("CLAUDE_PROJECT_DIR")
    if env and os.path.isdir(env):
        return os.path.abspath(env)
    atual = os.path.abspath(os.getcwd())
    while True:
        for marca in (".cais", ".git", ".claude"):
            if os.path.isdir(os.path.join(atual, marca)):
                return atual
        pai = os.path.dirname(atual)
        if pai == atual:
            return os.path.abspath(os.getcwd())
        atual = pai


RAIZ = achar_raiz()
DIR = os.path.join(RAIZ, ".cais")
CLIENTES = os.path.join(DIR, "clientes.csv")

MARCOS = ["intake", "documentos", "combinado", "kickoff"]  # "recebido" é implícito
CAMPOS_CLIENTE = [
    "slug", "nome", "empresa", "servico", "valor", "inicio", "contato",
    "canal", "m_intake", "m_documentos", "m_combinado", "m_kickoff",
    "criado_em", "atualizado_em",
]

ACOES = {
    "intake":     "Enviar o questionário de intake (modo Levantar) e registrar as respostas.",
    "documentos": "Pedir os documentos/acessos que faltam (modo Reunir) e marcar o que chegar.",
    "combinado":  "Fechar o combinado de escopo & expectativas (modo Combinar) com o cliente.",
    "kickoff":    "Marcar e preparar a reunião de largada (modo Largada).",
    "pronto":     "Onboarding completo — passar para a entrega (Planta/Escuta/Pauta) e retenção (Âncora).",
}

# --------------------------------------------------------------------------- #
# Utilidades
# --------------------------------------------------------------------------- #

def garantir_dir():
    os.makedirs(DIR, exist_ok=True)


def agora():
    return datetime.now().strftime("%Y-%m-%d %H:%M")


def slugificar(texto):
    t = (texto or "").strip().lower()
    subs = {"á":"a","à":"a","â":"a","ã":"a","ä":"a","é":"e","ê":"e","è":"e",
            "í":"i","ì":"i","î":"i","ó":"o","ô":"o","õ":"o","ò":"o","ú":"u",
            "ù":"u","û":"u","ü":"u","ç":"c","ñ":"n"}
    for a, b in subs.items():
        t = t.replace(a, b)
    t = re.sub(r"[^a-z0-9]+", "-", t).strip("-")
    return t or "cliente"


def parse_data_br(txt):
    """Aceita DD/MM/AAAA, DD/MM/AA, DD-MM-AAAA e AAAA-MM-DD. Devolve date ou None."""
    if not txt:
        return None
    txt = txt.strip()
    for fmt in ("%d/%m/%Y", "%d/%m/%y", "%d-%m-%Y", "%Y-%m-%d"):
        try:
            return datetime.strptime(txt, fmt).date()
        except ValueError:
            continue
    return None


def ler_csv(caminho):
    if not os.path.exists(caminho):
        return []
    with open(caminho, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def escrever_csv(caminho, campos, linhas):
    garantir_dir()
    with open(caminho, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=campos)
        w.writeheader()
        for l in linhas:
            w.writerow({c: l.get(c, "") for c in campos})


def caminho_itens(slug):
    return os.path.join(DIR, f"{slug}.itens.csv")


def caminho_intake(slug):
    return os.path.join(DIR, f"{slug}.intake.csv")


def erro(msg):
    print(f"⚠️  {msg}")
    sys.exit(1)


# --------------------------------------------------------------------------- #
# Acesso aos clientes
# --------------------------------------------------------------------------- #

def carregar_clientes():
    return ler_csv(CLIENTES)


def salvar_clientes(linhas):
    escrever_csv(CLIENTES, CAMPOS_CLIENTE, linhas)


def achar_cliente(slug):
    for c in carregar_clientes():
        if c.get("slug") == slug:
            return c
    return None


def tocar(slug):
    """Atualiza o carimbo 'atualizado_em' de um cliente."""
    linhas = carregar_clientes()
    for c in linhas:
        if c.get("slug") == slug:
            c["atualizado_em"] = agora()
    salvar_clientes(linhas)


# --------------------------------------------------------------------------- #
# Cálculo de prontidão
# --------------------------------------------------------------------------- #

def intake_completo(slug, cliente):
    if (cliente.get("m_intake") or "").strip().lower() == "sim":
        return True
    linhas = ler_csv(caminho_intake(slug))
    if not linhas:
        return False
    return all((l.get("respondido") or "").strip().lower() == "sim" for l in linhas)


def documentos_completos(slug, cliente):
    if (cliente.get("m_documentos") or "").strip().lower() == "sim":
        return True
    linhas = ler_csv(caminho_itens(slug))
    obrig = [l for l in linhas if (l.get("obrigatorio") or "sim").strip().lower() == "sim"]
    if not obrig:
        return False
    return all((l.get("status") or "").strip().lower() == "recebido" for l in obrig)


def marco_ok(slug, cliente, marco):
    if marco == "intake":
        return intake_completo(slug, cliente)
    if marco == "documentos":
        return documentos_completos(slug, cliente)
    return (cliente.get(f"m_{marco}") or "").strip().lower() == "sim"


def prontidao(slug, cliente):
    """Devolve (percentual, dict de marcos, próxima ação)."""
    estado = {"recebido": True}  # cadastrar já é o 1º marco
    for m in MARCOS:
        estado[m] = marco_ok(slug, cliente, m)
    feitos = sum(1 for v in estado.values() if v)
    total = len(estado)
    pct = round(feitos * 100 / total)
    # próxima ação = 1º marco em aberto na ordem
    proxima = ACOES["pronto"]
    for m in MARCOS:
        if not estado[m]:
            proxima = ACOES[m]
            break
    return pct, estado, proxima


def semaforo(pct):
    if pct >= 100:
        return "🟢"
    if pct >= 40:
        return "🟡"
    return "🔴"


def dias_desde(txt):
    if not txt:
        return None
    for fmt in ("%Y-%m-%d %H:%M", "%Y-%m-%d"):
        try:
            d = datetime.strptime(txt.strip(), fmt).date()
            return (date.today() - d).days
        except ValueError:
            continue
    return None


# --------------------------------------------------------------------------- #
# Comandos
# --------------------------------------------------------------------------- #

def cmd_cliente_add(a):
    if not a.nome:
        erro("Informe --nome do cliente.")
    slug = a.slug or slugificar(a.nome if not a.empresa else f"{a.nome}")
    if achar_cliente(slug):
        erro(f"Já existe um cliente com o slug '{slug}'. Use --slug para diferenciar.")
    inicio = ""
    if a.inicio:
        d = parse_data_br(a.inicio)
        inicio = d.strftime("%d/%m/%Y") if d else a.inicio
    nova = {
        "slug": slug, "nome": a.nome, "empresa": a.empresa or "",
        "servico": a.servico or "[A PREENCHER]", "valor": a.valor or "",
        "inicio": inicio, "contato": a.contato or "", "canal": a.canal or "",
        "m_intake": "", "m_documentos": "", "m_combinado": "", "m_kickoff": "",
        "criado_em": agora(), "atualizado_em": agora(),
    }
    linhas = carregar_clientes()
    linhas.append(nova)
    salvar_clientes(linhas)
    print(f"✅ Cliente cadastrado: {a.nome}  (slug: {slug})")
    print(f"   Serviço: {nova['servico']}  ·  Início: {inicio or '[A PREENCHER]'}")
    print("   Marco 1/5 concluído: RECEBIDO. Próximo: enviar a mensagem de boas-vindas")
    print("   e o questionário de intake (modo Levantar).")


def cmd_clientes(a):
    linhas = carregar_clientes()
    if not linhas:
        print("Nenhum cliente em onboarding ainda. Use 'cliente-add' para começar.")
        return
    print(f"📋 Clientes em onboarding ({len(linhas)}):\n")
    for c in linhas:
        pct, _, prox = prontidao(c["slug"], c)
        print(f"  {semaforo(pct)} {pct:>3}%  {c['nome']}  ·  {c.get('servico','')}")
        print(f"          slug: {c['slug']}  ·  próximo: {prox}")
    print()


def cmd_cliente_ver(a):
    c = achar_cliente(a.slug)
    if not c:
        erro(f"Cliente '{a.slug}' não encontrado.")
    pct, estado, prox = prontidao(a.slug, c)
    print(f"{semaforo(pct)} {c['nome']}  ({pct}% pronto)")
    print(f"   Empresa:  {c.get('empresa') or '—'}")
    print(f"   Serviço:  {c.get('servico') or '—'}")
    print(f"   Valor:    {c.get('valor') or '—'}")
    print(f"   Início:   {c.get('inicio') or '[A PREENCHER]'}")
    print(f"   Contato:  {c.get('contato') or '—'}  ·  Canal: {c.get('canal') or '—'}")
    print("   Marcos:")
    nomes = {"recebido": "Recebido (cadastro + boas-vindas)", "intake": "Intake respondido",
             "documentos": "Documentos & acessos completos", "combinado": "Combinado fechado",
             "kickoff": "Kickoff realizado"}
    for k in ["recebido"] + MARCOS:
        print(f"     {'✅' if estado[k] else '⬜'} {nomes[k]}")
    print(f"   → Próxima ação: {prox}")


def cmd_marco(a):
    c = achar_cliente(a.slug)
    if not c:
        erro(f"Cliente '{a.slug}' não encontrado.")
    if a.marco not in MARCOS:
        erro(f"Marco inválido. Use um de: {', '.join(MARCOS)}.")
    linhas = carregar_clientes()
    for l in linhas:
        if l["slug"] == a.slug:
            l[f"m_{a.marco}"] = "" if a.desfazer else "sim"
            l["atualizado_em"] = agora()
    salvar_clientes(linhas)
    verbo = "desmarcado" if a.desfazer else "concluído"
    print(f"✅ Marco '{a.marco}' {verbo} para {c['nome']}.")
    c = achar_cliente(a.slug)
    pct, _, prox = prontidao(a.slug, c)
    print(f"   Prontidão agora: {semaforo(pct)} {pct}%  ·  próximo: {prox}")


def cmd_item_add(a):
    if not achar_cliente(a.slug):
        erro(f"Cliente '{a.slug}' não encontrado.")
    campos = ["item", "tipo", "obrigatorio", "status", "pedido_em", "recebido_em", "obs"]
    linhas = ler_csv(caminho_itens(a.slug))
    if any((l.get("item") or "").strip().lower() == a.item.strip().lower() for l in linhas):
        erro(f"O item '{a.item}' já está na checklist deste cliente.")
    linhas.append({
        "item": a.item, "tipo": a.tipo or "documento",
        "obrigatorio": "nao" if a.opcional else "sim",
        "status": "pendente", "pedido_em": a.pedido_em or agora().split()[0],
        "recebido_em": "", "obs": a.obs or "",
    })
    escrever_csv(caminho_itens(a.slug), campos, linhas)
    tocar(a.slug)
    print(f"✅ Item adicionado à checklist de {a.slug}: {a.item} "
          f"({a.tipo or 'documento'}, {'opcional' if a.opcional else 'obrigatório'})")


def cmd_itens(a):
    c = achar_cliente(a.slug)
    if not c:
        erro(f"Cliente '{a.slug}' não encontrado.")
    linhas = ler_csv(caminho_itens(a.slug))
    if not linhas:
        print(f"Nenhum item na checklist de {c['nome']} ainda. Use 'item-add'.")
        return
    recebidos = [l for l in linhas if (l.get("status") or "").lower() == "recebido"]
    obrig = [l for l in linhas if (l.get("obrigatorio") or "sim").lower() == "sim"]
    obrig_ok = [l for l in obrig if (l.get("status") or "").lower() == "recebido"]
    print(f"📎 Documentos & acessos de {c['nome']}  "
          f"({len(recebidos)}/{len(linhas)} recebidos · "
          f"obrigatórios {len(obrig_ok)}/{len(obrig)}):\n")
    for i, l in enumerate(linhas, 1):
        marca = "✅" if (l.get("status") or "").lower() == "recebido" else "⏳"
        flag = "" if (l.get("obrigatorio") or "sim").lower() == "sim" else "  (opcional)"
        pend = ""
        if marca == "⏳":
            d = dias_desde(l.get("pedido_em"))
            if d is not None and d >= 3:
                pend = f"  ⚠️ pendente há {d} dia(s)"
        print(f"  {i:>2}. {marca} [{l.get('tipo','documento')}] {l['item']}{flag}{pend}")
    faltam = [l["item"] for l in obrig if (l.get("status") or "").lower() != "recebido"]
    if faltam:
        print(f"\n  Falta receber ({len(faltam)}): " + "; ".join(faltam))
        print("  → Gere a mensagem de cobrança educada no modo Reunir e o DONO envia.")
    else:
        print("\n  🟢 Todos os itens obrigatórios foram recebidos.")


def cmd_item_receber(a):
    if not achar_cliente(a.slug):
        erro(f"Cliente '{a.slug}' não encontrado.")
    campos = ["item", "tipo", "obrigatorio", "status", "pedido_em", "recebido_em", "obs"]
    linhas = ler_csv(caminho_itens(a.slug))
    achou = None
    for l in linhas:
        if a.item.isdigit():
            if linhas.index(l) + 1 == int(a.item):
                achou = l
        elif (l.get("item") or "").strip().lower() == a.item.strip().lower():
            achou = l
    if not achou:
        erro(f"Item '{a.item}' não encontrado na checklist. Use o número ou o nome exato.")
    achou["status"] = "recebido"
    achou["recebido_em"] = agora().split()[0]
    escrever_csv(caminho_itens(a.slug), campos, linhas)
    tocar(a.slug)
    print(f"✅ Recebido: {achou['item']}")
    obrig = [l for l in linhas if (l.get("obrigatorio") or "sim").lower() == "sim"]
    faltam = [l for l in obrig if (l.get("status") or "").lower() != "recebido"]
    if not faltam:
        print("   🟢 Todos os obrigatórios chegaram — o marco 'documentos' está completo.")
    else:
        print(f"   Ainda faltam {len(faltam)}: " + "; ".join(l["item"] for l in faltam))


def cmd_intake_add(a):
    if not achar_cliente(a.slug):
        erro(f"Cliente '{a.slug}' não encontrado.")
    campos = ["bloco", "pergunta", "resposta", "respondido"]
    linhas = ler_csv(caminho_intake(a.slug))
    linhas.append({"bloco": a.bloco or "Geral", "pergunta": a.pergunta,
                   "resposta": "", "respondido": ""})
    escrever_csv(caminho_intake(a.slug), campos, linhas)
    tocar(a.slug)
    print(f"✅ Pergunta de intake adicionada ({a.bloco or 'Geral'}): {a.pergunta}")


def cmd_intake(a):
    c = achar_cliente(a.slug)
    if not c:
        erro(f"Cliente '{a.slug}' não encontrado.")
    linhas = ler_csv(caminho_intake(a.slug))
    if not linhas:
        print(f"Nenhuma pergunta de intake para {c['nome']} ainda. Use 'intake-add'.")
        return
    ok = [l for l in linhas if (l.get("respondido") or "").lower() == "sim"]
    print(f"📝 Intake de {c['nome']}  ({len(ok)}/{len(linhas)} respondidas):\n")
    bloco_atual = None
    for i, l in enumerate(linhas, 1):
        if l.get("bloco") != bloco_atual:
            bloco_atual = l.get("bloco")
            print(f"  — {bloco_atual} —")
        marca = "✅" if (l.get("respondido") or "").lower() == "sim" else "⬜"
        print(f"    {i:>2}. {marca} {l['pergunta']}")
        if (l.get("resposta") or "").strip():
            print(f"        ↳ {l['resposta']}")
    if len(ok) < len(linhas):
        print("\n  Ainda há perguntas sem resposta — registre com 'intake-responder'.")


def cmd_intake_responder(a):
    if not achar_cliente(a.slug):
        erro(f"Cliente '{a.slug}' não encontrado.")
    campos = ["bloco", "pergunta", "resposta", "respondido"]
    linhas = ler_csv(caminho_intake(a.slug))
    achou = None
    for l in linhas:
        if a.pergunta.isdigit():
            if linhas.index(l) + 1 == int(a.pergunta):
                achou = l
        elif a.pergunta.strip().lower() in (l.get("pergunta") or "").strip().lower():
            achou = l
    if not achou:
        erro("Pergunta não encontrada. Use o número (veja 'intake') ou um trecho do texto.")
    achou["resposta"] = a.resposta
    achou["respondido"] = "sim"
    escrever_csv(caminho_intake(a.slug), campos, linhas)
    tocar(a.slug)
    print(f"✅ Resposta registrada para: {achou['pergunta']}")


def cmd_prontidao(a):
    c = achar_cliente(a.slug)
    if not c:
        erro(f"Cliente '{a.slug}' não encontrado.")
    pct, estado, prox = prontidao(a.slug, c)
    print(f"{semaforo(pct)} {c['nome']} — {pct}% pronto para começar\n")
    passos = [
        ("recebido", "Recebido — cadastro feito + boas-vindas enviadas"),
        ("intake", "Intake — questionário respondido"),
        ("documentos", "Documentos & acessos — tudo o que é obrigatório chegou"),
        ("combinado", "Combinado — escopo & expectativas alinhados"),
        ("kickoff", "Kickoff — reunião de largada realizada"),
    ]
    for chave, texto in passos:
        print(f"  {'✅' if estado[chave] else '⬜'} {texto}")
    print(f"\n  → Próxima ação: {prox}")
    if pct >= 100:
        print("  🎉 Onboarding concluído! Handoff para a entrega (Planta/Escuta/Pauta) e Âncora.")


def cmd_painel(a):
    linhas = carregar_clientes()
    if not linhas:
        print("Nenhum cliente em onboarding. Use 'cliente-add' para começar.")
        return
    dados = []
    for c in linhas:
        pct, estado, prox = prontidao(c["slug"], c)
        d = dias_desde(c.get("atualizado_em"))
        dados.append((c, pct, prox, d))
    prontos = [x for x in dados if x[1] >= 100]
    andamento = sorted([x for x in dados if x[1] < 100], key=lambda x: x[1])
    print("═" * 60)
    print(f"  PAINEL DE ONBOARDING — {len(linhas)} cliente(s)")
    print("═" * 60)
    print(f"  🟢 Prontos para começar: {len(prontos)}   ·   "
          f"🟡🔴 Em andamento: {len(andamento)}\n")
    if andamento:
        print("  EM ANDAMENTO (do menos pronto ao mais pronto):")
        for c, pct, prox, d in andamento:
            alerta = ""
            if d is not None and d >= a.dias:
                alerta = f"  ⚠️ parado há {d} dia(s)"
            print(f"   {semaforo(pct)} {pct:>3}%  {c['nome']}{alerta}")
            print(f"           → {prox}")
        print()
    if prontos:
        print("  PRONTOS (handoff para entrega + Âncora):")
        for c, pct, prox, d in prontos:
            print(f"   🟢 {c['nome']}  ·  {c.get('servico','')}")
        print()


def cmd_parados(a):
    linhas = carregar_clientes()
    limite = a.dias
    travados = []
    for c in linhas:
        pct, _, prox = prontidao(c["slug"], c)
        if pct >= 100:
            continue
        d = dias_desde(c.get("atualizado_em"))
        if d is not None and d >= limite:
            travados.append((c, pct, prox, d))
    if not travados:
        print(f"🟢 Nenhum onboarding parado há {limite}+ dias. Tudo fluindo.")
        return
    travados.sort(key=lambda x: -x[3])
    print(f"⚠️  Onboardings parados há {limite}+ dias ({len(travados)}):\n")
    for c, pct, prox, d in travados:
        print(f"   {semaforo(pct)} {pct:>3}%  {c['nome']}  ·  parado há {d} dia(s)")
        print(f"           → {prox}")
    print("\n  Sugestão: reative com um toque leve no tom do dono (o DONO envia).")


# --------------------------------------------------------------------------- #
# CLI
# --------------------------------------------------------------------------- #

def build_parser():
    p = argparse.ArgumentParser(
        prog="cais.py",
        description="Cais — motor local de onboarding/intake de cliente novo.")
    sub = p.add_subparsers(dest="cmd")

    s = sub.add_parser("cliente-add", help="cadastra um cliente novo (marco Recebido)")
    s.add_argument("--nome", required=True)
    s.add_argument("--empresa", default="")
    s.add_argument("--servico", default="")
    s.add_argument("--valor", default="")
    s.add_argument("--inicio", default="")
    s.add_argument("--contato", default="")
    s.add_argument("--canal", default="")
    s.add_argument("--slug", default="")
    s.set_defaults(func=cmd_cliente_add)

    s = sub.add_parser("clientes", help="lista todos os clientes em onboarding")
    s.set_defaults(func=cmd_clientes)

    s = sub.add_parser("cliente-ver", help="detalhe de um cliente")
    s.add_argument("--slug", required=True)
    s.set_defaults(func=cmd_cliente_ver)

    s = sub.add_parser("marco", help="marca/desmarca um marco (intake|documentos|combinado|kickoff)")
    s.add_argument("--slug", required=True)
    s.add_argument("--marco", required=True)
    s.add_argument("--desfazer", action="store_true")
    s.set_defaults(func=cmd_marco)

    s = sub.add_parser("item-add", help="adiciona documento/acesso à checklist")
    s.add_argument("--slug", required=True)
    s.add_argument("--item", required=True)
    s.add_argument("--tipo", default="documento", help="documento|acesso|material")
    s.add_argument("--opcional", action="store_true")
    s.add_argument("--pedido-em", dest="pedido_em", default="")
    s.add_argument("--obs", default="")
    s.set_defaults(func=cmd_item_add)

    s = sub.add_parser("itens", help="mostra a checklist de documentos & acessos")
    s.add_argument("--slug", required=True)
    s.set_defaults(func=cmd_itens)

    s = sub.add_parser("item-receber", help="marca um item como recebido (número ou nome)")
    s.add_argument("--slug", required=True)
    s.add_argument("--item", required=True)
    s.set_defaults(func=cmd_item_receber)

    s = sub.add_parser("intake-add", help="adiciona pergunta ao questionário de intake")
    s.add_argument("--slug", required=True)
    s.add_argument("--pergunta", required=True)
    s.add_argument("--bloco", default="Geral")
    s.set_defaults(func=cmd_intake_add)

    s = sub.add_parser("intake", help="mostra o questionário de intake e o que já respondeu")
    s.add_argument("--slug", required=True)
    s.set_defaults(func=cmd_intake)

    s = sub.add_parser("intake-responder", help="registra a resposta de uma pergunta (número ou trecho)")
    s.add_argument("--slug", required=True)
    s.add_argument("--pergunta", required=True)
    s.add_argument("--resposta", required=True)
    s.set_defaults(func=cmd_intake_responder)

    s = sub.add_parser("prontidao", help="prontidão de um cliente: marcos, percentual e próxima ação")
    s.add_argument("--slug", required=True)
    s.set_defaults(func=cmd_prontidao)

    s = sub.add_parser("painel", help="visão geral de todos os onboardings")
    s.add_argument("--dias", type=int, default=5, help="dias sem atividade para sinalizar parado")
    s.set_defaults(func=cmd_painel)

    s = sub.add_parser("parados", help="lista onboardings parados há N+ dias")
    s.add_argument("--dias", type=int, default=5)
    s.set_defaults(func=cmd_parados)

    return p


def main():
    parser = build_parser()
    args = parser.parse_args()
    if not getattr(args, "cmd", None):
        parser.print_help()
        return
    args.func(args)


if __name__ == "__main__":
    main()
