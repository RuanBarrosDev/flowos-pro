# Guia dos "nós" — como explicar cada bagunça sem assustar

Cada tipo de nó que o motor acha vem com uma gravidade. Explique em linguagem de gente,
diga por que importa, e o que dá pra fazer — sem drama e sem jargão. Nunca exponha o valor
de um segredo.

---

## 🔴 segredo-no-codigo (gravidade ALTA — é fato)
**O que é:** uma chave de API ou senha escrita direto dentro de um arquivo de código.
**Por que importa:** quem abrir esse arquivo (ou o repositório no GitHub) vê a senha. É o
erro nº 1 de quem constrói com IA.
**Como falar:** "Achei uma chave/senha escrita dentro do arquivo `X`, na linha Y (te mostro
mascarada, nunca o valor real). Isso é arriscado. No plano a gente move ela pra um lugar
seguro (um arquivo `.env` que não vai pro GitHub) e troca por uma chave nova."
**NUNCA** escreva o valor real da chave em lugar nenhum.

## 🔴 env-versionado (gravidade ALTA — é fato)
**O que é:** o arquivo `.env` (onde ficam os segredos) foi enviado pro Git/GitHub.
**Por que importa:** mesmo apagando depois, ele fica no histórico — o segredo pode já ter
vazado.
**Como falar:** "Seu arquivo de segredos foi parar no controle de versão. Vamos tirá-lo de
lá e trocar as chaves que estavam nele, por garantia."

## 🟡 arquivo-gigante (gravidade MÉDIA — é fato)
**O que é:** um arquivo com centenas de linhas fazendo coisa demais.
**Por que importa:** é onde a IA (e você) mais se perde e mais quebra coisa ao mexer.
**Como falar:** "O arquivo `X` está enorme, faz muita coisa junto. Não é urgente, mas quando
a gente dividir ele em pedaços por assunto, tudo fica mais fácil de mexer sem quebrar."

## 🟡 possivel-duplicacao (gravidade MÉDIA — possível, confirme)
**O que é:** dois arquivos com muitas linhas iguais — provavelmente a mesma lógica copiada.
**Por que importa:** quando você muda um, esquece do outro, e aí "conserta num lugar e
quebra no outro".
**Como falar:** "Parece que essa mesma lógica está repetida em `A` e `B`. Vale confirmar; se
for isso mesmo, a gente deixa só uma versão boa e faz os dois lados usarem ela."

## ⚪ possivel-codigo-morto (gravidade BAIXA — possível, confirme)
**O que é:** um arquivo que ninguém parece usar (nenhum outro arquivo o chama).
**Por que importa:** é peso morto que só confunde. Mas "parece" não é "é" — pode ser usado de
um jeito que a busca automática não pega.
**Como falar:** "Esse arquivo aqui não parece ser usado por ninguém. Pode ser sobra. Antes de
apagar, a gente confirma — e se apagar e faltar, volta num clique."
**Sempre confirme abrindo** antes de sugerir apagar. Um de cada vez.

## ⚪ arquivo-misterio (gravidade BAIXA — possível, confirme)
**O que é:** arquivo com nome genérico (`old`, `copy`, `temp`, `v2`, `final`, `teste1`) ou
quase vazio.
**Por que importa:** costuma ser rascunho/sobra esquecida que polui o projeto.
**Como falar:** "Tem uns arquivos com cara de rascunho (`temp_old.py`, `helpers_copy.py`).
Vamos abrir rapidinho: se não servem mais, some com eles; se servem, damos um nome claro."

## ⚪ sem-teste (gravidade BAIXA, mas importante — é fato)
**O que é:** o projeto não tem nenhum teste automático.
**Por que importa:** sem teste, você não tem como saber se uma arrumação quebrou algo — é
mexer no escuro.
**Como falar:** "Seu projeto não tem uma 'rede de segurança' (teste automático). Antes de
arrumar coisa pesada, vale criar um teste bem simples que só confere se o projeto abre e a
tela principal responde. Aí a gente mexe com tranquilidade."

---

## Regra transversal
- **Fato x suspeita:** segredo, `.env` versionado, arquivo gigante e falta de teste são
  fatos. Código morto, duplicação e mistério são **suspeitas** ("possível — confirme"):
  sempre abra e confirme com o dono antes de agir.
- **Nunca** transforme uma suspeita em acusação ("seu código está cheio de lixo"). Enquadre
  como "vamos confirmar juntos e limpar com cuidado".
- O objetivo não é envergonhar — é **devolver ao dono o controle do próprio projeto**.
