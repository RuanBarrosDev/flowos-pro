#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Instalação de primeira execução da Maquete.

Roda UMA vez, na primeira conversa. Coleta duas informações simples do dono
(como quer ser chamado e a plataforma padrão dos protótipos), grava a
configuração local em `.maquete/config.md` (fora do controle de versão),
garante que a pasta `.maquete/` está no `.gitignore` e, no fim, se autodestrói
— deixando a skill instalada limpa, sem arquivos de setup.

Não coleta nenhuma senha nem chave de API — a Maquete é 100% offline.
Uso:
    python3 setup/instalar.py --dono "Nome" --plataforma "web"
Qualquer campo omitido usa um padrão seguro e pode ser ajustado depois no config.
"""

import os
import sys
import shutil
import argparse


def find_root(start):
    """Sobe a árvore procurando .git/.claude; senão usa o cwd."""
    env = os.environ.get("CLAUDE_PROJECT_DIR")
    if env and os.path.isdir(env):
        return os.path.abspath(env)
    walk = os.path.abspath(start)
    while True:
        if os.path.isdir(os.path.join(walk, ".git")) or os.path.isdir(os.path.join(walk, ".claude")):
            return walk
        parent = os.path.dirname(walk)
        if parent == walk:
            return os.path.abspath(start)
        walk = parent


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dono", default="")
    ap.add_argument("--plataforma", default="")
    args = ap.parse_args()

    here = os.path.dirname(os.path.abspath(__file__))
    skill_root = os.path.dirname(here)          # pasta da skill (Maquete/)
    project_root = find_root(os.getcwd())
    mdir = os.path.join(project_root, ".maquete")
    os.makedirs(mdir, exist_ok=True)

    # 1) inicializa a estrutura via motor (cria CSVs + projeto)
    engine = os.path.join(skill_root, "scripts", "maquete.py")
    try:
        import subprocess
        subprocess.run([sys.executable, engine, "init"], cwd=project_root,
                       check=False, capture_output=True)
    except Exception:
        pass  # o motor também cria a estrutura sob demanda

    # 2) grava a configuração local (git-ignored)
    dono = args.dono.strip() or "[A CONFERIR]"
    plataforma = (args.plataforma.strip() or "web").lower()
    if plataforma not in ("web", "mobile", "desktop"):
        plataforma = "web"
    cfg_path = os.path.join(mdir, "config.md")
    with open(cfg_path, "w", encoding="utf-8") as f:
        f.write("# Configuração da Maquete (local — não versionar)\n\n")
        f.write("- **Dono:** %s\n" % dono)
        f.write("- **Plataforma padrão dos protótipos:** %s (web / mobile / desktop)\n" % plataforma)
        f.write("\n"
                "> A Maquete nunca inventa conteúdo real. O que o dono não disser vira "
                "[A CONFERIR] ou um rótulo genérico até ele confirmar.\n")

    # 3) garante .maquete/ no .gitignore
    gi = os.path.join(project_root, ".gitignore")
    linhas = []
    if os.path.exists(gi):
        with open(gi, encoding="utf-8") as f:
            linhas = f.read().splitlines()
    precisa = [p for p in (".maquete/",) if p not in linhas]
    if precisa:
        with open(gi, "a", encoding="utf-8") as f:
            if linhas and linhas[-1].strip():
                f.write("\n")
            f.write("# Maquete — dados locais do design (fluxos, telas, protótipos)\n")
            for p in precisa:
                f.write(p + "\n")

    print("✓ Maquete instalada.")
    print("  Configuração: %s" % cfg_path)
    print("  Dados locais protegidos no .gitignore (.maquete/).")

    # 4) autodestruição da pasta setup/
    try:
        shutil.rmtree(here)
        print("  Setup concluído e removido — a skill está limpa e pronta para usar.")
    except Exception as e:
        print("  (Aviso: não consegui remover a pasta setup/ automaticamente: %s)" % e)
        print("  Pode apagá-la manualmente — não é mais necessária.")


if __name__ == "__main__":
    main()
