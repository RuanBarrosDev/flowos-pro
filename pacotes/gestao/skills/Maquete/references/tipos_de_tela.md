# Catálogo de tipos de tela (e o que cada uma costuma ter)

Use isto para propor telas completas — não esquecer os blocos que quase sempre
faltam. Passe o `--tipo` correspondente no `tela-add`; ele só organiza, o desenho
vem dos `--blocos`.

## login / cadastro
Entrar ou criar conta. Costuma ter: `titulo`, `campo: E-mail`, `campo: Senha`,
`botao: Entrar -> (tela inicial)`, `link: Esqueci a senha -> (recuperar)`,
`link: Criar conta -> (cadastro)`. Não esqueça a tela de **recuperar senha**.

## onboarding
Os primeiros passos de quem acabou de entrar. Poucas telas, uma ideia por tela,
sempre com `botao: Próximo` e um `link: Pular`. Termina levando à tela inicial.

## dashboard / painel
A visão geral. Costuma ter: `titulo`, alguns `metrica: rótulo | valor` (os números
que importam), uma `tabela` ou `lista` do que é recente, um `botao` de ação principal
e uma `nav` para as outras áreas.

## lista / índice
Uma coleção (clientes, pedidos, produtos). Costuma ter: `titulo`, `campo: Buscar`,
filtros (`selecao`), a `lista`/`tabela`, e um `botao: Novo -> (formulário)`. Cada
item da lista idealmente leva ao **detalhe** (`link -> T.xx`).

## detalhe
Uma coisa só, a fundo (um cliente, um pedido). Costuma ter: `titulo` (o nome do
item), `texto`/`card` com os dados, e `botao: Editar` / `botao: Excluir`.

## formulário
Criar ou editar. Costuma ter: `titulo`, vários `campo`/`area`/`selecao`,
`botao: Salvar -> (volta pra lista/detalhe)` e `link: Cancelar -> (volta)`. Pense no
que acontece **depois de salvar** (volta pra onde? mostra confirmação?).

## confirmação / sucesso
A tela que diz "deu certo". Quase sempre esquecida — e é ela que fecha o fluxo.
Costuma ter: `titulo: Pronto!`, `texto` do que foi feito, `botao: Voltar ao início`.

## busca / resultados
`campo: Buscar`, filtros, e a `lista`/`tabela` de resultados — mais o **estado vazio**
("nada encontrado").

## checkout / pagamento
Resumo do pedido (`card`/`tabela`), dados de pagamento (`campo`), `botao: Pagar` e a
tela de **confirmação** depois.

## perfil / configurações
Dados da conta e preferências: `campo`s, `selecao`s, `botao: Salvar`. Costuma ter
`abas` (Conta / Notificações / Segurança).

## vazio / erro (estados, não telas separadas)
Toda lista/dashboard precisa de uma versão **vazia** (primeiro acesso: "você ainda
não tem X, comece por aqui") e de uma versão **erro** ("algo deu errado, tente de
novo"). Marque com `--estado vazio` ou `--estado erro` e um `aviso:` no corpo. Veja
`estados_e_vazios.md`.
