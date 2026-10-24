#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Sextante — motor do diagnóstico de maturidade em IA de uma empresa.
Só biblioteca padrão do Python. Guarda tudo em .sextante/<cliente>.json (local, git-ignored).

O consultor conversa em português; o Claude chama estes comandos por baixo.
Nada aqui inventa dado do cliente — o que não foi respondido fica em branco/[SUPOR].
"""
import json, os, sys, argparse, datetime, unicodedata, re

RAIZ = ".sextante"

# As 6 dimensoes da prontidao (adaptadas para PMEs de servico).
DIMENSOES = [
    ("estrategia", "Estrategia & Lideranca"),
    ("dados",      "Dados & Organizacao da informacao"),
    ("processos",  "Processos"),
    ("pessoas",    "Pessoas & Cultura"),
    ("ferramentas","Ferramentas & Integracao"),
    ("governanca", "Governanca & Confianca"),
]
DIM_KEYS = [d[0] for d in DIMENSOES]
# Dimensoes que sao pre-requisito: nota baixa aqui trava recomendacoes agressivas.
PORTOES = ("dados", "governanca")

ESTAGIOS = [
    (0,  24, "Iniciante",  "A empresa ainda usa IA de forma solta ou nenhuma. Base a construir."),
    (25, 39, "Explorando", "Ha experimentos isolados; falta metodo e continuidade."),
    (40, 51, "Praticando", "IA ja entrega valor em algumas frentes de forma consistente."),
    (52, 60, "Escalando",  "IA e parte da operacao; da para ampliar e integrar com seguranca."),
]

def _agora():
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M")

def _config():
    """Le .sextante/config.json (consultor/tom/moeda). Vazio se nao houver setup."""
    p = os.path.join(RAIZ, "config.json")
    if os.path.exists(p):
        try:
            with open(p, encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass
    return {"consultor": "", "tom": "", "moeda": "R$"}

def _slug(txt):
    t = unicodedata.normalize("NFKD", txt).encode("ascii", "ignore").decode()
    t = re.sub(r"[^a-zA-Z0-9]+", "-", t).strip("-").lower()
    return t or "cliente"

def _caminho(cliente):
    return os.path.join(RAIZ, _slug(cliente) + ".json")

def _carregar(cliente):
    p = _caminho(cliente)
    if os.path.exists(p):
        with open(p, encoding="utf-8") as f:
            return json.load(f)
    return {
        "cliente": cliente,
        "criado_em": _agora(),
        "notas": {},          # dimensao -> {"1": 0|1|2, ...}
        "observacoes": {},    # dimensao -> texto do consultor
        "casos": [],          # oportunidades levantadas
    }

def _salvar(dados):
    os.makedirs(RAIZ, exist_ok=True)
    dados["atualizado_em"] = _agora()
    with open(_caminho(dados["cliente"]), "w", encoding="utf-8") as f:
        json.dump(dados, f, ensure_ascii=False, indent=2)

# ---------- calculo ----------
def _nota_dimensao(dados, dim):
    n = dados["notas"].get(dim, {})
    if not n:
        return None, 0, 0
    vals = [int(v) for v in n.values()]
    return sum(vals), len(vals), 10  # (soma, respondidas, max esperado por dim)

def _total(dados):
    soma = 0
    resp = 0
    for dim in DIM_KEYS:
        s, r, _ = _nota_dimensao(dados, dim)
        if s is not None:
            soma += s
            resp += r
    return soma, resp

def _estagio(total):
    for lo, hi, nome, desc in ESTAGIOS:
        if lo <= total <= hi:
            return nome, desc
    return ESTAGIOS[-1][2], ESTAGIOS[-1][3]

def _elo_fraco(dados):
    piores = []
    for dim, rot in DIMENSOES:
        s, r, mx = _nota_dimensao(dados, dim)
        if s is None:
            continue
        piores.append((s, rot, dim))
    if not piores:
        return None
    piores.sort()
    return piores[0]  # (soma, rotulo, dim)

def _portao_reprovado(dados):
    """Retorna lista de dimensoes-portao com nota fraca (< 5 de 10)."""
    reprov = []
    for dim in PORTOES:
        s, r, mx = _nota_dimensao(dados, dim)
        if s is not None and s < 5:
            rot = dict(DIMENSOES)[dim]
            reprov.append(rot)
    return reprov

# ---------- comandos ----------
def cmd_nota(args):
    dados = _carregar(args.cliente)
    if args.dim not in DIM_KEYS:
        print("ERRO: dimensao invalida. Use uma de:", ", ".join(DIM_KEYS)); sys.exit(1)
    if args.valor not in (0, 1, 2):
        print("ERRO: valor deve ser 0, 1 ou 2."); sys.exit(1)
    dados["notas"].setdefault(args.dim, {})[str(args.pergunta)] = args.valor
    if args.obs:
        dados["observacoes"][args.dim] = args.obs
    _salvar(dados)
    print(f"OK: {args.dim} pergunta {args.pergunta} = {args.valor}")

def cmd_caso(args):
    dados = _carregar(args.cliente)
    caso = {
        "id": len(dados["casos"]) + 1,
        "titulo": args.titulo,
        "area": args.area or "",
        "alcance": args.alcance,      # 1-5 quantas pessoas/clientes toca
        "frequencia": args.frequencia, # 1-5 quao recorrente
        "dor": args.dor,               # 1-5 quanto incomoda hoje
        "esforco": args.esforco,       # 1-5 quao dificil de implantar
        "obs": args.obs or "",
    }
    dados["casos"].append(caso)
    _salvar(dados)
    print(f"OK: caso #{caso['id']} '{caso['titulo']}' registrado.")

def _score_caso(c):
    impacto = c["alcance"] * c["frequencia"] * c["dor"]
    return round(impacto / max(1, c["esforco"]), 1)

def _quadrante(c):
    impacto = c["alcance"] * c["frequencia"] * c["dor"]
    alto_imp = impacto >= 27  # ~metade de 125
    baixo_esf = c["esforco"] <= 2
    if alto_imp and baixo_esf:  return "Ganho Rapido"
    if alto_imp and not baixo_esf: return "Projeto"
    if not alto_imp and baixo_esf: return "Talvez"
    return "Evite por ora"

def cmd_priorizar(args):
    dados = _carregar(args.cliente)
    if not dados["casos"]:
        print("Nenhum caso de uso registrado ainda. Rode o modo Oportunidades primeiro."); return
    casos = sorted(dados["casos"], key=_score_caso, reverse=True)
    reprov = _portao_reprovado(dados)
    print(f"== Oportunidades priorizadas — {dados['cliente']} ==")
    for c in casos:
        print(f"  #{c['id']} [{_quadrante(c)}] score {_score_caso(c)} — {c['titulo']}"
              + (f"  ({c['area']})" if c["area"] else ""))
    if reprov:
        print("\n  ATENCAO (portao de pre-requisito reprovado): " + ", ".join(reprov))
        print("  Priorize primeiro arrumar essa base — automatizar sobre ela multiplica erro.")

def cmd_roadmap(args):
    dados = _carregar(args.cliente)
    total, resp = _total(dados)
    est, _ = _estagio(total)
    casos = sorted(dados["casos"], key=_score_caso, reverse=True)
    ganhos = [c for c in casos if _quadrante(c) == "Ganho Rapido"]
    projetos = [c for c in casos if _quadrante(c) == "Projeto"]
    talvez = [c for c in casos if _quadrante(c) == "Talvez"]
    cfg = _config()
    autoria = f"  ·  {cfg['consultor']}" if cfg.get("consultor") else ""
    print(f"== Roadmap de adocao — {dados['cliente']} (estagio: {est}){autoria} ==")
    print("\nOnda 1 — proximos 90 dias (ganhos rapidos, prova de valor):")
    for c in (ganhos or talvez)[:3] or ["(levante oportunidades primeiro)"]:
        print("  - " + (c["titulo"] if isinstance(c, dict) else c))
    print("\nOnda 2 — 3 a 6 meses (projetos de maior retorno):")
    for c in projetos[:3] or ["(a definir apos a Onda 1)"]:
        print("  - " + (c["titulo"] if isinstance(c, dict) else c))
    print("\nOnda 3 — 6 a 12 meses (integrar e escalar):")
    reprov = _portao_reprovado(dados)
    if reprov:
        print("  - Consolidar base antes de escalar: " + ", ".join(reprov))
    print("  - Conectar sistemas, medir ROI e treinar o time no que ja funciona.")
    if est == "Iniciante":
        print("\n  Nota: estagio Iniciante — comece pequeno e manual-assistido; "
              "nao empurre automacao complexa ainda.")

def cmd_relatorio(args):
    dados = _carregar(args.cliente)
    cfg = _config()
    total, resp = _total(dados)
    est, desc = _estagio(total)
    print(f"# Diagnostico de Maturidade em IA — {dados['cliente']}")
    autoria = f" · por {cfg['consultor']}" if cfg.get("consultor") else ""
    print(f"_Gerado em {_agora()}{autoria} · pontuacao {total}/60 · estagio {est}_\n")
    print(f"**Panorama:** {desc}\n")
    print("## Prontidao por dimensao")
    for dim, rot in DIMENSOES:
        s, r, mx = _nota_dimensao(dados, dim)
        if s is None:
            print(f"- {rot}: (nao avaliada)")
        else:
            barra = "#" * s + "." * (10 - s)
            obs = dados["observacoes"].get(dim, "")
            print(f"- {rot}: {s}/10  [{barra}]" + (f" — {obs}" if obs else ""))
    elo = _elo_fraco(dados)
    if elo:
        print(f"\n**Elo mais fraco:** {elo[1]} — atacar isto destrava o resto.")
    print("\n## Principais oportunidades")
    casos = sorted(dados["casos"], key=_score_caso, reverse=True)[:5]
    if not casos:
        print("(nenhuma levantada ainda)")
    for c in casos:
        print(f"- [{_quadrante(c)}] {c['titulo']}" + (f" — {c['area']}" if c["area"] else ""))
    print("\n## Recomendacao")
    print(f"Seguir o roadmap em ondas a partir do estagio {est}. "
          "Comecar pelos ganhos rapidos para gerar prova de valor antes de investir em projetos maiores.")

def cmd_resumo(args):
    dados = _carregar(args.cliente)
    total, resp = _total(dados)
    est, _ = _estagio(total)
    print(f"Cliente: {dados['cliente']}")
    print(f"Perguntas respondidas: {resp} · pontuacao {total}/60 · estagio {est}")
    faltam = [rot for dim, rot in DIMENSOES if _nota_dimensao(dados, dim)[0] is None]
    if faltam:
        print("Dimensoes ainda nao avaliadas: " + ", ".join(faltam))
    print(f"Casos de uso registrados: {len(dados['casos'])}")

def main():
    p = argparse.ArgumentParser(description="Motor do Sextante")
    sub = p.add_subparsers(dest="cmd", required=True)

    a = sub.add_parser("nota"); a.add_argument("cliente"); a.add_argument("dim")
    a.add_argument("pergunta", type=int); a.add_argument("valor", type=int)
    a.add_argument("--obs", default=""); a.set_defaults(func=cmd_nota)

    a = sub.add_parser("caso"); a.add_argument("cliente"); a.add_argument("titulo")
    a.add_argument("--area", default=""); a.add_argument("--alcance", type=int, default=3)
    a.add_argument("--frequencia", type=int, default=3); a.add_argument("--dor", type=int, default=3)
    a.add_argument("--esforco", type=int, default=3); a.add_argument("--obs", default="")
    a.set_defaults(func=cmd_caso)

    for nome, fn in [("priorizar", cmd_priorizar), ("roadmap", cmd_roadmap),
                     ("relatorio", cmd_relatorio), ("resumo", cmd_resumo)]:
        a = sub.add_parser(nome); a.add_argument("cliente"); a.set_defaults(func=fn)

    args = p.parse_args()
    args.func(args)

if __name__ == "__main__":
    main()
