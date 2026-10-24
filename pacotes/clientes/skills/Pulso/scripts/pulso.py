#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Pulso — motor de medição de satisfação do cliente (NPS / CSAT / CES).

Lê o livro de respostas em .pulso/respostas.csv e devolve, em português
simples, a nota da base, a tendência, a fila de detratores para recuperar,
a lista de promotores e os temas que mais aparecem na voz do cliente.
Usa SOMENTE a biblioteca padrão do Python. Nunca inventa número: tudo que
sai daqui veio das respostas registradas pelo usuário.

Formato do CSV (.pulso/respostas.csv), com cabeçalho:
    data,cliente,canal,tipo,nota,comentario
    2026-05-03,Maria Silva,whatsapp,nps,9,Atendimento rápido e gente boa
    2026-05-04,João Souza,email,csat,2,Demorou demais pra responder
    2026-05-05,,formulario,ces,6,Foi fácil resolver

  - data: YYYY-MM-DD ou DD/MM/YYYY
  - cliente: opcional
  - canal: opcional (whatsapp, email, formulario, telefone, presencial...)
  - tipo: nps (0-10) | csat (1-5) | ces (1-7)
  - nota: número inteiro dentro da escala do tipo
  - comentario: opcional (a resposta aberta / voz do cliente)

Escalas:
  - NPS  0-10 → Promotor 9-10 | Neutro 7-8 | Detrator 0-6. Nota = %prom − %detr.
  - CSAT 1-5  → Satisfeito 4-5 (top-2-box). Nota = % de satisfeitos.
  - CES  1-7  → 7 = muito fácil. Nota = média (quanto maior, menos esforço).

Comandos:
    python3 pulso.py resumo                     # panorama geral (semáforo)
    python3 pulso.py nps                        # NPS + faixas + tendência
    python3 pulso.py csat                       # % de satisfeitos
    python3 pulso.py ces                        # esforço médio
    python3 pulso.py tendencia --tipo nps --meses 6
    python3 pulso.py detratores                 # fila de recuperação
    python3 pulso.py promotores                 # candidatos a prova social
    python3 pulso.py temas                      # voz do cliente por tema
    python3 pulso.py alertas                    # o que merece atenção agora
Opções globais: --arquivo <csv>  (padrão: .pulso/respostas.csv)
                --desde YYYY-MM  --ate YYYY-MM  (recorte de período)
                --formato json   (padrão: texto)
