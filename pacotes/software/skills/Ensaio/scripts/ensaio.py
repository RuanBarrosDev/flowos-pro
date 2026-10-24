#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Ensaio — ferramenta de apoio (somente biblioteca padrao do Python, sem internet).

Faz DUAS coisas, e so isso:
  1) detectar  -> inspeciona o projeto e sugere linguagem / framework de teste / comando de rodar.
  2) resumo    -> le a SAIDA de uma rodada de testes (um arquivo de texto que voce ja salvou) e
                  devolve um resumo em portugues (quantos passaram, quantos quebraram, quais).

Este script NUNCA roda os testes nem nenhum comando por conta propria. Quem executa os testes e o
Claude, pelo Bash; o script apenas LE arquivos e resume. Assim nada inesperado acontece na maquina
do dono.

Uso:
  python3 ensaio.py detectar [caminho-do-projeto]
  python3 ensaio.py resumo <arquivo-com-a-saida-dos-testes>
"""
import os
import re
import sys
import json

# --------------------------------------------------------------------------- #
# 1) DETECTAR
# --------------------------------------------------------------------------- #

def _ler(path):
    try:
        with open(path, encoding="utf-8", errors="ignore") as f:
            return f.read()
    except OSError:
        return ""

def detectar(raiz="."):
    raiz = os.path.abspath(raiz)
    achados = {
        "raiz": raiz,
        "linguagem": None,
        "gerenciador": None,
        "tipo_app": None,
        "frameworks_de_teste": [],
        "pastas_de_teste": [],
        "comando_sugerido": None,
        "ja_tem_teste": False,
        "observacoes": [],
    }

    tem = lambda nome: os.path.exists(os.path.join(raiz, nome))

    # ---- Node / JavaScript / TypeScript ----
    if tem("package.json"):
        achados["linguagem"] = "JavaScript/TypeScript"
        pkg_txt = _ler(os.path.join(raiz, "package.json"))
        try:
            pkg = json.loads(pkg_txt)
        except ValueError:
            pkg = {}
        deps = {}
        for chave in ("dependencies", "devDependencies"):
            deps.update(pkg.get(chave, {}) or {})
        if tem("pnpm-lock.yaml"):
            achados["gerenciador"] = "pnpm"
        elif tem("yarn.lock"):
            achados["gerenciador"] = "yarn"
        else:
            achados["gerenciador"] = "npm"
        for fw, marca in (("Playwright", "@playwright/test"), ("Vitest", "vitest"),
                          ("Jest", "jest"), ("Cypress", "cypress"), ("Mocha", "mocha")):
            if marca in deps:
                achados["frameworks_de_teste"].append(fw)
        for fw, marca in (("React", "react"), ("Next.js", "next"), ("Vue", "vue"),
                          ("Express", "express"), ("Svelte", "svelte")):
            if marca in deps:
                achados["tipo_app"] = fw
                break
        scripts = pkg.get("scripts", {}) or {}
        if "test" in scripts:
            g = achados["gerenciador"]
            achados["comando_sugerido"] = f"{g} test" if g != "npm" else "npm test"

    # ---- Python ----
    elif tem("pyproject.toml") or tem("requirements.txt") or tem("setup.py"):
        achados["linguagem"] = "Python"
        achados["gerenciador"] = "pip"
        blob = _ler(os.path.join(raiz, "pyproject.toml")) + _ler(os.path.join(raiz, "requirements.txt"))
        if "pytest" in blob:
            achados["frameworks_de_teste"].append("Pytest")
            achados["comando_sugerido"] = "python3 -m pytest -q"
        else:
            achados["frameworks_de_teste"].append("unittest (padrao do Python)")
            achados["comando_sugerido"] = "python3 -m unittest -v"

    # ---- Go ----
    elif tem("go.mod"):
        achados["linguagem"] = "Go"
        achados["gerenciador"] = "go modules"
        achados["frameworks_de_teste"].append("go test (nativo)")
        achados["comando_sugerido"] = "go test ./..."

    # ---- Ruby ----
    elif tem("Gemfile"):
        achados["linguagem"] = "Ruby"
        achados["gerenciador"] = "bundler"
        blob = _ler(os.path.join(raiz, "Gemfile"))
        if "rspec" in blob.lower():
            achados["frameworks_de_teste"].append("RSpec")
            achados["comando_sugerido"] = "bundle exec rspec"

    # ---- PHP ----
    elif tem("composer.json"):
        achados["linguagem"] = "PHP"
        achados["gerenciador"] = "composer"
        achados["frameworks_de_teste"].append("PHPUnit (provavel)")
        achados["comando_sugerido"] = "./vendor/bin/phpunit"

    # ---- Site estatico (HTML puro) ----
    elif tem("index.html"):
        achados["linguagem"] = "HTML/CSS/JS (site estatico)"
        achados["tipo_app"] = "Site estatico"
        achados["observacoes"].append(
            "Sem gerenciador de pacotes: para testar comportamento, o caminho e um teste de tela "
            "(Playwright) rodando o site num navegador."
        )

    # ---- procurar pastas/arquivos de teste ----
    padroes_dir = {"tests", "test", "__tests__", "spec", "e2e", "cypress"}
    padroes_arq = re.compile(r"(\.test\.|\.spec\.|_test\.|(^|/)test_)", re.IGNORECASE)
    encontrados = set()
    for base, dirs, files in os.walk(raiz):
        # nao entrar em pastas pesadas/irrelevantes
        dirs[:] = [d for d in dirs if d not in {"node_modules", ".git", "dist", "build",
                                                ".venv", "venv", "vendor", ".next", "__pycache__"}]
        rel = os.path.relpath(base, raiz)
        nome_base = os.path.basename(base)
        if nome_base in padroes_dir and rel != ".":
            encontrados.add(rel)
        for fn in files:
            if padroes_arq.search(fn):
                encontrados.add(rel if rel != "." else fn)
    achados["pastas_de_teste"] = sorted(encontrados)[:20]
    achados["ja_tem_teste"] = bool(encontrados)

    if not achados["linguagem"]:
        achados["observacoes"].append(
            "Nao reconheci a tecnologia automaticamente. Pergunte ao dono como o app foi feito e "
            "como ele roda hoje."
        )
    if not achados["ja_tem_teste"]:
        achados["observacoes"].append(
            "Nenhum teste encontrado. Este projeto esta sem rede de seguranca — o modo Rede deve "
            "instalar o framework e cobrir os caminhos criticos."
        )
    return achados

def imprimir_deteccao(a):
    print("=" * 60)
    print("ENSAIO — o que encontrei no projeto")
    print("=" * 60)
    print(f"Pasta ............: {a['raiz']}")
    print(f"Linguagem ........: {a['linguagem'] or '(nao reconhecida)'}")
    print(f"Gerenciador ......: {a['gerenciador'] or '-'}")
    print(f"Tipo de app ......: {a['tipo_app'] or '(a confirmar com o dono)'}")
    print(f"Ja tem teste? ....: {'SIM' if a['ja_tem_teste'] else 'NAO'}")
    fws = ", ".join(a["frameworks_de_teste"]) or "(nenhum detectado)"
    print(f"Framework(s) .....: {fws}")
    print(f"Comando sugerido .: {a['comando_sugerido'] or '(a definir)'}")
    if a["pastas_de_teste"]:
        print("Testes em ........: " + ", ".join(a["pastas_de_teste"]))
    if a["observacoes"]:
        print("\nObservacoes:")
        for o in a["observacoes"]:
            print(f"  - {o}")
    print("\n(JSON abaixo para uso do Claude)")
    print(json.dumps(a, ensure_ascii=False))


# --------------------------------------------------------------------------- #
# 2) RESUMO da saida de testes
# --------------------------------------------------------------------------- #

# Cada padrao devolve (passaram, quebraram, pulados) quando casa. None = campo desconhecido.
def _resumir_texto(txt):
    linhas_falha = []

    passaram = quebraram = pulados = None

    # Jest/Vitest:  "Tests: 1 failed, 2 skipped, 20 passed, 23 total"  (tem o prefixo "Tests:")
    j = re.search(r"Tests?:\s+.*?\bpassed", txt)
    # Pytest / generico:  conta CADA campo de forma independente, sem depender da ordem.
    # (a ordem "passed" antes de "failed" causava falso-verde — nunca mais.)
    def _campo(nome):
        mm = re.search(r"(\d+)\s+" + nome, txt)
        return int(mm.group(1)) if mm else None
    pyt_passed = _campo(r"passed")
    pyt_failed = _campo(r"failed")
    pyt_skipped = _campo(r"skipped")
    pyt_errors = _campo(r"errors?")

    # Go:  contagem de "--- FAIL:" e "--- PASS:"
    go_fail = len(re.findall(r"^--- FAIL:", txt, re.MULTILINE))
    go_pass = len(re.findall(r"^--- PASS:", txt, re.MULTILINE))

    if j:
        # dentro da linha do Jest, campos independentes tambem
        linha = txt[j.start(): txt.find("\n", j.start()) if txt.find("\n", j.start()) != -1 else len(txt)]
        gp = re.search(r"(\d+)\s+passed", linha)
        gf = re.search(r"(\d+)\s+failed", linha)
        gs = re.search(r"(\d+)\s+skipped", linha)
        passaram = int(gp.group(1)) if gp else 0
        quebraram = int(gf.group(1)) if gf else 0
        pulados = int(gs.group(1)) if gs else 0
    elif pyt_passed is not None or pyt_failed is not None:
        passaram = pyt_passed or 0
        quebraram = (pyt_failed or 0) + (pyt_errors or 0)
        pulados = pyt_skipped or 0
    elif go_pass or go_fail:
        passaram = go_pass
        quebraram = go_fail

    # nomes dos testes que falharam (varios formatos), ancorados na linha para nao
    # pegar o token errado entre linhas.
    for pat in (r"^FAILED\s+(\S+)",                 # pytest (resumo curto): "FAILED path::teste"
                r"^(\S+::\S+)\s+FAILED\b",           # pytest (verboso): "path::teste FAILED"
                r"^--- FAIL:\s+(\S+)",               # go: "--- FAIL: TestNome"
                r"^\s*[×✕✗✖]\s+(.+?)\s*$"):          # jest/vitest: simbolo de falha + nome
        for mm in re.finditer(pat, txt, re.MULTILINE):
            nome = mm.group(1).strip()
            # ignora rotulos que nao sao nome de teste
            if nome and nome.upper() not in {"FAILED", "FAIL", "PASS", "PASSED"} \
                    and nome not in linhas_falha:
                linhas_falha.append(nome)

    # sinal de "nada rodou" (vermelho disfarcado de verde)
    nada_rodou = bool(re.search(r"\b0 (tests?|passed)\b", txt)) or re.search(
        r"No tests? (found|ran|collected)", txt, re.IGNORECASE)

    return passaram, quebraram, pulados, linhas_falha[:30], bool(nada_rodou)

def imprimir_resumo(caminho):
    if not os.path.exists(caminho):
        print(f"ERRO: nao achei o arquivo '{caminho}'. Salve a saida da rodada de testes num "
              f"arquivo de texto e passe o caminho dele.")
        return 2
    txt = _ler(caminho)
    passaram, quebraram, pulados, falhas, nada_rodou = _resumir_texto(txt)

    print("=" * 60)
    print("ENSAIO — resumo da rodada de testes")
    print("=" * 60)

    if nada_rodou and not passaram and not quebraram:
        print("ATENCAO: parece que NENHUM teste rodou de verdade.")
        print("Isso e vermelho disfarcado de verde — nao declare 'passou'. Verifique o comando,")
        print("filtros ligados (.only/skip) ou a pasta de testes antes de seguir.")
        return 1

    if passaram is None and quebraram is None:
        print("Nao consegui reconhecer o formato desta saida automaticamente.")
        print("Leia o texto manualmente e conte passaram/quebraram — nao chute um resultado verde.")
        return 1

    p = passaram or 0
    q = quebraram or 0
    sk = pulados or 0
    total = p + q + sk
    print(f"Passaram .....: {p}")
    print(f"QUEBRARAM ....: {q}")
    if sk:
        print(f"Pulados ......: {sk}")
    print(f"Total ........: {total}")
    print("-" * 60)
    if q == 0:
        print("VEREDITO: tudo verde. As protecoes conferidas passaram nesta rodada.")
        print("(Lembre: verde so vale se os testes sao capazes de falhar — regra de ouro nº 1.)")
    else:
        print(f"VEREDITO: {q} protecao(oes) QUEBROU(RAM). NAO suba nada com vermelho.")
        if falhas:
            print("O que quebrou:")
            for f in falhas:
                print(f"  - {f}")
        print("Para o dono: traduza cada falha para o COMPORTAMENTO que parou de funcionar")
        print("(ex.: 'o calculo do total do carrinho parou de somar o frete'), diga a causa")
        print("provavel e o caminho mais seguro de consertar.")
    return 0


# --------------------------------------------------------------------------- #
def main():
    if len(sys.argv) < 2 or sys.argv[1] in ("-h", "--help", "ajuda"):
        print(__doc__)
        return 0
    cmd = sys.argv[1]
    if cmd == "detectar":
        raiz = sys.argv[2] if len(sys.argv) > 2 else "."
        imprimir_deteccao(detectar(raiz))
        return 0
    if cmd == "resumo":
        if len(sys.argv) < 3:
            print("Uso: python3 ensaio.py resumo <arquivo-com-a-saida-dos-testes>")
            return 2
        return imprimir_resumo(sys.argv[2])
    print(f"Comando desconhecido: {cmd}\n")
    print(__doc__)
    return 2

if __name__ == "__main__":
    raise SystemExit(main())
