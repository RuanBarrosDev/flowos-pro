# Levantamento de oportunidades (casos de uso)

Depois do diagnóstico, ajude o cliente a listar **onde a IA pode entrar**. Vá área por área, com perguntas concretas. Para cada oportunidade capture 4 notas (1 a 5) e registre:

`python3 scripts/sextante.py caso "<cliente>" "<título>" --area "<área>" --alcance N --frequencia N --dor N --esforco N --obs "<detalhe>"`

- **alcance** (1-5): quantas pessoas/clientes a tarefa toca.
- **frequencia** (1-5): quão recorrente é (1 = raro, 5 = todo dia).
- **dor** (1-5): quanto atrapalha/custa hoje.
- **esforco** (1-5): quão difícil de implantar (1 = fácil, 5 = complexo).

O motor calcula `impacto = alcance × frequencia × dor` e prioriza por `impacto / esforço`, classificando em quadrantes:
**Ganho Rápido**, **Projeto**, **Talvez**, **Evite por ora**.

> Regra de ouro: **nunca invente o dado do cliente**. Se ele não souber estimar, pergunte ou marque `[SUPOR — validar]` na observação. Nunca automatize um processo quebrado ou sem base de dados — conserte a base primeiro.

## Gatilhos por área (para provocar a conversa)
- **Atendimento/Vendas:** responder dúvidas repetidas, montar orçamento, follow-up, triagem de leads, resumo de conversa.
- **Marketing/Conteúdo:** rascunho de post, roteiro, e-mail, legenda, reaproveitar conteúdo.
- **Operação/Entrega:** checklist, relatório padrão, resumo de reunião, transcrição, laudo/documento modelo.
- **Financeiro/Administrativo:** conferência de nota, cobrança, categorização de despesa, resumo de extrato.
- **Gestão/Decisão:** painel simples, priorização, análise de dado que já existe, previsão grosseira.
- **RH/Interno:** triagem de currículo, treinamento, base de perguntas frequentes do time.

## Biblioteca de casos comuns em PMEs de serviço
Use como repertório para sugerir — sempre validando se faz sentido para ESTE cliente:
1. Atendente que responde as 20 perguntas mais frequentes no WhatsApp.
2. Gerador de orçamento a partir de uma descrição em texto.
3. Resumo automático de reuniões/áudios em ata com próximos passos.
4. Redação de propostas/contratos a partir de um modelo.
5. Classificação e resumo de e-mails/mensagens que chegam.
6. Rascunho de conteúdo (posts, e-mails) no tom da marca.
7. Conferência de documentos contra um checklist.
8. Painel de indicadores a partir de uma planilha que já existe.
