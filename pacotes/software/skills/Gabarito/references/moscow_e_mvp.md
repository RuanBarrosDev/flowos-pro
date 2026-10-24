# MoSCoW e MVP: o que entra na primeira versão

Você não vai construir tudo de uma vez — e não deve. A priorização MoSCoW separa o
que é vital do que é enfeite, e desenha o MVP (a primeira versão útil).

## As quatro faixas
- **Obrigatório (Must)** — sem isto, a solução não resolve o problema. É o MVP.
- **Importante (Should)** — dói ficar sem, mas dá para lançar sem por ora.
- **Desejável (Could)** — seria bom; entra se sobrar tempo.
- **Fora por ora (Won't)** — combinado que NÃO entra agora (não é "nunca", é "não
  nesta rodada"). Registrar isto é o que protege o escopo.

Regra prática saudável: os **Obrigatórios** devem ser a minoria. Se quase tudo é
"obrigatório", nada é — puxe o dono a escolher o que de fato não pode faltar no
dia 1.

## O MVP é o conjunto dos Obrigatórios
```bash
python3 scripts/gabarito.py prioridade --id RF.01 --nivel obrigatorio
python3 scripts/gabarito.py moscow
```
O `moscow` mostra as quatro faixas, aponta o MVP e avisa se algum obrigatório está
**sem critério de aceite** (não dá para construir o essencial no escuro).

## A trava de dependência
Um Obrigatório **não pode depender** de um Desejável. Se ele depende, ou o item do
qual ele depende também é Obrigatório, ou o seu "obrigatório" não é tão obrigatório
assim. O motor detecta e avisa:

> RNF.01 (Obrigatório) depende de RF.02 (Importante) — o mais importante não pode
> depender do menos importante.

Como registrar uma dependência:
```bash
python3 scripts/gabarito.py requisito-add --necessidade CN.01 --enunciado "..." --depende RF.01
```

Corrija subindo a prioridade do item do qual você depende, ou repensando se o
requisito é mesmo obrigatório. Uma dependência invertida vira bloqueio no meio da
obra.
