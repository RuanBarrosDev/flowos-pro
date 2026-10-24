# Churn: as duas formas de medir o cancelamento (e as coortes)

**Churn** é a taxa de cancelamento — quanto da sua base foi embora no período. O erro comum é medir de
um jeito só. Existem **duas** formas, e você precisa das duas.

## Churn de LOGO (clientes)
Conta **quantos clientes** saíram.
> Churn de logo = clientes que cancelaram ÷ clientes ativos no início do mês.

Exemplo: começou o mês com 100 clientes, 5 cancelaram → **5% de churn de logo**.

## Churn de RECEITA (reais)
Conta **quantos reais** saíram.
> Churn de receita = MRR que cancelou ÷ MRR no início do mês.

Exemplo: começou com R$ 20.000 de MRR, cancelou R$ 3.000 → **15% de churn de receita**.

## Por que você precisa dos dois
Perder **5 clientes pequenos** é muito diferente de perder **1 cliente grande**. Olhando só o número
de clientes (logo), os dois parecem iguais. Olhando a receita, você vê a verdade.

**Regra de leitura:** se o churn de **receita** é MAIOR que o de **logo**, seus **clientes maiores estão
indo embora** — é o alarme mais perigoso, priorize retê-los. Se o de logo é maior, quem sai são os
pequenos e o impacto no faturamento é menor.

A Cadência mostra os dois lado a lado no comando `churn-taxa` e dispara o aviso automaticamente.

## Churn de receita bruto × líquido
- **Bruto** — só os cancelamentos.
- **Líquido** — os cancelamentos + downgrades **menos** os upgrades (expansão). Se os clientes que
  ficam gastam mais, eles compensam parte do que saiu. Quando a expansão supera as perdas, o churn
  líquido fica **negativo** — é o santo graal (veja NRR em `o_que_e_ltv.md`... na verdade em `retencao`).

## Coortes: ONDE as pessoas desistem
Olhar o churn total esconde *quando* as pessoas saem. A **coorte** agrupa quem entrou no **mesmo mês** e
acompanha quantos continuam pagando no mês 1, 2, 3… A matriz (`coorte`) mostra, para cada turma de
entrada, o % que sobrou ao longo do tempo.

Onde o número **desaba** é onde está o problema:
- Cai logo no **mês 1-2** → problema de **entrega inicial / onboarding** (o cliente não viu valor rápido).
- Cai lá no **mês 6-12** → problema de **valor contínuo** (a novidade passou e não há motivo pra ficar).

Retenção é mais barata que aquisição: reduzir o churn quase sempre rende mais que comprar mais tráfego.
A coorte te diz exatamente onde agir.
