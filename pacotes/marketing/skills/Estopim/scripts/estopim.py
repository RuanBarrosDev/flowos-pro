#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Estopim — motor de organização de campanha (somente biblioteca padrão do Python).

O motor NÃO cria conteúdo e NÃO inventa dado. Ele apenas organiza a pasta de trabalho
`.estopim/`, cria os arquivos a partir de modelos e imprime a rubrica do Crivo como
checklist. Toda a criação (briefing, insight, ideia, texto, parecer) é feita pela IA na
conversa; o motor só guarda e recupera.

Uso:
  python3 scripts/estopim.py init
  python3 scripts/estopim.py briefing "Nome da campanha"
  python3 scripts/estopim.py crivo
  python3 scripts/estopim.py status
"""

import sys
import os
from datetime import date

WORKDIR = ".estopim"

# ----------------------------------------------------------------------------- modelos

CONFIG_TEMPLATE = """# Configuração do Estopim — marca/negócio

> Preenchido na primeira conversa. A IA lê este arquivo para não perguntar o básico de novo.
> Onde faltar dado, mantenha o marcador de pendência no campo — nunca invente.

- **Marca/negócio:** [PREENCHER]
- **O que vende / entrega:** [PREENCHER]
- **Público que atende:** [PREENCHER]
- **Tom de voz (como a marca fala):** [PREENCHER]
- **Canais que usa:** [PREENCHER]
- **Concorrentes / referências:** [PREENCHER]
- **O que NUNCA pode aparecer (limites de marca):** [PREENCHER]
"""

BRIEFING_TEMPLATE = """# Briefing criativo — {campanha}
_Data: {hoje}_

## 1. Objetivo de negócio
[PREENCHER] — o que precisa acontecer no mundo real (com meta/número quando possível).

## 2. Público
- Quem é: [PREENCHER]
- O que pensa hoje: [PREENCHER]
- O que queremos que passe a pensar/fazer: [PREENCHER]

## 3. A promessa
[PREENCHER] — o que a marca entrega que importa para esse público.

## 4. Tom
[PREENCHER] — (herdar de config.md se existir)

## 5. Obrigatoriedades e limites
- Não pode faltar: [PREENCHER]
- Não pode aparecer: [PREENCHER]
- Prazo: [PREENCHER]
- Verba: [PREENCHER]
- Canais disponíveis: [PREENCHER]

## 6. Prova (por que acreditar)
[PREENCHER] — números, cases, garantia, autoridade.

## Frase única do briefing
> Esta campanha precisa fazer [público] [ação], porque [insight], e a marca prova isso com [prova].
"""

CONCEITO_TEMPLATE = """# Conceito — {campanha}

## Insight escolhido
> "Eu [desejo/medo], mas [barreira] — então [comportamento]."
[PREENCHER pela IA no modo Insight]

## Conceito A — [nome]
- **Plataforma:** [PREENCHER]
- **Por que funciona:** [PREENCHER]
- **Como se expressa:** [PREENCHER]

## Conceito B — [nome]
- **Plataforma:** [PREENCHER]
- **Por que funciona:** [PREENCHER]
- **Como se expressa:** [PREENCHER]

## Conceito C — [nome]
- **Plataforma:** [PREENCHER]
- **Por que funciona:** [PREENCHER]
- **Como se expressa:** [PREENCHER]

## Recomendação
[PREENCHER] — qual conceito seguir e por quê.
"""

CAMPANHA_TEMPLATE = """# Campanha — {campanha}

## Conceito escolhido
[PREENCHER]

## Desdobramento por canal
[PREENCHER pela IA no modo Desdobramento]

## Manifesto
[PREENCHER pela IA no modo Manifesto]

## Roteiros
[PREENCHER]

## Headlines
[PREENCHER]

