# Gravidade (as cores) e os 4 sinais de saúde

A base de todo plantão. Primeiro você mede o **tamanho do estrago** (a cor).
Depois olha **quais dos 4 sinais** estão ruins para saber por onde investigar.

---

## As 4 cores da gravidade

Pinte a cor pela pergunta: **quanta gente está sentindo, e há como contornar?**

| Cor | O que significa | Exemplos | Ritmo de resposta |
|---|---|---|---|
| 🔴 **Vermelho** | Tudo fora do ar ou prejuízo direto. Ninguém compra, ninguém entra, ou dados em risco. Sem contorno. | Site totalmente fora; checkout não fecha nenhuma venda; login não funciona pra ninguém | Largue tudo. Aja agora. Atualize as pessoas a cada ~30 min |
| 🟠 **Laranja** | Parte importante quebrada ou muita gente afetada, mas há um contorno parcial | Pagamento falha em parte das vezes; uma região fora; o bot responde, mas erra | Aja hoje, sem parar, até estabilizar |
| 🟡 **Amarelo** | Incômodo limitado. Tem contorno, o negócio continua | Uma tela lenta; um relatório que não gera; uma função secundária fora | Resolva no dia, sem pânico |
| ⚪ **Cinza** | Cosmético ou preventivo. Ninguém sente ainda | Erro de alinhamento; um limite se aproximando (ainda não estourou) | Entra na fila normal de melhorias |

**Duas regras de ouro:**
- **Na dúvida, pinte mais grave.** É barato rebaixar depois; é caro descobrir tarde.
- **A cor pode mudar.** Começou Vermelho e você achou um contorno? Vira Laranja. Registre a mudança.

> Uma coisa pode ser "pequena" tecnicamente e mesmo assim ser 🔴: um bug bobo numa
> tela durante uma demonstração ao vivo pro seu maior cliente é urgência máxima.
> A cor mede **o impacto no negócio**, não a dificuldade técnica.

---

## Os 4 sinais de saúde

Toda a saúde de um sistema no ar cabe em quatro perguntas. Quando algo quebra,
descubra **qual sinal** está ruim — ele aponta a família da causa.

### 1. No ar? (responde?)
O endereço responde quando alguém acessa?
- **Sinal ruim:** não carrega, dá tela branca, "não foi possível conectar", erro 500/502/503.
- **Onde olhar:** a checagem da Vigia (`scripts/vigia.py check`), ou abrir o endereço você mesmo.

### 2. Rápido? (demora?)
Responde num tempo aceitável ou está arrastado?
- **Sinal ruim:** carrega, mas leva muitos segundos; o cliente desiste antes.
- **Régua simples:** acima de ~3 segundos para abrir já incomoda. Defina o seu "normal" no Cartão de Saúde.

### 3. Sem erro? (entrega certo?)
Está fazendo o que deveria ou devolvendo erro/resultado errado?
- **Sinal ruim:** mensagens de erro, pagamento recusado sem motivo, o agente responde besteira, e-mail não sai.
- **Onde olhar:** o texto do erro, o log, o histórico do bot, o painel da ferramenta.

### 4. Aguenta? (tem fôlego?)
Está sobrando capacidade ou está no talo?
- **Sinal ruim:** memória/CPU no limite, disco cheio, "cota excedida", plano estourado, muitos acessos ao mesmo tempo.
- **Onde olhar:** o painel da hospedagem/ferramenta, avisos de "limite atingido", a fatura.

---

## De qual sinal para qual família de causa

| Sinal ruim | Famílias de causa mais prováveis (ver causas-comuns.md) |
|---|---|
| **No ar? = não** | Última mudança/deploy quebrou; serviço/hospedagem fora; certificado vencido; dependência de fora caiu |
| **Rápido? = não** | Banco/consulta no limite; muitos acessos; falta de fôlego (memória/CPU); dependência lenta |
| **Sem erro? = não** | Última mudança introduziu erro; credencial/chave vencida; dependência mudou; cota estourada |
| **Aguenta? = não** | Pico de acesso; vazamento de memória; disco cheio; plano/cota pequenos demais |

Sempre confirme com o **sinal real** antes de agir. Marque `✅ FATO` (medido) vs.
`🔎 HIPÓTESE` (a testar).
