# Cardápio de tipos (em português) e como cada banco entende

Você escolhe o tipo pelo nome em português. O motor traduz para o tipo real do
banco escolhido. Isso deixa o modelo simples para quem não é técnico **e** correto
para quem é.

| Tipo (você escreve) | Serve para | SQLite | PostgreSQL | MySQL |
|---|---|---|---|---|
| `id` | identificador único de cada linha (a chave primária) | INTEGER PK AUTOINCREMENT | BIGSERIAL PK | BIGINT AUTO_INCREMENT PK |
| `texto` | nome, e-mail, título, telefone (texto curto) | TEXT | VARCHAR(255) | VARCHAR(255) |
| `texto_longo` | observação, descrição grande, corpo de mensagem | TEXT | TEXT | TEXT |
| `numero` | quantidade, idade, contagem (inteiro, sem centavo) | INTEGER | INTEGER | INT |
| `decimal` | medida com casas (peso, nota, percentual) | DECIMAL(12,2) | DECIMAL(12,2) | DECIMAL(12,2) |
| `dinheiro` | **preço, valor, total, salário** — qualquer R$ | DECIMAL(12,2) | DECIMAL(12,2) | DECIMAL(12,2) |
| `booleano` | sim/não (ativo?, pago?, entregue?) | INTEGER (0/1) | BOOLEAN | TINYINT(1) |
| `data` | dia sem hora (nascimento, vencimento) | DATE | DATE | DATE |
| `datahora` | momento exato (criado em, agendado para) | DATETIME | TIMESTAMP | DATETIME |
| `opcao` | uma escolha de uma lista fixa (status, tipo) | TEXT + CHECK | VARCHAR(50) + CHECK | VARCHAR(50) + CHECK |
| `ref` | ligação com outra tabela (chave estrangeira) | INTEGER + FK | BIGINT + FK | BIGINT + FK |

## As três regras que evitam 90% dos erros

1. **Dinheiro é sempre `dinheiro`.** Número comum (float) arredonda e você
   perde centavos — o cliente reclama do valor errado. `dinheiro` guarda o
   centavo exato.
2. **Data é `data` ou `datahora`, nunca `texto`.** Data como texto ("15/03/26")
   não ordena, não filtra "últimos 30 dias", não calcula prazo. Guarde como
   data de verdade.
3. **Escolha limitada é `opcao` com `opcoes`.** Se um campo só pode ser
   "aberto/pago/cancelado", declare `"opcoes": ["aberto","pago","cancelado"]`.
   O banco passa a **recusar** qualquer valor fora da lista — dado sempre limpo.

## Marcas extras de uma coluna

- `"pk": true` — é a chave primária (normalmente só o `id`).
- `"nn": true` — obrigatório (NOT NULL): não pode ficar em branco.
- `"unico": true` — não pode repetir (ex.: e-mail, CPF). Já cria índice.
- `"ref": "clientes.id"` — para o tipo `ref`: diz a qual tabela.coluna liga.
- `"ao_apagar": "cascata"` — se apagar o pai, apaga os filhos junto
  (ex.: apagou o pedido → some os itens dele). `"nulo"` deixa a ligação vazia.
- `"opcoes": [...]` — para o tipo `opcao`: a lista fechada de valores.
- `"default": "agora"` — valor automático. `"agora"` preenche a data/hora do
  momento; qualquer outro valor vira o padrão daquela coluna.
- `"descricao": "..."` — o que o campo é, em português. Vira o dicionário de
  dados. **Sempre preencha** — é o que faz o dono entender o modelo.

## Qual banco escolher (resumo honesto)

- **SQLite** — o padrão para começar. É um arquivo só, não precisa instalar
  servidor, roda em qualquer lugar. Perfeito para protótipo, app pequeno/médio,
  ferramenta interna. Comece por aqui a não ser que já saiba que precisa de mais.
- **PostgreSQL** — quando o sistema cresce, tem muitos acessos ao mesmo tempo,
  ou você quer recursos avançados. É o "profissional" mais recomendado hoje.
- **MySQL** — muito usado em hospedagem comum e sistemas legados. Escolha se o
  ambiente do cliente já é MySQL.

O mesmo `modelo.json` gera o SQL dos três — você troca com `--dialeto`.
