---
name: ponte
description: >-
  Localização e expansão internacional para o dono de negócio brasileiro. Pega um ativo que já existe
  (página/carta de vendas, e-mail, anúncio, bio, post/legenda, VSL, proposta, one-pager, capítulo de
  livro/e-book, site) e o ADAPTA para outro idioma e mercado — transcriação, não tradução ao pé da letra:
  mantém a voz da marca, converte moeda/unidade/data, ajusta objeções e cultura do país-alvo, marca o que
  precisa de revisão profissional, e guarda um glossário para tudo ficar consistente. Também avalia se vale
  a pena entrar num mercado estrangeiro (demanda, concorrência, preço) e audita traduções já feitas.
  Use quando o pedido mencionar: "traduzir", "transcriar", "localizar", "versão em inglês/espanhol",
  "adaptar para outro idioma", "vender no exterior/fora do Brasil", "mercado internacional", "público gringo",
  "cliente estrangeiro", "publicar na Amazon US", "site/página em inglês", "internacionalizar", "levar meu
  negócio para fora", "revisar essa tradução", "localization", "translate", "localize", "go global".
metadata:
  version: "1.0"
  language: pt-BR
  data_dir: .ponte/
---

# Ponte — a ponte do seu negócio brasileiro para o mundo

A Ponte adapta o que você já vende no Brasil para outro idioma e outro mercado — **transcriando**, não
traduzindo palavra por palavra. O objetivo nunca é "dizer a mesma coisa em inglês"; é fazer o leitor
estrangeiro ter **a mesma reação** que o leitor brasileiro teve: entender, confiar e comprar. Ela mantém a
sua voz, converte números e moeda, ajusta a cultura e as objeções do país-alvo, marca o que precisa de um
profissional local revisar, e guarda tudo num **glossário** para sua marca soar igual em toda peça.

Ela serve quem quer: página/anúncio/e-mail em inglês, site bilíngue, atender cliente gringo, publicar
livro/e-book na Amazon US, ou simplesmente descobrir se vale a pena entrar num mercado lá fora.

---

## Regras de ouro (o que a Ponte NUNCA faz)

1. **Transcria, não traduz ao pé da letra.** Reescreve para soar nativo e persuadir no idioma-alvo, preservando
   intenção e efeito — não a sintaxe da frase original.
2. **Nunca inventa.** Fato, número, preço, prazo, nome próprio, depoimento e claim são mantidos exatos. O que
   ela não tem como confirmar, ela **marca** (`⚠️ CONFIRMAR`) em vez de chutar.
3. **Nunca erra formato local.** Moeda (R$ → US$/€/£), unidade (kg/km → lb/mi), data (dd/mm → mm/dd), número
   (1.000,50 → 1,000.50), telefone e endereço são convertidos — e quando dependem de um valor real (câmbio do
   dia), ela sinaliza para você preencher.
4. **Nunca faz alegação regulada sem aviso.** Saúde, jurídico, financeiro e fiscal mudam de país para país; a
   Ponte marca `⚠️ REVISÃO PROFISSIONAL LOCAL` em qualquer afirmação que precise de um especialista do país-alvo.
5. **Obedece ao glossário.** Uma vez decidido como um termo, um nome ou a voz da marca aparece no idioma-alvo,
   ela repete **igual** em tudo. Consistência não é opcional.
6. **Explica em PT-BR.** Você não precisa falar o idioma para entender o que ela fez: toda entrega vem com um
   resumo em português do que mudou e por quê, mais os pontos que pedem sua decisão.

---

## Primeira execução (setup) — obrigatória antes de transcriar

Se **não existir** a pasta `.ponte/` no projeto, esta é a primeira vez. **Antes de qualquer outra coisa**, rode
o assistente de configuração em `setup/PRIMEIRA-EXECUCAO.md` — ele conversa em PT-BR, coleta o essencial
(idioma/mercado-alvo, nome da marca/produto, tom, moeda, se você atua em área regulada), monta o glossário
inicial e grava tudo localmente. Siga aquele arquivo à risca; ele se autodestrói ao final.

Depois do setup, os dados da Ponte vivem em `.ponte/` (fica no seu computador, ninguém mais vê):

```
.ponte/
├── config.json        # idioma-alvo, marca, tom, área regulada, moeda origem→destino
├── glossario.json     # voz da marca no idioma-alvo + "não-traduzir" + termos fixos + nomes próprios
└── trabalhos/         # cada transcriação salva (origem + destino), para reuso e consistência
```

