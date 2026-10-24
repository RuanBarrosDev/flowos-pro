# Amarra — a proposta que amarra o negócio

**Amarra** é uma skill de Claude Code para donos de negócio de serviço que vendem por reunião: leva uma
oportunidade B2B do "tenho uma reunião marcada" ao "cliente assinou". Ela cuida do **meio da venda
consultiva** — prepara a reunião de descoberta, entende a dor de verdade, quantifica o valor e monta a
**proposta consultiva que vende** (não um orçamento seco de preço), mais uma biblioteca de objeções.

Você só conversa em português. Por baixo, um motor Python (biblioteca padrão, **offline**) guarda tudo
em `.amarra/` na raiz do projeto. **Nunca inventa a dor, o número, o decisor ou o preço, e nunca acessa
a internet.** Nomes e valores de clientes ficam 100% no seu computador (LGPD).

## Como instalar

1. Baixe e descompacte a pasta `Amarra`.
2. Copie-a para dentro de `.claude/skills/` do seu projeto (ou de `~/.claude/skills/` para deixá-la
   disponível em qualquer projeto):
   ```
   .claude/skills/Amarra/
   ```
3. Abra o Claude Code nesse projeto. Na primeira vez que você pedir algo de venda/proposta, a skill
   dispara sozinha e conduz um **setup rápido** (nome do negócio, moeda, o que você vende).

## Como usar (você só conversa)

- "Tenho uma reunião com a empresa X na quinta, me ajuda a preparar" → ela monta o **roteiro de
  descoberta**.
- "A reunião foi assim: eles perdem 30% dos leads, quem decide é o Piero..." → ela **captura** e
  **qualifica** a oportunidade (nota 0-100 + lacunas).
- "Monta a proposta pra eles" → ela gera a **proposta consultiva completa** com 3 opções, ROI, riscos
  e próximo passo, pronta pra você revisar e enviar.
- "O cliente disse que tá caro" → ela traz o **reframe** certo pra objeção.

O que a Amarra faz é **preparar e redigir**. Quem conduz a reunião e envia a proposta é sempre você — a
venda é uma conversa humana.

## O que a diferencia

Uma IA comum, pedida pra "montar uma proposta", inventa um texto genérico que não cita o cliente e
chuta um preço. A Amarra faz o oposto: tudo na proposta vem do que **você capturou** na descoberta,
nas palavras do cliente; o que falta aparece como **[A CONFERIR]**; e ela **nunca chuta preço** — monta
as 3 opções e deixa você definir os valores. É o que faz uma proposta *vender*: mostrar que ouviu.

## Requisitos

- Claude Code
- Python 3 (já vem no macOS e na maioria dos Linux)
- Nenhuma chave de API, nenhuma conta, nenhum acesso à internet.

## Licença

MIT — veja `LICENSE`.
