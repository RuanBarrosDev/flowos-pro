#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Alfândega — motor de sourcing e CUSTO DE ATERRISSAGEM (landed cost).

Descobre e compara fornecedores e calcula quanto um produto CUSTA DE VERDADE
para chegar na sua prateleira: produto + frete + seguro + impostos + despesas.
Python biblioteca padrão, offline. Guarda tudo em ./.alfandega/.

A parte VERIFICÁVEL (contas de imposto, câmbio, comparação, nota de risco) é
deste motor. As mensagens de negociação e a leitura do caso quem escreve é a IA.

NUNCA inventa alíquota, NCM ou lei. Alíquotas de referência são ESTIMATIVAS
marcadas — o dono confirma no NCM/simulador oficial antes de comprar.
"""

import argparse
import csv
import os
import unicodedata
from datetime import datetime

DATA_DIR = os.path.join(os.getcwd(), ".alfandega")
FORNECEDORES = os.path.join(DATA_DIR, "fornecedores.csv")
COTACOES = os.path.join(DATA_DIR, "cotacoes.csv")
CONFIG = os.path.join(DATA_DIR, "config.md")

FORN_COLS = ["id", "nome", "pais", "produto", "contato", "moq", "prazo_dias",
             "pagamento", "incoterm", "moeda", "risco_score", "risco_nivel",
             "risco_notas", "criado"]
COT_COLS = ["id", "produto", "fornecedor", "regime", "moeda", "cambio",
            "preco_unit_orig", "qtd", "frete_intl", "seguro", "modal", "ncm",
            "aliq_ii", "aliq_ipi", "aliq_icms", "outras_desp",
            "custo_total_brl", "custo_unit_brl", "criado"]

# ---------------------------------------------------------------------------
# Alíquotas de REFERÊNCIA (estimativas — sempre confirmar no NCM oficial).
# PIS/COFINS-Importação usam alíquotas gerais; II/IPI/ICMS variam por produto/UF.
PIS_IMPORT = 2.10      # % sobre valor aduaneiro (regra geral)
COFINS_IMPORT = 9.65   # % sobre valor aduaneiro (regra geral)
AFRMM = 8.0            # % sobre o frete MARÍTIMO internacional
TAXA_SISCOMEX = 154.23  # R$ fixo por DI (referência — confira o valor vigente)

# Regime simplificado (Remessa Conforme / courier até US$ 3.000): estimativa.
RTS_II = 60.0          # % de II sobre (produto + frete + seguro)
RTS_OBS = ("Regime simplificado (Remessa Conforme/courier). Estimativa: II 60% "
           "sobre produto+frete+seguro, + ICMS do seu estado. A lei muda — "
           "confirme na Receita Federal / programa Remessa Conforme.")

NIVEIS_RISCO = [
    (0, 34, "🔴 ALTO", "Não pague nada antes de resolver os itens em aberto."),
    (35, 69, "🟡 MÉDIO", "Reduza o risco: amostra + pagamento protegido antes do pedido cheio."),
    (70, 100, "🟢 BAIXO", "Fornecedor razoavelmente verificado. Ainda assim, comece pequeno."),
]

# Checklist de verificação de fornecedor (anti-golpe). Peso soma 100.
RISCO_ITENS = [
    ("empresa_verificada", 18, "Empresa existe e é verificável (CNPJ/registro, site, tempo de mercado)"),
    ("amostra", 16, "Você recebeu (ou vai receber) uma AMOSTRA antes do pedido cheio"),
    ("pagamento_protegido", 18, "Pagamento por meio PROTEGIDO (Trade Assurance/cartão/escrow), não PIX/TED direto"),
    ("contato_oficial", 10, "Contato por canal oficial da empresa, não só WhatsApp/Wechat pessoal"),
    ("referencias", 12, "Tem referências/avaliações de outros compradores"),
    ("contrato", 10, "Combinado por escrito: specs, prazo, quem paga o quê (Incoterm)"),
    ("preco_coerente", 10, "Preço coerente com o mercado (bom demais = alerta de golpe)"),
    ("historico", 6, "Já comprou antes desse fornecedor sem problema"),
]


def _ensure_dir():
    os.makedirs(DATA_DIR, exist_ok=True)


def _read(path, cols):
    if not os.path.exists(path):
        return []
    with open(path, encoding="utf-8") as f:
        return list(csv.DictReader(f))


def _write(path, cols, rows):
    _ensure_dir()
    with open(path, "w", encoding="utf-8", newline="") as f:
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
        if rid.startswith(prefix):
            try:
                n = max(n, int(rid[len(prefix):]))
            except ValueError:
                pass
    return f"{prefix}{n + 1:03d}"


def _f(v, default=0.0):
    try:
        return float(str(v).replace(",", "."))
    except (ValueError, TypeError):
        return default


def _brl(v):
    return f"R$ {v:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")


def _strip(s):
    return "".join(c for c in unicodedata.normalize("NFD", s)
                   if unicodedata.category(c) != "Mn").lower()


def _find_forn(key):
    rows = _read(FORNECEDORES, FORN_COLS)
    for r in rows:
        if r["id"] == key:
            return r
    k = _strip(key)
    for r in rows:
        if k in _strip(r["nome"]):
            return r
    return None


# ---------------------------------------------------------------------------
def cmd_init(_):
    _ensure_dir()
    if not os.path.exists(FORNECEDORES):
        _write(FORNECEDORES, FORN_COLS, [])
    if not os.path.exists(COTACOES):
        _write(COTACOES, COT_COLS, [])
    print("✅ Alfândega pronta. Dados em ./.alfandega/ (fornecedores.csv, cotacoes.csv).")
    print("   Lembre: .alfandega/ deve estar no .gitignore (preço, custo e fornecedor são privados).")


def cmd_fornecedor_add(a):
    rows = _read(FORNECEDORES, FORN_COLS)
    fid = _next_id(rows, "F")
    row = {
        "id": fid, "nome": a.nome, "pais": a.pais or "", "produto": a.produto or "",
        "contato": a.contato or "", "moq": a.moq or "", "prazo_dias": a.prazo or "",
        "pagamento": a.pagamento or "", "incoterm": (a.incoterm or "").upper(),
        "moeda": (a.moeda or "").upper(), "risco_score": "", "risco_nivel": "",
        "risco_notas": "", "criado": _now(),
    }
    rows.append(row)
    _write(FORNECEDORES, FORN_COLS, rows)
    print(f"✅ Fornecedor {fid} — {a.nome} cadastrado.")
    print("   Rode a verificação de risco: `risco --fornecedor " + fid + " ...`")


def cmd_fornecedores(_):
    rows = _read(FORNECEDORES, FORN_COLS)
    if not rows:
        print("Nenhum fornecedor cadastrado ainda. Use `fornecedor-add`.")
        return
    print(f"📇 {len(rows)} fornecedor(es):\n")
    for r in rows:
        risco = f"{r['risco_nivel']} ({r['risco_score']})" if r["risco_score"] else "risco não avaliado"
        print(f"  {r['id']} — {r['nome']}  [{r['pais']}]  {risco}")
        det = []
        if r["produto"]:
            det.append(r["produto"])
        if r["moq"]:
            det.append(f"MOQ {r['moq']}")
        if r["prazo_dias"]:
            det.append(f"prazo {r['prazo_dias']}d")
        if r["incoterm"]:
            det.append(r["incoterm"])
        if det:
            print("       " + " · ".join(det))


def cmd_risco(a):
    forn = _find_forn(a.fornecedor)
    if not forn:
        print(f"❌ Fornecedor '{a.fornecedor}' não encontrado. Veja `fornecedores`.")
        return
    marcados = set()
    if a.sim:
        for tok in a.sim.split(","):
            marcados.add(tok.strip())
    score = 0
    linhas = []
    for chave, peso, texto in RISCO_ITENS:
        ok = chave in marcados
        score += peso if ok else 0
        linhas.append(f"  [{'x' if ok else ' '}] ({peso:>2}) {texto}")
    nivel, dica = "", ""
    for lo, hi, nome, orient in NIVEIS_RISCO:
        if lo <= score <= hi:
            nivel, dica = nome, orient
            break
    forn["risco_score"] = str(score)
    forn["risco_nivel"] = nivel
    forn["risco_notas"] = a.sim or ""
    rows = _read(FORNECEDORES, FORN_COLS)
    _write(FORNECEDORES, FORN_COLS, [forn if r["id"] == forn["id"] else r for r in rows])
    print(f"🛡️  Verificação de {forn['nome']} — nota {score}/100  {nivel}\n")
    print("\n".join(linhas))
    print(f"\n👉 {dica}")
    faltam = [t for c, _, t in RISCO_ITENS if c not in marcados]
    if faltam:
        print("\nEm aberto (resolva antes de pagar):")
        for t in faltam:
            print(f"  • {t}")


def _calc_landed(regime, preco_unit, qtd, cambio, frete, seguro, modal,
                 aliq_ii, aliq_ipi, aliq_icms, outras):
    """Retorna dict com o detalhamento em BRL. Valores de entrada na moeda de origem
    (preco_unit, frete, seguro) já convertidos por 'cambio' quando aplicável."""
    fob_total = preco_unit * qtd
    # converte para BRL
    fob_brl = fob_total * cambio
    frete_brl = frete * cambio
    seguro_brl = seguro * cambio
    det = {}
    if regime == "nacional":
        # compra nacional: sem II/IPI-import/PIS/COFINS-import. Só produto + custos.
        base = fob_brl + frete_brl + seguro_brl + outras
        det = {
            "Produto (FOB)": fob_brl, "Frete": frete_brl, "Seguro": seguro_brl,
            "Outras despesas": outras,
        }
        total = base
    elif regime == "simplificado":
        va = fob_brl + frete_brl + seguro_brl  # base do simplificado
        ii = va * (RTS_II / 100.0)
        base_icms = va + ii
        icms = base_icms / (1 - aliq_icms / 100.0) * (aliq_icms / 100.0) if aliq_icms else 0.0
        det = {
            "Produto (FOB)": fob_brl, "Frete": frete_brl, "Seguro": seguro_brl,
            f"II simplificado ({RTS_II:.0f}%)": ii,
            f"ICMS ({aliq_icms:.0f}%, por dentro)": icms,
            "Outras despesas": outras,
        }
        total = fob_brl + frete_brl + seguro_brl + ii + icms + outras
    else:  # formal
        va = fob_brl + frete_brl + seguro_brl  # Valor Aduaneiro (CIF)
        ii = va * (aliq_ii / 100.0)
        ipi = (va + ii) * (aliq_ipi / 100.0)
        pis = va * (PIS_IMPORT / 100.0)
        cofins = va * (COFINS_IMPORT / 100.0)
        afrmm = (frete_brl * AFRMM / 100.0) if modal == "maritimo" else 0.0
        siscomex = TAXA_SISCOMEX
        despesas_aduaneiras = afrmm + siscomex + outras
        # ICMS "por dentro": base = (VA + II + IPI + PIS + COFINS + despesas) / (1 - aliq)
        soma = va + ii + ipi + pis + cofins + despesas_aduaneiras
        icms = soma / (1 - aliq_icms / 100.0) * (aliq_icms / 100.0) if aliq_icms else 0.0
        det = {
            "Produto (FOB)": fob_brl, "Frete internacional": frete_brl,
            "Seguro": seguro_brl,
            f"II ({aliq_ii:.1f}%)": ii,
            f"IPI ({aliq_ipi:.1f}%)": ipi,
            f"PIS-Import ({PIS_IMPORT}%)": pis,
            f"COFINS-Import ({COFINS_IMPORT}%)": cofins,
        }
        if afrmm:
            det[f"AFRMM ({AFRMM:.0f}% do frete marítimo)"] = afrmm
        det["Taxa Siscomex"] = siscomex
        if outras:
            det["Outras despesas (despachante etc.)"] = outras
        det[f"ICMS ({aliq_icms:.0f}%, por dentro)"] = icms
        total = va + ii + ipi + pis + cofins + despesas_aduaneiras + icms
    unit = total / qtd if qtd else total
    return det, total, unit


def cmd_cotar(a):
    regime = a.regime if a.regime in ("formal", "simplificado", "nacional") else "formal"
    cambio = _f(a.cambio, 1.0) if regime != "nacional" else _f(a.cambio, 1.0)
    if regime == "nacional" and not a.cambio:
        cambio = 1.0
    preco = _f(a.preco)
    qtd = int(_f(a.qtd, 1)) or 1
    frete = _f(a.frete)
    seguro = _f(a.seguro)
    outras = _f(a.outras)
    modal = a.modal if a.modal in ("maritimo", "aereo", "rodoviario", "") else ""
    aliq_ii = _f(a.ii)
    aliq_ipi = _f(a.ipi)
    aliq_icms = _f(a.icms)

    det, total, unit = _calc_landed(regime, preco, qtd, cambio, frete, seguro,
                                    modal, aliq_ii, aliq_ipi, aliq_icms, outras)

    rows = _read(COTACOES, COT_COLS)
    cid = _next_id(rows, "C")
    row = {
        "id": cid, "produto": a.produto, "fornecedor": a.fornecedor or "",
        "regime": regime, "moeda": (a.moeda or "BRL").upper(), "cambio": cambio,
        "preco_unit_orig": preco, "qtd": qtd, "frete_intl": frete, "seguro": seguro,
        "modal": modal, "ncm": a.ncm or "", "aliq_ii": aliq_ii, "aliq_ipi": aliq_ipi,
        "aliq_icms": aliq_icms, "outras_desp": outras,
        "custo_total_brl": round(total, 2), "custo_unit_brl": round(unit, 2),
        "criado": _now(),
    }
    rows.append(row)
    _write(COTACOES, COT_COLS, rows)

    print(f"📦 Cotação {cid} — {a.produto}  (regime: {regime})")
    if a.fornecedor:
        print(f"   Fornecedor: {a.fornecedor}")
    if regime != "nacional":
        print(f"   Câmbio usado: {cambio:.4f}  ·  {qtd} un a {a.moeda or 'moeda'} {preco:.2f}")
    if a.ncm:
        print(f"   NCM: {a.ncm}")
    print("\n   Detalhamento (em BRL):")
    for k, v in det.items():
        print(f"     {k:<40} {_brl(v)}")
    print(f"     {'—' * 40}")
    print(f"     {'CUSTO TOTAL':<40} {_brl(total)}")
    print(f"     {'CUSTO POR UNIDADE':<40} {_brl(unit)}")
    print(f"\n   💾 Salvo como {cid}. Use `comparar --produto \"{a.produto}\"` p/ comparar cotações.")
    if regime == "simplificado":
        print("\n   ⚠️  " + RTS_OBS)
    if regime == "formal":
        print("\n   ⚠️  Alíquotas de II/IPI/ICMS variam por NCM e estado. Confirme no "
              "Simulador do Portal Único Siscomex / no seu contador antes de comprar.")


def cmd_comparar(a):
    rows = [r for r in _read(COTACOES, COT_COLS)
            if _strip(a.produto) in _strip(r["produto"])]
    if len(rows) < 1:
        print(f"Nenhuma cotação encontrada para '{a.produto}'. Use `cotar` primeiro.")
        return
    rows.sort(key=lambda r: _f(r["custo_unit_brl"]))
    print(f"⚖️  Comparação de {len(rows)} cotação(ões) para '{a.produto}' "
          f"(ordenado pelo custo UNITÁRIO aterrissado):\n")
    melhor = _f(rows[0]["custo_unit_brl"])
    for i, r in enumerate(rows):
        unit = _f(r["custo_unit_brl"])
        dif = ""
        if i > 0 and melhor > 0:
            pct = (unit - melhor) / melhor * 100
            dif = f"  (+{pct:.1f}% vs. melhor)"
        selo = "🥇" if i == 0 else "  "
        forn = r["fornecedor"] or "?"
        print(f"  {selo} {r['id']}  {forn:<18} {r['regime']:<12} "
              f"unit {_brl(unit)}  total {_brl(_f(r['custo_total_brl']))}{dif}")
    print("\n👉 O menor PREÇO FOB nem sempre é o menor custo real — compare sempre "
          "o custo UNITÁRIO aterrissado (com frete + imposto + câmbio).")


def cmd_cambio(a):
    valor = _f(a.valor)
    taxa = _f(a.taxa)
    if not taxa:
        print("Informe a taxa: `cambio --valor 1000 --taxa 5.45 --moeda USD`")
        return
    brl = valor * taxa
    v_fmt = f"{valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    print(f"💱 {a.moeda or 'moeda'} {v_fmt} × {taxa:.4f} = {_brl(brl)}")
    if a.margem:
        m = _f(a.margem)
        pior = valor * taxa * (1 + m / 100.0)
        print(f"   Se o câmbio subir {m:.0f}%: {_brl(pior)}  "
              f"(reserve essa folga no preço de venda).")


def cmd_painel(_):
    forn = _read(FORNECEDORES, FORN_COLS)
    cot = _read(COTACOES, COT_COLS)
    print("📊 Painel Alfândega\n")
    print(f"  Fornecedores cadastrados: {len(forn)}")
    if forn:
        avaliados = [r for r in forn if r["risco_score"]]
        print(f"    avaliados de risco: {len(avaliados)}/{len(forn)}")
        for r in forn:
            if r["risco_nivel"].startswith("🔴"):
                print(f"    ⚠️  {r['nome']} está em RISCO ALTO — não pague antes de resolver.")
    print(f"  Cotações registradas: {len(cot)}")
    produtos = {}
    for r in cot:
        produtos.setdefault(r["produto"], []).append(_f(r["custo_unit_brl"]))
    for p, custos in produtos.items():
        print(f"    • {p}: {len(custos)} cotação(ões), melhor custo/un {_brl(min(custos))}")


def cmd_exportar(a):
    rows = _read(COTACOES, COT_COLS)
    r = next((x for x in rows if x["id"] == a.cotacao), None)
    if not r:
        print(f"❌ Cotação '{a.cotacao}' não encontrada.")
        return
    print(f"=== PLANO DE IMPORTAÇÃO — {r['produto']} ({r['id']}) ===\n")
    print(f"Fornecedor: {r['fornecedor'] or '—'}")
    print(f"Regime: {r['regime']}   NCM: {r['ncm'] or '—'}   Modal: {r['modal'] or '—'}")
    print(f"Quantidade: {r['qtd']} un")
    if r["regime"] != "nacional":
        print(f"Preço origem: {r['moeda']} {_f(r['preco_unit_orig']):.2f}/un  ·  câmbio {_f(r['cambio']):.4f}")
        print(f"Frete internacional: {_f(r['frete_intl']):.2f}  ·  Seguro: {_f(r['seguro']):.2f}")
        print(f"Alíquotas usadas: II {r['aliq_ii']}%  IPI {r['aliq_ipi']}%  ICMS {r['aliq_icms']}%")
    print(f"\nCUSTO TOTAL:  {_brl(_f(r['custo_total_brl']))}")
    print(f"CUSTO/UNIDADE: {_brl(_f(r['custo_unit_brl']))}")
    print("\n⚠️  Números são estimativa de planejamento. Confirme alíquotas no NCM/simulador "
          "oficial e o câmbio no dia do fechamento antes de comprar.")


def build_parser():
    p = argparse.ArgumentParser(description="Alfândega — sourcing e custo de aterrissagem.")
    sub = p.add_subparsers(dest="cmd", required=True)

    sub.add_parser("init").set_defaults(func=cmd_init)

    fa = sub.add_parser("fornecedor-add")
    fa.add_argument("--nome", required=True)
    fa.add_argument("--pais")
    fa.add_argument("--produto")
    fa.add_argument("--contato")
    fa.add_argument("--moq")
    fa.add_argument("--prazo")
    fa.add_argument("--pagamento")
    fa.add_argument("--incoterm")
    fa.add_argument("--moeda")
    fa.set_defaults(func=cmd_fornecedor_add)

    sub.add_parser("fornecedores").set_defaults(func=cmd_fornecedores)

    rk = sub.add_parser("risco")
    rk.add_argument("--fornecedor", required=True)
    rk.add_argument("--sim", help="itens confirmados, separados por vírgula (ex: amostra,pagamento_protegido)")
    rk.set_defaults(func=cmd_risco)

    ct = sub.add_parser("cotar")
    ct.add_argument("--produto", required=True)
    ct.add_argument("--fornecedor")
    ct.add_argument("--regime", help="formal | simplificado | nacional")
    ct.add_argument("--moeda")
    ct.add_argument("--cambio")
    ct.add_argument("--preco", help="preço unitário na moeda de origem")
    ct.add_argument("--qtd")
    ct.add_argument("--frete", help="frete internacional total (moeda de origem)")
    ct.add_argument("--seguro")
    ct.add_argument("--modal", help="maritimo | aereo | rodoviario")
    ct.add_argument("--ncm")
    ct.add_argument("--ii", help="alíquota II (percentual)")
    ct.add_argument("--ipi", help="alíquota IPI (percentual)")
    ct.add_argument("--icms", help="alíquota ICMS (percentual)")
    ct.add_argument("--outras", help="outras despesas em BRL (despachante, armazenagem)")
    ct.set_defaults(func=cmd_cotar)

    cp = sub.add_parser("comparar")
    cp.add_argument("--produto", required=True)
    cp.set_defaults(func=cmd_comparar)

    cb = sub.add_parser("cambio")
    cb.add_argument("--valor", required=True)
    cb.add_argument("--taxa", required=True)
    cb.add_argument("--moeda")
    cb.add_argument("--margem", help="stress: percentual de alta do câmbio a simular")
    cb.set_defaults(func=cmd_cambio)

    sub.add_parser("painel").set_defaults(func=cmd_painel)

    ex = sub.add_parser("exportar")
    ex.add_argument("--cotacao", required=True)
    ex.set_defaults(func=cmd_exportar)

    return p


def main():
    args = build_parser().parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
