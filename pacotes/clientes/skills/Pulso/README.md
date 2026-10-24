# Pulso — o sensor de satisfação dos seus clientes

O **Pulso** é uma skill de Claude Code que mede se os seus clientes estão
satisfeitos — e transforma isso em ação. Ele desenha a pesquisa, lê as respostas,
calcula a nota (NPS, CSAT ou CES), mostra se está subindo ou caindo, separa quem
você precisa recuperar de quem pode virar depoimento, e resume os comentários nos
temas que mais pesam. Tudo em português simples e **100% na sua máquina**.

## O que ele faz

- **Calcula NPS, CSAT e CES** a partir das suas respostas — sem você fazer conta.
- **Mostra a tendência** mês a mês (está melhorando ou piorando?).
- **Monta a fila de detratores** — quem reclamou, com o comentário, pronto para recuperar.
- **Lista os promotores** — quem te ama e pode virar depoimento e indicação.
- **Destila a voz do cliente** — agrupa os comentários abertos nos temas mais frequentes.
- **Desenha a pesquisa** e escreve os textos de recuperação no seu tom.

## Instalação

1. Descompacte o arquivo `Pulso.zip`.
2. Copie a pasta `Pulso` para dentro de `.claude/skills/` no seu projeto
   (ou em `~/.claude/skills/Pulso` para deixar disponível em qualquer pasta).
3. Abra o Claude Code nessa pasta. Na primeira vez, é só dizer algo como
   *"quero começar a medir a satisfação dos meus clientes"* — o Pulso conduz
   uma conversa rápida de configuração e cria a pasta `.pulso/` com seus dados.

## Como usar (você só conversa)

Você nunca digita comando nenhum — fala em português e o Pulso faz a conta por baixo.
Exemplos do que dizer:

- *"Qual o meu NPS?"*
- *"Como está a satisfação dos clientes esse mês?"*
- *"Quem está insatisfeito? Preciso recuperar."*
- *"Quem eu posso pedir depoimento?"*
- *"O que os clientes mais reclamam?"*
- *"Monta uma pesquisa de satisfação pra eu mandar no WhatsApp."*
- *"Colei aqui 30 respostas do Google Forms — organiza e me dá a leitura."*

## O que esperar

- **Nunca inventa nota.** Todo número vem das respostas que você registrou.
- **Tudo local.** As opiniões dos seus clientes ficam só na pasta `.pulso/` da
  sua máquina — nada é enviado para fora.
- **Sempre com contexto.** Toda nota vem com o tamanho da base e o período.
- **Você decide.** O Pulso mede e recomenda; a ação é sua.

## Requisitos

Apenas o **Python 3** que já vem no seu computador. Sem internet, sem conta, sem
chave de API, nada para instalar.

## Licença

MIT — use, adapte e compartilhe à vontade.
