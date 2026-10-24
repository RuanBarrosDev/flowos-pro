# Achar os caminhos críticos (o que vale a pena proteger)

Uma rede de testes não protege tudo — protege o que, se quebrar, vira **desastre, prejuízo ou
vergonha**. Esses são os caminhos críticos. Descubra-os conversando em linguagem de negócio, não
de código.

## A pergunta-chave para o dono
> "Se você acordasse amanhã e UMA coisa do seu app tivesse parado de funcionar sem ninguém
> avisar, o que seria pior?"

A resposta (e as 3–4 seguintes) são a lista de críticos. Traduza cada uma para um comportamento
concreto e verificável.

## Os candidatos quase sempre críticos
- **Entrar na conta** (login/cadastro) — se quebra, ninguém usa o app.
- **Dinheiro** — pagamento, checkout, cálculo de total/frete/imposto/desconto. Erro aqui custa
  caro e mina a confiança. Sempre profundidade **Reforçada**.
- **Não perder dados** — salvar, editar, o dado gravado é mesmo o que foi digitado; nada some.
- **A ação principal do app** — o que o usuário veio fazer (enviar o formulário, gerar o
  relatório, agendar, publicar).
- **Permissões** — quem NÃO pode ver/fazer algo realmente não consegue (o cliente A não vê o
  dado do cliente B).

## Como transformar "crítico" em teste
Para cada crítico, escreva o comportamento como uma frase concreta que dá para verificar:
- Ruim (vago): "testar o checkout".
- Bom (concreto): "com o cartão recusado, aparece a opção de tentar de novo e o carrinho continua
  cheio"; "o total de 2 itens de R$ 50 com frete R$ 20 é R$ 120,00".

Uma frase concreta assim vira um teste bom. Uma frase vaga vira um teste inútil.

## Regra da profundidade por risco
Quanto mais perigoso o caminho, mais fundo o teste vai:
- **Dinheiro, login, apagar/alterar coisa irreversível** → Reforçada (caminho feliz + erros +
  bordas + permissões).
- **Ação principal do dia a dia** → Padrão (feliz + principais erros + pior caso).
- **Tela cosmética, coisa interna, algo que muda toda semana** → Essencial ou nem testa.

Não gaste esforço protegendo o que é barato de quebrar e fácil de perceber. Gaste no que quebra
calado e dói.
