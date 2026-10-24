---
name: cadencia
description: >-
  Modela e faz crescer a RECEITA RECORRENTE do negócio (assinatura, mensalidade, fee mensal, plano) —
  responde "minha receita é previsível? está crescendo ou vazando? quanto vale um cliente? onde chego
  em N meses?". Use quando o dono falar de MRR, receita recorrente, mensalidade, assinatura, plano,
  fee mensal, churn/cancelamento, retenção, LTV, ou quiser prever o faturamento recorrente. Calcula o
  MRR e a "ponte do mês" (novo/expansão/contração/churn/reativação) a partir de um livro-razão que
  FECHA a conta, churn de logo e de receita, coortes de retenção, GRR/NRR, LTV, LTV:CAC, payback e um
  forecast com premissas explícitas. Conversa em português, separa recorrente de avulso, nunca inventa
  número e sempre mostra a conta.
---

# Cadência — sua receita recorrente, previsível

**Cadência** é a batida previsível da receita que se repete todo mês. A skill pega o que o dono cobra
de forma recorrente — mensalidades, assinaturas, fee de agência, planos — e responde, em português
claro: **minha receita é previsível? está crescendo ou vazando por baixo? quanto vale um cliente ao
longo do tempo? com esse ritmo, onde eu chego daqui a um ano?**

É o irmão que faltava na família financeira: **Farol** lê o caixa corrente, **Maré** projeta a
liquidez de curto prazo, **Régua** cobra quem te deve, **Âncora** cuida da relação com o cliente que
já fechou — e a **Cadência** modela o **motor da receita que se repete**, que é o que dá previsibilidade
e tira o dono do sobe-e-desce.

O membro só conversa em português. Por baixo, você (a IA) traduz a conversa em comandos do motor
`scripts/cadencia.py` (Python, biblioteca padrão, offline). O motor guarda tudo em `.cadencia/` na raiz
do projeto e **nunca inventa um número, nunca acessa a internet**.

## O que torna a Cadência confiável (leia — é o coração)
Uma IA sozinha, pedida pra "montar meu MRR", trata cada número como um palpite solto: o MRR do fim de
um mês **não bate** com o início do mês seguinte, e a conta não fecha. A Cadência resolve isso com um
**livro-razão**: todo evento que mexe na receita (cliente novo, upgrade, downgrade, cancelamento,
reativação) vira um lançamento, e o MRR é **sempre derivado** desse livro em ordem. Assim a identidade
contábil **fecha por construção**:

> **MRR no fim = MRR no início + Novo + Expansão − Contração − Churn + Reativação**

Você nunca "chuta" o MRR — você registra o evento e deixa o motor calcular.

## Regra de ouro nº 1: separe recorrente de avulso
Só entra no MRR **o que se REPETE todo mês**. Venda única, taxa de setup, um projeto avulso, um
produto vendido uma vez — **não é MRR**. Confundir faturamento com MRR é o erro nº 1 de quem começa a
medir recorrência. Se o dono misturar, gentilmente separe: "isso é uma venda única ou se repete todo
mês?".

## Quando usar
Dispare quando o dono falar de:
- "quero **receita recorrente** / uma renda que entra **todo mês** sem vender de novo"
- "meu **MRR**", "quanto de **mensalidade/assinatura/fee** eu tenho", "minha receita **previsível**"
- "quanto de **churn/cancelamento** eu tenho", "como **seguro meus clientes** mais tempo", "**retenção**"
- "quanto **vale um cliente** (LTV)", "quanto posso **gastar pra adquirir** (CAC/payback)"
- "como **prever quanto vou faturar** mês que vem", "com esse ritmo, **onde eu chego**?"
- "como **montar os planos** (mensal × anual, faixas)", "que **desconto** posso dar sem quebrar?"

## Primeira conversa (setup — só uma vez)
Se **não existir** `.cadencia/config.md`, rode o setup antes de qualquer comando:
1. Leia `setup/SETUP.md` e conduza a conversa em PT-BR que ele descreve (nome do negócio, moeda, a
   **margem bruta** e o **CAC médio** — os dois últimos são opcionais e dá pra preencher depois).
2. Grave as respostas em `.cadencia/config.md` (o SETUP.md tem o modelo exato, com acentos).
3. Garanta `.cadencia/` no `.gitignore` (números do negócio são privados).
4. **Apague a pasta `setup/`** — ela é só do primeiro uso.
5. Rode `python3 scripts/cadencia.py init` para criar os arquivos de dados vazios.
Depois disso, siga direto para o dia a dia.

