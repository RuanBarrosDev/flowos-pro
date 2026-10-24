# Emissário — monte o seu assistente de IA de atendimento

O **emissário** é quem fala e representa você onde você não pode estar. Esta skill do Claude Code monta
exatamente isso: um **assistente de IA que atende os seus clientes por você** — no seu tom, só com o que você
ensinou, e que chama um humano na hora certa.

Você **conversa em português**; o Emissário faz o trabalho de arquiteto e te entrega o **system prompt pronto** —
o texto que você cola no **GPT personalizado**, no **Projeto do Claude**, num **bot de WhatsApp** (ManyChat/
Typebot) ou no **chat do site**. Sem escrever uma linha de código.

## O que ele faz
Em 6 passos, guiados em conversa:
1. **Definir** — qual é o trabalho do assistente (missão, público, o que faz e o que NÃO faz).
2. **Persona** — o nome, a voz e o jeito de falar, na marca do seu negócio.
3. **Conhecimento** — a base de onde ele responde (serviços, preços, horários, políticas, FAQ). *O passo que mais importa.*
4. **Conversa** — os caminhos de atendimento (dúvida, orçamento, reclamação, "não sei", coleta de contato).
5. **Travas & Escalar** — o que ele nunca faz e quando passa para um humano.
6. **Montar & Testar** — gera o system prompt e um roteiro de 10 perguntas difíceis pra validar antes de subir.

## Por que é seguro
O system prompt gerado **já vem com travas**:
- **Não inventa** — responde só do que está na sua base; se não sabe, confirma com a equipe e escala.
- **Anti-"ignore as instruções"** — recusa quem tenta burlar ou ver o prompt.
- **Não promete resultado**, respeita **LGPD/dados sensíveis**, e sempre tem **porta de saída para um humano**.

## Instalar
1. Baixe e descompacte.
2. Copie a pasta `Emissário` para dentro de `.claude/skills/` do seu projeto (ou de `~/.claude/skills/` para
   usar em qualquer projeto).
3. Abra o Claude Code e diga algo como *"quero criar um assistente de IA pra atender meus clientes"*. A skill é
   acionada sozinha e faz o setup de primeira vez.

## Como usar (você só conversa)
- **"Quero um assistente de IA pro meu WhatsApp."** → o Emissário começa pelo setup e te leva pelos 6 passos.
- **"Vamos montar a base do meu assistente."** → entra no modo Conhecimento.
- **"Monta o system prompt e me dá o teste."** → gera o texto pronto + as 10 perguntas de validação.
- **"Como publico no WhatsApp?"** → passo a passo por plataforma.

Sob o capô, o Claude roda um pequeno motor em Python (offline, sem instalar nada, sem internet) que monta o
prompt, mede a prontidão e gera o roteiro de teste. Tudo fica numa pasta `.emissario/` no seu projeto — **100%
local, nada é enviado para fora**.

## Diferença para skills parecidas
- **Balcão** responde cada mensagem com você no comando; o **Emissário** constrói o assistente que atende sozinho.
- **Molde** cria skills de Claude Code (ferramenta de dev); o **Emissário** cria um assistente que fala com o cliente.
- **Prisma** faz um prompt avulso; o **Emissário** projeta um assistente inteiro (persona + base + fluxos + travas).

## Licença
MIT — veja `LICENSE`. Feito para a comunidade da Maestria Academy.
