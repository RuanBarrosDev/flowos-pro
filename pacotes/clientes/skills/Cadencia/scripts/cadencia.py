#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
cadencia.py — motor de RECEITA RECORRENTE (MRR) do pequeno negócio (offline, só biblioteca padrão).

Filosofia (igual aos irmãos Farol/Maré/Régua/Lastro):
  - A Cadência modela a RECEITA QUE SE REPETE TODO MÊS (assinaturas, mensalidades, fee, planos) —
    responde "minha receita é previsível? está crescendo ou vazando? quanto vale um cliente?
    onde chego em N meses?".
  - Insight que a torna confiável: a IA NÃO chuta os números. O MRR e o "movimento do mês"
    (novo/expansão/contração/churn/reativação) saem de um LIVRO-RAZÃO replayado em ordem — então a
    identidade contábil FECHA por construção: MRR fim = MRR início + novo + expansão − contração
    − churn + reativação. Um LLM sozinho trata cada célula como palpite e a conta não bate.
  - SEPARA recorrente de avulso: só o que se REPETE vira MRR. Venda única/setup/projeto NÃO entram.
  - O motor NUNCA inventa um número (assinante, valor, margem, CAC, churn). Se falta dado, avisa.
  - SEMPRE mostra a conta. Não acessa a internet. Projeção é estimativa — premissas explícitas.

Dados (tudo em <raiz>/.cadencia/, git-ignored):
  config.md       — negócio, moeda, margem bruta padrão (%), CAC médio (opcional)
  assinantes.csv  — id, nome, plano, valor, ciclo, mrr, inicio, status, fim, criado
  movimentos.csv  — mes, assinante_id, tipo, valor_mrr, obs   (o livro-razão do MRR)

Uso: python3 cadencia.py <comando> [opções].  Rode `python3 cadencia.py ajuda` para o mapa.
"""

import os
import sys
import csv
import re
import argparse
import unicodedata
from datetime import date

# --------------------------------------------------------------------------- #
# Localização da "casa" de dados (.cadencia/)                                  #
# --------------------------------------------------------------------------- #

def achar_raiz():
    """Ancora o .cadencia/ na raiz do projeto do membro.
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
CASA = os.path.join(RAIZ, ".cadencia")
CONFIG = os.path.join(CASA, "config.md")
ASSIN = os.path.join(CASA, "assinantes.csv")
MOVS = os.path.join(CASA, "movimentos.csv")

COLS_ASSIN = ["id", "nome", "plano", "valor", "ciclo", "mrr", "inicio", "status", "fim", "criado"]
COLS_MOV = ["mes", "assinante_id", "tipo", "valor_mrr", "obs"]

MESES_CICLO = {"mensal": 1, "trimestral": 3, "semestral": 6, "anual": 12}

# tipos de movimento e o SINAL que aplicam ao MRR
SINAL = {"novo": +1, "expansao": +1, "reativacao": +1, "contracao": -1, "churn": -1}

MES_NOME = {
    "janeiro": 1, "fevereiro": 2, "marco": 3, "abril": 4, "maio": 5, "junho": 6,
    "julho": 7, "agosto": 8, "setembro": 9, "outubro": 10, "novembro": 11, "dezembro": 12,
    "jan": 1, "fev": 2, "mar": 3, "abr": 4, "mai": 5, "jun": 6, "jul": 7, "ago": 8,
    "set": 9, "out": 10, "nov": 11, "dez": 12,
}

# --------------------------------------------------------------------------- #
# Leitura/escrita                                                             #
# --------------------------------------------------------------------------- #

def garantir_casa():
    os.makedirs(CASA, exist_ok=True)
    if not os.path.exists(ASSIN):
        _escrever(ASSIN, COLS_ASSIN, [])
    if not os.path.exists(MOVS):
        _escrever(MOVS, COLS_MOV, [])

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

def ler_assinantes():
    return _ler(ASSIN, COLS_ASSIN)

def salvar_assinantes(linhas):
    _escrever(ASSIN, COLS_ASSIN, linhas)

def ler_movs():
    return _ler(MOVS, COLS_MOV)

def salvar_movs(linhas):
    _escrever(MOVS, COLS_MOV, linhas)

# --------------------------------------------------------------------------- #
# Parsers BR e texto                                                          #
# --------------------------------------------------------------------------- #

def sem_acento(s):
    s = unicodedata.normalize("NFD", s or "")
    return "".join(c for c in s if unicodedata.category(c) != "Mn").lower().strip()

def num(v, padrao=0.0):
    """Parser BR robusto. Aceita '1.234,56', '50.000', '199,90', 'R$ 89', '12,5', '1000'.
    Regra: vírgula = decimal; ponto agrupando 3 dígitos = separador de milhar."""
    if v is None:
        return padrao
    s = str(v).strip().replace("R$", "").replace(" ", "")
    if s == "":
        return padrao
    neg = s.startswith("-")
    s = s.lstrip("+-")
    if "," in s:
        s = s.replace(".", "").replace(",", ".")
    elif "." in s:
        if re.fullmatch(r"\d{1,3}(\.\d{3})+", s):
            s = s.replace(".", "")
    try:
        x = float(s)
        return -x if neg else x
    except ValueError:
        return padrao

