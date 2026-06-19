# Guia de Instalação — FlowOS Pro

**Tempo estimado: 20-30 minutos**

---

## O que você vai precisar

- [ ] Computador com Windows, Mac ou Linux
- [ ] VS Code instalado (gratuito) — [code.visualstudio.com](https://code.visualstudio.com)
- [ ] Conta Claude Pro da Anthropic (~R$100/mês) — [claude.ai](https://claude.ai)
- [ ] Claude Code instalado (gratuito com Claude Pro)

---

## Passo 1 — Instalar o VS Code

Se ainda não tem, baixa em [code.visualstudio.com](https://code.visualstudio.com) e instala normalmente.

---

## Passo 2 — Criar conta no Claude Pro

1. Acessa [claude.ai](https://claude.ai)
2. Cria uma conta (pode usar e-mail ou Google)
3. Faz upgrade para o plano Pro (necessário para usar o Claude Code)
4. Anota seu e-mail e senha — vai precisar no passo 4

**Por que precisa do Claude Pro?**
O FlowOS Pro roda dentro do Claude Code, que é a interface de terminal da Anthropic. Os agentes são skills que o Claude executa. Sem o Pro, o Claude tem limite de mensagens que inviabiliza o uso diário.

---

## Passo 3 — Instalar o Claude Code

**No Windows:**
1. Abre o terminal (PowerShell ou cmd)
2. Cola e executa:
```
npm install -g @anthropic-ai/claude-code
```

**No Mac:**
1. Abre o Terminal
2. Cola e executa:
```
npm install -g @anthropic-ai/claude-code
```

> Se aparecer erro de "npm não encontrado", instala o Node.js primeiro em [nodejs.org](https://nodejs.org) (versão LTS) e repete.

**Verifica a instalação:**
```
claude --version
```
Deve aparecer um número de versão.

---

## Passo 4 — Baixar o FlowOS Pro

**Opção A — Terminal (recomendado):**
```bash
git clone https://github.com/flowzera/flowos-pro.git
cd flowos-pro
code .
```

**Opção B — Download direto:**
1. Acessa [github.com/flowzera/flowos-pro](https://github.com/flowzera/flowos-pro)
2. Clica em "Code" → "Download ZIP"
3. Extrai a pasta
4. Abre o VS Code e vai em "File → Open Folder" → seleciona a pasta extraída

---

## Passo 5 — Abrir o Claude Code na pasta

1. Com a pasta `flowos-pro` aberta no VS Code
2. Abre o terminal integrado: **Ctrl + '** (Windows) ou **Cmd + '** (Mac)
3. Digita `claude` e dá Enter
4. Na primeira vez, vai pedir para autenticar com a conta da Anthropic
5. Segue as instruções de autenticação na tela

---

## Passo 6 — Rodar o /instalar

Com o Claude Code aberto:

1. Digita `/instalar` e dá Enter
2. O sistema vai te fazer perguntas sobre o negócio
3. Responde com calma — são 2 rodadas de 4 perguntas cada
4. O /instalar cria o arquivo `_memoria/negocio.md` automaticamente

**Isso roda uma vez só.** Depois disso, todos os 18 agentes já conhecem o seu negócio.

---

## Passo 7 — Renomear a pasta

Depois que o `/instalar` terminar:

1. Fecha o VS Code
2. Renomeia a pasta `flowos-pro` para o nome do seu negócio (ex: `Clínica Sorriso`, `BarbeariaRS`)
3. Abre o VS Code de novo na pasta renomeada

A pasta agora é o seu negócio, não mais o FlowOS genérico.

---

## Primeiro teste

Com tudo pronto, testa um agente:

```
/Escriba escreve uma legenda para o Instagram apresentando meu negócio
```

Se o agente responder no tom correto com os dados do seu negócio, está tudo funcionando.

---

## Dúvidas frequentes

**O Claude pediu chave de API. O que faço?**
Na primeira vez que abre o Claude Code, ele pede para logar. Segue o link que aparece no terminal — ele abre o navegador para autenticação.

**O /instalar não aparece como opção. O que houve?**
Confirma que você abriu o terminal DENTRO da pasta do FlowOS no VS Code (não em outra pasta). O Claude Code precisa estar rodando na pasta certa para encontrar as skills.

**Posso instalar em mais de um computador?**
Sim. O FlowOS Pro é seu — instala em quantos computadores quiser. A memória do negócio (`_memoria/negocio.md`) fica local, você pode copiar entre máquinas.

**Preciso fazer backup?**
Recomendado. Sobe a pasta para o GitHub (privado) ou Google Drive. Assim não perde a memória configurada.

---

## Próximos passos

Com a instalação concluída:

1. Lê o playbook do seu nicho em `_setup/playbooks/`
2. Segue o roteiro em `_setup/primeiros-7-dias.md`
3. Usa o `Leme` toda manhã para organizar o dia

Bem-vindo ao FlowOS Pro.
