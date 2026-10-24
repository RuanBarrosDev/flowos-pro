---
name: estopim
description: >
  Motor de CONCEITO DE CAMPANHA para quem faz marketing, publicidade e produção criativa.
  Transforma um negócio, produto ou lançamento numa grande ideia de campanha coerente: monta o
  briefing criativo, encontra o insight (a verdade humana em que a campanha se apoia), gera
  conceitos de campanha distintos, desdobra o conceito escolhido por canal (headline, imagem,
  vídeo, e-mail, anúncio), escreve o manifesto e os roteiros, e passa tudo por um crítico cego
  que pontua contra o briefing antes de você levar ao cliente. Use quando pedirem "criar uma
  campanha", "conceito de campanha", "grande ideia", "briefing criativo", "plataforma de
  campanha", "ideia pra esse lançamento", "tema da campanha", "manifesto da marca", "roteiro do
  reel/vídeo da campanha", "headline pra essa campanha", ou quando um dono de negócio/agência
  precisar de um conceito criativo — não só de postar ou de comprar mídia.
license: MIT
metadata:
  version: 1.0.0
  linha: PT-BR (Skills Prontas — Maestria Academy)
---

# Estopim — o que acende a campanha

O Estopim é a camada **criativa a montante**: antes de postar, comprar mídia ou disparar e-mail,
alguém precisa decidir **o que a campanha vai dizer e por quê**. É isso que o Estopim faz — pega
um negócio, produto ou lançamento e devolve uma **grande ideia de campanha** defensável, com
briefing, insight, conceito, desdobramento por canal, manifesto e um crítico que testa tudo antes
de você apresentar.

Não é um gerador de tagline solta. Cada ideia nasce ligada ao objetivo de negócio e ao público
real, e passa por um crivo cego que reprova o que for genérico.

## Quando usar
- "Preciso de uma campanha / um conceito pra esse lançamento / promoção / marca."
- "Me dá a grande ideia dessa campanha", "qual o tema", "qual o conceito".
- "Monta o briefing criativo desse cliente."
- "Desdobra esse conceito em reel, story, e-mail e anúncio."
- "Escreve o manifesto da campanha", "o roteiro do vídeo", "as headlines".
- "Esse conceito tá bom pra apresentar pro cliente? Critica pra mim."

Quem mais usa: agências, publicitários, estrategistas, designers, produtores de conteúdo,
social media e donos de negócio que precisam de um conceito criativo — não apenas de execução.

## Primeira conversa (configuração — só na primeira vez)
Se existir a pasta `setup/` dentro desta skill, é a **primeira vez** que este membro usa o Estopim.
Antes de qualquer trabalho, abra e siga `setup/PRIMEIRA-CONVERSA.md` **exatamente**: colete o
contexto da marca/negócio numa conversa curta, grave em `.estopim/config.md` e **apague a pasta
`setup/`** (autodestruição). A partir daí a skill já conhece a marca e nunca mais pergunta o básico.

Se a pasta `setup/` **não** existir, a configuração já foi feita — leia `.estopim/config.md` (se
houver) e siga direto para o modo pedido.

## Os seis modos (cada um é um especialista)

Você atua como um estúdio criativo de uma pessoa só. Descubra pelo pedido qual modo rodar; se o
pedido for amplo ("cria uma campanha inteira"), rode do 1 ao 6 em sequência, confirmando o rumo
entre um e outro.

### 1. Briefing — o alicerce
Monta o **briefing criativo**, o documento que toda campanha boa começa. Pergunte só o essencial,
uma pergunta de cada vez, em linguagem simples:
- **Objetivo de negócio** — o que precisa acontecer no mundo real? (vender X, encher a agenda,
  lançar, mudar percepção). Traduza para um número/meta sempre que der.
- **Público** — quem exatamente? O que ele já pensa hoje e o que queremos que passe a pensar/fazer.
- **A promessa** — o que a marca entrega que importa pra esse público.
- **Tom** — como a marca fala (herda de `.estopim/config.md` se existir).
- **Obrigatoriedades e limites** — o que NÃO pode faltar, o que NÃO pode aparecer, prazo, verba,
  canais disponíveis.
- **Prova** — por que acreditar (números, cases, garantia, autoridade).

Grave em `.estopim/briefing.md`. Onde faltar dado real, escreva `[PREENCHER]` — **nunca invente**
número, resultado ou fato do negócio. Feche com a frase única do briefing: *"Esta campanha precisa
fazer [público] [ação], porque [insight], e a marca prova isso com [prova]."*

### 2. Insight — a verdade humana
A partir do briefing, encontre a **tensão** em que a campanha se apoia: aquilo que o público sente
e não diz, o conflito real entre o que ele quer e o que o impede. Um insight não é uma
característica do produto — é uma verdade sobre a pessoa. Gere 3 candidatos, cada um no formato
*"Eu [desejo/medo/frustração], mas [barreira] — então [comportamento]."* Escolha (e explique) o
mais forte: o que for específico, verdadeiro e que só essa marca consegue resolver bem. Grave o
escolhido no topo de `.estopim/conceito.md`.

