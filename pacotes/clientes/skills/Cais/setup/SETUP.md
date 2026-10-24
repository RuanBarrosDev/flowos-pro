# Setup de primeira execução — Cais

Só rode isto **uma vez**, na primeira vez que o dono usa a Cais (quando ainda
**não existe** o arquivo `.cais/config.md`). Depois de concluído, esta pasta
`setup/` se apaga sozinha.

## O que fazer (você, a IA)

1. **Dê as boas-vindas em 1 linha** e explique que vai fazer 5 perguntas rápidas
   para personalizar as mensagens de onboarding. Faça **uma pergunta por vez**,
   em português simples:
   - **Qual o seu nome?** (como o cliente te chama)
   - **Qual o seu negócio?** (ex.: "Consultoria de RH", "Clínica odontológica")
   - **Qual o serviço principal que você entrega?** (ex.: agência/marketing, clínica/saúde,
     jurídico, contábil, consultoria/dev, design/conteúdo, ou descreva)
   - **Qual seu canal preferido para falar com cliente?** (WhatsApp, e-mail…)
   - **Em quanto tempo você costuma responder um cliente?** (ex.: "no mesmo dia",
     "até 1 dia útil") — e, se quiser, **qual o tom das suas mensagens?** (ex.:
     "próximo e descontraído", "formal e objetivo").

2. **Grave a configuração** rodando o script de setup (ele encontra a raiz do
   projeto sozinho, cria `.cais/`, escreve o `config.md`, garante `.cais/` no
   `.gitignore` e **apaga esta pasta setup/**). Use o caminho absoluto da própria
   skill — o script sabe se localizar:
   ```bash
   python3 "<caminho-da-skill>/setup/first_run.py" \
     --nome "<nome>" --negocio "<negócio>" --servico "<serviço>" \
     --canal "<canal>" --tom "<tom>" --resposta "<tempo de resposta>"
   ```
   (Ex.: se a skill está em `.claude/skills/cais/`, o caminho é
   `.claude/skills/cais/setup/first_run.py`.)

3. **Confirme** que apareceu "Configuração gravada" e "Pasta setup/ removida".
   A partir daqui, siga o `SKILL.md` normalmente — comece perguntando qual cliente
   o dono quer receber/onboarding (modo Receber) ou mostre o `painel` se já houver
   clientes.

> Se algo falhar na remoção da pasta setup/, apague-a manualmente — não é um erro
> grave. O que importa é o `.cais/config.md` ter sido criado.