def mes_iso(v, padrao=None):
    """Normaliza uma competência para 'AAAA-MM'. Aceita 'AAAA-MM', 'MM/AAAA', 'AAAA/MM',
    'agosto/2026', 'ago 2026', 'agosto de 2026'. Retorna padrao (ou mês atual) se vazio."""
    if v is None or str(v).strip() == "":
        if padrao is not None:
            return padrao
        hoje = date.today()
        return f"{hoje.year:04d}-{hoje.month:02d}"
    s = sem_acento(str(v)).replace(" de ", " ").strip()
    # AAAA-MM ou AAAA/MM
    m = re.fullmatch(r"(\d{4})[-/](\d{1,2})", s)
    if m:
        return f"{int(m.group(1)):04d}-{int(m.group(2)):02d}"
    # MM/AAAA
    m = re.fullmatch(r"(\d{1,2})[-/](\d{4})", s)
    if m:
        return f"{int(m.group(2)):04d}-{int(m.group(1)):02d}"
    # nome do mês + ano
    m = re.fullmatch(r"([a-z]+)[ /]+(\d{4})", s)
    if m and m.group(1) in MES_NOME:
        return f"{int(m.group(2)):04d}-{MES_NOME[m.group(1)]:02d}"
    # só o nome do mês -> ano atual
    if s in MES_NOME:
        return f"{date.today().year:04d}-{MES_NOME[s]:02d}"
    return padrao if padrao is not None else f"{date.today().year:04d}-{date.today().month:02d}"

def mes_add(mes, k):
    """Soma k meses a 'AAAA-MM' -> 'AAAA-MM'."""
    a, m = int(mes[:4]), int(mes[5:7])
    total = a * 12 + (m - 1) + k
    return f"{total // 12:04d}-{total % 12 + 1:02d}"

def mes_diff(a, b):
    """Meses de a até b (b - a). Ambos 'AAAA-MM'."""
    return (int(b[:4]) * 12 + int(b[5:7])) - (int(a[:4]) * 12 + int(a[5:7]))

def norm_ciclo(v):
    s = sem_acento(v)
    for k in MESES_CICLO:
        if s.startswith(k[:4]):
            return k
    return "mensal"

def mrr_de(valor, ciclo):
    """MRR normalizado = o que é cobrado no ciclo dividido pelos meses do ciclo."""
    return round(num(valor) / MESES_CICLO.get(ciclo, 1), 2)

# --------------------------------------------------------------------------- #
# Config                                                                       #
# --------------------------------------------------------------------------- #

def ler_config():
    cfg = {"negocio": "", "moeda": "R$", "margem": None, "cac": None}
    if not os.path.exists(CONFIG):
        return cfg
    for linha in open(CONFIG, encoding="utf-8"):
        m = re.match(r"\s*-\s*\*\*(.+?):\*\*\s*(.*)", linha)
        if not m:
            continue
        rot = sem_acento(m.group(1))
        val = m.group(2).strip()
        if "negocio" in rot:
            cfg["negocio"] = val
        elif "moeda" in rot:
            cfg["moeda"] = val or "R$"
        elif "margem" in rot:
            cfg["margem"] = num(val.replace("%", "")) if val else None
        elif "cac" in rot:
            cfg["cac"] = num(val) if val else None
    return cfg

def money(x, cfg):
    s = f"{abs(x):,.2f}".replace(",", "§").replace(".", ",").replace("§", ".")
    return f"{cfg['moeda']} {'-' if x < 0 else ''}{s}"

def pct(x):
    return f"{x*100:.1f}%".replace(".", ",")

# --------------------------------------------------------------------------- #
# Núcleo: MRR derivado do LIVRO-RAZÃO (identidade garantida)                   #
# --------------------------------------------------------------------------- #

def meses_com_dados():
    ms = sorted({m["mes"] for m in ler_movs() if m.get("mes")})
    return ms

def mrr_ate(mes_incl):
    """MRR acumulado (soma dos deltas com sinal) até o fim de 'mes_incl', inclusive."""
    total = 0.0
    for mv in ler_movs():
        if mv["mes"] <= mes_incl:
            total += SINAL.get(mv["tipo"], 0) * num(mv["valor_mrr"])
    return round(total, 2)

def movimento_do_mes(mes):
    """Agrega os deltas do mês por tipo. Retorna dict com novo/expansao/contracao/churn/reativacao."""
    ag = {t: 0.0 for t in SINAL}
    for mv in ler_movs():
        if mv["mes"] == mes and mv["tipo"] in ag:
            ag[mv["tipo"]] += num(mv["valor_mrr"])
    return {k: round(v, 2) for k, v in ag.items()}

def ativos_em(mes):
    """Lista de assinantes ATIVOS ao fim de 'mes' (inicio<=mes e (status ativo OU fim>mes))."""
    out = []
    for a in ler_assinantes():
        ini = a.get("inicio", "")
        if not ini or ini > mes:
            continue
        fim = a.get("fim", "")
        if a.get("status") == "cancelado" and fim and fim <= mes:
            continue
        out.append(a)
    return out

def mrr_ativos_em(mes):
    return round(sum(num(a["mrr"]) for a in ativos_em(mes)), 2)

def proximo_id():
    ids = [int(a["id"]) for a in ler_assinantes() if str(a.get("id", "")).isdigit()]
    return (max(ids) + 1) if ids else 1

def achar_assinante(idv):
    for a in ler_assinantes():
        if str(a["id"]) == str(idv):
            return a
    return None

def registrar_mov(mes, aid, tipo, valor_mrr, obs=""):
    movs = ler_movs()
    movs.append({"mes": mes, "assinante_id": str(aid), "tipo": tipo,
                 "valor_mrr": f"{abs(round(valor_mrr,2))}", "obs": obs})
    salvar_movs(movs)

# --------------------------------------------------------------------------- #
# Semáforos                                                                    #
# --------------------------------------------------------------------------- #

def sinal_crescimento(net):
    if net > 0.005:
        return "🟢 crescendo"
    if net < -0.005:
        return "🔴 encolhendo"
    return "🟡 de pé (estável)"

