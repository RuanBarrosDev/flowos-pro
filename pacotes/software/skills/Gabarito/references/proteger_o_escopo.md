# Proteger o escopo (a defesa contra o retrabalho)

O escopo incha sozinho. No meio da conversa aparece "ah, e já que estamos nisso,
podia também…". Cada "já que" não registrado vira atraso, custo e a obra errada. O
Gabarito combate isso separando o que é o quê — e nunca misturando.

## A fronteira: quatro caixas
- **Dentro do escopo** — o que esta versão VAI fazer.
- **Fora do escopo** — o que esta versão NÃO faz (a caixa mais importante).
- **Depende de terceiro** — precisa de algo que não está nas suas mãos (um dado do
  cliente, um acesso, uma decisão de outra área).
- **Bloqueado por decisão** — parado esperando alguém decidir.

## O contexto: quatro caixas separadas
Nunca misture estes quatro — cada um pede uma ação diferente:
- **Suposição** — o que você está ASSUMINDO como verdade (e pode estar errado). Ex.:
  "assumo que o cliente já tem uma conta de e-mail para envio."
- **Risco** — o que pode dar errado e o impacto se der. Ex.: "o número de WhatsApp
  pode ser bloqueado por envio em massa."
- **Restrição** — um limite que não se negocia. Ex.: "tem que rodar no celular do
  garçom, que é Android antigo."
- **Pergunta em aberto** — o que ainda falta decidir/descobrir. Ex.: "usaremos o
  WhatsApp oficial ou não?"

## Por que separar
Se você joga tudo num monte de "observações", ninguém age. Separado:
- Suposição vira item a **confirmar**.
- Risco vira item a **mitigar**.
- Restrição vira **regra de projeto**.
- Pergunta em aberto vira **decisão pendente** que trava a especificação até fechar.

## Como registrar
```bash
python3 scripts/gabarito.py escopo-add --tipo fora     --texto "não faz emissão de nota fiscal nesta versão"
python3 scripts/gabarito.py escopo-add --tipo depende  --texto "precisa da planilha de clientes do dono"
python3 scripts/gabarito.py escopo-add --tipo suposicao --texto "assumo 1 unidade só, sem multi-filial"
python3 scripts/gabarito.py escopo-add --tipo risco    --texto "envio em massa pode bloquear o número"
python3 scripts/gabarito.py escopo-add --tipo pergunta --texto "WhatsApp oficial ou comum?"
python3 scripts/gabarito.py escopo
```
Se a caixa "Fora do escopo" estiver vazia, o motor avisa: sem ela, o projeto incha.
A frase "isto NÃO faz parte" dita hoje economiza semanas amanhã.
