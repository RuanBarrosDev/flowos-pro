# Transcriar — a metodologia (leia antes dos modos Transcriar, Página e Documento)

Transcriar é reescrever para que o leitor estrangeiro tenha **a mesma reação** que o brasileiro — não dizer
"a mesma coisa em outro idioma". Tradução literal soa robótica, mata a persuasão e deixa "cara de tradução".
Sempre leia `.ponte/glossario.json` (voz + não-traduzir + termos) antes de escrever a primeira palavra.

## Os 5 passos (todo texto passa pelos cinco)

**Passo 0 — Classifique o tipo.** O tipo manda no registro:
- **Rótulo/UI curto** (botão, título, campo, menu): brevidade máxima, verbo imperativo, zero decoração.
- **Texto de venda longo** (página, carta, e-mail, VSL, anúncio): fluência natural, ritmo, persuasão.
- **Institucional/informativo** (sobre, FAQ, política): claro e factual, respeita a inteligência do leitor.

**Passo 1 — Entenda antes de escrever.** Leia a peça inteira. Ache o argumento, a promessa central, a
sequência emocional (a "montanha-russa" que leva à ação). Marque as provas e os claims.

**Passo 2 — Extraia a intenção.** Diga em UMA frase o que o leitor deve pensar, sentir e fazer depois de ler.
É essa intenção que você vai recriar — não a estrutura das frases.

**Passo 3 — Escreva nativo.** Componha como se estivesse escrevendo do zero no idioma-alvo. Um nativo não pode
perceber que é tradução. Preserve os dispositivos retóricos (pergunta retórica, contraste, prova, gancho), mas
reconstrua as frases na lógica do idioma-alvo. Se o original tem 3 palavras, mire 3; se o alvo precisa de 5,
use 5 — nunca encha linguiça.

**Passo 4 — Passe o anti-slop.** Tire a "gordura de tradução":
- Conectivos e muletas que entraram sem estar no original ("neste sentido", "vale ressaltar", "in this regard").
- Hedges e amaciadores ausentes no original ("talvez", "parece que", "might", "perhaps").
- Advérbios de enchimento ("basicamente", "essencialmente", "actually", "simply").
- Falsos cognatos (pt "pretender" ≠ en "pretend"; pt "atualmente" ≠ en "actually"; pt "eventualmente" ≠ en "eventually").
- Qualquer palavra na tradução sem correspondência de intenção no original.
- Violações da voz da marca (veja `.ponte/glossario.json` → `voz.proibidos`).

## Regras para rótulos e UI (botões, campos, menus, títulos curtos)
1. **Consistência é obrigatória.** O mesmo conceito recebe sempre a mesma palavra em todo o material.
2. **Preserve placeholders exatamente.** `{nome}`, `{{count}}`, `%s`, `%1$s`, `%{var}` ficam iguais, sem traduzir.
3. **Preserve tags/markup.** `<b>`, `<span>`, `<br/>`, `<0>`, `<1>` ficam como estão; traduza só o texto entre tags.
4. **Botão = verbo imperativo nativo.** "Agendar" → "Book", não "Booking". "Baixar" → "Download", não "The Download".
5. **Teto de tamanho ~150%.** Rótulo do alvo não deve passar de 1,5× o tamanho do original (alemão estica; sinalize).
6. **Capitalização segue o idioma.** Inglês usa Title Case em títulos; português, espanhol e francês capitalizam
   só a primeira palavra; alemão capitaliza substantivos.
7. **Erro específico, não genérico.** Mensagem de erro traduz o erro exato, não um "algo deu errado".

## Textos longos e livros (modo Documento)
Para e-book, livro, apostila, capítulo ou qualquer material com muitas seções:
1. **Monte/atualize o glossário primeiro** (personagens, termos recorrentes, nomes) para não oscilar entre capítulos.
2. **Divida em blocos por capítulo/seção.** Nunca corte no meio de uma tabela ou de uma cena. Trabalhe bloco a bloco.
3. **Mantenha um índice do que foi feito** (capítulo, status) para retomar sem repetir nem pular.
4. **Preserve a estrutura**: mesma quantidade de capítulos, títulos, listas, tabelas e notas. Nada some, nada é
   inventado para "completar".
5. **Feche com uma varredura de consistência**: o mesmo termo/nome aparece igual do começo ao fim?
6. Para publicação (ex.: Amazon KDP), marque `⚠️ REVISÃO PROFISSIONAL LOCAL` no que for claim de saúde, jurídico
   ou financeiro, e lembre o dono de um revisor nativo antes de publicar — a Ponte deixa 95% pronto, não assina por você.

## Cultura, não só idioma
- **Objeções mudam de país.** O que trava a compra no Brasil pode não ser o que trava lá fora — reancore a copy nas
  objeções locais (veja o modo Mercado).
- **Provas e números.** Mantenha depoimentos, cases e estatísticas exatos; adapte só o enquadramento. Nunca invente
  um depoimento "equivalente".
- **Referências locais.** Feriados, gírias, exemplos e comparações precisam de um equivalente que faça sentido no
  país-alvo — traduzir a referência ao pé da letra confunde.
- **Moeda, unidade, data, formato de número**: rode `scripts/formato.py` e converta; marque `⚠️ CONFIRMAR` no que
  depender do câmbio do dia.

## Checklist de entrega (transcriação)
- [ ] Li o glossário antes de escrever (voz, não-traduzir, termos).
- [ ] Sei dizer a intenção de cada trecho em uma frase.
- [ ] Recriei os dispositivos retóricos, não só as palavras.
- [ ] O ritmo soa natural no idioma-alvo (não "cara de tradução").
- [ ] Placeholders, tags e links preservados exatamente.
- [ ] Anti-slop feito (sem gordura, sem falso cognato, sem hedge extra).
- [ ] Moeda/unidade/data convertidas + `⚠️ CONFIRMAR` onde precisa.
- [ ] `⚠️ REVISÃO PROFISSIONAL LOCAL` em tudo regulado.
- [ ] Trabalho salvo em `.ponte/trabalhos/` + resumo em PT-BR do que mudou.
