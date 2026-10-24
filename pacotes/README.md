# Pacotes do FlowOS Pro

O núcleo (12 agentes) já vem ligado. Os pacotes abaixo ficam guardados aqui e só entram no seu Claude Code quando você ativa. Assim ele não fica com dezenas de agentes disputando atenção num negócio que só usa alguns.

Para ver, ativar ou desativar: digite `/pacotes` no Claude Code.

Ativar copia as skills do pacote para `.claude/skills/` e os agentes para `.claude/agents/`. Desativar apaga só essas cópias: o original continua aqui e os dados que o agente criou (pastas que começam com ponto, como `.ancora/`) não são tocados.

---

## Clientes (11 skills)
Do primeiro "sim" à renovação: venda consultiva, onboarding, retenção, cobrança e o agente de IA que atende por você.

| Skill | Para quê |
|---|---|
| Cais | Onboarding do cliente que acabou de fechar: boas-vindas, questionário, acessos e combinado de escopo |
| Amarra | Da reunião de descoberta à proposta com 3 opções, ROI com os números do cliente e biblioteca de objeções |
| Planta | Escopo, complexidade e organização da entrega de um projeto de automação ou IA para cliente |
| Sextante | Diagnóstico de maturidade em IA de uma empresa, com roadmap em ondas |
| Âncora | Saúde de cada cliente recorrente, radar de renovação e plano para quem está em risco |
| Pulso | NPS, CSAT e CES: mede a satisfação e mostra o que mudar |
| Aceno | Reativa quem comprou e sumiu, com a mensagem de retorno certa |
| Cadência | Receita recorrente: MRR, churn, LTV e previsão com premissas à vista |
| Régua | Quem está devendo, quanto e há quantos dias, e a cobrança sem perder o cliente |
| Emissário | Projeta o seu agente de IA de atendimento (persona, base, fluxos, quando chamar humano) |
| Rédea | Testa e governa esse agente antes e depois de ir para o ar |

## Marketing (6 skills)
Tráfego, campanha, e-mail e venda de produto.

| Skill | Para quê |
|---|---|
| Turbina | Tráfego pago Meta e Google Ads: estrutura da conta, verba e leitura dos números |
| Estopim | Conceito de campanha: briefing, insight e a grande ideia antes do criativo |
| Ponte | Adapta página, e-mail, anúncio ou VSL para outro idioma e mercado |
| Missiva | E-mail marketing e newsletter: lista, sequências e campanhas |
| Mostruário | Anúncio de produto para marketplace e loja: título, atributos, descrição e fotos |
| Alfândega | Fornecedor e custo real de importação (produto, frete, impostos e câmbio) |

## Gestão (7 skills)
Decisão, números, impostos, estudo e autoridade.

| Skill | Para quê |
|---|---|
| Fisco | Impostos, regime tributário e calendário de obrigações, com a Reforma Tributária em português simples |
| Fulcro | Estrutura uma decisão difícil para você decidir melhor, sem travar e sem impulso |
| Garimpo | Responde perguntas sobre qualquer planilha ou CSV |
| Alambique | Transforma vídeo, aula, podcast ou PDF em resumo e cartões de revisão |
| Tribuna | Ponto de vista e método próprios para virar referência no seu nicho |
| Maquete | Desenho navegável de um app ou sistema (fluxos e telas) antes de programar |
| Veredito | Painel para aprovar ou rejeitar um lote de itens um a um |

## Software (8 skills + 5 agentes Estaleiro)
Para quem constrói app, site, sistema ou automação com o Claude Code.

| Skill / agente | Para quê |
|---|---|
| Gabarito | Transforma um pedido vago em especificação com critério de aceite |
| Arcabouço | Desenha o banco de dados antes de programar |
| Prumo | Plano enxuto que economiza tokens e acerta na primeira |
| Crivo | Revisão do que mudou antes de subir: bug, segurança e excesso |
| Rastro | Depuração metódica até a causa do bug |
| Ensaio | Testes automáticos do que é crítico, para quem não lê o próprio código |
| Vigia | Monitoramento e plantão quando o sistema já está no ar |
| Novelo | Desembaraça e explica um projeto que virou bagunça |
| estaleiro-arquiteto, -construtor, -testes, -revisor, -sentinela | Tripulação que planeja, implementa, testa, revisa e blinda o código |

Setup opcional do Estaleiro: diga "Rode o setup do Estaleiro" (perguntas em `pacotes/software/setup-estaleiro/`).

## YouTube (6 agentes Claquete)
O canal de ponta a ponta.

| Agente | Para quê |
|---|---|
| claquete-pauteiro | Ideias e pauta da semana com base em demanda real |
| claquete-roteirista | Roteiro com gancho e estrutura de retenção, para vídeo longo ou Shorts |
| claquete-diretor-arte | Thumbnail e 3 a 5 títulos clicáveis sem mentira |
| claquete-otimizador | Descrição, tags, capítulos e palavras-chave |
| claquete-produtor | Coordena tudo e monta o pacote de publicação |
| claquete-analista | Lê os números do vídeo publicado e diz o que mudar no próximo |

Setup opcional da Claquete: diga "Rode o setup da Claquete" (perguntas em `pacotes/youtube/setup-claquete/`).

---

As skills e os agentes dos pacotes são da Maestria Academy, sob licença MIT. Cada pasta traz o seu arquivo `LICENSE`. Detalhes em `CREDITOS.md`, na raiz do kit.
