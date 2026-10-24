# Autópsia sem culpa — a revisão depois que passou

Depois que o sistema voltou e a poeira baixou. **Obrigatória** para incidentes
🔴 Vermelho e 🟠 Laranja. O objetivo é **aprender e não repetir** — nunca achar
culpado.

## Por que "sem culpa"?
Porque medo esconde informação. Quando as pessoas temem punição, escondem os
detalhes que a equipe precisa para consertar de verdade. A premissa é sempre:

> **Todos agiram de boa-fé, com a informação e as ferramentas que tinham naquele
> momento.**

Pessoas não "falham". São os *sistemas* que criam as condições onde a falha fica
provável. A autópsia procura essas condições e as corrige. Trocar "fulano
esqueceu de X" por "não havia nada que avisasse quando X ficava para trás" é a
diferença entre punir e melhorar.

---

## As 6 partes

### 1. Resumo de uma linha
O que quebrou, quanto tempo durou, quem sentiu. Exemplo: *"O checkout ficou fora
do ar por 42 minutos; nenhum cliente conseguiu pagar entre 14:07 e 14:49."*

### 2. Linha do tempo
Do primeiro sinal ao "voltou", com horários. Inclua quando **começou**, quando
foi **percebido** (e por quem/o quê — o cliente avisou ou um sensor?), e quando
**voltou**. A distância entre "começou" e "percebido" costuma ser a maior lição.

### 3. Por que foi possível (os "porquês" em cadeia)
Pergunte "por quê?" até chegar na raiz — sempre no sistema, nunca na pessoa:
> O checkout caiu. **Por quê?** O último deploy tinha um erro.
> **Por quê?** Passou sem ninguém perceber. **Por quê?** Não havia teste que
> pegasse esse caso. **Por quê?** Nunca montamos uma rede de testes. ← raiz

### 4. O que foi bem
O que ajudou a resolver rápido (para **manter**): reverter o deploy foi fácil,
a mensagem ao cliente já estava pronta, alguém tinha o acesso à mão.

### 5. Ações para não repetir
Poucas, reais, com dono e prazo. Uma ação sem dono e sem prazo é um desejo, não
um plano.

| Ação | Dono | Prazo |
|------|------|-------|
| ex.: montar rede de testes do checkout (Ensaio) | você | 2 semanas |

### 6. Sensor novo — fecha o loop
A pergunta que amarra tudo: **qual vigilância teria avisado antes do cliente?**
Se o cliente reclamou primeiro, faltava um sensor. Devolva isso para o
**Modo 1 · Sensores** e ligue o que faltava — assim o próximo incidente do mesmo
tipo é pego cedo, ou nem acontece.

---

## Cuidado com os anti-padrões
- **Ação genérica** ("ter mais cuidado") → sem dono, sem prazo, não vira nada.
- **Culpar pessoa** → mata a franqueza e o aprendizado.
- **Autópsia que vira lista de desejos** → escolha 1 a 3 ações que você realmente fará.
- **Não fechar o loop** → sem o sensor novo, o mesmo problema volta e te pega igual.
