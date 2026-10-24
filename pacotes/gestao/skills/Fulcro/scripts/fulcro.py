#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Fulcro — copiloto de decisão difícil. 100% local, só stdlib.

O Fulcro não decide por você: ele estrutura a escolha e devolve a caneta.
Faz três coisas que um modelo de texto não faz confiável "de cabeça":

  1. matriz  — matriz de decisão ponderada (critérios com peso × nota de cada
     opção) + teste de sensibilidade (quão robusto é o vencedor: bastaria mudar
     um peso para virar o resultado?).
  2. risco   — ordena os modos de falha de um pré-mortem por Probabilidade ×
     Impacto (L×I), do mais perigoso ao menos, para você agir no que importa.
  3. diario  — guarda cada decisão num diário local (o que você escolheu, o que
     pesou, o que previu) e, na data de revisão, deixa você registrar o que de
     fato aconteceu e CALIBRAR seu julgamento ao longo do tempo.

Nunca acessa a internet, nunca publica nada. Só lê/escreve arquivos locais na
pasta de trabalho do dono (.fulcro/), nunca dentro de .claude/skills/.
"""
import argparse
import datetime
import html
import json
import os
import re
import sys


# --------------------------------------------------------------------------- #
# Onde os dados moram: a pasta de trabalho do dono, NUNCA a pasta da skill.
# --------------------------------------------------------------------------- #
def work_root():
    cwd = os.getcwd()
    marker = os.sep + ".claude" + os.sep + "skills" + os.sep
    if marker in cwd + os.sep:
        return cwd.split(os.sep + ".claude" + os.sep)[0] or cwd
    return cwd


BASE = os.path.join(work_root(), ".fulcro")
CONFIG = os.path.join(BASE, "config.json")
CONFIG_MD = os.path.join(BASE, "config.md")
DIARIO = os.path.join(BASE, "diario.jsonl")
ENTREGAS = os.path.join(work_root(), "deliveries")


def hoje():
    return datetime.date.today()


def hoje_br():
    return hoje().strftime("%d/%m/%Y")


def parse_data(s):
    """Aceita dd/mm/aaaa ou aaaa-mm-dd. Devolve datetime.date ou None."""
    if not s:
        return None
    s = s.strip()
    for fmt in ("%d/%m/%Y", "%Y-%m-%d", "%d-%m-%Y"):
        try:
            return datetime.datetime.strptime(s, fmt).date()
        except ValueError:
            continue
    return None


def slug(txt):
    import unicodedata
    txt = unicodedata.normalize("NFKD", txt or "").encode("ascii", "ignore").decode()
    txt = re.sub(r"[^a-zA-Z0-9]+", "-", txt).strip("-").lower()
    return txt or "decisao"


# --------------------------------------------------------------------------- #
# init / config
# --------------------------------------------------------------------------- #
def esqueleto_config():
    return {
        "config": {"dono": "", "criado_em": hoje_br()},
        "negocio": {"nome": "", "papel": "", "uma_frase": "", "contexto": ""},
        "preferencias": {
            "horizonte_padrao": "6 meses",
            "postura_risco": "",
        },
    }


def carregar_config():
    if os.path.exists(CONFIG):
        try:
            with open(CONFIG, encoding="utf-8") as f:
                return json.load(f)
        except (json.JSONDecodeError, OSError):
            pass
    return esqueleto_config()


def salvar_config(cfg):
    os.makedirs(BASE, exist_ok=True)
    with open(CONFIG, "w", encoding="utf-8") as f:
        json.dump(cfg, f, ensure_ascii=False, indent=2)


def cmd_init(args):
    os.makedirs(BASE, exist_ok=True)
    if not os.path.exists(CONFIG):
        salvar_config(esqueleto_config())
    if not os.path.exists(DIARIO):
        open(DIARIO, "a", encoding="utf-8").close()
    print("OK: .fulcro/ pronto em", BASE)


# --------------------------------------------------------------------------- #
# matriz — matriz de decisão ponderada + sensibilidade
# --------------------------------------------------------------------------- #
# Entrada (JSON), por arquivo (--arquivo) ou stdin:
# {
#   "titulo": "Trocar de sistema de gestão?",
#   "criterios": [
#     {"nome": "Custo total", "peso": 5},
#     {"nome": "Facilidade de migrar", "peso": 3},
#     {"nome": "Suporte", "peso": 4}
#   ],
#   "opcoes": [
#     {"nome": "Ficar no atual", "notas": [4, 5, 2]},
#     {"nome": "Sistema B",      "notas": [3, 2, 5]}
#   ]
# }
# Notas e pesos de 1 a 5. A ordem de "notas" segue a ordem de "criterios".
def _ler_json_entrada(args):
    if getattr(args, "arquivo", None):
        with open(args.arquivo, encoding="utf-8") as f:
            return json.load(f)
    dados = sys.stdin.read()
    return json.loads(dados)


def _validar_matriz(d):
    crit = d.get("criterios") or []
    ops = d.get("opcoes") or []
    if not crit or not ops:
        raise ValueError("Preciso de pelo menos 1 critério e 2 opções.")
    n = len(crit)
    for o in ops:
        notas = o.get("notas") or []
        if len(notas) != n:
            raise ValueError(
                "A opção '%s' tem %d notas, mas há %d critérios."
                % (o.get("nome", "?"), len(notas), n)
            )
    return crit, ops


def _totais(crit, ops):
    pesos = [max(0, float(c.get("peso", 1))) for c in crit]
    soma_pesos = sum(pesos) or 1.0
    linhas = []
    for o in ops:
        notas = [float(x) for x in o["notas"]]
        subtotais = [p * nt for p, nt in zip(pesos, notas)]
        total = sum(subtotais)
        # normaliza para 0-100 (nota máxima possível = 5 * soma_pesos)
        pct = 100.0 * total / (5.0 * soma_pesos)
        linhas.append({
            "nome": o.get("nome", "?"),
            "notas": notas,
            "subtotais": subtotais,
            "total": total,
            "pct": pct,
        })
    linhas.sort(key=lambda x: -x["total"])
    return pesos, linhas


def _sensibilidade(crit, ops, linhas):
    """Quão robusto é o vencedor? Testa: se eu zerar o peso de UM critério,
    o vencedor muda? Reporta os critérios que fazem o ranking virar."""
    if len(linhas) < 2:
        return []
    vencedor = linhas[0]["nome"]
    viram = []
    for i, c in enumerate(crit):
        crit_mod = [dict(x) for x in crit]
        crit_mod[i]["peso"] = 0
        _, linhas_mod = _totais(crit_mod, ops)
        if linhas_mod[0]["nome"] != vencedor:
            viram.append({
                "criterio": c.get("nome", "?"),
                "novo_vencedor": linhas_mod[0]["nome"],
            })
    return viram


def cmd_matriz(args):
    d = _ler_json_entrada(args)
    crit, ops = _validar_matriz(d)
    pesos, linhas = _totais(crit, ops)
    viram = _sensibilidade(crit, ops, linhas)

    print("=" * 60)
    print("MATRIZ DE DECISÃO — " + (d.get("titulo") or "sem título"))
    print("=" * 60)
    print("\nCritérios (peso 1-5):")
    for c, p in zip(crit, pesos):
        print("  • %-28s peso %s" % (c.get("nome", "?"), int(p) if p == int(p) else p))
    print("\nRanking das opções (nota 0-100 = quão bem atende o conjunto):")
    for pos, ln in enumerate(linhas, 1):
        marca = "  <= vencedor" if pos == 1 else ""
        print("  %d. %-26s %5.1f/100  (bruto %.1f)%s"
              % (pos, ln["nome"], ln["pct"], ln["total"], marca))

    # margem entre 1º e 2º
    if len(linhas) >= 2:
        margem = linhas[0]["pct"] - linhas[1]["pct"]
        print("\nMargem 1º sobre 2º: %.1f ponto(s) de 100." % margem)
        if margem < 5:
            print("  ⚠ Empate técnico: a matriz NÃO está decidindo por você. "
                  "Olhe o pré-mortem e o que o seu instinto diz.")

    print("\nTeste de sensibilidade (o vencedor é robusto?):")
    if not viram:
        print("  ✓ Robusto: nenhum critério sozinho, se ignorado, muda o vencedor.")
    else:
        print("  ⚠ Frágil: o vencedor depende destes critérios —")
        for v in viram:
            print("      - se '%s' não contasse, venceria '%s'."
                  % (v["criterio"], v["novo_vencedor"]))
        print("  Confira se o PESO desses critérios reflete mesmo a sua prioridade.")

    print("\nRegra de ouro: a matriz INFORMA, ela não DECIDE. Se o vencedor te dá")
    print("um nó no estômago, isso é dado — provavelmente falta um critério na conta.")


# --------------------------------------------------------------------------- #
# risco — pré-mortem: ordena modos de falha por Probabilidade × Impacto
# --------------------------------------------------------------------------- #
# Entrada (JSON) por arquivo ou stdin:
# {
#   "titulo": "...",
#   "falhas": [
#     {"descricao": "Cliente-âncora não renova", "prob": 4, "impacto": 5,
#      "tipo": "externo",
#      "prevenir": "...", "detectar": "...", "limitar": "..."}
#   ]
# }
# prob e impacto de 1 (raro/leve) a 5 (quase certo/catastrófico).
L_LABEL = {1: "raro", 2: "pouco provável", 3: "possível", 4: "provável", 5: "quase certo"}
I_LABEL = {1: "leve", 2: "menor", 3: "moderado", 4: "grave", 5: "catastrófico"}


def _bucket(score):
    if score >= 16:
        return "CRÍTICO"
    if score >= 9:
        return "ALTO"
    if score >= 4:
        return "MÉDIO"
    return "BAIXO"


def cmd_risco(args):
    d = _ler_json_entrada(args)
    falhas = d.get("falhas") or []
    if not falhas:
        raise ValueError("Preciso de pelo menos 1 modo de falha em 'falhas'.")
    for f in falhas:
        p = int(f.get("prob", 3))
        i = int(f.get("impacto", 3))
        f["_p"] = max(1, min(5, p))
        f["_i"] = max(1, min(5, i))
        f["_score"] = f["_p"] * f["_i"]
        f["_bucket"] = _bucket(f["_score"])
    falhas.sort(key=lambda x: -x["_score"])

    print("=" * 60)
    print("PRÉ-MORTEM — " + (d.get("titulo") or "sem título"))
    print("=" * 60)
    print("Premissa: já deu errado. Estes são os motivos, do mais perigoso ao menos.\n")
    for pos, f in enumerate(falhas, 1):
        tipo = f.get("tipo", "")
        tipo_txt = (" [%s]" % tipo) if tipo else ""
        print("%d. (%s · L×I=%d) %s%s"
              % (pos, f["_bucket"], f["_score"], f.get("descricao", "?"), tipo_txt))
        print("     probabilidade: %s (%d) · impacto: %s (%d)"
              % (L_LABEL[f["_p"]], f["_p"], I_LABEL[f["_i"]], f["_i"]))
        for chave, rot in (("prevenir", "prevenir"), ("detectar", "detectar"),
                           ("limitar", "limitar o estrago")):
            if f.get(chave):
                print("     %s: %s" % (rot, f[chave]))
        print()

    # cobertura externo/interno
    tipos = [f.get("tipo", "").lower() for f in falhas]
    tem_ext = any("ext" in t for t in tipos)
    tem_int = any("int" in t for t in tipos)
    print("-" * 60)
    if not (tem_ext and tem_int):
        print("⚠ Cobertura: marque cada falha como 'externo' (mercado, cliente,")
        print("  concorrente, fornecedor) ou 'interno' (execução, prazo, equipe,")
        print("  fôlego). Uma lista só de um lado está cega para metade do risco.")
    else:
        print("✓ Cobertura: há falhas externas E internas — bom sinal.")
    criticos = [f for f in falhas if f["_bucket"] in ("CRÍTICO", "ALTO")]
    print("\nAja primeiro nos %d modo(s) CRÍTICO/ALTO. Para cada um, garanta pelo"
          % len(criticos))
    print("menos UMA ação de 'prevenir' ou 'limitar' — senão é só susto, não plano.")
    print("\nLembre: L×I é ordem de prioridade, não probabilidade exata. Serve para")
    print("saber onde olhar primeiro, não para fingir precisão que ninguém tem.")


# --------------------------------------------------------------------------- #
# diario — registrar, listar, revisar, calibrar
# --------------------------------------------------------------------------- #
def _ler_diario():
    itens = []
    if not os.path.exists(DIARIO):
        return itens
    with open(DIARIO, encoding="utf-8") as f:
        for linha in f:
            linha = linha.strip()
            if not linha:
                continue
            try:
                itens.append(json.loads(linha))
            except json.JSONDecodeError:
                continue
    return itens


def _reescrever_diario(itens):
    os.makedirs(BASE, exist_ok=True)
    with open(DIARIO, "w", encoding="utf-8") as f:
        for it in itens:
            f.write(json.dumps(it, ensure_ascii=False) + "\n")


def _proximo_id(itens):
    n = 0
    for it in itens:
        m = re.match(r"D-(\d+)", str(it.get("id", "")))
        if m:
            n = max(n, int(m.group(1)))
    return "D-%04d" % (n + 1)


def cmd_diario_add(args):
    itens = _ler_diario()
    novo = {
        "id": _proximo_id(itens),
        "data": hoje_br(),
        "titulo": args.titulo,
        "tipo": args.tipo or "",
        "reversivel": (args.reversivel == "sim"),
        "escolhida": args.escolhida or "",
        "alternativas": [x.strip() for x in (args.alternativas or "").split("|") if x.strip()],
        "o_que_pesou": args.pesou or "",
        "confianca": args.confianca or "média",
        "previsao": args.previsao or "",
        "prob_sucesso": float(args.prob) if args.prob else None,
        "principal_risco": args.risco or "",
        "gatilho_reversao": args.gatilho or "",
        "rever_em": (parse_data(args.rever_em).strftime("%d/%m/%Y")
                     if parse_data(args.rever_em) else ""),
        "status": "aberta",
        "resultado": None,
        "revisado_em": None,
        "risco_ocorreu": None,
        "aprendizado": None,
    }
    os.makedirs(BASE, exist_ok=True)
    with open(DIARIO, "a", encoding="utf-8") as f:
        f.write(json.dumps(novo, ensure_ascii=False) + "\n")
    print("Registrada %s: %s" % (novo["id"], novo["titulo"]))
    if novo["rever_em"]:
        print("Marcada para revisão em %s." % novo["rever_em"])


def cmd_diario_list(args):
    itens = _ler_diario()
    if not itens:
        print("Diário vazio. Registre a primeira decisão com o modo Diário.")
        return
    ref = hoje()
    pendentes = []
    print("=" * 60)
    print("DIÁRIO DE DECISÕES — %d registro(s)" % len(itens))
    print("=" * 60)
    for it in itens:
        rev = parse_data(it.get("rever_em"))
        st = it.get("status", "aberta")
        flag = ""
        if st == "aberta" and rev and rev <= ref:
            flag = "  ⏰ PENDENTE DE REVISÃO"
            pendentes.append(it)
        porta = "mão dupla (reversível)" if it.get("reversivel") else "mão única (difícil de voltar)"
        print("\n%s · %s · [%s]" % (it.get("id"), it.get("data"), st))
        print("  %s" % it.get("titulo"))
        print("  escolha: %s | porta: %s" % (it.get("escolhida") or "—", porta))
        if it.get("rever_em"):
            print("  revisar em: %s%s" % (it.get("rever_em"), flag))
    if pendentes:
        print("\n" + "-" * 60)
        print("⏰ %d decisão(ões) esperando revisão. Use o modo Diário para"
              % len(pendentes))
        print("   registrar o que aconteceu — é assim que seu julgamento calibra.")


def cmd_rever(args):
    itens = _ler_diario()
    alvo = None
    for it in itens:
        if str(it.get("id")).upper() == args.id.upper():
            alvo = it
            break
    if not alvo:
        print("Não achei a decisão %s. Rode 'diario list' para ver os ids." % args.id)
        sys.exit(1)
    alvo["status"] = "revisada"
    alvo["revisado_em"] = hoje_br()
    alvo["resultado"] = args.resultado  # "bom" | "ruim" | "misto"
    if args.risco_ocorreu:
        alvo["risco_ocorreu"] = (args.risco_ocorreu == "sim")
    if args.aprendizado:
        alvo["aprendizado"] = args.aprendizado
    _reescrever_diario(itens)
    print("Revisada %s. Resultado: %s." % (alvo["id"], alvo["resultado"]))
    print("Rode o modo Diário → calibrar para ver o padrão do seu julgamento.")


def cmd_calibrar(args):
    itens = _ler_diario()
    revisadas = [it for it in itens if it.get("status") == "revisada"]
    print("=" * 60)
    print("CALIBRAÇÃO DO SEU JULGAMENTO")
    print("=" * 60)
    if not revisadas:
        print("Ainda não há decisões revisadas. Quando as datas de revisão")
        print("chegarem e você registrar o que aconteceu, o padrão aparece aqui.")
        return
    n = len(revisadas)
    bons = sum(1 for it in revisadas if it.get("resultado") == "bom")
    ruins = sum(1 for it in revisadas if it.get("resultado") == "ruim")
    mistos = n - bons - ruins
    print("Decisões revisadas: %d  (bom: %d · misto: %d · ruim: %d)"
          % (n, bons, mistos, ruins))

    # otimismo: prob_sucesso média declarada vs taxa real de "bom"
    probs = [it.get("prob_sucesso") for it in revisadas
             if isinstance(it.get("prob_sucesso"), (int, float))]
    if probs:
        media_prev = sum(probs) / len(probs)
        taxa_real = bons / n
        print("\nOtimismo declarado vs realidade:")
        print("  você previu, em média, %.0f%% de chance de dar bom." % (100 * media_prev))
        print("  na prática, %.0f%% deram bom." % (100 * taxa_real))
        dif = media_prev - taxa_real
        if n < 5:
            print("  (poucos dados — %d decisões — trate como tendência, não veredito.)" % n)
        elif dif > 0.15:
            print("  → tendência a OTIMISMO: você superestima as chances. Desconte um pouco.")
        elif dif < -0.15:
            print("  → tendência a PESSIMISMO: sai melhor do que você teme. Ouse um pouco mais.")
        else:
            print("  → bem calibrado: sua sensação de chance bate com o que acontece.")

    # os riscos que você previu, aconteceram?
    com_risco = [it for it in revisadas if it.get("risco_ocorreu") is not None]
    if com_risco:
        ocorreu = sum(1 for it in com_risco if it.get("risco_ocorreu"))
        print("\nSeus principais riscos previstos aconteceram em %d de %d casos."
              % (ocorreu, len(com_risco)))
        if len(com_risco) >= 5:
            taxa = ocorreu / len(com_risco)
            if taxa < 0.2:
                print("  → você tende a superdimensionar o risco principal (medo > dano real).")
            elif taxa > 0.6:
                print("  → seus medos costumam se confirmar: leve o pré-mortem ainda mais a sério.")


# --------------------------------------------------------------------------- #
# relatorio — briefing HTML de uma decisão (entregável)
# --------------------------------------------------------------------------- #
def cmd_relatorio(args):
    itens = _ler_diario()
    alvo = None
    for it in itens:
        if str(it.get("id")).upper() == args.id.upper():
            alvo = it
            break
    if not alvo:
        print("Não achei a decisão %s." % args.id)
        sys.exit(1)
    os.makedirs(ENTREGAS, exist_ok=True)
    caminho = os.path.join(ENTREGAS, "Decisao-%s-%s.html" % (alvo["id"], slug(alvo["titulo"])))

    def esc(x):
        return html.escape(str(x)) if x else "—"

    porta = "Mão dupla — reversível" if alvo.get("reversivel") else "Mão única — difícil de voltar"
    alts = "".join("<li>%s</li>" % esc(a) for a in alvo.get("alternativas", [])) or "<li>—</li>"
    prob = alvo.get("prob_sucesso")
    prob_txt = ("%.0f%%" % (100 * prob)) if isinstance(prob, (int, float)) else "—"

    doc = """<!doctype html><html lang="pt-BR"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Decisão %(id)s — %(titulo)s</title>
