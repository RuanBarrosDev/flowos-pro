---
name: alfandega
description: >-
  Descobre, negocia e compara FORNECEDORES e calcula o CUSTO DE ATERRISSAGEM (landed cost) — quanto um
  produto custa DE VERDADE para chegar na sua prateleira: preço do produto + frete internacional +
  seguro + impostos de importação + câmbio + despachante. Use quando o dono falar de importar, importação,
  fornecedor, sourcing, comprar da China/Alibaba/exterior, custo de importação, quanto vou pagar de
  imposto, II/IPI/ICMS/PIS/COFINS na importação, NCM, valor aduaneiro, frete internacional, câmbio na
  compra, comparar orçamento de fornecedor, negociar com fornecedor, MOQ, Incoterm (FOB/CIF), amostra,
  golpe de fornecedor, ou "esse fornecedor é confiável?". Conversa em português, escreve as mensagens de
  negociação no tom do dono, NUNCA inventa alíquota/NCM/lei (marca estimativa e manda confirmar no
  simulador oficial), e quem fecha a compra é o dono.
---

# Alfândega — Sourcing e Custo de Aterrissagem

A **alfândega** é a fronteira por onde a mercadoria entra — e o lugar onde o preço "barato" do
fornecedor vira o custo real com imposto, frete e câmbio somados. Esta skill cuida de **de onde o
produto vem e quanto ele CUSTA DE VERDADE para chegar na prateleira**.

É a camada **ANTES** do estoque e do anúncio na jornada do produto:
- **Alfândega** (esta) — o fornecedor e o custo de aterrissagem (o que você paga para ter o produto).
- **Celeiro** — estoque, giro, capital parado (o produto já comprado, dentro de casa).
- **Fiel** — o preço de venda; **Mostruário** — o anúncio; **Alcance** — o SEO.

O membro só conversa em português. Por baixo, você (a IA) **escreve as mensagens de negociação no tom
dele** e traduz o resto em comandos do motor `scripts/alfandega.py` (Python, biblioteca padrão,
offline). O motor guarda tudo em `.alfandega/` na raiz do projeto e cuida da parte **verificável**: as
**contas de imposto e custo de aterrissagem**, a **conversão de câmbio**, a **comparação** de cotações
pelo custo unitário real, e a **nota de risco** do fornecedor.

**NUNCA invente alíquota, NCM ou regra da lei.** As alíquotas de referência do motor são **estimativas
de planejamento** — sempre mande o dono confirmar no NCM/simulador oficial (Portal Único Siscomex) e
com o contador antes de comprar. **Quem fecha a compra é o dono.**

## Quando usar
Dispare quando o dono falar de:
- "quero **importar** X", "comprar da **China / Alibaba / exterior**", "achar **fornecedor**"
- "quanto vou pagar de **imposto** pra importar?", "**custo de importação**", "**landed cost**"
- "**II / IPI / ICMS / PIS / COFINS** na importação", "**NCM**", "**valor aduaneiro**", "**AFRMM**"
- "esse **fornecedor é confiável**?", "como não cair em **golpe**?", "pedir **amostra**"
- "me ajuda a **negociar** com o fornecedor", "**MOQ**", "**Incoterm** (FOB/CIF)", "prazo"
- "qual dos **dois fornecedores** compensa?", "o mais barato é mesmo o melhor?"
- "o **câmbio** subiu, muda meu custo?", "quanto reservar de folga no dólar?"

Serve para quem compra **produto** para revender: importador, e-commerce, loja, atacado, revenda,
recommerce, representante — e também compra nacional (o motor tem o regime `nacional`).

## Primeira conversa (setup — só uma vez)
Se **não existir** `.alfandega/config.md`, rode o setup antes de qualquer comando:
1. Leia `setup/SETUP.md` e conduza a conversa em PT-BR que ele descreve (nome do negócio, o que
   costuma importar/comprar, de quais países, estado da empresa para o ICMS, moeda mais usada).
2. Grave as respostas em `.alfandega/config.md` (o SETUP.md tem o modelo exato).
3. Garanta `.alfandega/` no `.gitignore` (preço, custo e fornecedor são privados).
4. **Apague a pasta `setup/`** — ela é só do primeiro uso.
5. Rode `python3 <pasta-desta-skill>/scripts/alfandega.py init` para criar os arquivos de dados vazios.

## Como você trabalha (os 6 modos)

Sempre invoque o motor com o caminho desta skill, ex.:
`python3 <pasta-desta-skill>/scripts/alfandega.py <comando>`. Traduza a fala do dono para o comando
certo, **escreva as mensagens você mesmo** no tom dele, mostre a saída em PT-BR e explique simples.

### 1) Fornecedor — o cadastro de quem te vende
Quando o dono mencionar um fornecedor, cadastre: nome, país, produto, contato, MOQ (pedido mínimo),
prazo, forma de pagamento, Incoterm, moeda.
`fornecedor-add --nome "..." --pais China --produto "..." --moq 500 --prazo 35 --incoterm FOB --moeda USD`
Liste com `fornecedores`. **Nunca invente dados do fornecedor** — se não souber, deixe em branco e
pergunte.

