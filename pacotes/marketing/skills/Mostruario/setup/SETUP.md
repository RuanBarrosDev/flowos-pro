# Setup do Mostruário — primeira conversa (só uma vez)

Este roteiro roda **uma única vez**, na primeira vez que o membro usa o Mostruário. Ao terminar,
a pasta `setup/` inteira é apagada — o Mostruário instalado fica limpo.

## O que fazer (você, a IA)

Converse em **português, tom acolhedor e simples**, uma pergunta de cada vez. Não faça o dono
digitar comando nenhum — você faz tudo. Colete:

1. **Nome do negócio / loja** — como ele chama a loja.
2. **Onde você vende?** — Mercado Livre, Shopee, Amazon, loja própria/Nuvemshop (pode ser mais de um).
   Isso define os limites e as fórmulas de título que você vai usar.
3. **Tipo de produto** — o que ele vende (moda, eletrônico, cosmético, móvel, alimento, peça...).
   Só ajuda a escolher a linguagem e os atributos que importam.
4. **Tom da marca** — como ele fala com o cliente (formal, próximo/descontraído, técnico/objetivo).
   Usado quando você escrever título, bullets e descrição.
5. **Moeda** — padrão `R$` (Brasil). Só mude se ele for de outro país.

## Como gravar

Crie o arquivo `.mostruario/config.md` na raiz do projeto **exatamente** neste formato
(o motor lê linhas `- **Rótulo:** valor`, e **preserve todos os acentos**):

```markdown
# Configuração do Mostruário

- **Negócio:** Loja Corre & Treina
- **Marketplaces:** Mercado Livre, Shopee
- **Tipo de produto:** acessórios esportivos
- **Tom:** próximo e direto
- **Moeda:** R$
```

Depois:
1. Garanta que **`.mostruario/`** está no `.gitignore` do projeto (crie o `.gitignore` se não existir e
   adicione a linha `.mostruario/`). Custo, preço, margem e fornecedor são privados.
2. Rode `python3 <pasta-desta-skill>/scripts/mostruario.py init` para criar `produtos.csv`,
   `anuncios.csv` e a pasta `anuncios/`.
3. **Apague a pasta `setup/` inteira** (`rm -rf` no caminho absoluto da pasta `setup/` desta skill) —
   ela não é mais necessária.
4. Ofereça para já cadastrar o primeiro produto e montar o primeiro anúncio.

## Regra de ouro do setup
Nunca invente os dados do negócio. Se o dono não tiver certeza de onde vende ou do tom, use padrões
razoáveis (Mercado Livre + tom próximo) e diga que dá pra ajustar depois. O objetivo é sair do setup
com um `config.md` válido e o dono pronto pra cadastrar o primeiro produto.
