# Quanto vale um cliente: LTV, CAC e payback (em linguagem de gente)

## LTV — o valor do cliente no tempo
**LTV** (do inglês *lifetime value*) é **quanto de lucro** um cliente deixa **enquanto fica** com você.
Versão simples que a Cadência usa:

> **LTV = ticket mensal × margem bruta × meses que ele fica**

- **Ticket mensal (ARPU)** — quanto um cliente paga por mês, em média (MRR ÷ nº de ativos).
- **Margem bruta** — de cada real que ele paga, quanto SOBRA depois do custo de entregar o serviço.
- **Meses que ele fica (vida média)** — quanto menor o churn, mais tempo ele fica. A conta é
  `vida média = 1 ÷ churn mensal`. Um churn de 5% ao mês = cliente fica ~20 meses; 10% = ~10 meses.

**A grande sacada:** o LTV depende muito mais do **churn** do que do preço. Reduzir o churn pela metade
**dobra** o tempo que o cliente fica e, portanto, dobra o LTV. Por isso reter vale ouro.

## CAC — o custo de trazer um cliente
**CAC** (*customer acquisition cost*) é quanto você gasta, em média, pra conquistar **um** cliente novo
(anúncio, comissão, tempo de venda). A Cadência não adivinha isso — você informa (no config ou com
`--cac`).

## As duas contas que dizem se o negócio fecha
**LTV : CAC** — quantas vezes o cliente devolve o que custou trazê-lo.
- **≥ 3×** 🟢 saudável — o cliente vale pelo menos 3× o que custou.
- **1× a 3×** 🟡 apertado.
- **< 1×** 🔴 prejuízo — cada cliente custa mais do que deixa.

**Payback do CAC** — em **quantos meses** você recupera o que gastou pra trazer o cliente.
> Payback = CAC ÷ (ticket mensal × margem)
- **< 12 meses** 🟢 saudável.
- **12 a 18 meses** 🟡 no limite.
- **> 18 meses** 🔴 aperta o caixa — você fica sem dinheiro esperando o cliente se pagar, **mesmo** que
  o LTV pareça bom no papel.

Um LTV alto com payback longo ainda quebra o caixa no curto prazo. Olhe os dois juntos.

## Quick ratio (bônus)
Aparece na `ponte`: (novo + expansão) ÷ (churn + contração). Diz se o crescimento é eficiente ou se o
vazamento está comendo o esforço de venda. Acima de 4× é ótimo; perto de 1× você corre no lugar.

## O que a Cadência nunca faz
Não inventa a sua margem nem o seu CAC. Se você não informou, ela pede ou marca `[A CONFERIR]` — porque
um LTV com número chutado é pior que nenhum LTV.
