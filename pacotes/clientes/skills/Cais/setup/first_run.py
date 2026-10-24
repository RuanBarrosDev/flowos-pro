#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Cais — setup de primeira execução.

Grava .cais/config.md na raiz do projeto com as preferências do dono, garante que
.cais/ esteja no .gitignore da raiz e, por fim, SE AUTODESTRÓI (apaga a pasta
setup/) para deixar a skill instalada limpa.

Roda uma única vez. Depois disto, o arquivo .cais/config.md existir é o sinal de
que o setup já foi feito.

Uso (a IA preenche a partir da conversa do SETUP.md):
    python3 <skill>/setup/first_run.py \\
        --nome "Maria Silva" --negocio "Consultoria de RH" \\
        --servico "Consultoria" --canal "WhatsApp" \\
        --tom "próximo e profissional" --resposta "até 1 dia útil"
"""

import argparse
import os
import shutil
import sys


def achar_raiz():
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


def garantir_gitignore(raiz):
    gi = os.path.join(raiz, ".gitignore")
    linha = ".cais/"
    existe = ""
    if os.path.exists(gi):
        with open(gi, encoding="utf-8") as f:
            existe = f.read()
        if linha in existe:
            return
    with open(gi, "a", encoding="utf-8") as f:
        if existe and not existe.endswith("\n"):
            f.write("\n")
        f.write("# Dados locais da skill Cais (onboarding de clientes)\n")
        f.write(linha + "\n")


def main():
    p = argparse.ArgumentParser(description="Setup de primeira execução da Cais.")
    p.add_argument("--nome", required=True, help="nome do dono")
    p.add_argument("--negocio", default="", help="nome/descrição do negócio")
    p.add_argument("--servico", default="", help="tipo de serviço principal")
    p.add_argument("--canal", default="WhatsApp", help="canal preferido de contato")
    p.add_argument("--tom", default="próximo e profissional", help="tom de voz")
    p.add_argument("--resposta", default="até 1 dia útil", help="tempo de resposta padrão")
    a = p.parse_args()

    raiz = achar_raiz()
    dir_cais = os.path.join(raiz, ".cais")
    os.makedirs(dir_cais, exist_ok=True)

    config = f"""# Configuração da Cais

Preferências do dono, usadas para personalizar as mensagens de onboarding.
Edite este arquivo à mão quando algo mudar.

- **Nome:** {a.nome}
- **Negócio:** {a.negocio or "[A PREENCHER]"}
- **Serviço principal:** {a.servico or "[A PREENCHER]"}
- **Canal preferido:** {a.canal}
- **Tom de voz:** {a.tom}
- **Tempo de resposta padrão:** {a.resposta}
"""
    caminho = os.path.join(dir_cais, "config.md")
    with open(caminho, "w", encoding="utf-8") as f:
        f.write(config)

    garantir_gitignore(raiz)

    print(f"✅ Configuração gravada em {caminho}")
    print(f"   .cais/ adicionado ao .gitignore da raiz ({raiz}).")

    # --- autodestruição da pasta setup/ ---
    setup_dir = os.path.dirname(os.path.abspath(__file__))
    if os.path.basename(setup_dir) == "setup":
        try:
            shutil.rmtree(setup_dir)
            print("🧹 Pasta setup/ removida — a skill está limpa e pronta para uso.")
        except Exception as e:
            print(f"(aviso: não consegui remover a pasta setup/ automaticamente: {e})")
            print(f" Pode apagá-la manualmente: {setup_dir}")
    print("\nTudo pronto! Agora é só usar a Cais normalmente.")


if __name__ == "__main__":
    main()
