# Princípios de modelagem em português (leia antes de `modelar` e `revisar`)

Modelar dados é responder três perguntas: **que coisas eu guardo, que
informações de cada coisa, e como elas se ligam.** Estas regras deixam o modelo
correto sem precisar de teoria pesada.

## 1. Uma tabela por "coisa" do mundo real

Cada tabela representa **um tipo de coisa**: clientes, pedidos, produtos,
consultas, funcionários, salas. Se você consegue dizer "cada linha é UM(A)
___", é uma tabela boa. Cada informação dessa coisa é uma **coluna**.

Teste rápido: "cliente" tem nome, e-mail, telefone → tabela `clientes` com
colunas `nome`, `email`, `telefone`. 

## 2. Toda tabela precisa de uma chave (o `id`)

A chave identifica cada linha sem confusão. Nome não serve (dois "João Silva"),
e-mail muda. Use uma coluna `id` do tipo `id`. É a âncora de todas as ligações.

## 3. As três formas de ligação

### Um-para-muitos (1-N) — a mais comum
"Um cliente faz **vários** pedidos, mas cada pedido é de **um** cliente."
→ O lado "muitos" (pedido) guarda a referência: `pedidos.cliente_id → clientes.id`.
Nunca o contrário. A referência mora sempre no filho.

### Muitos-para-muitos (N-N) — precisa de tabela do meio
"Um pedido tem **vários** produtos e um produto está em **vários** pedidos."
Não dá para pôr a referência em nenhum dos dois. Crie uma **tabela do meio**
(`itens_pedido`) com `pedido_id` e `produto_id` (duas referências) — e ela ainda
guarda o que é específico da ligação (quantidade, preço no momento).
Outros exemplos: alunos↔cursos (matrículas), médicos↔pacientes (consultas),
posts↔tags (marcações).

### Um-para-um (1-1) — rara
"Cada usuário tem um perfil e cada perfil é de um usuário." Quase sempre é só
mais colunas na mesma tabela. Só separe se for dado sensível/opcional/pesado.

## 4. Não repita informação (normalização, em palavras)

**A regra:** cada fato mora em UM lugar só. Se o mesmo dado aparece copiado em
várias linhas, ele deveria estar em outra tabela, referenciado.

- ❌ Guardar `nome_do_cliente` dentro de cada pedido. Se o cliente troca de
  nome, você tem que caçar em mil pedidos. → Guarde só `cliente_id`; o nome
  mora em `clientes`.
- ❌ Uma coluna `produtos` com "Camiseta; Boné; Caneca" tudo junto. Não dá para
  contar, filtrar nem somar. → Vira a tabela do meio `itens_pedido`.
- ❌ Colunas `telefone1`, `telefone2`, `telefone3`. E o quarto telefone? →
  Vira uma tabela `telefones` ligada ao cliente.

**Regra prática:** se você sentir vontade de numerar colunas (`item1`, `item2`)
ou de colar vários valores numa célula, falta uma tabela.

## 5. Anti-padrões que o `revisar` deve caçar (em ordem de impacto)

1. **Tabela sem chave primária** — não dá para referenciar nem atualizar com
   segurança. Toda tabela precisa de `id`.
2. **Dinheiro como número/float** — perde centavo, dá diferença de caixa.
   Troque para o tipo `dinheiro`.
3. **Informação repetida** (nome do cliente copiado em cada pedido) — vira
   referência.
4. **Vários valores numa célula** ("João; Maria") — vira tabela do meio.
5. **Data guardada como texto** — não ordena nem calcula prazo. Vira `data`.
6. **Chave estrangeira sem índice** — junção e busca ficam lentas quando cresce.
   (O motor cria o índice automaticamente para todo `ref`.)
7. **Campo que aceita qualquer coisa** onde só cabem 3 valores — vira `opcao`
   com lista fechada, o banco passa a recusar lixo.
8. **Colunas numeradas** (`fone1`, `fone2`) — vira tabela filha.

## 6. Migração segura (modo `migrar`)

Mudar a estrutura de um banco que já tem dados e está rodando é delicado. Faça
em **passos pequenos e reversíveis**, nunca tudo de uma vez:

- **Adicionar** coluna/tabela nova → seguro, faça primeiro (o velho continua
  funcionando).
- **Renomear** → em vez de renomear direto (quebra o que usa o nome antigo),
  crie o novo, copie os dados, aponte o código para o novo, só então remova o
  velho.
- **Dividir uma tabela** (ex.: separar `endereco` de `clientes`) → crie a nova,
  copie os dados, ligue por referência, depois remova as colunas antigas.
- **Sempre tenha o "como voltar"** (rollback) escrito antes de aplicar.
- **Teste numa cópia** antes de rodar no banco de verdade.

## 7. Nomes

- Tabelas no plural, minúsculas, sem acento: `clientes`, `ordens_servico`.
- Colunas minúsculas, sem acento, com `_`: `data_nascimento`, `cliente_id`.
- Referência = `<coisa>_id`: `cliente_id`, `produto_id` (o motor até adivinha a
  ligação por esse padrão).
- O nome bonito em português ("Ordens de Serviço") mora na `descricao` e no
  dicionário — não no nome técnico.
