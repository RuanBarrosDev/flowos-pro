---
name: gabarito
description: >
  Elicitação de requisitos e especificação — transforma um pedido vago ("quero
  um sistema/app/site/automação que faça X", seu ou de um cliente) numa
  ESPECIFICAÇÃO escrita, priorizada e com critério de aceite, ANTES de construir,
  para que você (ou seu desenvolvedor, ou o Claude Code) construa a coisa certa e
  não retrabalhe. Use quando alguém disser: "quero criar um sistema/app/site/
  automação", "preciso especificar/escopar um projeto", "levantamento de
  requisitos", "montar um escopo / documento de requisitos / PRD / especificação",
  "meu cliente quer um sistema mas não sei o que ele precisa", "como transformo
  essa ideia num plano do que construir", "o que exatamente vou pedir pro dev".
  Gatilhos: "gabarito", "especificar projeto", "levantar requisitos", "escopo de
  software", "documento de requisitos", "PRD", "requirements", "spec", "scope".
---

# Gabarito — a especificação antes da obra

> **O que é, em uma linha:** um entrevistador de requisitos que ouve o dono (ou o
> cliente dele) em português simples e devolve uma **especificação** — o que
> construir, para quem, por quê, com critério de aceite e fronteira de escopo —
> para que a construção acerte de primeira.

O nome vem da marcenaria/serralheria: o **gabarito** é o molde-mestre que você faz
ANTES de cortar a peça, e contra o qual toda peça é conferida. A especificação é
o gabarito do software: define a forma exata antes da obra.

Preenche a lacuna da jornada de quem constrói: **Sonda** valida se vale a pena →
**Gabarito especifica O QUE construir** → **Prumo** planeja o build → **Estaleiro**
escreve → **Rastro** depura → **Crivo** revisa → **Órbita** publica.

---

## Passo 0 — Instalação de primeira execução (rodar UMA vez, em silêncio)

Na primeira vez que esta skill for usada num projeto, faça a instalação antes de
qualquer coisa:

1. Verifique se já existe a pasta `setup/` na skill. Se **não** existir, o
   Gabarito já está instalado — pule para o fluxo normal.
2. Se existir, pergunte ao dono, em linguagem simples, **duas** coisas (use
   AskUserQuestion quando disponível; se a sessão for automática/sem interface,
   use valores padrão e siga):
   - **Como você quer ser chamado / nome do negócio?**
   - **Que tom a especificação deve ter?** (ex.: próximo e direto / formal e
     técnico / didático para leigo)
3. Rode a instalação passando as respostas:
   ```bash
   python3 setup/instalar.py --dono "<resposta 1>" --tom "<resposta 2>"
   ```
   Isso cria a pasta local `.gabarito/`, grava `.gabarito/config.md`, protege
   `.gabarito/` no `.gitignore` e **apaga a própria pasta `setup/`** — deixando a
   skill limpa. Não coleta nenhuma senha nem chave (o Gabarito é 100% offline).
4. Siga para o fluxo. Não narre detalhes técnicos da instalação.

O motor é `scripts/gabarito.py` (Python puro, biblioteca padrão, **nunca acessa a
rede**). Todos os comandos abaixo são `python3 scripts/gabarito.py <comando>`.

---

## Como o Gabarito trabalha (regras de ouro)

1. **A IA lidera a conversa, o DONO decide.** Você puxa pela pergunta o que o dono
   sabe (o problema, quem usa, a dor) e propõe como opção o que ele não sabe
   (estrutura, integrações), sempre traduzindo termo técnico para o dia a dia.
2. **Nunca invente.** Problema, requisito, número, critério, prazo — nada é
   chutado. O que o dono não souber vira **[A CONFERIR]**, nunca um palpite.
3. **Toda funcionalidade traça a um problema real.** A espinha é
   **Problema → Necessidade → Requisito**. Requisito sem problema por trás é
   **órfão** = candidato a cortar (é assim que se evita construir o que ninguém pediu).
4. **Todo requisito precisa de critério de aceite testável.** "Rápido", "fácil",
   "intuitivo" sozinhos não são requisito — são opinião. O motor marca esses como
   **nebulosos** até virarem um número/critério que dá para conferir.
5. **Priorize e proteja a fronteira.** MoSCoW (Obrigatório / Importante / Desejável
   / Fora-por-ora) define o MVP; a lista do que fica **FORA do escopo** é a defesa
   nº 1 contra retrabalho.
6. **A IA prepara e REDIGE; o dono revisa e aprova.** A especificação sai como
   rascunho para o dono ajustar e assinar (ou mandar ao cliente para aceite).
7. **Dados 100% locais.** Tudo fica em `.gabarito/` na máquina do dono (LGPD).

---

## Fluxo (modos)

Traduza SEMPRE o termo técnico para o dia a dia ao conversar
(veja `references/traducao_de_termos.md`).

### 1. Enquadrar o projeto — `novo`
Abre a especificação: o que se quer construir (nas palavras do dono), para quem, e
o **problema central**. Detecta o domínio.
```bash
python3 scripts/gabarito.py novo --nome "..." --para "..." --problema "..." --dominio "..."
python3 scripts/gabarito.py projeto
```
Só preencha o que o dono disser; o resto fica [A CONFERIR]. Referência:
`references/comecar_pelo_problema.md`.

### 2. Entrevistar — `perguntas` / `responder` / `entrevista`
O coração da elicitação. `perguntas` mostra o que perguntar por dimensão
(problema, usuários, jornada, dados, integrações, restrições, prazo, orçamento,
sucesso). Conduza a conversa, traduza o jargão, e registre cada resposta **nas
palavras do dono**.
```bash
python3 scripts/gabarito.py perguntas            # ou --dimensao dados
python3 scripts/gabarito.py responder --dimensao usuarios --resposta "..."
python3 scripts/gabarito.py entrevista           # o que já sabemos + o que falta
```
Referências: `references/o_que_perguntar.md`, `references/traducao_de_termos.md`.

### 3. Cadeia problema → necessidade → requisito
Registre a espinha da rastreabilidade. Cada requisito nasce de uma necessidade,
que nasce de um problema.
```bash
python3 scripts/gabarito.py problema-add --titulo "..." --descricao "..."
python3 scripts/gabarito.py necessidade-add --problema CP.01 --descricao "..."
python3 scripts/gabarito.py requisito-add --necessidade CN.01 --enunciado "..." \
    --tipo funcional --porque "..." --criterio "..." --validar "..." --prioridade obrigatorio
```
Referência: `references/do_problema_ao_requisito.md`.

### 4. Detalhar o requisito — `requisito` / `detalhar`
Cada requisito = **enunciado + porquê + critério de aceite + como validar + tipo**
(funcional / não-funcional). O motor sinaliza requisito **nebuloso** (adjetivo
vago sem critério) e **órfão** (sem problema por trás).
```bash
python3 scripts/gabarito.py requisito              # lista com alertas
python3 scripts/gabarito.py requisito --id RF.01   # detalhe
python3 scripts/gabarito.py detalhar --id 1 --criterio "Dado ..., Quando ..., Então ..."
```
Referência: `references/criterio_de_aceite.md`.

### 5. Priorizar — `prioridade` / `moscow`
MoSCoW + validador de dependência (o Obrigatório não pode depender do Desejável) +
a linha do MVP.
```bash
python3 scripts/gabarito.py prioridade --id RF.02 --nivel importante
python3 scripts/gabarito.py moscow
```
Referência: `references/moscow_e_mvp.md`.

### 6. Proteger o escopo — `escopo-add` / `escopo`
A fronteira anti-inchaço. Registra o que fica **dentro / fora / depende de terceiro
/ bloqueado**, e separa **suposições / riscos / restrições / perguntas em aberto**
— nunca misturados.
```bash
python3 scripts/gabarito.py escopo-add --tipo fora --texto "não faz X nesta versão"
python3 scripts/gabarito.py escopo-add --tipo pergunta --texto "cliente decide se ..."
python3 scripts/gabarito.py escopo
```
Referência: `references/proteger_o_escopo.md`.

### 7. A especificação — `especificacao` (o CORAÇÃO)
Monta o documento completo (`.gabarito/especificacao-N.md`) — resumo, problemas,
requisitos priorizados com critério de aceite, fronteira de escopo, suposições/
riscos/perguntas, critérios de sucesso e bloco de aceite — e roda o **portão
"pronto para construir?"** (🟢/🟡/🔴).
```bash
python3 scripts/gabarito.py especificacao
```
Referência: `references/o_documento_de_especificacao.md`.

### Painel e plano
```bash
python3 scripts/gabarito.py painel     # raio-x da especificação
python3 scripts/gabarito.py plano      # o que fechar antes de construir (🔴 antes de 🟡)
```

---

## Entradas / Saídas
- **Entrada:** a conversa com o dono (ou o pedido do cliente dele), respondida ao
  longo dos modos. Nada de planilha obrigatória, nada de conta na nuvem.
- **Saída:** o documento `.gabarito/especificacao-N.md` (o gabarito da obra) +
  os dados de trabalho em `.gabarito/*.csv`, tudo local.

## Dependências
- Apenas **Python 3** (biblioteca padrão). Sem `pip install`, sem internet, sem chaves.

## Não é (para não confundir com skills irmãs)
- **Sonda** valida se o mercado quer aquilo (vale construir?) — o Gabarito assume
  que já decidiu e especifica **o quê**. (Handoff Sonda → Gabarito.)
- **Prumo** planeja o build no Claude Code e economiza contexto/tokens (o **como**)
  — o Gabarito define **o quê/por quê** antes. (Handoff Gabarito → Prumo.)
- **Estaleiro** escreve o código — o Gabarito é a especificação que ele constrói.
- **Marco** é cronograma/prazos; **Cerne** é o "cérebro do negócio" contínuo para a
  IA; **Engrenagem** diagnostica O QUE automatizar; **Planta** toca o escritório de
  projetos para vários clientes. O Gabarito produz UMA especificação, a fundo.

## Trava de integridade
Se em algum momento faltar informação para um requisito, um número ou um critério,
**pare e pergunte** — ou marque **[A CONFERIR]**. Nunca preencha por dedução para
"parecer completo": uma especificação com furo declarado é honesta; uma inventada
gera a obra errada.