"""

import argparse
import csv
import json
import os
import re
import sys
import unicodedata
from collections import defaultdict, Counter
from datetime import date

ARQUIVO_PADRAO = os.path.join(".pulso", "respostas.csv")
TEMAS_PADRAO_ARQ = os.path.join(".pulso", "temas.md")

# Dicionário-semente de temas da voz do cliente (palavra-chave → tema).
# Sobreponível por .pulso/temas.md (uma linha "Tema: kw1, kw2, ...").
DEFAULT_TEMAS = {
    "Atendimento": ["atendimento", "atencao", "educacao", "simpatia", "grosseria",
                    "mal atendido", "atendente", "recepcao", "cordial"],
    "Prazo/Entrega": ["prazo", "demora", "demorou", "atraso", "atrasou", "rapido",
                      "rapidez", "lento", "entrega", "esperar", "espera", "fila"],
    "Preço": ["preco", "caro", "barato", "valor", "custo", "cobranca", "cobrar",
              "cobrou", "reajuste", "mensalidade", "taxa"],
    "Qualidade": ["qualidade", "ruim", "otimo", "excelente", "perfeito", "defeito",
                  "quebrou", "estragou", "acabamento", "capricho"],
    "Produto/Recurso": ["produto", "recurso", "funcionalidade", "funcao", "faltou",
                        "faltando", "poderia ter", "sentindo falta", "opcao"],
    "Suporte/Técnico": ["suporte", "bug", "erro", "travou", "nao funciona", "problema tecnico",
                        "sistema", "app", "site", "instalar", "configurar"],
    "Comunicação": ["comunicacao", "informacao", "aviso", "retorno", "resposta",
                    "nao respondeu", "sumiu", "ninguem respondeu", "contato"],
    "Experiência/Facilidade": ["facil", "dificil", "complicado", "confuso", "intuitivo",
                              "simples", "esforco", "trabalhoso", "burocracia"],
}


# ---------------------------------------------------------------- utilidades

def _norm(s):
    """minúsculas e sem acento, para comparação tolerante."""
    s = unicodedata.normalize("NFD", (s or "").strip().lower())
    return "".join(c for c in s if unicodedata.category(c) != "Mn")


def parse_data(bruto):
    """'YYYY-MM-DD' ou 'DD/MM/YYYY' → date. None se inválido."""
    s = (bruto or "").strip()
    if not s:
        return None
    for fmt in ("%Y-%m-%d", "%d/%m/%Y", "%Y/%m/%d", "%d-%m-%Y"):
        try:
            from datetime import datetime
            return datetime.strptime(s, fmt).date()
        except ValueError:
            continue
    return None


def parse_nota(bruto):
    """Converte a nota em inteiro. None se vazio/inválido."""
    s = (bruto or "").strip().replace(",", ".")
    if not s:
        return None
    try:
        return int(round(float(s)))
    except ValueError:
        return None


ESCALAS = {
    "nps": (0, 10),
    "csat": (1, 5),
    "ces": (1, 7),
}


def classifica_nps(n):
    if n >= 9:
        return "promotor"
    if n >= 7:
        return "neutro"
    return "detrator"


def classifica_csat(n):
    if n >= 4:
        return "satisfeito"
    if n == 3:
        return "neutro"
    return "insatisfeito"


# ---------------------------------------------------------------- carregar

def carregar(arquivo, desde=None, ate=None):
    """Lê o CSV e devolve lista de dicts normalizados, filtrada por período."""
    if not os.path.exists(arquivo):
        erro(f"Não encontrei o livro de respostas em '{arquivo}'. "
             f"Rode a primeira conversa (setup) para criá-lo.")
    linhas = []
    problemas = []
    with open(arquivo, newline="", encoding="utf-8-sig") as f:
        leitor = csv.DictReader(f)
        campos = {(_norm(c)): c for c in (leitor.fieldnames or [])}
        req = ["data", "tipo", "nota"]
        faltando = [c for c in req if c not in campos]
        if faltando:
            erro(f"O CSV precisa das colunas {req}. Faltando: {faltando}.")
        for i, row in enumerate(leitor, start=2):
            def g(nome):
                col = campos.get(nome)
                return row.get(col, "") if col else ""
            # pula linhas de comentário/modelo (primeira célula começa com '#')
            primeira = (g("data") or "").strip()
            if primeira.startswith("#"):
                continue
            tipo = _norm(g("tipo"))
            if tipo not in ESCALAS:
                if any(v.strip() for v in row.values()):
                    problemas.append(f"linha {i}: tipo '{g('tipo')}' desconhecido (use nps/csat/ces)")
                continue
            nota = parse_nota(g("nota"))
            lo, hi = ESCALAS[tipo]
            if nota is None or not (lo <= nota <= hi):
                problemas.append(f"linha {i}: nota '{g('nota')}' fora da escala {tipo} ({lo}-{hi})")
                continue
            d = parse_data(g("data"))
            if desde and (not d or d.strftime("%Y-%m") < desde):
                continue
            if ate and (not d or d.strftime("%Y-%m") > ate):
                continue
            linhas.append({
                "data": d,
                "cliente": g("cliente").strip(),
                "canal": g("canal").strip(),
                "tipo": tipo,
                "nota": nota,
                "comentario": g("comentario").strip(),
            })
    return linhas, problemas


def carregar_temas():
    """Carrega o dicionário de temas de .pulso/temas.md, ou usa o padrão."""
    if not os.path.exists(TEMAS_PADRAO_ARQ):
        return {t: [_norm(k) for k in kws] for t, kws in DEFAULT_TEMAS.items()}
    temas = {}
    with open(TEMAS_PADRAO_ARQ, encoding="utf-8") as f:
        for ln in f:
            ln = ln.strip()
            if not ln or ln.startswith("#") or ":" not in ln:
                continue
            nome, kws = ln.split(":", 1)
            palavras = [_norm(k) for k in kws.split(",") if k.strip()]
            if palavras:
                temas[nome.strip()] = palavras
    return temas or {t: [_norm(k) for k in kws] for t, kws in DEFAULT_TEMAS.items()}


def erro(msg):
    print(f"ERRO: {msg}", file=sys.stderr)
    sys.exit(1)


# ---------------------------------------------------------------- cálculos

def calc_nps(linhas):
    r = [x for x in linhas if x["tipo"] == "nps"]
    total = len(r)
    if not total:
        return None
    prom = sum(1 for x in r if x["nota"] >= 9)
    neu = sum(1 for x in r if 7 <= x["nota"] <= 8)
    det = sum(1 for x in r if x["nota"] <= 6)
    p_prom = prom / total * 100
    p_det = det / total * 100
    return {
        "total": total, "promotores": prom, "neutros": neu, "detratores": det,
        "pct_promotores": round(p_prom, 1), "pct_neutros": round(neu / total * 100, 1),
        "pct_detratores": round(p_det, 1), "nps": round(p_prom - p_det),
    }


def calc_csat(linhas):
    r = [x for x in linhas if x["tipo"] == "csat"]
    total = len(r)
    if not total:
        return None
    satisfeitos = sum(1 for x in r if x["nota"] >= 4)
    neutros = sum(1 for x in r if x["nota"] == 3)
    insatisfeitos = sum(1 for x in r if x["nota"] <= 2)
    media = sum(x["nota"] for x in r) / total
    return {
        "total": total, "satisfeitos": satisfeitos, "neutros": neutros,
        "insatisfeitos": insatisfeitos, "csat": round(satisfeitos / total * 100, 1),
        "media": round(media, 2),
    }


def calc_ces(linhas):
    r = [x for x in linhas if x["tipo"] == "ces"]
    total = len(r)
    if not total:
        return None
    media = sum(x["nota"] for x in r) / total
    faceis = sum(1 for x in r if x["nota"] >= 6)   # 6-7 = fácil
    dificeis = sum(1 for x in r if x["nota"] <= 3)  # 1-3 = difícil/esforço alto
    return {
        "total": total, "media": round(media, 2),
        "faceis": faceis, "dificeis": dificeis,
        "pct_faceis": round(faceis / total * 100, 1),
        "pct_dificeis": round(dificeis / total * 100, 1),
    }


def eh_detrator(x):
    """Um detrator é qualquer resposta claramente insatisfeita, em qualquer escala."""
    return (x["tipo"] == "nps" and x["nota"] <= 6) or \
           (x["tipo"] == "csat" and x["nota"] <= 2) or \
           (x["tipo"] == "ces" and x["nota"] <= 3)


def conta_detratores(linhas):
    return sum(1 for x in linhas if eh_detrator(x))


def por_mes(linhas, tipo):
    """Agrupa por mês (YYYY-MM) e calcula a nota daquele tipo em cada um."""
    grupos = defaultdict(list)
    for x in linhas:
        if x["tipo"] != tipo or not x["data"]:
            continue
        grupos[x["data"].strftime("%Y-%m")].append(x)
    saida = []
    for mes in sorted(grupos):
        g = grupos[mes]
        if tipo == "nps":
            c = calc_nps(g)
            nota = c["nps"] if c else None
        elif tipo == "csat":
            c = calc_csat(g)
            nota = c["csat"] if c else None
        else:
            c = calc_ces(g)
            nota = c["media"] if c else None
        saida.append({"mes": mes, "nota": nota, "respostas": len(g)})
    return saida


def temas_dos_comentarios(linhas, temas):
    """Conta ocorrências de cada tema e a nota média associada a ele."""
    contagem = Counter()
    notas = defaultdict(list)
    exemplos = defaultdict(list)
    sem_tema = 0
    com_comentario = 0
    for x in linhas:
        com = _norm(x["comentario"])
        if not com:
            continue
        com_comentario += 1
        achou = False
        for tema, kws in temas.items():
            if any(k in com for k in kws):
                contagem[tema] += 1
                notas[tema].append((x["tipo"], x["nota"]))
                if len(exemplos[tema]) < 3 and x["comentario"]:
                    exemplos[tema].append(x["comentario"][:140])
                achou = True
        if not achou:
            sem_tema += 1
    resultado = []
    for tema, n in contagem.most_common():
        # sinal de dor: fração de notas "baixas" (detrator nps / insatisf csat / difícil ces)
        baixas = 0
        for tp, nota in notas[tema]:
            if tp == "nps" and nota <= 6:
                baixas += 1
            elif tp == "csat" and nota <= 2:
                baixas += 1
            elif tp == "ces" and nota <= 3:
                baixas += 1
        resultado.append({
            "tema": tema, "mencoes": n,
            "pct_negativas": round(baixas / len(notas[tema]) * 100, 1) if notas[tema] else 0.0,
            "exemplos": exemplos[tema],
        })
    return {
        "com_comentario": com_comentario, "sem_tema": sem_tema,
        "temas": resultado,
    }


# ---------------------------------------------------------------- saída texto

def selo(nps):
    if nps is None:
        return "—"
    if nps >= 50:
        return "🟢 excelente"
    if nps >= 0:
        return "🟡 na média"
    return "🔴 crítico"


def selo_csat(pct):
    if pct is None:
        return "—"
    if pct >= 80:
        return "🟢 forte"
    if pct >= 60:
        return "🟡 ok"
    return "🔴 fraco"


def seta_tendencia(serie):
    vals = [p["nota"] for p in serie if p["nota"] is not None]
    if len(vals) < 2:
        return "sem histórico suficiente"
    delta = vals[-1] - vals[-2]
    if delta > 0.5:
        return f"↗ subindo (+{round(delta,1)} vs mês anterior)"
    if delta < -0.5:
        return f"↘ caindo ({round(delta,1)} vs mês anterior)"
    return "→ estável vs mês anterior"


def cmd_resumo(linhas, temas, fmt):
    nps = calc_nps(linhas)
    csat = calc_csat(linhas)
    ces = calc_ces(linhas)
    serie_nps = por_mes(linhas, "nps")
    dados = {
        "total_respostas": len(linhas),
        "nps": nps, "csat": csat, "ces": ces,
        "tendencia_nps": seta_tendencia(serie_nps) if nps else None,
    }
    if fmt == "json":
        return dados
    L = []
    L.append(f"PULSO DA BASE — {len(linhas)} respostas registradas")
    L.append("")
    if nps:
        L.append(f"NPS: {nps['nps']:+d}  {selo(nps['nps'])}   ({nps['total']} respostas)")
        L.append(f"   promotores {nps['pct_promotores']}% · neutros {nps['pct_neutros']}% · detratores {nps['pct_detratores']}%")
        L.append(f"   tendência: {dados['tendencia_nps']}")
    else:
        L.append("NPS: sem respostas do tipo 'nps' ainda.")
    if csat:
        L.append(f"CSAT: {csat['csat']}% satisfeitos  {selo_csat(csat['csat'])}   (média {csat['media']}/5, {csat['total']} respostas)")
    if ces:
        L.append(f"CES: esforço médio {ces['media']}/7  ({ces['pct_faceis']}% acharam fácil, {ces['pct_dificeis']}% acharam difícil)")
    ndet = conta_detratores(linhas)
    if ndet:
        L.append("")
        L.append(f"⚠ {ndet} detrator(es) esperando recuperação — rode: detratores")
    return "\n".join(L)


def cmd_nps(linhas, fmt):
    c = calc_nps(linhas)
    if not c:
        return "Sem respostas do tipo 'nps' no período." if fmt != "json" else {"nps": None}
    serie = por_mes(linhas, "nps")
    if fmt == "json":
        return {"resumo": c, "por_mes": serie}
    L = [f"NPS: {c['nps']:+d}  {selo(c['nps'])}",
         f"Base: {c['total']} respostas",
         f"  🟢 promotores (9-10): {c['promotores']}  ({c['pct_promotores']}%)",
         f"  🟡 neutros    (7-8):  {c['neutros']}  ({c['pct_neutros']}%)",
         f"  🔴 detratores (0-6):  {c['detratores']}  ({c['pct_detratores']}%)",
         "", f"Tendência: {seta_tendencia(serie)}"]
    return "\n".join(L)


def cmd_csat(linhas, fmt):
    c = calc_csat(linhas)
    if not c:
        return "Sem respostas do tipo 'csat' no período." if fmt != "json" else {"csat": None}
    if fmt == "json":
        return c
    return (f"CSAT: {c['csat']}% satisfeitos  {selo_csat(c['csat'])}\n"
            f"Base: {c['total']} respostas (média {c['media']}/5)\n"
            f"  satisfeitos (4-5): {c['satisfeitos']}\n"
            f"  neutros (3):       {c['neutros']}\n"
            f"  insatisfeitos(1-2):{c['insatisfeitos']}")


def cmd_ces(linhas, fmt):
    c = calc_ces(linhas)
    if not c:
        return "Sem respostas do tipo 'ces' no período." if fmt != "json" else {"ces": None}
    if fmt == "json":
        return c
    return (f"CES: esforço médio {c['media']}/7 (7 = muito fácil)\n"
            f"Base: {c['total']} respostas\n"
            f"  acharam fácil (6-7):  {c['faceis']} ({c['pct_faceis']}%)\n"
            f"  acharam difícil(1-3): {c['dificeis']} ({c['pct_dificeis']}%)")


def cmd_tendencia(linhas, tipo, meses, fmt):
    serie = por_mes(linhas, tipo)
    if meses:
        serie = serie[-meses:]
    if fmt == "json":
        return {"tipo": tipo, "serie": serie}
    if not serie:
        return f"Sem histórico do tipo '{tipo}'."
    unidade = "" if tipo == "ces" else ("%" if tipo == "csat" else "")
    L = [f"TENDÊNCIA — {tipo.upper()} (últimos {len(serie)} meses)"]
    for p in serie:
        nota = p["nota"]
        barra = ""
        if nota is not None:
            if tipo == "nps":
                barra = "█" * max(0, int((nota + 100) / 10))
            elif tipo == "csat":
                barra = "█" * int(nota / 5)
            else:
                barra = "█" * int(nota * 3)
        L.append(f"  {p['mes']}: {str(nota).rjust(5)}{unidade}  {barra}  ({p['respostas']} resp.)")
    L.append("")
    L.append(seta_tendencia(serie))
    return "\n".join(L)


def cmd_detratores(linhas, fmt):
    det = [x for x in linhas if eh_detrator(x)]
    det.sort(key=lambda x: (x["data"] or date.min), reverse=True)
    if fmt == "json":
        return {"total": len(det), "detratores": [
            {**d, "data": d["data"].isoformat() if d["data"] else None} for d in det]}
    if not det:
        return "Nenhum detrator no período. 🎉"
    L = [f"FILA DE RECUPERAÇÃO — {len(det)} detrator(es)", ""]
    for d in det:
        quando = d["data"].strftime("%d/%m/%Y") if d["data"] else "sem data"
        quem = d["cliente"] or "(cliente não identificado)"
        L.append(f"• {quem} — {d['tipo'].upper()} {d['nota']} — {quando}"
                 + (f" [{d['canal']}]" if d["canal"] else ""))
        if d["comentario"]:
            L.append(f"    “{d['comentario']}”")
    return "\n".join(L)


def cmd_promotores(linhas, fmt):
    prom = [x for x in linhas if
            (x["tipo"] == "nps" and x["nota"] >= 9) or
            (x["tipo"] == "csat" and x["nota"] >= 5)]
    prom.sort(key=lambda x: (x["data"] or date.min), reverse=True)
    if fmt == "json":
        return {"total": len(prom), "promotores": [
            {**p, "data": p["data"].isoformat() if p["data"] else None} for p in prom]}
    if not prom:
        return "Nenhum promotor identificado no período ainda."
    L = [f"PROMOTORES — {len(prom)} candidato(s) a depoimento/indicação", ""]
    for p in prom:
        quem = p["cliente"] or "(cliente não identificado)"
        quando = p["data"].strftime("%d/%m/%Y") if p["data"] else "sem data"
        L.append(f"• {quem} — {p['tipo'].upper()} {p['nota']} — {quando}")
        if p["comentario"]:
            L.append(f"    “{p['comentario']}”")
    return "\n".join(L)


def cmd_temas(linhas, temas, fmt):
    r = temas_dos_comentarios(linhas, temas)
    if fmt == "json":
        return r
    if not r["temas"]:
        return "Ainda não há comentários suficientes para extrair temas."
    L = [f"VOZ DO CLIENTE — {r['com_comentario']} comentário(s) analisado(s)", ""]
    for t in r["temas"]:
        alerta = "  🔴" if t["pct_negativas"] >= 50 else ("  🟡" if t["pct_negativas"] >= 25 else "")
        L.append(f"• {t['tema']}: {t['mencoes']} menção(ões) · {t['pct_negativas']}% negativas{alerta}")
        for ex in t["exemplos"]:
            L.append(f"    “{ex}”")
    if r["sem_tema"]:
        L.append("")
        L.append(f"({r['sem_tema']} comentário(s) não se encaixaram em nenhum tema — "
                 f"leia-os direto ou ajuste .pulso/temas.md)")
    return "\n".join(L)


def cmd_alertas(linhas, temas, fmt):
    alertas = []
    nps = calc_nps(linhas)
    serie = por_mes(linhas, "nps")
    vals = [p["nota"] for p in serie if p["nota"] is not None]
    if nps and nps["nps"] < 0:
        alertas.append(("🔴", f"NPS negativo ({nps['nps']:+d}): há mais detratores que promotores."))
    if len(vals) >= 2 and (vals[-1] - vals[-2]) <= -10:
        alertas.append(("🔴", f"NPS caiu {vals[-2]-vals[-1]} pontos vs o mês anterior."))
    det = conta_detratores(linhas)
    if det:
        alertas.append(("🟡", f"{det} detrator(es) na fila de recuperação (rode: detratores)."))
    r = temas_dos_comentarios(linhas, temas)
    for t in r["temas"]:
        if t["mencoes"] >= 3 and t["pct_negativas"] >= 50:
            alertas.append(("🟡", f"Tema '{t['tema']}' quente: {t['mencoes']} menções, {t['pct_negativas']}% negativas."))
    csat = calc_csat(linhas)
    if csat and csat["csat"] < 60:
        alertas.append(("🔴", f"CSAT baixo ({csat['csat']}% satisfeitos)."))
    if fmt == "json":
        return {"alertas": [{"nivel": n, "texto": t} for n, t in alertas]}
    if not alertas:
        return "Nenhum alerta no momento. A base está saudável. 🟢"
    return "ALERTAS\n" + "\n".join(f"  {n} {t}" for n, t in alertas)


# ---------------------------------------------------------------- CLI

def main():
    p = argparse.ArgumentParser(description="Pulso — medição de satisfação do cliente")
    p.add_argument("comando", choices=["resumo", "nps", "csat", "ces", "tendencia",
                                       "detratores", "promotores", "temas", "alertas"])
    p.add_argument("--arquivo", default=ARQUIVO_PADRAO)
    p.add_argument("--desde", help="mês inicial YYYY-MM")
    p.add_argument("--ate", help="mês final YYYY-MM")
    p.add_argument("--tipo", default="nps", choices=["nps", "csat", "ces"])
    p.add_argument("--meses", type=int, default=0)
    p.add_argument("--formato", default="texto", choices=["texto", "json"])
    a = p.parse_args()

    linhas, problemas = carregar(a.arquivo, a.desde, a.ate)
    temas = carregar_temas()

    if a.comando == "resumo":
        out = cmd_resumo(linhas, temas, a.formato)
    elif a.comando == "nps":
        out = cmd_nps(linhas, a.formato)
    elif a.comando == "csat":
        out = cmd_csat(linhas, a.formato)
    elif a.comando == "ces":
        out = cmd_ces(linhas, a.formato)
    elif a.comando == "tendencia":
        out = cmd_tendencia(linhas, a.tipo, a.meses, a.formato)
    elif a.comando == "detratores":
        out = cmd_detratores(linhas, a.formato)
    elif a.comando == "promotores":
        out = cmd_promotores(linhas, a.formato)
    elif a.comando == "temas":
        out = cmd_temas(linhas, temas, a.formato)
    elif a.comando == "alertas":
        out = cmd_alertas(linhas, temas, a.formato)

    if a.formato == "json":
        payload = out if isinstance(out, dict) else {"resultado": out}
        if problemas:
            payload["_avisos"] = problemas
        print(json.dumps(payload, ensure_ascii=False, indent=2))
    else:
        print(out)
        if problemas:
            print("\n---\nAvisos ao ler o CSV (linhas ignoradas):", file=sys.stderr)
            for pr in problemas:
                print(f"  - {pr}", file=sys.stderr)


if __name__ == "__main__":
    main()
