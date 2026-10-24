# Começar pelo problema (não pela funcionalidade)

O erro mais caro de quem vai construir software é começar pela lista de telas e
botões. A pessoa diz "quero um app com dashboard, login e relatório" e seis meses
depois ninguém lembra por que o dashboard existe nem o que quebra se apagá-lo.

O Gabarito inverte a ordem: **primeiro o problema, depois a necessidade, só então
o requisito.** Cada peça que você vai construir tem que responder "que dor isso
resolve?". Se não responde, é enfeite — e enfeite atrasa, encarece e confunde.

## As três perguntas do enquadramento

Ao rodar `novo`, você define três coisas — e só o que o dono realmente disser:

1. **Para quem** é a solução? (quem vai usar no dia a dia)
2. Qual é o **problema central**? (a dor concreta, o que dói hoje SEM isso)
3. Em que **domínio** vive? (agendamento, loja, finanças, saúde, educação…)

Se o dono não sabe responder alguma, **não invente** — deixe [A CONFERIR] e
descubra na entrevista. Um problema central vago ("melhorar a gestão") não sustenta
uma especificação; puxe até o concreto: "hoje perco 20% dos agendamentos por
esquecimento" é um problema; "ser mais eficiente" não é.

## Como reconhecer um bom "problema central"
- Descreve uma **situação atual ruim**, não a solução desejada.
  - ✅ "pacientes faltam sem avisar e a agenda fica com buracos"
  - ❌ "quero um sistema de lembretes" (isso já é a solução — pode não ser a melhor)
- Tem **quem** sente e **com que frequência**.
- Dá para imaginar o **custo** de não resolver (tempo, dinheiro, erro, estresse).

Comece pelo problema e a solução certa aparece quase sozinha. Comece pela solução
e você constrói o que pediram — não o que precisavam.
