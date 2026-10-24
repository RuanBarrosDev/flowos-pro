# Preparação do Ensaio (roda uma vez só)

> Este arquivo guia a **primeira conversa** do Ensaio num projeto. Ao terminar, **apague a
> pasta `setup/` inteira** — ela não é mais necessária e não deve ir junto quando o dono
> compartilhar o projeto.

O objetivo é criar `.ensaio/perfil.md` na raiz do projeto: a memória local que todos os modos
do Ensaio leem depois, para não varrer o projeto de novo a cada conversa.

## Passo 1 — Descobrir a tecnologia (sem perguntar ainda)
Inspecione o projeto (pode usar `python3 ../scripts/ensaio.py detectar` a partir da pasta da
skill, ou olhar direto):
- **Linguagem e gerenciador:** `package.json` (Node/JS/TS), `pyproject.toml`/`requirements.txt`
  (Python), `go.mod` (Go), `Gemfile` (Ruby), `pom.xml`/`build.gradle` (Java), `composer.json` (PHP).
- **Tipo de app:** site/front-end (React, Next, Vue, HTML puro), API/back-end, script, app mobile.
- **Já existe teste?** Procure pastas `tests/`, `__tests__/`, `spec/`, arquivos `*.test.*`,
  `*_test.*`, `test_*.py`. Se existir, veja qual ferramenta (Jest, Vitest, Playwright, Cypress,
  Pytest, Go test, etc.) e qual o comando de rodar (nos scripts do `package.json` ou na config).
- **Como o app roda localmente** e em que porta, se for um site/servidor.
- **Regras do projeto:** existe `CLAUDE.md`, `AGENTS.md`, `docs/`, config de lint? Elas mandam.

## Passo 2 — Perguntar só o que não dá para descobrir
Junte TUDO numa pergunta só (nunca uma de cada vez), em português simples. Típico:
- "Qual a parte do seu app que **não pode quebrar de jeito nenhum**?" (isso vira os caminhos
  críticos — ex.: entrar na conta, pagar, salvar cadastro).
- "O que mais te dá medo hoje: não ter teste nenhum, ter teste que falha à toa, ou não saber
  se o que você mexe quebra o resto?"
- Se for um site que precisa de login para testar: "tem um usuário de teste que eu posso usar?
  (me diga o mecanismo, **não** a senha de verdade)".
- Se algo do Passo 1 ficou contraditório, pergunte qual é a verdade.

Se o dono não souber responder algo, registre como **lacuna em aberto** no perfil — não chute.

## Passo 3 — Escrever o perfil
Crie a pasta `.ensaio/` na raiz do projeto e escreva dois arquivos:

**`.ensaio/.gitignore`** com uma única linha `*` (para o perfil ficar só na máquina do dono e
nunca vazar em repositório público).

**`.ensaio/perfil.md`** com este esqueleto (preencha com o que descobriu; fatos, não opinião):

```markdown
# Perfil do Ensaio
> Gerado na preparação em <data>. Os modos do Ensaio leem este arquivo em vez de varrer o
> projeto. Refaça a preparação se a tecnologia do projeto mudar muito.

## Tecnologia      — linguagem, gerenciador, tipo de app, como rodar o app localmente (+porta)
## Testes hoje     — framework(s), onde ficam, quantos, como rodar (comando exato)
## Comandos        — rodar todos os testes / um arquivo só / (se houver) checagem de tipos e lint
## Caminhos críticos — o que não pode quebrar, em linguagem de negócio (preenchido no modo Rede)
## Ambiente seguro — onde pode testar; o que NUNCA pode ser tocado (ex.: produção); como obter
                     usuário de teste (o mecanismo, nunca a senha)
## Regras do projeto — link para CLAUDE.md/AGENTS.md/docs do projeto (não copie, referencie)
## Lacunas em aberto — perguntas sem resposta, marcadas se bloqueiam algo
```

## Passo 4 — Conferir e fechar
- Rode o comando de teste mais barato (ex.: listar os testes) para provar que o comando do
  perfil está certo. Um perfil com comando errado envenena todos os modos depois.
- Mostre ao dono um resumo de 5 linhas: tecnologia, se já tem teste, o que está protegido hoje,
  e o próximo passo sugerido (**Diagnóstico** se já há testes, ou **Rede** se não há nenhum).
- **Apague a pasta `setup/`** desta skill (o Preparo já cumpriu seu papel). A partir daqui, a
  existência de `.ensaio/perfil.md` é o sinal de que a preparação foi feita.
