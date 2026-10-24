#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
amarra.py — motor de VENDA CONSULTIVA B2B do pequeno negócio (offline, só biblioteca padrão).

Filosofia (igual aos irmãos Farol/Cadência/Lastro):
  - A Amarra pega uma OPORTUNIDADE já qualificada e a leva do "tenho uma reunião marcada" ao
    "cliente assinou": prepara a REUNIÃO DE DESCOBERTA, captura a dor/impacto/decisor nas palavras
    do cliente, qualifica a chance (0-100), quantifica o VALOR/ROI e monta a PROPOSTA CONSULTIVA
    que vende — situação → solução → escopo → 3 opções (bom/melhor/ótimo) → critérios → ROI →
    riscos → próximo passo — além de uma biblioteca de objeções pronta.
  - Insight que a torna confiável: a IA NÃO inventa a dor, o número, o decisor nem o preço. Tudo o
    que entra na proposta vem do que foi CAPTURADO na descoberta; o que falta aparece como
    [A CONFERIR]. Uma IA sozinha "inventa" uma proposta genérica; a Amarra lidera pela SITUAÇÃO
    (mostra que ouviu) e só afirma o que o cliente disse.
  - Regra de ouro: a Amarra PREPARA e REDIGE; o DONO conduz a reunião e envia a proposta. Venda é
    conversa humana — a IA nunca fala pelo dono nem manda nada sozinha.
  - Sempre 3 opções na proposta (proposta de opção única fecha menos). ROI mesmo aproximado, com
    premissas à vista. Riscos declarados constroem confiança. Desqualificar é uma decisão válida.
  - Não acessa a internet. Dados 100% locais (LGPD — dados de cliente são sensíveis).

Dados (tudo em <raiz>/.amarra/, git-ignored):
  config.md          — negócio, moeda, o que vende (oferta), ticket típico (opcional)
  oportunidades.csv  — id, cliente, persona, contato, oferta, valor, framework, estagio, criado
  descoberta.csv     — oportunidade_id, chave, valor        (o que o cliente disse — key/value)
  valores.csv        — oportunidade_id, driver, tipo, valor_ano   (drivers de ROI)

