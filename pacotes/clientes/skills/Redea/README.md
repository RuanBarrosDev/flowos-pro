# Rédea 🐴

**Governança e controle de qualidade do seu agente de IA.**

Você colocou (ou vai colocar) um agente de IA para falar com clientes — um chatbot no
WhatsApp, um atendente no site, um assistente no ManyChat, um GPT. A Rédea é o
**gerente + o controle de qualidade + o inspetor de segurança** desse funcionário de
IA: define as regras que ele nunca pode quebrar, testa antes de soltar na frente do
cliente, dá nota, monitora o dia a dia e diz o que fazer quando ele erra.

A Rédea **não constrói** o agente e **não depende** de onde ele mora — ela governa
qualquer agente que já exista, em qualquer plataforma.

## O que ela faz (5 modos)
1. **Regras da Casa** — a fonte-da-verdade do que o agente pode e não pode fazer.
2. **Simulado** — testa o agente com ataques (jailbreak, autoridade falsa, vazamento,
   promessa indevida…) **e** com perguntas legítimas, antes de encarar o cliente.
3. **Boletim** — dá uma nota de resiliência (0–100), caso a caso, e guarda o histórico.
4. **Ronda** — confere amostras de conversas reais para ver se ele continua na linha.
5. **Plano de Contingência** — o passo a passo de quando o agente sai da linha.

## Instalação
1. Descompacte a pasta **Rédea**.
2. Coloque-a dentro da sua pasta de skills do Claude Code
   (`.claude/skills/Rédea` no projeto, ou `~/.claude/skills/Rédea` para todos).
3. Abra o Claude Code e diga, por exemplo:
   *"Meu chatbot atende clientes no WhatsApp; quero testar se ele não fala besteira."*
   A Rédea começa pela primeira conversa (setup) e depois conduz cada modo.

## Como usar (você só conversa)
Você não precisa saber programar. A Rédea faz as perguntas, roda as ferramentas por
baixo e te explica tudo em português. Frases que a acionam:
- "Quero pôr regras no meu agente e conferir se ele obedece."
- "Faz um red-team / teste de segurança no meu bot."
- "Meu atendente de IA inventou um desconto — o que eu faço?"
- "Me dá uma nota da qualidade das respostas do meu assistente."

## Privacidade
Tudo fica em arquivos locais na pasta `.redea/` do seu projeto — regras, respostas e
boletins **não saem da sua máquina**. O motor é 100% biblioteca-padrão do Python:
sem instalar nada, sem internet.

## Licença
MIT — veja `LICENSE`.
