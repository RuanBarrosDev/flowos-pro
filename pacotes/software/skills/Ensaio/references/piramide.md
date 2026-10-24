# A pirâmide de testes (por que nem todo teste custa igual)

Nem todo teste é igual em custo e velocidade. A rede fica forte e barata de manter quando a
maior parte dos testes é do tipo **rápido e barato**, e só o mínimo necessário é do tipo **lento
e caro**. Isso é a pirâmide.

## Os três andares (do mais barato ao mais caro)
1. **Teste de peça (unitário)** — verifica uma peça isolada (o cálculo do total, a validação do
   CPF). Roda em milésimos de segundo, quase nunca fica instável. **A base da pirâmide — a maioria
   dos testes deve ser assim.**
2. **Teste de encaixe (integração)** — verifica duas ou três peças conversando (salvar no banco e
   ler de volta). Mais lento, ainda confiável. **O meio.**
3. **Teste de tela (ponta a ponta / e2e)** — abre o app de verdade num navegador e faz o percurso
   como um usuário (entrar, adicionar ao carrinho, pagar). Lento, mais frágil, caro de manter.
   **O topo — poucos, só para os percursos críticos que atravessam tudo.**

## A regra de ouro do custo
> **Empurre a verificação para baixo.** Antes de escrever um teste de tela, pergunte: "isso não
> poderia ser um teste de peça?" Um cálculo errado de frete se pega com um teste de peça
> rápido — não precisa abrir o navegador inteiro para descobrir isso.

Cinco testes de tela onde bastaria um de tela + quatro de peça = uma suíte lenta, instável e cara.
Um sinal de rede mal montada.

## Traduzindo a profundidade (modo Rede) para andares
- **Essencial** → só o caminho feliz de cada crítico; mistura de peça e um ou outro de tela.
- **Padrão** → feliz + erros comuns + pior caso, com a maior parte em testes de peça/encaixe e
  um teste de tela por percurso crítico.
- **Reforçada** → o acima + permissões, bordas e dados reais; ainda assim, cada checagem no andar
  mais barato onde ela couber.

## Para o dono, em uma frase
"Vou proteger o que importa com muitos testes rápidos e baratinhos e só uns poucos testes de tela
completos — assim a rede pega os problemas em segundos, não em minutos, e não fica falhando à toa."
