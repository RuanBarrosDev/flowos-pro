# Causas comuns — o que mais derruba um sistema no ar

Quando algo quebra, a causa quase nunca é exótica. Esta é a lista das suspeitas
de sempre, **na ordem em que valem ser checadas** — cada uma com o sinal que a
denuncia e o primeiro movimento. A Vigia percorre de cima para baixo, marcando
`✅ FATO` ou `🔎 HIPÓTESE`, sem chutar correção.

> Princípio: **estabilizar primeiro, entender depois.** Se está 🔴/🟠, o objetivo
> imediato é voltar ao ar — o diagnóstico completo vem em seguida.

---

## 1. A última mudança quebrou (a suspeita nº 1)
- **Sinal:** o problema começou logo depois de um deploy, uma publicação, um
  ajuste de configuração, um "liguei uma opção nova" ou uma atualização.
- **Pergunta-chave:** *o que mudou nas últimas horas?*
- **Primeiro movimento:** **desfazer a última mudança** — voltar para a versão
  que estava funcionando (reverter o deploy, desligar a opção nova, restaurar a
  config anterior). É o movimento mais rápido e mais barato para parar o
  sangramento. Entender *por quê* vem depois, com calma.

## 2. Uma dependência de fora caiu
- **Sinal:** o erro cita um serviço externo (gateway de pagamento, provedor de
  e-mail, API de um parceiro, banco de dados hospedado, a própria IA que o
  sistema chama). Seu sistema está "no ar", mas engasga naquele ponto.
- **Primeiro movimento:** confira a página de status daquele serviço; se for ele,
  não há conserto do seu lado — comunique o cliente, ative um contorno se houver,
  e aguarde/escale com o fornecedor.

## 3. Banco de dados ou consulta no limite
- **Sinal:** ficou **lento** (Rápido? = não) ou dá erro só sob carga; picos de uso.
- **Primeiro movimento:** veja o painel do banco (conexões/CPU no talo?). Reduza
  a carga (desligue algo pesado), aumente o fôlego se o plano permitir, e depois
  investigue a consulta pesada com calma.

## 4. Cota / plano / crédito estourado
- **Sinal:** "limite atingido", "cota excedida", "créditos esgotados", parou
  exatamente ao virar o mês ou depois de um pico de uso. Comum com IA/API paga,
  envio de e-mail, SMS/WhatsApp, armazenamento.
- **Primeiro movimento:** confira o painel de uso/fatura do serviço. Recarregue,
  suba o plano, ou reduza o consumo. Anote o limite no Cartão de Saúde para
  virar um sensor ("me avise em 80%").

## 5. Credencial ou certificado vencido
- **Sinal:** parou "do nada", sem mudança recente; erro de autenticação (401/403),
  "chave inválida", ou aviso de certificado/SSL vencido (cadeado quebrado, "site
  não seguro").
- **Primeiro movimento:** renove/gire a chave ou o certificado. Certificados
  costumam ter data de validade — anote a próxima como sensor.

## 6. Sem fôlego: memória, CPU ou disco cheio
- **Sinal:** lento e piorando, reinícios sozinho, "sem espaço", travou depois de
  horas no ar (vazamento de memória).
- **Primeiro movimento:** reinicie para aliviar já; libere disco; suba o tamanho
  da máquina/plano se for recorrente; depois investigue o vazamento.

## 7. Pico de acesso / muita gente ao mesmo tempo
- **Sinal:** caiu logo após uma campanha, um post que viralizou, um envio em massa.
- **Primeiro movimento:** aumente o fôlego temporariamente se possível; segure o
  que dá para adiar; comunique. Planeje capacidade para o próximo pico.

---

## Tabela-relâmpago

| # | Causa | Sinal que aponta | Primeiro movimento |
|---|---|---|---|
| 1 | Última mudança | começou após deploy/ajuste | **desfazer a última mudança** |
| 2 | Dependência de fora | erro cita serviço externo | ver status do fornecedor; contorno + avisar |
| 3 | Banco/consulta no limite | lento sob carga | reduzir carga / subir fôlego |
| 4 | Cota/plano estourado | "limite atingido" | recarregar / subir plano |
| 5 | Credencial/certificado | parou sem mudança; 401/403/SSL | renovar chave / certificado |
| 6 | Sem fôlego (memória/CPU/disco) | lento e piorando; travou após horas | reiniciar; liberar; aumentar |
| 7 | Pico de acesso | caiu após campanha/viral | subir fôlego; segurar o adiável |

---

## O que NÃO é da Vigia (encaminhe)
- **Suspeita de ataque, golpe, invasão, phishing, sequestro de conta, vazamento
  proposital** → **Baluarte** (cibersegurança defensiva). A Vigia cuida de
  confiabilidade e disponibilidade, não de defesa contra atacante.
- **É um bug no código, em desenvolvimento, ainda não está no ar** → **Rastro**.
- **Quero uma rede de testes que impeça isso antes de subir** → **Ensaio**.
- **Só preciso colocar/repor no ar** → **Órbita**.
