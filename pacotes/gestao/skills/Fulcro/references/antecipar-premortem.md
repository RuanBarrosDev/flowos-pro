# Antecipar — o pré-mortem

O pré-mortem é o contrário do post-mortem. Em vez de descobrir o que deu errado **depois** que
falhou, você imagina que **já falhou** e descobre por quê **antes** de começar. É a técnica de
decisão mais valorizada por quem estuda o assunto — porque muda o que o cérebro consegue enxergar.

## Por que funciona: a moldura da bola de cristal

Quando você pergunta "o que pode dar errado?", a pessoa (e o modelo de IA) dá respostas cautelosas,
hipotéticas e mornas. Quando você diz **"isso já deu errado — me conte como"**, o cérebro entra
em modo narrativa e gera motivos muito mais específicos, criativos e honestos. Pesquisadores
chamam isso de *retrospectiva prospectiva*, e ela aumenta bastante a capacidade de identificar as
causas reais de um fracasso futuro.

Isso importa ainda mais com IA: o modelo tende a concordar e a ser otimista. Se você pergunta "é
um bom plano?", ele acha razões para dizer sim. O pré-mortem quebra esse padrão: o plano está
morto, resta explicar a autópsia.

**A frase certa** (use o passado, sem "talvez"):
> "É [horizonte] no futuro. Essa escolha deu errado — não 'pode dar', deu, é fato. O que aconteceu?"

Escolha o **horizonte** onde "com certeza saberíamos se falhou": contratação → 12 meses; troca de
sistema → 3-6 meses; parceria → 12 meses; campanha curta → 4-8 semanas. Nem tão curto que só pegue
problema de largada, nem tão longo que vire ficção científica.

## Cubra os dois lados: externo e interno

Uma lista só de um lado está cega para metade do risco. Puxe dos dois:

- **Externas:** o mercado mudou, o cliente-âncora saiu, um concorrente cortou preço, o fornecedor
  falhou, a regra mudou, o timing estava errado.
- **Internas:** a execução travou, o prazo estourou, faltou fôlego/dinheiro no meio, a pessoa-chave
  adoeceu ou se distraiu, o escopo inchou, faltou habilidade.

## Equilibre o exótico com o chato

A armadilha clássica do pré-mortem é listar só falhas dramáticas (disrupção, ataque do concorrente)
e esquecer as **chatas e comuns** — que são as que mais matam plano:

- o prazo escorregou 40% por coisas que ninguém orçou;
- a pessoa-chave saiu, adoeceu ou virou a atenção para outra prioridade;
- ficou pronto mas ninguém percebeu porque a divulgação foi um detalhe de última hora;
- a motivação morreu entre o mês 2 e o mês 4;
- um imprevisto pessoal comeu o tempo do dono.

Force pelo menos **duas falhas mundanas** na lista. A taxa-base importa mais que o enredo.

## Pontue por Probabilidade × Impacto

Para cada falha, o dono estima:

- **Probabilidade (1-5):** 1 raro (<5%), 2 pouco provável, 3 possível, 4 provável, 5 quase certo.
  Regra prática: se pensou "pode acontecer", é no mínimo 3; se "acontece com certeza", é 5.
- **Impacto (1-5):** 1 leve (ninguém reclama) … 5 catastrófico (mata o negócio, perda
  irreparável, consequência jurídica).

Rode:
```bash
python3 scripts/fulcro.py risco --arquivo .fulcro/risco.json
```
Formato:
```json
{
  "titulo": "Contratar 1º funcionário",
  "falhas": [
    {"descricao": "Fluxo de caixa não aguenta a folha", "prob": 4, "impacto": 5,
     "tipo": "interno", "prevenir": "reserva de 3 folhas antes", "limitar": "contrato de experiência"},
    {"descricao": "Cliente-âncora cancela", "prob": 2, "impacto": 5,
     "tipo": "externo", "detectar": "conversa mensal de satisfação"}
  ]
}
```
O script ordena por P×I (do mais perigoso ao menos), marca **CRÍTICO/ALTO/MÉDIO/BAIXO** e confere
se você cobriu externo e interno.

> **Cuidado:** P×I é **ordem de prioridade**, não probabilidade exata. Serve para saber onde olhar
> primeiro — nunca para fingir uma precisão que ninguém tem. Não vire refém do número.

## Para cada risco grande, um plano — o tripé da mitigação

Falha CRÍTICA ou ALTA sem ação é só susto. Para cada uma, escolha ao menos um:

- **Prevenir:** reduzir a chance de acontecer ("reserva de 3 folhas antes de contratar").
- **Detectar:** montar o alarme que avisa cedo ("conversa mensal de satisfação com o cliente-âncora").
- **Limitar o estrago:** ter o plano B se acontecer ("contrato de experiência", "cláusula de saída").

## O contrapé: e se NÃO fizer?

Se a recomendação começar a pender para "melhor não fazer / adiar", rode um mini pré-mortem ao
contrário: *"Passou o horizonte. Você NÃO fez — e foi um erro. Por quê?"* Três motivos fortes. Isso
protege contra o viés de que "não agir é seguro" — muitas vezes a inação é o risco maior.

## Fecho do Antecipar

Ao final você tem a lista de falhas ordenada por P×I, com externo e interno cobertos, e um plano de
prevenir/detectar/limitar para cada risco grande — mais o contrapé da inação. Agora dá para ganhar
distância e decidir.
