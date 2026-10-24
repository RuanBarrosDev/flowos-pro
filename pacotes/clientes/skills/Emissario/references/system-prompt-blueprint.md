# Blueprint do system prompt (a estrutura que o `montar` gera)

O motor costura os blocos do dono nesta ordem — é a anatomia de um assistente que **não sai do trilho**.
Você não precisa escrever isto à mão; entenda a estrutura para saber **o que perguntar ao dono** em cada modo.

## As 7 seções do system prompt final
1. **IDENTIDADE** — quem o assistente é, o negócio, o público, a missão em uma frase, o idioma e o tom.
   (Vem do `config.md`, fechado no modo Definir + Persona.)
2. **COMO VOCÊ FALA (PERSONA)** — personalidade, saudação de abertura e jeito de falar. (Modo Persona → `persona.md`.)
3. **BASE DE CONHECIMENTO — a única fonte de verdade** — tudo que o assistente pode afirmar, + a **regra de
   ouro**: responde só do que está aqui; se não achar, não inventa e escala. (Modo Conhecimento → `base.md`.)
4. **FLUXOS DE CONVERSA** — como conduzir cada caminho. (Modo Conversa → `fluxos.md`.)
5. **O QUE VOCÊ NUNCA FAZ (TRAVAS)** — as travas do negócio + as universais que o motor injeta
   (anti-invenção, anti-override, não prometer, LGPD). (Modo Travas → `travas.md`.)
6. **QUANDO CHAMAR UM HUMANO (ESCALONAR)** — gatilhos + quem assume. (Modo Travas.)
7. **COLETA** — pedir nome/contato/necessidade com educação, um dado por vez.

## Escopo: o que trava o assistente
O par mais importante do modo Definir é **DENTRO** × **FORA** do escopo. Sem o "FORA", o assistente tenta
responder tudo — e é aí que ele inventa. Peça ao dono, explicitamente:
- **Faz:** 2 a 5 coisas concretas ("tirar dúvidas sobre os serviços", "agendar avaliação", "informar preços e horários").
- **NÃO faz:** o que deve recusar e encaminhar ("não dá diagnóstico", "não fecha contrato", "não fala de assunto
  fora do negócio", "não promete prazo de entrega").

## Princípios (por que funciona)
- **Papel específico bate genérico.** "Você é a recepcionista da Clínica X" ativa vocabulário e prioridades
  certos — muito melhor que "você é um assistente".
- **Trava nomeada bate trava vaga.** "Nunca informe preço que não esteja na base" funciona; "seja responsável" não.
- **Recusa estreita, não total.** Se só parte do pedido é fora do escopo, o assistente resolve a parte de dentro
  e encaminha só a de fora — não abandona o cliente.
- **Uma responsabilidade clara.** Um assistente com um trabalho é testável e confiável; um que faz tudo, não.
