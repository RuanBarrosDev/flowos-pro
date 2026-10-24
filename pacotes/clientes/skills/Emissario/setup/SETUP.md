# Setup de primeira execução do Emissário

> Você (a IA) está lendo isto porque **não existe `.emissario/config.md` na raiz do projeto**. Conduza este
> setup UMA vez, em conversa PT-BR, e depois se autodestrua. Se `.emissario/config.md` já existir, NÃO rode o
> setup — vá direto para os modos do SKILL.md.

## O que fazer

### 1. Converse (curto, amigável, sem jargão)
Explique em uma frase o que vamos fazer ("vamos projetar o seu assistente de IA de atendimento — eu monto o
'cérebro' dele e te entrego o texto pronto pra colar no WhatsApp, num GPT ou no site"). Depois pergunte, uma de
cada vez (aceite respostas curtas; nada é obrigatório além do nome):

1. **Como você quer ser chamado?** (ex.: Marina)
2. **Qual o nome do seu negócio?** (ex.: Clínica Vida, Ótica Sol)
3. **Que nome você quer dar ao assistente?** (ex.: Bia, Léo) — se não souber, sugira um e siga.
4. **Quem ele vai atender?** (ex.: pacientes novos, clientes da loja, quem pede orçamento)
5. **Em uma frase, qual o trabalho dele?** (a missão — ex.: "tirar dúvidas e agendar avaliação")
6. **Onde ele vai rodar?** (WhatsApp, um GPT, Projeto do Claude, site — pode ser mais de um)
7. **Que tom combina com o negócio?** (ex.: próximo e leve / formal e técnico / descontraído)
8. **Quando o assistente não der conta, quem assume?** (nome/telefone/canal de quem recebe o cliente)

Não invente respostas. Se o dono não sabe, registre "a definir".

### 2. Grave a config
Crie o arquivo **`.emissario/config.md`** na **raiz do projeto** (não dentro da skill) com este formato exato
(mantenha os `**` e os acentos):

```markdown
# Config do Emissário

- **Nome:** [nome do dono]
- **Negócio:** [nome do negócio]
- **Assistente:** [nome do assistente]
- **Atende:** [quem ele atende]
- **Missão:** [o trabalho dele em uma frase]
- **Canal:** [WhatsApp / GPT / Projeto do Claude / site]
- **Tom:** [tom de voz]
- **Idioma:** português do Brasil
- **Contato humano:** [quem assume ao escalar]
- **Criado em:** [data de hoje YYYY-MM-DD]
```

### 3. Garanta o `.gitignore`
A pasta `.emissario/` guarda a base, os fluxos e o assistente do dono — **não deve ir pro Git**. Cheque se a raiz
do projeto tem um `.gitignore` com a linha `.emissario/`; se não tiver, acrescente:
```
.emissario/
```
(Se o projeto não usa Git, ignore este passo.)

### 4. Confirme e mostre o caminho
Diga algo como:
> "Pronto, [Nome]! Vamos montar o **[Assistente]**, o assistente de atendimento da **[Negócio]**. O jeito mais
> forte é irmos por partes: primeiro o **jeito de falar** dele (Persona), depois a **base** do que ele pode
> responder (Conhecimento — a parte que mais importa), os **caminhos de conversa** (Conversa), as **travas** de
> segurança (Travas & Escalar), e aí eu **monto o system prompt** e a gente **testa** antes de publicar. Quer
> começar pela persona ou já ir montando a base de conhecimento?"

Liste os 6 modos em uma linha cada (Definir, Persona, Conhecimento, Conversa, Travas & Escalar, Montar & Testar).

### 5. AUTODESTRUA o setup
Depois de gravar `.emissario/config.md`, **apague a pasta `setup/` inteira** da skill para o Emissário ficar limpo:
```
rm -rf setup
```
(Rode isso a partir da pasta da skill `Emissário/`. Se tiver dúvida do caminho, apague a subpasta `setup/` que
fica ao lado de `SKILL.md`.)

Feito isso, o setup nunca mais roda — nas próximas vezes o Emissário vê o `.emissario/config.md` e vai direto ao
trabalho.
