---
name: ensaio
description: >
  Rede de segurança de testes automatizados para quem construiu um app/site/sistema
  com IA e NÃO sabe (nem precisa) ler o próprio código. Faz o ensaio geral antes de
  cada estreia: descobre o que no seu app é crítico (login, pagamento, salvar dados),
  escreve testes de verdade que provam que aquilo funciona, roda esses testes e avisa —
  em português claro — o que passou e o que quebrou, toda vez que você muda alguma coisa.
  Use quando a pessoa disser coisas como "meu app vive quebrando", "mudei uma coisa e
  parou de funcionar", "como garanto que não quebrei nada", "coloca teste no meu projeto",
  "cria uma rede de segurança pro meu sistema", "confere se meu app ainda funciona",
  "meus testes falham à toa", "acabei de fazer uma tela nova, cobre ela", "rodar o ensaio",
  "conferência antes de subir", ou quando alguém que constrói com Claude Code tem medo de
  quebrar o que já funciona sem perceber. NÃO é para caçar um bug específico já conhecido
  (isso é depuração) nem para revisar um trecho de código pontual — é para montar e MANTER
  uma rede permanente que impede regressões.
---

# Ensaio — a rede de segurança do seu app

> **A ideia em uma frase:** você construiu algo que funciona. O medo é mexer e quebrar
> sem perceber. O Ensaio faz o "ensaio geral" antes de cada estreia — escreve testes que
> provam que as partes importantes funcionam e roda tudo toda vez que você muda algo, te
> avisando em português claro se alguma coisa quebrou **antes** do seu usuário ver.

Você **nunca escreve um teste** e **nunca precisa ler código**. Você conversa; o Claude
monta a rede, roda e traduz o resultado. O trabalho técnico acontece por baixo — você só
recebe o veredito e a recomendação.

---

## Antes de tudo: a Preparação (primeira conversa)

**Sempre verifique se existe o arquivo `.ensaio/perfil.md` na raiz do projeto.**

- **Se NÃO existir** → esta é a primeira vez. Abra `setup/PREPARO.md` (na pasta desta skill)
  e siga-o passo a passo: ele descobre com que tecnologia o app foi feito, se já existe
  algum teste, como rodar, e grava tudo em `.ensaio/perfil.md` (a memória local do Ensaio).
  Ao terminar, **apague a pasta `setup/`** — ela só serve uma vez.
- **Se existir** → leia `.ensaio/perfil.md` primeiro. Ele te diz a linguagem, o framework, o
  comando de teste e os caminhos críticos já mapeados, para você **não varrer o projeto de
  novo** a cada conversa.

O perfil é a fonte da verdade do projeto. Se o app mudou muito de tecnologia, sugira refazer
a Preparação.

---

## As regras de ouro (valem em TODO modo — não negociáveis)

Estas cinco regras são o que separa uma rede de testes que protege de uma que dá falsa
sensação de segurança. Elas vêm antes de qualquer pressa.

1. **Um teste que nunca falha é lixo — pior que não ter teste.**
   Todo teste novo é **provado capaz de falhar**: quebre de propósito a coisa que ele
   verifica, veja o teste acusar (falhar pelo motivo certo), conserte, veja passar. Só então
   o teste entra na rede. Um teste que passa mesmo com o app quebrado é uma armadilha — ver
   `references/teste-que-falha.md`.

2. **Nunca diga "passou" sem ter rodado agora.**
   "Os testes passaram" exige uma execução real, com a saída à vista, **nesta conversa**,
   depois da última mudança. Desconfie de verde fácil (cache, servidor velho, filtro `.only`
   ligado): quando parecer bom demais, rode de novo do zero.

3. **Fale a língua do dono, não a do código.**
   O membro não lê código. Relate em desfechos: *"o login está protegido; o cálculo do total
   do carrinho está protegido; a tela de relatório NÃO está — se você mexer nela, ninguém vai
   te avisar se quebrar."* Nada de despejar arquivos de teste que a pessoa não vai entender.

