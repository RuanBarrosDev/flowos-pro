# Missiva — o canal de e-mail que trabalha por você

Missiva é uma skill de Claude Code que vira o seu estrategista de **e-mail marketing e
newsletter** — em português, sem você programar. Ela cuida da lista, das sequências
automáticas, da newsletter, da escrita, do pré-voo de segurança antes do disparo e do
painel de métricas. **Ela não conecta em nenhuma ferramenta e não dispara e-mail:** planeja
e organiza tudo no seu computador, e você cola o resultado no Mailchimp/Brevo/MailerLite/etc.
O botão de enviar é sempre seu.

## O que ela faz (6 modos)
1. **Base** — importa, limpa e segmenta sua lista; sinaliza quem está sem opt-in.
2. **Sequência** — desenha automações de ciclo de vida (boas-vindas, nutrição, carrinho,
   pós-compra, reengajamento, aniversário).
3. **Newsletter** — monta o calendário editorial recorrente com proporção saudável valor/oferta.
4. **Escrita** — assunto, preview, corpo e CTA que não caem no spam.
5. **Disparo** — o pré-voo de segurança: pacote de aprovação + veredito 🟢/🟡/🔴 que
   **bloqueia** envio sem consentimento, descadastro ou endereço físico.
6. **Painel** — você cola as métricas do ESP e ela diz, por campanha, o que fazer.

## Instalar
1. Baixe e descompacte o arquivo.
2. Copie a pasta `Missiva` para dentro de `.claude/skills/` do seu projeto (ou de
   `~/.claude/skills/` para deixar disponível em qualquer projeto).
3. Abra o Claude Code nesse projeto. A skill é descoberta sozinha.

Caminho final esperado:
```
.claude/skills/Missiva/
├── SKILL.md
├── scripts/missiva.py
├── references/
└── setup/
```

## Usar
Você só **conversa em português**. Exemplos que acionam a Missiva:
- "quero começar a fazer e-mail marketing"
- "monta uma sequência de boas-vindas pra minha lista"
- "importa esses leads e me diz quantos posso enviar"
- "planeja minha newsletter semanal"
- "antes de disparar, faz o pré-voo desse segmento"
- "colei as métricas da campanha — o que eu faço agora?"

Na **primeira vez**, ela faz um setup curto (nome do negócio, remetente, endereço do
rodapé, ferramenta de envio…) e guarda em `.missiva/config.md`, que fica **só no seu
computador** (adicionado ao `.gitignore` automaticamente).

## Requisitos
- Claude Code.
- Python 3 (já vem no macOS e na maioria dos Linux). **Nenhuma biblioteca extra** — só a
  biblioteca padrão. Nada é instalado, nada sai do seu computador.

## Privacidade
Seus contatos e métricas ficam em `.missiva/` na raiz do seu projeto, ignorado pelo Git.
A skill nunca envia nada para a internet e nunca dispara e-mail — quem envia é você, no seu ESP.

## Licença
MIT — veja `LICENSE`.
