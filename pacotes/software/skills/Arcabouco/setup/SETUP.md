# Configuração de primeira execução do Arcabouço

Você (Claude) está rodando o Arcabouço pela **primeira vez** neste projeto.
Antes de modelar qualquer coisa, faça esta configuração rápida com o dono —
uma vez só. No fim, esta pasta `setup/` se apaga sozinha.

## O que perguntar (uma pergunta de cada vez, em português)

1. **Nome do projeto/sistema** — "Que nome dou para este sistema?"
   (ex.: "Agenda da Clínica", "CRM da consultoria"). Vira o campo `projeto`.

2. **Qual banco de dados você vai usar?** Explique simples e ofereça:
   - **SQLite** (recomendado para começar) — um arquivo só, sem instalar nada.
   - **PostgreSQL** — o profissional, para quando cresce.
   - **MySQL** — para hospedagem comum / ambiente que já é MySQL.
   Se a pessoa não souber, escolha **SQLite**. Vira o campo `engine`.

3. **Seu nível com banco de dados** — "Você já mexe com banco de dados ou
   prefere que eu explique tudo em português, sem termos técnicos?"
   - `tecnico` — pode usar termos (chave estrangeira, normalização, DDL).
   - `simples` — traduzir todo jargão, falar só em "coisas, informações e
     ligações". (Padrão se não souber.)

## O que gravar

Crie a pasta `.arcabouco/` na raiz do projeto e escreva **dois** arquivos:

### `.arcabouco/config.md`
```md
# Configuração do Arcabouço
- Projeto: <nome>
- Banco (engine): <sqlite|postgres|mysql>
- Nível: <tecnico|simples>
- Configurado em: <data de hoje>
```

### `.arcabouco/modelo.json` (modelo vazio, pronto para receber tabelas)
```json
{
  "projeto": "<nome do projeto>",
  "engine": "<sqlite|postgres|mysql>",
  "tabelas": []
}
```

Use o `engine` escolhido nos dois arquivos.

## Autodestruição (obrigatório)

Depois de gravar os dois arquivos, **remova a pasta de setup** para que a skill
instalada fique limpa:

```bash
rm -rf setup
```

E na SKILL.md, se o bloco "> **Primeiro uso:** ..." atrapalhar, pode ignorá-lo —
ele só existe para acionar este setup, que agora já rodou.

## Depois do setup

Confirme para o dono em uma frase que está tudo pronto e ofereça começar:
"Pronto! Me conta em palavras o que seu sistema precisa guardar (clientes,
pedidos, agendamentos…) que eu desenho a estrutura." — e siga para o modo
`modelar` da SKILL.md.
