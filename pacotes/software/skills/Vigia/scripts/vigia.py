#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Vigia — o plantão do seu sistema no ar.

Ferramenta de apoio, só biblioteca padrão do Python (zero instalação, zero conta,
zero API paga). O dono não roda isto na mão: a skill Vigia usa por baixo.

Comandos:
  init                     cria a pasta vigia/ e o esqueleto de config.json
  check [URL]              checa de verdade um endereço (responde? tempo? codigo?)
                          sem URL, usa a "url_principal" do config
  novo-incidente "<txt>"   cria vigia/plantao/incidente-AAAA-MM-DD-<slug>.md
  nova-autopsia  "<txt>"   cria vigia/plantao/autopsia-AAAA-MM-DD-<slug>.md
  lista                    lista plantoes e autopsias ja registrados

Privacidade: a UNICA parte que acessa a rede e o comando `check`, e ele so
acessa o endereco que voce mesmo colocou no seu config (ou passou na linha).
Nada e enviado para fora; tudo mais fica em arquivos locais na pasta vigia/.
"""

import sys
import os
import json
import re
import time
import unicodedata
from datetime import date, datetime

def _raiz_projeto():
    """Onde a pasta de trabalho 'vigia/' deve morar: SEMPRE a raiz do projeto do
    dono, nunca dentro da pasta da skill. Se o script for chamado de dentro de
    uma arvore .claude/skills/..., sobe ate a pasta que CONTEM o .claude. Caso
    contrario, usa o diretorio atual (a raiz do projeto de onde o dono trabalha).
    """
    cwd = os.getcwd()
    marker = os.sep + ".claude" + os.sep
    idx = cwd.find(marker)
    if idx != -1:
        return cwd[:idx] or os.sep
    return cwd


RAIZ = os.path.join(_raiz_projeto(), "vigia")
CONFIG = os.path.join(RAIZ, "config.json")
PLANTAO = os.path.join(RAIZ, "plantao")


def _slug(txt):
    txt = unicodedata.normalize("NFKD", txt).encode("ascii", "ignore").decode("ascii")
    txt = txt.lower()
    txt = re.sub(r"[^a-z0-9]+", "-", txt).strip("-")
    return (txt or "sem-titulo")[:48]


def _garante_pastas():
    os.makedirs(PLANTAO, exist_ok=True)


def cmd_init():
    _garante_pastas()
    if os.path.exists(CONFIG):
        print(f"[vigia] config ja existe em {CONFIG} — nada a fazer.")
        return 0
    esqueleto = {
        "nome_sistema": "",
        "o_que_e": "",
        "url_principal": "",
        "urls_extras": [],
        "normal_responde_em_segundos": 3,
        "onde_ficam_os_erros": "",
        "quem_avisar": "",
        "criado_em": datetime.now().strftime("%Y-%m-%d %H:%M"),
    }
    with open(CONFIG, "w", encoding="utf-8") as f:
        json.dump(esqueleto, f, ensure_ascii=False, indent=2)
    print(f"[vigia] criado {CONFIG} — preencha o Cartão de Saúde na primeira conversa.")
    return 0


def _carrega_config():
    if os.path.exists(CONFIG):
        try:
            with open(CONFIG, encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return {}
    return {}


def cmd_check(url=None):
    """Checagem real de disponibilidade do endereco do PROPRIO dono."""
    import urllib.request
    import ssl

    if not url:
        cfg = _carrega_config()
        url = (cfg.get("url_principal") or "").strip()
    if not url:
        print("[vigia] sem URL para checar. Passe a URL ou preencha 'url_principal' no config.")
        return 2
    if not re.match(r"^https?://", url):
        url = "https://" + url

    ctx = ssl.create_default_context()
    req = urllib.request.Request(url, method="GET", headers={"User-Agent": "Vigia/1.0 (health-check do proprio dono)"})
    inicio = time.time()
    try:
        with urllib.request.urlopen(req, timeout=15, context=ctx) as resp:
            dt = time.time() - inicio
            codigo = resp.getcode()
            no_ar = 200 <= codigo < 400
            print(f"NO_AR={'sim' if no_ar else 'nao'}  CODIGO={codigo}  TEMPO={dt:.2f}s  URL={url}")
            if dt > 3:
                print("  -> lento: acima de 3s. Investigar 'Rápido?' (ver referencias/gravidade-e-sinais.md).")
            return 0 if no_ar else 1
    except urllib.error.HTTPError as e:
        dt = time.time() - inicio
        print(f"NO_AR=nao  CODIGO={e.code}  TEMPO={dt:.2f}s  URL={url}  (erro do servidor: {e.reason})")
        return 1
    except Exception as e:
        dt = time.time() - inicio
        print(f"NO_AR=nao  CODIGO=--  TEMPO={dt:.2f}s  URL={url}  (nao respondeu: {type(e).__name__}: {e})")
        return 1


TEMPLATE_INCIDENTE = """# Plantão — {resumo}