# --------------------------------------------------------------------------- #
# Comandos                                                                     #
# --------------------------------------------------------------------------- #

def cmd_init(args):
    garantir_casa()
    print("✅ Cadência iniciada. Arquivos de dados criados em .cadencia/ (assinantes.csv, movimentos.csv).")

def cmd_novo(args):
    garantir_casa()
    cfg = ler_config()
    ciclo = norm_ciclo(args.ciclo or "mensal")
    valor = num(args.valor)
    if valor <= 0:
        print("⚠️  Preciso do valor cobrado (> 0). Nada foi gravado. Ex.: --valor 199,90")
        return
    mrr = mrr_de(valor, ciclo)
    mes = mes_iso(args.mes)
    aid = proximo_id()
    a = {"id": str(aid), "nome": args.nome or f"Assinante {aid}", "plano": args.plano or "",
         "valor": f"{valor}", "ciclo": ciclo, "mrr": f"{mrr}", "inicio": mes,
         "status": "ativo", "fim": "", "criado": date.today().isoformat()}
    ass = ler_assinantes(); ass.append(a); salvar_assinantes(ass)
    registrar_mov(mes, aid, "novo", mrr, obs=a["plano"])
    extra = "" if ciclo == "mensal" else f" (cobrança {ciclo} de {money(valor,cfg)} → {money(mrr,cfg)}/mês normalizado)"
    print(f"✅ Novo assinante #{aid} — {a['nome']} · plano {a['plano'] or '—'} · {money(mrr,cfg)}/mês · entrou {mes}{extra}")
    print(f"   MRR total agora ({mes}): {money(mrr_ate(mes), cfg)}")

def cmd_expansao(args):
    _ajuste(args, "expansao")

def cmd_contracao(args):
    _ajuste(args, "contracao")

def _ajuste(args, tipo):
    garantir_casa()
    cfg = ler_config()
    a = achar_assinante(args.id)
    if not a:
        print(f"⚠️  Assinante #{args.id} não encontrado. Nada foi gravado.")
        return
    if a.get("status") != "ativo":
        print(f"⚠️  Assinante #{args.id} ({a['nome']}) não está ativo (status: {a.get('status')}). "
              f"Para trazê-lo de volta use 'reativacao'.")
        return
    mrr_antigo = num(a["mrr"])
    mes = mes_iso(args.mes)
    if args.novo_valor is not None:
        ciclo = a.get("ciclo", "mensal")
        mrr_novo = mrr_de(num(args.novo_valor), ciclo)
        a["valor"] = f"{num(args.novo_valor)}"
    elif args.delta is not None:
        d = abs(num(args.delta))
        mrr_novo = mrr_antigo + d if tipo == "expansao" else mrr_antigo - d
    else:
        print("⚠️  Informe --novo-valor (o novo preço) ou --delta (quanto mudou no MRR). Nada gravado.")
        return
    delta = round(mrr_novo - mrr_antigo, 2)
    if tipo == "expansao" and delta <= 0:
        print("⚠️  Expansão precisa AUMENTAR o MRR. O novo valor não é maior que o atual. Nada gravado.")
        return
    if tipo == "contracao" and delta >= 0:
        print("⚠️  Contração precisa DIMINUIR o MRR. O novo valor não é menor que o atual. Nada gravado.")
        return
    a["mrr"] = f"{round(mrr_novo,2)}"
    ass = [x if x["id"] != a["id"] else a for x in ler_assinantes()]
    salvar_assinantes(ass)
    registrar_mov(mes, a["id"], tipo, abs(delta), obs="")
    verbo = "subiu" if tipo == "expansao" else "caiu"
    print(f"✅ {tipo.capitalize()} de #{a['id']} ({a['nome']}) em {mes}: MRR {verbo} "
          f"{money(mrr_antigo,cfg)} → {money(mrr_novo,cfg)} ({'+' if delta>0 else ''}{money(delta,cfg)})")
    print(f"   MRR total agora ({mes}): {money(mrr_ate(mes), cfg)}")

def cmd_churn(args):
    garantir_casa()
    cfg = ler_config()
    a = achar_assinante(args.id)
    if not a:
        print(f"⚠️  Assinante #{args.id} não encontrado. Nada foi gravado.")
        return
    if a.get("status") == "cancelado":
        print(f"⚠️  #{args.id} ({a['nome']}) já está cancelado desde {a.get('fim') or '—'}.")
        return
    mrr = num(a["mrr"])
    mes = mes_iso(args.mes)
    a["status"] = "cancelado"; a["fim"] = mes
    ass = [x if x["id"] != a["id"] else a for x in ler_assinantes()]
    salvar_assinantes(ass)
    registrar_mov(mes, a["id"], "churn", mrr, obs=args.motivo or "")
    print(f"✅ Churn de #{a['id']} ({a['nome']}) em {mes}: saiu {money(mrr,cfg)}/mês da base"
          + (f" · motivo: {args.motivo}" if args.motivo else ""))
    print(f"   MRR total agora ({mes}): {money(mrr_ate(mes), cfg)}")

def cmd_reativacao(args):
    garantir_casa()
    cfg = ler_config()
    a = achar_assinante(args.id)
    if not a:
        print(f"⚠️  Assinante #{args.id} não encontrado. Nada foi gravado.")
        return
    if a.get("status") == "ativo":
        print(f"⚠️  #{args.id} ({a['nome']}) já está ativo. Para aumentar o plano use 'expansao'.")
        return
    mes = mes_iso(args.mes)
    ciclo = a.get("ciclo", "mensal")
    if args.valor is not None:
        mrr = mrr_de(num(args.valor), ciclo); a["valor"] = f"{num(args.valor)}"
    else:
        mrr = num(a["mrr"])  # volta com o mesmo plano de antes
    a["mrr"] = f"{round(mrr,2)}"; a["status"] = "ativo"; a["fim"] = ""
    ass = [x if x["id"] != a["id"] else a for x in ler_assinantes()]
    salvar_assinantes(ass)
    registrar_mov(mes, a["id"], "reativacao", mrr, obs="")
    print(f"✅ Reativação de #{a['id']} ({a['nome']}) em {mes}: voltou {money(mrr,cfg)}/mês para a base")
    print(f"   MRR total agora ({mes}): {money(mrr_ate(mes), cfg)}")

