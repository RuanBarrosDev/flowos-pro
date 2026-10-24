# Os estados de tela que quase todo mundo esquece

Todo desenhador de software desenha a tela "cheia e feliz" — a lista com 10 itens, o
dashboard com números bonitos. E esquece os três estados que o usuário vive na vida
real. Eles são a diferença entre um produto que parece pronto e um que realmente é
usável.

## 1. Estado VAZIO (o primeiro acesso)
No primeiro dia, a lista está vazia, o dashboard está zerado. Se a tela só mostra
"nenhum resultado", o usuário novo se sente perdido. O estado vazio bem-feito **ensina
o próximo passo**: "Você ainda não cadastrou nenhum cliente. Comece por aqui →".
- Marque com `--estado vazio`.
- No corpo, troque a `lista`/`tabela` cheia por um `aviso:` amigável + um
  `botao: Cadastrar o primeiro -> (formulário)`.

## 2. Estado de CARREGANDO
Enquanto o sistema busca os dados, a tela não pode ficar em branco (parece travada).
- Marque com `--estado carregando`.
- É o próprio lo-fi da Maquete: as linhas de tabela já vêm como "esqueleto" cinza,
  que é exatamente como se mostra carregamento.

## 3. Estado de ERRO
Deu errado (sem internet, dado inválido, servidor fora). O usuário precisa entender o
que houve e como sair — nunca um beco-sem-saída.
- Marque com `--estado erro`.
- No corpo: `aviso: Não foi possível carregar. Tente de novo.` +
  `botao: Tentar de novo -> (a própria tela)` e/ou `link: Voltar`.

## Também não esqueça
- **Confirmação de sucesso** — a telinha "Pronto! Seu horário foi marcado." que fecha
  o fluxo. Sem ela, o usuário não sabe se deu certo.
- **Confirmação destrutiva** — antes de excluir, um `aviso:` "Tem certeza?" com
  `botao: Sim, excluir` e `link: Cancelar`.

## Regra prática
Para cada tela que mostra uma lista ou dados, pergunte: **"E quando estiver vazia? E
carregando? E se der erro?"**. Desenhar esses estados agora (baratos, no wireframe)
evita um produto que quebra na cara do primeiro usuário real.
