# Aceno — reativação de clientes que sumiram (win-back)

O **Aceno** é a skill que traz de volta quem já foi seu cliente e esfriou. Ele
olha a sua carteira, mede quem parou de comprar, diz quem vale a pena chamar
primeiro, ajuda a entender por que a pessoa sumiu, escolhe o motivo certo para
ela voltar e escreve o aceno — a mensagem calorosa que reabre a relação sem
parecer desespero nem spam.

Reativar cliente antigo é o dinheiro mais barato do negócio: ele já te conhece e
já confiou. O Aceno ajuda a resgatar o faturamento que está parado na sua base.

## O que ele faz

- **Termômetro da carteira** — mostra quantos clientes estão Ativos, Esfriando,
  Dormindo ou Perdidos, e quanto dinheiro está parado fora da faixa Ativa.
- **Fila de resgate** — ordena quem abordar primeiro (valor do cliente × chance
  de voltar), para você não travar diante da base inteira.
- **Diagnóstico** — levanta a hipótese de por que a pessoa sumiu (esqueceu,
  concorrente, preço, experiência ruim, necessidade mudou, sazonal).
- **Isca de retorno** — o motivo certo para voltar, começando pelos mais baratos
  e honestos, deixando desconto por último.
- **Mensagem** — escreve o aceno personalizado por faixa e canal (WhatsApp/e-mail).
- **Cadência & painel** — a sequência de 3 toques e a conta final: quantos
  voltaram, taxa de retorno e valor recuperado.

## Como instalar

1. Descompacte o arquivo `Aceno.zip`.
2. Copie a pasta `Aceno` para dentro da sua pasta de skills do Claude Code:
   - no projeto: `.claude/skills/Aceno/`
   - ou global: `~/.claude/skills/Aceno/`
3. Abra o Claude Code e comece a conversar. Na primeira vez, o Aceno faz algumas
   perguntas rápidas (nome do negócio, ramo, de quanto em quanto tempo o cliente
   costuma voltar) e já fica pronto.

## Como usar (você só conversa)

Você fala com o Aceno em português, do jeito natural. Por baixo, ele roda as
contas sozinho. Frases que acionam:

- "Meus clientes somem e não voltam, como recupero?"
- "Quem parou de comprar comigo?"
- "Quero reativar minha base."
- "Faz tempo que o fulano não aparece, o que eu mando pra ele?"
- "Monta uma campanha de retorno."

Traga sua lista de clientes (uma planilha, uma exportação do sistema, ou só os
que você lembra) e o Aceno começa a medir quem esfriou.

## Suas regras de ouro (o que esperar)

- **Nunca inventa** cliente, data ou valor — tudo vem da sua base.
- **Não é spam** — no máximo 3 toques espaçados por cliente.
- **Desconto não é a primeira isca** — ele protege sua margem.
- **Ele prepara, você envia** — o tom verdadeiro com o cliente é seu.
- **Seus dados ficam no seu computador** — a carteira nunca sai da pasta `.aceno/`.

## Requisitos

- Claude Code.
- Python 3 (já vem no macOS e na maioria dos Linux). O motor usa só a biblioteca
  padrão — não instala nada, não acessa a internet.

## Licença

MIT — veja o arquivo `LICENSE`. Skill original, escrita para a comunidade.