4. **Teste o que dói, não o que é fácil.**
   Priorize os **caminhos críticos** — o que, se quebrar, vira desastre ou vergonha: entrar
   na conta, pagar, salvar/não perder dados, enviar o formulário, o cálculo que vira dinheiro.
   Não encha a rede de testes bonitinhos de coisas que não importam (ver `references/piramide.md`).

5. **O projeto manda.**
   Se o projeto já tem convenções, um `CLAUDE.md`/`AGENTS.md`, um jeito de rodar teste — isso
   vence os padrões do Ensaio. O Ensaio dá o ponto de partida, não a lei. Ao detectar conflito,
   siga o projeto e diga isso ao dono.

---

## Os cinco modos (dispare pelo que a pessoa disser)

Escolha o modo pela intenção. Se estiver ambíguo, faça UMA pergunta curta e siga.

### 1. Diagnóstico — "meu app tem teste? presta?"
**Gatilhos:** "meu app tem teste?", "meus testes servem pra alguma coisa?", "confere a saúde
do meu projeto", "isso aqui está protegido?"

O raio-X honesto do que existe hoje. Não escreve teste nenhum — só avalia e relata.
1. Leia o perfil. Rode a suíte de teste que já existir (se existir) uma vez e registre:
   quantos passam, quebram, são pulados, e quanto tempo leva. Uma suíte que nem roda é o
   **achado nº 1**.
2. Procure os três venenos (ver `references/teste-que-falha.md` e `references/flakiness.md`):
   - **Falso-verde:** testes que passam mesmo com o app quebrado (sem verificação de verdade,
     erro engolido, mock testando o próprio mock).
   - **Instável (flaky):** passa e falha sem nada ter mudado (espera por tempo fixo, ordem,
     estado compartilhado).
   - **Cópia/entulho:** testes duplicados, mortos, que ninguém sabe pra que servem.
3. Entregue a **nota de saúde em português**: o que está protegido, o que NÃO está, e os
   três problemas mais graves em ordem de risco — cada um com o que significa na prática.
   Termine oferecendo o modo **Rede** (para cobrir o que falta) ou **Faxina** (para consertar
   o que está podre).

### 2. Rede — "cria a rede de segurança do meu app"
**Gatilhos:** "põe teste no que importa", "protege meu app", "cria a rede", "quero garantir
que o [login/pagamento/checkout] sempre funcione", "monta os testes do zero".

O coração do Ensaio: montar a rede de proteção nos caminhos críticos.
1. **Instale a rede se ainda não houver** — se o projeto não tem framework de teste, escolha
   o padrão da tecnologia dele (ver perfil) e instale/configure de forma mínima. Explique em
   uma linha o que foi instalado e por quê.
2. **Mapeie os caminhos críticos** com o dono, em linguagem de negócio (ver
   `references/caminhos-criticos.md`): "o que NÃO pode quebrar de jeito nenhum?". Ex.: entrar
   na conta, finalizar compra, salvar o cadastro, o cálculo do total.
3. **Combine a profundidade** (sem escolher calado — ofereça e recomende):
   - **Essencial** — só o caminho feliz de cada crítico. Rápido, barato de manter.
   - **Padrão** (recomendado) — caminho feliz + os erros mais comuns + o pior caso de cada um.
   - **Reforçada** — o acima + permissões (quem NÃO pode fazer), casos de borda, dados reais.
     Para dinheiro, login e coisas irreversíveis. Diga que cada nível ~dobra o custo de manter.
4. **Escreva os testes de verdade** — cada um seguindo a regra de ouro nº 1 (provado capaz de
   falhar). Priorize testes rápidos e baratos sobre testes de tela lentos (ver `piramide.md`).
5. **Rode tudo** e entregue o veredito em português: o que agora está protegido, com prova de
   execução real. Grave os caminhos cobertos em `.ensaio/perfil.md`.

### 3. Conferência — "mexi no app, confere se quebrou algo"
**Gatilhos:** "rodar o ensaio", "confere se está tudo funcionando", "vou subir, tá tudo ok?",
"mudei uma coisa, quebrou alguma coisa?", "conferência antes de publicar".

