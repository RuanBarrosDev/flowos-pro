---
name: cais
description: >
  Onboarding e intake de cliente novo — o ritual dos primeiros dias depois que o
  cliente diz "sim". Use quando o dono de um negócio de serviço fechou (ou está
  fechando) com um cliente e precisa começar bem: dar as boas-vindas, levantar o
  contexto com um questionário de intake, reunir os documentos e acessos, alinhar
  escopo e expectativas (o "combinado", anti-scope-creep) e fazer a reunião de
  largada — acompanhando a prontidão de cada cliente até estar pronto para a
  entrega. Dispara com frases como "fechei um cliente novo", "acabei de vender pra
  um cliente", "como começar com esse cliente", "onboarding de cliente",
  "questionário de intake", "quais documentos pedir pro cliente", "monta o
  combinado de escopo", "reunião de kickoff", "o cliente sumiu e o trabalho não
  começou", "meu cliente novo não mandou os acessos". É para donos de negócio de
  serviço (agências, clínicas, advogados, contadores, consultores, freelancers) e
  não exige nenhum conhecimento técnico — a pessoa só conversa em português.
---

# Cais — onboarding e intake de cliente novo

O **cais** é onde o cliente atraca: você o recebe, carrega tudo que a viagem
precisa (contexto, documentos, acessos, combinado) e só então zarpa para a
entrega. Esta skill cuida da **ponte entre o "sim" e o começo do trabalho** — os
primeiros dias que decidem se a relação começa com confiança ou com atrito.

O que ela resolve, na prática:
- Cliente paga e some ("e agora?") → **boas-vindas** que dão o próximo passo.
- Trabalho não começa porque falta acesso/documento → **checklist + cobrança educada**.
- Cliente espera mais do que foi contratado → **combinado de escopo** anti-scope-creep.
- Kickoff bagunçado → **pauta + briefing** de largada.
- Vários clientes novos ao mesmo tempo → **painel de prontidão** com quem está travado.

## Como esta skill trabalha (leia primeiro)

- **A IA conversa; o motor conta.** Toda a parte exata (quem está em onboarding, %
  de prontidão, o que falta, o que está parado) vem do `scripts/cais.py` — um
  programa local, offline, só com biblioteca padrão do Python. A IA nunca "acha" um
  número: ela roda o motor e lê o resultado.
- **Nunca inventa.** Nome, serviço, resposta de intake, documento — se o dono não
  informou, fica visível como `[A PREENCHER]`/`[PENDENTE]`. Nada de dado fabricado.
- **Uma pergunta por vez.** No intake, vá em diálogo (pergunta → resposta → próxima),
  nunca um paredão. Não repita o que o cliente já respondeu.
- **O dono é quem envia.** A Cais monta a mensagem no tom do dono; quem manda ao
  cliente é o dono (WhatsApp-first ou o canal do `config.md`). A IA não dispara nada.
- **Dados 100% locais.** Tudo fica em `.cais/` na raiz do projeto. Nada sai da máquina.

## Primeira vez? Rode o setup

Se **não existe** `.cais/config.md`, esta é a primeira execução: abra
`setup/SETUP.md` e conduza o mini-setup (nome/negócio do dono, tipo de serviço
principal, canal e tom, tempo de resposta padrão). Ele grava `.cais/config.md` e
**se autodestrói** (a pasta `setup/` é apagada). Só rode uma vez.

Se `.cais/config.md` já existe, pule o setup e vá direto ao modo pedido.

## Os 6 modos

Descubra a intenção do dono e conduza o modo certo. Sempre feche cada interação com
a **próxima ação** (o motor te dá em `prontidao`/`painel`).

### 1. Receber (boas-vindas)
Cadastra o cliente novo e gera a mensagem de boas-vindas.
- Colete: nome, empresa, serviço contratado, valor, data de início, contato, canal.
  O que faltar, pergunte — não invente.
- Cadastre:
  ```bash
  python3 scripts/cais.py cliente-add --nome "<nome>" --empresa "<empresa>" \
    --servico "<serviço>" --valor "<R$...>" --inicio DD/MM/AAAA \
    --contato "<email/telefone>" --canal "<WhatsApp/e-mail>"
  ```
- Monte a **mensagem de boas-vindas** seguindo `references/mensagens.md` §1, no tom
  do `config.md`. O dono envia. (Esse é o marco "Recebido".)

