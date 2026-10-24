# Primeira conversa do Estopim (configuração — só na primeira vez)

Este arquivo existe **apenas na primeira vez** que o membro usa o Estopim. Quando ele aparece,
a IA deve rodar esta configuração curta ANTES de qualquer trabalho de campanha, gravar o resultado
e depois se autodestruir.

## O que fazer (passo a passo)

1. **Diga, em uma frase, o que vem agora:**
   > "Antes de criar campanhas, vou te conhecer rapidinho — umas 6 perguntas — pra não te
   > perguntar o básico toda vez. Leva 2 minutos."

2. **Faça as perguntas UMA DE CADA VEZ**, em linguagem simples, esperando a resposta antes da
   próxima. Não despeje tudo de uma vez.
   1. Qual é a marca ou o negócio? (nome + o que vende/entrega)
   2. Quem é o público que você atende?
   3. Como a marca fala? (o tom — ex.: próximo e bem-humorado, técnico e sóbrio, premium…)
   4. Em quais canais você trabalha? (Instagram, YouTube, e-mail, anúncios, LP…)
   5. Tem concorrentes ou referências que você admira (ou quer se diferenciar)?
   6. Tem algo que NUNCA pode aparecer na comunicação da marca? (palavras, promessas, temas)

3. **Grave as respostas** em `.estopim/config.md` na pasta onde a pessoa está trabalhando.
   - Primeiro rode: `python3 scripts/estopim.py init` (cria a pasta `.estopim/` e o `config.md`
     modelo, e adiciona `.estopim/` ao `.gitignore`).
   - Depois **substitua cada `[PREENCHER]`** do `config.md` pela resposta real.
   - Se a pessoa não souber ou não quiser responder algo, deixe `[PREENCHER]` — **nunca invente**.

4. **Autodestrua o setup.** Depois de gravar o `config.md`, apague a pasta `setup/` inteira desta
   skill, para o Estopim ficar limpo:
   ```bash
   rm -rf setup
   ```
   (Rode a partir da pasta da skill Estopim. Se rodar de outro lugar, apague o caminho completo
   `.../Estopim/setup`.)

5. **Confirme e siga.** Diga que está tudo pronto e siga direto para o que a pessoa pediu (ou
   pergunte qual campanha ela quer criar). A partir daqui a pasta `setup/` não existe mais e o
   Estopim vai direto ao trabalho, lendo `.estopim/config.md` quando precisar do contexto da marca.

## Importante
- Isto roda **uma única vez por instalação**. Se a pasta `setup/` não existir, a configuração já
  foi feita — nunca refaça.
- O `.estopim/config.md` fica **na máquina do membro** e é git-ignored. Nada é enviado para lugar
  nenhum.
