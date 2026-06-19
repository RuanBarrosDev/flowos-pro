# FlowOS Pro

**O sistema operacional do seu negócio dentro do Claude Code.**

Você acaba de instalar o FlowOS Pro. Em alguns minutos, seu negócio vai ter uma memória própria e 18 agentes especializados prontos para trabalhar por você — atendimento, financeiro, conteúdo, vendas e operacional.

Você não precisa saber programar. Você precisa saber o que quer delegar.

---

## Ligando o sistema

Dois caminhos. Escolhe o que combina contigo.

### Caminho 1 — Pelo Claude (mais rápido)

Abre o Claude Code em qualquer pasta e cola o prompt abaixo:

```
Clona o https://github.com/flowzera/flowos-pro.git na pasta atual, entra nela e roda o /instalar.
```

Ele clona, entra na pasta e dispara a entrevista de setup. Você só responde.

### Caminho 2 — Pelo terminal (mais previsível)

Cola estes comandos no terminal, um por vez:

```bash
git clone https://github.com/flowzera/flowos-pro.git
cd flowos-pro
code .
```

Na janela do VS Code que abrir:

1. Abre o terminal integrado (`Ctrl + '` no Windows, `Cmd + '` no Mac)
2. Digita `claude` e dá Enter
3. Digita `/instalar` e dá Enter

### Depois que o /instalar terminar

Renomeia a pasta `flowos-pro/` para o nome do seu negócio:

- Fecha o VS Code
- Renomeia a pasta no Explorer (Windows) ou Finder (Mac)
- Abre o VS Code de novo na pasta renomeada

A pasta não fica como "flowos-pro" — ela é o teu negócio agora.

O `/instalar` roda uma vez só. Te entrevista sobre o negócio, monta a memória e configura todos os agentes. Depois disso, é só usar.

---

## O sistema

### Clientes — nunca mais perde quem entrou em contato
| Agente | O que faz | Exemplo |
|--------|-----------|---------|
| **Balcão** | Atendimento inbound no seu tom, 24/7 | `/Balcao Aqui a mensagem do WhatsApp, o que respondo?` |
| **Fisga** | Prospecção e primeiro contato estratégico | `/Fisga pesquisa essa empresa e monta abordagem` |
| **Aplauso** | Mais avaliações 5★ no Google | `/Aplauso o cliente X elogiou, o que faço?` |
| **Escuta** | Resumo de calls e follow-up automático | `/Escuta aqui o que aconteceu na reunião de hoje` |

### Financeiro — sabe onde está o dinheiro
| Agente | O que faz | Exemplo |
|--------|-----------|---------|
| **Farol** | Mini-CFO: fecha o mês em 15 minutos | `/Farol aqui as entradas e saídas de junho` |
| **Leme** | Top 3 prioridades do dia | `/Leme aqui tudo que tenho pra fazer, por onde começo?` |
| **Engrenagem** | Mapeia e melhora processos | `/Engrenagem esse processo tá quebrando, me ajuda` |

### Conteúdo — para de perder domingo escrevendo
| Agente | O que faz | Exemplo |
|--------|-----------|---------|
| **Escriba** | Posts e textos no seu tom em minutos | `/Escriba escreve 3 legendas pra esse produto` |
| **Pauta** | 30 dias de conteúdo planejado | `/Pauta monta o calendário de julho` |
| **Holofote** | Posicionamento e autoridade no nicho | `/Holofote quero aparecer mais no LinkedIn` |
| **Vitrine** | Relatórios e apresentações profissionais | `/Vitrine monta relatório de resultados pro cliente X` |

### Crescimento — estrutura para escalar
| Agente | O que faz | Exemplo |
|--------|-----------|---------|
| **Alavanca** | Transforma conhecimento em produto | `/Alavanca como transformo meu conhecimento em curso?` |
| **Forja** | Materiais comerciais prontos na hora | `/Forja preciso de um one-pager pra reunião amanhã` |
| **Orq. Propostas** | Proposta completa em minutos | `/orquestra-propostas monta proposta pro cliente Y` |
| **Orq. Tráfego** | Estrutura campanhas com estratégia real | `/orquestra-trafego campanha de leads pra clínica` |

### Operacional — a retaguarda do negócio
| Agente | O que faz | Exemplo |
|--------|-----------|---------|
| **Orq. Conteúdo** | Volume de conteúdo sem perder o tom | `/orquestra-conteudo 10 posts sobre gestão financeira` |
| **Orq. Documentos** | Contratos e documentos profissionais | `/orquestra-documentos contrato de prestação de serviços` |
| **Trilha** | Onboarding de clientes impecável | `/Trilha o cliente X fechou, monta o onboarding` |
| **Maestro** | Coordena todos os agentes | `/orquestra-maestro preciso fechar o mês e preparar proposta` |

---

## A tese

IA não é uma ferramenta que sua empresa usa. É o sistema operacional em que ela roda.

A diferença não é velocidade. É capacidade nova — uma pessoa com o FlowOS faz o que antes exigia um time inteiro. Atendimento, financeiro, conteúdo e operacional deixam de ser gargalos e passam a ser delegados.

O sistema não substitui você. Ele vira parte do seu negócio.

---

## Como o FlowOS pensa

`_memoria/negocio.md` é o cérebro. Tudo que importa do seu negócio mora aqui — quem você é, o que você vende, quem é o seu cliente, como você fala. O Claude lê isso antes de cada resposta. Quanto melhor a memória, melhor o sistema.

`_setup/` tem os guias. Instalação passo a passo e roteiro dos primeiros 7 dias.

`_setup/playbooks/` tem os guias de nicho. Encontra o seu segmento e começa por ele.

`.claude/skills/` tem os agentes. São 18 especializados no seu negócio.

---

## Quando precisar

[flowzera.com](https://flowzera.com) · ruan@flowzera.com · [@flowzera](https://instagram.com/flowzera)
