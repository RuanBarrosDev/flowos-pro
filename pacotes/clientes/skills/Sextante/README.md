# Sextante 🧭

**Diagnóstico de maturidade em IA de uma empresa inteira.** Você conversa em português; a Sextante avalia a prontidão do negócio em 6 dimensões, encontra as oportunidades de maior retorno e monta um roadmap de adoção em ondas — tudo num relatório pronto para apresentar.

Feita para **consultores, prestadores de serviço e donos** que querem responder: _"essa empresa está pronta para IA? Por onde ela começa?"_.

## O que ela faz
- **Diagnóstico** — entrevista guiada (6 dimensões, 30 perguntas, nota 0/1/2) → pontuação e estágio de maturidade.
- **Oportunidades** — levanta, área por área, onde a IA entra, com nota de impacto e esforço.
- **Priorizar** — ranqueia em quadrantes (Ganho Rápido / Projeto / Talvez / Evite por ora).
- **Roadmap** — 3 ondas (90 dias / 3-6 meses / 6-12 meses) respeitando a prontidão.
- **Relatório** — o documento apresentável para o cliente.

## Instalar
1. Descompacte a pasta `Sextante`.
2. Coloque-a dentro da sua pasta de skills do Claude Code: `.claude/skills/Sextante` (no projeto) ou `~/.claude/skills/Sextante` (global).
3. Abra o Claude Code e diga algo como: _"quero fazer o diagnóstico de maturidade em IA da empresa X"_.

Na primeira vez, a skill faz uma configuração rápida (seu nome/marca, tom, moeda) e depois se limpa sozinha.

## Como usar
Fale naturalmente. Exemplos:
- _"Vamos avaliar se a Padaria Sol está pronta para IA."_
- _"Levanta as oportunidades de IA por área nessa empresa."_
- _"Prioriza e monta o roadmap."_
- _"Gera o relatório para eu apresentar."_

## Privacidade
Tudo fica na sua máquina, em `.sextante/` (ignorado pelo git). Nada é enviado para fora. Nenhuma chave ou API necessária — só Python 3.

## Golden rules
Nunca inventa dado do cliente · nunca automatiza processo quebrado ou sem base · recomenda proporcional à prontidão · você decide e apresenta · dados locais · português simples.

## Licença
MIT — use, adapte e distribua livremente.
