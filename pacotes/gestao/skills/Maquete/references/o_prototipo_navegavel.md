# O protótipo navegável — o que é e como usar

O comando `prototipo` gera um arquivo `.maquete/prototipo-N.html`. É um **único
arquivo, offline** — não precisa de internet, servidor, conta nem instalação. O dono
dá um duplo-clique e ele abre no navegador.

## O que tem dentro
- **Moldura do dispositivo** — web (janela de navegador), mobile (celular) ou desktop,
  conforme a plataforma do produto.
- **A tela atual** desenhada em lo-fi, com o conteúdo (blocos) que você definiu.
- **Painel lateral** com a lista de todas as telas (clique para pular para qualquer
  uma) e a lista de fluxos.
- **Navegação de verdade** — clicar num botão/link leva à tela de destino, como no
  produto real. É isto que faz dele um protótipo, não uma imagem.
- **Modo passo-a-passo por fluxo** — clique num fluxo na lateral e use as setas
  `← →` (do stepper embaixo, ou do teclado) para andar pela jornada na ordem certa.
  Ótimo para apresentar: "veja, o cliente entra aqui, clica aqui, e termina aqui".

## Para que serve (dois usos)
1. **Validar com usuário real** — sente com uma pessoa da persona, peça para ela
   "marcar um horário" clicando, e observe onde ela trava. Cada travada é um furo no
   fluxo que você corrige ANTES de gastar horas construindo. Isto se chama teste de
   usabilidade, e é o jeito mais barato de descobrir que o produto está errado.
2. **Fechar o projeto com o cliente** (consultor/agência) — mostrar um protótipo
   clicável faz o cliente "sentir" o produto e aprovar o escopo antes de você
   programar. Vende melhor que qualquer proposta em texto, e blinda o escopo.

## Como apresentar bem
- Abra pelo **fluxo principal** (o stepper já começa nele).
- Deixe claro que é **rascunho** (o próprio protótipo diz "não é a arte final") — o
  cinza é de propósito, para discutir estrutura, não cor.
- Anote cada pedido de mudança e volte ao passo 3/4 (fluxo/tela) para ajustar. Gere o
  protótipo de novo (`prototipo` cria `-2.html`, `-3.html`... sem apagar os anteriores)
  — assim você guarda o histórico das versões.

## Limites honestos
- É baixa fidelidade: não tem cor de marca, animação nem dados reais — de propósito.
- Os campos não guardam o que você digita (é maquete, não o sistema). O valor está em
  **clicar e navegar**, não em preencher.
