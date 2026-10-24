# Ponte 🌉

**A ponte do seu negócio brasileiro para o mundo.** A Ponte adapta o que você já vende no Brasil para outro
idioma e outro mercado — **transcriando**, não traduzindo palavra por palavra. O objetivo é fazer o leitor
estrangeiro ter a mesma reação que o brasileiro: entender, confiar e comprar.

Serve para: página/anúncio/e-mail em inglês, site bilíngue, atender cliente de fora, publicar livro/e-book na
Amazon US, ou descobrir se vale a pena entrar num mercado lá fora.

## O que ela faz (6 modos)

1. **Mercado** — avalia se vale a pena entrar num mercado estrangeiro (demanda, concorrência, preço, objeções) → go/no-go.
2. **Transcriar** — adapta uma peça (headline, anúncio, e-mail, bio, post, página/carta de vendas, VSL) para o idioma-alvo.
3. **Página** — localiza um site/página inteira, com moeda, CTAs e palavras-chave de SEO no novo idioma.
4. **Documento** — proposta, contrato, one-pager, apresentação, capítulo de livro/e-book — preservando estrutura e nomes.
5. **Glossário** — a memória da marca: voz no idioma-alvo + termos que não se traduzem + termos fixos. Tudo consistente.
6. **Revisar** — audita uma tradução já feita em 5 dimensões e devolve a versão corrigida.

## Regras de ouro

- Transcria, **não** traduz literal. · Nunca inventa (marca `⚠️ CONFIRMAR`). · Converte moeda/unidade/data.
- Marca `⚠️ REVISÃO PROFISSIONAL LOCAL` no que é regulado (saúde/jurídico/financeiro). · Obedece ao glossário.
- Explica tudo em **PT-BR** — você não precisa falar o idioma para entender o que ela fez.

## Instalação

1. Descompacte o arquivo.
2. Copie a pasta `Ponte/` para dentro de `.claude/skills/` do seu projeto (ou de `~/.claude/skills/` para usar em qualquer projeto).
3. Abra o Claude Code nesse projeto. Na primeira vez, diga algo como **"quero traduzir minha página para inglês"** —
   a Ponte roda o assistente de configuração (idioma-alvo, marca, tom, moeda) e cria a pasta local `.ponte/`.

## Como usar (é só conversar, em português)

- "Faz um estudo se vale a pena vender meu serviço nos Estados Unidos." → modo **Mercado**
- "Transcria essa página de vendas para inglês." → modo **Transcriar**
- "Localiza meu site inteiro para o público de Portugal." → modo **Página**
- "Adapta essa proposta para um cliente dos EUA." / "Prepara meu e-book para a Amazon US." → modo **Documento**
- "Revisa essa tradução que fizeram e me diz o que está errado." → modo **Revisar**

Você conversa em português; a Ponte entrega o material no idioma-alvo **mais** um resumo em PT-BR do que mudou.

## Onde ficam seus dados

Tudo local, no seu computador, dentro de `.ponte/` (não vai para lugar nenhum):
- `config.json` — idioma-alvo, marca, tom, moeda, área regulada.
- `glossario.json` — voz da marca + "não-traduzir" + termos fixos + nomes próprios.
- `trabalhos/` — cada transcriação salva, para reuso e consistência.

## Ferramentas incluídas (opcionais, offline, sem chave)

- `scripts/ponte.py` — cria e mantém `.ponte/` (config + glossário). Ex.: `python3 scripts/ponte.py ver`.
- `scripts/formato.py` — detecta moeda/unidade/data num texto e sugere a conversão. Ex.:
  `python3 scripts/formato.py "custa R$ 2.000 e pesa 3 kg"`.

Só usam a biblioteca padrão do Python 3 — nada para instalar, nenhuma conexão com a internet.

## Licença

MIT. Feito para a comunidade **Maestros da IA**.
