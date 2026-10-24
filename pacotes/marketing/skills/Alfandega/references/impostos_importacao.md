# Como cada imposto entra na conta do custo de aterrissagem

> Tudo aqui é **referência de planejamento**. As alíquotas reais dependem do **NCM** do produto e do
> **estado** (ICMS). Sempre confirme no **Simulador do Portal Único Siscomex** e com o contador antes
> de comprar. Nunca invente alíquota.

## A ordem da conta (importação formal)

1. **Valor Aduaneiro (VA) = produto (FOB) + frete internacional + seguro.**
   É o "CIF" — a base sobre a qual quase tudo é calculado. Tudo convertido para BRL pelo câmbio do dia.

2. **II — Imposto de Importação** = VA × alíquota do NCM.
   Varia muito (de 0% a ~35%). É o imposto que existe *porque* o produto veio de fora.

3. **IPI** = (VA + II) × alíquota do NCM.
   Incide sobre produtos industrializados. Muitos itens têm IPI 0%.

4. **PIS-Importação** = VA × 2,10% (alíquota geral).
5. **COFINS-Importação** = VA × 9,65% (alíquota geral).
   (Alguns produtos têm alíquotas específicas — confira o NCM.)

6. **AFRMM** = 8% sobre o **frete marítimo** internacional. Só existe em importação por navio.

7. **Taxa Siscomex** — valor fixo por Declaração de Importação (confira o valor vigente).

8. **Outras despesas** — despachante aduaneiro, armazenagem no porto, capatazia, taxa do banco no
   câmbio. Entram como `--outras` em BRL.

9. **ICMS "por dentro"** — o mais confuso, e o que mais gente erra.
   O ICMS incide sobre **tudo o que veio antes** (VA + II + IPI + PIS + COFINS + despesas aduaneiras) e
   ainda **sobre ele mesmo** ("por dentro"). A fórmula correta é:

   ```
   base = VA + II + IPI + PIS + COFINS + despesas_aduaneiras
   ICMS = base ÷ (1 − alíquota_ICMS) × alíquota_ICMS
   ```

   Exemplo: base R$ 35.290,87 e ICMS 18% → 35.290,87 ÷ 0,82 × 0,18 = **R$ 7.746,78**.
   (Se você calculasse "18% da base" simples daria R$ 6.352 — por isso o ICMS por dentro sempre sai
   maior; ignorar isso é o erro clássico que estoura a margem.)

10. **Custo total** = soma de tudo. **Custo por unidade** = custo total ÷ quantidade.

## Regime simplificado (Remessa Conforme / courier)
Para remessas de menor valor (até US$ 3.000, via correio/courier), a tributação é simplificada:
II de 60% sobre (produto + frete + seguro) + ICMS do estado. **A lei desse regime muda com frequência**
— trate como estimativa e confirme na Receita Federal / programa Remessa Conforme.

## Compra nacional
Sem imposto de importação. O custo é produto + frete + eventuais despesas. Útil para comparar "importar
vs. comprar de um distribuidor nacional" pelo custo real de cada caminho.

## O que dizer ao dono
- O preço do fornecedor lá fora é só o começo — o imposto + frete + câmbio costumam **somar de 50% a
  100%** sobre o FOB numa importação formal.
- Peça sempre o **NCM** do produto; sem ele, as alíquotas são chute.
- Guarde uma **folga de câmbio** no preço de venda (veja o modo `cambio`).
