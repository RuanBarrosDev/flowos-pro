# Arcabouço — o esqueleto de dados do seu sistema

**Arcabouço** projeta a **estrutura de dados** (o banco de dados) de um
sistema, app, site, ERP, CRM ou automação — **em português, antes de
programar**. Você descreve em palavras o que o sistema precisa guardar e ele
devolve o modelo pronto: as tabelas, os campos, as chaves, as ligações, o
**diagrama entidade-relação**, o **SQL pronto** (SQLite, PostgreSQL ou MySQL) e
o **dicionário de dados** em português.

Serve para os dois lados: quem manja recebe um banco normalizado, com chaves e
índices; quem não sabe nada conversa em português ("que informações você
precisa guardar?") e recebe um mapa que entende.

## O que ele faz (8 modos)

| Modo | Para quê |
|------|----------|
| **modelar** | Da ideia em palavras → tabelas, campos, chaves e relações |
| **diagrama** | Desenha o diagrama entidade-relação (você *vê* a estrutura) |
| **sql** | Gera o `CREATE TABLE` pronto (SQLite / PostgreSQL / MySQL) |
| **revisar** | Conserta um banco ou planilha que já existe (acha os erros) |
| **consultar** | Pergunta em português → a consulta SQL, explicada |
| **migrar** | Planeja mudar a estrutura sem quebrar o que já roda |
| **dicionario** | O mapa em português: cada tabela e campo explicado |
| **semear** | Gera dados de exemplo para testar o modelo |

## Como instalar

1. Descompacte o arquivo `Arcabouço.zip`.
2. Copie a pasta **`Arcabouço`** para dentro de `.claude/skills/` no seu
   projeto (ou em `~/.claude/skills/` para usar em qualquer projeto):
   ```
   .claude/skills/Arcabouço/
   ```
3. Abra o Claude Code nesse projeto. Pronto — a skill é reconhecida sozinha.

## Como usar

Fale naturalmente com o Claude, por exemplo:

- *"Preciso estruturar o banco de um sistema de agendamento pra minha clínica."*
- *"Que tabelas eu preciso pra um CRM?"*
- *"Meu banco tá uma bagunça, dá uma revisada nessa estrutura aqui: …"*
- *"Gera o SQL desse modelo pra PostgreSQL."*
- *"Como escrevo a consulta pra ver quanto cada cliente comprou este mês?"*

Na primeira vez, o Claude faz 3 perguntas rápidas (nome do projeto, qual banco,
seu nível) e já começa. Debaixo dos panos ele conversa, monta o modelo e um
pequeno programa em Python (que já vem junto) gera o diagrama, o SQL e o
dicionário — você só fala em português.

## O que esperar

- **Nunca inventa** tabela ou campo que você não pediu — na dúvida, pergunta.
- **Protege o seu dinheiro:** todo valor em R$ vira um tipo que guarda o centavo
  exato (nunca "arredonda").
- **Tudo local:** o modelo e o banco são seus, ficam na sua máquina, nada é
  enviado para fora.
- **Um arquivo é a fonte da verdade** (`.arcabouco/modelo.json`): o diagrama, o
  SQL e o dicionário sempre saem dele, então nunca "brigam" entre si.

## Requisitos

- **Claude Code** instalado.
- **Python 3** (só a biblioteca padrão — nada para instalar).
- Opcional: `sqlite3` (já vem no Mac e no Linux) para testar o SQL na hora.

## Exemplos de partida inclusos

Em `references/exemplos/` já vêm quatro modelos prontos para copiar e adaptar:
**CRM de vendas**, **agenda de atendimentos** (clínica/salão), **loja/e-commerce**
e **escola/cursos**.

---

Feito para a comunidade **Maestria Academy**. Licença MIT — use, adapte e
compartilhe à vontade.
