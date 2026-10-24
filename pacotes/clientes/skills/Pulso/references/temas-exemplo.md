# Dicionário de temas da voz do cliente (modelo)

O Pulso agrupa os comentários abertos em **temas** para você ver, de relance, o
que os clientes mais tocam. Sem este arquivo, ele usa um conjunto genérico que já
funciona para a maioria dos negócios de serviço.

Se o seu ramo tem vocabulário próprio, copie este modelo para `.pulso/temas.md`
e ajuste. Uma linha por tema, no formato `Nome do tema: palavra1, palavra2, ...`.
A busca ignora acentos e maiúsculas, então escreva as palavras como preferir.

```
# .pulso/temas.md — dicionário de temas do seu negócio
Atendimento: atendimento, atenção, educação, simpatia, grosseria, atendente, recepção
Prazo/Entrega: prazo, demora, atraso, rápido, lento, entrega, espera, fila
Preço: preço, caro, barato, valor, custo, cobrança, reajuste, mensalidade
Qualidade: qualidade, ruim, ótimo, excelente, defeito, acabamento, capricho
Produto/Recurso: recurso, funcionalidade, faltou, sentindo falta, opção
Suporte/Técnico: suporte, bug, erro, travou, não funciona, sistema, app, site
Comunicação: comunicação, informação, retorno, resposta, não respondeu, contato
Experiência/Facilidade: fácil, difícil, complicado, confuso, intuitivo, burocracia
```

## Como adaptar para o seu ramo (exemplos)

- **Clínica/consultório:** troque "Produto/Recurso" por `Estrutura: sala, espera, limpeza, conforto` e adicione `Resultado: melhora, dor, tratamento, resultado`.
- **Restaurante/delivery:** `Comida: sabor, temperatura, porção, fresco` · `Entrega: motoboy, atraso, embalagem`.
- **Agência/serviço digital:** `Resultado: resultado, ROI, leads, vendas` · `Relacionamento: reunião, alinhamento, proatividade`.
- **SaaS/app:** `Onboarding: configurar, começar, aprender` · `Estabilidade: bug, caiu, lento, travou`.

> Dica: comece com os temas genéricos, leia os comentários que "não se encaixaram
> em nenhum tema" e crie novos temas a partir das palavras que se repetem lá.
