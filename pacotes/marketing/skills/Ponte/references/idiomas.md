# Convenções por idioma e mercado

Notas práticas por idioma/mercado-alvo. Sempre confirme a variante no `.ponte/config.json` e prefira o que o
público **realmente escreve**, não a regra de gramática de manual. Formato de moeda/data/número: cheque com
`scripts/formato.py --alvo <código>`.

## Inglês — Estados Unidos (en-US)
- Tratamento: "you" (único). Tom direto, orientado a benefício e ação.
- Títulos em **Title Case**. Data **MM/DD/YYYY**. Número: milhar `,` decimal `.` (1,000.50). Moeda **US$** antes do valor ($49).
- Unidades: **imperiais** (lb, mi, ft, °F) — converta kg/km/°C. Ortografia: color, organize, center (sem "u", com "z").
- Evite regionalismos e gírias BR traduzidas ao pé da letra. CTA curto e imperativo ("Get started", "Book a call").

## Inglês — Reino Unido (en-GB)
- "you". Tom um pouco mais reservado/educado que o americano. Ortografia **britânica**: colour, organise, centre.
- Data **DD/MM/YYYY**. Moeda **£**. Unidades mistas (kg no varejo, mas milhas e °C).

## Espanhol — América Latina (es-419)
- **tú** informal ou **usted** formal — confira o `tratamento` no config; no marketing costuma ser "tú".
- Evite espanhol "neutro" artificial; ajuste ao país específico se souber (MX/AR/CO mudam gíria e moeda).
- Data DD/MM/YYYY. Número: milhar `,` decimal `.` na maior parte (mas confira o país). Moeda: **defina** (MXN, ARS, COP, US$...).

## Espanhol — Espanha (es-ES)
- **tú** informal (marketing) ou **usted**. **vosotros** existe (não use "ustedes" para o plural informal como na América Latina).
- Data DD/MM/YYYY. Número: milhar `.` decimal `,` (1.000,50). Moeda **€** depois do valor (49 €).

## Português — Portugal (pt-PT)
- Mesma língua, mercado diferente: ortografia e vocabulário mudam (ex.: "utilizador" não "usuário"; "telemóvel"
  não "celular"; "casa de banho" não "banheiro"; "ecrã" não "tela"; "gestão de" formas). Trate por **você/tu** conforme o config.
- Data DD/MM/YYYY. Número: milhar `.` decimal `,`. Moeda **€**. Evite brasileirismos e o gerúndio à brasileira ("estou a fazer", não "estou fazendo").

## Francês (fr-FR)
- Registro **vous** (padrão para produtos/serviços). Tipografia francesa: espaço fino **antes** de `:` `;` `!` `?`.
- Data DD/MM/YYYY. Número: milhar espaço, decimal `,` (1 000,50). Moeda **€** depois do valor (49 €).

## Alemão (de-DE)
- **Sie** (formal) por padrão; **du** só se a marca for jovem/informal (confirme). Substantivos capitalizados.
- Compostos ficam longos — cuidado com o teto de 150% em rótulos. Data DD.MM.YYYY. Número: milhar `.` decimal `,`. Moeda **€**.

## Italiano (it-IT)
- **tu** informal (marketing) ou **Lei** formal. Data DD/MM/YYYY. Número: milhar `.` decimal `,`. Moeda **€** depois do valor.

## Regras que valem para todos
- **Não-traduzir**: nomes de marca, produto e siglas do glossário ficam no original em qualquer idioma.
- **Nomes próprios**: pessoas, empresas e lugares mantêm a grafia oficial (confirme com WebSearch quando houver dúvida).
- **SEO no idioma-alvo**: a palavra-chave certa é a que o público de lá busca, não a tradução literal da sua keyword BR.
- **Uma decisão, sempre igual**: registrou um termo no glossário? Repita idêntico em toda peça daquele idioma.
