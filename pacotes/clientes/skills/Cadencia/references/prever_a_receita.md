# Prever a receita recorrente (e o teste da previsibilidade)

A grande promessa da recorrência é **saber quanto vai entrar mês que vem**. A Cadência faz isso com o
comando `prever` — mas de um jeito honesto: com **premissas explícitas**, nunca um número mágico.

## Como a previsão funciona
A cada mês futuro, a Cadência aplica duas forças à base atual:
1. **Adições** — quanto de MRR novo entra por mês (novo + expansão + reativação). Por padrão, usa a
   **média dos últimos 3 meses**; você pode fixar com `--adicoes`.
2. **Churn** — a taxa de receita que sai por mês. Por padrão, usa a média do seu histórico; você pode
   fixar com `--churn`.

A conta de cada mês é: `MRR próximo = MRR atual × (1 − churn) + adições`. Ela mostra onde você chega em
3, 6, 12 meses (ou no horizonte que pedir).

**Isso é estimativa.** Vale enquanto as premissas se mantiverem. Se seu churn piorar ou você parar de
vender, o número muda — por isso as premissas ficam à vista pra você editar. A IA calcula, você decide.

## O teste de previsibilidade: "se eu parar de vender hoje?"
O número mais revelador do `prever` é o cenário **"se você parar de vender/expandir agora"**. Sem
nenhuma venda nova, só o churn agindo, em quantos meses a base cai à **metade**? Isso é a **meia-vida**
da sua receita recorrente.

- Meia-vida **longa** (muitos meses) → base sólida, previsível: mesmo sem vender, você tem fôlego.
- Meia-vida **curta** (poucos meses) → base frágil: você depende de vender sem parar só pra ficar no
  mesmo lugar (o churn come tudo). É o sinal de que o problema é **retenção**, não aquisição.

Um negócio recorrente saudável derrete devagar. Se o seu derrete rápido, priorize churn antes de
gastar em tráfego.

## O que NÃO fazer
- Não trate a previsão como promessa. É um mapa que muda quando o território muda.
- Não "rode 3 vezes e chame de pessimista/realista/otimista" — cenário de verdade é **mudar a premissa**
  (ex.: `--churn 8` pra ver o pessimista, `--adicoes` maior pro otimista), não repetir o mesmo cálculo.
- Não persiga só crescimento de topo (adições) ignorando o churn: crescer com o balde furado é caro e
  cansativo. Tape o furo primeiro.
