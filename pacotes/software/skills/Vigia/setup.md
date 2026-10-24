# Primeira conversa da Vigia (roda só uma vez)

Este arquivo existe só na **primeira vez**. Ao terminar, ele se apaga sozinho e
a Vigia fica limpa e pronta para o dia a dia.

## O que fazer (Claude, siga na ordem)

1. **Diga oi e explique em 2 linhas** o que a Vigia faz: ela é o plantão do
   sistema do dono depois que ele já está no ar — avisa antes do cliente, ajuda
   quando algo quebra, e fecha o assunto para não repetir.

2. **Monte o Cartão de Saúde** perguntando ao dono, em linguagem simples (uma de
   cada vez ou em bloco; se estiver num modo automático/sem interação, use as
   respostas que já vieram na conversa e siga sem travar):
   - **Qual é o sistema?** (nome + o que é em uma frase — ex.: "loja online de
     ferramentas", "bot de atendimento no WhatsApp", "site de agendamento").
   - **Qual o endereço principal que precisa responder?** (a URL do site/app; se
     for um bot/automação sem URL, anote onde ele "vive" e como se percebe que
     está funcionando).
   - **O que é "normal"?** (ex.: "abre em menos de 3 segundos"; "o bot responde
     em até 1 minuto").
   - **Onde aparecem os erros hoje?** (um painel da hospedagem? um arquivo de
     log? o histórico do bot? "não sei" é uma resposta válida — a Vigia ajuda a
     descobrir depois).
   - **Quem precisa ser avisado quando algo cai?** (você? um sócio? por qual
     canal — WhatsApp, e-mail?).

3. **Grave o Cartão de Saúde.** Rode `python3 scripts/vigia.py init` para criar o
   esqueleto (a pasta `vigia/` nasce na **raiz do projeto do dono**, nunca dentro
   da pasta da skill — o script cuida disso sozinho), depois preencha
   `vigia/config.json` com as respostas (campos:
   `nome_sistema`, `o_que_e`, `url_principal`, `urls_extras`,
   `normal_responde_em_segundos`, `onde_ficam_os_erros`, `quem_avisar`) e escreva
   um `vigia/cartao-de-saude.md` legível com o mesmo conteúdo em prosa.

4. **Ligue o primeiro sensor de verdade.** Se houver uma `url_principal`, rode
   `python3 scripts/vigia.py check` e mostre o resultado (no ar? em quanto tempo?).
   Se não responder, já entre em modo Plantão. Em seguida, ofereça ensinar a
   plugar um monitor externo grátis para vigilância contínua.

5. **Autodestrua o setup.** Quando o Cartão estiver gravado, **apague este
   arquivo**: `rm -f setup.md`. Confirme ao dono que a Vigia está pronta e
   explique as 3 frases que ele pode usar a partir de agora:
   - "dá uma checada no meu site" (Sensores/checagem)
   - "meu site caiu / está lento / deu erro" (Plantão)
   - "vamos fazer a autópsia do que aconteceu" (Autópsia)

## Regra importante
Não invente dados do dono. Se ele não souber um campo, deixe em branco no config
e registre no Cartão que está "a definir" — nunca preencha com chute.
