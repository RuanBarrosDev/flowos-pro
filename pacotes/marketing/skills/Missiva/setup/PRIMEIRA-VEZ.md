# Primeira vez com a Missiva (setup guiado)

> Esta pasta existe só para orientar a primeira conversa. Depois que o setup roda, a
> própria skill remove esta pasta (`autodestruir-setup`). Você não precisa fazer nada aqui
> manualmente — é só conversar com o Claude.

Quando a pessoa acionar a Missiva pela primeira vez, o Claude:

1. **Checa** se já existe `.missiva/config.md` na raiz do projeto. Se existir, pula o setup.
2. **Se não existir**, faz um mini-questionário acolhedor em português, **uma pergunta por vez**:
   - Nome do negócio
   - Quem assina os e-mails (nome do remetente / marca)
   - Nicho/área
   - E-mail de resposta (reply-to)
   - Endereço físico do rodapé (exigido por lei anti-spam / LGPD)
   - Ferramenta de envio atual (Mailchimp/Brevo/MailerLite/RD/… ou "ainda nenhuma")
   - Tom de voz
   - Se a ferramenta já coloca descadastro em 1 clique
3. **Grava a config**:
   ```bash
   python3 scripts/missiva.py setup \
     --negocio "..." --responsavel "..." --nicho "..." \
     --remetente "..." --reply-to "..." --endereco "..." \
     --esp "..." --tom "..." --descadastro "sim"
   ```
   Isso cria `.missiva/config.md` e garante `.missiva/` no `.gitignore`.
4. **Remove esta pasta de setup**:
   ```bash
   python3 scripts/missiva.py autodestruir-setup
   ```
5. Explica em uma frase os 6 modos e pergunta por onde a pessoa quer começar.

Se a pessoa não souber uma resposta, o Claude grava `[A PREENCHER]` e segue — **nunca inventa**.
