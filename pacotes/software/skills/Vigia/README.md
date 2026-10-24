# Vigia — o plantão do seu sistema no ar

Você colocou um site, app, loja, automação, bot ou agente **no ar**. Ótimo. Mas
e agora — como você sabe que ele **continua funcionando**? Hoje, quase sempre, a
resposta é: *você descobre pelo cliente reclamando.* A **Vigia** muda isso.

A Vigia é uma skill de Claude Code que faz o **plantão do seu sistema depois que
ele já está no ar**. Ela fala a sua língua — dono de negócio, não engenheiro — e
trabalha em três momentos:

- **Antes (Sensores):** monta uma vigilância simples para você ser avisado
  **antes do cliente**.
- **Durante (Plantão):** quando algo quebra, ela classifica a gravidade,
  estabiliza primeiro, levanta as causas mais prováveis com base no sinal real,
  guia o conserto e redige a mensagem honesta ao cliente.
- **Depois (Autópsia):** faz a revisão sem culpa para o mesmo problema não voltar
  — e liga o sensor que faltava.

## Como instalar

1. Baixe e **descompacte** a pasta `Vigia`.
2. Coloque a pasta `Vigia` dentro da pasta de skills do seu Claude Code:
   - no seu projeto: `.claude/skills/Vigia/`, **ou**
   - para todos os projetos: `~/.claude/skills/Vigia/`
3. Abra o Claude Code e diga algo como **"quero montar a vigilância do meu
   sistema"** ou **"meu site caiu"**. A Vigia dispara sozinha.

## A primeira conversa

Na primeira vez, a Vigia te faz algumas perguntas simples para montar o **Cartão
de Saúde** do seu sistema (o quê é, o endereço, o que é "normal", onde ficam os
erros, quem avisar) e já liga o primeiro sensor. Depois disso, o arquivo de
setup some sozinho e é só conversar.

## O que você fala (não precisa saber comandos)

| Você diz | A Vigia faz |
|---|---|
| "dá uma checada no meu site agora" | acessa seu endereço e diz se está no ar, em quanto tempo respondeu |
| "meu site caiu / está lento / deu erro" | abre o plantão: gravidade, estabilizar, causas prováveis, conserto, mensagem ao cliente |
| "vamos fazer a autópsia do que aconteceu" | revisão sem culpa + o sensor novo para não repetir |

## O contrato dela
- **Nunca inventa a causa** — só conclui do sinal real (separa fato de hipótese).
- **Estabilizar primeiro, entender depois.**
- **Você no comando da comunicação** — ela redige, você envia.
- **Seus dados ficam com você** — tudo em arquivos locais na pasta `vigia/`.
- **Fora do escopo, ela encaminha:** ataque/golpe → Baluarte · bug em
  desenvolvimento → Rastro · testes antes de subir → Ensaio · colocar no ar → Órbita.

## Requisitos
Apenas Python 3 (já vem no Mac e no Linux). Zero instalação, zero conta, zero
API paga. A única parte que acessa a internet é a checagem do **seu próprio
endereço** — nada é enviado para fora.

## Licença
MIT. Use, adapte e compartilhe.
