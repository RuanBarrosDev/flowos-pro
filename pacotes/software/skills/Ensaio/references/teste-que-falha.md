# O teste que é capaz de falhar (e a caça ao falso-verde)

A pergunta que separa proteção de teatro: **"esse teste consegue falhar se o app quebrar?"**
Se a resposta for não, ele é pior que nada — ele mente dizendo que está tudo bem.

## A prova obrigatória (todo teste novo passa por ela)
1. Escreva o teste.
2. **Quebre de propósito** a coisa que ele deveria proteger (mude o valor esperado, ou estrague
   o comportamento por um instante).
3. Rode. O teste **tem** que falhar — e falhar **pelo motivo certo** (não por um erro bobo de
   digitação no teste).
4. Desfaça a quebra. Rode. O teste passa.
5. Só agora o teste entra na rede.

Se o teste passou no passo 3 (ou seja, passou mesmo com o app quebrado), ele é falso-verde:
conserte ou jogue fora.

## O catálogo do falso-verde (o que procurar num Diagnóstico/Faxina)
- **Sem verificação de verdade:** o teste faz a ação mas não confere o resultado ("clicou no
  botão" e acabou, sem checar o que devia acontecer).
- **Verificação fraca:** confere que "existe algo" em vez de "o valor certo" (ex.: "a página
  carregou" em vez de "o total é R$ 150,00").
- **Erro engolido:** o teste captura a exceção e segue como se nada fosse; o app pode estar
  explodindo e o teste fica verde.
- **Mock testando o mock:** tanta coisa foi simulada que o teste só prova que a simulação
  funciona, não o app real. Simule a fronteira (rede, banco), nunca o miolo que você quer testar.
- **Verificação condicional:** o `if` do teste faz a checagem só acontecer num caminho que nunca
  roda — na prática, nada é verificado.
- **Asserção sempre-verdadeira:** comparar uma coisa com ela mesma, ou esperar algo que é sempre
  válido.

## Armadilhas de "verde fácil" (regra de ouro nº 2)
- **Cache:** checagem de tipos ou build reaproveitando resultado velho — rode do zero quando o
  verde vier rápido demais.
- **Servidor antigo:** o teste de tela conversando com uma versão anterior do app ainda no ar.
- **Filtro ligado:** um `.only`/`focus`/`skip` esquecido fazendo a suíte rodar 1 teste em vez de
  200 e declarar "tudo passou".
- **Nada rodou:** "0 testes, 0 falhas" é vermelho disfarçado de verde.

Quando o resultado parecer bom demais, desconfie e rode de novo, frio.
