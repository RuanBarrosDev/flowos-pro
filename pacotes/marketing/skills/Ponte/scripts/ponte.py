#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ponte.py — gerência local da Ponte (config + glossário + registro de trabalhos).

Sem dependências externas (só biblioteca padrão). Nunca acessa a internet.
Guarda tudo em ./.ponte/ no diretório de onde você roda o comando.

Uso:
  python3 scripts/ponte.py init --idioma en --mercado "Estados Unidos" --tom conversacional \
      --tratamento informal --moeda-origem BRL --moeda-destino USD \
      --marca "Minha Marca" --produto "Meu Produto" --regulada ""
  python3 scripts/ponte.py ver
  python3 scripts/ponte.py add-nao-traduzir "UTXO" "MinhaMarca"
  python3 scripts/ponte.py add-termo --origem "agendamento" --destino "booking" --contexto "botão" --confianca alta
  python3 scripts/ponte.py add-nome --origem "João Silva" --destino "João Silva" --tipo pessoa
  python3 scripts/ponte.py set-voz --registro marketing --publico "donos de e-commerce" --pessoa "você"
  python3 scripts/ponte.py set-concorrentes "Acme" "Globex"
  python3 scripts/ponte.py log-trabalho --tipo transcriar --titulo "Página de vendas" --origem-arq page.pt.md --destino-arq page.en.md