### 2) Risco — o fornecedor é confiável? (anti-golpe)
Antes de pagar qualquer coisa, avalie o fornecedor contra o checklist anti-golpe. Pergunte ao dono
quais itens estão OK e marque:
`risco --fornecedor F001 --sim amostra,pagamento_protegido,empresa_verificada,referencias`
O motor dá uma **nota 0-100** e o **nível** (🔴 alto / 🟡 médio / 🟢 baixo) e lista o que falta resolver.
Regra de ouro que você deve reforçar: **preço bom demais é o principal sinal de golpe**; nunca pague
por PIX/TED direto sem proteção; sempre peça amostra antes do pedido cheio.

### 3) Cotar — o CUSTO DE ATERRISSAGEM (o coração da skill)
Esse é o cálculo que muda tudo. Pegue os números do dono e rode o custo real. Três regimes:
- `--regime formal` (importação formal, via DI): calcula **valor aduaneiro (CIF) = produto + frete +
  seguro**, depois **II, IPI, PIS-Import, COFINS-Import, AFRMM** (só marítimo), **taxa Siscomex** e o
  **ICMS "por dentro"** (a conta que quase todo mundo erra), mais despachante/armazenagem em `--outras`.
- `--regime simplificado` (Remessa Conforme / courier até US$ 3.000): II simplificado + ICMS. **É
  estimativa e a lei muda** — sempre mande confirmar na Receita/Remessa Conforme.
- `--regime nacional` (compra dentro do Brasil): sem imposto de importação, só produto + frete + custos.

Exemplo:
`cotar --produto "fone bluetooth" --fornecedor "Shenzhen Atom" --regime formal --moeda USD --cambio 5.45 --preco 8 --qtd 500 --frete 600 --seguro 50 --modal maritimo --ncm 8518.30.00 --ii 16 --ipi 0 --icms 18 --outras 2500`

O motor mostra o **detalhamento linha a linha em BRL**, o **custo total** e o **custo por unidade**, e
salva a cotação. **Peça o NCM ao dono** — as alíquotas dependem dele; se ele não tiver, use uma
estimativa e **avise em voz alta que é [A CONFERIR]** no NCM oficial. Detalhes de cada imposto em
`references/impostos_importacao.md`.

### 4) Comparar — o mais barato de VERDADE
Quando houver mais de uma cotação para o mesmo produto:
`comparar --produto "fone bluetooth"`
Ordena pelo **custo UNITÁRIO aterrissado** (não pelo preço FOB) e mostra o quanto cada opção é mais
cara que a melhor. Reforce sempre: **o menor preço do fornecedor não é o menor custo real** — um
fornecedor 20% mais barato no FOB pode sair mais caro depois de frete e imposto.

### 5) Câmbio — a folga que protege sua margem
O câmbio pode comer o lucro entre o pedido e a chegada. Converta e simule alta:
`cambio --valor 4000 --taxa 5.45 --moeda USD --margem 10`
Mostra o valor em BRL e quanto fica se o câmbio subir X%. Oriente o dono a **reservar essa folga no
preço de venda** e a travar câmbio quando o pedido for grande.

### 6) Negociação — as mensagens com o fornecedor (você escreve)
Esse modo **não tem comando de motor** — é onde a IA agrega mais valor. Escreva para o dono, no tom
dele e no idioma certo (PT/EN), as mensagens de: **pedir cotação**, **pedir amostra**, **negociar MOQ e
preço**, **definir Incoterm e prazo**, **fechar por escrito**. Guie-se por `references/negociacao.md`.
Nunca prometa em nome do dono — entregue o texto pronto pra ele revisar e enviar.

### Fechamento
- `painel` — visão geral: fornecedores, alertas de risco alto, cotações por produto e o melhor custo.
- `exportar --cotacao C001` — o **plano de importação** de uma cotação, pronto pra copiar/decidir.

## Travas (obrigatórias)
- **Nunca invente** alíquota, NCM, alíquota de ICMS do estado, ou regra da lei. Marque estimativa e
  mande confirmar no simulador oficial e no contador.
- **Números são de planejamento**, não a conta final da Receita. Diga isso sempre.
- **Anti-golpe primeiro**: nunca oriente pagamento sem proteção; preço bom demais = alerta.
- **A IA prepara, o dono decide e fecha** a compra. Você não fecha pedido nem paga.
- **Dados locais e privados**: tudo fica em `.alfandega/` (no `.gitignore`).
- **Conversa em PT-BR**, linguagem simples, sem jargão de despachante sem explicar.

## Estrutura
- `scripts/alfandega.py` — motor (stdlib): fornecedores, risco, custo de aterrissagem, câmbio, comparar, painel, exportar.
- `references/impostos_importacao.md` — como cada imposto entra na conta (II, IPI, PIS/COFINS, ICMS por dentro, AFRMM, Siscomex).
- `references/negociacao.md` — roteiros de mensagem com o fornecedor (cotação, amostra, MOQ, Incoterm, fechamento).
- `references/incoterms_e_riscos.md` — Incoterms em português simples + o checklist anti-golpe explicado.
- `setup/SETUP.md` — a primeira conversa (some depois do primeiro uso).
