# O que é MRR (e por que não é o seu faturamento)

**MRR = Receita Recorrente Mensal.** É só o dinheiro que **se repete todo mês** por causa das
assinaturas/mensalidades/planos que estão ativos. Nada mais.

## O erro nº 1: confundir faturamento com MRR
Faturamento é **tudo** que caiu na conta no mês: mensalidades + uma venda avulsa + uma taxa de setup +
um projeto único. O MRR é **só a parte que vai se repetir mês que vem sem você vender de novo**.

Exemplo: uma clínica faturou R$ 30.000 no mês. Desses, R$ 12.000 são de 60 pacientes no plano mensal
de R$ 200, e R$ 18.000 foram consultas avulsas. **O MRR é R$ 12.000, não R$ 30.000.** Só os R$ 12.000
entram de novo mês que vem sem esforço de venda — é o que dá previsibilidade.

**Regra de ouro:** ao cadastrar receita na Cadência, pergunte sempre "isso se repete todo mês ou é uma
venda única?". Só o que se repete vira MRR. Venda avulsa, setup, projeto único → **não entram**.

## Como o MRR é calculado
Jeito simples: **nº de assinantes ativos × ticket médio mensal**. A Cadência faz isso somando o MRR de
cada assinante ativo.

## Planos que não são mensais (anual, trimestral)
Se o cliente paga **R$ 2.400 por ano**, isso não é R$ 2.400 de MRR — é **R$ 200/mês** (2.400 ÷ 12). A
Cadência **normaliza** todo plano para o valor mensal equivalente:
- Anual → dividido por 12
- Trimestral → dividido por 3
- Semestral → dividido por 6

Assim planos de ciclos diferentes ficam comparáveis e o MRR fica honesto. Ao cadastrar, informe o
**valor cobrado** e o **ciclo** (`--ciclo anual`), e o motor calcula o mensal.

## ARR
**ARR = Receita Recorrente Anual = MRR × 12.** É o mesmo número, só olhado no ano. Serve pra ter a
dimensão anual da base recorrente.

## Por que separar recorrente de avulso muda o jogo
Quando você separa, consegue pela primeira vez responder "quanto vai entrar mês que vem?" com um
número em vez de um palpite. É o começo de sair do sobe-e-desce (feast-or-famine) e ter caixa
previsível.