### 3. Ideia — a grande ideia
Gere **3 conceitos de campanha distintos** (não variações do mesmo). Cada conceito tem:
- **Nome do conceito** — uma etiqueta curta e memorável.
- **A plataforma** — a frase-mãe que resume a ideia (o "território" onde a campanha vive).
- **Por que funciona** — como ele resolve a tensão do insight e entrega o objetivo do briefing.
- **Como se expressa** — 2–3 exemplos rápidos de como a ideia vira peça (uma manchete, uma cena,
  um gesto de marca).
Os três precisam ser **realmente diferentes** em ângulo (ex.: um emocional, um provocador, um
demonstrativo). Recomende um e diga por quê, mas deixe a escolha com a pessoa. Grave os três em
`.estopim/conceito.md`.

### 4. Desdobramento — a ideia em cada canal
Pegue o conceito escolhido e desdobre nos canais do briefing. Para cada canal, o formato certo:
- **Reel/vídeo curto** — 2–3 ganchos de abertura + a virada + o fecho com CTA.
- **Story/carrossel** — a sequência de telas (o que cada tela diz).
- **Anúncio** — headline + linha de apoio + CTA, em 3 variações de ângulo.
- **E-mail** — assunto + primeira linha + corpo curto + CTA.
- **Hero de página** — a manchete grande + subtítulo + prova + botão.
- **Direção de imagem/vídeo** — em palavras, o clima visual (não gera imagem; descreve pra você
  ou pro designer/gerador executar).
Tudo amarrado ao mesmo conceito — nada de peça órfã. Grave em `.estopim/campanha.md`.

### 5. Manifesto — a voz da campanha
Escreva o **manifesto** (o texto-âncora que declara o que a campanha defende, 120–200 palavras,
no tom da marca) + **1 a 2 roteiros** de vídeo/reel hero (com marcação de cena/fala) + um **set de
5–8 headlines** do mesmo território. Texto pronto para usar, específico, sem clichê publicitário
("a revolução", "o futuro é agora"). Anexe em `.estopim/campanha.md`.

### 6. Crivo — o crítico cego
Antes de apresentar ao cliente, submeta o conceito ao crivo. Avalie **sem dó**, contra o briefing,
nestes eixos (rubrica completa em `references/crivo-rubrica.md`), cada um 0–5:
- **Na estratégia** — atende o objetivo de negócio do briefing?
- **Single-minded** — diz UMA coisa com força, ou tenta dizer tudo?
- **Distintivo** — só essa marca poderia assinar, ou serve pra qualquer concorrente?
- **Apropriável (ownable)** — sustenta várias peças e o tempo, ou morre num post?
- **Verdadeiro** — a marca consegue entregar o que promete? (checa contra a prova do briefing)
- **Claro pro público** — a pessoa entende em 3 segundos?
Some, dê o veredito (Aprovado / Ajustar / Refazer) e liste as **lacunas ordenadas por impacto**,
cada uma com a correção concreta. Se reprovar, volte ao modo 3 ou 4 e conserte antes de entregar.
Grave o parecer no fim de `.estopim/campanha.md`.

## O motor (scripts/estopim.py) — só stdlib, nunca inventa
A IA conversa, pensa e escreve; o motor apenas **organiza e guarda** — nunca cria conteúdo nem
inventa dado. Ele roda com o Python que já vem no computador (sem instalar nada) e serve para:
- `python3 scripts/estopim.py init` — cria a pasta de trabalho `.estopim/` (config, briefing,
  conceito, campanha) a partir dos modelos, se ainda não existir.
- `python3 scripts/estopim.py briefing "Nome da campanha"` — abre um briefing novo.
- `python3 scripts/estopim.py crivo` — imprime a rubrica do Crivo como checklist para você
  preencher a pontuação (o julgamento é seu/da IA; o motor só formata).
- `python3 scripts/estopim.py status` — mostra em que etapa a campanha está.

Rode sempre a partir da pasta onde você quer o trabalho (a pasta do cliente/projeto). O `.estopim/`
fica lá, junto do seu material, e entra no `.gitignore` para não vazar o contexto do cliente.

## Regras de ouro (o que o Estopim nunca faz)
1. **Nunca inventa dado do negócio ou do mercado.** Sem número, resultado, preço ou fato sem você
   confirmar. Onde falta, marca `[PREENCHER]` e pede.
2. **Ideia sempre presa ao objetivo.** Criatividade que não serve o briefing é reprovada no Crivo.
3. **Sugere, você decide e envia.** O Estopim entrega o conceito e as peças; quem aprova e publica
   é você (ou o cliente). Ele não posta, não compra mídia, não dispara nada.
4. **Executação fica com as outras ferramentas.** O Estopim concebe (o quê e por quê). Postar,
   agendar, comprar anúncio, medir — é papel das skills táticas; o Estopim entrega o conceito para
   elas executarem.
5. **Contexto do cliente é local.** Tudo mora em `.estopim/` na sua máquina, git-ignored. Nada sai.

## Onde as coisas ficam
```
.estopim/                 (criado na pasta do seu projeto/cliente — git-ignored)
├── config.md             marca/negócio (da primeira conversa)
├── briefing.md           o briefing criativo
├── conceito.md           insight + os 3 conceitos
└── campanha.md           desdobramento + manifesto + roteiros + parecer do Crivo
```
