---
name: arcabouco
description: >-
  Projeta a ESTRUTURA DE DADOS (o banco de dados) de um sistema, app, site,
  ERP, CRM ou automação — em português claro, antes de programar. Transforma
  uma ideia descrita em palavras ("quero um sistema que guarda clientes,
  pedidos e agendamentos") num modelo de dados correto: as tabelas, os campos,
  as chaves, as relações, o diagrama entidade-relação, o SQL pronto (CREATE
  TABLE para SQLite/PostgreSQL/MySQL) e o dicionário de dados. Também revisa e
  conserta um banco/planilha que já existe, escreve consultas SQL a partir de
  uma pergunta em português, planeja mudanças de estrutura (migração) e gera
  dados de teste. Use quando alguém disser "como estruturar os dados",
  "modelar o banco", "desenhar o banco de dados", "que tabelas eu preciso",
  "montar o schema", "diagrama do banco", "gerar o SQL", "meu banco está
  bagunçado", "normalizar", "modelo de dados", "estrutura do ERP/CRM/app".
---

# Arcabouço — o esqueleto de dados do seu sistema

O **arcabouço** de uma construção é a estrutura que segura tudo. Num sistema,
essa estrutura são os **dados**: quais *coisas* você guarda (clientes, pedidos,
produtos, consultas), quais *informações* de cada coisa, e como elas se
**ligam**. Errar aqui é caro — dá retrabalho, dado duplicado, bug e prejuízo
lá na frente. Acertar aqui faz o resto do sistema ficar simples.

Esta skill projeta essa estrutura **em português, antes de programar**, e
entrega o modelo pronto para o desenvolvedor (ou para a própria IA) construir.
Serve tanto para quem manja de banco de dados (recebe DDL normalizado, índices,
chaves) quanto para quem não sabe nada (conversa em português: "que informações
você precisa guardar?").

## Onde o Arcabouço entra

É a **camada de dados**, o elo entre "decidi o que o sistema faz" e "comecei a
construir". Ele NÃO analisa dados que já existem (isso é análise de planilha),
NÃO escreve a especificação de funcionalidades e NÃO programa a tela. Ele
desenha **onde e como os dados moram**.

## A fonte da verdade: um arquivo de modelo

Tudo gira em torno de UM arquivo: **`.arcabouco/modelo.json`**. Ele descreve o
modelo inteiro (tabelas, campos, tipos, chaves, relações). A IA conversa com o
dono e **escreve** esse arquivo; o motor (`scripts/arcabouco.py`) **lê** o
arquivo e gera — sempre igual e correto — o diagrama, o SQL, o dicionário e os
dados de teste. Assim o desenho nunca "briga" com o código.

> **Primeiro uso:** se existir a pasta `setup/`, rode o setup UMA vez
> (leia `setup/SETUP.md`) para escolher o banco preferido e o nível de
> linguagem. Ele grava `.arcabouco/config.md` + um `.arcabouco/modelo.json`
> vazio e se apaga. Se não existir `setup/`, já está configurado.

## Como trabalhar (sempre assim)

1. **Descubra o modo.** Encaixe o pedido em um dos 8 modos abaixo.
2. **Leia as referências quando o modo pedir** — `references/tipos.md` (o
   cardápio de tipos e a tradução para cada banco) e `references/modelagem.md`
   (os princípios em português: uma tabela por coisa, chaves, relações 1-N e
   N-N, normalização em palavras, anti-padrões). NÃO improvise essas regras.
3. **Escreva/atualize `.arcabouco/modelo.json`** com o que descobriu.
4. **Rode o motor** para gerar/validar o resultado — nunca gere SQL ou
   diagrama "de cabeça"; deixe o motor fazer, para sair sempre consistente.
5. **Explique em português** o que mudou e por quê, na linguagem do dono.

O motor (rode a partir da pasta do projeto do membro):
```
python3 scripts/arcabouco.py validar      # confere a integridade do modelo
python3 scripts/arcabouco.py mermaid       # desenha o diagrama entidade-relação
python3 scripts/arcabouco.py sql --dialeto sqlite|postgres|mysql
python3 scripts/arcabouco.py dicionario    # dicionário de dados em português
python3 scripts/arcabouco.py semear --por 3 # dados de exemplo para testar
```
(Se o membro não passar o caminho, o motor usa `./.arcabouco/modelo.json`.)

---

## Os 8 modos

### 1. `modelar` — da ideia em palavras ao modelo
O pedido: "quero um sistema/app que faça X", "que tabelas eu preciso?".
1. **Entreviste em português, sem jargão.** Pergunte QUE coisas o sistema
   guarda (viram tabelas) e QUE informações de cada uma (viram colunas).
   Bons gatilhos: "quem são os atores? (clientes, funcionários…)", "o que
   acontece? (pedidos, agendamentos, pagamentos…)", "o que se cataloga?
   (produtos, serviços, salas…)".
2. **Encontre as ligações.** "Um cliente tem vários pedidos" → o pedido guarda
   `cliente_id` (uma referência). "Um pedido tem vários produtos e um produto
   está em vários pedidos" → é N-para-N, precisa de uma tabela do meio
   (`itens_pedido`). Veja `references/modelagem.md`.
3. **Escolha os tipos** de cada campo pelo cardápio (`references/tipos.md`).
   Regra de ouro: **dinheiro é sempre o tipo `dinheiro`**, nunca número comum.
4. **Comece de um exemplo pronto quando servir.** Se o negócio se parece com
   um dos modelos em `references/exemplos/` (CRM, agendamento/clínica, loja,
   curso/escola), copie e adapte — não comece do zero.
5. **Escreva `.arcabouco/modelo.json`**, rode `validar`, corrija o que apontar,
   e mostre o resultado com `dicionario` (em português) + `mermaid` (o desenho).

### 2. `diagrama` — mostrar a estrutura
Rode `mermaid`. Cole o resultado num bloco ```mermaid (renderiza na comunidade,
no Notion, no GitHub). Depois **descreva as relações em uma frase cada** ("cada
cliente faz vários pedidos; cada pedido tem vários itens"). O desenho é para o
dono *ver* que a estrutura bate com o negócio dele.

### 3. `sql` — gerar o banco pronto
Rode `sql --dialeto <banco>` (padrão = o `engine` do modelo). Sai o `CREATE
TABLE` com chave primária, chaves estrangeiras, travas (`NOT NULL`, `UNIQUE`,
`CHECK` das opções), valores padrão e **um índice em cada chave estrangeira**.
Entregue o arquivo `.sql` e explique em português o que ele cria. Nunca escreva
DDL à mão — o motor garante que bate com o modelo.

### 4. `revisar` — consertar um banco/planilha que já existe
O dono cola o `CREATE TABLE` atual, OU descreve uma planilha bagunçada.
1. **Traduza para o modelo.json** o que existe hoje.
2. Rode `validar` e leia `references/modelagem.md` (seção anti-padrões).
3. **Aponte os problemas em ordem de impacto**, em português: tabela sem chave,
   informação repetida (deveria virar outra tabela), dinheiro como número,
   falta de índice na chave estrangeira, campo que guarda várias coisas juntas
   ("João; Maria; Ana" numa célula), datas como texto solto.
4. Entregue o **modelo corrigido** + o SQL de como chegar lá.

### 5. `consultar` — pergunta em português → SQL
O dono pergunta "quanto cada cliente comprou este mês?". Você escreve a consulta
`SELECT ... JOIN ... GROUP BY ...` **a partir das tabelas do modelo**, e explica
linha por linha o que ela faz. Sempre confira os nomes reais de tabela/coluna no
`modelo.json` antes de escrever.

### 6. `migrar` — mudar a estrutura com segurança
Precisa acrescentar/renomear/dividir uma tabela ou coluna sem quebrar o que já
roda. Planeje em **passos ordenados e reversíveis** (primeiro adiciona o novo,
depois copia os dados, depois remove o velho), em português + o SQL de cada
passo, com o "como voltar atrás" (rollback). Veja `references/modelagem.md`.

### 7. `dicionario` — o mapa em português
Rode `dicionario`. Sai uma tabela por *coisa*, uma linha por *informação*
(o que é, tipo, se é obrigatório). É o documento que o consultor entrega ao
cliente e que o dono não-técnico entende. Sempre acompanhe a entrega de um
modelo com o dicionário.

### 8. `semear` — dados de teste
Rode `semear --por N`. Sai `INSERT`s de exemplo para popular o banco e testar
antes de ter dados reais. Bom para provar que o modelo funciona.

---

## Regras de ouro (o que NUNCA violar)

- **Nunca invente coluna/tabela que o dono não pediu nem implicou.** Na dúvida,
  pergunte. Um modelo enxuto e certo vale mais que um cheio e errado.
- **Dinheiro é sempre o tipo `dinheiro`** (vira DECIMAL, guarda o centavo).
  Nunca use número comum para preço/valor/total/salário.
- **Toda tabela tem uma chave** que identifica cada linha (um `id`).
- **Toda ligação é uma referência** (`ref` → `outra_tabela.id`), e o motor
  cria índice nela — buscas e junções ficam rápidas.
- **Nomes em minúsculas, sem acento e sem espaço** (`ordens_servico`, não
  "Ordens de Serviço") — o dicionário guarda o nome bonito em português.
- **O `modelo.json` é a fonte única.** Diagrama, SQL e dicionário sempre saem
  dele pelo motor; nunca escreva esses três à mão.
- **Sempre rode `validar` antes de entregar o SQL.** Se apontar erro, conserte
  antes — não entregue banco com relação quebrada.
- **Fale português.** Traduza todo jargão. O dono decide sobre o negócio dele;
  você cuida de que a estrutura fique correta.
- **Nada sai da máquina.** O modelo e o banco são do dono, ficam locais.

## Formato do `modelo.json` (referência rápida)
```json
{
  "projeto": "Nome do sistema",
  "engine": "sqlite",
  "tabelas": [
    {
      "nome": "clientes",
      "descricao": "Quem compra de você",
      "colunas": [
        {"nome": "id", "tipo": "id", "pk": true, "descricao": "identificador"},
        {"nome": "nome", "tipo": "texto", "nn": true, "descricao": "nome completo"},
        {"nome": "email", "tipo": "texto", "unico": true, "descricao": "e-mail"},
        {"nome": "criado_em", "tipo": "datahora", "nn": true, "default": "agora"}
      ]
    },
    {
      "nome": "pedidos",
      "descricao": "Cada compra feita por um cliente",
      "colunas": [
        {"nome": "id", "tipo": "id", "pk": true},
        {"nome": "cliente_id", "tipo": "ref", "ref": "clientes.id", "nn": true,
         "ao_apagar": "cascata", "rotulo": "faz", "descricao": "de quem é"},
        {"nome": "valor", "tipo": "dinheiro", "nn": true, "descricao": "total"},
        {"nome": "status", "tipo": "opcao", "opcoes": ["aberto","pago","cancelado"],
         "nn": true, "default": "aberto"}
      ]
    }
  ]
}
```
Campos de coluna: `nome`, `tipo` (ver `references/tipos.md`), `pk` (chave
primária), `nn` (obrigatório/NOT NULL), `unico` (UNIQUE), `ref` (para tipo
`ref`: "tabela.coluna"), `ao_apagar` ("cascata"|"nulo"), `rotulo` (nome da
relação no diagrama), `opcoes` (para tipo `opcao`), `default` ("agora" ou um
valor), `descricao` (o que é, em português — vira o dicionário).

## Entradas e saídas
- **Entra:** uma ideia em palavras, ou um banco/planilha que já existe, ou uma
  pergunta sobre os dados.
- **Sai:** `.arcabouco/modelo.json` (a fonte), o diagrama entidade-relação, o
  SQL pronto por banco, o dicionário de dados em português, dados de teste.

## Dependências
- **Python 3** (só a biblioteca padrão — nada para instalar).
- Opcional: `sqlite3` (vem no Mac/Linux) para testar o SQL gerado na hora.
