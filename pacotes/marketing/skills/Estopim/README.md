# Estopim — o que acende a campanha

**Estopim** é uma skill para o Claude Code que transforma um negócio, produto ou lançamento numa
**grande ideia de campanha** coerente — do briefing ao conceito, do desdobramento por canal ao
manifesto — e ainda passa tudo por um crítico cego antes de você apresentar ao cliente.

Não é gerador de tagline solta. Cada ideia nasce presa ao objetivo de negócio e ao público real,
e é reprovada se for genérica. Feito para agências, publicitários, estrategistas, designers,
produtores de conteúdo, social media e donos de negócio que precisam de **conceito criativo** —
não só de execução.

## O que ela faz (6 modos)
1. **Briefing** — monta o briefing criativo perguntando só o essencial.
2. **Insight** — encontra a verdade humana / tensão em que a campanha se apoia.
3. **Ideia** — gera 3 conceitos de campanha distintos (grande ideia + plataforma + porquê).
4. **Desdobramento** — desdobra o conceito escolhido por canal (reel, story, anúncio, e-mail, LP).
5. **Manifesto** — escreve o manifesto + roteiros de vídeo + set de headlines.
6. **Crivo** — crítico cego que pontua contra o briefing e lista lacunas por impacto.

## Como instalar
1. Descompacte o arquivo `Estopim.zip`.
2. Copie a pasta **`Estopim`** para dentro da pasta de skills do seu Claude Code:
   - Para usar em qualquer projeto: `~/.claude/skills/Estopim`
   - Ou dentro de um projeto específico: `.claude/skills/Estopim`
3. Pronto. O Claude Code detecta a skill sozinho.

## Como usar
Abra o Claude Code na pasta do cliente/projeto onde você quer trabalhar e simplesmente **converse**:

- **Primeira vez:** diga *"quero criar uma campanha"* — o Estopim faz uma configuração curta (6
  perguntas sobre a marca), grava o contexto localmente e some com a etapa de setup.
- **No dia a dia:** fale naturalmente:
  - *"Monta o briefing dessa campanha de lançamento."*
  - *"Me dá a grande ideia pra essa promoção."*
  - *"Desdobra esse conceito em reel, story e e-mail."*
  - *"Escreve o manifesto e um roteiro de reel."*
  - *"Critica esse conceito antes de eu apresentar pro cliente."*

Você conversa; a IA pensa e escreve. Por baixo, um pequeno motor em Python (que já vem no seu
computador — não instala nada) organiza os arquivos da campanha numa pasta `.estopim/` ao lado do
seu material.

## O que esperar
- **Nunca inventa dado do negócio ou do mercado.** Onde falta informação, marca `[PREENCHER]` e
  pede a você.
- **Toda ideia amarrada ao objetivo.** Criatividade que não serve o briefing é reprovada no Crivo.
- **Sugere; você decide e envia.** O Estopim entrega o conceito e as peças; publicar, agendar e
  comprar mídia é com você (ou com as ferramentas de execução).
- **Seu contexto é local.** Tudo mora em `.estopim/` na sua máquina e entra no `.gitignore`. Nada
  sai do seu computador.

## Requisitos
- Claude Code instalado.
- Python 3 (já vem no macOS e na maioria dos Linux; no Windows, instale pelo site oficial).
- Nenhuma chave de API, nenhuma conta, nenhum serviço externo.

## Licença
MIT — use, adapte e distribua livremente.