def cmd_base(args):
    garantir_casa()
    cfg = ler_config()
    ass = ler_assinantes()
    if not ass:
        print("A base está vazia. Cadastre o primeiro assinante recorrente com 'novo'. "
              "Lembre: só entra o que se REPETE todo mês — venda avulsa/setup/projeto único não é MRR.")
        return
    ms = meses_com_dados()
    ref = ms[-1] if ms else mes_iso(None)
    ativos = ativos_em(ref)
    print(f"📋 Base recorrente — {cfg['negocio'] or 'seu negócio'} (competência {ref})")
    print(f"{'#':>3}  {'Nome':<22} {'Plano':<12} {'Ciclo':<11} {'MRR':>12}  Status")
    print("-" * 74)
    for a in sorted(ass, key=lambda x: (x.get("status") != "ativo", x.get("nome",""))):
        marca = "ativo" if a.get("status") == "ativo" else f"cancelado {a.get('fim','')}"
        print(f"{a['id']:>3}  {(a.get('nome') or '')[:22]:<22} {(a.get('plano') or '—')[:12]:<12} "
              f"{a.get('ciclo',''):<11} {money(num(a['mrr']),cfg):>12}  {marca}")
    print("-" * 74)
    total = mrr_ativos_em(ref)
    print(f"Ativos: {len(ativos)}   ·   MRR (base ativa): {money(total,cfg)}   ·   "
          f"ARR (×12): {money(total*12,cfg)}")
    razao = mrr_ate(ref)
    if abs(razao - total) > 0.05:
        print(f"ℹ️  Livro-razão do MRR em {ref}: {money(razao,cfg)} "
              f"(pequena diferença para a base ativa pode indicar um lançamento a conferir).")

def cmd_ponte(args):
    """A PONTE do MRR: início + novo + expansão − contração − churn + reativação = fim."""
    garantir_casa()
    cfg = ler_config()
    ms = meses_com_dados()
    if not ms:
        print("Ainda não há movimentos. Cadastre assinantes/eventos primeiro.")
        return
    mes = mes_iso(args.mes, padrao=ms[-1]) if args.mes else ms[-1]
    ini = mrr_ate(mes_add(mes, -1))
    mv = movimento_do_mes(mes)
    net = round(mv["novo"] + mv["expansao"] + mv["reativacao"] - mv["contracao"] - mv["churn"], 2)
    fim = round(ini + net, 2)
    print(f"🌉 Ponte do MRR — {mes}   ({cfg['negocio'] or 'seu negócio'})")
    print("-" * 52)
    print(f"  MRR no início do mês ............ {money(ini,cfg):>16}")
    print(f"  + Novo (clientes novos) ......... {money(mv['novo'],cfg):>16}")
    print(f"  + Expansão (upgrades) ........... {money(mv['expansao'],cfg):>16}")
    print(f"  + Reativação (voltaram) ......... {money(mv['reativacao'],cfg):>16}")
    print(f"  − Contração (downgrades) ........ {money(-mv['contracao'],cfg):>16}")
    print(f"  − Churn (cancelaram) ............ {money(-mv['churn'],cfg):>16}")
    print("-" * 52)
    print(f"  = MRR no fim do mês ............. {money(fim,cfg):>16}")
    print(f"  Movimento líquido (net-new) ..... {('+' if net>=0 else '')+money(net,cfg):>16}   {sinal_crescimento(net/ini if ini else net)}")
    # identidade contábil (fecha por construção)
    conf = mrr_ate(mes)
    ok = abs(conf - fim) < 0.05
    print(f"  Conferência da identidade: {money(conf,cfg)} "
          f"{'✓ fecha' if ok else '✗ NÃO fecha — há lançamento fora de ordem'}")
    # quick ratio do mês
    entra = mv["novo"] + mv["expansao"] + mv["reativacao"]
    sai = mv["churn"] + mv["contracao"]
    if sai > 0:
        qr = entra / sai
        sinal = "🟢 crescimento eficiente" if qr >= 4 else ("🟡 crescendo devagar" if qr >= 1 else "🔴 vazando mais do que entra")
        print(f"  Quick ratio (entra ÷ sai) ....... {qr:.1f}×   {sinal}")
    elif entra > 0:
        print(f"  Quick ratio: só entrou receita neste mês (nenhuma saída) — 🟢")

