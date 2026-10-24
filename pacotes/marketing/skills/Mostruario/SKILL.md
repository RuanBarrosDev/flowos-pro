---
name: mostruario
description: >-
  Transforma um produto num ANÚNCIO que vende em marketplace e loja — título no formato e no limite
  certos, ficha técnica/atributos, bullets de benefício, descrição persuasiva, roteiro de fotos e
  palavras de busca. Use quando o dono falar de anúncio/anúncios, "meu produto não aparece/não vende",
  título de produto, Mercado Livre, Shopee, Amazon, Nuvemshop/loja, ficha técnica, atributos, bullets,
  descrição do produto, SEO de marketplace, palavras-chave, fotos do produto, variações (cor/tamanho),
  cadastrar produto, otimizar anúncio, ranquear no marketplace. Conversa em português, escreve a copy
  no tom do dono, NUNCA inventa especificação do produto, e quem publica é o dono.
---

# Mostruário — Anúncios de Produto que Vendem

O **mostruário** é a vitrine onde a mercadoria se apresenta pra quem vai comprar. Esta skill pega um
produto e monta o **anúncio completo** — o que faz o cliente parar, entender e clicar em comprar — no
formato e nos limites de cada marketplace (**Mercado Livre, Shopee, Amazon**) e da **loja própria**.

É o **FRENTE** do produto (o anúncio que vende). O **Celeiro** cuida do fundo (estoque, compra, capital
parado). O **Fiel** cuida do preço, o **Alcance** do SEO no Google, o **Holofote** do conteúdo social,
o **Verbo** da copy de serviço — o **Mostruário** é o único que cuida do **anúncio do produto físico**.

O membro só conversa em português. Por baixo, você (a IA) escreve a copy persuasiva **no tom dele** e
traduz o resto em comandos do motor `scripts/mostruario.py` (Python, biblioteca padrão, offline). O
motor guarda tudo em `.mostruario/` na raiz do projeto e cuida da parte **verificável**: catálogo, as
**regras e limites** de cada marketplace, a **checagem do título**, a **nota** do anúncio contra um
checklist de conversão, e a **exportação** do anúncio pronto pra colar. **Nunca invente uma
especificação, medida, material ou compatibilidade do produto.**

## Quando usar
Dispare quando o dono falar de:
- "meu anúncio **não aparece / não vende**", "quero **ranquear** no Mercado Livre/Shopee/Amazon"
- "me ajuda a montar o **título** do produto", "esse título cabe no limite?"
- "o que colocar na **descrição** / nos **bullets** / na **ficha técnica**?"
- "que **fotos** eu preciso tirar?", "como fazer as **variações** (cor/tamanho) sem duplicar anúncio?"
- "quais **palavras-chave** o cliente usa pra achar meu produto?"
- "cadastrar produto", "**otimizar** meu anúncio", "melhorar minha loja / Nuvemshop"

Serve para quem vende **produto** — loja, e-commerce, atacado, importador, revenda, representante.

## Primeira conversa (setup — só uma vez)
Se **não existir** `.mostruario/config.md`, rode o setup antes de qualquer comando:
1. Leia `setup/SETUP.md` e conduza a conversa em PT-BR que ele descreve (nome do negócio, marketplaces
   onde vende, tipo de produto, tom da marca, moeda).
2. Grave as respostas em `.mostruario/config.md` (o SETUP.md tem o modelo exato).
3. Garanta `.mostruario/` no `.gitignore` (preço, custo e fornecedor são privados).
4. **Apague a pasta `setup/`** — ela é só do primeiro uso.
5. Rode `python3 scripts/mostruario.py init` para criar os arquivos de dados vazios.

## Como você trabalha (os 6 modos)

Sempre invoque o motor com o caminho desta skill, ex.:
`python3 <pasta-desta-skill>/scripts/mostruario.py <comando>`. Traduza a fala do dono para o comando
certo, **escreva a copy você mesmo** no tom dele, mostre a saída em PT-BR e explique simples.

### 1) Catálogo — o retrato honesto do produto
Antes de escrever qualquer anúncio, colete o que o produto REALMENTE é. Cadastre nome, categoria,
marca, modelo, público, atributos (ficha técnica), diferenciais e as palavras que o cliente usa pra
buscar. **Nunca invente atributo** — se o dono não souber (voltagem, material, medida, compatibilidade),
cadastre sem e marque **[A CONFERIR]**; pergunte a ele.
- `produto-add --nome "..." --categoria "..." --marca "..." --modelo "..." --publico "..." --marketplace ml --custo 45,00 --preco 129,90 --atributos "cor=preto||material=algodão||tamanho=M" --diferenciais "a||b||c" --palavras "como o cliente busca||sinônimo||uso"`
- `catalogo` — lista tudo · `produto --id P001` — o retrato completo de um produto
- `definir --id P001 --campo atributos --valor "cor=azul||material=couro"` — corrige/atualiza um campo

