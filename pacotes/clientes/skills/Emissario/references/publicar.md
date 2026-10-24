# Publicar — onde colar o system prompt do seu assistente

Depois que o `prontidao` deu 🟢 e você validou as 10 perguntas do `teste`, é hora de subir. O arquivo que você
publica é sempre o mesmo: **`.emissario/build/system-prompt.txt`**. Você **cola** o conteúdo dele no campo de
instruções da plataforma que escolher. Escolha por onde seus clientes falam com você.

> Antes de qualquer plataforma: abra o `system-prompt.txt`, leia de cima a baixo e confira que não sobrou
> nenhum `[PREENCHER]`. Se sobrou, volte ao modo correspondente, rode `montar` de novo e revalide.

## 1. GPT personalizado (ChatGPT) — o mais rápido para testar
1. No ChatGPT, vá em **Explorar GPTs → Criar** (precisa de uma conta paga para publicar).
2. Na aba **Configurar**, cole o `system-prompt.txt` inteiro no campo **Instruções**.
3. Dê o nome do assistente e uma descrição curta. Se tiver documentos da base, anexe em **Conhecimento**.
4. Salve como **Apenas com link** (ou público) e teste pelo próprio painel antes de compartilhar o link.

## 2. Projeto do Claude (claude.ai) — ótimo para uso interno e testes
1. Em claude.ai, crie um **Projeto**.
2. Cole o `system-prompt.txt` no campo de **instruções do projeto**.
3. Anexe os arquivos da base (se houver) ao Projeto.
4. Converse no Projeto para testar. Bom para você e sua equipe usarem; para o cliente final, prefira WhatsApp/site.

## 3. WhatsApp (ManyChat, Typebot e similares) — onde a maioria dos clientes está
O WhatsApp não roda IA sozinho — você usa uma plataforma de chatbot que conecta ao seu número e tem um bloco de
IA. O passo comum a todas:
1. Conecte seu WhatsApp Business à plataforma ([ManyChat](https://manychat.partnerlinks.io/9tevnjmn2uy4-u934l7), Typebot, SleekFlow, etc. — siga o guia dela).
2. Adicione um **bloco/etapa de IA** (nomes variam: "AI Step", "Bloco de IA", "Assistente").
3. Cole o `system-prompt.txt` no campo de **instruções/prompt do sistema** desse bloco.
4. Configure o **encaminhamento para humano** da plataforma (transferir para um atendente) e ligue-o aos
   gatilhos de escalonamento que você definiu.
5. Teste com o seu próprio número antes de abrir para os clientes.
> Dica: comece com o assistente respondendo só fora do horário ou só uma dúvida específica, e vá ampliando.

## 4. Chat no site (widget) — para quem recebe visita no site
1. Escolha um widget de chat com IA (Chatbase, Typebot embed, Tidio com IA, etc.).
2. Cole o `system-prompt.txt` nas **instruções** do bot e anexe a base como fonte de conhecimento.
3. Ative a opção de **falar com humano** e ligue aos seus gatilhos.
4. Copie o trechinho de código (script) que a ferramenta gera e peça para colocarem no seu site (ou use o
   plugin do WordPress/Wix da própria ferramenta). Teste no site publicado.

## Depois de publicar
- **Reteste ao vivo** as perguntas #5 (alucinação) e #7 (override) na plataforma real — cada plataforma responde
  um pouco diferente.
- **Acompanhe as primeiras conversas.** Toda vez que o assistente tiver que escalar por falta de informação,
  isso é uma **lacuna da base**: adicione a resposta no `base.md`, rode `montar` e atualize o prompt na plataforma.
- A base cresce com o uso. Um assistente que escala com honestidade hoje vira um que resolve sozinho amanhã.
