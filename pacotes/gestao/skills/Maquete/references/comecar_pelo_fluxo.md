# Começar pelo fluxo, não pela tela

O erro nº 1 de quem desenha software é começar listando telas bonitas ("preciso de
uma home, uma tela de perfil, um dashboard..."). O resultado são telas soltas que
não conversam e um produto que ninguém consegue usar de ponta a ponta.

**A ordem certa é a inversa:**

1. **Qual a tarefa?** O que a pessoa quer CUMPRIR? (marcar um horário, emitir um
   orçamento, ver quanto vendeu no mês). Um produto existe para cumprir tarefas.
2. **Quem faz essa tarefa?** A persona (a recepcionista, o dono, o cliente final).
   Cada uma enxerga o produto de um jeito.
3. **Em que ordem?** A jornada tela-a-tela: abre onde, clica no quê, vai para onde,
   termina em quê. Isso é o fluxo.
4. **Só então: quais telas esse fluxo precisa?** As telas nascem do fluxo. Se uma
   tela não aparece em nenhum fluxo, pergunte: para que ela serve? Provavelmente é
   uma tela órfã — corte ou ligue a um fluxo.

## O primeiro fluxo é o mais importante
Comece pela **tarefa nº 1** — a razão de o produto existir. Se um app de agenda não
deixa marcar um horário em poucos cliques, nada mais importa. Desenhe esse fluxo
inteiro e navegável ANTES de partir para os secundários (configurações, perfil,
relatórios). Um fluxo principal impecável vale mais que dez telas pela metade.

## Sinais de um fluxo bem desenhado
- Tem começo (onde a pessoa entra) e fim (a confirmação de que deu certo).
- Cada passo leva ao próximo com UMA ação clara.
- Não tem beco-sem-saída no meio (tela sem para onde ir).
- Você consegue narrar em uma frase: "abre em X, faz Y, confirma em Z".

## Como registrar
- `fluxo-add` cria o fluxo com a ordem das telas (`--telas "T.01, T.02, T.03"`).
- As telas citadas podem ainda não existir — desenhe-as no passo seguinte (`tela-add`)
  e o fluxo já as encontra.
- `fluxo-set --telas ...` reordena quando você perceber que faltou um passo (quase
  sempre falta a **tela de confirmação** no fim).