O uso do dia a dia — o portão que impede a regressão.
1. Rode a rede inteira (regra de ouro nº 2 — execução real, agora).
2. Traduza o resultado:
   - **Tudo verde** → "Pode subir com segurança: [N] proteções conferidas, nada quebrou."
   - **Algo quebrou** → diga **em português** o que parou de funcionar (não o nome do arquivo:
     *"o cálculo do frete parou de somar o imposto"*), o que provavelmente causou, e o **caminho
     mais seguro** para consertar. Não empurre para produção nada com vermelho.
3. Se um teste falhou por ser instável (e não por bug real), diga isso claramente e ofereça a
   **Faxina** — não mande consertar o app por um teste mentiroso.

### 4. Reforço — "acabei de criar a tela X, cobre ela"
**Gatilhos:** "adicionei [funcionalidade], põe teste nela", "cobre o que acabei de fazer",
"fiz uma mudança grande, protege isso também".

Estende a rede para o que acabou de nascer, sem reescrever o que já está coberto.
1. Descubra o que mudou (pela descrição do dono ou pelo histórico do projeto — `git diff`).
2. Veja o que **já** está coberto disso e o que ficou de fora (não conte como coberto um teste
   que só encosta no arquivo — leia se ele realmente prova o comportamento novo).
3. Planeje só as lacunas, escreva os testes (regra nº 1), rode a área mexida **e os vizinhos**
   (sua mudança pode ter quebrado quem estava do lado). Relate em português.

### 5. Faxina — "meus testes estão lentos / falham à toa"
**Gatilhos:** "meus testes falham do nada", "a suíte demora demais", "sempre tenho que rodar
duas vezes", "tem teste quebrado que ninguém arruma", "limpa os testes".

Conserta a rede podre para que ela volte a ser confiável.
1. Ache a causa-raiz da instabilidade (ver `references/flakiness.md`): espera por tempo fixo,
   corrida, estado compartilhado, dependência de ordem, seletor frágil.
2. Conserte pela raiz, não com "roda de novo até passar". Ao reescrever um teste, **re-prove
   que ele ainda é capaz de falhar** pelo motivo certo (a armadilha da faxina é um teste
   "consertado" que parou de testar o comportamento).
3. Remova entulho: testes mortos, duplicados, comentados. Relate o antes/depois: quanto mais
   rápido ficou, quantos venenos saíram, o que ficou mais confiável.

---

## Como o Ensaio trabalha por baixo (para o Claude, não para o dono)

- **Ferramenta de apoio:** `scripts/ensaio.py` (só biblioteca padrão do Python, sem internet,
  sem instalar nada). `python3 scripts/ensaio.py detectar` inspeciona o projeto e sugere a
  linguagem/framework/comando de teste. `python3 scripts/ensaio.py resumo <arquivo>` lê a
  saída de uma rodada de testes que você salvou e devolve um resumo em português (quantos
  passaram/quebraram e quais). O script **nunca** roda comandos por conta própria — quem roda
  os testes é você (Claude), pelo Bash; o script só detecta e resume.
- **Verificação cega (opcional, para redes grandes):** ao escrever muitos testes, você pode
  disparar uma sub-tarefa separada que **audita** os testes gerados contra as regras de ouro
  (principalmente falso-verde) sem ver seu raciocínio — e só aceitar os que passarem. Traga o
  parecer de volta e conserte os reprovados antes de fechar.
- **Memória:** tudo que for durável (tecnologia, comandos, caminhos críticos cobertos) vai
  para `.ensaio/perfil.md`, que fica no projeto do dono e é git-ignorado por padrão.

## Quando NÃO usar o Ensaio (encaminhe)
- Caçar **um** bug específico já conhecido → é depuração metódica, não rede de testes.
- Revisar **um** trecho de código antes de subir (bugs/segurança/simplificação) → é revisão de
  código pontual.
- Construir um app do zero → o Ensaio entra **depois** que já existe algo funcionando para
  proteger.
