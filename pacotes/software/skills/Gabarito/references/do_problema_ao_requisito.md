# Do problema ao requisito (a cadeia de rastreabilidade)

Toda especificação sólida se lê nos dois sentidos: para a frente, "o que vou
construir", e para trás, "por que existe". O Gabarito garante isso com uma cadeia
de três elos, cada um nomeando o pai:

```
CP.01  Problema do cliente/negócio   →  "a dor"
  └─ CN.01  Necessidade               →  "o que resolveria a dor"
       └─ RF.01 / RNF.01  Requisito   →  "o que o sistema faz para atender"
```

- **CP (Problema):** a situação ruim de hoje. Ex.: *CP.01 — pacientes faltam sem
  avisar e a agenda fica com buracos.*
- **CN (Necessidade):** o que precisa acontecer para a dor sumir, ainda sem falar de
  tela/botão. Ex.: *CN.01 — lembrar o paciente antes da consulta.*
- **RF / RNF (Requisito):** a coisa concreta que o sistema faz.
  - **RF** = requisito **funcional** (o que faz). Ex.: *RF.01 — enviar lembrete no
    WhatsApp 24h antes.*
  - **RNF** = requisito **não-funcional** (qualidade: desempenho, segurança,
    privacidade, disponibilidade). Ex.: *RNF.01 — guardar o dado do paciente
    criptografado (LGPD).*

## Por que isso importa
- **Corta o supérfluo.** Se você tem um requisito que não sobe até nenhum problema,
  o motor marca como **órfão**. Órfão é candidato a cortar — provavelmente é uma
  ideia que entrou "porque seria legal", não porque resolve algo.
- **Prioriza com clareza.** Requisito ligado a um problema grande é mais importante
  que um ligado a um problema pequeno. A cadeia dá o argumento.
- **Explica para o cliente/dev.** "Isto existe por causa de CP.01" encerra a maioria
  das discussões de escopo.

## Como cadastrar
```bash
python3 scripts/gabarito.py problema-add --titulo "..." --descricao "..."
python3 scripts/gabarito.py necessidade-add --problema CP.01 --descricao "..."
python3 scripts/gabarito.py requisito-add --necessidade CN.01 --enunciado "..." --tipo funcional
```
Um problema pode ter várias necessidades; uma necessidade, vários requisitos. Mas
**todo requisito tem que ter um pai** — senão é órfão.
