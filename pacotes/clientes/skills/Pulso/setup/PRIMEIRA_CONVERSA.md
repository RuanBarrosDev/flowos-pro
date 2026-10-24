# Primeira conversa do Pulso (roteiro de setup)

> Este arquivo orienta APENAS a primeira execução. Depois de concluir o setup,
> apague a pasta `setup/` inteira — a skill segue funcionando só com o
> `.pulso/config.md` criado.

## Como conduzir

Converse como um analista de experiência do cliente simpático conhecendo um novo
negócio. Uma pergunta de cada vez, em português simples. Colete:

1. **Nome do negócio** e **nome do dono** (como prefere ser chamado).
2. **Ramo** (clínica, barbearia, agência, consultoria, loja, SaaS, escola...).
   O ramo ajuda a sugerir os temas certos da voz do cliente.
3. **Como colhe feedback hoje** (não colhe, WhatsApp, formulário, avaliação do
   Google, boca a boca). Isso define o próximo passo prático.
4. **Qual régua começar** — explique as três em uma frase cada e recomende uma:
   - **NPS** (0-10, "o quanto me indicaria"): melhor para a saúde geral. Comece aqui se estiver na dúvida.
   - **CSAT** (1-5, "o quanto ficou satisfeito"): melhor logo após um atendimento/entrega.
   - **CES** (1-7, "o quão fácil foi"): melhor para medir atrito num processo.
5. **Meta** (opcional): tem uma nota-alvo em mente? (ex.: "quero NPS acima de 50").

## O que criar ao final

1. **`.pulso/config.md`** com o que foi coletado:

```markdown
# Configuração do Pulso
- Negócio: <nome>
- Dono: <nome>
- Ramo: <ramo>
- Coleta hoje: <como colhe feedback>
- Régua principal: <NPS | CSAT | CES>
- Meta: <nota-alvo ou "a definir">
- Configurado em: <data de hoje>
```

2. **`.pulso/respostas.csv`** — copie `references/modelo-respostas.csv` da skill
   para `.pulso/respostas.csv` (já vem com o cabeçalho e linhas de exemplo
   comentadas no formato certo; ofereça apagar os exemplos assim que as respostas
   reais entrarem).

3. **`.pulso/temas.md`** (opcional, recomendado) — se o ramo tiver vocabulário
   próprio, crie o dicionário de temas copiando/adaptando `references/temas-exemplo.md`.
   Sem esse arquivo, o Pulso usa um conjunto de temas genérico que já funciona.

4. Se a pasta do usuário for um repositório git, adicione `.pulso/` ao `.gitignore`
   (crie o arquivo se não existir) — opinião de cliente não vai para repositório.

## Fechamento do setup

- Explique em 3 frases o que o Pulso faz: "Eu meço se seus clientes estão
  satisfeitos e te digo a nota, se ela está subindo ou caindo, quem você precisa
  recuperar e quem pode virar depoimento. Você me passa as respostas do jeito que
  tiver — formulário, print de avaliação, mensagens — e eu organizo e leio. Tudo
  fica aqui na sua máquina."
- Se ele ainda **não coleta feedback**, ofereça desenhar a primeira pesquisa
  agora (uma pergunta de nota + uma aberta, no canal certo).
- Se ele **já tem respostas**, convide: "Quer me passar as avaliações/respostas
  que você já tem para eu fazer sua primeira leitura de NPS?"
- **Apague a pasta `setup/` da skill** (`rm -rf <skill>/setup` ou exclusão
  equivalente) — o roteiro não é mais necessário.
