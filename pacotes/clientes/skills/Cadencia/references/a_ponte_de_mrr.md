# A ponte do MRR — o mês inteiro em uma conta que fecha

Todo mês, o seu MRR sofre cinco forças. A "ponte" (também chamada de *waterfall*) mostra como você saiu
do MRR do início e chegou no MRR do fim. A identidade é:

> **MRR fim = MRR início + Novo + Expansão − Contração − Churn + Reativação**

## O que é cada força
- **Novo** — MRR de **clientes novos** que entraram no mês. (+)
- **Expansão** — clientes atuais que **subiram de plano / gastaram mais** (upgrade). (+)
- **Reativação** — clientes que tinham cancelado e **voltaram**. (+)
- **Contração** — clientes que **desceram de plano / gastaram menos** (downgrade). (−)
- **Churn** — clientes que **cancelaram** de vez. (−)

O resultado das cinco forças é o **net-new** (movimento líquido): quanto a base cresceu ou encolheu no
mês. Se o net-new é positivo, sua base 🟢 cresceu; se é negativo, ela 🔴 encolheu.

## Por que a conta FECHA (e por que isso importa)
A Cadência não "chuta" o MRR. Cada evento (novo, upgrade, cancelamento…) vira um lançamento no
livro-razão, e o MRR é a **soma** desses lançamentos em ordem. Por isso a ponte **sempre fecha**: o
"MRR do fim" que a ponte calcula é exatamente o MRR que aparece no mês seguinte como "início".

Isso é o que uma IA sozinha **não** consegue fazer de forma confiável — ela trataria cada mês como um
número solto e a conta não bateria. Aqui, bate sempre. Você confia no número porque ele vem da conta,
não do palpite.

## Quick ratio: o crescimento é eficiente?
No fim da ponte a Cadência mostra o **quick ratio** = (o que entrou) ÷ (o que saiu) =
(novo + expansão + reativação) ÷ (churn + contração).
- **≥ 4×** 🟢 crescimento eficiente: pra cada R$1 que vaza, entram R$4.
- **1× a 4×** 🟡 crescendo, mas devagar — o vazamento está comendo boa parte do que entra.
- **< 1×** 🔴 você corre pra trás: sai mais do que entra.

Um negócio pode parecer que "está vendendo muito" e mesmo assim ter quick ratio baixo — é o sinal de
que o churn está mascarando o esforço de venda. A ponte revela isso.

## Como usar no dia a dia
Rode `ponte` no fim de cada mês. Se o net-new veio negativo ou o quick ratio caiu, o problema quase
sempre está no **churn/contração** (lado direito) — e aí o próximo passo é `churn-taxa` e `retencao`.
