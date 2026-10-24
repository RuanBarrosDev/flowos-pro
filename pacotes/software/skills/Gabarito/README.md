# Gabarito — a especificação antes da obra

**Transforma um pedido vago — "quero um sistema/app/site/automação que faça X"
(seu ou de um cliente) — numa especificação escrita, priorizada e com critério de
aceite, ANTES de construir.** Assim você (ou seu desenvolvedor, ou o Claude Code)
constrói a coisa certa e não joga tempo fora refazendo.

O nome vem da marcenaria: o **gabarito** é o molde-mestre que você faz antes de
cortar a peça. A especificação é o gabarito do software.

## O que ele faz
- **Entrevista você** em português simples (a IA lidera, você decide) e traduz todo
  termo técnico para o dia a dia.
- Liga cada funcionalidade a um problema real: **Problema → Necessidade → Requisito**.
  O que não resolve nada ele marca como **órfão** (candidato a cortar).
- Exige **critério de aceite testável** em cada requisito — nada de "rápido" e
  "fácil" soltos.
- Prioriza com **MoSCoW** (Obrigatório/Importante/Desejável/Fora), desenha o **MVP**
  e confere dependências.
- Protege a **fronteira de escopo** — o que fica de fora, o que é suposição, risco,
  restrição e pergunta em aberto, sem misturar.
- Gera o **documento de especificação** pronto para o dono aprovar ou o dev construir.

Nunca inventa: o que você não souber vira **[A CONFERIR]**. Tudo fica **local** na
sua máquina (nada vai para a internet).

## Como instalar
1. Baixe e descompacte o arquivo.
2. Copie a pasta `Gabarito/` para dentro de `.claude/skills/` do seu projeto (ou de
   `~/.claude/skills/` para usar em qualquer projeto):
   ```
   .claude/skills/Gabarito/
   ```
3. Abra o Claude Code nesse projeto. Pronto — a skill é reconhecida sozinha.

## Como usar
Fale naturalmente. Exemplos que disparam a skill:
- "Quero criar um sistema de agendamento para minha clínica, me ajuda a especificar."
- "Meu cliente pediu um app, mas não sei direito o que ele precisa."
- "Preciso montar o escopo/documento de requisitos desse projeto."

Na primeira vez, a skill faz uma instalação rápida (pergunta seu nome e o tom da
escrita) e some com os arquivos de setup. Depois é só conversar: ela entrevista,
organiza os requisitos, prioriza e monta a especificação.

Você nunca precisa digitar comando nenhum — a IA cuida disso nos bastidores. Você
só conversa.

## O que esperar (regras de ouro)
- **Ela pergunta, você decide.** A IA conduz, mas quem sabe do negócio é você.
- **Nunca inventa.** Sem dado, fica [A CONFERIR] — nunca um chute.
- **Começa pelo problema**, não pela lista de telas.
- **Todo requisito tem critério de aceite** — dá para conferir se ficou pronto.
- **Protege o escopo** — o "isto NÃO faz parte" dito hoje economiza semanas amanhã.
- **Seus dados são seus.** Tudo local, nada na nuvem (LGPD).

## Requisitos técnicos
Apenas **Python 3** (já vem no macOS e na maioria dos Linux). Sem instalação de
pacotes, sem conta, sem internet.

## Onde ficam seus dados
Tudo em `.gabarito/` na raiz do seu projeto (ignorado pelo Git). A especificação
final fica em `.gabarito/especificacao-1.md`, `-2.md`, etc.

---

Feito pela **Maestria Academy** para a comunidade. Licença MIT.
