---
name: sextante
description: Diagnóstico de maturidade em IA de uma empresa inteira — para consultor, prestador de serviço ou dono avaliar a prontidão de um negócio em 6 dimensões, achar as oportunidades de maior retorno e montar um roadmap de adoção em ondas, num relatório apresentável. Use quando alguém disser "quero avaliar se minha empresa (ou a do meu cliente) está pronta para IA", "por onde uma empresa começa com IA", "diagnóstico de maturidade em IA", "monta um roadmap de IA para essa empresa", "assessment de IA", "qual o nível de IA desse negócio". NÃO é para uma única tarefa nem um único processo — é o retrato da organização toda.
---

# Sextante — Diagnóstico de Maturidade em IA de uma empresa

A Sextante ajuda um **consultor, prestador de serviço ou dono** a olhar uma empresa por inteiro e responder: _"quão pronta ela está para IA, onde a IA traz mais retorno e em que ordem adotar?"_. O resultado é um **relatório apresentável** — a oferta de entrada perfeita para quem ajuda empresas a adotar IA.

**Onde ela se encaixa (não confunda):** a Sextante é o retrato da **empresa inteira** (6 dimensões + roadmap em ondas). Ela NÃO mapeia as tarefas do próprio dono (isso é outra skill), NÃO destrincha um único processo, e NÃO executa um projeto pontual. Ela é o **assessment org-wide** que vem antes de tudo isso.

## Quando usar
- "Avaliar se a empresa/o cliente está pronto para IA", "diagnóstico/assessment de maturidade em IA".
- "Por onde essa empresa começa com IA", "monta um roadmap de IA".
- Consultor que quer um deliverable de diagnóstico para apresentar a um prospect.

## Primeira conversa (setup)
Se ainda existir o arquivo `SETUP.md` na pasta, siga-o UMA vez: colete nome/marca do consultor, tom e moeda, grave em `.sextante/config.json` e apague os arquivos de setup. Depois disso a skill está limpa.

## Modos (o consultor fala em português; você chama o motor por baixo)
Sempre trabalhe sobre um **cliente** nomeado. Chame o motor **sem trocar de diretório** (não use `cd`), pelo caminho da skill a partir da pasta do projeto, para que o estado `.sextante/` fique na raiz do projeto do usuário:
`python3 .claude/skills/Sextante/scripts/sextante.py <comando> "<cliente>" ...` (ou `~/.claude/skills/Sextante/scripts/sextante.py` se instalada global).

1. **Diagnóstico** — conduza a entrevista guiada por `references/rubrica.md` (6 dimensões, 30 perguntas, nota 0/1/2). Traduza cada pergunta para o mundo do cliente. Grave cada resposta com `nota`. Nunca invente — se o cliente não sabe, pergunte ou deixe em branco.
2. **Oportunidades** — use `references/casos-de-uso.md` para levantar, área por área, onde a IA pode entrar. Para cada uma capture alcance/frequência/dor/esforço (1-5) e grave com `caso`.
3. **Priorizar** — `python3 scripts/sextante.py priorizar "<cliente>"`: ranqueia por impacto/esforço em quadrantes (Ganho Rápido / Projeto / Talvez / Evite por ora). Se `dados` ou `governanca` tiverem nota baixa, o motor avisa que a base precisa vir antes.
4. **Roadmap** — `python3 scripts/sextante.py roadmap "<cliente>"`: monta as 3 ondas (90 dias / 3-6 meses / 6-12 meses) respeitando o estágio de prontidão. Nunca empurra IA avançada para quem está no estágio Iniciante.
5. **Relatório** — `python3 scripts/sextante.py relatorio "<cliente>"`: gera o documento apresentável (pontuação, estágio, prontidão por dimensão, elo mais fraco, top oportunidades, recomendação). Você pode enriquecer o texto para a apresentação — sem inventar dado.
6. **Resumo/Status** — `python3 scripts/sextante.py resumo "<cliente>"`: mostra o que já foi avaliado e o que falta.

## Estágios de maturidade (pontuação 0-60)
- **Iniciante** (0-24), **Explorando** (25-39), **Praticando** (40-51), **Escalando** (52-60).

## Regras de ouro
1. **Nunca inventa dado do cliente** — o que falta vira pergunta ou `[SUPOR — validar]`.
2. **Nunca automatiza processo quebrado ou sem base** — dados/governança fracos travam recomendação agressiva; conserte a base primeiro.
3. **Recomenda proporcional à prontidão** — o roadmap respeita o estágio.
4. **Esculpe e sugere; o consultor decide e apresenta** — a skill entrega o rascunho, não a palavra final.
5. **Dados locais** — tudo fica em `.sextante/` na máquina do usuário, git-ignored. Nada sai para fora.
6. **Português simples** — sem jargão; traduza tudo para o mundo do cliente.

## Entradas / Saídas
- **Entra:** respostas da entrevista + oportunidades levantadas (via conversa).
- **Sai:** `.sextante/<cliente>.json` (estado) + o relatório de diagnóstico e o roadmap em texto apresentável.

## Dependências
- Python 3 (só biblioteca padrão). Nenhuma API, chave ou serviço externo.