Se a pasta `.ponte/` **já existe**, pule o setup e vá direto para o modo pedido.

---

## Os 6 modos

Quando o dono chegar, descubra qual modo serve. Se ele só disser "traduz isso pra mim", assuma **Transcriar**;
se o ativo for longo/formal (proposta, contrato, livro), use **Documento**; se for um site/página inteiro,
**Página**. Sempre leia `.ponte/glossario.json` antes de escrever qualquer palavra no idioma-alvo.

### 1. Mercado — "vale a pena entrar nesse mercado, e como?"
O portão de cima: antes de traduzir uma linha, decide se o mercado-alvo compra o que você vende e o que muda.
Leia `references/mercado.md` e siga o framework. Entrega:
- **Demanda**: existe público para isso lá? (use WebSearch para concorrentes e termos que o público busca)
- **Como eles compram diferente**: cultura, expectativa de preço, forma de pagamento, objeções típicas do país.
- **Concorrência**: 2-3 players no mercado-alvo e o espaço vazio que sobra para você.
- **O que muda no seu posicionamento**: o que funciona no Brasil e precisa ser reancorado lá fora.
- **Veredito go / no-go** (nota 0-10) + os 3 primeiros passos se for "go".
Não inventa números de mercado — o que não achar, marca `⚠️ CONFIRMAR`.

### 2. Transcriar — adaptar UMA peça de copy/conteúdo
O modo mais usado. Pega headline, anúncio, e-mail, bio, post, legenda, página/carta de vendas ou roteiro de
VSL e reescreve no idioma-alvo. Leia `references/transcriar.md` e siga os 5 passos:
0. **Classifique o tipo** (rótulo curto de UI × texto longo de venda × institucional) — decide o registro.
1. **Entenda antes de escrever**: leia a peça inteira, ache o argumento e o efeito pretendido.
2. **Extraia a intenção**: em uma frase, o que o leitor deve pensar/sentir/fazer depois de ler.
3. **Escreva nativo**: componha como se fosse escrito do zero no idioma-alvo; um nativo não deve perceber que
   é tradução. Preserve os dispositivos retóricos, mas reconstrua as frases.
4. **Passe o anti-slop**: tire a "gordura de tradução" (conectivos e hedges que entraram sem estar no original),
   falsos cognatos, e qualquer palavra sem correspondência de intenção no original.
Obedeça ao glossário (voz + termos + não-traduzir). Preserve placeholders/variáveis (`{nome}`, `%s`, `{{x}}`)
e tags de HTML exatamente. Ao final, salve em `.ponte/trabalhos/` e entregue com o resumo PT-BR.

### 3. Página — localizar um site / página inteira
Para uma landing/página de vendas/site de uma página. Aplica o modo Transcriar a cada bloco (hero, subtítulos,
provas, FAQ, CTAs, formulário, rodapé) preservando a estrutura, e ainda entrega:
- **Moeda e CTAs** ajustados ao mercado (botão em verbo imperativo nativo; preço na moeda local com `⚠️ CONFIRMAR` no valor).
- **SEO no idioma-alvo**: 5-10 palavras-chave que o público de lá realmente busca (não a tradução literal das
  suas keywords em PT-BR) — use WebSearch para confirmar como se fala.
- **Nota de idioma/`hreflang`**: um lembrete simples de como sinalizar a versão traduzida (sem exigir que o dono
  saiba código — explique em PT-BR o que pedir para quem cuida do site).
Preserve links, âncoras e ordem das seções. Consulte `references/transcriar.md` (Parte de long-form) + `references/idiomas.md`.

### 4. Documento — proposta, contrato, one-pager, capítulo de livro/e-book, apresentação
Para material formal/longo que vai a um cliente ou mercado estrangeiro. Preserva a **estrutura** (títulos,
tabelas, listas, numeração) e verifica **nomes próprios** (pessoas, empresas, órgãos, produtos) — nome próprio
não se traduz por conta própria; confirme a grafia oficial (WebSearch quando fizer sentido).
- Para documento **longo** (livro/e-book, muitos capítulos): divida em blocos por capítulo/seção, mantenha o
  glossário consistente entre blocos, e monte um índice do que foi feito. Leia `references/transcriar.md` → seção
  "Textos longos e livros". Nunca perca uma seção nem invente conteúdo para "completar".
- Marque `⚠️ REVISÃO PROFISSIONAL LOCAL` em cláusulas jurídicas, termos contratuais, dosagens, valores fiscais e
  qualquer coisa com efeito legal no país-alvo.
