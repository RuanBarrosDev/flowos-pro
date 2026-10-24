---
name: maquete
description: >
  Design de produto antes de codar — transforma um pedido de software ("quero um
  app/site/SaaS/sistema que faça X", seu ou de um cliente) no DESENHO navegável do
  produto: as personas, os fluxos de uso (a jornada tela-a-tela), os wireframes
  lo-fi de cada tela e — a joia — um PROTÓTIPO HTML clicável que o dono abre no
  navegador, mostra pro cliente e valida com usuário, ANTES de escrever uma linha
  de código. No fim, gera o brief de handoff pronto pro build. Use quando alguém
  disser: "quero criar um app/site/sistema", "como vão ser as telas", "desenha a
  interface / a tela de X", "quero um protótipo / mockup / wireframe", "monta a
  navegação do app", "como o usuário anda pela tela", "quero mostrar pro cliente
  antes de construir", "preciso ver o app antes de mandar o dev fazer", "desenha o
  fluxo de uso". Gatilhos: "maquete", "protótipo", "wireframe", "mockup", "desenhar
  telas", "desenho de telas", "fluxo de telas", "interface do app", "UX do produto",
  "navegação do app", "tela de login/cadastro/dashboard".
---

# Maquete — o desenho do produto antes da obra

> **O que é, em uma linha:** um designer de produto que ouve o dono em português
> simples e devolve os **fluxos de uso**, os **wireframes lo-fi** de cada tela e um
> **protótipo HTML clicável** que se navega no navegador — para VER e validar o
> produto antes de construí-lo.

O nome vem da arquitetura: a **maquete** é o modelo em escala que se monta ANTES da
obra, para todo mundo ver, andar em volta e aprovar antes de assentar o primeiro
tijolo. Aqui é a maquete do software: as telas e a navegação, em baixa fidelidade,
para decidir a forma antes de gastar tempo (seu ou do dev) construindo.

Preenche a lacuna da jornada de quem constrói: **Sonda/Cadinho** validam se vale a
pena → **Gabarito** especifica O QUE construir → **Maquete DESENHA como o produto se
parece e se usa** → **Arcabouço** modela os dados → **Estaleiro** escreve → **Rastro**
depura → **Crivo** revisa → **Órbita** publica. O Gabarito começa pelo problema, "não
pela lista de telas" — a Maquete é justamente quem cuida das telas e da navegação.

Dupla utilidade: serve o **construtor** (desenha antes de codar) E o **consultor/agência**
(gera um protótipo clicável para mostrar ao cliente e fechar o projeto antes de programar).

---

## Passo 0 — Instalação de primeira execução (rodar UMA vez, em silêncio)

Na primeira vez que esta skill for usada num projeto, faça a instalação antes de
qualquer coisa:

1. Verifique se existe a pasta `setup/` na skill. Se **não** existir, a Maquete já
   está instalada — pule para o fluxo normal.
2. Se existir, pergunte ao dono, em linguagem simples, **duas** coisas (use
   AskUserQuestion quando disponível; se a sessão for automática/sem interface, use
   os padrões e siga):
   - **Como você quer ser chamado / nome do negócio?**
   - **Seus produtos costumam ser para qual tela?** (site/web, celular/app, ou
     programa de computador/desktop) — vira a plataforma padrão dos protótipos.
3. Rode a instalação passando as respostas:
   ```bash
   python3 setup/instalar.py --dono "<resposta 1>" --plataforma "<web|mobile|desktop>"
   ```
   Isso cria a pasta local `.maquete/`, grava `.maquete/config.md`, protege
   `.maquete/` no `.gitignore` e **apaga a própria pasta `setup/`** — deixando a
   skill limpa. Não coleta nenhuma senha nem chave (a Maquete é 100% offline).
4. Siga para o fluxo. Não narre detalhes técnicos da instalação.

O motor é `scripts/maquete.py` (Python puro, biblioteca padrão, **nunca acessa a
rede**). Todos os comandos abaixo são `python3 scripts/maquete.py <comando>`.

---

## Como a Maquete trabalha (regras de ouro)

1. **Começa pela TAREFA do usuário, não pela tela bonita.** Primeiro o fluxo (o que
   a pessoa quer cumprir e em que ordem), depois as telas que esse fluxo precisa.
   Tela que não serve a nenhum fluxo é **órfã** = candidata a cortar.
2. **Fidelidade LO-FI de propósito.** O protótipo é cinza, sem cor de marca, sem
   arte final — de propósito. Isso força a conversa sobre **estrutura e navegação**
   ("falta uma tela de confirmação aqui"), não sobre "a cor do botão". Cor e marca
   vêm depois, no build.
3. **Nunca invente conteúdo real.** Nome de cliente, valor, data, texto de e-mail —
   nada é chutado. Use rótulos genéricos ("[nome do cliente]", "R$ [valor]") ou
   marque **[A CONFERIR]**. Um protótipo honesto tem placeholders; um inventado
   engana o dono e o cliente.
4. **Toda ação leva a algum lugar.** Cada botão/link aponta para outra tela (o
   `-> T.xx`). O motor sinaliza **ação quebrada** (aponta para tela inexistente) e
   **beco-sem-saída** (tela sem nenhuma saída). Se não dá para clicar e chegar lá, o
   fluxo tem furo.
5. **É protótipo, não a arte final.** A maquete existe para DECIDIR e VALIDAR, não
   para ser bonita. A IA desenha e propõe; o **dono valida cada tela**.
6. **Dados 100% locais.** Tudo fica em `.maquete/` na máquina do dono (LGPD). Sem
   nuvem, sem conta, sem chave, offline.

---

## Fluxo (modos)

Fale sempre em português do dia a dia; traduza qualquer termo técnico.

### 1. Enquadrar o produto — `novo`
Abre o design: o que se quer construir (nas palavras do dono), para quem, em que
plataforma (web/mobile/desktop) e o **problema central** que resolve.
```bash
python3 scripts/maquete.py novo --nome "..." --para "..." --plataforma web \
    --problema "..." --tom "limpo e simples"
python3 scripts/maquete.py projeto
```
Só preencha o que o dono disser; o resto fica [A CONFERIR]. Referência:
`references/comecar_pelo_fluxo.md`.

### 2. Quem usa — `persona-add` / `personas`
Registre quem vai usar o produto e o que cada um quer resolver. Amarra cada tela a
um objetivo real de gente de verdade.
```bash
python3 scripts/maquete.py persona-add --nome "Recepcionista" --papel "operadora" \
    --objetivo "marcar e remarcar rápido" --contexto "atende telefone o dia todo"
python3 scripts/maquete.py personas
```

### 3. Desenhar os fluxos — `fluxo-add` / `fluxos` / `fluxo-set`
O coração da UX. Um fluxo é a **jornada tela-a-tela** para cumprir uma tarefa. Comece
pela tarefa nº 1 (a razão de o produto existir). A lista de telas do fluxo é a ordem
em que elas acontecem — pode citar telas que você vai desenhar no próximo passo.
```bash
python3 scripts/maquete.py fluxo-add --nome "Marcar um horário" --persona P.01 \
    --objetivo "recepção marca em 20s" --telas "T.01, T.02, T.03, T.02" \
    --gatilho "paciente liga"
python3 scripts/maquete.py fluxos
python3 scripts/maquete.py fluxo-set --id F.01 --telas "T.01, T.02, T.03"  # ajusta a ordem
```
Referência: `references/comecar_pelo_fluxo.md`.

### 4. Desenhar cada tela — `tela-add` / `tela-set` / `tela` / `telas`
Cada tela = tipo + objetivo + **blocos** (o conteúdo lo-fi) + estado. Os blocos usam
um vocabulário simples (o motor os desenha como wireframe). Cada botão/link aponta o
destino com `-> T.xx` — é isso que torna o protótipo navegável.
```bash
python3 scripts/maquete.py tela-add --nome "Login" --tipo login \
    --objetivo "entrar no sistema" \
    --blocos "titulo: Entrar || campo: E-mail || campo: Senha || botao: Entrar -> T.02 || link: Esqueci a senha -> T.05"
python3 scripts/maquete.py telas          # lista, marca telas órfãs
python3 scripts/maquete.py tela --id T.01 # detalhe dos blocos
```
**Vocabulário de blocos** (um por linha, separados por `||`):
`titulo` · `subtitulo` · `texto` · `campo` (input) · `area` (texto longo) ·
`selecao` (dropdown) · `botao: rótulo -> T.xx` · `link: rótulo -> T.xx` ·
`lista: a, b, c` · `tabela: Col1, Col2, Col3` · `card: título | linha` ·
`imagem: legenda` · `abas: A, B` · `nav: Início -> T.02, Perfil -> T.05` ·
`metrica: rótulo | valor` · `aviso: texto` · `espaco`.
Tipos de tela comuns e o que costumam ter: `references/tipos_de_tela.md`.
Não esqueça os **estados** (vazio/carregando/erro) que quase todo mundo esquece:
`references/estados_e_vazios.md`.

### 5. O mapa de navegação — `mapa`
Mostra o grafo tela → tela e roda as travas: **telas órfãs** (ninguém chega nelas) e
**ações quebradas** (botão apontando para tela que não existe). É o raio-X que prova
que o produto é navegável de ponta a ponta.
```bash
python3 scripts/maquete.py mapa
```

### 6. Os wireframes em documento — `wireframes`
Gera `.maquete/wireframes-N.md`: cada tela desenhada em lo-fi (texto), com objetivo,
estado e para onde cada ação leva. Bom para revisar tela-a-tela e comentar.
```bash
python3 scripts/maquete.py wireframes
```

### 7. O protótipo navegável — `prototipo` (o CORAÇÃO)
Gera `.maquete/prototipo-N.html`: um arquivo único, offline, que o dono abre no
navegador (duplo-clique) e **navega clicando pelos botões**. Tem a moldura do
dispositivo (web/mobile/desktop), a lista de telas, e um **modo passo-a-passo por
fluxo** (setas ← → andam pela jornada). É o que se mostra pro cliente e se usa para
validar com usuário real.
```bash
python3 scripts/maquete.py prototipo
```
Referência: `references/o_prototipo_navegavel.md`.

### 8. O brief para o build — `entregar`
Gera `.maquete/brief-de-construcao-N.md`: o handoff pronto para o Gabarito/Estaleiro/
Claude Code construir — o produto, as personas, os fluxos, o inventário de telas (com
os dados que entram e as ações de cada uma) e as pendências do design.
```bash
python3 scripts/maquete.py entregar
```
Referência: `references/do_prototipo_ao_build.md`.

### Painel e plano
```bash
python3 scripts/maquete.py painel   # raio-x: contagens, alertas, prontidão 🟢/🟡/🔴
python3 scripts/maquete.py plano    # o que fechar antes de considerar o design pronto
```

---

## Entradas / Saídas
- **Entrada:** a conversa com o dono (ou o pedido do cliente dele) — a tarefa, quem
  usa, as telas. Nada de ferramenta de design, nada de conta na nuvem.
- **Saída:** o **protótipo** `.maquete/prototipo-N.html` (navegável, offline), os
  **wireframes** `.maquete/wireframes-N.md`, o **brief** `.maquete/brief-de-construcao-N.md`
  e os dados de trabalho em `.maquete/*.csv` — tudo local.

## Dependências
- Apenas **Python 3** (biblioteca padrão) e um navegador para abrir o protótipo.
  Sem `pip install`, sem internet, sem chave, sem Figma/conta de design.

## Não é (para não confundir com skills irmãs)
- **Gabarito** especifica O QUE construir em palavras (requisitos, critério de aceite)
  e explicitamente NÃO desenha telas — a Maquete pega essa deixa e desenha as telas e
  a navegação. (Handoff Gabarito → Maquete.)
- **Sonda/Cadinho** validam se o mercado quer a ideia (vale construir?) — a Maquete
  assume que já decidiu e desenha como o produto se usa.
- **Arcabouço** modela os dados (tabelas, campos) que ficam POR TRÁS das telas — a
  Maquete desenha o que aparece NA FRENTE. (Andam juntas: tela ↔ dados.)
- **Estaleiro** escreve o código de verdade — a Maquete é o desenho que ele constrói.
- **Fachada** faz o SITE público de marketing do negócio; **Palco** monta um deck de
  slides; **Vitrine** apresenta resultados/dados prontos. A Maquete desenha a
  INTERFACE de um produto/app que o usuário opera, não uma página de venda nem um slide.

## Trava de integridade
Se faltar informação para uma tela, um rótulo ou um destino de botão, **pare e
pergunte** — ou use um placeholder genérico / **[A CONFERIR]**. Nunca invente nome de
cliente, número ou texto real para "parecer pronto": um protótipo com placeholder
declarado é honesto; um com dado inventado engana quem decide e leva a construir a
coisa errada.
