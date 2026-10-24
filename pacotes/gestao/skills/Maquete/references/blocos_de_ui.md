# Vocabulário de blocos (o que cada um vira na tela)

Os blocos são a "linguagem" com que você descreve uma tela. Um bloco por linha, no
campo `--blocos`, separados por `||`. O motor desenha cada um em lo-fi. Ações
(botão/link/nav/abas) apontam o destino com `-> T.xx`.

| Bloco | Escreve assim | Vira na tela |
|-------|---------------|--------------|
| `titulo` | `titulo: Entrar` | Título grande da tela |
| `subtitulo` | `subtitulo: Seus dados` | Um subtítulo de seção |
| `texto` | `texto: Escolha um horário abaixo` | Um parágrafo/instrução |
| `campo` | `campo: E-mail` | Um campo de digitar (input) com rótulo |
| `area` | `area: Observações` | Um campo de texto longo |
| `selecao` | `selecao: Cidade` | Uma caixa de escolha (dropdown) |
| `botao` | `botao: Salvar -> T.02` | Botão sólido que NAVEGA para T.02 |
| `link` | `link: Cancelar -> T.02` | Link de texto que NAVEGA para T.02 |
| `lista` | `lista: Ana, Bruno, Carla` | Uma lista de itens |
| `tabela` | `tabela: Hora, Cliente, Status` | Cabeçalho de tabela + linhas vazias |
| `card` | `card: Plano Pro \| R$ 99/mês` | Um cartão com título e uma linha |
| `imagem` | `imagem: foto do produto` | Um quadro de imagem (placeholder) |
| `abas` | `abas: Dados, Segurança` | Abas no topo (podem navegar com `-> T.xx`) |
| `nav` | `nav: Início -> T.02, Perfil -> T.05` | Barra de navegação (cada item navega) |
| `metrica` | `metrica: Vendas \| R$ 12k` | Um quadradinho de número (KPI) |
| `aviso` | `aviso: Preencha o e-mail` | Uma faixa de aviso |
| `espaco` | `espaco` | Um respiro em branco entre blocos |

## Regras rápidas
- **O destino `-> T.xx` é o que torna o protótipo clicável.** Botão sem destino vira
  um botão "morto" (cinza claro) — útil para marcar "aqui vai ter uma ação, mas ainda
  não sei para onde".
- **`nav` e `abas` aceitam vários itens** separados por vírgula, cada um com seu
  destino: `nav: Início -> T.02, Pedidos -> T.03, Perfil -> T.05`.
- **`card` usa `|`** para separar título de subtítulo: `card: Pedido #12 | aguardando`.
- **`metrica` usa `|`** para separar rótulo de valor: `metrica: Novos clientes | 8`.
- Não precisa decorar: escreva em português normal e o motor entende. Bloco que ele
  não reconhecer, ele mostra como texto (não quebra).
