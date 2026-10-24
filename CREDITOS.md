# Créditos e licenças

## Núcleo
Os agentes do núcleo (`.claude/skills/`) e os guias em `_setup/` são do FlowOS Pro, por Ruan Barros.

## Pacotes
As skills e os agentes em `pacotes/` foram criados pela **Maestria Academy** (comunidade Maestros da IA) e são distribuídos sob a **licença MIT**, que permite usar, copiar, modificar e redistribuir, desde que o aviso de copyright e a licença acompanhem o material.

- Cada skill traz o seu arquivo `LICENSE` dentro da própria pasta.
- Os agentes Estaleiro e Claquete trazem a licença em `pacotes/software/LICENSE-estaleiro` e `pacotes/youtube/LICENSE-claquete`.

Alterações feitas no FlowOS Pro:
- pastas renomeadas sem acento (Âncora → `Ancora`, Cadência → `Cadencia` e assim por diante);
- Veredito: `read_verdict.py` e `serve_judge.py` corrigidos para Windows (lá, `os.kill(pid, 0)` encerra o processo em vez de só checar se ele existe);
- Alambique: a descrição no cabeçalho do `SKILL.md` virou bloco YAML (`>-`); o texto tinha dois-pontos e o Claude Code não carregava a skill;
- agentes Claquete: o caminho `referencias/` passou a apontar para `pacotes/youtube/referencias/`;
- setups do Estaleiro e da Claquete movidos para `pacotes/<pacote>/setup-<nome>/`.

Texto da licença MIT (o mesmo de cada `LICENSE`):

```
MIT License

Copyright (c) 2026 Maestria Academy

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```
