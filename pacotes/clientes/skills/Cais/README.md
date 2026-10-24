# Cais — onboarding e intake de cliente novo

O **cais** é onde o cliente atraca: você recebe, carrega tudo que a viagem precisa
(contexto, documentos, acessos, combinado) e só então zarpa para a entrega. A Cais
cuida da **ponte entre o "sim" e o começo do trabalho** — os primeiros dias que
decidem se a relação começa com confiança ou com atrito.

Para donos de negócio de serviço — agências, clínicas, advogados, contadores,
consultores, freelancers. **Não exige nenhum conhecimento técnico:** você só
conversa em português; a skill faz o resto.

## O que ela faz (6 modos)

1. **Receber** — cadastra o cliente novo e monta a mensagem de boas-vindas (mata o
   "paguei e agora?").
2. **Levantar** — questionário de intake sob medida para o seu tipo de serviço.
3. **Reunir** — checklist de documentos & acessos + cobrança educada do que falta.
4. **Combinar** — o "combinado" de escopo & expectativas em linguagem simples
   (anti-scope-creep na origem).
5. **Largada** — pauta e briefing da reunião de kickoff.
6. **Painel** — prontidão de cada cliente (5 marcos, 🔴🟡🟢) e quem está travado.

## Como instalar

1. Baixe e descompacte o arquivo.
2. Copie a pasta `Cais` para dentro de `.claude/skills/` no seu projeto
   (ou em `~/.claude/skills/` para deixar disponível em qualquer pasta):
   ```
   .claude/skills/Cais/
   ```
3. Abra o Claude Code nesse projeto. Na primeira vez que você pedir algo de
   onboarding, a skill roda um **setup rápido** (5 perguntas) e já fica pronta.

## Como usar

É só conversar. Exemplos de frases que ativam a Cais:
- "Fechei um cliente novo, me ajuda a começar certo."
- "Monta um questionário de intake pra esse cliente."
- "Quais documentos eu peço pra começar?"
- "Faz o combinado de escopo pra não virar bagunça."
- "Prepara a reunião de kickoff."
- "Me mostra o painel de onboarding / quem tá travado."

A skill sugere as mensagens no seu tom; **quem envia ao cliente é você**.

## Princípios

- **Nunca inventa** dado do cliente, resposta ou documento — o que falta fica visível.
- **Você é quem envia** as mensagens (a skill só monta).
- **100% local e offline** — tudo fica em `.cais/` na sua máquina; nada sai daí.
- O "combinado" é alinhamento de expectativas em linguagem simples, **não é um
  contrato jurídico**.

## Onde ela se encaixa

Achar cliente → pipeline → contrato → **Cais (onboarding)** → entrega → retenção →
depoimento. A Cais é o elo que cuida do **começo da relação depois do "sim"**.

## Requisitos

- Claude Code.
- Python 3 (já vem no macOS e na maioria dos Linux) — usado só para a parte de
  contagem/organização, sem instalar nada.

---

Feito com carinho pela **Maestria Academy** para a comunidade Maestros da IA.
Licença MIT — use, adapte e compartilhe.
