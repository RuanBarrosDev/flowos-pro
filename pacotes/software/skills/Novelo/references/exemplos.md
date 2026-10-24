# Exemplos por perfil — frases que disparam o Novelo e o que ele faz

O Novelo serve qualquer pessoa que tenha um projeto de código que cresceu e virou uma
bagunça — em especial quem construiu com IA sem ser programador de carreira.

---

## O professor que vibe-codou e se perdeu
> "Comecei um programa pra organizar minha biblioteca de eBooks com o Claude e virou uma
> teia imensa de scripts. Me perdi. Me ajuda a entender o que eu fiz?"

- **Desembolar:** mapa em PT — "seu projeto tem 14 arquivos; começa no `main.py`, que lê a
  pasta de eBooks (`scanner.py`), extrai os dados (`metadata.py`) e guarda numa planilha
  (`salvar.py`)."
- **Fios:** "esses 4 são o coração; os outros 10 são ajudantes. Tem 3 arquivos soltos que
  ninguém usa — provavelmente tentativas antigas."
- **Nós:** "achei 2 arquivos-rascunho (`scanner_v2.py`, `teste3.py`) e uma chave da API de
  livros escrita no código."
- **Desatar:** "vamos: 1) tirar a chave do código; 2) confirmar e apagar os 2 rascunhos;
  3) juntar a lógica repetida de leitura. Um por vez, conferindo que ainda lê seus eBooks."

## O consultor que herdou um sistema
> "Peguei pra tocar um sisteminha que outra pessoa fez com IA. Não sei nem por onde começar."

- **Desembolar + Fios:** dá a ele o mapa e o fluxo que o autor original nunca escreveu.
- **Rumo:** "onde mexo pra mudar o texto do e-mail?" → aponta o arquivo certo sem ele ter
  que ler tudo.

## O dono de negócio que "poliu ideias até virar bagunça"
> "Fui criando várias automações e agora tá tudo espalhado, não sei o que ainda uso."

- **Nós + Desatar:** separa o que está vivo do que é sobra, e limpa com segurança, sem
  apagar nada que ainda rode.

## O semi-técnico com um app quase pronto
> "Meu app funciona, mas tá uma zona por dentro. Antes de crescer, queria organizar."

- **Nós:** aponta arquivos gigantes e duplicação.
- **Desatar:** plano de refino em passos pequenos, cada um com conferência — sem parar o
  app que já funciona.

---

## Frases-gatilho (todas devem acionar o Novelo)
- "me perdi no meu projeto" · "virou uma bagunça / teia de scripts"
- "não entendo mais meu código" · "me explica esse projeto"
- "o que cada arquivo faz aqui?" · "mapeia meu projeto"
- "como esses arquivos se conectam?"
- "onde eu mexo pra fazer ___?"
- "tem código morto? tem coisa repetida? tem risco?"
- "herdei esse projeto, por onde começo?"
- "esse código tá uma zona, organiza sem quebrar tudo"

## O que o Novelo NÃO é (para não confundir a IA)
- **Não constrói projeto novo** (validar/desenhar/programar do zero é outra jornada).
- **Não caça UM bug específico** (isso é depuração metódica).
- **Não faz deploy / coloca no ar.**
- **Não reescreve o código sozinho** — ele mapeia, explica e planeja; a mão no código é do
  dono, um passo por vez.