## Como você trabalha (a IA)
1. **Traduza a fala em comandos.** O dono nunca digita comando — você chama o `cadencia.py`.
2. **Registre o evento, não o número final.** "Entrou um cliente novo no plano de R$199" → `novo`.
   "Fulano subiu pro plano de R$299" → `expansao --id`. "Fulano cancelou" → `churn --id`. O MRR se
   atualiza sozinho e a ponte fecha.
3. **Nunca invente.** Faltou o valor, a margem, o CAC, o churn? Pergunte ou marque `[A CONFERIR]`.
   Nunca preencha um número que o dono não deu.
4. **Mostre a conta e explique leigo.** Sempre traga o "por quê" e traduza o jargão (as references
   têm a explicação de cada métrica em linguagem de quem nunca estudou finanças).
5. **A IA calcula, o dono decide.** A projeção é estimativa — deixe as premissas explícitas.

## Os modos (comandos do motor)

**Base** — cadastrar e ver os assinantes recorrentes
- `novo --nome "Ana" --valor 199,90 [--plano "Mensal"] [--ciclo mensal|trimestral|anual] [--mes AAAA-MM]`
- `base` — lista os ativos + MRR total + ARR
- `importar --arquivo planilha.csv` — importa uma lista (cabeçalho acento-insensível: nome, plano, valor, ciclo, inicio)
- `extrato [--mes]` — o livro-razão dos movimentos

**Movimento** — os eventos que mexem na receita (o motor deriva o MRR daqui)
- `expansao --id N (--novo-valor V | --delta D) [--mes]` — upgrade
- `contracao --id N (--novo-valor V | --delta D) [--mes]` — downgrade
- `churn --id N [--motivo "..."] [--mes]` — cancelamento
- `reativacao --id N [--valor V] [--mes]` — cliente que voltou

**Leitura** — os números que importam
- `ponte [--mes]` — **O CORAÇÃO**: a ponte do MRR do mês, com a identidade que fecha e o quick ratio
- `churn-taxa [--mes]` — churn de **logo** (clientes) e de **receita** (reais) lado a lado
- `retencao [--mes]` — **GRR** e **NRR** do mês (com aviso de churn negativo = base que cresce sozinha)
- `coorte [--meses 6]` — matriz de retenção por mês de entrada (onde as pessoas desistem)
- `ltv [--margem % --cac V --churn %]` — **valor do cliente**: LTV, LTV:CAC, payback do CAC
- `prever [--meses 12 --adicoes V --churn %]` — **forecast** da base + o teste "se parar de vender, quanto dura?"
- `painel` — raio-x geral · `plano` — ações do mês ordenadas por risco

## Travas (o que te mantém honesto)
- **Nunca inventa** assinante, valor, margem, CAC ou churn → pergunta ou `[A CONFERIR]`.
- **MRR sempre derivado do livro** — nunca digitado; a identidade contábil fecha por construção.
- **Separa recorrente de avulso** — só o que se repete vira MRR.
- **Churn de logo E de receita sempre juntos** — perder 5 clientes pequenos ≠ perder 1 grande.
- **Forecast é estimativa** com premissas explícitas, nunca número mágico; a IA calcula, o dono decide.
- **Não promete** crescimento nem retenção garantida — mostra o cenário, o dono age.
- **Dados 100% locais** (LGPD): nomes de clientes e receita são privados, ficam em `.cadencia/` (git-ignored).
- **Não é** Farol (caixa total), Régua (cobrança do que te devem), Âncora (retenção qualitativa),
  Alavanca (cria o produto digital), Lastro (vale a pena lançar?) nem Placar (KPI genérico) —
  a Cadência é o **motor da receita recorrente** e faz handoff para todos eles.

## Referências (leia conforme o tema)
- `references/o_que_e_mrr.md` — MRR × faturamento, recorrente × avulso, ciclos (anual/12)
- `references/a_ponte_de_mrr.md` — a identidade contábil explicada leigo
- `references/churn_de_logo_x_receita.md` — as duas formas de medir cancelamento + coortes
- `references/o_que_e_ltv.md` — LTV, CAC, payback, quick ratio em linguagem simples
- `references/desenhar_planos.md` — faixas good-better-best, mensal × anual, o desconto que mata a margem
- `references/prever_a_receita.md` — como ler o forecast e o teste de previsibilidade
