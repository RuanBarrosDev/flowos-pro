# Testes instáveis (flaky) — por que "roda de novo que passa" é veneno

Um teste **instável** passa às vezes e falha às vezes sem nada ter mudado. Ele é traiçoeiro:
treina o dono a ignorar o vermelho ("ah, é aquele teste chato de sempre") — e no dia em que o
vermelho for um bug de verdade, ninguém vai acreditar. Instabilidade se conserta pela **raiz**,
nunca com "roda de novo até passar".

## O catálogo das causas (o que procurar)
- **Espera por tempo fixo:** o teste "espera 2 segundos" e torce para a tela estar pronta. Em
  máquina lenta, falha. **Conserto:** esperar pela condição ("espere o botão aparecer"), não pelo
  relógio.
- **Corrida (race condition):** o teste checa antes de a ação terminar. **Conserto:** aguardar o
  resultado real acontecer.
- **Estado compartilhado:** um teste deixa lixo (um registro, um arquivo, um usuário logado) que
  bagunça o próximo. **Conserto:** cada teste cria o que precisa e limpa depois; nenhum depende do
  outro.
- **Dependência de ordem:** a suíte só passa se rodar na ordem X. **Conserto:** cada teste tem que
  passar sozinho, em qualquer ordem.
- **Seletor frágil (telas):** o teste procura o elemento por texto que muda, por posição, ou por
  um caminho gigante que quebra a cada ajuste visual. **Conserto:** apontar para marcas estáveis
  (um identificador de teste, um papel/rótulo acessível), não para a aparência.
- **Dados/tempo/aleatório:** o teste depende da data de hoje, de um número sorteado, do fuso.
  **Conserto:** fixar esses valores no teste.
- **Ambiente externo:** o teste chama um serviço de terceiro de verdade que às vezes está fora.
  **Conserto:** simular a fronteira externa; deixar a chamada real só para pouquíssimos testes
  marcados.

## Como o Ensaio trata a instabilidade num Diagnóstico/Conferência
- Se um teste falhou por **instabilidade** (não por bug real), **diga isso claramente** ao dono e
  não mande consertar o app — o app não tem culpa de um teste mentiroso. Ofereça a **Faxina**.
- Na Faxina, ao reescrever um teste instável, **re-prove que ele ainda é capaz de falhar** pelo
  motivo certo — a armadilha é "estabilizar" um teste tirando dele justamente a verificação que
  importava.

## O teste de sanidade da faxina
Depois de consertar, rode a suíte algumas vezes seguidas. Se ela dá o mesmo resultado toda vez,
ganhou estabilidade. Se ainda oscila, a causa-raiz não foi encontrada — não declare resolvido.