"""

import argparse
import json
import os
import sys
from datetime import datetime, timezone

DIR = os.path.join(os.getcwd(), ".ponte")
CONFIG = os.path.join(DIR, "config.json")
GLOSS = os.path.join(DIR, "glossario.json")
WORKS = os.path.join(DIR, "trabalhos")


def _now():
    return datetime.now(timezone.utc).strftime("%Y-%m-%d")


def _load(path, default):
    if not os.path.exists(path):
        return default
    try:
        with open(path, encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, OSError):
        return default


def _save(path, data):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
        f.write("\n")


def cmd_init(a):
    if os.path.exists(CONFIG):
        print("A pasta .ponte/ já existe. Nada foi sobrescrito. Use 'ver' para inspecionar ou os comandos "
              "'set-voz'/'add-termo' para ajustar.")
        return 0
    os.makedirs(WORKS, exist_ok=True)
    config = {
        "criado_em": _now(),
        "idioma_origem": "pt-BR",
        "idioma_alvo": a.idioma,
        "mercado_alvo": a.mercado,
        "moeda_origem": a.moeda_origem,
        "moeda_destino": a.moeda_destino,
        "area_regulada": [x.strip() for x in (a.regulada or "").split(",") if x.strip()],
        "concorrentes_alvo": [],
    }
    nao_traduzir = []
    for v in (a.marca, a.produto):
        if v and v.strip():
            nao_traduzir.append(v.strip())
    glossario = {
        "voz": {
            "registro": a.tom,
            "publico": "",
            "pessoa": a.tratamento,
            "pontuacao": "natural do idioma-alvo",
            "proibidos": [
                "buzzwords vazias (seamless, cutting-edge, world-class)",
                "urgência falsa (act now, don't miss out)",
                "ponto de exclamação em rótulos/botões",
            ],
        },
        "nao_traduzir": nao_traduzir,
        "termos": [],
        "nomes_proprios": [],
    }
    _save(CONFIG, config)
    _save(GLOSS, glossario)
    print("Ponte configurada. Criados:")
    print("  .ponte/config.json")
    print("  .ponte/glossario.json")
    print("  .ponte/trabalhos/")
    return cmd_ver(a)


def cmd_ver(_a):
    config = _load(CONFIG, None)
    gloss = _load(GLOSS, None)
    if not config:
        print("Ainda não configurado. Rode o setup (setup/PRIMEIRA-EXECUCAO.md) ou 'ponte.py init'.")
        return 1
    print("=== Ponte — configuração atual ===")
    print(f"  Idioma-alvo : {config.get('idioma_alvo')}  ({config.get('mercado_alvo')})")
    print(f"  Moeda       : {config.get('moeda_origem')} -> {config.get('moeda_destino')}")
    reg = config.get("area_regulada") or []
    print(f"  Área regulada: {', '.join(reg) if reg else 'nenhuma'}")
    conc = config.get("concorrentes_alvo") or []
    print(f"  Concorrentes: {', '.join(conc) if conc else '(nenhum cadastrado)'}")
    if gloss:
        voz = gloss.get("voz", {})
        print("  --- voz da marca ---")
        print(f"    registro: {voz.get('registro')}  | pessoa: {voz.get('pessoa')}")
        nt = gloss.get("nao_traduzir") or []
        print(f"  Não-traduzir: {', '.join(nt) if nt else '(vazio)'}")
        print(f"  Termos fixos: {len(gloss.get('termos') or [])}   Nomes próprios: {len(gloss.get('nomes_proprios') or [])}")
    n = len(os.listdir(WORKS)) if os.path.isdir(WORKS) else 0
    print(f"  Trabalhos salvos: {n}")
    return 0


def _require():
    if not os.path.exists(GLOSS):
        print("Ainda não configurado. Rode 'ponte.py init' primeiro.")
        sys.exit(1)


def cmd_add_nao_traduzir(a):
    _require()
    g = _load(GLOSS, {})
    lst = g.setdefault("nao_traduzir", [])
    for t in a.termos:
        if t not in lst:
            lst.append(t)
    _save(GLOSS, g)
    print(f"Não-traduzir agora: {', '.join(lst)}")
    return 0


def cmd_add_termo(a):
    _require()
    g = _load(GLOSS, {})
    termos = g.setdefault("termos", [])
    termos.append({
        "origem": a.origem,
        "destino": a.destino,
        "contexto": a.contexto or "",
        "confianca": a.confianca or "media",
    })
    _save(GLOSS, g)
    print(f"Termo adicionado: '{a.origem}' -> '{a.destino}'  ({len(termos)} no total)")
    return 0


def cmd_add_nome(a):
    _require()
    g = _load(GLOSS, {})
    nomes = g.setdefault("nomes_proprios", [])
    nomes.append({"origem": a.origem, "destino": a.destino, "tipo": a.tipo or "outro"})
    _save(GLOSS, g)
    print(f"Nome próprio adicionado: '{a.origem}' -> '{a.destino}'  ({len(nomes)} no total)")
    return 0


def cmd_set_voz(a):
    _require()
    g = _load(GLOSS, {})
    voz = g.setdefault("voz", {})
    if a.registro:
        voz["registro"] = a.registro
    if a.publico:
        voz["publico"] = a.publico
    if a.pessoa:
        voz["pessoa"] = a.pessoa
    _save(GLOSS, g)
    print("Voz atualizada:", json.dumps(voz, ensure_ascii=False))
    return 0


def cmd_set_concorrentes(a):
    if not os.path.exists(CONFIG):
        print("Ainda não configurado. Rode 'ponte.py init' primeiro.")
        return 1
    c = _load(CONFIG, {})
    c["concorrentes_alvo"] = list(a.nomes)
    _save(CONFIG, c)
    print(f"Concorrentes-alvo: {', '.join(a.nomes)}")
    return 0


def cmd_log_trabalho(a):
    _require()
    os.makedirs(WORKS, exist_ok=True)
    existing = [x for x in os.listdir(WORKS) if x.endswith(".json")]
    idx = len(existing) + 1
    safe = "".join(ch if ch.isalnum() else "-" for ch in (a.titulo or "trabalho")).strip("-").lower()[:40]
    fname = f"{idx:03d}-{safe or 'trabalho'}.json"
    _save(os.path.join(WORKS, fname), {
        "data": _now(),
        "tipo": a.tipo,
        "titulo": a.titulo,
        "origem_arq": a.origem_arq or "",
        "destino_arq": a.destino_arq or "",
    })
    print(f"Trabalho registrado: .ponte/trabalhos/{fname}")
    return 0


def build_parser():
    p = argparse.ArgumentParser(description="Gerência local da Ponte (config + glossário).")
    sub = p.add_subparsers(dest="cmd", required=True)

    pi = sub.add_parser("init", help="cria .ponte/ com config e glossário")
    pi.add_argument("--idioma", required=True)
    pi.add_argument("--mercado", required=True)
    pi.add_argument("--tom", default="conversacional")
    pi.add_argument("--tratamento", default="informal")
    pi.add_argument("--moeda-origem", dest="moeda_origem", default="BRL")
    pi.add_argument("--moeda-destino", dest="moeda_destino", required=True)
    pi.add_argument("--marca", default="")
    pi.add_argument("--produto", default="")
    pi.add_argument("--regulada", default="")
    pi.set_defaults(func=cmd_init)

    sub.add_parser("ver", help="mostra a configuração atual").set_defaults(func=cmd_ver)

    pnt = sub.add_parser("add-nao-traduzir", help="adiciona termos que NÃO se traduzem")
    pnt.add_argument("termos", nargs="+")
    pnt.set_defaults(func=cmd_add_nao_traduzir)

    pt = sub.add_parser("add-termo", help="adiciona um termo fixo origem->destino")
    pt.add_argument("--origem", required=True)
    pt.add_argument("--destino", required=True)
    pt.add_argument("--contexto", default="")
    pt.add_argument("--confianca", default="media", choices=["alta", "media", "baixa"])
    pt.set_defaults(func=cmd_add_termo)

    pn = sub.add_parser("add-nome", help="adiciona um nome próprio verificado")
    pn.add_argument("--origem", required=True)
    pn.add_argument("--destino", required=True)
    pn.add_argument("--tipo", default="outro", choices=["pessoa", "empresa", "lugar", "produto", "orgao", "outro"])
    pn.set_defaults(func=cmd_add_nome)

    pv = sub.add_parser("set-voz", help="ajusta a voz da marca")
    pv.add_argument("--registro", default="")
    pv.add_argument("--publico", default="")
    pv.add_argument("--pessoa", default="")
    pv.set_defaults(func=cmd_set_voz)

    pc = sub.add_parser("set-concorrentes", help="define os concorrentes do mercado-alvo")
    pc.add_argument("nomes", nargs="+")
    pc.set_defaults(func=cmd_set_concorrentes)

    pl = sub.add_parser("log-trabalho", help="registra uma transcriação feita")
    pl.add_argument("--tipo", required=True)
    pl.add_argument("--titulo", required=True)
    pl.add_argument("--origem-arq", dest="origem_arq", default="")
    pl.add_argument("--destino-arq", dest="destino_arq", default="")
    pl.set_defaults(func=cmd_log_trabalho)

    return p


def main():
    parser = build_parser()
    args = parser.parse_args()
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