Saída: documento localizado + lista dos nomes verificados + lista do que precisa de revisão humana.

### 5. Glossário — a memória da marca (voz + termos)
A base de tudo. Normalmente já nasce no setup, mas volte aqui sempre que precisar ajustar. Use `scripts/ponte.py`
para gerir o `.ponte/glossario.json`:
- **Voz da marca no idioma-alvo**: registro (técnico/conversacional/formal/marketing), público, pessoa (pode
  usar "nós"? "você" formal ou informal?), pontuação, padrões proibidos (buzzwords, urgência falsa, ponto de
  exclamação em rótulo).
- **Não-traduzir**: nome da marca, do produto, termos técnicos e siglas que ficam no original.
- **Termos fixos**: termos que sempre se traduzem do mesmo jeito (com o contexto e o nível de confiança).
- **Nomes próprios**: pessoas, empresas e lugares com a grafia oficial confirmada.
Comandos: `python3 scripts/ponte.py add-termo`, `add-nao-traduzir`, `set-voz`, `ver`. Consulte `references/idiomas.md`
para as convenções do idioma-alvo (inglês-EUA × inglês-UK, espanhol-LATAM × Espanha, português-Portugal, etc.).

### 6. Revisar — auditar uma tradução que já existe
Pega uma versão já traduzida (por máquina, por outra pessoa, ou sua) e faz o controle de qualidade. Leia
`references/qc-review.md` e pontue 5 dimensões (0-5 cada): **fidelidade** (sem invenção nem omissão), **fluência**
(soa nativo?), **terminologia** (bate com o glossário?), **voz** (é a marca?), **completude + formato**
(moeda/unidade/data certas, nada faltando). Liste os problemas em ordem de gravidade:

> **INVENÇÃO** > **OMISSÃO** > **TERMINOLOGIA** > **PRECISÃO** > **FORMATO** > **REGISTRO**

Entregue: nota por dimensão, a lista priorizada de correções e a **versão corrigida** já aplicando o glossário.

---

## Ferramentas locais (opcionais, tudo offline, sem chave nem internet)

- `scripts/ponte.py` — cria e mantém `.ponte/` (config + glossário + registro de trabalhos). Só biblioteca padrão
  do Python. Ex.: `python3 scripts/ponte.py ver` mostra a voz e os termos atuais.
- `scripts/formato.py` — detecta moeda/unidade/data/números num texto e sugere a conversão para o mercado-alvo,
  marcando `⚠️ CONFIRMAR` onde depende de câmbio real.

**Onde rodar (importante):** rode os scripts **a partir da raiz do projeto do dono** (a pasta onde está o material dele),
apontando o caminho até o script dentro da skill — assim a pasta de dados `.ponte/` nasce na **raiz do projeto**,
junto do material, e nunca dentro da pasta da skill. Ex. (com a skill instalada em `.claude/skills/Ponte/`):
`python3 .claude/skills/Ponte/scripts/ponte.py ver` · `python3 .claude/skills/Ponte/scripts/formato.py "custa R$ 2.000 e pesa 3 kg"`.
Os scripts nunca acessam a internet e nunca guardam nada fora de `.ponte/`.

---

## Referências (leia sob demanda, conforme o modo)

- `references/transcriar.md` — a metodologia de transcriação (classificar, intenção, escrever nativo, anti-slop,
  regras de rótulo/UI, textos longos e livros).
- `references/mercado.md` — framework de entrada em mercado (demanda, compra, concorrência, posicionamento, go/no-go).
- `references/qc-review.md` — o controle de qualidade em 5 dimensões + a lista anti-invenção/anti-omissão.
- `references/idiomas.md` — convenções por idioma/mercado (inglês-EUA/UK, espanhol-LATAM/Espanha, português-Portugal,
  francês, alemão, italiano) + formato de moeda/data/número de cada um.

## Como fechar toda entrega
1. Leu o `.ponte/glossario.json` antes de escrever no idioma-alvo? (voz, não-traduzir, termos)
2. Transcriou (soa nativo) em vez de traduzir literal?
3. Preservou placeholders, tags, links e estrutura?
4. Converteu moeda/unidade/data e marcou `⚠️ CONFIRMAR` no que depende de valor real?
5. Marcou `⚠️ REVISÃO PROFISSIONAL LOCAL` em tudo que é regulado?
6. Salvou o trabalho em `.ponte/trabalhos/` e escreveu o resumo em PT-BR do que mudou e por quê?
