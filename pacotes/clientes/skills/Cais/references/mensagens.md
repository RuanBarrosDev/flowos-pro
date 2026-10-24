# Modelos de mensagem — boas-vindas, cobrança de documentos e kickoff

A Cais **monta** o texto no tom do dono; **quem envia é o dono** (WhatsApp-first
ou o canal do `config.md`). Nunca dispare nada automaticamente. Nunca invente
resultado, prazo ou dado que o dono não tenha confirmado.

---

## 1) Mensagem de boas-vindas (modo Receber)

Enviada logo depois do "sim"/pagamento. Objetivo: confirmar o combinado, dizer o
que vem a seguir e matar a ansiedade de "e agora?". Estrutura:

1. **Comemora** de forma genuína ("Que alegria ter você comigo!").
2. **Confirma** em uma linha o que foi contratado.
3. **Próximos passos** (3–4 itens claros): responder o intake, enviar documentos,
   marcar o kickoff.
4. **Como a gente trabalha**: canal oficial e tempo de resposta.
5. **Fecho** com uma frase que olha pra frente.

**Exemplo (tom próximo, ajuste ao config.md):**
> Oi, [nome]! Que bom ter você comigo no [serviço]. 🎉
> Pra gente começar redondo, os próximos passos são:
> 1. Te mando um questionário rapidinho (5 min) pra eu entender o seu contexto.
> 2. Vou te pedir alguns acessos/documentos — assim que chegarem, eu já engato.
> 3. A gente marca uma conversa de largada de 30 min.
> Nosso canal oficial é o [canal] e eu costumo responder em até [tempo].
> Qualquer coisa é só me chamar por aqui. Bora pra cima! 🚀

---

## 2) Cobrança educada de documentos/acessos (modo Reunir)

A dor real: o cliente some e o trabalho não começa porque falta material. A
mensagem lembra sem soar chata, junta tudo que falta numa lista e facilita a vida.

**Regras:**
- Liste **só o que ainda falta** (o motor te dá com `itens`).
- Explique **por que** cada item destrava o trabalho ("com o acesso ao Gerenciador
  eu já subo a primeira campanha").
- Ofereça ajuda ("se tiver dúvida de onde achar, te mando o passo a passo").
- Uma cobrança leve; se já é a 2ª/3ª, suba o tom com gentileza e cite o impacto no prazo.

**Exemplo (1ª cobrança):**
> Oi, [nome]! Tô só a um passo de começar. Pra destravar, ainda preciso de:
> • [item 1] — [por que destrava]
> • [item 2] — [por que destrava]
> Se ficar mais fácil me mandar por aqui mesmo, pode ser. Qualquer dúvida de onde
> encontrar, me fala que te guio! 🙌

**Exemplo (lembrete, item parado há dias):**
> Oi, [nome]! Passando só pra não perder o embalo 😊 Ainda falta [item] pra eu
> começar [o quê]. Assim que você me mandar, engato na hora. Consegue hoje/amanhã?

---

## 3) Pauta da reunião de largada (modo Largada)

Objetivo: alinhar todo mundo antes do trabalho começar. Monte uma pauta curta:

1. **Boas-vindas + objetivo** (2 min): por que estamos aqui, o resultado que buscamos.
2. **Confirmar o combinado** (5 min): o que está incluído, o que não está, prazos.
3. **Revisar o intake** (10 min): confirmar o que o cliente respondeu, tirar dúvidas
   das pendências.
4. **Como vamos trabalhar** (5 min): canal, ritmo de atualização, quem aprova o quê.
5. **Plano da 1ª semana** (5 min): os 2–3 primeiros passos e o que cada lado faz.
6. **Próximo contato** (2 min): quando e como.

Antes da reunião, gere um **briefing de 1 minuto** para o dono chegar preparado:
resumo do intake + itens ainda pendentes + o que precisa confirmar na conversa.

Ao concluir o kickoff:
`python3 scripts/cais.py marco --slug <cliente> --marco kickoff`

---

## 4) Plano da 1ª semana (fecho do onboarding)

Depois do kickoff, entregue ao cliente um resumo simples do que vem: os primeiros
passos, o que você vai fazer, o que depende dele e quando terá a primeira novidade.
Isso transforma a expectativa em confiança e abre a porta para a entrega
(handoff para Planta/Escuta/Pauta) e a retenção (Âncora).
