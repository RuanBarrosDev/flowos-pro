# Maquete — o desenho do produto antes da obra

**Transforma um pedido de software — "quero um app/site/sistema que faça X" (seu ou
de um cliente) — no desenho navegável do produto: os fluxos de uso, os wireframes
lo-fi de cada tela e um protótipo HTML clicável que você abre no navegador, mostra
pro cliente e valida com usuário — ANTES de escrever uma linha de código.**

O nome vem da arquitetura: a **maquete** é o modelo em escala que se monta antes da
obra, para todo mundo ver e aprovar antes de assentar o primeiro tijolo.

## O que ela faz
- **Desenha o fluxo primeiro** (a tarefa que o usuário quer cumprir), depois as telas
  que esse fluxo precisa — nada de telas soltas que não conversam.
- Monta cada tela em **lo-fi** com um vocabulário simples (título, campo, botão,
  lista, tabela, métrica, nav...) — sem você precisar de Figma nem saber desenhar.
- Gera um **protótipo HTML clicável e navegável** — um arquivo único, offline, que
  abre com duplo-clique e se navega de verdade pelos botões, com modo passo-a-passo
  por fluxo.
- Roda travas de qualidade: aponta **telas órfãs** (ninguém chega nelas) e **ações
  quebradas** (botão sem destino).
- Entrega o **brief de construção** pronto para o Gabarito/Estaleiro/Claude Code
  construir a coisa certa.

Nunca inventa conteúdo real: o que você não disser vira placeholder ou **[A CONFERIR]**.
Tudo fica **local** na sua máquina (nada vai para a internet).

## Como instalar
1. Baixe e descompacte o arquivo.
2. Copie a pasta `Maquete/` para dentro de `.claude/skills/` do seu projeto (ou de
   `~/.claude/skills/` para usar em qualquer projeto):
   ```
   .claude/skills/Maquete/
   ```
3. Abra o Claude Code nesse projeto. Pronto — a skill é reconhecida sozinha.

## Como usar
Fale naturalmente. Exemplos que disparam a skill:
- "Quero criar um app de agendamento para minha clínica — me ajuda a desenhar as telas."
- "Como vai ser a navegação do meu sistema? Quero um protótipo pra mostrar pro cliente."
- "Desenha a tela de login e o painel principal desse SaaS."

Na primeira vez, a skill faz uma instalação rápida (pergunta seu nome e a plataforma
padrão) e some com os arquivos de setup. Depois é só conversar: ela desenha os fluxos,
monta as telas, gera o protótipo navegável e o brief para construir.

Você nunca precisa digitar comando nenhum — a IA cuida disso nos bastidores. Você só
conversa e, no fim, abre o protótipo no navegador.

## O que esperar (regras de ouro)
- **Começa pelo fluxo**, não pela tela bonita — a tarefa do usuário vem primeiro.
- **Lo-fi de propósito** — cinza, sem arte final, para discutir estrutura e navegação
  (a cor e a marca vêm depois, no build).
- **Nunca inventa** — sem dados reais, fica placeholder / [A CONFERIR].
- **Toda ação leva a algum lugar** — se não dá para clicar e chegar, o fluxo tem furo,
  e a skill avisa.
- **É protótipo, não a arte final** — serve para DECIDIR e VALIDAR antes de construir.
- **Seus dados são seus** — tudo local, nada na nuvem (LGPD).

## Requisitos técnicos
Apenas **Python 3** (já vem no macOS e na maioria dos Linux) e um navegador para abrir
o protótipo. Sem instalação de pacotes, sem conta, sem internet.

## Onde ficam seus dados
Tudo em `.maquete/` na raiz do seu projeto (ignorado pelo Git). O protótipo fica em
`.maquete/prototipo-1.html`, `-2.html`, etc.; os wireframes e o brief em `.maquete/`.

---

Feito pela **Maestria Academy** para a comunidade. Licença MIT.
