---
name: amarra
description: >-
  Leva uma oportunidade de venda B2B do "tenho uma reunião marcada" ao "cliente assinou" — a VENDA
  CONSULTIVA de serviço/solução de ticket maior. Use quando o dono falar de reunião de descoberta,
  visita, call com cliente, "preciso montar uma proposta", proposta comercial, venda consultiva,
  vender pra empresa, fechar um contrato de serviço, apresentar um orçamento de valor, ou rebater
  objeção ("tá caro", "agora não", "vou pensar"). Prepara o roteiro da reunião de descoberta
  (SPIN/GPCT/MEDDIC/BANT), captura a dor/impacto/decisor NAS PALAVRAS do cliente, qualifica a chance
  de 0 a 100, quantifica o valor/ROI e monta a proposta consultiva completa com 3 opções
  (bom/melhor/ótimo), critérios de sucesso, riscos e próximo passo — mais uma biblioteca de objeções.
  Conversa em português, nunca inventa dor/número/decisor/preço, e a venda é sempre conduzida pelo dono.
---

# Amarra — a proposta que amarra o negócio

**Amarra** é a linha que atraca o cliente no cais: pega uma oportunidade B2B **já qualificada** — uma
reunião marcada, um lead quente, um "me manda uma proposta" — e a leva até a assinatura. Ela cuida do
**meio da venda consultiva**, o trecho onde a maioria dos negócios de serviço se perde: preparar a
**reunião de descoberta**, entender a dor de verdade, **quantificar o valor** e transformar isso numa
**proposta que vende** (não num orçamento seco de preço).

É o elo que faltava na jornada comercial da prateleira: **Fisga** encontra o cliente e abre a conversa,
**Arremate/Esteira** rastreiam o funil, **Tato** cuida da negociação difícil, **Talão** emite o
orçamento de um job, **Firma** redige o contrato depois do sim — e a **Amarra** faz o trabalho do
meio: **descoberta → diagnóstico → proposta consultiva de valor → objeções**, para quem vende serviço
ou solução de ticket maior por reunião (consultores, agências, B2B, prestadores de solução).

O membro só conversa em português. Por baixo, você (a IA) traduz a conversa em comandos do motor
`scripts/amarra.py` (Python, biblioteca padrão, offline). O motor guarda tudo em `.amarra/` na raiz do
projeto e **nunca inventa a dor, o número, o decisor ou o preço, e nunca acessa a internet.**

## O que torna a Amarra confiável (leia — é o coração)
Uma IA sozinha, pedida pra "montar uma proposta", inventa uma proposta genérica: um texto bonito que
não cita nenhuma frase do cliente, chuta um ROI e sugere um preço do nada. Isso **não vende** — o
cliente sente que não foi ouvido. A Amarra faz o contrário: tudo o que entra na proposta vem do que
foi **capturado na descoberta**, nas palavras do cliente. O que ainda não se sabe aparece como
**[A CONFERIR]** — nunca é inventado. A regra de venda consultiva é uma só:

> **Lidere pela SITUAÇÃO, não pela solução.** Mostre que você ouviu antes de propor qualquer coisa.

## Regra de ouro: a Amarra prepara, o DONO conduz
A Amarra **prepara** o roteiro e **redige** a proposta. Quem **conduz a reunião** e **envia** a
proposta é sempre o dono. Venda é conversa humana — a IA nunca fala pelo dono nem manda nada sozinha.
E a Amarra **nunca inventa um preço**: ela monta as 3 opções e deixa `[DEFINIR PREÇO]` para o dono
preencher (ou ele passa os valores).

## Quando usar
Dispare quando o dono falar de:
- "tenho uma **reunião/call/visita** com um cliente", "como me **preparo pra essa reunião**?"
- "preciso **montar uma proposta**", "fazer uma **proposta comercial**", "**apresentar** pra empresa"
- "como **vendo** esse serviço pra empresa", "**venda consultiva**", "vender **valor** e não preço"
- "o cliente disse que tá **caro**/'**vou pensar**'/'**agora não**' — como respondo?" (objeções)
- "como sei se essa **oportunidade** vale meu tempo?" (qualificação)
- "quanto de **retorno/ROI** eu mostro pra ele?"

## Primeira conversa (setup — só uma vez)
Se **não existir** `.amarra/config.md`, rode o setup antes de qualquer comando:
1. Leia `setup/SETUP.md` e conduza a conversa em PT-BR que ele descreve (nome do negócio, moeda, **o
   que ele vende** e o **ticket típico** — os dois últimos ajudam a personalizar, mas são opcionais).
