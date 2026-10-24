# Primeiro acesso do Novelo (a IA lê isto uma vez)

Esta pasta `setup/` existe só para a primeira conversa. Depois que a configuração for
gravada, o próprio motor **apaga esta pasta** — a skill instalada fica limpa.

## O que fazer na primeira vez
1. Converse com o dono em português e colete (sem tecniquês):
   - **Nome do projeto** — como ele chama isso ("meu organizador de eBooks").
   - **O que faz** — uma frase ("organiza minha biblioteca de livros digitais").
   - **Linguagem/tecnologia principal** — se ele não souber, tudo bem: "não sei".
   - **Como ele roda hoje** — o comando ou jeito de abrir; se não souber, "não sei".

2. Grave tudo com UM comando (passe as respostas por flags — não dispare perguntas
   interativas do sistema, que travam a sessão):
   ```bash
   python3 scripts/novelo.py setup \
     --projeto "Meu organizador de eBooks" \
     --o-que-e "organiza minha biblioteca de livros digitais numa planilha" \
     --linguagem "Python" \
     --rodar "python3 main.py"
   ```

3. O motor então:
   - cria `.novelo/config.md` (fica só na máquina do dono);
   - adiciona `.novelo/` ao `.gitignore` (o mapa nunca vai pro GitHub);
   - **apaga esta pasta `setup/`** sozinho.

4. Confirme ao dono que está pronto e siga para o mapa:
   > "Configurado! Agora me deixa desembolar seu projeto — vou ler os arquivos e montar
   > o mapa." → rode `python3 scripts/novelo.py mapear` e comece a preencher os propósitos
   > (veja `references/modos.md`).

## Importante
- Nunca invente dado do projeto. Se o dono não souber a linguagem, grave "não sei" — o
  motor detecta pelos arquivos depois.
- Se `.novelo/config.md` já existir, o setup já foi feito: pule direto para `mapear`.
