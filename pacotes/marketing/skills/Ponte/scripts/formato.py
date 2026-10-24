#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
formato.py — detecta moeda, unidade, data e número num texto em PT-BR e sugere como localizar
para o mercado-alvo. Só biblioteca padrão, 100% offline. NUNCA inventa câmbio: onde o valor
depende da cotação do dia, marca "⚠️ CONFIRMAR" para o dono preencher.

Uso:
  python3 scripts/formato.py "O plano custa R$ 2.000,00, o produto pesa 3 kg e a entrega é 12/07/2026."
  python3 scripts/formato.py --alvo en-US "custa R$ 49,90 por mês"    # ajusta as dicas de formato ao alvo

Saída: uma lista de achados, cada um com o trecho, o tipo e a sugestão de localização.
"""

import argparse
import re
import sys

# Convenções de formato por mercado (número/data). Moeda e unidade viram sempre "⚠️ CONFIRMAR"
# porque dependem de câmbio/preferência do dono — a ferramenta nunca chuta cotação.
ALVOS = {
    "en-US": {"decimal": ".", "milhar": ",", "data": "MM/DD/YYYY", "unidade": "imperial (lb, mi, °F)"},
    "en-GB": {"decimal": ".", "milhar": ",", "data": "DD/MM/YYYY", "unidade": "misto (kg mas mi, °C)"},
    "es-419": {"decimal": ".", "milhar": ",", "data": "DD/MM/YYYY", "unidade": "métrico (kg, km, °C)"},
    "es-ES": {"decimal": ",", "milhar": ".", "data": "DD/MM/YYYY", "unidade": "métrico (kg, km, °C)"},
    "pt-PT": {"decimal": ",", "milhar": ".", "data": "DD/MM/YYYY", "unidade": "métrico (kg, km, °C)"},
    "fr-FR": {"decimal": ",", "milhar": " ", "data": "DD/MM/YYYY", "unidade": "métrico (kg, km, °C)"},
    "de-DE": {"decimal": ",", "milhar": ".", "data": "DD.MM.YYYY", "unidade": "métrico (kg, km, °C)"},
    "it-IT": {"decimal": ",", "milhar": ".", "data": "DD/MM/YYYY", "unidade": "métrico (kg, km, °C)"},
}

MESES = ("jan", "fev", "mar", "abr", "mai", "jun", "jul", "ago", "set", "out", "nov", "dez")


def achar(texto, alvo):
    cfg = ALVOS.get(alvo, ALVOS["en-US"])
    achados = []

    # Moeda: R$ 1.234,56  |  R$1234  |  reais
    for m in re.finditer(r"R\$\s?\d[\d\.\,]*", texto):
        achados.append((m.group(0), "MOEDA",
                        f"Converter para {cfg_moeda(alvo)} — ⚠️ CONFIRMAR o valor (depende do câmbio do dia "
                        f"e do preço que você quer praticar no mercado-alvo)."))
    if re.search(r"\breais?\b", texto, re.I):
        achados.append(("reais", "MOEDA", "Trocar a palavra 'reais' pela moeda-alvo. ⚠️ CONFIRMAR o valor."))

    # Unidades métricas comuns
    for m in re.finditer(r"\b\d+(?:[\.,]\d+)?\s?(kg|g|km|m|cm|litros?|l|°C)\b", texto, re.I):
        achados.append((m.group(0), "UNIDADE",
                        f"Se o mercado-alvo usa {cfg['unidade']}, converter a unidade. "
                        f"⚠️ CONFIRMAR o número convertido."))

    # Datas numéricas dd/mm/aaaa ou dd/mm
    for m in re.finditer(r"\b(\d{1,2})/(\d{1,2})(?:/(\d{2,4}))?\b", texto):
        achados.append((m.group(0), "DATA",
                        f"Reescrever no formato {cfg['data']} do mercado-alvo (cuidado: dd/mm vira mm/dd em en-US)."))
    # Datas por extenso em PT (12 de julho)
    for m in re.finditer(r"\b\d{1,2}\s+de\s+[a-zç]+", texto, re.I):
        achados.append((m.group(0), "DATA", "Reescrever a data por extenso no idioma-alvo."))

    # Números grandes no padrão PT (1.234,56) — sinaliza inversão de separadores
    for m in re.finditer(r"\b\d{1,3}(?:\.\d{3})+(?:,\d+)?\b", texto):
        achados.append((m.group(0), "NÚMERO",
                        f"Padrão PT (milhar '.', decimal ','). No alvo use milhar '{cfg['milhar']}' e "
                        f"decimal '{cfg['decimal']}'."))

    # Telefone BR
    for m in re.finditer(r"\(?\d{2}\)?\s?9?\d{4}[-\s]?\d{4}", texto):
        achados.append((m.group(0), "TELEFONE",
                        "Acrescentar o código do país (+55) ou trocar por um contato local. ⚠️ CONFIRMAR."))

    return achados


def cfg_moeda(alvo):
    return {
        "en-US": "US$ (dólar americano)",
        "en-GB": "£ (libra)",
        "es-419": "moeda local (US$/MXN/ARS...) — ⚠️ definir",
        "es-ES": "€ (euro)",
        "pt-PT": "€ (euro)",
        "fr-FR": "€ (euro)",
        "de-DE": "€ (euro)",
        "it-IT": "€ (euro)",
    }.get(alvo, "a moeda do mercado-alvo")


def main():
    p = argparse.ArgumentParser(description="Detecta moeda/unidade/data/número e sugere localização.")
    p.add_argument("texto", nargs="?", help="o texto a inspecionar (entre aspas)")
    p.add_argument("--alvo", default="en-US", choices=list(ALVOS.keys()),
                   help="mercado-alvo para as convenções de formato (padrão en-US)")
    a = p.parse_args()

    texto = a.texto
    if not texto:
        texto = sys.stdin.read()
    if not texto or not texto.strip():
        print("Passe um texto entre aspas. Ex.: python3 scripts/formato.py \"custa R$ 2.000 e pesa 3 kg\"")
        return 1

    achados = achar(texto, a.alvo)
    if not achados:
        print("Nenhuma moeda/unidade/data/número que precise de localização foi encontrada.")
        return 0

    print(f"=== Formatos a localizar (mercado-alvo: {a.alvo}) ===")
    for trecho, tipo, dica in achados:
        print(f"  [{tipo}] {trecho!r}\n      -> {dica}")
    print(f"\n{len(achados)} item(ns). Onde aparece '⚠️ CONFIRMAR', você decide o valor final.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
