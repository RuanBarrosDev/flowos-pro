---
name: pacotes
description: >-
  Lista, ativa e desativa os pacotes de agentes do FlowOS Pro (Clientes, Marketing, Gestão,
  Software, YouTube). Use quando o usuário digitar /pacotes, pedir "quais agentes eu tenho",
  "ativa o pacote X", "quero o Turbina/Amarra/Cais...", "desativa o pacote Y" ou chamar uma skill
  que existe em pacotes/ mas ainda não está ativa.
---

# Pacotes do FlowOS Pro

Os pacotes moram em `pacotes/<pacote>/`. Cada um pode ter:
- `skills/<Skill>/` → ativar copia para `.claude/skills/<Skill>/`
- `agents/<agente>.md` → ativar copia para `.claude/agents/<agente>.md`
- `setup-<nome>/` e `referencias/` → ficam onde estão; os agentes leem dali

O catálogo com a descrição de cada skill está em `pacotes/README.md`. Leia antes de responder.

## Regras
- Fale simples: o usuário não é técnico.
- Nunca apague nada fora de `.claude/skills/` e `.claude/agents/`. Pastas de dados dos agentes (as que começam com ponto, como `.ancora/` ou `.claquete/`) e o `_memoria/` nunca são tocados.
- Nunca mexa nas skills do núcleo (as que existem em `.claude/skills/` e não existem em nenhum `pacotes/*/skills/`), nem em `instalar` e `pacotes`.
- Copie a pasta inteira de cada skill (com `scripts/`, `references/`, `LICENSE` etc.), não só o `SKILL.md`.
- Se a cópia já existe em `.claude/skills/`, não sobrescreva sem perguntar: o usuário pode ter ajustado o agente.

## Fluxo

### 1. Mostrar o estado
Para cada pacote em `pacotes/`, verifique quantas das suas skills e agentes já existem em `.claude/`. Mostre uma tabela curta:

| Pacote | O que faz | Status |
|---|---|---|
| Clientes | venda, onboarding, retenção, cobrança, agente de IA | ativo / inativo / parcial |

Use as frases de abertura de cada pacote no `pacotes/README.md`.

### 2. Perguntar
Use AskUserQuestion com `multiSelect: true`: "Quais pacotes você quer ativos?", uma opção por pacote, com a descrição curta. Marque na descrição os que já estão ativos.

Se o usuário pediu um pacote ou uma skill específica pelo nome, pule a pergunta e faça só aquilo.

### 3. Aplicar
- Pacote marcado e inativo (ou parcial): copie o que falta para `.claude/skills/` e `.claude/agents/`.
- Pacote desmarcado e ativo: confirme numa frase ("Vou desativar o pacote X. Os dados que ele já criou ficam guardados.") e apague só as cópias desse pacote em `.claude/skills/` e `.claude/agents/`.
- Use as ferramentas de arquivo do Claude Code ou um comando de cópia do sistema do usuário (no Windows, PowerShell `Copy-Item -Recurse`; no Mac/Linux, `cp -R`).

### 4. Confirmar
Diga o que entrou e o que saiu e sugira um primeiro uso de um agente recém-ativado, ligado ao negócio descrito em `_memoria/negocio.md`. Exemplo: "Experimente: /Amarra tenho reunião com um cliente novo amanhã, monta o roteiro de descoberta".

Avise que skills novas aparecem na hora, mas que agentes (`.claude/agents/`) podem exigir abrir o Claude Code de novo.

Se ativou Software ou YouTube, ofereça o setup opcional:
- Estaleiro: siga `pacotes/software/setup-estaleiro/perguntas.md` e grave `.estaleiro/config.md` no formato de `pacotes/software/setup-estaleiro/config.exemplo.md`.
- Claquete: siga `pacotes/youtube/setup-claquete/perguntas.md` e grave `.claquete/config.md` no formato de `pacotes/youtube/setup-claquete/config.exemplo.md`.
Os dois funcionam sem setup; ele só deixa as respostas mais afiadas. Não apague a pasta de setup no fim.

## Quando o usuário chama uma skill que não está ativa
Se ele pedir `/Turbina` (ou outra) e ela só existir em `pacotes/`, diga em qual pacote ela está e pergunte se pode ativar. Com o sim, ative o pacote inteiro e siga o pedido original.
