# Primeira conversa da Sextante (rode UMA vez)

Olá! Antes de usar a Sextante pela primeira vez, faça esta configuração rápida com o usuário — em português, uma pergunta de cada vez:

1. **Seu nome ou o da sua marca/consultoria** (aparece nos relatórios).
2. **Tom** que você prefere nos textos: `direto`, `caloroso` ou `formal`.
3. **Moeda** usada nos números (padrão: `R$`).

Depois de coletar, grave o arquivo `.sextante/config.json` (crie a pasta `.sextante/` se não existir) com este conteúdo, preenchido:

```json
{
  "consultor": "<nome ou marca>",
  "tom": "<direto|caloroso|formal>",
  "moeda": "R$"
}
```

Grave o `.sextante/config.json` na **raiz do projeto** (o mesmo lugar onde o motor guarda o estado — não dentro da pasta da skill).

Por fim, **apague este arquivo de setup** (que fica na pasta da skill) para deixá-la limpa — use o caminho de onde a skill está instalada:

```bash
rm -f .claude/skills/Sextante/SETUP.md 2>/dev/null || rm -f ~/.claude/skills/Sextante/SETUP.md
```

Pronto. A partir daqui, é só dizer, por exemplo: _"vamos fazer o diagnóstico de maturidade em IA da empresa Padaria Sol"_ e seguir os modos do `SKILL.md`.
