# Veredito

Painel para você **aprovar ou rejeitar, um por um**, qualquer lote que o Claude gerar:
imagens, thumbnails, títulos, textos, ideias, links e mudanças de código.

## Como instalar
1. Descompacte o arquivo `Veredito.zip`.
2. Copie a pasta `Veredito` para `~/.claude/skills/` (vale para todos os projetos)
   ou para `.claude/skills/` dentro do seu projeto.
3. Abra o Claude Code. Pronto — não precisa configurar nada.

## Como usar
Peça em português normal, por exemplo:
- "Gera 10 títulos para meu vídeo e monta um painel pra eu aprovar."
- "Quero revisar essas imagens uma por uma."
- "Me deixa aprovar ou rejeitar essas ideias de post."

No painel: **A** aprova · **R** rejeita · **M** talvez · **S** pula · **C** comenta.
Cada clique é salvo na hora; o Claude lê seus motivos e melhora a próxima rodada.

## Requisitos
Python 3 (já vem no Mac). Opcional: Pillow, para deixar imagens mais leves.

Licença: MIT.
