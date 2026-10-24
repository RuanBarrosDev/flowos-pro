# Do protótipo ao build — o handoff

Depois que o protótipo foi validado (o dono aprovou, ou o cliente navegou e fechou),
a Maquete gera o **brief de construção** com `entregar`. É a ponte entre o desenho e
o código.

## O que o brief contém (`.maquete/brief-de-construcao-N.md`)
- **O produto** — nome, para quem, plataforma, problema que resolve, tom.
- **Quem usa** — as personas e o que cada uma quer.
- **Os fluxos** — a ordem em que as telas acontecem, com gatilho e jornada.
- **As telas, uma a uma** — objetivo, estado especial, **os dados que entram**
  (os campos) e **as ações** (cada botão e para onde leva).
- **As pendências do design** — ações quebradas, telas órfãs e o que ficou [A CONFERIR].

## Como usar o brief
1. **Com o Gabarito** — se você ainda não escreveu os requisitos formais, o brief
   alimenta o Gabarito: cada tela e cada dado viram requisitos com critério de aceite.
2. **Com o Estaleiro / Claude Code** — cole o brief + aponte o protótipo HTML como
   referência visual. O agente de engenharia constrói tela a tela sabendo exatamente
   o que cada uma faz, quais dados recebe e para onde navega. O protótipo mostra a
   forma; o brief explica o comportamento.
3. **Com o Arcabouço** — os campos que aparecem nas telas (o "dados que entram" do
   brief) são a matéria-prima do modelo de dados. Tela e banco andam juntos.

## A regra de ouro do handoff
O que está no protótipo e no brief é o **contrato do que construir**. Se no build
surgir uma tela ou uma ação que não estava no desenho, pare: ou o desenho estava
incompleto (volte à Maquete e atualize), ou é escopo novo (decida antes de codar).
Assim o build não "descobre" o produto no meio do caminho — ele executa um desenho
já validado. É isso que economiza o retrabalho.