- **Aberto em:** {agora}
- **Gravidade:** (🔴 Vermelho / 🟠 Laranja / 🟡 Amarelo / ⚪ Cinza)
- **O que está acontecendo:**
- **Desde quando:**
- **Quem está afetado:**
- **O que mudou nas últimas horas (deploy/ajuste/config):**

## Sinais coletados (✅ FATO)
-

## Hipóteses em aberto (🔎 HIPÓTESE, mais provável primeiro)
1.

## Ações tomadas (linha do tempo)
| Hora | O que fizemos | Resultado |
|------|---------------|-----------|
|      |               |           |

## Volta confirmada?
- [ ] Endereço responde de novo
- [ ] Erro sumiu
- [ ] Cliente consegue usar

## Mensagem enviada ao cliente?
- [ ] Sim, em: ____   (texto em referencias/mensagens-ao-cliente.md)
"""

TEMPLATE_AUTOPSIA = """# Autópsia (revisão sem culpa) — {resumo}

- **Data:** {agora}
- **Incidente relacionado:** vigia/plantao/incidente-...md

## 1. Resumo de uma linha
(o que quebrou, quanto tempo durou, quem sentiu)

## 2. Linha do tempo
| Hora | Evento |
|------|--------|
|      | primeiro sinal |
|      | voltou |

## 3. Por que foi possível (sistema, nunca pessoa)
- Por quê? ->
  - Por quê? ->
    - Por quê? -> (raiz)

## 4. O que foi bem (manter)
-

## 5. Ações para não repetir
| Ação | Dono | Prazo |
|------|------|-------|
|      |      |       |

## 6. Sensor novo a instalar (fecha o loop -> Modo 1 · Sensores)
-
"""


def _cria_doc(prefixo, resumo, template):
    _garante_pastas()
    slug = _slug(resumo)
    nome = f"{prefixo}-{date.today().isoformat()}-{slug}.md"
    caminho = os.path.join(PLANTAO, nome)
    if os.path.exists(caminho):
        base, ext = os.path.splitext(caminho)
        caminho = f"{base}-{datetime.now().strftime('%H%M')}{ext}"
    with open(caminho, "w", encoding="utf-8") as f:
        f.write(template.format(resumo=resumo, agora=datetime.now().strftime("%Y-%m-%d %H:%M")))
    print(f"[vigia] criado {caminho}")
    return caminho


def cmd_novo_incidente(resumo):
    _cria_doc("incidente", resumo, TEMPLATE_INCIDENTE)
    return 0


def cmd_nova_autopsia(resumo):
    _cria_doc("autopsia", resumo, TEMPLATE_AUTOPSIA)
    return 0


def cmd_lista():
    if not os.path.isdir(PLANTAO):
        print("[vigia] nenhum plantão registrado ainda.")
        return 0
    arqs = sorted(os.listdir(PLANTAO))
    if not arqs:
        print("[vigia] nenhum plantão registrado ainda.")
        return 0
    inc = [a for a in arqs if a.startswith("incidente-")]
    aut = [a for a in arqs if a.startswith("autopsia-")]
    print(f"Plantoes ({len(inc)}):")
    for a in inc:
        print("  -", a)
    print(f"Autopsias ({len(aut)}):")
    for a in aut:
        print("  -", a)
    return 0


def main(argv):
    if not argv:
        print(__doc__)
        return 0
    cmd = argv[0]
    arg = argv[1] if len(argv) > 1 else None
    if cmd == "init":
        return cmd_init()
    if cmd == "check":
        return cmd_check(arg)
    if cmd == "novo-incidente":
        if not arg:
            print('Uso: novo-incidente "<resumo>"')
            return 2
        return cmd_novo_incidente(arg)
    if cmd == "nova-autopsia":
        if not arg:
            print('Uso: nova-autopsia "<resumo>"')
            return 2
        return cmd_nova_autopsia(arg)
    if cmd == "lista":
        return cmd_lista()
    print(f"[vigia] comando desconhecido: {cmd}")
    print(__doc__)
    return 2


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
