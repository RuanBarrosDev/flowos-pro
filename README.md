# FlowOS Pro

**O sistema operacional do seu negócio dentro do Claude Code.**

Em alguns minutos o seu negócio ganha uma memória própria, um núcleo de 12 agentes e um acervo de mais 43 em 5 pacotes: clientes, marketing, gestão, software e YouTube. Você liga só o que faz sentido para você.

Você não precisa saber programar. Precisa saber o que quer delegar.

---

## Ligando o sistema

Dois caminhos. Escolha o que combina com você.

### Caminho 1: pelo Claude (mais rápido)

Abra o Claude Code em qualquer pasta e cole o prompt abaixo:

```
Clona o https://github.com/RuanBarrosDev/flowos-pro.git na pasta atual, entra nela e roda o /instalar.
```

Ele clona, entra na pasta e começa a entrevista de setup. Você só responde.

### Caminho 2: pelo terminal (mais previsível)

Cole estes comandos no terminal, um por vez:

```bash
git clone https://github.com/RuanBarrosDev/flowos-pro.git
cd flowos-pro
code .
```

Na janela do VS Code que abrir:

1. Abra o terminal integrado (`Ctrl + '` no Windows, `Cmd + '` no Mac)
2. Digite `claude` e dê Enter
3. Digite `/instalar` e dê Enter

### Depois que o /instalar terminar

Renomeie a pasta `flowos-pro/` para o nome do seu negócio:

- Feche o VS Code
- Renomeie a pasta no Explorer (Windows) ou no Finder (Mac)
- Abra o VS Code de novo na pasta renomeada

O `/instalar` roda uma vez só. Ele te entrevista sobre o negócio, monta a memória e pergunta quais pacotes ligar. Depois disso, é só usar.

---

## O núcleo (sempre ligado)

| Agente | O que faz | Exemplo |
|--------|-----------|---------|
| **Balcão** | Atendimento no seu tom | `/Balcao Aqui a mensagem do WhatsApp, o que respondo?` |
| **Fisga** | Prospecção e primeiro contato | `/Fisga pesquisa essa empresa e monta abordagem` |
| **Aplauso** | Avaliações e reputação no Google | `/Aplauso o cliente X elogiou, o que faço?` |
| **Escuta** | Resumo de reunião e follow-up | `/Escuta aqui o que aconteceu na reunião de hoje` |
| **Farol** | Fecha o mês e mostra onde está o dinheiro | `/Farol aqui as entradas e saídas de junho` |
| **Leme** | As 3 prioridades do dia | `/Leme aqui tudo que tenho pra fazer, por onde começo?` |
| **Escriba** | Posts e textos no seu tom | `/Escriba escreve 3 legendas pra esse produto` |
| **Holofote** | Calendário de conteúdo e autoridade | `/Holofote monta o calendário do mês` |
| **Vitrine** | Relatórios e apresentações | `/Vitrine monta relatório de resultados pro cliente X` |
| **Alavanca** | Conhecimento vira produto digital | `/Alavanca como transformo o que eu sei em curso?` |
| **Orq. Documentos** | Contratos e documentos | `/orquestra-documentos contrato de prestação de serviços` |
| **Maestro** | Coordena os outros agentes | `/orquestra-maestro preciso fechar o mês e preparar proposta` |

## Os pacotes (você escolhe)

| Pacote | O que tem |
|---|---|
| **Clientes** (11) | Cais, Amarra, Planta, Sextante, Âncora, Pulso, Aceno, Cadência, Régua, Emissário, Rédea |
| **Marketing** (6) | Turbina, Estopim, Ponte, Missiva, Mostruário, Alfândega |
| **Gestão** (7) | Fisco, Fulcro, Garimpo, Alambique, Tribuna, Maquete, Veredito |
| **Software** (13) | Gabarito, Arcabouço, Prumo, Crivo, Rastro, Ensaio, Vigia, Novelo + 5 agentes Estaleiro |
| **YouTube** (6) | Agentes Claquete: pauta, roteiro, thumbnail, SEO, publicação e análise |

O que cada um faz está em [`pacotes/README.md`](pacotes/README.md). Para ligar ou desligar a qualquer hora: `/pacotes`.

---

## A tese

IA não é uma ferramenta que a sua empresa usa. É o sistema operacional em que ela roda.

A diferença não é só velocidade, é capacidade nova: uma pessoa com o FlowOS faz o que antes pedia um time. Atendimento, financeiro, conteúdo e operação deixam de ser gargalo e passam a ser delegados.

O sistema não substitui você. Ele vira parte do seu negócio.

---

## Como o FlowOS pensa

`_memoria/negocio.md` é o cérebro. Tudo que importa do seu negócio mora ali: quem você é, o que vende, quem é o seu cliente, como você fala. O Claude lê isso antes de cada resposta. Quanto melhor a memória, melhor o sistema.

`.claude/skills/` tem os agentes ligados. `pacotes/` tem os guardados.

`_setup/` tem os guias: instalação passo a passo e o roteiro dos primeiros 7 dias. Em `_setup/playbooks/` estão os guias por nicho.

---

## Créditos

Os agentes dos pacotes são da Maestria Academy, sob licença MIT. Veja [`CREDITOS.md`](CREDITOS.md).

## Quando precisar

[flowzhub.com/flowos](https://flowzhub.com/flowos) · ruan@flowzera.com · [@barrosruan_](https://instagram.com/barrosruan_)