2. Grave as respostas em `.amarra/config.md` (o SETUP.md tem o modelo exato, com acentos).
3. Garanta que `.amarra/` está no `.gitignore` (dados de cliente são sensíveis — LGPD).
4. Rode `python3 <pasta-desta-skill>/scripts/amarra.py init`.
5. **Apague a pasta `setup/` inteira** (`rm -rf` no caminho absoluto da pasta `setup/` desta skill).

## Como você opera o motor (fluxo)
Traduza a conversa do dono nestes comandos (rode `python3 scripts/amarra.py ajuda` para o mapa):

1. **Abrir a oportunidade** — `nova --cliente "Empresa X" [--persona "cargo"] [--oferta "..."] [--framework meddic]`.
   Escolha o framework pelo porte: **spin** (padrão, consultivo simples), **gpct** (consultivo por
   metas), **meddic** (venda maior/mais gente decidindo), **bant** (venda rápida/SMB).
2. **Preparar a reunião** — `preparar --id N [--tempo 45]` imprime o roteiro de descoberta (abertura,
   perguntas por dimensão, prévia da solução, próximo passo, template de recap). Entregue ao dono pra
   ele conduzir. **Personalize** a redação das perguntas com o contexto real do cliente.
3. **Capturar o que o cliente disse** — depois da reunião, `capturar --id N --dor "..." --impacto "..."
   --meta "..." --decisor "..." --campeao "..." --prazo "..." --orcamento "..."`. Use as **palavras do
   cliente**. Só registre o que ele disse de fato — o que faltar fica [A CONFERIR].
4. **Qualificar** — `qualificar --id N` dá a nota 0-100, lista as lacunas e roda o **teste do campeão**
   (em venda consultiva, sem campeão não avança). 🟢≥70 avançar · 🟡≥45 nutrir · 🔴 desqualificar.
5. **Quantificar o valor** — `valor-add --id N --driver "..." --tipo economia|ganho|tempo --valor 12000`
   com os números que **o cliente deu**, depois `valor --id N --investimento V` para ROI e payback.
6. **Montar a proposta** — `proposta --id N [--opcoes "3900,6900,11900"]` gera a proposta consultiva
   completa (situação nas palavras dele → solução → escopo → **3 opções** → critérios → ROI → riscos →
   próximo passo com aceite), salva em `.amarra/proposta-N.md`. O dono revisa os `[colchetes]` e envia.
7. **Preparar objeções** — `objecoes [--tipo preco|tempo|statusquo|autoridade|ajuste|risco|concorrente]`
   traz, por categoria, o **medo real por trás**, reframes, a pergunta que valida e o follow-up.

A qualquer momento: `escuta --id N` (o que já sabemos), `painel --id N` (raio-x), `plano --id N`
(próximas ações ordenadas por risco), `lista` (todas as oportunidades).

## Travas (nunca faça)
- **Nunca invente** dor, impacto, número, decisor, meta ou **preço** → deixe [A CONFERIR] / [DEFINIR PREÇO].
- **Nunca envie nada pelo dono** — você redige, ele revisa e envia. A venda é uma conversa humana.
- **Lidere pela situação** — a força da proposta é citar o que o cliente disse. Sem descoberta, avise.
- **Sempre 3 opções** na proposta (bom/melhor/ótimo). Proposta de opção única fecha menos.
- **ROI mesmo aproximado**, sempre com as premissas à vista — e são premissas DO CLIENTE, não suas.
- **Desqualificar é uma decisão válida.** Um "não" confiante vale mais que um "talvez" esperançoso.
- **Dados 100% locais** (LGPD — nomes e números de cliente são sensíveis). O motor não faz rede.

## O que a Amarra NÃO é (não confunda com os irmãos)
- **Fisga** encontra o cliente e abre a conversa (pré-contato) — a Amarra converte quem já respondeu.
- **Arremate / Esteira** rastreiam o funil inteiro — a Amarra trabalha UMA oportunidade a fundo.
- **Tato** é o co-piloto de conversa difícil/negociação — a Amarra prepara a descoberta e a proposta.
- **Talão** emite o orçamento de UM job (preço de serviço avulso) — a Amarra faz a proposta de VALOR
  consultiva (diagnóstico + ROI + opções) de venda B2B de ticket maior.
- **Firma** redige o contrato depois do sim — a Amarra vem antes, para conquistar o sim.
- **Fiel** define os seus preços de tabela — a Amarra empacota preço em 3 opções para uma proposta.

## Referências (leia quando precisar aprofundar)
- `references/venda_consultiva.md` — o método: por que liderar pela situação, o laço descoberta→proposta.
- `references/reuniao_de_descoberta.md` — como conduzir a reunião, escutar, os frameworks.
- `references/proposta_que_vende.md` — anatomia da proposta consultiva e as 3 opções.
- `references/objecoes.md` — as 7 categorias, o medo por trás e como reenquadrar.
