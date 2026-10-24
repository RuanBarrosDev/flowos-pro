# Playbook FlowOS Pro para Agências e Prestadores de Marketing

**Para:** agências de tráfego pago, social media, criação, conteúdo, automação e serviços digitais para empresas.

**Antes de começar:** boa parte deste playbook usa agentes dos pacotes **Clientes** e **Marketing**. Se não ativou no `/instalar`, roda `/pacotes` e liga os dois.

---

## Os 3 agentes que mudam o jogo para você primeiro

### 1. Turbina: estrutura de campanha que você apresenta como estrategista, não como operador

(pacote Marketing: ative com `/pacotes`)

Agência que apresenta estratégia cobra mais e retém cliente por mais tempo. A Turbina planeja a estrutura da conta, faz a conta da verba e lê os números da campanha para dizer o que pausar, ajustar ou escalar. Ela não mexe na conta: quem executa no Gerenciador é você.

**Estruturando campanha para cliente novo:**
```
/Turbina estrutura campanha de leads para cliente novo: [tipo de negócio]
Objetivo: [X leads/mês]
Verba: R$[valor]/mês
Público: [cidade/região]
```

**Lendo os números da semana:**
```
/Turbina aqui a exportação da semana do cliente [nome]: [cola as métricas]
O que pausar, o que ajustar e o que escalar?
```

**Decidindo quanto investir:**
```
/Turbina o cliente [nome] vende [produto] a R$[X] com margem de [Y]%. Qual o custo por venda máximo e quanto de verba faz sentido para começar?
```

O texto do anúncio fica com o Escriba:
```
/Escriba escreve 3 textos de anúncio para [cliente]. Produto: [X]. Público: [quem]. Objetivo: leads.
```

---

### 2. Vitrine: relatório que o cliente entende e que justifica o contrato

Cliente que não entende o relatório uma hora questiona o valor. O Vitrine monta relatórios que comunicam resultado, não só números.

**Relatório mensal:**
```
/Vitrine monta relatório de tráfego do mês para o cliente [nome]
Dados: [métricas de Google Ads / Meta Ads]
Compare com mês anterior: [dados anteriores]
```

**Apresentação de resultados em reunião:**
```
/Vitrine estrutura apresentação dos resultados do trimestre para o cliente [nome]. Foco: mostrar o ROI e o que vem pela frente.
```

---

### 3. Amarra: da reunião de descoberta à proposta que fecha

(pacote Clientes: ative com `/pacotes`)

Agência perde muito prospect no "vou pensar". A Amarra prepara o roteiro da reunião de descoberta, registra a dor do cliente nas palavras dele e monta uma proposta consultiva com 3 opções. Ela não inventa preço: os valores saem de você.

**Antes da reunião:**
```
/Amarra tenho reunião de descoberta com [tipo de negócio] na quinta. Monta o roteiro de perguntas.
```

**Proposta de gestão de tráfego:**
```
/Amarra fiz a reunião com [cliente]. O que ele disse: [dor, meta, prazo, quem decide].
Monta a proposta de gestão de tráfego com 3 opções.
Meus preços: [valor de cada opção]
```

**Quando o prospect trava:**
```
/Amarra mandei a proposta de tráfego + social media para [cliente] e ele disse "vou pensar". Como respondo?
```

---

## Rotina mensal recomendada

| Frequência | Agente | Tarefa |
|-----------|--------|--------|
| Todo dia | Leme | Prioridades entre clientes (urgências, entregas) |
| Toda semana | Turbina | Leitura dos números e ajustes nas campanhas dos clientes |
| Toda semana | Holofote + Escriba | Calendário e posts para as redes dos clientes |
| Quinzenal | Vitrine | Relatório de resultados para cada cliente |
| Por demanda | Amarra | Toda proposta nova ou renovação |
| Por demanda | Cais | Todo cliente novo que fechar |
| Mensal | Âncora | Saúde da carteira e quem está em risco de cancelar |
| Mensal | Régua | Quem está devendo e a cobrança no tom certo |
| Mensal | Farol | Análise de margem por cliente e do negócio como um todo |

Cais, Âncora e Régua ficam no pacote Clientes (ative com `/pacotes`).

---

## Exemplos práticos por situação

**Cliente insatisfeito com resultado:**
```
/Ancora o cliente [nome] reclamou dos resultados dessa semana. O que ele disse: [resume a conversa]. Ele está em risco? Monta o plano para segurar.
```

**Onboarding de cliente novo:**
```
/Cais cliente [nome] fechou gestão de tráfego. Monta as boas-vindas, a lista de acessos e documentos que preciso receber e a reunião de largada.
```

**Mensalidade atrasada:**
```
/Regua o cliente [nome] está com a mensalidade de R$[X] atrasada há [N] dias. Monta a cobrança sem estragar a relação.
```

**Contrato de prestação de serviços:**
```
/orquestra-documentos cria contrato de gestão de tráfego pago
Valor: R$[X]/mês
Prazo mínimo: 3 meses
Incluso: [o que você gerencia]
```

**Captando nova agência para parceria:**
```
/Fisga quero me aproximar de agências de comunicação que não fazem tráfego para fazer parceria. Monta abordagem.
```

**Definindo precificação dos serviços:**
```
/Farol tenho [N] clientes pagando R$[X]/mês em média. Meus custos com ferramentas são R$[Y]. Equipe custa R$[Z]. Qual minha margem real?
```

---

## Crescimento da agência com o FlowOS

**Vendendo automação além do tráfego** (Planta, pacote Clientes: ative com `/pacotes`):
```
/Planta o cliente [nome] quer automatizar o atendimento no WhatsApp. Me ajuda a levantar o processo dele e montar o escopo do projeto.
```

**Criando material para captar novos clientes:**
```
/Vitrine monta uma apresentação com o case de resultado do cliente [nome] para usar na prospecção. Dados: [o que foi feito e os números]
```

**Alavancando conhecimento:**
```
/Alavanca quero criar um produto para ensinar [habilidade da agência] para outros donos de negócio. Por onde começo?
```

---

> Dúvidas? ruan@flowzera.com · [@flowzera](https://instagram.com/flowzera)
