# Primeira execução da Ponte (assistente de configuração)

> Você (Claude) está lendo isto porque a pasta `.ponte/` ainda não existe. Conduza esta conversa em PT-BR,
> de forma leve e sem jargão. NÃO peça nada técnico. Ao final, grave os arquivos e **apague a pasta `setup/`**.

## Como conduzir

Faça as perguntas abaixo **uma de cada vez**, em linguagem simples. Aceite respostas curtas. Se o dono não
souber ou não quiser responder algo opcional, use o padrão indicado e siga em frente — nunca trave.

### Perguntas

1. **Para qual idioma e mercado você quer levar seu material?**
   Exemplos: inglês (Estados Unidos), inglês (Reino Unido), espanhol (América Latina), espanhol (Espanha),
   português (Portugal), francês, alemão, italiano.
   → guarde `idioma_alvo` (ex.: "en") e `mercado_alvo` (ex.: "Estados Unidos").

2. **Qual é o nome da sua marca e do seu produto/serviço?** (esses nomes NÃO serão traduzidos)
   → guarde em `nao_traduzir` (lista). Se ele citar siglas ou termos técnicos que devem ficar no original,
   adicione também.

3. **Como você quer soar nesse idioma?** Escolha um tom:
   (a) Conversacional e próximo · (b) Formal e sóbrio · (c) Técnico e direto · (d) Marketing e vibrante.
   → guarde `tom` (padrão: "conversacional").

4. **Você trata seu cliente por "você" (informal) ou por uma forma mais formal?**
   Em inglês quase sempre é o mesmo "you"; em espanhol muda (tú × usted); em alemão/francês também (du/Sie, tu/vous).
   → guarde `tratamento` (padrão: "informal" para inglês; pergunte se o idioma tiver distinção).

5. **Sua moeda hoje é o Real (R$). Qual será a moeda no mercado-alvo?** (US$, €, £, etc.)
   → guarde `moeda_origem` ("BRL") e `moeda_destino` (ex.: "USD"). A Ponte nunca chuta câmbio — ela marca o valor
   para você confirmar.

6. **Você atua em alguma área regulada?** Saúde, jurídico, financeiro/fiscal, ou nenhuma.
   → guarde `area_regulada` (lista; padrão: vazia). Se marcar alguma, a Ponte passa a avisar
   `⚠️ REVISÃO PROFISSIONAL LOCAL` nas alegações desse tipo.

7. **(Opcional) Cite 1 ou 2 concorrentes que já atuam nesse mercado-alvo.** Ajuda no modo Mercado.
   → guarde `concorrentes_alvo` (lista; pode ficar vazia).

### Gravação

Depois de coletar as respostas, crie a pasta `.ponte/` e grave os dois arquivos. Você pode fazer isso rodando o
script (recomendado) ou escrevendo os JSON à mão.

**Opção recomendada — pelo script.** Rode **a partir da raiz do projeto do dono** (a pasta onde está o material
dele), apontando o caminho até o script — assim `.ponte/` é criada na raiz do projeto, e NÃO dentro da skill.
Ajuste o caminho ao local onde a skill está instalada (ex.: `.claude/skills/Ponte/`):

```bash
python3 .claude/skills/Ponte/scripts/ponte.py init \
  --idioma "<idioma_alvo>" --mercado "<mercado_alvo>" \
  --tom "<tom>" --tratamento "<tratamento>" \
  --moeda-origem "BRL" --moeda-destino "<moeda_destino>" \
  --marca "<Nome da Marca>" --produto "<Nome do Produto>" \
  --regulada "<área ou vazio>"
```

Isso cria `.ponte/config.json` e semeia `.ponte/glossario.json` com a voz da marca e a lista "não-traduzir".
Se o dono citou concorrentes, adicione-os depois com `python3 .claude/skills/Ponte/scripts/ponte.py set-concorrentes "A" "B"` (a partir da raiz do projeto).

**Se o script não estiver disponível por qualquer motivo**, crie você mesmo `.ponte/config.json` e
`.ponte/glossario.json` com a mesma estrutura descrita no README, e a pasta `.ponte/trabalhos/`.

### Confirmação e autodestruição

1. Rode `python3 .claude/skills/Ponte/scripts/ponte.py ver` (a partir da raiz do projeto) e mostre ao dono, em PT-BR, o resumo do que foi gravado (idioma, tom,
   moeda, marca, área regulada).
2. Explique em uma frase o que ele pode pedir a partir de agora (ex.: "Agora é só me mandar uma página, e-mail
   ou anúncio e dizer 'transcria isso'.").
3. **Apague a pasta de setup** para deixar a skill limpa. Use o caminho completo até a pasta `setup/` DENTRO da
   skill (não um `setup` solto na raiz do projeto) — ajuste ao local onde a skill está instalada:
   ```bash
   rm -rf .claude/skills/Ponte/setup
   ```
   (Só a pasta `setup/` da skill. NÃO apague `scripts/`, `references/`, `SKILL.md` nem `.ponte/`.)

Pronto. Da próxima vez, como `.ponte/` já existe, a Ponte pula direto para o modo pedido.
