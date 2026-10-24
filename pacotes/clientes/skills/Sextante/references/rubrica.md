# Rubrica do Diagnóstico — 6 dimensões, 30 perguntas

Pontue cada pergunta **0 / 1 / 2**. Regra de calibração: se a resposta é "sim, mas…", a nota é **1**.

| Nota | Significa |
|:----:|-----------|
| **0** | Não existe, ou só como intenção/conversa. |
| **1** | Existe, mas é inconsistente, informal, restrito a uma pessoa/área ou recém-começado. |
| **2** | Documentado, praticado de forma consistente, dá para apontar uma prova concreta (planilha, política, fluxo rodando). |

Grave cada resposta com: `python3 scripts/sextante.py nota "<cliente>" <dimensao> <numero> <0|1|2> --obs "<observação opcional>"`

Faça a entrevista em linguagem simples — traduza cada pergunta para o mundo do cliente. **Nunca invente a resposta**: se o cliente não sabe, pergunte ou deixe em branco.

---

## estrategia — Estratégia & Liderança
1. Existe uma visão ou objetivo claro do que a empresa quer com IA, ligado às metas do negócio?
2. Já identificaram onde a IA poderia trazer mais retorno?
3. A liderança (dono/diretoria) apoia de verdade e patrocina o uso de IA?
4. Existe alguma meta/número para saber se a IA está dando resultado?
5. Há um plano realista, por etapas, para adotar IA aos poucos?

## dados — Dados & Organização da informação
6. A informação que a IA precisaria (clientes, histórico, preços) está acessível e organizada?
7. Os dados estão num lugar só, ou espalhados em cabeças, papéis e planilhas soltas?
8. Existe algum cuidado/rotina para manter os dados limpos e atualizados?
9. Privacidade e segurança dos dados de cliente são respeitadas?
10. Dá para exportar/consultar esses dados sem depender de uma única pessoa?

## processos — Processos
11. Os principais processos da empresa estão minimamente mapeados (quem faz o quê)?
12. As tarefas repetitivas são feitas sempre do mesmo jeito (padrão)?
13. Sabem o volume (quantas vezes por dia/semana) das tarefas mais pesadas?
14. Já existe algum processo apoiado por ferramenta/automação hoje?
15. Quando algo dá errado num processo, percebem e corrigem?

## pessoas — Pessoas & Cultura
16. A maioria da equipe entende o básico do que a IA faz e não faz?
17. As pessoas estão abertas (não com medo) a usar IA no dia a dia?
18. Existe alguém responsável por puxar o assunto IA dentro da empresa?
19. Há espaço/tempo para experimentar e aprender ferramentas novas?
20. A empresa investe (ou pretende) em treinar o time em IA?

## ferramentas — Ferramentas & Integração
21. As ferramentas atuais (CRM, planilha, sistema) atendem bem a operação?
22. Esses sistemas conseguem conversar/trocar dados entre si?
23. A empresa usa nuvem/ferramentas online que facilitam integrar IA?
24. Há orçamento previsto para ferramentas de IA quando fizer sentido?
25. Alguém consegue configurar/manter as ferramentas sem travar tudo?

## governanca — Governança & Confiança
26. Existe alguma regra de como usar IA com segurança (o que pode/não pode)?
27. Sabem que dado sensível não deve ir cru para uma IA pública?
28. Toda saída importante da IA passa por revisão humana antes de valer?
29. A empresa se preocupa com LGPD / uso ético dos dados?
30. Se a IA errar, existe um responsável e um caminho para corrigir?

---

### Como fechar o diagnóstico
- Depois de pontuar as dimensões, rode `python3 scripts/sextante.py relatorio "<cliente>"` para o resumo com estágio + elo mais fraco.
- **Portões de pré-requisito:** `dados` e `governanca` com nota baixa (< 5/10) travam recomendações agressivas — o motor avisa. Base ruim + automação = erro multiplicado.
