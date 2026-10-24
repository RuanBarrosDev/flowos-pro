# Setup da Cadência — primeira conversa (só uma vez)

Este roteiro roda **uma única vez**, na primeira vez que o membro usa a Cadência. Ao terminar,
a pasta `setup/` inteira é apagada — a Cadência instalada fica limpa.

## O que fazer (você, a IA)

Converse em **português, tom acolhedor e simples**, uma pergunta de cada vez. Não faça o dono
digitar comando nenhum — você faz tudo. Colete:

1. **Nome do negócio** — como ele chama a empresa/clínica/agência/escola/comunidade.
2. **Moeda** — padrão `R$` (Brasil). Só mude se ele for de outro país.
3. **Margem bruta (opcional, %)** — explique leigo:
   > "De cada R$100 que um cliente paga, quanto SOBRA depois do custo de entregar o serviço a ele
   > (não conta aluguel/marketing, só o custo direto)? Serviço costuma ter margem alta, 60% a 90%.
   > Isso é usado só pra calcular quanto um cliente vale (LTV). Se não souber agora, a gente deixa em
   > branco e você preenche depois."
   Nunca crave por ele. Se ele não souber, deixe o campo vazio (o motor pede quando precisar).
4. **CAC médio (opcional)** — explique leigo:
   > "Em média, quanto você gasta pra trazer UM cliente novo (anúncio, comissão, tempo de venda)?
   > Serve pra saber em quantos meses o cliente 'se paga'. Se não tiver o número, deixamos em branco."
   Deixe vazio se ele não souber.

## Como gravar

Crie o arquivo `.cadencia/config.md` na raiz do projeto **exatamente** neste formato
(o motor lê linhas `- **Rótulo:** valor`, e **preserve todos os acentos**):

```markdown
# Configuração da Cadência

- **Negócio:** Clínica Bem Viver
- **Moeda:** R$
- **Margem bruta padrão:** 70
- **CAC médio:** 300
```

Se a margem ou o CAC ficaram em branco, deixe a linha assim (só o rótulo, sem valor):

```markdown
- **Margem bruta padrão:**
- **CAC médio:**
```

Depois:
1. Garanta que **`.cadencia/`** está no `.gitignore` do projeto (crie o `.gitignore` se não existir e
   adicione a linha `.cadencia/`). Os nomes de clientes e a receita são privados (LGPD).
2. Rode `python3 <pasta-desta-skill>/scripts/cadencia.py init` para criar `assinantes.csv` e
   `movimentos.csv` vazios.
3. **Apague a pasta `setup/` inteira** (`rm -rf` no caminho absoluto da pasta `setup/` desta skill) —
   ela não é mais necessária.
4. Ofereça pra já cadastrar os primeiros assinantes recorrentes que ele tiver na cabeça (ou importar
   uma planilha). Lembre a regra de ouro: **só entra o que se REPETE todo mês** — venda avulsa não é MRR.

## Regra de ouro do setup
Nunca invente os dados do negócio. Margem e CAC são opcionais — se o dono não souber, deixe em branco;
o motor pede quando precisar. O objetivo é sair do setup com um `config.md` válido e o dono pronto pra
cadastrar a primeira base recorrente.
