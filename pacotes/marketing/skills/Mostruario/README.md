# 🛍️ Mostruário — Anúncios de Produto que Vendem

Uma skill de Claude Code que transforma o seu produto num **anúncio completo** — no formato e no limite
certos de cada marketplace (**Mercado Livre, Shopee, Amazon**) e da **loja própria** — conversando em
português, no seu tom, sem virar técnico.

É o **frente** do produto (o anúncio que vende). O **Celeiro** cuida do fundo (estoque e compras),
o **Fiel** cuida do preço, o **Alcance** do Google, o **Holofote** das redes — o **Mostruário** cuida
do **anúncio do produto**.

Serve pra quem vende **produto**: loja, e-commerce, atacado, importador, revenda, representante comercial.

---

## O que ela faz

- **Título** que cabe no limite (ML 60 · Shopee 256 · Amazon) e começa pelas palavras que o cliente busca.
- **Ficha técnica e bullets** — vira cada especificação num benefício concreto pro cliente.
- **Descrição** persuasiva na estrutura que converte (gancho → benefícios → prova → objeções → chamada).
- **Roteiro de fotos** — quais 7-9 fotos tirar (principal fundo branco, lifestyle, detalhe, infográfico).
- **Variações e palavras-chave** — agrupa cor/tamanho sem duplicar anúncio e acha os termos de busca.
- **Nota do anúncio (0-100)** — um checklist que aponta exatamente o que falta pra converter.

A skill **nunca inventa** uma especificação do produto. Se faltar um dado (voltagem, material, medida),
ela marca **[A CONFERIR]** e pergunta pra você. E quem publica no marketplace é você — ela prepara tudo,
você confere e cola.

---

## Como instalar

1. Baixe e **descompacte** o arquivo `Mostruário.zip`.
2. Coloque a pasta `Mostruário` dentro de `.claude/skills/` do seu projeto
   (ou em `~/.claude/skills/Mostruário` para usar em qualquer projeto).
3. Abra o Claude Code nesse projeto. Pronto — a skill é reconhecida sozinha.

Caminho final esperado:
```
seu-projeto/
└── .claude/
    └── skills/
        └── Mostruário/
            ├── SKILL.md
            ├── scripts/mostruario.py
            └── references/
```

---

## Como usar

Só **fale naturalmente** com o Claude. Exemplos que disparam a skill:

- "meu anúncio no Mercado Livre não vende, me ajuda a melhorar"
- "monta o título e a descrição desse produto pra Shopee"
- "que fotos eu preciso tirar desse produto?"
- "quais palavras-chave o cliente usa pra achar isso?"
- "como faço as variações de cor e tamanho sem criar vários anúncios?"

Na **primeira conversa**, a skill faz um setup rápido (nome da loja, onde você vende, tipo de produto,
tom da marca) e cria uma pasta local `.mostruario/` com seus dados. A partir daí, é só conversar.

---

## Privacidade

Tudo fica **no seu computador**, na pasta `.mostruario/` do projeto (já entra no `.gitignore`).
Custos, preços, margens e fornecedores **não vão para a internet** — a skill funciona offline e nunca
publica nada sozinha: ela prepara o anúncio, você confere e publica.

---

## Requisitos

- Claude Code instalado.
- Python 3 (já vem no macOS e na maioria dos Linux). A skill usa **só a biblioteca padrão** — nada de instalar pacote.

---

Feito para a comunidade **Maestria Academy**. Licença MIT (veja `LICENSE`).
