# Novelo 🧶

**Perdeu-se no próprio projeto?** O Novelo desembaraça um projeto de código que já
existe e virou uma "teia de scripts": ele **lê** os arquivos que estão na sua máquina,
monta um **mapa em português** do que cada um faz, mostra **como eles se conectam**, acha
a **bagunça** (código morto, coisa repetida, arquivo gigante, senha exposta, falta de
teste) e te entrega um **plano de limpeza em passos pequenos e seguros**.

É a peça que faltava: quase tudo por aí te ajuda a **construir do zero**. O Novelo te
ajuda a **entender e arrumar o que você já tem** — sem precisar ser programador.

> O Novelo **não reescreve seu código**. Ele é o mapa e o guia. Quem dá cada passo de
> arrumação é você (ou o Claude, sob seu comando, um passo por vez, sempre conferindo que
> nada quebrou).

## Para quem é
Para quem construiu algo com IA (Claude Code, etc.) e o projeto cresceu até ninguém mais
entender; para quem **herdou** um sistema e não sabe por onde começar; para o
semi-técnico que quer organizar antes de crescer. Feito para **não-técnicos** — você só
conversa em português.

## O que ele faz (em 6 modos)
| Você diz | O Novelo faz |
|---|---|
| "desembola meu projeto" | Mapa em PT: o que cada arquivo faz |
| "como as peças se conectam?" | Diagrama das conexões + os arquivos mais importantes |
| "tem bagunça / risco aqui?" | Acha código morto, duplicação, arquivo gigante, senha exposta |
| "onde eu mexo pra fazer X?" | Aponta o arquivo certo (e o que não encostar) |
| "me dá um plano pra arrumar" | Roteiro de limpeza do mais seguro ao mais pesado |
| "como tá isso?" | Painel do estado + próximo passo |

## Como instalar
1. Descompacte a pasta `Novelo`.
2. Coloque-a dentro da sua pasta de skills do Claude Code:
   - só para este projeto: `SEU-PROJETO/.claude/skills/Novelo/`
   - para todos os projetos: `~/.claude/skills/Novelo/`
3. Abra o Claude Code **dentro do projeto que você quer entender** e comece a conversar.

## Como usar
Na primeira vez, o Novelo faz uma pergunta rápida (nome do projeto, o que faz, linguagem,
como roda) e guarda numa configuração local. Depois é só falar naturalmente:

> "Me perdi nesse projeto, desembola pra mim."
> "Como esses arquivos se conectam?"
> "Tem código que não serve pra nada aqui?"
> "Onde eu mexo pra mudar o texto do e-mail?"
> "Me dá um plano pra arrumar isso sem quebrar tudo."

O Claude aciona o Novelo sozinho e conduz você passo a passo.

## Suas garantias
- **Nunca inventa.** Só fala do que está de fato nos arquivos; o que é palpite vem marcado
  "possível — confirme".
- **Nunca reescreve o projeto.** Mapeia e planeja; a mão no código é sua.
- **Passo pequeno e seguro.** Nada de reescrever tudo de uma vez; cada passo vem com "como
  conferir que não quebrou".
- **Nunca vaza segredo.** Se acha uma senha no código, mostra mascarada — nunca o valor real.
- **100% na sua máquina.** Lê os arquivos localmente, offline. Nada sai do computador.

## Requisitos
Apenas **Python 3** (já vem no Mac e em Linux; no Windows, instale de python.org). Não
precisa instalar nenhum pacote. Funciona sem internet.

## Licença
MIT — use, adapte e compartilhe à vontade.
