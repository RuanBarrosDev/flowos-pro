# Fulcro — o copiloto de decisão difícil

**O ponto de apoio onde a decisão se equilibra e vira.** O Fulcro é uma skill de Claude Code que
estrutura uma escolha importante para você decidir **melhor** — sem paralisar remoendo por semanas
e sem decidir no impulso e se arrepender. Ele não decide por você: monta o enquadramento, abre as
opções, faz a conta, antecipa o que pode dar errado e devolve a caneta. E guarda cada decisão num
diário local para você **aprender com seus próprios acertos e erros** ao longo do tempo.

Feito para donos de negócio de serviço, consultores, autônomos, gestores e profissionais — em
português, linguagem de gente, sem jargão.

## O que ele faz

O Fulcro conduz a decisão por seis frentes, **escalando o esforço ao tamanho da aposta**:

1. **Enquadrar** — qual é a decisão de verdade, o prazo, e se é *porta de mão única* (difícil de
   voltar → decida devagar) ou *porta de mão dupla* (reversível → decida rápido).
2. **Ampliar** — nunca aceitar "faço ou não faço": abrir pelo menos três opções reais e achar o
   teste barato que evita a aposta grande.
3. **Ponderar** — uma matriz de decisão ponderada (critérios com peso × nota de cada opção),
   calculada de verdade, com teste de robustez do vencedor.
4. **Antecipar** — o pré-mortem: imaginar que já deu errado e listar os motivos, ordenados por
   probabilidade × impacto, com plano de prevenir / detectar / limitar.
5. **Distanciar & Decidir** — ver a escolha por um pequeno conselho de perspectivas, o teste
   10-10-10 e a quebra dos vieses, e então a recomendação + uma ação datada + o gatilho de reversão.
6. **Diário** — registrar a decisão e, na data de revisão, anotar o que aconteceu para **calibrar
   seu julgamento** (você é otimista demais nos prazos? superdimensiona o medo?).

## Como instalar

1. Baixe e descompacte o pacote.
2. Copie a pasta `Fulcro` para dentro da pasta de skills do Claude Code:
   - no seu projeto: `.claude/skills/Fulcro/`
   - ou global: `~/.claude/skills/Fulcro/`
3. Abra o Claude Code na pasta onde você quer guardar suas decisões e comece a conversar.

## Como usar

Você só conversa — o Fulcro faz o resto por baixo. Na primeira vez ele puxa uma conversa rápida
de configuração (quem é você, o que faz, como costuma decidir) e depois é só trazer a decisão:

- *"Não sei se contrato um assistente ou continuo sozinho."*
- *"Devo aceitar esse cliente grande que vai tomar todo meu tempo?"*
- *"Vale a pena trocar de sistema de gestão?"*
- *"Estou travado nessa decisão há duas semanas."*

O Fulcro enquadra, abre as opções, monta a conta, antecipa os riscos e te ajuda a bater o martelo
— com uma ação concreta e datada no fim. Depois, na data de revisão, ele te lembra de anotar o que
aconteceu.

## Privacidade

100% local. Tudo o que você decide fica na pasta `.fulcro/` do seu computador. O Fulcro **nunca**
acessa a internet, nunca publica e nunca envia nada. Usa apenas a biblioteca padrão do Python — sem
instalar nada, sem chave de API.

## Licença

MIT. Use, modifique e compartilhe à vontade.
