# Mensagens ao cliente — o que dizer quando algo quebra

Comunicar bem no meio de um problema **reduz o pânico e aumenta a confiança** —
às vezes mais do que a rapidez do conserto. A Vigia redige; **você decide se e
quando envia.**

## Princípios (valem para todas)
- **Calma, clara, honesta.** Sem jargão. Sem prometer o que não sabe.
- **Frequência vence conteúdo.** Atualize no ritmo combinado **mesmo sem novidade**
  ("seguimos trabalhando, próxima atualização às HH:MM"). O silêncio é o que
  assusta.
- **Foco no impacto, não na técnica.** O cliente quer saber "posso usar?" e
  "quando volta?", não qual servidor caiu.
- **Sempre dê a próxima hora.** "Próxima atualização até HH:MM" é a frase mais
  tranquilizadora que existe num incidente.
- **Nunca aponte culpado** nem detalhe interno que não ajuda o cliente.

---

## As 3 fases da mensagem

### Fase 1 — Investigando (nos primeiros minutos)
> ⚠️ **Estamos verificando** — identificamos que [o quê: ex. "o site/checkout"]
> pode estar [sintoma: "fora do ar" / "lento" / "com erro"] desde [hora].
> Nossa equipe já está cuidando disso. Próxima atualização até [HH:MM].

Versão curta (problema pequeno):
> Estamos verificando relatos de [sintoma] em [serviço]. Em breve, mais detalhes.

### Fase 2 — Identificado (quando você já sabe a causa)
> 🔧 **Já identificamos** o que está causando [sintoma] em [serviço]. Estamos
> aplicando a correção agora. [Se houver contorno: "Enquanto isso, você pode
> [alternativa]."] Próxima atualização até [HH:MM].

### Fase 3 — Resolvido (quando confirmou a volta)
> ✅ **Resolvido** — desde [hora], [serviço] voltou a funcionar normalmente. O
> problema durou [tempo] e aconteceu por [causa em uma frase simples]. Obrigado
> pela paciência — qualquer coisa, estamos à disposição.

---

## Aviso interno (para você / sua equipe)
Curto, para alinhar quem está ajudando:
```
[VERMELHO] checkout fora do ar
Desde: 14:07 — ~todos os clientes não conseguem pagar
Status: estabilizando (revertendo o último deploy)
Responsável: <você>
Próxima atualização: 14:30
Arquivo do plantão: vigia/plantao/incidente-....md
```

## Papéis num incidente maior (se você não estiver sozinho)
- **Quem comanda:** decide os movimentos e mantém o ritmo das atualizações.
- **Quem põe a mão:** executa o conserto.
- **Quem comunica:** cuida das mensagens ao cliente, para o resto focar no conserto.
> Sozinho? Você acumula os três — por isso a Vigia redige a comunicação por você,
> para você não ter que escolher entre consertar e avisar.

---

## Onde publicar
- Uma **página de status** (se tiver) com os estados: Operacional / Degradado /
  Parcialmente fora / Fora / Em manutenção.
- Ou o canal onde seus clientes já te encontram: WhatsApp, e-mail, o topo do
  site, a rede social. Escolha **um** canal oficial e mantenha ele atualizado.