Uso: python3 amarra.py <comando> [opções].  Rode `python3 amarra.py ajuda` para o mapa.
"""

import os
import sys
import csv
import re
import argparse
import unicodedata
from datetime import date

# --------------------------------------------------------------------------- #
# Localização da "casa" de dados (.amarra/)                                    #
# --------------------------------------------------------------------------- #

def achar_raiz():
    """Ancora o .amarra/ na raiz do projeto do membro.
    Ordem: CLAUDE_PROJECT_DIR -> sobe procurando .git/.claude -> cwd."""
    env = os.environ.get("CLAUDE_PROJECT_DIR")
    if env and os.path.isdir(env):
        return env
    d = os.getcwd()
    while True:
        if os.path.isdir(os.path.join(d, ".git")) or os.path.isdir(os.path.join(d, ".claude")):
            return d
        pai = os.path.dirname(d)
        if pai == d:
            break
        d = pai
    return os.getcwd()

RAIZ = achar_raiz()
CASA = os.path.join(RAIZ, ".amarra")
CONFIG = os.path.join(CASA, "config.md")
OPS = os.path.join(CASA, "oportunidades.csv")
DESC = os.path.join(CASA, "descoberta.csv")
VALS = os.path.join(CASA, "valores.csv")

COLS_OP = ["id", "cliente", "persona", "contato", "oferta", "valor", "framework", "estagio", "criado"]
COLS_DESC = ["oportunidade_id", "chave", "valor"]
COLS_VAL = ["oportunidade_id", "driver", "tipo", "valor_ano"]

ESTAGIOS = ["descoberta", "qualificado", "proposta", "negociacao", "fechado", "perdido"]

# chaves canônicas da descoberta (o que capturamos do que o cliente disse)
CHAVES = {
    "situacao": "Situação atual",
    "dor": "Dor / problema",
    "impacto": "Custo de não resolver",
    "meta": "Meta / resultado desejado",
    "prazo": "Prazo / urgência",
    "decisor": "Quem decide (decisor econômico)",
    "campeao": "Campeão interno (quem defende)",
    "criterio": "Critério de decisão",
    "concorrente": "Concorrente / alternativa avaliada",
    "orcamento": "Orçamento / verba",
}

# --------------------------------------------------------------------------- #
# Leitura/escrita                                                             #
# --------------------------------------------------------------------------- #

def garantir_casa():
    os.makedirs(CASA, exist_ok=True)
    if not os.path.exists(OPS):
        _escrever(OPS, COLS_OP, [])
    if not os.path.exists(DESC):
        _escrever(DESC, COLS_DESC, [])
    if not os.path.exists(VALS):
        _escrever(VALS, COLS_VAL, [])

def _ler(caminho, cols):
    if not os.path.exists(caminho):
        return []
    with open(caminho, newline="", encoding="utf-8") as f:
        return [dict(r) for r in csv.DictReader(f)]

def _escrever(caminho, cols, linhas):
    os.makedirs(os.path.dirname(caminho), exist_ok=True)
    with open(caminho, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=cols)
        w.writeheader()
        for l in linhas:
            w.writerow({c: l.get(c, "") for c in cols})

def ler_ops():
    return _ler(OPS, COLS_OP)

def salvar_ops(l):
    _escrever(OPS, COLS_OP, l)

def ler_desc():
    return _ler(DESC, COLS_DESC)

def salvar_desc(l):
    _escrever(DESC, COLS_DESC, l)

def ler_vals():
    return _ler(VALS, COLS_VAL)

def salvar_vals(l):
    _escrever(VALS, COLS_VAL, l)

# --------------------------------------------------------------------------- #
# Parsers BR e texto                                                          #
# --------------------------------------------------------------------------- #

def sem_acento(s):
    s = unicodedata.normalize("NFD", s or "")
    return "".join(c for c in s if unicodedata.category(c) != "Mn").lower().strip()

def num(v, padrao=0.0):
    """Parser BR robusto: '1.234,56', '50.000', '199,90', 'R$ 89', '12,5', '1000'."""
    if v is None:
        return padrao
    s = str(v).strip().replace("R$", "").replace(" ", "")
    if s == "":
        return padrao
    neg = s.startswith("-")
    s = s.lstrip("+-")
    if "," in s:
        s = s.replace(".", "").replace(",", ".")
    else:
        # sem vírgula: ponto agrupando exatamente 3 dígitos = milhar
        if re.fullmatch(r"\d{1,3}(\.\d{3})+", s):
            s = s.replace(".", "")
    try:
        x = float(s)
    except ValueError:
        return padrao
    return -x if neg else x

def dinheiro(v, moeda="R$"):
    try:
        x = float(v)
    except (ValueError, TypeError):
        x = 0.0
    s = f"{x:,.2f}".replace(",", "§").replace(".", ",").replace("§", ".")
    return f"{moeda} {s}"

def dec1(v):
    try:
        x = float(v)
    except (ValueError, TypeError):
        x = 0.0
    return f"{x:,.1f}".replace(",", "§").replace(".", ",").replace("§", ".")

def hoje():
    return date.today().isoformat()

# --------------------------------------------------------------------------- #
# Config                                                                       #
# --------------------------------------------------------------------------- #

def ler_config():
    cfg = {"negocio": "", "moeda": "R$", "oferta": "", "ticket": ""}
    if not os.path.exists(CONFIG):
        return cfg
    txt = open(CONFIG, encoding="utf-8").read()
    for linha in txt.splitlines():
        m = re.match(r"\s*-\s*\*\*(.+?):\*\*\s*(.*)", linha)
        if not m:
            continue
        rot, val = sem_acento(m.group(1)), m.group(2).strip()
        if "negocio" in rot:
            cfg["negocio"] = val
        elif "moeda" in rot:
            cfg["moeda"] = val or "R$"
        elif "oferta" in rot or "vende" in rot:
            cfg["oferta"] = val
        elif "ticket" in rot:
            cfg["ticket"] = val
    return cfg

def moeda():
    return ler_config().get("moeda", "R$") or "R$"

# --------------------------------------------------------------------------- #
# Helpers de oportunidade                                                      #
# --------------------------------------------------------------------------- #

def prox_id(linhas):
    ids = [int(l["id"]) for l in linhas if str(l.get("id", "")).isdigit()]
    return str(max(ids) + 1) if ids else "1"

def achar_op(ops, ident):
    ident = str(ident).strip()
    for o in ops:
        if o["id"] == ident:
            return o
    alvo = sem_acento(ident)
    for o in ops:
        if sem_acento(o["cliente"]) == alvo:
            return o
    for o in ops:
        if alvo and alvo in sem_acento(o["cliente"]):
            return o
    return None

def desc_da_op(ident):
    return {d["chave"]: d["valor"] for d in ler_desc() if d["oportunidade_id"] == str(ident)}

def vals_da_op(ident):
    return [v for v in ler_vals() if v["oportunidade_id"] == str(ident)]

def exige_op(ident):
    op = achar_op(ler_ops(), ident)
    if not op:
        print(f"⚠️  Não encontrei a oportunidade '{ident}'. Rode `lista` para ver os ids, ou "
              f"`nova --cliente \"Nome\"` para cadastrar.")
        sys.exit(1)
    return op

# --------------------------------------------------------------------------- #
# BANCO DE PERGUNTAS DE DESCOBERTA (por framework)                             #
# --------------------------------------------------------------------------- #
# Frameworks consultivos. Cada dimensão tem perguntas abertas, comportamentais
# e quantitativas — a IA adapta a redação ao contexto do dono.

BANCO = {
    "spin": [
        ("Situação", [
            "Como funciona hoje o seu processo de [área]? Me conta o passo a passo.",
            "Que ferramentas/pessoas estão envolvidas nisso hoje?",
            "Há quanto tempo é feito assim?",
        ]),
        ("Problema", [
            "Onde isso costuma travar ou dar retrabalho?",
            "O que mais te incomoda nesse processo do jeito que está?",
            "Com que frequência esse problema aparece?",
        ]),
        ("Implicação", [
            "Quando isso trava, o que acontece depois? Quem mais é afetado?",
            "Quanto isso custa — em dinheiro, tempo ou cliente perdido?",
            "Se continuar assim por mais 12 meses, onde você chega?",
        ]),
        ("Necessidade-solução", [
            "Se esse problema sumisse amanhã, o que mudaria pra você?",
            "Quanto valeria resolver isso de vez?",
            "O que precisaria ser verdade pra você tratar isso como prioridade agora?",
        ]),
    ],
    "gpct": [
        ("Metas (Goals)", [
            "Qual é o resultado que você quer alcançar em [prazo]?",
            "Como você mede sucesso nessa área hoje? Qual é o número atual?",
        ]),
        ("Planos (Plans)", [
            "Como você está tentando chegar lá hoje?",
            "Já tentou resolver isso antes? O que funcionou e o que não?",
        ]),
        ("Desafios (Challenges)", [
            "O que está no caminho entre você e essa meta?",
            "O que acontece se você não resolver isso?",
        ]),
        ("Prazo (Timeline)", [
            "Até quando isso precisa estar resolvido? Por quê essa data?",
            "O que muda pra você se atrasar?",
        ]),
    ],
    "meddic": [
        ("Métricas", [
            "Como vocês medem sucesso em [área]? Qual é o número hoje?",
            "Qual é o custo do problema hoje — em R$, tempo ou risco?",
        ]),
        ("Decisor econômico", [
            "Além de você, quem mais entra numa decisão dessas?",
            "Quem assina o orçamento se seguirmos em frente?",
        ]),
        ("Critério de decisão", [
            "O que é mais importante quando você avalia uma solução dessas?",
            "O que faria você NÃO seguir em frente?",
        ]),
        ("Processo de decisão", [
            "Como decisões assim costumam acontecer aí? Quais etapas?",
            "Tem compras/jurídico? Qual é um prazo realista se tudo correr bem?",
        ]),
        ("Dor (Identify Pain)", [
            "O que está te fazendo olhar isso agora, e não há 6 meses?",
            "Quem mais sente essa dor — e o quão alto?",
        ]),
        ("Campeão", [
            "Quem aí dentro está mais animado pra resolver isso?",
            "Se precisar de alguém pra defender isso internamente, quem seria?",
        ]),
    ],
    "bant": [
        ("Necessidade (Need)", [
            "Qual é o problema que você está tentando resolver?",
            "O que acontece se ele não for resolvido?",
        ]),
        ("Orçamento (Budget)", [
            "Você já tem uma verba reservada pra isso?",
            "Que faixa de investimento faz sentido pra você?",
        ]),
        ("Autoridade (Authority)", [
            "Quem mais participa dessa decisão além de você?",
            "Você decide sozinho ou precisa aprovar com alguém?",
        ]),
        ("Prazo (Timeline)", [
            "Quando você gostaria de ter isso resolvido?",
            "Tem alguma data ou evento forçando esse prazo?",
        ]),
    ],
}

FRAMEWORK_PADRAO = {"": "spin", "spin": "spin", "gpct": "gpct", "meddic": "meddic", "bant": "bant"}


def escolher_framework(f):
    return FRAMEWORK_PADRAO.get(sem_acento(f or "spin"), "spin")

# --------------------------------------------------------------------------- #
# BIBLIOTECA DE OBJEÇÕES (7 categorias)                                        #
# --------------------------------------------------------------------------- #
# Cada objeção: medo real por trás + reframes + pergunta de validação + follow-up.

OBJECOES = {
    "preco": {
        "titulo": "Preço / Orçamento",
        "exemplos": ['"Está caro."', '"Não tenho verba agora."', '"Achei mais barato em outro lugar."'],
        "medo": "\"E se eu pagar e não valer? Não quero errar com o dinheiro.\"",
        "validar": "Caro comparado a quê — a outra proposta, ou ao custo de continuar como está?",
        "reframes": [
            "Ancore no CUSTO DE NÃO RESOLVER (o impacto que ele mesmo te disse): "
            "\"Você comentou que [dor] te custa [impacto]/mês. A proposta se paga em [payback].\"",
            "Divida no tempo/uso: R$ X por mês, ou por cliente/atendimento, não o total de uma vez.",
            "Ofereça a opção menor (bom) ou um piloto: reduz o risco sem baixar o valor do serviço.",
        ],
        "followup": "Envie a conta do ROI (a matemática) por escrito e proponha revisar juntos numa call de 15 min.",
    },
    "tempo": {
        "titulo": "Momento / Timing",
        "exemplos": ['"Agora não, me chama daqui a uns meses."', '"Estamos no meio de outra coisa."'],
        "medo": "\"Não tenho banda pra mais um projeto agora e vou me enrolar.\"",
        "validar": "É o momento mesmo, ou é o esforço de implantar? Se fosse do meu lado, mudaria algo?",
        "reframes": [
            "Custo da espera: \"Cada mês parado é [impacto]. Adiar 6 meses custa [6× impacto].\"",
            "Reduza o esforço de entrada: comece pela fase 1, sem parar a operação dele.",
            "Marque o próximo passo com data (\"revisamos em [data]\") pra não virar um 'nunca'.",
        ],
        "followup": "Combine um gatilho concreto (\"quando [evento] acontecer\") e agende o retorno já.",
    },
    "statusquo": {
        "titulo": "Já resolvo de outro jeito",
        "exemplos": ['"Já uso [concorrente]."', '"A gente faz na planilha mesmo."', '"Resolvo internamente."'],
        "medo": "\"Trocar dá trabalho e posso passar vergonha se der errado.\"",
        "validar": "O que funciona bem no jeito atual? E o que você mudaria nele se pudesse?",
        "reframes": [
            "Reconheça o que funciona e mire só a lacuna: \"A planilha resolve X; o que ela não faz é [dor].\"",
            "Mostre o custo escondido do jeito atual (tempo, erro, retrabalho) — que ele já admitiu.",
            "Prova social de quem saiu do mesmo jeito e o resultado — sem atacar a escolha dele.",
        ],
        "followup": "Ofereça um comparativo lado a lado (atual × proposto) focado no que ELE valoriza.",
    },
    "autoridade": {
        "titulo": "Preciso falar com / decidir depois",
        "exemplos": ['"Preciso conversar com meu sócio."', '"Me manda por escrito que eu vejo."'],
        "medo": "\"Não sou eu que decido sozinho\" — ou é um jeito educado de adiar.",
        "validar": "Quem mais entra nessa decisão? O que ELE vai querer saber pra dizer sim?",
        "reframes": [
            "Vire o \"manda por escrito\" numa proposta que VENDE por você (situação + ROI + opções).",
            "Ofereça entrar na conversa com o sócio/decisor pra tirar dúvidas ao vivo.",
            "Pergunte direto: \"Se dependesse só de você, seguiria?\" — separa objeção real de cortesia.",
        ],
        "followup": "Envie um resumo de 1 página feito pro decisor ausente e marque o retorno com data.",
    },
    "ajuste": {
        "titulo": "Não é pra mim / não preciso",
        "exemplos": ['"Acho que não é o meu caso."', '"Meu negócio é pequeno demais pra isso."'],
        "medo": "\"Não vejo como isso me ajuda de verdade\" — faltou conectar à dor dele.",
        "validar": "Me conta como você lida hoje com [área] — só pra eu não sugerir o que não serve.",
        "reframes": [
            "Volte pra descoberta: reconecte a solução à dor específica que ELE disse.",
            "Mostre um caso do mesmo porte/segmento dele pra quebrar o \"pequeno demais\".",
            "Se realmente não há dor, DESQUALIFIQUE com elegância — não force o que não encaixa.",
        ],
        "followup": "Se não é fit agora, agende um retorno leve pra quando o gatilho aparecer.",
    },
    "risco": {
        "titulo": "Risco / Confiança",
        "exemplos": ['"Nunca ouvi falar de vocês."', '"E se não funcionar?"', '"Migrar é arriscado."'],
        "medo": "\"E se eu confiar e me ferrar?\" — medo de perder dinheiro e credibilidade.",
        "validar": "O que precisaria existir pra você se sentir seguro em começar?",
        "reframes": [
            "Reverta o risco: garantia, piloto, marco de saída, pagamento por etapa entregue.",
            "Prova: caso parecido + depoimento + número real. Confiança se compra com evidência.",
            "Declare os riscos e como você mitiga cada um — esconder risco assusta mais.",
        ],
        "followup": "Envie 1-2 casos de clientes parecidos e ofereça falar com um deles como referência.",
    },
    "concorrente": {
        "titulo": "Estou avaliando outro",
        "exemplos": ['"O [concorrente] faz por menos."', '"O outro tem mais recursos."'],
        "medo": "\"Não quero pagar mais caro por algo que acho igual.\"",
        "validar": "O que te atraiu no outro? E o que ainda não te convenceu totalmente nele?",
        "reframes": [
            "Não ataque o concorrente — diferencie pelo que ELE valoriza (o critério que ele te deu).",
            "Traga o custo total (implantação, suporte, resultado), não só o preço de tabela.",
            "Prova de resultado no problema específico dele, não lista de recursos.",
        ],
        "followup": "Monte um comparativo honesto focado no critério nº1 dele e proponha decidir com data.",
    },
}

# --------------------------------------------------------------------------- #
# COMANDOS                                                                      #
# --------------------------------------------------------------------------- #

def cmd_init(_):
    garantir_casa()
    print("✅ Amarra pronta. Arquivos criados em .amarra/ (oportunidades, descoberta, valores).")
    print("   Próximo passo: `nova --cliente \"Nome do cliente\"` para abrir a primeira oportunidade.")

def cmd_nova(a):
    garantir_casa()
    ops = ler_ops()
    if achar_op(ops, a.cliente):
        print(f"⚠️  Já existe uma oportunidade com esse cliente. Use `lista` para ver.")
        return
    nid = prox_id(ops)
    op = {
        "id": nid, "cliente": a.cliente.strip(), "persona": (a.persona or "").strip(),
        "contato": (a.contato or "").strip(), "oferta": (a.oferta or "").strip(),
        "valor": str(num(a.valor)) if a.valor else "", "framework": escolher_framework(a.framework),
        "estagio": "descoberta", "criado": hoje(),
    }
    ops.append(op)
    salvar_ops(ops)
    print(f"✅ Oportunidade #{nid} aberta: {op['cliente']}"
          + (f" ({op['persona']})" if op['persona'] else ""))
    print(f"   Framework de descoberta: {op['framework'].upper()}. "
          f"Rode `preparar --id {nid}` para o roteiro da reunião.")

def cmd_lista(_):
    ops = ler_ops()
    if not ops:
        print("Nenhuma oportunidade ainda. Abra a primeira com `nova --cliente \"Nome\"`.")
        return
    m = moeda()
    print("OPORTUNIDADES\n" + "-" * 60)
    for o in ops:
        v = dinheiro(o["valor"], m) if o.get("valor") else "valor a definir"
        print(f"#{o['id']:<3} {o['cliente'][:28]:<28} {o['estagio']:<12} {v}")

def cmd_preparar(a):
    op = exige_op(a.id)
    cfg = ler_config()
    fw = escolher_framework(a.framework or op.get("framework"))
    tempo = int(a.tempo) if a.tempo else 30
    dados = desc_da_op(op["id"])
    oferta = cfg.get("oferta") or "[o que você vende]"
    print("=" * 66)
    print(f"ROTEIRO DE DESCOBERTA — {op['cliente']}"
          + (f" ({op['persona']})" if op.get('persona') else ""))
    print(f"Duração sugerida: {tempo} min · Framework: {fw.upper()}")
    print("=" * 66)
    print("\n▸ ABERTURA (2-3 min) — crie rapport e combine a agenda. NÃO apresente ainda.")
    print("   \"Antes de começar, tem algo específico que você quer garantir que a gente veja hoje?\"")
    print(f"   \"Minha ideia: nos primeiros {max(tempo-10,15)} min eu te escuto pra entender seu")
    print("    contexto; depois te mostro como costumo ajudar quem está numa situação parecida e")
    print("    a gente decide junto se faz sentido. Combinado?\"")
    print(f"\n▸ DESCOBERTA ({max(tempo-12,15)} min) — escute mais do que fala. Perguntas por dimensão:")
    for dim, perguntas in BANCO[fw]:
        print(f"\n   {dim}")
        for p in perguntas:
            print(f"     • {p}")
    print("\n▸ PRÉVIA DA SOLUÇÃO (5-7 min) — provoque, não demonstre tudo.")
    print(f"   \"Pelo que você contou — principalmente [dor] e [meta] — é assim que costumo ajudar")
    print(f"    com {oferta}...\"  Mostre 1 resultado, 1 prova, 1 caminho de 3 passos. Sem preço ainda.")
    print("\n▸ PRÓXIMO PASSO (3-5 min) — feche com um compromisso mútuo e uma DATA.")
    print("   \"Faz sentido eu te mandar uma proposta com o escopo e as opções até [data], e a")
    print("    gente marca 15 min pra revisar juntos em [data]?\"")
    if dados:
        print("\n▸ JÁ SABEMOS (do que foi capturado antes — confirme, não repita):")
        for k, v in dados.items():
            if v:
                print(f"     - {CHAVES.get(k, k)}: {v}")
    print("\n" + "-" * 66)
    print("Depois da reunião: rode `capturar --id %s --dor \"...\" --impacto \"...\" --decisor \"...\"`" % op["id"])
    print("para registrar o que o cliente disse; depois `qualificar --id %s`." % op["id"])
    print("Lembre: você (dono) CONDUZ a conversa. A IA só te preparou o roteiro.")

def cmd_capturar(a):
    op = exige_op(a.id)
    linhas = ler_desc()
    campos = {k: getattr(a, k) for k in CHAVES if getattr(a, k, None) is not None}
    if not campos:
        print("Nada capturado. Passe ao menos um campo, ex.: --dor \"...\" --impacto \"...\".")
        print("Campos: " + ", ".join(f"--{k}" for k in CHAVES))
        return
    for k, v in campos.items():
        v = (v or "").strip()
        # upsert por (op, chave)
        achou = False
        for l in linhas:
            if l["oportunidade_id"] == op["id"] and l["chave"] == k:
                l["valor"] = v
                achou = True
        if not achou:
            linhas.append({"oportunidade_id": op["id"], "chave": k, "valor": v})
    salvar_desc(linhas)
    print(f"✅ Descoberta de #{op['id']} ({op['cliente']}) atualizada:")
    for k in campos:
        print(f"   - {CHAVES[k]}: {campos[k]}")
    print(f"\nRode `qualificar --id {op['id']}` para pontuar a chance e ver as lacunas.")

def cmd_escuta(a):
    op = exige_op(a.id)
    dados = desc_da_op(op["id"])
    print(f"O QUE SABEMOS DE #{op['id']} — {op['cliente']}\n" + "-" * 60)
    algum = False
    for k, rot in CHAVES.items():
        v = dados.get(k, "")
        if v:
            print(f"  {rot}: {v}")
            algum = True
        else:
            print(f"  {rot}: [A CONFERIR]")
    if not algum:
        print("\n(Ainda não capturamos nada. Rode `capturar --id %s --dor \"...\"`.)" % op["id"])

# pesos da qualificação (soma 100)
PESO_QUAL = {"dor": 20, "impacto": 15, "meta": 10, "decisor": 15, "campeao": 15,
             "prazo": 10, "orcamento": 10, "criterio": 5}

def cmd_qualificar(a):
    op = exige_op(a.id)
    dados = desc_da_op(op["id"])
    score = 0
    presentes, lacunas = [], []
    for k, peso in PESO_QUAL.items():
        if dados.get(k):
            score += peso
            presentes.append((k, peso))
        else:
            lacunas.append((k, peso))
    # campeão check
    tem_campeao = bool(dados.get("campeao"))
    tem_decisor = bool(dados.get("decisor"))
    print("=" * 60)
    print(f"QUALIFICAÇÃO — #{op['id']} {op['cliente']}   ·   NOTA: {score}/100")
    if score >= 70:
        vered = "🟢 AVANÇAR — chance sólida. Pode montar a proposta."
    elif score >= 45:
        vered = "🟡 NUTRIR — falta base. Volte às lacunas antes de propor."
    else:
        vered = "🔴 DESQUALIFICAR ou NUTRIR — informação insuficiente pra investir tempo."
    print(vered)
    print("=" * 60)
    print("\n✅ O que já temos:")
    for k, p in presentes:
        print(f"   +{p:>2}  {CHAVES[k]}: {dados[k][:54]}")
    if lacunas:
        print("\n❓ Lacunas (pergunte na próxima conversa):")
        for k, p in lacunas:
            print(f"   -{p:>2}  {CHAVES[k]}  → [A CONFERIR]")
    print("\n🎯 Teste do campeão (em venda consultiva, sem campeão não avança):")
    print(f"   {'✅' if tem_campeao else '⚠️ '} Tem alguém defendendo por dentro? "
          + (dados.get('campeao','') if tem_campeao else "NÃO mapeado — descubra quem."))
    print(f"   {'✅' if tem_decisor else '⚠️ '} O decisor econômico está mapeado? "
          + (dados.get('decisor','') if tem_decisor else "NÃO — quem assina o orçamento?"))
    if score >= 70:
        print(f"\n➡️  `valor --id {op['id']}` para a conta do ROI, depois `proposta --id {op['id']}`.")
    else:
        print(f"\n➡️  Feche as lacunas com `capturar --id {op['id']} ...` e qualifique de novo.")

def cmd_valor_add(a):
    op = exige_op(a.id)
    linhas = ler_vals()
    tipo = sem_acento(a.tipo or "economia")
    if tipo not in ("economia", "ganho", "tempo"):
        tipo = "economia"
    linhas.append({"oportunidade_id": op["id"], "driver": a.driver.strip(),
                   "tipo": tipo, "valor_ano": str(num(a.valor))})
    salvar_vals(linhas)
    print(f"✅ Driver de valor adicionado a #{op['id']}: {a.driver} "
          f"({tipo}, {dinheiro(num(a.valor), moeda())}/ano).")
    print(f"   Rode `valor --id {op['id']} --investimento <valor>` para ver o ROI.")

def cmd_valor(a):
    op = exige_op(a.id)
    m = moeda()
    drivers = vals_da_op(op["id"])
    if not drivers:
        print(f"Ainda não há drivers de valor em #{op['id']}. Adicione com:")
        print(f"   `valor-add --id {op['id']} --driver \"economia de X\" --tipo economia --valor 12000`")
        print("Nunca invente o retorno — use números que o CLIENTE te deu na descoberta.")
        return
    total = sum(num(d["valor_ano"]) for d in drivers)
    print("=" * 60)
    print(f"VALOR / ROI — #{op['id']} {op['cliente']}")
    print("=" * 60)
    print("\nGanho anual estimado (premissas do próprio cliente):")
    for d in drivers:
        print(f"   • {d['driver'][:42]:<42} {dinheiro(d['valor_ano'], m):>16}  [{d['tipo']}]")
    print(f"   {'TOTAL/ano':<42} {dinheiro(total, m):>16}")
    inv = num(a.investimento) if a.investimento else 0.0
    if inv > 0:
        roi = (total - inv) / inv * 100 if inv else 0
        payback = (inv / total * 12) if total > 0 else None
        print(f"\nInvestimento (ano 1): {dinheiro(inv, m)}")
        print(f"Retorno líquido ano 1: {dinheiro(total - inv, m)}")
        print(f"ROI ano 1: {dec1(roi)}%")
        if payback is not None:
            print(f"Payback: {dec1(payback)} meses")
        if roi >= 100:
            print("🟢 Retorno forte — leve essa conta pra dentro da proposta.")
        elif roi >= 0:
            print("🟡 Retorno positivo, mas magro — reforce ganhos ou ajuste o escopo/preço.")
        else:
            print("🔴 Não fecha com esse investimento — reveja escopo, opção menor ou mais valor.")
    else:
        print("\n(Passe `--investimento <valor>` para calcular ROI e payback.)")
    print("\nÉ estimativa, não promessa. Use na seção ROI da proposta com as premissas à vista.")

def _opcoes(a, m):
    """Monta as 3 opções bom/melhor/ótimo. Preço só se o dono passar --opcoes; nunca inventa."""
    nomes = ["Essencial (bom)", "Recomendada (melhor)", "Completa (ótimo)"]
    precos = []
    if a.opcoes:
        precos = [num(x) for x in str(a.opcoes).split(",")][:3]
    linhas = []
    for i, nome in enumerate(nomes):
        preco = dinheiro(precos[i], m) if i < len(precos) and precos[i] > 0 else "[DEFINIR PREÇO]"
        linhas.append((nome, preco))
    return linhas

def cmd_proposta(a):
    op = exige_op(a.id)
    cfg = ler_config()
    m = cfg.get("moeda", "R$")
    d = desc_da_op(op["id"])
    drivers = vals_da_op(op["id"])
    total_valor = sum(num(x["valor_ano"]) for x in drivers)
    oferta = op.get("oferta") or cfg.get("oferta") or "[a solução proposta]"
    g = lambda k: d.get(k) or "[A CONFERIR]"

    L = []
    L.append(f"# Proposta para {op['cliente']}")
    L.append(f"**Preparada por:** {cfg.get('negocio') or '[seu negócio]'}  ·  **Data:** {hoje()}  "
             f"·  **Válida até:** 30 dias")
    L.append("")
    L.append("## Resumo")
    L.append(f"1. **O que ouvimos:** {g('dor')}")
    L.append(f"2. **O que propomos:** {oferta}")
    L.append(f"3. **Resultado esperado:** {g('meta')}" + (f" (até {d['prazo']})" if d.get('prazo') else ""))
    L.append("")
    L.append("## 1. Sua situação (do jeito que você nos contou)")
    L.append(f"- **Como está hoje:** {g('situacao')}")
    L.append(f"- **O que incomoda:** {g('dor')}")
    L.append(f"- **Custo de não resolver:** {g('impacto')}")
    L.append(f"- **Onde você quer chegar:** {g('meta')}")
    if d.get("decisor") or d.get("campeao"):
        L.append(f"- **Quem está envolvido:** " +
                 ", ".join(x for x in [d.get('campeao'), d.get('decisor')] if x))
    L.append("")
    L.append("## 2. Solução recomendada")
    L.append(f"Propomos **{oferta}**, desenhada para o que você descreveu — liderando pelo resultado, "
             "não pela lista de recursos.")
    L.append("")
    L.append("**O que está incluído:**")
    L.append("- ✅ [Entregável 1 — ligue à dor do cliente]")
    L.append("- ✅ [Entregável 2]")
    L.append("- ✅ [Entregável 3]")
    L.append("")
    L.append("**O que NÃO está incluído (fora do escopo):**")
    L.append("- ❌ [Fora de escopo] — disponível como adicional")
    L.append("")
    L.append("## 3. Escopo e fases")
    L.append("- **Fase 1 — [nome] (semanas 1-2):** [entrega] · seu envolvimento: [tempo]")
    L.append("- **Fase 2 — [nome] (semanas 3-6):** [entrega]")
    L.append("- **Fase 3 — [nome] (semanas 7-12):** [entrega]")
    L.append("")
    L.append("## 4. Investimento — 3 opções")
    for nome, preco in _opcoes(a, m):
        L.append(f"### {nome}")
        L.append(f"- Investimento: **{preco}**")
        L.append("- Inclui: [itens desta opção]")
        L.append("")
    L.append("_Condições: [à vista / parcelado / entrada + saldo]. Preços em " + m + ", + impostos._")
    L.append("")
    L.append("## 5. Critérios de sucesso (combinados desde já)")
    L.append("| Indicador | Hoje | Meta 90 dias | Meta 12 meses |")
    L.append("|---|---|---|---|")
    L.append("| [Indicador 1] | [nº] | [nº] | [nº] |")
    L.append("| [Indicador 2] | [nº] | [nº] | [nº] |")
    L.append("")
    L.append("## 6. Retorno esperado (ROI)")
    if drivers:
        L.append("| Fonte de ganho | Impacto/ano |")
        L.append("|---|---|")
        for x in drivers:
            L.append(f"| {x['driver']} | {dinheiro(x['valor_ano'], m)} |")
        L.append(f"| **Total/ano** | **{dinheiro(total_valor, m)}** |")
        L.append("")
        L.append("_Estimativa com base nas premissas que você compartilhou. A IA calcula, você confere._")
    else:
        L.append("[A CONFERIR — quantifique o retorno com os números que o cliente deu na descoberta. "
                 "Rode `valor-add` para montar esta tabela. Não invente.]")
    L.append("")
    L.append("## 7. Riscos e como mitigamos (transparência gera confiança)")
    L.append("| Risco | Mitigação |")
    L.append("|---|---|")
    L.append("| [Atraso de implantação] | Rollout em fases, PM dedicado |")
    L.append("| [Baixa adoção] | Treinamento + acompanhamento |")
    L.append("")
    L.append("## 8. Próximo passo")
    L.append("1. Você revisa a proposta" + (f" com {d['decisor']}" if d.get('decisor') else "") + " até [data]")
    L.append("2. Tiramos dúvidas numa call de 15 min em [data]")
    L.append("3. Fechamento e kickoff")
    L.append("")
    L.append("---")
    L.append(f"**Aceite:** ao aprovar, {op['cliente']} concorda com o escopo, o investimento e as "
             "condições da **Opção [ ___ ]**.")
    L.append("")
    L.append("Assinatura: __________________________   Data: ____________")

    texto = "\n".join(L)
    saida = a.saida or os.path.join(CASA, f"proposta-{op['id']}.md")
    with open(saida, "w", encoding="utf-8") as f:
        f.write(texto + "\n")
    print(texto)
    print("\n" + "-" * 66)
    faltas = [CHAVES[k] for k in ("dor", "impacto", "meta") if not d.get(k)]
    if faltas:
        print("⚠️  A proposta tem [A CONFERIR] em: " + ", ".join(faltas) +
              ". Capture isso antes de enviar — a força vem de mostrar que você OUVIU.")
    if "[DEFINIR PREÇO]" in texto:
        print("⚠️  Defina os preços das 3 opções (ou passe `--opcoes \"3000,6000,9000\"`). "
              "A Amarra nunca inventa preço.")
    print(f"📄 Rascunho salvo em: {saida}")
    print("Revise, ajuste os [colchetes] e ENVIE você mesmo. A IA redigiu; a venda é sua.")

def cmd_objecoes(a):
    if a.tipo:
        chave = sem_acento(a.tipo)
        mapa = {"preco": "preco", "orcamento": "preco", "caro": "preco",
                "tempo": "tempo", "timing": "tempo", "momento": "tempo",
                "statusquo": "statusquo", "concorrente_uso": "statusquo", "planilha": "statusquo",
                "autoridade": "autoridade", "decisor": "autoridade", "socio": "autoridade",
                "ajuste": "ajuste", "fit": "ajuste", "necessidade": "ajuste",
                "risco": "risco", "confianca": "risco",
                "concorrente": "concorrente"}
        alvo = mapa.get(chave)
        if not alvo:
            print("Categorias: preco, tempo, statusquo, autoridade, ajuste, risco, concorrente.")
            return
        _print_objecao(alvo)
        return
    print("BIBLIOTECA DE OBJEÇÕES — 7 categorias (rode com --tipo <cat> para uma só)\n")
    for chave in OBJECOES:
        _print_objecao(chave)
        print()

def _print_objecao(chave):
    o = OBJECOES[chave]
    print("=" * 60)
    print(f"▣ {o['titulo']}")
    print("  Ex.: " + "  ".join(o["exemplos"]))
    print(f"  Medo real por trás: {o['medo']}")
    print(f"  Valide primeiro: \"{o['validar']}\"")
    print("  Reframes:")
    for r in o["reframes"]:
        print(f"    → {r}")
    print(f"  Follow-up: {o['followup']}")

def cmd_painel(a):
    op = exige_op(a.id)
    d = desc_da_op(op["id"])
    m = moeda()
    drivers = vals_da_op(op["id"])
    score = sum(p for k, p in PESO_QUAL.items() if d.get(k))
    print("=" * 60)
    print(f"PAINEL — #{op['id']} {op['cliente']}  ·  estágio: {op['estagio']}")
    print("=" * 60)
    print(f"Nota de qualificação: {score}/100  "
          + ("🟢" if score >= 70 else "🟡" if score >= 45 else "🔴"))
    print(f"Dor: {d.get('dor') or '[A CONFERIR]'}")
    print(f"Impacto (custo de não resolver): {d.get('impacto') or '[A CONFERIR]'}")
    print(f"Decisor: {d.get('decisor') or '[A CONFERIR]'}   ·   "
          f"Campeão: {d.get('campeao') or '[A CONFERIR]'}")
    if drivers:
        tot = sum(num(x['valor_ano']) for x in drivers)
        print(f"Valor/ano estimado: {dinheiro(tot, m)}")
    print("\nRode `plano --id %s` para as próximas ações ordenadas por risco." % op["id"])

def cmd_plano(a):
    op = exige_op(a.id)
    d = desc_da_op(op["id"])
    score = sum(p for k, p in PESO_QUAL.items() if d.get(k))
    drivers = vals_da_op(op["id"])
    acoes = []
    # ordenado por risco: lacuna crítica -> campeão -> decisor -> valor -> proposta -> follow-up
    if not d.get("dor"):
        acoes.append("🔴 Capturar a DOR real do cliente — sem ela não há venda consultiva.")
    if not d.get("impacto"):
        acoes.append("🔴 Quantificar o CUSTO DE NÃO RESOLVER — é a âncora do preço e do ROI.")
    if not d.get("campeao"):
        acoes.append("🟠 Descobrir o CAMPEÃO interno — quem defende isso quando você não está na sala.")
    if not d.get("decisor"):
        acoes.append("🟠 Mapear o DECISOR econômico — quem assina o orçamento.")
    if not d.get("meta"):
        acoes.append("🟡 Registrar a META do cliente com número e prazo.")
    if not drivers:
        acoes.append("🟡 Montar a conta do VALOR/ROI com os números do próprio cliente (`valor-add`).")
    if score >= 70 and not os.path.exists(os.path.join(CASA, f"proposta-{op['id']}.md")):
        acoes.append("🟢 Qualificação sólida — gerar a PROPOSTA (`proposta --id %s`)." % op["id"])
    acoes.append("⚪ Preparar as OBJEÇÕES prováveis (`objecoes`) antes de enviar/apresentar.")
    print(f"PLANO PARA FECHAR — #{op['id']} {op['cliente']}\n" + "-" * 60)
    for a_ in acoes:
        print("  " + a_)
    print("\nLembre: a Amarra prepara e redige. Quem conduz a conversa e envia é você.")

def cmd_ajuda(_):
    print("""Amarra — venda consultiva B2B (offline, dados 100% locais)

