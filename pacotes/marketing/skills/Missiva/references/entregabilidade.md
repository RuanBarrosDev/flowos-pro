# Entregabilidade — como não cair no spam

Entregabilidade é sua capacidade de chegar na caixa de entrada (não no spam, não no
"Promoções"). Ela depende de reputação, autenticação e higiene. Explique isso ao dono
em linguagem simples.

## Os 3 selos de autenticação (configura uma vez, no seu domínio)
Sem eles, provedores como Gmail e Outlook desconfiam de você. Quem cuida do domínio (ou
o suporte do seu ESP) configura no DNS:
- **SPF** — diz quais servidores podem enviar em nome do seu domínio.
- **DKIM** — assinatura que prova que o e-mail não foi adulterado.
- **DMARC** — a política que junta os dois e diz o que fazer com quem falha.
> Gmail e Yahoo passaram a **exigir** os três para quem envia volume. Se você usa um ESP
> (Mailchimp/Brevo/etc.), ele tem um passo a passo para autenticar seu domínio — faça isso
> antes de escalar. Enviar de um @gmail.com comum em massa é o caminho mais rápido para o spam.

## Higiene de lista (o que mais protege sua reputação)
- **Nunca compre nem raspe lista.** É ilegal (LGPD) e é a forma nº 1 de queimar o domínio.
- **Opt-in sempre.** Só envie para quem pediu. Confirmação dupla (double opt-in) é o padrão-ouro.
- **Suprima na hora:** descadastrados, bounces e reclamações saem da lista e não voltam.
- **Sunset:** quem não abre há 60–90 dias entra no win-back; se não reagir, pare de enviar.
  Manter inativo derruba a entrega de TODA a lista.

## Métricas que sinalizam problema (o Painel calcula isso)
Benchmarks são referência, variam por setor e mudam com o tempo — **verifique os atuais
antes de decidir**. Ordens de grandeza saudáveis:
- **Reclamação de spam:** mantenha **abaixo de 0,1%**. A partir daí é emergência de reputação.
  (Gmail trata ~0,3% como linha vermelha dura.)
- **Bounce:** **abaixo de ~2%**. Acima disso, higiene urgente.
- **Descadastro:** até ~**0,5%** é normal; acima sinaliza fadiga ou lista mal segmentada.
- **Abertura:** varia muito (o Apple Mail infla artificialmente desde o MPP). Use como
  **direção**, não verdade absoluta. Compare consigo mesmo ao longo do tempo, não com "a média".
- **Clique:** o sinal mais honesto de interesse real.

## Cair no "Promoções" do Gmail
Não é o fim do mundo (é onde muita compra acontece), mas para sair de lá: menos imagens e
mais texto, um CTA só, evitar cara de anúncio, incentivar resposta e marcação como importante.

## Falha silenciosa (o risco que ninguém vê)
O pior cenário é um fluxo automático que **parou de disparar** e você só descobre semanas
depois. O Painel não avisa sozinho — **revise seus fluxos no ESP toda semana**: algum
parou? algum está com erro? alguma métrica despencou?

## Consentimento e lei (LGPD, no Brasil)
- Base legal para marketing: consentimento (a pessoa pediu para receber).
- Todo e-mail: identificação de quem envia, **endereço físico** e **descadastro em 1 clique**.
- Respeite o descadastro imediatamente. É lei e é a coisa certa.
- Dado sensível (saúde, por exemplo) tem proteção reforçada — nunca em e-mail marketing.
