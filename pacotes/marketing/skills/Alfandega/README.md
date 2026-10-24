# Alfândega — Sourcing e Custo de Aterrissagem

Uma skill de Claude Code para quem compra produto para revender. A Alfândega descobre e compara
**fornecedores** e calcula o **custo de aterrissagem** (landed cost) — quanto um produto custa DE
VERDADE para chegar na sua prateleira, com **produto + frete internacional + seguro + impostos de
importação + câmbio + despachante** somados. Você conversa em português; a IA escreve as mensagens de
negociação e o motor faz as contas de imposto, o câmbio, a comparação e a nota de risco do fornecedor.

## O que ela faz (6 modos)
1. **Fornecedor** — cadastra quem te vende (país, produto, MOQ, prazo, Incoterm, pagamento).
2. **Risco** — avalia se o fornecedor é confiável, com uma nota 0-100 anti-golpe.
3. **Cotar** — o custo de aterrissagem real, em 3 regimes: importação **formal** (II, IPI, PIS/COFINS,
   ICMS por dentro, AFRMM, Siscomex), **simplificado** (Remessa Conforme) e compra **nacional**.
4. **Comparar** — ordena as cotações pelo custo UNITÁRIO real (não pelo preço do fornecedor).
5. **Câmbio** — converte e simula alta do dólar para você reservar folga na margem.
6. **Negociação** — a IA escreve as mensagens com o fornecedor (cotação, amostra, MOQ, Incoterm, fechamento).

## Como instalar
1. Baixe e descompacte a pasta `Alfândega`.
2. Coloque a pasta `Alfândega` dentro de `.claude/skills/` (no seu projeto ou em `~/.claude/skills/`).
3. Abra o Claude Code e fale naturalmente: *"quero importar fones da China"*, *"esse fornecedor é
   confiável?"*, *"quanto vou pagar de imposto para importar isso?"*.

Na primeira conversa a skill faz um setup rápido (nome do negócio, o que você importa, de onde, seu
estado para o ICMS, moeda). Depois é só conversar.

## Regras importantes
- **Nunca inventa** alíquota, NCM ou regra da lei — os números são **estimativa de planejamento** e a
  skill sempre manda confirmar no Simulador do Portal Único Siscomex e com o contador.
- **Anti-golpe primeiro**: amostra antes do pedido cheio, pagamento protegido, desconfiar do barato demais.
- **A IA prepara, você decide e fecha** a compra.
- **Dados locais e privados**: tudo fica em `.alfandega/` no seu computador (fora do Git).

## Requisitos
- Claude Code.
- Python 3 (só biblioteca padrão — nada para instalar).

Tudo funciona offline. Nenhum dado seu sai da sua máquina.
