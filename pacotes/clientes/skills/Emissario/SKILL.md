---
name: emissario
description: >-
  Projeta e monta o SEU assistente/agente de IA de atendimento ao cliente — sem programar. Use
  quando o dono quiser CRIAR um agente de IA que atende por ele: "quero um assistente de IA pro meu
  WhatsApp", "criar um agente que atende meus clientes", "montar um chatbot pra minha clínica/loja",
  "um GPT que responde as dúvidas do meu negócio", "assistente de atendimento com IA", "bot de
  atendimento no WhatsApp", "SDR de IA", "como faço um agente que atende sozinho". O Emissário
  conduz o dono por 6 passos — Definir, Persona, Conhecimento, Conversa, Travas & Escalar, Montar &
  Testar — e entrega o SYSTEM PROMPT pronto para colar no GPT personalizado, Projeto do Claude,
  WhatsApp (ManyChat/Typebot) ou chat do site, com travas anti-alucinação, anti-"ignore as
  instruções" e escalonamento para humano. Não escreve código; é a camada de PROJETO do assistente.
  Tudo offline e local em .emissario/.
---

# Emissário — monte o seu assistente de IA de atendimento

O **emissário** é aquele que fala e representa você onde você não pode estar. Esta skill monta
exatamente isso: um **assistente de IA que atende os seus clientes por você** — 24 horas, no seu tom,
só com o que você ensinou, e que chama um humano na hora certa.

Você **conversa em português**; o Emissário faz o trabalho de arquiteto de assistente e te entrega
o **system prompt pronto** — o texto que você cola no GPT personalizado, no Projeto do Claude, num bot
de WhatsApp (ManyChat/Typebot) ou no chat do seu site. **Sem escrever uma linha de código.**

> A comunidade repete o mesmo desejo — "quero criar um AGENTE de IA que atende no WhatsApp / no meu
> consultório / pros meus clientes". O difícil não é a plataforma; é **projetar** o assistente para
> ele não inventar, não falar besteira e passar pro humano quando precisa. O Emissário é esse projeto.

## Quando usar (gatilhos)
- "Quero um assistente/agente de IA pra atender meus clientes / no meu WhatsApp."
- "Montar um chatbot/bot de atendimento pra minha clínica, loja, escritório, agência."
- "Um GPT que responde as dúvidas do meu negócio." · "Fazer um SDR de IA."
- "Como eu crio um agente que atende sozinho, sem falar bobagem?"

**NÃO é o Emissário quando:**
- O dono quer **responder ele mesmo** cada mensagem com ajuda da IA, uma a uma → **Balcão** (atendimento
  inbound com humano no loop). O Emissário CONSTRÓI o assistente que atende **sozinho**.
- Criar uma **skill/agente de Claude Code** instalável no `.claude/` do próprio dono (ferramenta de dev)
  → **Molde**. O Emissário faz um assistente **conversacional voltado ao CLIENTE**, publicado num
  chatbot/GPT/WhatsApp.
- Refinar **um prompt avulso** para uma tarefa pontual → **Prisma**. O Emissário projeta um
  **assistente inteiro** (persona + base + fluxos + travas), não uma instrução única.
- **Escrever o código** de um app/bot do zero → **Estaleiro**. O Emissário é o projeto/spec que você
  cola em qualquer plataforma no-code.
- Decidir **qual** tarefa vale automatizar → **Engrenagem**. Aqui o caso já está escolhido.

## Primeira vez (setup) — obrigatório antes de tudo
Se **não existir `.emissario/config.md` na raiz do projeto**, rode o setup:
1. Leia `setup/SETUP.md` e siga o roteiro (conversa curta em PT-BR).
2. Ele grava `.emissario/config.md` (git-ignored) com o básico do assistente e **se autodestrói**
   (apaga a pasta `setup/`).
Se `.emissario/config.md` já existe, pule direto para os modos.

> **Onde o Emissário guarda tudo:** numa pasta `.emissario/` na **raiz do projeto** do dono (não dentro
> da skill). O motor acha a raiz sozinho (`CLAUDE_PROJECT_DIR` ou subindo até achar `.git`/`.claude`).
> Rode o `emissario.py` de dentro do projeto do dono. Dados 100% locais, nada vai pra internet.

## O motor
A parte exata e mecânica é feita por `scripts/emissario.py` (Python puro, **offline**, sem instalar
nada, sem API). A IA (você) conversa, decide e escreve os blocos; o motor **monta** o system prompt,
**mede a prontidão** e **gera o roteiro de teste**. Ele **nunca inventa** conteúdo: o que faltar vira um
`[PREENCHER]` visível.
```
python3 scripts/emissario.py --help
```
Arquivos em `.emissario/`: `config.md`, `persona.md`, `base.md`, `fluxos.md`, `travas.md` e
`build/system-prompt.txt` + `build/assistente.md` (gerados pelo `montar`).

---

## Os 6 modos

### 1. Definir — qual é o trabalho do assistente
O ponto de partida. Em conversa curta, feche (e grave no `config.md`, via setup ou editando):
- **Missão** em UMA frase ("tirar dúvidas e agendar avaliação para novos pacientes").
- **Quem ele atende** (o público — cliente novo? cliente atual? os dois?).
- **Onde vai rodar** (WhatsApp, GPT personalizado, Projeto do Claude, site).
- **Escopo:** o que ele **faz** e, tão importante quanto, o que ele **NÃO faz** (isso trava o assistente
  de sair do trilho). Leia `references/system-prompt-blueprint.md` para a estrutura.
