# Controle de qualidade — auditar uma tradução (modo Revisar)

Pega uma versão já traduzida (por máquina, por outra pessoa, ou sua) e faz o controle de qualidade sério. O maior
risco de tradução automática não é "soar estranho" — é **inventar** (adicionar frase que não existia) e **omitir**
(engolir um trecho). Por isso a auditoria começa por aí.

## As 5 dimensões (pontue cada uma de 0 a 5)

1. **Fidelidade (0-5)** — a tradução diz exatamente o que o original diz? Sem inventar (frase/dado/claim novo),
   sem omitir (trecho engolido), sem distorcer números, nomes ou promessas.
2. **Fluência (0-5)** — soa nativo? Um leitor do país-alvo diria "isto foi escrito por alguém daqui"? Sem "cara de
   tradução", sem falso cognato, sem ordem de frase importada do português.
3. **Terminologia (0-5)** — bate com o `.ponte/glossario.json`? Termos fixos usados igual, "não-traduzir" preservados,
   nomes próprios com grafia oficial, consistência do começo ao fim.
4. **Voz (0-5)** — é a voz da marca (registro, pessoa, pontuação, padrões proibidos)? Não caiu num tom genérico
   nem violou a voz definida.
5. **Completude + formato (0-5)** — nada faltando; moeda/unidade/data/número no formato do país-alvo; placeholders,
   tags e links preservados.

Some as notas (0-25) e traduza numa recomendação: **≥22 aprovado** · **16-21 aprovado com correções** ·
**<16 refazer**.

## Lista priorizada de problemas (sempre nesta ordem de gravidade)

> **INVENÇÃO** > **OMISSÃO** > **TERMINOLOGIA** > **PRECISÃO** > **FORMATO** > **REGISTRO**

- **INVENÇÃO** — texto, dado, claim, número ou depoimento que aparece na tradução mas NÃO existe no original. É o
  pior defeito. Aponte cada caso.
- **OMISSÃO** — trecho/frase/seção do original que sumiu na tradução.
- **TERMINOLOGIA** — termo que diverge do glossário ou é inconsistente entre trechos; "não-traduzir" que foi traduzido.
- **PRECISÃO** — sentido levemente torcido, falso cognato, número/tempo verbal errado.
- **FORMATO** — moeda/unidade/data/número no padrão errado, placeholder/tag quebrado, link trocado.
- **REGISTRO** — tom/voz fora do definido (formal demais, informal demais, buzzword proibida, ! em rótulo).

Para cada problema: **[GRAVIDADE] trecho → o que está errado → correção sugerida.**

## Anti-invenção / anti-omissão (a checagem que nunca se pula)
1. Percorra o original e a tradução **em paralelo**, parágrafo a parágrafo.
2. Todo parágrafo do original tem um correspondente na tradução? (marca omissão)
3. Todo parágrafo da tradução tem origem no original? (marca invenção)
4. Números, nomes próprios, datas, preços e claims batem **um a um**?
5. Nada de "melhorar" o original: se o autor não disse, a tradução não diz.

## Entrega
1. **Nota por dimensão** (5 linhas) + total /25 + recomendação.
2. **Lista priorizada** de problemas (na ordem acima).
3. **Versão corrigida** já aplicando o glossário e os consertos — pronta para o dono usar.
4. Resumo em PT-BR: "encontrei X invenções, Y omissões, Z de terminologia; a versão corrigida está abaixo".
