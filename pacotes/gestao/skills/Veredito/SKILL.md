---
name: veredito
description: >-
  Painel HTML de APROVAR / REJEITAR item por item. Use SEMPRE que o usuário quiser julgar
  um lote de coisas uma a uma e devolver um veredito — imagens, thumbnails, títulos, frases,
  CTAs, ideias e textos em markdown, mudanças (diffs), links/URLs (com screenshot embutido)
  ou trechos de código. PT: "painel de aprovar/rejeitar", "me deixa aprovar ou rejeitar
  esses", "quero revisar um por um", "faz um html pra eu aprovar", "monta um painel pra eu
  aprovar essas thumbs/títulos/links", "veredito", "ar-board". EN: "approve/reject board",
  "let me approve or reject these", "review these one by one", "thumbs up/down on these".
  Julgamento SEMPRE individual (teclas A aprovar / R rejeitar / M talvez / S pular /
  C comentar) — nunca comparação A/B, nunca nota de 1 a 5. Modo AO VIVO: cada clique grava
  o veredito em disco e o Claude age sobre os motivos.
---

# Veredito — painel de aprovar / rejeitar

Um lote de itens vira um **único HTML autossuficiente** onde o usuário julga **um por um**
(A/R/M/S + comentário). No modo ao vivo, cada ação grava o veredito em disco; você lê o
resultado e **age sobre os motivos** — nunca responde só "ok".

**Regra de ouro:** julgamento é **sempre individual**. Nunca monte comparação A/B, nunca
peça nota de 1 a 5. Só existe: **A** aprovar · **R** rejeitar · **M** talvez · **S** pular ·
**C** comentar. Setas navegam; dentro do comentário a **seta-direita avança** (A/R/M/S ficam
bloqueadas no campo). A/R/M avançam sozinhos. Comentário disponível em qualquer item e em
qualquer estado. Há nota geral do lote, barra de progresso, strip numerada, JSON ao vivo,
Baixar/Copiar/Limpar, resumo de fechamento e salvamento no navegador (localStorage).

## Onde estão os arquivos

`SKILL_DIR` = a pasta onde este `SKILL.md` está (ex.: `~/.claude/skills/veredito/` ou
`.claude/skills/veredito/` do projeto). Rode todos os comandos com `cd "$SKILL_DIR"`.

| arquivo | papel |
|---|---|
| `build_panel.py` | manifesto JSON → HTML autossuficiente (embute/comprime imagens em base64). |
| `serve_judge.py` | servidor local do modo ao vivo (porta efêmera, watchdog, auto-encerramento). |
| `read_verdict.py` | lê o veredito normalizado de um lote. |
| `template/panel.html` | motor único do painel. **Não edite por lote** — os dados vêm do manifesto. |
| `reference/manifest-schema.md` | schema completo do manifesto e do veredito. |
| `examples/` | um manifesto por tipo + `example-mixed.json`. |
| `_run/<lote>/` | criado sozinho por lote: `panel.html`, `server.port`, `verdict.json`, `verdict.FINAL.json`. |

Tipos (`kind`) suportados: **image, text, markdown, diff, change_card, url, code**.
Leia `reference/manifest-schema.md` antes de montar o manifesto.

## Fluxo (modo AO VIVO é o padrão)

### 1) Monte o manifesto JSON
`{title, subtitle, batch, round?, items:[{id, kind, ...}]}`. IDs únicos. Salve em
`_run/<lote>/manifest.json`. Veja o schema para os campos de cada tipo.

**Para `kind:"url"`** — se houver uma ferramenta de navegador (ex.: Playwright MCP), abra a
URL, tire um screenshot PNG e coloque o caminho no campo `screenshot` do item. Sem
navegador, o item mostra só o link. Feche o navegador no fim.

Toda imagem é **embutida em base64** — o HTML fica 100% autossuficiente.

### 2) Gere o HTML
```bash
cd "$SKILL_DIR"
python3 build_panel.py _run/<lote>/manifest.json      # -> _run/<lote>/panel.html
```

### 3) Suba o servidor ao vivo e abra o painel
```bash
cd "$SKILL_DIR"
nohup python3 serve_judge.py --html _run/<lote>/panel.html --batch <lote> \
      > _run/<lote>/server.log 2>&1 &
until [ -f _run/<lote>/server.port ]; do sleep 0.2; done
PORT=$(cat _run/<lote>/server.port)
open "http://127.0.0.1:$PORT/"        # macOS; Linux: xdg-open; Windows: start
```
- Por padrão o painel só abre **nesta máquina**. Se o usuário pedir para julgar pelo
  celular/outro computador da mesma rede, suba com `--host 0.0.0.0` e passe
  `http://<ip-da-rede>:$PORT/` (avise que qualquer pessoa da rede local consegue abrir).
- **Watchdog = 180 minutos**: sem nenhuma requisição, o servidor se encerra sozinho.
- Ao completar o lote, grava `verdict.FINAL.json`; comentários feitos depois ainda são salvos;
  encerra 30 min depois.
- Na largada, encerra servidores esquecidos de lotes anteriores desta skill.

### 4) Ritmo de espera
Não fique checando de minuto em minuto. Diga ao usuário que avise quando terminar, ou cheque
o `verdict.json` com calma (a cada ~30 min). Se o painel expirar, ofereça reabrir — o
navegador preserva o que já foi marcado.

### 5) Leia o veredito
```bash
python3 read_verdict.py <lote>
```
`status: complete` = lote fechado. `partial` = em andamento. `none` = ninguém tocou ainda.

### 6) PÓS-VEREDITO — nunca responda só "ok"
1. **Agrupe os motivos das rejeições em padrões** (ex.: "3 rejeitados por CTA fraca; 2 por promessa exagerada").
2. **Declare o que vai mudar** com base nesses padrões — concreto, item a item quando fizer sentido.
3. Se `approved == 0` **ou** o usuário pedir, rode uma **NOVA RODADA**: manifesto com `round: 2`,
   os aprovados anteriores como referência fixa e os novos candidatos para julgar.
4. Entregue o resumo: quantos A/R/M, motivos agrupados e o próximo passo — não a lista crua.

## Modo arquivo (plano B)
Se o servidor não subir, abra o `panel.html` direto no navegador. O cabeçalho mostra
**"offline (modo arquivo)"** e o usuário usa **Baixar JSON** / **Copiar** para te mandar o
veredito colando na conversa.

## Notas
- Sem dependências externas: tudo é Python padrão. `build_panel.py` usa Pillow (PIL) só para
  comprimir imagens, se estiver instalado; sem ele, embute a imagem original.
- Se o usuário quiser guardar o painel, copie o `panel.html` para onde ele indicar.
- Rodadas: use `round: N` no manifesto — separa o salvamento e sai no veredito.
