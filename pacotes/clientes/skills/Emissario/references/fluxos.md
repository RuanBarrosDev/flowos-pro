# Modo Conversa — os fluxos

Um assistente bom não é uma FAQ que devolve texto: ele **conduz** a conversa. Aqui você desenha os caminhos
mais comuns, em linguagem simples. Escreva em `.emissario/fluxos.md`. Não precisa de fluxograma técnico — é
"quando o cliente diz X, o assistente faz Y".

## Os caminhos que quase todo negócio tem
1. **Abertura** — cumprimenta (usa a saudação da persona), pergunta em que pode ajudar.
2. **Entender a necessidade** — 1 pergunta para saber o que a pessoa quer, antes de despejar informação.
3. **Tirar dúvida** — responde pela base; se não estiver na base, vai pro caminho "não sei".
4. **Orçar / agendar** (se o negócio faz) — coleta o mínimo (o que precisa, quando, contato) e encaminha
   ou informa como funciona.
5. **Reclamação** — acolhe, não discute, pede desculpa quando cabe, e escala para humano.
6. **"Não sei" (fora da base)** — não inventa; diz que vai confirmar com a equipe, pega o contato e escala.
7. **Encerramento** — confirma se resolveu, deixa a porta aberta.

## Modelo para `fluxos.md`
```markdown
# Fluxos de conversa

## Abertura
[saudação] → "Como posso ajudar?" → escuta antes de responder.

## Dúvida
Responde pela base. Se a resposta não estiver na base → caminho "Não sei".

## Orçamento / agendamento
Coleta: [o que precisa] + [quando] + [nome e contato]. Depois: [informa preço da base OU encaminha para a equipe].

## Reclamação
Acolhe → pede desculpa se cabe → NÃO discute → escala para [humano].

## Não sei (fora da base)
"Ótima pergunta — deixa eu confirmar isso com a equipe pra te passar certo. Qual o melhor contato?" → escala.

## Coleta (educada, um dado por vez)
Nome → melhor contato → o que precisa. Explica por que pergunta. Se não quiser dar, tudo bem.
```

## Dicas
- **Uma pergunta por vez.** Interrogatório afasta. Pede o próximo dado só quando precisar.
- **Escuta antes de despejar.** Melhor "o que você procura?" do que colar a tabela de preços inteira.
- **Todo caminho tem saída.** Nenhum fluxo termina no vazio — ou resolve, ou coleta e escala.
- Adapte à realidade do negócio: um restaurante tem "reserva/cardápio"; uma clínica tem "agendar/convênio";
  uma agência tem "briefing/orçamento". Pergunte ao dono quais são os 3-4 caminhos que mais chegam.
