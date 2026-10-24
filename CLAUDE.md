# FlowOS Pro: sistema operacional do negócio

Este arquivo é carregado automaticamente em todas as sessões. Ele conecta os agentes ao contexto do seu negócio.

Se você ainda não rodou o `/instalar`, rode agora: ele configura a memória e liga os pacotes.

---

## Memória do negócio

@_memoria/negocio.md

---

## Núcleo (sempre ligado)

| Área | Agente | Função |
|---|---|---|
| **Clientes** | Balcão | Atendimento no seu tom |
| **Clientes** | Fisga | Prospecção e primeiro contato |
| **Clientes** | Aplauso | Avaliações e reputação |
| **Clientes** | Escuta | Resumo de reunião e follow-up |
| **Financeiro** | Farol | Fechamento do mês e caixa |
| **Rotina** | Leme | Prioridades do dia |
| **Conteúdo** | Escriba | Posts e textos no seu tom |
| **Conteúdo** | Holofote | Calendário de conteúdo e autoridade |
| **Conteúdo** | Vitrine | Relatórios e apresentações |
| **Crescimento** | Alavanca | Conhecimento vira produto digital |
| **Operacional** | Orq. Documentos | Contratos e documentos |
| **Operacional** | Maestro | Coordena todos os agentes |

## Pacotes (ligue com `/pacotes`)

| Pacote | Agentes |
|---|---|
| Clientes | Cais, Amarra, Planta, Sextante, Âncora, Pulso, Aceno, Cadência, Régua, Emissário, Rédea |
| Marketing | Turbina, Estopim, Ponte, Missiva, Mostruário, Alfândega |
| Gestão | Fisco, Fulcro, Garimpo, Alambique, Tribuna, Maquete, Veredito |
| Software | Gabarito, Arcabouço, Prumo, Crivo, Rastro, Ensaio, Vigia, Novelo + agentes Estaleiro |
| YouTube | agentes Claquete |

Catálogo completo em `pacotes/README.md`. Os ligados estão em `.claude/skills/` e `.claude/agents/`.

Se o pedido do usuário pede um agente de um pacote desligado, diga qual pacote liga ele e ofereça `/pacotes` antes de seguir. Não improvise o trabalho de um agente desligado como se ele tivesse rodado.

---

## Como usar

1. Chame o agente pelo nome: `/Balcao`, `/Farol`, `/Amarra` etc.
2. Descreva o que precisa. O agente já conhece o seu negócio.
3. Delegue.

Para tarefas que cruzam várias áreas, use o Maestro: `/orquestra-maestro`.