FLUXO: nova → preparar (reunião) → capturar (o que o cliente disse) → qualificar →
       valor/ROI → proposta → objecoes.  Veja tudo com painel/plano.

  init                                     cria os arquivos em .amarra/
  nova --cliente "X" [--persona ..] [--oferta ..] [--valor ..] [--framework spin|gpct|meddic|bant]
  lista                                    todas as oportunidades
  preparar --id N [--framework ..] [--tempo 30]     roteiro da reunião de descoberta
  capturar --id N [--dor ..] [--impacto ..] [--meta ..] [--decisor ..] [--campeao ..]
                  [--prazo ..] [--orcamento ..] [--criterio ..] [--concorrente ..] [--situacao ..]
  escuta --id N                            mostra o que já foi capturado
  qualificar --id N                        nota 0-100, lacunas, teste do campeão
  valor-add --id N --driver "X" --tipo economia|ganho|tempo --valor 12000
  valor --id N [--investimento V]          soma o ganho, calcula ROI e payback
  proposta --id N [--opcoes "3000,6000,9000"] [--saida arquivo.md]   proposta consultiva completa
  objecoes [--tipo preco|tempo|statusquo|autoridade|ajuste|risco|concorrente]
  painel --id N   ·   plano --id N

Regras: nunca inventa dor/número/decisor/preço → [A CONFERIR]. Sempre 3 opções na proposta.
A IA prepara e redige; o DONO conduz a reunião e envia. Não acessa a internet.""")

# --------------------------------------------------------------------------- #
# CLI                                                                          #
# --------------------------------------------------------------------------- #

def main():
    p = argparse.ArgumentParser(prog="amarra", add_help=False)
    sub = p.add_subparsers(dest="cmd")

    sub.add_parser("init")
    sp = sub.add_parser("nova")
    sp.add_argument("--cliente", required=True)
    sp.add_argument("--persona"); sp.add_argument("--contato")
    sp.add_argument("--oferta"); sp.add_argument("--valor"); sp.add_argument("--framework")
    sub.add_parser("lista")
    sp = sub.add_parser("preparar")
    sp.add_argument("--id", required=True); sp.add_argument("--framework"); sp.add_argument("--tempo")
    sp = sub.add_parser("capturar")
    sp.add_argument("--id", required=True)
    for k in CHAVES:
        sp.add_argument("--" + k)
    sp = sub.add_parser("escuta"); sp.add_argument("--id", required=True)
    sp = sub.add_parser("qualificar"); sp.add_argument("--id", required=True)
    sp = sub.add_parser("valor-add")
    sp.add_argument("--id", required=True); sp.add_argument("--driver", required=True)
    sp.add_argument("--tipo"); sp.add_argument("--valor", required=True)
    sp = sub.add_parser("valor"); sp.add_argument("--id", required=True); sp.add_argument("--investimento")
    sp = sub.add_parser("proposta")
    sp.add_argument("--id", required=True); sp.add_argument("--opcoes"); sp.add_argument("--saida")
    sp = sub.add_parser("objecoes"); sp.add_argument("--tipo")
    sp = sub.add_parser("painel"); sp.add_argument("--id", required=True)
    sp = sub.add_parser("plano"); sp.add_argument("--id", required=True)
    sub.add_parser("ajuda")

    a = p.parse_args()
    cmds = {
        "init": cmd_init, "nova": cmd_nova, "lista": cmd_lista, "preparar": cmd_preparar,
        "capturar": cmd_capturar, "escuta": cmd_escuta, "qualificar": cmd_qualificar,
        "valor-add": cmd_valor_add, "valor": cmd_valor, "proposta": cmd_proposta,
        "objecoes": cmd_objecoes, "painel": cmd_painel, "plano": cmd_plano, "ajuda": cmd_ajuda,
    }
    if not a.cmd:
        cmd_ajuda(a)
        return
    cmds[a.cmd](a)

if __name__ == "__main__":
    main()
