# Modo Conhecimento — a base de onde o assistente responde

Este é **o passo que mais pesa**. Tudo que o assistente pode afirmar tem que estar aqui — porque a regra de
ouro do system prompt é: **responde só do que está na base; se não achar, não inventa e escala.** Uma base boa
é o que separa um assistente confiável de um que fala bobagem. Escreva em `.emissario/base.md`.

## O que cobrir (ajude o dono a preencher cada bloco)
- **O que o negócio faz** — em 2-3 frases claras.
- **Serviços/produtos** — lista com o nome que o cliente usa + o que inclui.
- **Preços e condições** — valores reais, formas de pagamento, parcelamento, o que está/não está incluso.
  (Se o preço "depende", escreva a regra: "avaliação gratuita, orçamento após avaliar".)
- **Horários e endereço** — dias, horas, localização, atendimento online/presencial.
- **Políticas** — remarcação, cancelamento, garantia, prazo, devolução — o que costuma gerar dúvida.
- **FAQ** — as 8 a 15 perguntas que mais chegam, com a resposta certa. (Se o dono tem um Balcão/base pronta,
  aproveite.)
- **O que ele deve encaminhar** — assuntos que existem mas o assistente não resolve (ex.: "casos clínicos → a
  doutora", "financeiro em atraso → o financeiro").

## Formato de `base.md` (livre, mas organizado por títulos)
```markdown
# Base de conhecimento — [Negócio]

## Sobre
[o que fazemos]

## Serviços e preços
- [Serviço] — [o que inclui] — [preço/condição]
- ...

## Horários e endereço
[dias e horas] · [endereço / online]

## Políticas
- Remarcação: [regra]
- Pagamento: [formas]
- ...

## Perguntas frequentes
**[Pergunta]?** [Resposta certa.]
**[Pergunta]?** [Resposta certa.]
```

## Regras de qualidade
- **Nada de "achismo".** Só entra o que é verdade e o dono confirma. Preço chutado vira problema real.
- **Cubra as lacunas óbvias agora.** Pergunte ativamente o que costuma faltar (preço, horário, "atende
  convênio?", "faz a domicílio?"). Cada buraco na base é um lugar onde o assistente vai ter que escalar.
- **O que não está na base, o assistente não afirma.** Isso é proposital e seguro — melhor "vou confirmar"
  do que uma informação errada. Deixe o dono tranquilo: a base cresce com o tempo.
- Se o dono não sabe uma resposta agora, **não invente** — marque `[PREENCHER: ...]` e siga.