def cmd_churn_taxa(args):
    """Churn de LOGO (clientes) e de RECEITA (reais) lado a lado."""
    garantir_casa()
    cfg = ler_config()
    ms = meses_com_dados()
    if not ms:
        print("Ainda não há movimentos para calcular churn.")
        return
    mes = mes_iso(args.mes, padrao=ms[-1]) if args.mes else ms[-1]
    ant = mes_add(mes, -1)
    ativos_ini = ativos_em(ant)
    n_ini = len(ativos_ini)
    mrr_ini = mrr_ate(ant)
    # quem cancelou neste mês
    cancelaram = [a for a in ler_assinantes() if a.get("status") == "cancelado" and a.get("fim") == mes]
    n_churn = len(cancelaram)
    mv = movimento_do_mes(mes)
    print(f"💧 Vazamento — {mes}   ({cfg['negocio'] or 'seu negócio'})")
    print("-" * 52)
    if n_ini > 0:
        logo = n_churn / n_ini
        print(f"  Churn de LOGO (clientes): {n_churn} de {n_ini} = {pct(logo)}")
    else:
        logo = 0.0
        print("  Churn de LOGO: base inicial vazia (sem base para medir).")
    if mrr_ini > 0:
        rev_bruto = mv["churn"] / mrr_ini
        rev_liq = (mv["churn"] + mv["contracao"] - mv["expansao"]) / mrr_ini
        print(f"  Churn de RECEITA (bruto, só cancelamentos): {money(mv['churn'],cfg)} de "
              f"{money(mrr_ini,cfg)} = {pct(rev_bruto)}")
        print(f"  Churn de RECEITA (líquido, − expansão): {pct(rev_liq)}")
        if rev_bruto > logo + 0.005 and n_ini > 0:
            print("  ⚠️  A receita está caindo MAIS do que o número de clientes: "
                  "seus assinantes MAIORES estão indo embora — priorize retê-los.")
        elif logo > rev_bruto + 0.005 and n_ini > 0:
            print("  ℹ️  Quem sai são os menores: a perda de clientes pesa pouco no faturamento.")
    else:
        print("  Churn de RECEITA: MRR inicial zero (sem base para medir).")
    if cancelaram:
        motivos = [c.get("id") for c in cancelaram]
        print(f"  Cancelaram em {mes}: " + ", ".join(f"#{c['id']} {c['nome']}" for c in cancelaram))

def cmd_retencao(args):
    """GRR e NRR do mês (baseado no movimento sobre a base inicial)."""
    garantir_casa()
    cfg = ler_config()
    ms = meses_com_dados()
    if not ms:
        print("Ainda não há movimentos para calcular retenção.")
        return
    mes = mes_iso(args.mes, padrao=ms[-1]) if args.mes else ms[-1]
    mrr_ini = mrr_ate(mes_add(mes, -1))
    mv = movimento_do_mes(mes)
    if mrr_ini <= 0:
        print(f"Retenção em {mes}: a base do mês anterior é zero — sem o que reter ainda.")
        return
    grr = (mrr_ini - mv["churn"] - mv["contracao"]) / mrr_ini
    nrr = (mrr_ini - mv["churn"] - mv["contracao"] + mv["expansao"]) / mrr_ini
    print(f"🔁 Retenção de receita — {mes}   (sobre a base de {mes_add(mes,-1)} = {money(mrr_ini,cfg)})")
    print(f"  GRR (retenção BRUTA, sem contar upgrades): {pct(grr)}")
    print(f"  NRR (retenção LÍQUIDA, com upgrades): {pct(nrr)}")
    if nrr >= 1.0:
        print("  🟢 NRR ≥ 100%: sua base cresce SOZINHA, sem cliente novo — os atuais gastam mais "
              "do que os que saem. É o 'churn negativo', o santo graal da recorrência.")
    elif nrr >= 0.9:
        print("  🟡 NRR entre 90% e 100%: a base quase se sustenta; falta um pouco de expansão.")
    else:
        print("  🔴 NRR < 90%: a base atual está vazando receita — mexa em churn e expansão.")

def cmd_coorte(args):
    """Matriz de retenção por coorte (mês de entrada × meses depois)."""
    garantir_casa()
    cfg = ler_config()
    ass = ler_assinantes()
    if not ass:
        print("Sem assinantes para montar coortes.")
        return
    maxk = int(args.meses) if args.meses else 6
    # agrupa por mês de entrada
    coortes = {}
    for a in ass:
        ini = a.get("inicio", "")
        if ini:
            coortes.setdefault(ini, []).append(a)
    print(f"👥 Coortes de retenção (quantos % da turma que entrou continuam pagando)")
    print(f"    linha = mês de entrada · coluna = meses depois · {cfg['negocio'] or ''}")
    header = "  entrada   tam " + "".join(f"  m{k:<2}" for k in range(0, maxk + 1))
    print(header)
    print("-" * len(header))
    for ini in sorted(coortes):
        turma = coortes[ini]
        tam = len(turma)
        row = f"  {ini}  {tam:>3} "
        for k in range(0, maxk + 1):
            mes_k = mes_add(ini, k)
            # ativos da turma nesse mês
            vivos = 0
            for a in turma:
                fim = a.get("fim", "")
                if a.get("status") == "cancelado" and fim and fim <= mes_k:
                    continue
                vivos += 1
            row += f"  {int(round(100*vivos/tam)):>3}"
        print(row)
    print("-" * len(header))
    print("  Leia da esquerda pra direita: onde o número DESABA é onde as pessoas desistem.")

def _churn_mensal_medio(ms):
    """Média das taxas de churn de receita BRUTO dos meses com base > 0 (para LTV/forecast)."""
    taxas = []
    for mes in ms:
        ini = mrr_ate(mes_add(mes, -1))
        if ini > 0:
            taxas.append(movimento_do_mes(mes)["churn"] / ini)
    return sum(taxas) / len(taxas) if taxas else 0.0

