# Primeira conversa do Aceno (setup)

Rode isto **uma única vez**, quando `.aceno/config.md` ainda não existir. O
objetivo é conhecer o negócio o suficiente para medir quem esfriou — sem pedir
nada demais. Conversa curta, em português simples.

## O que perguntar (uma coisa de cada vez)

1. **Qual o nome do seu negócio?**
2. **Qual o seu ramo?** (barbearia, contabilidade, clínica, agência, seguros…)
3. **De quanto em quanto tempo um bom cliente costuma voltar a comprar de você?**
   → Esse é o *ciclo de recompra*, em dias. Se a pessoa não souber, sugira a
   partir do ramo: barbearia/salão ~30, contador/mensalidade ~30, restaurante ~15,
   dentista ~180, arquiteto/advogado ~365. Confirme antes de gravar.
4. **Que tom você usa com seu cliente?** (próximo e informal / cordial e
   profissional / formal) — isso guia a mensagem de aceno depois.

## O que fazer com as respostas

1. Crie a pasta `.aceno/` na raiz do projeto do usuário.
2. Escreva `.aceno/config.md` **com acentos**, neste formato:

   ```markdown
   # Config do Aceno
   - **Negócio:** <nome>
   - **Ramo:** <ramo>
   - **Ciclo de recompra em dias:** <número>
   - **Tom de voz:** <próximo | cordial | formal>
   ```

3. Crie `.aceno/clientes.csv` só com o cabeçalho:

   ```
   nome,contato,ultimo_contato,valor_total,compras,status,observacao
   ```

4. Se houver um `.git` na raiz, garanta a linha `.aceno/` no `.gitignore` (a
   carteira de clientes é dado sensível — nunca deve ir para o repositório).
5. Confirme com `python3 scripts/aceno.py check`.
6. **Apague a pasta `setup/` desta skill** — ela só serve para o primeiro uso.

## Depois do setup

Convide o dono a trazer a base: "me manda a planilha dos seus clientes, ou me
conta os que você lembra que faz tempo que não aparecem — nome, quando foi a
última vez e quanto costumavam gastar". Assim que houver clientes no CSV, rode o
**termômetro** para mostrar o valor parado na carteira.
