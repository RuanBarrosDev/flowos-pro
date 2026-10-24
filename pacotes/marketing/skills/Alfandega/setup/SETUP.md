# Primeira conversa da Alfândega (setup — só uma vez)

Faça estas perguntas em PT-BR, uma de cada vez, tom leve. Não peça nada técnico.

1. **Como se chama o seu negócio?**
2. **O que você costuma comprar/importar para revender?** (ex.: eletrônicos, roupas, peças, decoração)
3. **De onde costuma comprar?** (ex.: China/Alibaba, EUA, ou fornecedor nacional)
4. **Em que estado a sua empresa fica?** (para estimar o ICMS — cada estado tem uma alíquota)
5. **Qual moeda você mais usa nas compras de fora?** (ex.: USD, EUR — deixe BRL se for compra nacional)

Depois, grave em `.alfandega/config.md` exatamente neste formato:

```markdown
# Config Alfândega
- negocio: <nome>
- compra: <o que importa/compra>
- origem: <países/fornecedores habituais>
- estado: <UF, para o ICMS>
- moeda: <USD/EUR/BRL>
```

Em seguida:
1. Garanta que `.alfandega/` está no `.gitignore` (crie o arquivo se não existir e adicione a linha `.alfandega/`). Preço, custo e fornecedor são privados.
2. Rode `python3 <pasta-desta-skill>/scripts/alfandega.py init` para criar os arquivos de dados vazios.
3. **Apague a pasta `setup/`** desta skill — ela só serve para o primeiro uso.
4. Confirme ao dono, em uma frase simples, que a Alfândega está pronta e explique que agora é só falar
   com ela ("quero importar X", "esse fornecedor é confiável?", "quanto vou pagar de imposto?").