def cmd_ltv(args):
    """LTV, LTV:CAC e payback de CAC — quanto vale um cliente e em quanto tempo ele se paga."""
    garantir_casa()
    cfg = ler_config()
    ms = meses_com_dados()
    if not ms:
        print("Ainda não há dados para calcular o valor do cliente.")
        return
    ref = ms[-1]
    ativos = ativos_em(ref)
    n = len(ativos)
    mrr = mrr_ativos_em(ref)
    if n == 0 or mrr <= 0:
        print("Sem base ativa para calcular ARPU/LTV.")
        return
    arpu = mrr / n
    margem = num(args.margem) / 100 if args.margem is not None else (cfg["margem"] / 100 if cfg["margem"] is not None else None)
    cac = num(args.cac) if args.cac is not None else cfg["cac"]
    churn = num(args.churn) / 100 if args.churn is not None else _churn_mensal_medio(ms)
    print(f"💠 Valor do cliente — {cfg['negocio'] or 'seu negócio'} (competência {ref})")
    print(f"  Ticket médio recorrente (ARPU): {money(arpu,cfg)}/mês  ({n} assinantes ativos)")
    if margem is None:
        print("  Margem bruta: [A CONFERIR] — quanto sobra de cada real depois do custo de entregar? "
              "Passe --margem 70 (em %) ou defina no config para calcular o LTV.")
        return
    print(f"  Margem bruta usada: {pct(margem)}")
    if churn <= 0:
        print("  Churn mensal: 0% no histórico (ou base nova). Sem churn > 0 não dá pra estimar por "
              "quanto tempo o cliente fica — registre alguns meses ou passe --churn (em %).")
        return
    vida = 1 / churn
    ltv = arpu * margem * vida
    print(f"  Churn mensal médio: {pct(churn)}  →  vida média ≈ {vida:.1f} meses")
    print(f"  LTV (lucro que o cliente deixa enquanto fica): {money(ltv,cfg)}")
    print(f"     conta: ticket {money(arpu,cfg)} × margem {pct(margem)} × {vida:.1f} meses")
    if cac is not None and cac > 0:
        ratio = ltv / cac
        payback = cac / (arpu * margem)
        sinal_r = "🟢 saudável (≥3×)" if ratio >= 3 else ("🟡 apertado (1–3×)" if ratio >= 1 else "🔴 no prejuízo (<1×)")
        sinal_p = "🟢" if payback < 12 else ("🟡" if payback <= 18 else "🔴")
        print(f"  Custo pra adquirir (CAC): {money(cac,cfg)}")
        print(f"  LTV : CAC = {ratio:.1f}×   {sinal_r}")
        print(f"  Payback do CAC (meses pra recuperar o gasto): {payback:.1f}   {sinal_p} "
              f"(abaixo de 12 é saudável, acima de 18 aperta o caixa)")
    else:
        print("  CAC: [A CONFERIR] — quanto você gasta em média pra trazer 1 cliente? "
              "Passe --cac ou defina no config para ver LTV:CAC e payback.")

def cmd_prever(args):
    """Forecast da base recorrente com premissas EXPLÍCITAS (nunca número mágico)."""
    garantir_casa()
    cfg = ler_config()
    ms = meses_com_dados()
    if not ms:
        print("Ainda não há histórico para projetar.")
        return
    ref = ms[-1]
    mrr = mrr_ate(ref)
    n_meses = int(args.meses) if args.meses else 12
    # premissas: adições médias em R$ (novo+expansão+reativação) e taxa de churn de receita
    ultimos = ms[-3:] if len(ms) >= 3 else ms
    if args.adicoes is not None:
        adic = num(args.adicoes)
    else:
        vals = []
        for mes in ultimos:
            mv = movimento_do_mes(mes)
            vals.append(mv["novo"] + mv["expansao"] + mv["reativacao"])
        adic = sum(vals) / len(vals) if vals else 0.0
    churn = num(args.churn) / 100 if args.churn is not None else _churn_mensal_medio(ultimos)
    print(f"🔮 Previsão da receita recorrente — {cfg['negocio'] or 'seu negócio'}")
    print(f"  Ponto de partida (MRR em {ref}): {money(mrr,cfg)}")
    print(f"  Premissas (edite com --adicoes e --churn):")
    print(f"    • Entram por mês (novo+expansão+reativação): {money(adic,cfg)}  "
          f"[média dos últimos {len(ultimos)} meses]")
    print(f"    • Churn de receita por mês: {pct(churn)}")
    print("-" * 52)
    base = mrr
    marcos = {3, 6, 12, n_meses}
    for k in range(1, n_meses + 1):
        base = base * (1 - churn) + adic
        if k in marcos:
            print(f"  Em {mes_add(ref,k)} ({k:>2} meses): {money(base,cfg)}   ({sinal_crescimento((base-mrr)/mrr if mrr else 0)})")
    print("-" * 52)
    # cenário "se parar de vender novo": só o churn corrói a base (meia-vida)
    if churn > 0:
        import math
        meia_vida = math.log(2) / (-math.log(1 - churn)) if churn < 1 else 0
        print(f"  🧪 Se você PARAR de vender/expandir hoje, só o churn agindo, a base cai à METADE "
              f"em ≈ {meia_vida:.1f} meses. É o teste de previsibilidade: quanto mais lento esse "
              f"derretimento, mais sólida é a sua recorrência.")
    else:
        print("  🧪 Sem churn no histórico, a base não derrete sozinha — mas confirme com mais meses de dados.")
    print("  ⚠️  Projeção é estimativa: vale enquanto as premissas se mantiverem. A conta é da IA; "
          "a decisão é sua.")

def cmd_extrato(args):
    garantir_casa()
    cfg = ler_config()
    movs = ler_movs()
    if not movs:
        print("Livro-razão vazio.")
        return
    if args.mes:
        alvo = mes_iso(args.mes)
        movs = [m for m in movs if m["mes"] == alvo]
    idx = {a["id"]: a["nome"] for a in ler_assinantes()}
    print(f"{'Mês':<8} {'Tipo':<11} {'Assinante':<22} {'Δ MRR':>12}  Obs")
    print("-" * 66)
    for m in sorted(movs, key=lambda x: (x["mes"], x["tipo"])):
        d = SINAL.get(m["tipo"], 0) * num(m["valor_mrr"])
        nome = idx.get(str(m["assinante_id"]), f"#{m['assinante_id']}")
        print(f"{m['mes']:<8} {m['tipo']:<11} {nome[:22]:<22} {money(d,cfg):>12}  {m.get('obs','')}")