### 2. Levantar (intake)
Monta o questionário de intake sob medida para o tipo de serviço.
- Abra `references/intake_por_area.md`, escolha o bloco da área e adapte ao serviço.
- Registre as perguntas escolhidas e, conforme o cliente responde, as respostas:
  ```bash
  python3 scripts/cais.py intake-add --slug <slug> --bloco "<bloco>" --pergunta "<...>"
  python3 scripts/cais.py intake-responder --slug <slug> --pergunta <nº|trecho> --resposta "<...>"
  python3 scripts/cais.py intake --slug <slug>        # ver o que já respondeu
  ```
- Uma pergunta/bloco por vez. Quando tudo estiver respondido, o marco "intake" fecha
  sozinho (ou marque com `marco --marco intake`).

### 3. Reunir (documentos & acessos)
Monta e acompanha a checklist do que o dono precisa para começar.
- Sugira os itens típicos do serviço (acessos, logins, logo, contrato, dados) e
  cadastre:
  ```bash
  python3 scripts/cais.py item-add --slug <slug> --item "<item>" --tipo acesso|documento|material [--opcional]
  python3 scripts/cais.py itens --slug <slug>                    # ver a checklist + % e pendentes
  python3 scripts/cais.py item-receber --slug <slug> --item <nº|nome>   # quando chegar
  ```
- Para o que estiver pendente, monte a **cobrança educada** (`references/mensagens.md`
  §2). O dono envia. Quando todos os obrigatórios chegam, o marco "documentos" fecha.

### 4. Combinar (escopo & expectativas)
Monta o "combinado" em linguagem simples — o anti-scope-creep na origem.
- Siga `references/fora_de_escopo.md`: o que está incluído, **o que NÃO está**,
  prazos, ritmo, o que depende do cliente, rodadas de ajuste.
- Escreva o combinado (salve o texto para o dono revisar/enviar). Ao fechar:
  ```bash
  python3 scripts/cais.py marco --slug <slug> --marco combinado
  ```

### 5. Largada (kickoff)
Prepara a reunião de início.
- Gere a **pauta do kickoff** + um **briefing de 1 minuto** (resumo do intake +
  pendências + o que confirmar) — `references/mensagens.md` §3.
- Depois da reunião:
  ```bash
  python3 scripts/cais.py marco --slug <slug> --marco kickoff
  ```

### 6. Painel (prontidão & travados)
A visão de gestão do onboarding.
```bash
python3 scripts/cais.py painel                 # todos, do menos ao mais pronto + parados
python3 scripts/cais.py prontidao --slug <slug> # os 5 marcos + % + próxima ação de um cliente
python3 scripts/cais.py parados --dias 5        # onboardings sem atividade há N+ dias
```
Quando um cliente chega a 100%, faça o **handoff**: entrega (Planta/Escuta/Pauta) e
retenção (Âncora).

## Os 5 marcos do onboarding (a espinha)

1. **Recebido** — cadastro feito + boas-vindas enviadas (automático ao cadastrar).
2. **Intake** — questionário respondido.
3. **Documentos** — todos os itens obrigatórios recebidos.
4. **Combinado** — escopo & expectativas alinhados.
5. **Kickoff** — reunião de largada realizada.

Prontidão = marcos feitos ÷ 5. 🔴 &lt;40% · 🟡 40–99% · 🟢 100%.

## Travas (o que a Cais nunca faz)
- Nunca inventa dado do cliente, resposta de intake, documento ou resultado.
- Nunca promete prazo/resultado que o dono não definiu.
- Nunca envia mensagem — só monta; **o dono envia**.
- O "combinado" **não é contrato jurídico** (isso é a skill Firma) — é alinhamento
  de expectativas em linguagem simples.
- Intake de saúde é administrativo, **nunca** coleta de dado clínico sensível de
  paciente. Dado sensível segue a LGPD e fica com o profissional.
- Dados 100% locais em `.cais/`.

## Onde a Cais se encaixa (handoffs)
Fisga (achar) → Esteira (pipeline) → Firma (contrato) → **Cais (onboarding)** →
Planta/Escuta/Pauta (entrega) → Âncora (retenção) → Aplauso (depoimento).

A Cais é o único elo que cuida do **começo da relação depois do "sim"** — o ritual
de receber, levantar, reunir, combinar e dar a largada.
