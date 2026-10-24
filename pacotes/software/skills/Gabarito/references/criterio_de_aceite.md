# Critério de aceite: como saber que ficou pronto

Um requisito sem critério de aceite não pode ser entregue nem cobrado — ninguém
sabe dizer se está "pronto". "A tela tem que ser rápida" não é requisito: rápido
para quem? em quantos segundos? O Gabarito marca frases assim como **nebulosas** e
não deixa a especificação fechar até virarem algo conferível.

## O que é um bom critério de aceite
Uma condição **observável e testável** — dá para alguém checar e responder sim/não.

Duas formas úteis:

**1. Dado / Quando / Então** (bom para comportamento)
> Dado que existe uma consulta amanhã, Quando faltam 24 horas, Então o sistema
> envia exatamente 1 mensagem de lembrete ao paciente.

**2. Lista de condições** (bom para regras e telas)
> - A busca retorna resultados em até 2 segundos com 10 mil registros.
> - O cliente recebe e-mail de confirmação em até 1 minuto após pagar.
> - Só o dono e o gerente veem o relatório financeiro.

## Trocar o vago pelo conferível

| Vago (nebuloso) | Conferível (critério de aceite) |
|---|---|
| "rápido" | "carrega em menos de 2 segundos" |
| "fácil de usar" | "um usuário novo completa o cadastro em até 3 passos" |
| "seguro" | "senha guardada com criptografia; só o dono acessa dados financeiros" |
| "sempre no ar" | "fica disponível 99% do mês; se cair, avisa o dono" |
| "bonito" | "segue a paleta e a logo da marca X" (peça a referência) |

## Requisito não-funcional (qualidade)
Além do "o que faz", declare a qualidade quando importar:
- **Desempenho:** tempo de resposta, volume suportado.
- **Segurança / Privacidade:** quem acessa o quê, LGPD, dados sensíveis.
- **Confiabilidade / Disponibilidade:** o que não pode falhar, quanto pode ficar fora.
- **Compatibilidade:** celular, computador, navegador.

## Como preencher
```bash
python3 scripts/gabarito.py detalhar --id 1 \
  --criterio "Dado ..., Quando ..., Então ..." \
  --porque "traça ao problema CP.01" \
  --validar "como testar: ..."
```
Regra: se você não consegue escrever o critério, **você ainda não entende o
requisito** — volte a perguntar ao dono. Não invente um número para "fechar".
