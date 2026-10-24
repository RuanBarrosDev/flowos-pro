# Ensaio — a rede de segurança do seu app

Você construiu um app, site ou sistema com IA e ele **funciona**. O medo agora é o seguinte:
você mexe numa coisa e, sem perceber, quebra outra que estava funcionando — e só descobre quando
o cliente reclama.

O **Ensaio** resolve isso. Ele faz o "ensaio geral" antes de cada estreia: escreve testes que
provam que as partes importantes do seu app funcionam, roda esses testes toda vez que você muda
algo, e te avisa **em português claro** se alguma coisa quebrou — **antes** do seu usuário ver.

> Você nunca escreve um teste. Você nunca precisa ler código. Você conversa; o Claude monta a
> rede, roda e te dá o veredito.

---

## O que ele faz por você

- **Descobre o que é crítico** no seu app (entrar na conta, pagar, salvar dados, o cálculo que
  vira dinheiro) e protege isso primeiro.
- **Monta a rede de testes** do zero, mesmo que seu projeto não tenha nenhum teste hoje.
- **Confere a cada mudança:** antes de publicar, você pede "roda o ensaio" e ele diz se pode subir
  com segurança ou o que quebrou.
- **Fala a sua língua:** em vez de "test_checkout falhou", ele diz *"o cálculo do frete parou de
  somar o imposto — não suba assim"*.
- **Não te engana:** um teste que passa mesmo com o app quebrado é lixo. O Ensaio prova que cada
  teste é capaz de falhar antes de confiar nele.

---

## Como instalar (uma vez)

1. Baixe o arquivo `Ensaio.zip` e **descompacte**.
2. Coloque a pasta `Ensaio` dentro da pasta de skills do seu Claude Code:
   - só para um projeto: `.claude/skills/Ensaio` dentro do projeto; ou
   - para todos os seus projetos: `~/.claude/skills/Ensaio`.
3. Abra o Claude Code no seu projeto. Pronto — o Ensaio já está disponível.

## Como usar (você só conversa)

**Primeira conversa** — deixe ele se preparar:
> "Prepara o Ensaio no meu projeto."

Ele descobre com que tecnologia seu app foi feito, se já tem testes e como rodar, e guarda isso
numa memória local. (Pode fazer uma ou duas perguntas simples, como "qual parte do seu app não
pode quebrar de jeito nenhum?".)

**Depois, use os cinco modos falando naturalmente:**

| Você quer... | Fale algo como... |
|---|---|
| Saber se seu app está protegido | *"Meu app tem teste? Presta pra alguma coisa?"* |
| Criar a rede de proteção | *"Cria a rede de segurança do meu app."* |
| Conferir antes de publicar | *"Mexi numa coisa, roda o ensaio e vê se quebrou algo."* |
| Proteger algo que acabou de criar | *"Acabei de fazer a tela de cadastro, cobre ela."* |
| Consertar testes chatos/lentos | *"Meus testes falham à toa, dá uma faxina."* |

---

## O que esperar (as garantias)

- **Um teste que nunca falha é lixo.** Todo teste é provado capaz de falhar antes de entrar na
  rede — senão ele daria uma falsa sensação de segurança.
- **Nunca inventa "passou".** Ele só diz que passou depois de rodar de verdade, com o resultado à
  vista.
- **Testa o que dói.** Foca no que, se quebrar, vira prejuízo ou vergonha — não em encher de teste
  bonitinho o que não importa.
- **Seus testes ficam no seu projeto.** Nada sai da sua máquina; nenhuma senha ou dado é enviado
  para lugar nenhum.
- **O seu projeto manda.** Se você já tem um jeito de fazer as coisas, o Ensaio segue o seu jeito.

---

*Feito para a comunidade Maestros da IA. Skill para Claude Code.*
