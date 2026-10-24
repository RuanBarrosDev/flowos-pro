# O documento de especificação (o gabarito da obra)

Rodar `especificacao` monta o documento completo em `.gabarito/especificacao-N.md`
e roda o portão "pronto para construir?". Este é o entregável — o que o dono revisa,
ajusta e aprova, ou manda ao cliente para aceite, ou entrega ao desenvolvedor / ao
Claude Code para construir.

## O que o documento traz
1. **Resumo** — para quem, problema central, domínio.
2. **Problemas e necessidades** — a cadeia CP → CN.
3. **Requisitos** — funcionais e não-funcionais, cada um com enunciado, porquê,
   critério de aceite, como validar e a qual problema traça.
4. **Prioridade (MoSCoW) e MVP** — o que entra na primeira versão.
5. **Fronteira de escopo** — fora do escopo, dependências, bloqueios, restrições.
6. **Suposições, riscos e perguntas em aberto** — separados.
7. **Critérios de sucesso** — como saberemos que valeu a pena (do que o dono disse
   na dimensão "sucesso").
8. **Aceite** — um bloco para o dono/cliente marcar que concorda.

## O portão "pronto para construir?"
Nove verificações, com semáforo 🟢/🟡/🔴:
1. Problema central definido?
2. Há cadeia problema→necessidade→requisito completa?
3. Todo requisito tem critério de aceite?
4. Nenhum requisito nebuloso (adjetivo vago sem critério)?
5. Nenhum requisito órfão (sem problema por trás)?
6. Dependências coerentes (obrigatório não depende de opcional)?
7. Escopo tem fronteira (algo declarado fora)?
8. MVP definido (há obrigatórios)?
9. Perguntas em aberto resolvidas?

Se tudo estiver 🟢, a especificação está sólida — próximo passo é o **Prumo**
(planejar o build) ou o desenvolvedor. Se houver 🔴/🟡, rode `plano` para a ordem
de ataque: o motor lista o que fechar, vermelhos primeiro. **Construir com furo
declarado é retrabalho garantido** — feche antes.

## Lembrete
O documento é um **rascunho honesto**: onde faltou informação, aparece [A CONFERIR].
Isso não é defeito — é o mapa do que o dono ainda precisa decidir. Preencher com
invenção para "parecer completo" é o único jeito de errar aqui.