## Parecer do Crivo
[PREENCHER pela IA no modo Crivo]
"""

CRIVO_EIXOS = [
    ("Na estratégia", "Atende o objetivo de negócio do briefing?"),
    ("Single-minded", "Diz UMA coisa com força, ou tenta dizer tudo?"),
    ("Distintivo", "Só essa marca poderia assinar, ou serve para qualquer concorrente?"),
    ("Apropriável (ownable)", "Sustenta várias peças e o tempo, ou morre num post?"),
    ("Verdadeiro", "A marca consegue entregar o que promete? (checar contra a prova)"),
    ("Claro para o público", "A pessoa entende em 3 segundos?"),
]


# ----------------------------------------------------------------------------- utilidades

def ensure_workdir():
    if not os.path.isdir(WORKDIR):
        os.makedirs(WORKDIR, exist_ok=True)


def write_if_absent(path, content):
    if os.path.exists(path):
        return False
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    return True


def ensure_gitignore():
    """Garante que .estopim/ está no .gitignore da pasta atual (contexto do cliente não vaza)."""
    line = ".estopim/"
    gi = ".gitignore"
    existing = ""
    if os.path.exists(gi):
        with open(gi, "r", encoding="utf-8") as f:
            existing = f.read()
    if line not in existing.split():
        with open(gi, "a", encoding="utf-8") as f:
            if existing and not existing.endswith("\n"):
                f.write("\n")
            f.write(line + "\n")


# ----------------------------------------------------------------------------- comandos

def cmd_init():
    ensure_workdir()
    ensure_gitignore()
    created = []
    if write_if_absent(os.path.join(WORKDIR, "config.md"), CONFIG_TEMPLATE):
        created.append("config.md")
    print("Pasta de trabalho .estopim/ pronta.")
    if created:
        print("Criados: " + ", ".join(created))
    else:
        print("Já existia — nada sobrescrito.")
    print("O .estopim/ foi adicionado ao .gitignore desta pasta.")


def cmd_briefing(nome):
    if not nome:
        print("Uso: python3 scripts/estopim.py briefing \"Nome da campanha\"")
        sys.exit(2)
    ensure_workdir()
    ensure_gitignore()
    hoje = date.today().isoformat()
    slug = "".join(c if c.isalnum() else "-" for c in nome.lower()).strip("-")
    files = {
        "briefing.md": BRIEFING_TEMPLATE.format(campanha=nome, hoje=hoje),
        "conceito.md": CONCEITO_TEMPLATE.format(campanha=nome),
        "campanha.md": CAMPANHA_TEMPLATE.format(campanha=nome),
    }
    for fname, content in files.items():
        write_if_absent(os.path.join(WORKDIR, fname), content)
    print(f"Campanha \"{nome}\" iniciada (slug: {slug}).")
    print("Arquivos prontos em .estopim/: briefing.md, conceito.md, campanha.md")
    print("Agora a IA preenche cada [PREENCHER] com o conteúdo real da conversa — sem inventar dado.")


def cmd_crivo():
    print("=" * 68)
    print("CRIVO — rubrica de avaliação do conceito (cada eixo 0 a 5)")
    print("=" * 68)
    for i, (eixo, pergunta) in enumerate(CRIVO_EIXOS, 1):
        print(f"\n{i}. {eixo}   [ __ /5 ]")
        print(f"   {pergunta}")
    total = len(CRIVO_EIXOS) * 5
    print("\n" + "-" * 68)
    print(f"SOMA: ____ / {total}")
    print("Veredito:  >= {a}  Aprovado   |   {b}-{c}  Ajustar   |   < {b}  Refazer".format(
        a=int(total * 0.8), b=int(total * 0.6), c=int(total * 0.8) - 1))
    print("Depois liste as LACUNAS ordenadas por impacto, cada uma com a correção concreta.")
    print("(O julgamento é da IA/seu; o motor só formata o checklist.)")


def cmd_status():
    if not os.path.isdir(WORKDIR):
        print("Nenhuma campanha iniciada aqui. Rode: python3 scripts/estopim.py init")
        return
    etapas = [
        ("config.md", "Configuração da marca"),
        ("briefing.md", "Briefing criativo"),
        ("conceito.md", "Insight + conceitos"),
        ("campanha.md", "Desdobramento + manifesto + Crivo"),
    ]
    print("Estado da campanha nesta pasta:")
    for fname, label in etapas:
        path = os.path.join(WORKDIR, fname)
        if not os.path.exists(path):
            mark = "· não criado"
        else:
            txt = open(path, encoding="utf-8").read()
            pend = txt.count("[PREENCHER]")
            mark = "OK (sem pendências)" if pend == 0 else f"{pend} campo(s) [PREENCHER] pendente(s)"
        print(f"  - {label}: {mark}")


def main():
    args = sys.argv[1:]
    if not args:
        print(__doc__)
        sys.exit(0)
    cmd = args[0]
    if cmd == "init":
        cmd_init()
    elif cmd == "briefing":
        cmd_briefing(args[1] if len(args) > 1 else "")
    elif cmd == "crivo":
        cmd_crivo()
    elif cmd == "status":
        cmd_status()
    else:
        print(f"Comando desconhecido: {cmd}")
        print(__doc__)
        sys.exit(2)


if __name__ == "__main__":
    main()