def cmd_importar(args):
    """Importa uma planilha de assinantes (cabeçalho acento-insensível: nome, plano, valor, ciclo, inicio)."""
    garantir_casa()
    cfg = ler_config()
    caminho = args.arquivo
    if not caminho or not os.path.exists(caminho):
        print(f"⚠️  Arquivo não encontrado: {caminho}")
        return
    with open(caminho, newline="", encoding="utf-8-sig") as f:
        # detecta separador simples
        amostra = f.readline(); f.seek(0)
        sep = ";" if amostra.count(";") > amostra.count(",") else ","
        rows = list(csv.DictReader(f, delimiter=sep))
    if not rows:
        print("Planilha vazia.")
        return
    def campo(r, *alvos):
        for k, v in r.items():
            if sem_acento(k) in alvos:
                return v
        return ""
    n = 0
    for r in rows:
        nome = campo(r, "nome", "cliente", "assinante")
        valor = campo(r, "valor", "preco", "mensalidade", "valor mensal", "valormensal")
        if not nome or num(valor) <= 0:
            continue
        ciclo = norm_ciclo(campo(r, "ciclo", "periodicidade") or "mensal")
        inicio = mes_iso(campo(r, "inicio", "entrada", "desde") or None)
        plano = campo(r, "plano", "tier")
        mrr = mrr_de(valor, ciclo)
        aid = proximo_id()
        ass = ler_assinantes()
        ass.append({"id": str(aid), "nome": nome, "plano": plano, "valor": f"{num(valor)}",
                    "ciclo": ciclo, "mrr": f"{mrr}", "inicio": inicio, "status": "ativo",
                    "fim": "", "criado": date.today().isoformat()})
        salvar_assinantes(ass)
        registrar_mov(inicio, aid, "novo", mrr, obs=plano)
        n += 1
    print(f"✅ Importados {n} assinantes recorrentes. Confira com 'base'. "
          f"Lembre: só importe o que se REPETE — venda avulsa não é MRR.")

def cmd_painel(args):
    garantir_casa()
    cfg = ler_config()
    ms = meses_com_dados()
    if not ms:
        print("Painel vazio — cadastre seus assinantes recorrentes com 'novo' para começar.")
        return
    ref = ms[-1]
    ativos = ativos_em(ref)
    mrr = mrr_ativos_em(ref)
    mv = movimento_do_mes(ref)
    net = round(mv["novo"] + mv["expansao"] + mv["reativacao"] - mv["contracao"] - mv["churn"], 2)
    mrr_ini = mrr_ate(mes_add(ref, -1))
    print(f"📊 Painel da Cadência — {cfg['negocio'] or 'seu negócio'}  (competência {ref})")
    print("=" * 56)
    print(f"  MRR (receita recorrente do mês) . {money(mrr,cfg):>18}")
    print(f"  ARR (×12) ....................... {money(mrr*12,cfg):>18}")
    print(f"  Assinantes ativos ............... {len(ativos):>18}")
    print(f"  Net-new do mês .................. {(('+' if net>=0 else '')+money(net,cfg)):>18}   {sinal_crescimento(net/mrr_ini if mrr_ini else net)}")
    if mrr_ini > 0:
        grr = (mrr_ini - mv["churn"] - mv["contracao"]) / mrr_ini
        nrr = (mrr_ini - mv["churn"] - mv["contracao"] + mv["expansao"]) / mrr_ini
        print(f"  Churn de receita (mês) .......... {pct(mv['churn']/mrr_ini):>18}")
        print(f"  NRR / GRR ....................... {(pct(nrr)+' / '+pct(grr)):>18}")
    entra, sai = mv["novo"]+mv["expansao"]+mv["reativacao"], mv["churn"]+mv["contracao"]
    if sai > 0:
        print(f"  Quick ratio ..................... {f'{entra/sai:.1f}×':>18}")
    print("=" * 56)
    print("  Detalhes: 'ponte' (movimento do mês), 'ltv' (valor do cliente), 'prever' (projeção).")

def cmd_plano(args):
    """Plano de ação do mês, ordenado por risco."""
    garantir_casa()
    cfg = ler_config()
    ms = meses_com_dados()
    if not ms:
        print("Sem dados para montar o plano. Cadastre a base com 'novo'.")
        return
    ref = ms[-1]
    mrr_ini = mrr_ate(mes_add(ref, -1))
    mv = movimento_do_mes(ref)
    acoes = []
    # 1) churn de receita alto
    if mrr_ini > 0 and mv["churn"] / mrr_ini > 0.05:
        acoes.append(("🔴", f"Churn de receita de {pct(mv['churn']/mrr_ini)} neste mês — acima de 5%. "
                            "Ligue para quem cancelou e ataque a causa raiz (veja 'churn-taxa')."))
    # 2) NRR baixo
    if mrr_ini > 0:
        nrr = (mrr_ini - mv["churn"] - mv["contracao"] + mv["expansao"]) / mrr_ini
        if nrr < 0.9:
            acoes.append(("🟠", f"NRR em {pct(nrr)} (<90%): a base atual vaza. Crie um caminho de "
                                "upgrade (expansão) para os clientes bons (veja 'retencao')."))
    # 3) net-new negativo
    net = mv["novo"] + mv["expansao"] + mv["reativacao"] - mv["contracao"] - mv["churn"]
    if net < 0:
        acoes.append(("🔴", f"A base ENCOLHEU {money(net,cfg)} no mês: saiu mais do que entrou. "
                            "Priorize reter antes de gastar em aquisição (veja 'ponte')."))
    # 4) sem expansão nenhuma
    if mv["expansao"] == 0 and len(ativos_em(ref)) >= 3:
        acoes.append(("🟡", "Zero expansão no mês: ninguém subiu de plano. Desenhe faixas "
                            "good-better-best para abrir caminho de upgrade (veja references/desenhar_planos.md)."))
    # 5) margem/CAC não configurados
    if cfg["margem"] is None:
        acoes.append(("🟡", "Margem bruta não definida — sem ela não dá pra saber quanto um cliente "
                            "vale (LTV). Defina no config ou passe --margem no comando 'ltv'."))
    print(f"🧭 Plano da Cadência — {cfg['negocio'] or 'seu negócio'}  (competência {ref})")
    if not acoes:
        print("  🟢 Nenhum alerta estrutural este mês. Base saudável — foque em crescer a cadência "
              "de aquisição e a expansão dos clientes atuais.")
        return
    ordem = {"🔴": 0, "🟠": 1, "🟡": 2}
    for i, (sev, txt) in enumerate(sorted(acoes, key=lambda x: ordem.get(x[0], 3)), 1):
        print(f"  {i}. {sev} {txt}")

