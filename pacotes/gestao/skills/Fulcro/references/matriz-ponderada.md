# Ponderar — a matriz de decisão ponderada

Quando há várias opções e vários fatores a pesar, a cabeça não dá conta de comparar tudo de uma
vez — ela pesa o último argumento mais alto e esquece os outros. A **matriz ponderada** resolve
isso: separa "o que importa" (critérios com peso) de "quão bem cada opção atende" (notas), e
deixa a conta ser conta. Ela combate a **paralisia de análise** — o script faz o cálculo, o dono
faz o julgamento.

## Passo 1 — os critérios que importam DE VERDADE

Liste com o dono os fatores que pesam na decisão. Poucos e reais valem mais que muitos e
genéricos — de 3 a 6 costuma bastar. Exemplos conforme o tipo de decisão:

- **Custo total** (não só o preço: instalação, migração, tempo perdido).
- **Tempo até dar resultado.**
- **Risco / chance de dar errado.**
- **Alinhamento com o que o dono realmente quer** (o critério mais esquecido e um dos mais
  importantes — uma opção "ótima no papel" que ele detesta tocar vai falhar na execução).
- **Esforço / carga sobre o dono.**
- **Potencial de crescimento.**
- **Reversibilidade** (dá para voltar atrás?).

## Passo 2 — o peso de cada critério (1 a 5)

Cada critério recebe um **peso de 1 (pouco importa) a 5 (decisivo)**, segundo a prioridade **do
dono**, não a sua. Aqui mora a alma da decisão: os pesos são os **valores** do dono virando
número. Se dois critérios têm o mesmo peso 5, tudo bem — mas force a distinção quando possível
("entre custo e tempo, qual dói mais errar?").

## Passo 3 — a nota de cada opção em cada critério (1 a 5)

Para cada opção, dê uma **nota de 1 (atende mal) a 5 (atende muito bem)** em cada critério. Peça
uma justificativa curta e concreta para a nota não ser chute ("por que Custo = 3 e não 5?"). Se
o dono não sabe a nota, esse é um sinal de que falta informação — talvez a melhor "opção" seja ir
buscar esse dado antes de decidir.

## Passo 4 — rode a conta (nunca some de cabeça)

Escreva o JSON em `.fulcro/matriz.json` e rode:

```bash
python3 scripts/fulcro.py matriz --arquivo .fulcro/matriz.json
```

Formato:
```json
{
  "titulo": "Trocar de sistema de gestão?",
  "criterios": [
    {"nome": "Custo total", "peso": 5},
    {"nome": "Facilidade de migrar", "peso": 3},
    {"nome": "Suporte", "peso": 4}
  ],
  "opcoes": [
    {"nome": "Ficar no atual", "notas": [4, 5, 2]},
    {"nome": "Sistema B",       "notas": [3, 2, 5]}
  ]
}
```
A ordem de `notas` segue a ordem de `criterios`. O script devolve:

- **o ranking** (nota 0-100 = quão bem a opção atende ao conjunto de prioridades);
- **a margem** entre 1º e 2º — margem menor que 5 pontos é **empate técnico**: a matriz **não
  está decidindo**, o desempate vem do pré-mortem e do instinto;
- **o teste de sensibilidade**: se, ao ignorar um único critério, o vencedor muda, o vencedor é
  **frágil** — ele depende demais daquele critério. Confira se o peso dele é mesmo tão alto, ou
  se você o inflou sem querer.

## A regra de ouro do Ponderar

**A matriz informa; ela não decide.** Ela é um espelho dos pesos e notas que o dono deu — se a
entrada muda, a saída muda. Dois usos honestos do resultado:

1. **Quando o vencedor bate com o instinto:** ótimo, a conta confirmou e você decide com mais
   confiança.
2. **Quando o vencedor dá um nó no estômago:** isso é **dado, não erro**. Quase sempre significa
   que falta um critério na conta (algo que o dono valoriza e não colocou) ou que um peso está
   errado. Volte, ache o critério que faltava, e rode de novo. O desconforto é a intuição
   avisando de uma variável esquecida — respeite-o.

Nunca mande ninguém "obedecer o número". O número é um conselheiro muito bom e um chefe péssimo.