### 2) Título — a linha que decide se o cliente clica
O título é o campo que mais pesa na busca. Cada marketplace tem **limite e fórmula própria**. Peça as
regras com `limites`, escreva **3 variações** de título com as palavras de busca no começo, e valide
cada uma no limite com `titulo-check` (ele conta os caracteres e avisa termo proibido/emoji).
- `limites --marketplace ml` (ou shopee / amazon / loja) — mostra limite, fórmula e o que é proibido
- `titulo-check --texto "..." --marketplace ml` — confere o tamanho e a qualidade do título
- Fórmulas: **ML 60 car** (Produto+Marca+Modelo+Especificação) · **Shopee 256 car** · **Amazon** keyword
  nos ~50 primeiros caracteres · **Loja** pensada também no Google.

### 3) Ficha & Bullets — atributo vira benefício
A **ficha técnica/atributos** é obrigatória e alimenta os filtros de busca — preencha o máximo (nunca em
branco, nunca inventado). Onde o marketplace usa **bullets** (Amazon, loja), escreva **5 bullets** no
formato **BENEFÍCIO em destaque + 1 frase de explicação** — transforme cada spec num ganho pro cliente
("20h de bateria" → "Treina a semana toda sem recarregar"). Veja `references/formula_titulo_bullets.md`.

### 4) Descrição — a conversa que tira a dúvida e vende
Escreva a descrição no tom do dono, na estrutura que converte: **gancho → benefícios → como usar/prova →
objeções respondidas → chamada final (CTA)**. Sempre a partir dos atributos reais — **nunca invente
spec**. Respeite o limite (Shopee 5.000 car). Não copie a descrição do fabricante (conteúdo duplicado
derruba no Google). Modelo em `references/estrutura_descricao.md`.

### 5) Fotos — o roteiro do que fotografar
O dono tira as fotos; você entrega o **roteiro que converte**: foto principal (fundo branco puro, produto
≥85% do quadro, sem texto/logo, ≥1000 px — Shopee 1024×1024), + lifestyle (uso real), + detalhe, +
infográfico (specs na imagem — chega a +94% de visualização). Recomende **7–9 fotos**. Checklist completo
em `references/roteiro_de_fotos.md`.

### 6) Variações & Palavras de busca — achar sem duplicar
Agrupe cor/tamanho/voltagem numa **única página de variações** (não crie anúncios separados — isso divide
review e ranking). Defina as **palavras-chave reais** que o cliente digita (no Amazon, os termos de
backend cabem em **249 bytes** — estourar de-indexa tudo; sem repetir o título, sem marca de concorrente).
Veja `references/variacoes_e_palavras.md`.

### Fechamento — montar, dar nota e exportar
Quando a copy estiver pronta, salve o anúncio e deixe o motor **auditar**:
- Escreva o anúncio final num arquivo `.md` (título, ficha, bullets/descrição, CTA) e rode
  `salvar --produto P001 --marketplace ml --arquivo <arquivo.md>` — ele guarda e dá a **nota 0–100**.
- `nota --produto P001 --marketplace ml` — o **scorecard**: o que está ok e o que falta pra converter.
- `exportar --produto P001 --marketplace ml` — imprime o anúncio pronto pra **o dono colar e publicar**.
- `painel` — todos os produtos, quais já têm anúncio e a nota de cada um.

## Travas (nunca quebre)
- **Nunca invente** especificação, medida, material, voltagem, compatibilidade ou origem do produto.
  Falta dado → cadastre sem e mostre **[A CONFERIR]**; pergunte ao dono.
- **Respeite os limites e as regras de cada marketplace** (título, nº de bullets, termos proibidos).
  As plataformas mudam — sempre diga "confirme na central de ajuda do marketplace".
- **Não prometa o que o produto não faz.** Nada de superlativo não comprovável ("o melhor", "cura"),
  alegação de saúde, ou "nº 1". Marketplaces penalizam e o cliente devolve.
- **Sem keyword stuffing** (encher de palavra repetida) e **sem copiar anúncio de concorrente** (plágio
  e conteúdo duplicado derrubam o anúncio).
- **A IA escreve, o dono confere e publica.** O motor **nunca** publica nada em marketplace nenhum.
- **Dados 100% locais** em `.mostruario/` (custo, preço, margem e fornecedor são sensíveis — LGPD).
- **Não é** estoque/compra (Celeiro), preço (Fiel), SEO de site no Google (Alcance), dashboard (Vitrine)
  nem conteúdo social (Holofote). O Mostruário cuida do **anúncio do produto**.

## Onde ficam os dados
`./.mostruario/` na raiz do projeto: `config.md`, `produtos.csv`, `anuncios.csv` e a pasta `anuncios/`
com cada anúncio pronto (`.md`). Tudo git-ignored.

## Handoffs
- Preço/margem do produto → **Fiel**. Estoque e reposição → **Celeiro**.
- SEO da loja própria no Google → **Alcance**. Painel de vendas → **Vitrine**.
- Divulgar o produto nas redes → **Holofote**.