def cmd_ajuda(args):
    print("""Cadência — motor de receita recorrente (MRR). Comandos:

  BASE
    novo --nome N --valor V [--plano P] [--ciclo mensal|trimestral|anual] [--mes AAAA-MM]
    base                          lista assinantes ativos + MRR/ARR
    importar --arquivo x.csv      importa planilha (cabeçalho: nome, plano, valor, ciclo, inicio)
    extrato [--mes AAAA-MM]       o livro-razão dos movimentos

  MOVIMENTO (o motor deriva o MRR do livro — a identidade fecha por construção)
    expansao  --id N (--novo-valor V | --delta D) [--mes]   upgrade
    contracao --id N (--novo-valor V | --delta D) [--mes]   downgrade
    churn     --id N [--motivo "..."] [--mes]               cancelamento
    reativacao --id N [--valor V] [--mes]                   voltou

  LEITURA
    ponte [--mes]                 a PONTE do MRR: início+novo+exp−contr−churn+reat=fim
    churn-taxa [--mes]            churn de LOGO (clientes) e de RECEITA (reais)
    retencao [--mes]              GRR e NRR do mês
    coorte [--meses 6]            matriz de retenção por mês de entrada
    ltv [--margem % --cac V --churn %]   valor do cliente: LTV, LTV:CAC, payback
    prever [--meses 12 --adicoes V --churn %]   forecast da base recorrente
    painel                        raio-x geral
    plano                         ações do mês ordenadas por risco

  Regras: nunca inventa número; só o que se REPETE vira MRR; dados 100% locais; a IA calcula, o dono decide.
""")

# --------------------------------------------------------------------------- #
# CLI                                                                          #
# --------------------------------------------------------------------------- #

def build_parser():
    p = argparse.ArgumentParser(prog="cadencia", add_help=True,
                                description="Motor de receita recorrente (MRR) — offline, stdlib.")
    sub = p.add_subparsers(dest="cmd")

    sub.add_parser("init")
    sub.add_parser("ajuda")
    sub.add_parser("base")
    sub.add_parser("painel")
    sub.add_parser("plano")

    sp = sub.add_parser("novo")
    sp.add_argument("--nome"); sp.add_argument("--valor"); sp.add_argument("--plano")
    sp.add_argument("--ciclo"); sp.add_argument("--mes")

    for nome in ("expansao", "contracao"):
        sp = sub.add_parser(nome)
        sp.add_argument("--id", required=True)
        sp.add_argument("--novo-valor", dest="novo_valor")
        sp.add_argument("--delta")
        sp.add_argument("--mes")

    sp = sub.add_parser("churn")
    sp.add_argument("--id", required=True); sp.add_argument("--motivo"); sp.add_argument("--mes")

    sp = sub.add_parser("reativacao")
    sp.add_argument("--id", required=True); sp.add_argument("--valor"); sp.add_argument("--mes")

    for nome in ("ponte", "churn-taxa", "retencao"):
        sp = sub.add_parser(nome)
        sp.add_argument("--mes")

    sp = sub.add_parser("coorte"); sp.add_argument("--meses")

    sp = sub.add_parser("ltv")
    sp.add_argument("--margem"); sp.add_argument("--cac"); sp.add_argument("--churn")

    sp = sub.add_parser("prever")
    sp.add_argument("--meses"); sp.add_argument("--adicoes"); sp.add_argument("--churn")

    sp = sub.add_parser("extrato"); sp.add_argument("--mes")
    sp = sub.add_parser("importar"); sp.add_argument("--arquivo")
    return p

DISPATCH = {
    "init": cmd_init, "ajuda": cmd_ajuda, "base": cmd_base, "painel": cmd_painel, "plano": cmd_plano,
    "novo": cmd_novo, "expansao": cmd_expansao, "contracao": cmd_contracao, "churn": cmd_churn,
    "reativacao": cmd_reativacao, "ponte": cmd_ponte, "churn-taxa": cmd_churn_taxa,
    "retencao": cmd_retencao, "coorte": cmd_coorte, "ltv": cmd_ltv, "prever": cmd_prever,
    "extrato": cmd_extrato, "importar": cmd_importar,
}

def main():
    parser = build_parser()
    args = parser.parse_args()
    if not args.cmd:
        cmd_ajuda(args)
        return
    DISPATCH[args.cmd](args)

if __name__ == "__main__":
    main()
