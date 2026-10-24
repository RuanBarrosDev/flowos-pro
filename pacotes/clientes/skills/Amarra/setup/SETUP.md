# Setup da Amarra — primeira conversa (só uma vez)

Este roteiro roda **uma única vez**, na primeira vez que o membro usa a Amarra. Ao terminar, a pasta
`setup/` inteira é apagada — a Amarra instalada fica limpa.

## O que fazer (você, a IA)

Converse em **português, tom acolhedor e simples**, uma pergunta de cada vez. Não faça o dono digitar
comando nenhum — você faz tudo. Colete:

1. **Nome do negócio** — como ele chama a empresa/consultoria/agência.
2. **Moeda** — padrão `R$` (Brasil). Só mude se ele for de outro país.
3. **O que você vende (opcional)** — em uma linha, o serviço/solução que ele oferece nas reuniões
   (ex.: "consultoria de implantação de IA no comercial", "gestão de tráfego pago", "software de
   gestão para clínicas"). Serve pra personalizar o roteiro e a proposta. Se ele preferir, deixe em
   branco e defina por oportunidade depois.
4. **Ticket típico (opcional)** — a faixa de valor de uma venda comum (ex.: "6.000"). Ajuda a
   sugerir as 3 opções depois. Nunca crave por ele; se não souber, deixe em branco.

## Como gravar

Crie o arquivo `.amarra/config.md` na raiz do projeto **exatamente** neste formato (o motor lê linhas
`- **Rótulo:** valor`, e **preserve todos os acentos**):

```markdown
# Configuração da Amarra

- **Negócio:** Consultoria Alavanca
- **Moeda:** R$
- **O que vende:** implantação de IA no comercial (consultoria + treinamento)
- **Ticket típico:** 6.000
```

Se "o que vende" ou "ticket típico" ficaram em branco, deixe a linha só com o rótulo:

```markdown
- **O que vende:**
- **Ticket típico:**
```

Depois:
1. Garanta que **`.amarra/`** está no `.gitignore` do projeto (crie o `.gitignore` se não existir e
   adicione a linha `.amarra/`). Nomes e números de clientes são privados (LGPD).
2. Rode `python3 <pasta-desta-skill>/scripts/amarra.py init` para criar os CSVs vazios.
3. **Apague a pasta `setup/` inteira** (`rm -rf` no caminho absoluto da pasta `setup/` desta skill) —
   ela não é mais necessária.
4. Ofereça pra já abrir a primeira oportunidade que ele tiver em mente (`nova --cliente "..."`) e
   preparar a reunião de descoberta.

## Regra de ouro do setup
Nunca invente os dados do negócio. "O que vende" e "ticket típico" são opcionais — se o dono não
souber, deixe em branco. O objetivo é sair do setup com um `config.md` válido e o dono pronto pra abrir
a primeira oportunidade.