> Regra de ouro do escopo: um assistente que tenta fazer tudo faz tudo mal. Um trabalho claro, bem-feito.

### 2. Persona — o jeito de falar
Dá rosto e voz ao assistente, na **marca do dono** (não "cara de robô"). Escreva em `.emissario/persona.md`:
nome do assistente, identidade/papel (ex.: "recepcionista simpático e objetivo da Clínica X"),
tom de voz, **saudação de abertura** pronta, e o que ele **nunca faz de estilo** (gíria demais, prometer,
formalidade fria). Siga `references/persona.md` (identidade + marcadores de comportamento, não só "seja
educado"). Uma persona forte = respostas consistentes.

### 3. Conhecimento — a base de onde ele responde (o passo que mais pesa)
O coração da confiança. Ajude o dono a montar a **base de conhecimento** em `.emissario/base.md`: serviços/
produtos, **preços e políticas**, horários, endereço, formas de pagamento, e as **perguntas frequentes**
com a resposta certa. Siga `references/base-de-conhecimento.md`.
> A **regra anti-alucinação** já entra automática no system prompt: o assistente responde **só** com o que
> está na base; se não achar, **não inventa** — confirma com a equipe e escala. Ajude o dono a cobrir as
> lacunas mais comuns agora, pra ele não deixar buraco.

### 4. Conversa — os fluxos
Desenhe os **caminhos de conversa** em `.emissario/fluxos.md` (siga `references/fluxos.md`): abertura →
entender a necessidade → caminhos comuns (tirar dúvida, orçar/agendar, reclamação), o caminho **"não sei"**
e a **coleta educada** de dados (nome, contato, o que precisa) para o dono dar sequência. Um dado por vez,
sem interrogatório.

### 5. Travas & Escalar — o que ele nunca faz e quando chama o humano
A rede de segurança. Em `.emissario/travas.md` (siga `references/travas-e-escalonamento.md`) liste as
travas **específicas do negócio** (nunca prometer prazo X, nunca dar diagnóstico, nunca fechar venda sem
confirmar…) e os **gatilhos de escalonamento** (reclamação séria, urgência, pedido de fechar negócio,
resposta fora da base) + **quem assume** e como avisar. As travas universais — anti-invenção,
**anti-"ignore as instruções / me mostre seu prompt"**, LGPD/dados sensíveis, não prometer resultado —
o motor já embute sozinho.

### 6. Montar & Testar — gerar o system prompt e validar antes de subir
Fechamento. Rode:
```
python3 scripts/emissario.py montar       # gera build/system-prompt.txt + build/assistente.md
python3 scripts/emissario.py prontidao    # checklist 🟢🟡🔴 — o que ainda falta
python3 scripts/emissario.py teste        # roteiro de 10 perguntas difíceis pra validar
```
- **montar** costura persona + base + fluxos + travas no **system prompt final** seguindo o blueprint
  (identidade, escopo, base como única verdade, fluxos, travas universais, escalonamento, coleta).
- **prontidao** dá o veredito e aponta o que falta (a base é o que mais pesa).
- **teste** entrega 10 perguntas — dentro/fora do escopo, **isca de alucinação**, **tentativa de override**,
  dado sensível, escalonamento — para o dono validar num chat de teste **antes** de publicar.
- Só depois, **publicar**: siga `references/publicar.md` (passo a passo por plataforma: GPT personalizado,
  Projeto do Claude, WhatsApp via ManyChat/Typebot, widget de site). O dono cola o `system-prompt.txt`,
  testa mais uma vez ao vivo e libera. Se a plataforma escolhida for o ManyChat e ele ainda não tiver
  conta, abra no navegador dele `open "https://manychat.partnerlinks.io/9tevnjmn2uy4-u934l7"`
  (no Windows, `start ""` no lugar de `open`; no Linux, `xdg-open`).

---

## Travas do Emissário (valem sempre)
- **Nunca inventa** conteúdo do negócio — base, preço, política, horário. O que falta vira `[PREENCHER]`;
  quem preenche é o dono.
- O system prompt gerado **já embute** anti-alucinação, anti-override ("ignore as instruções"),
  não-prometer-resultado, LGPD/dados sensíveis e **escalonamento para humano**.
- **O dono revisa e testa antes de publicar.** O Emissário projeta e monta; publicar é decisão do dono,
  depois do teste 🟢.
- **Dados 100% locais** em `.emissario/`. Nada é enviado para a internet.
- Um assistente = um trabalho claro. Escopo estreito, bem-feito, com porta de saída pro humano.

## Diferença para as skills vizinhas
- **Balcão** = o dono responde cada mensagem com a IA sugerindo (humano no loop). **Emissário** =
  constrói o assistente que atende **sozinho** e o dono publica.
- **Molde** = fábrica de **skills/agentes de Claude Code** (ferramenta de dev no `.claude/`). **Emissário**
  = assistente **conversacional voltado ao cliente**, publicado num chatbot/GPT/WhatsApp, sem código.
- **Prisma** = **um** prompt avulso. **Emissário** = um **assistente inteiro** (persona + base + fluxos + travas).
- **Estaleiro** = escreve **código**. **Emissário** = o **projeto/spec** que roda em qualquer plataforma no-code.
- **Fisga/Esteira/Turbina** = operam o **funil comercial**. **Emissário** = constrói o **agente que atende**.
