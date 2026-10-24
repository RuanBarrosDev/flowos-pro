# veredito — schema do manifesto

O manifesto é um único JSON. `build_panel.py` o transforma em um HTML autossuficiente
(motor `template/panel.html`). Julgamento é **sempre individual** (A/R/M/S por item) —
nunca comparação A/B, nunca nota 1–5.

## Topo

| campo      | tipo    | obrigatório | descrição |
|------------|---------|-------------|-----------|
| `title`    | string  | recomendado | Título no cabeçalho do painel. |
| `subtitle` | string  | não         | Subtítulo (aparece antes de "Lote: …"). |
| `batch`    | string  | recomendado | ID do lote. Vira nome da pasta em `_run/<batch>/` e chave do localStorage. Se ausente, usa o nome do arquivo do manifesto. |
| `round`    | int     | não         | Rodada (padrão 1). Numa 2ª rodada, use `round: 2` — muda a chave do localStorage e sai no veredito. |
| `items`    | array   | sim         | Lista de itens a julgar. |

## Item (comum a todos)

| campo   | tipo   | descrição |
|---------|--------|-----------|
| `id`    | string | **Obrigatório e único** no lote. Sai no veredito. |
| `kind`  | string | Um de: `image`, `text`, `markdown`, `diff`, `change_card`, `url`, `code`. |
| `meta`  | array  | Opcional. Linhas extras no painel lateral: `[{ "k": "Rótulo", "v": "valor" }]`. |
| `no_compress` | bool | Opcional. Em imagens, embute o arquivo cru (sem recompressão JPEG). |

## Por kind

### `image` — imagem (thumb, arte, print)
| campo | descrição |
|-------|-----------|
| `src` | Caminho local **ou** data: URI **ou** http(s). Caminho local → embutido em base64 (comprimido ~1100px / JPEG q70). |
| `title`, `caption`, `slug` | Metadados opcionais. |

### `text` — título / frase / CTA
| campo | descrição |
|-------|-----------|
| `text` | O texto a julgar. |
| `subkind` | `"cta"` mostra como chamada destacada; qualquer outro valor = título/frase grande. |
| `fonte`, `angulo` | Metadados opcionais. |

### `markdown` — texto longo (ideia, parágrafos)
| campo | descrição |
|-------|-----------|
| `text` | Markdown mínimo: `**negrito**`, `*itálico*`, `` `code` ``, `#`/`##`/`###`, listas `-`/`1.`, parágrafos por linha em branco. |
| `name` | Rótulo em destaque no topo (opcional). |
| `fonte` | Metadado opcional. |
| `img` | Opcional. Imagem (diagrama, print) mostrada ACIMA do texto; caminho local → base64. Clique amplia 2×. Para diagrama com texto miúdo use `no_compress: true` (senão vira JPEG 1100px). |

### `diff` — diff de código
| campo | descrição |
|-------|-----------|
| `title` | Título da mudança. |
| `file`  | Caminho do arquivo. |
| `lines` | Array de `{ "k": " "\|"+"\|"-", "t": "linha" }`. `+` adição, `-` remoção, `" "` contexto. |

### `change_card` — card de mudança (o quê / porquê / risco)
| campo | descrição |
|-------|-----------|
| `title` | Título. |
| `area`  | Área afetada. |
| `what`  | O que muda. |
| `why`   | Por que mudar. |
| `risk`  | Texto do risco (ex.: "alto — mexe no financeiro"). |
| `level` | `"baixo"` \| `"medio"` \| `"alto"` — cor do selo de risco. |

### `url` — link / página capturada
| campo | descrição |
|-------|-----------|
| `url` | A URL (sempre presente; vira o link "Abrir em nova aba"). |
| `domain` | Domínio exibido. |
| `title`, `desc` | Título e descrição. |
| `screenshot` | Caminho local de um PNG/JPG já capturado → embutido em base64 e mostrado como print. |
| `img` | Alternativa a `screenshot`: uma data: URI de screenshot já pronta. |

> **Fluxo de captura (feito pelo agente, não pelo build_panel):** para cada `url`,
> navegar com o Playwright MCP, esperar carregar, `browser_take_screenshot` para um PNG,
> e pôr o caminho no campo `screenshot`. O `build_panel.py` comprime e embute. Perfil
> Chrome do MCP é **global (um browser por vez)**; se der "Browser is already in use",
> usar `--isolated`. **Fechar o browser no fim.**

### `code` — trecho de código
| campo | descrição |
|-------|-----------|
| `title` | Título. |
| `lang`  | Linguagem (rótulo). |
| `code`  | O código (texto; quebras `\n`). |

## Veredito de saída (verdict.json / verdict.FINAL.json)

```json
{
  "batch": "meu-lote",
  "title": "…",
  "round": 1,
  "reviewed_at": "2026-09-21T18:00:00.000Z",
  "batch_note": "nota geral do lote",
  "counts": { "approved": 3, "rejected": 2, "maybe": 1, "pending": 0 },
  "items":    [ { "id", "kind", "label", "verdict", "comment" } ],
  "approved": [ { "id", "label", "comment" } ],
  "maybe":    [ { "id", "label", "comment" } ],
  "rejected": [ { "id", "label", "comment" } ]
}
```

`verdict.json` é reescrito a cada ação (parcial). `verdict.FINAL.json` só é gravado
quando `counts.pending == 0` (lote completo) — nesse momento o servidor se mata ~1s depois.

### `video` — vídeo tocando no card (autoplay, loop, mudo, com controles)
| campo | descrição |
|-------|-----------|
| `src` | URL http(s) do vídeo (NÃO é embutido; sirva a pasta, ex. `python3 -m http.server`). |
| `url`, `domain` | Opcional: link extra embaixo (ex. versão jogável). |
Em `kind:"url"`, o campo `video` faz o card tocar esse vídeo no lugar do screenshot.