<style>
  :root{--tinta:#1c1a17;--fundo:#f6f1e7;--carta:#fffdf8;--accent:#b3541e;--linha:#e2d8c4;}
  *{box-sizing:border-box}
  body{margin:0;background:var(--fundo);color:var(--tinta);
       font:16px/1.6 "Iowan Old Style",Georgia,serif;padding:40px 20px}
  .wrap{max-width:660px;margin:0 auto}
  .kick{font:600 12px/1 ui-sans-serif,system-ui;letter-spacing:.18em;
        text-transform:uppercase;color:var(--accent)}
  h1{font-size:32px;line-height:1.15;margin:8px 0 4px}
  .meta{color:#6b6357;font:14px/1.5 ui-sans-serif,system-ui;margin-bottom:24px}
  .card{background:var(--carta);border:1px solid var(--linha);border-radius:12px;
        padding:20px 22px;margin:16px 0;box-shadow:0 1px 2px rgba(60,40,10,.04),
        0 8px 24px rgba(60,40,10,.05)}
  h2{font:600 13px/1 ui-sans-serif,system-ui;letter-spacing:.08em;
     text-transform:uppercase;color:var(--accent);margin:0 0 10px}
  ul{margin:6px 0 0;padding-left:20px}
  .call{background:var(--tinta);color:#f6f1e7;border:none}
  .call h2{color:#e9a06b}
  .foot{color:#8a8172;font:13px/1.5 ui-sans-serif,system-ui;margin-top:24px;
        border-top:1px solid var(--linha);padding-top:12px}
</style></head><body><div class="wrap">
<div class="kick">Fulcro · briefing de decisão</div>
<h1>%(titulo)s</h1>
<div class="meta">%(id)s · registrada em %(data)s · %(porta)s</div>

<div class="card"><h2>A escolha</h2><p><strong>%(escolhida)s</strong></p>
<h2 style="margin-top:16px">Alternativas consideradas</h2><ul>%(alts)s</ul></div>

<div class="card"><h2>O que pesou</h2><p>%(pesou)s</p></div>

<div class="card"><h2>Previsão</h2><p>%(previsao)s</p>
<p style="color:#6b6357;font:14px ui-sans-serif,system-ui">
Confiança: %(confianca)s · chance de dar bom: %(prob)s · revisar em: %(rever)s</p></div>

<div class="card"><h2>Principal risco</h2><p>%(risco)s</p></div>

<div class="card call"><h2>Gatilho de reversão</h2>
<p>O sinal que dirá para mudar de rumo: %(gatilho)s</p></div>

<div class="foot">Este briefing foi montado pelo Fulcro a partir do seu diário local
(.fulcro/). Ele estrutura a decisão — a caneta é sua. Reabra na data de revisão para
registrar o que aconteceu e calibrar seu julgamento.</div>
</div></body></html>""" % {
        "id": esc(alvo["id"]), "titulo": esc(alvo["titulo"]), "data": esc(alvo.get("data")),
        "porta": esc(porta), "escolhida": esc(alvo.get("escolhida")),
        "alts": alts, "pesou": esc(alvo.get("o_que_pesou")),
        "previsao": esc(alvo.get("previsao")), "confianca": esc(alvo.get("confianca")),
        "prob": prob_txt, "rever": esc(alvo.get("rever_em")),
        "risco": esc(alvo.get("principal_risco")), "gatilho": esc(alvo.get("gatilho_reversao")),
    }
    with open(caminho, "w", encoding="utf-8") as f:
        f.write(doc)
    print("Briefing salvo em:", caminho)
    print("Abra no navegador e, se quiser, imprima como PDF.")


# --------------------------------------------------------------------------- #
# CLI
# --------------------------------------------------------------------------- #
def main():
    p = argparse.ArgumentParser(description="Fulcro — copiloto de decisão (local, stdlib).")
    sub = p.add_subparsers(dest="cmd")

    sub.add_parser("init", help="cria .fulcro/ (idempotente)")

    m = sub.add_parser("matriz", help="matriz de decisão ponderada + sensibilidade")
    m.add_argument("--arquivo", help="JSON com criterios+opcoes (senão lê do stdin)")

    r = sub.add_parser("risco", help="ordena modos de falha por Prob × Impacto")
    r.add_argument("--arquivo", help="JSON com falhas (senão lê do stdin)")

    da = sub.add_parser("add", help="registra uma decisão no diário")
    da.add_argument("--titulo", required=True)
    da.add_argument("--tipo", default="")
    da.add_argument("--reversivel", choices=["sim", "nao"], default="nao")
    da.add_argument("--escolhida", default="")
    da.add_argument("--alternativas", default="", help="separadas por |")
    da.add_argument("--pesou", default="")
    da.add_argument("--confianca", default="média")
    da.add_argument("--previsao", default="")
    da.add_argument("--prob", default="", help="chance de dar bom, 0 a 1 (ex.: 0.7)")
    da.add_argument("--risco", default="")
    da.add_argument("--gatilho", default="")
    da.add_argument("--rever-em", dest="rever_em", default="")

    sub.add_parser("list", help="lista o diário e o que está pendente de revisão")

    rv = sub.add_parser("rever", help="registra o resultado de uma decisão")
    rv.add_argument("--id", required=True)
    rv.add_argument("--resultado", choices=["bom", "ruim", "misto"], required=True)
    rv.add_argument("--risco-ocorreu", dest="risco_ocorreu", choices=["sim", "nao"], default="")
    rv.add_argument("--aprendizado", default="")

    sub.add_parser("calibrar", help="mostra o padrão do seu julgamento ao longo do tempo")

    rel = sub.add_parser("relatorio", help="gera o briefing HTML de uma decisão")
    rel.add_argument("--id", required=True)

    args = p.parse_args()
    if not args.cmd:
        p.print_help()
        return
    try:
        {
            "init": cmd_init,
            "matriz": cmd_matriz,
            "risco": cmd_risco,
            "add": cmd_diario_add,
            "list": cmd_diario_list,
            "rever": cmd_rever,
            "calibrar": cmd_calibrar,
            "relatorio": cmd_relatorio,
        }[args.cmd](args)
    except (ValueError, json.JSONDecodeError) as e:
        print("Erro:", e)
        sys.exit(1)


if __name__ == "__main__":
    main()
