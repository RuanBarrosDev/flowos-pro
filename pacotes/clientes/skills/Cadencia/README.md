# Cadência — sua receita recorrente, previsível

Uma skill de Claude Code que ajuda o dono de negócio a **modelar e fazer crescer a receita recorrente**
(mensalidades, assinaturas, fee mensal, planos). Responde, em português claro: **minha receita é
previsível? está crescendo ou vazando? quanto vale um cliente? com esse ritmo, onde eu chego?**

Você só conversa em português. Por baixo, o Claude usa um motor local (Python, sem internet) que guarda
tudo no seu computador e **nunca inventa um número**.

## O que ela faz
- **MRR e a "ponte do mês"** — quanto de receita se repete, e como ela mudou (clientes novos, upgrades,
  downgrades, cancelamentos, reativações) numa conta que **sempre fecha**.
- **Churn de clientes e de receita** — as duas formas de medir cancelamento, lado a lado, com o alerta
  "seus clientes maiores estão indo embora".
- **Retenção e coortes** — GRR/NRR e onde, no tempo, as pessoas desistem.
- **Valor do cliente** — LTV, LTV:CAC e payback (em quantos meses o cliente se paga).
- **Previsão** — onde sua base chega em N meses + o teste "se eu parar de vender, quanto dura?".
- **Planos** — como desenhar faixas e por que o desconto errado mata a margem.

## O diferencial
Uma IA pedida pra "montar meu MRR" chuta cada número e a conta não bate. A Cadência usa um **livro-razão**:
cada evento (novo cliente, upgrade, cancelamento…) vira um lançamento, e o MRR é derivado dele — então a
identidade **MRR fim = início + novo + expansão − contração − churn + reativação** fecha por construção.
Você confia no número porque ele vem da conta, não do palpite.

## Instalação
1. Baixe e descompacte o arquivo. Você terá uma pasta chamada **`Cadência`**.
2. Coloque essa pasta dentro de `.claude/skills/` do seu projeto (ou em `~/.claude/skills/` para deixá-la
   disponível em qualquer projeto). O caminho final fica assim:
   ```
   .claude/skills/Cadência/
   ```
3. Abra o Claude Code nesse projeto e comece a conversar: **"quero organizar minha receita recorrente"**.
   Na primeira vez, o Claude conduz um setup rápido (nome do negócio, moeda, e — se você souber — margem
   e CAC) e já começa.

## Como usar (você só fala, o Claude faz)
- "Tenho 40 alunos no plano de R$ 149 por mês" → ele cadastra sua base.
- "O João subiu pro plano de R$ 299" → registra a expansão.
- "A Maria cancelou esse mês" → registra o churn.
- "Como foi meu mês?" → a ponte do MRR.
- "Quanto vale um cliente meu?" → LTV, CAC e payback.
- "Com esse ritmo, onde eu chego em um ano?" → a previsão.

## Privacidade
Tudo fica em `.cadencia/` na raiz do seu projeto, ignorado pelo Git. Nomes de clientes e receita **nunca
saem do seu computador** e nunca vão pra internet.

## Requisitos
- Claude Code
- Python 3 (já vem no macOS e na maioria dos Linux; no Windows, instale pela loja ou python.org)

## Licença
MIT — use, adapte e compartilhe à vontade. Veja `LICENSE`.
