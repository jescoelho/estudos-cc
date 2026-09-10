# laudo-tecnico

Plugin com uma única skill: **laudo-tecnico**.

## O que faz

Recebe uma demanda técnica em texto (transcrição de reunião, e-mail, ticket, briefing) e cruza com um repositório de código para produzir um diagnóstico estruturado, cobrindo quatro fases:

1. **Entendimento** — Gap Analysis (As-Is/To-Be) + C4 Model + gate de entrada (DoR)
2. **Execução** — Production Readiness Review (PRR) + RAID log
3. **Justificativa** — Business Case + TCO
4. **Planejamento** — EAP (WBS), sempre obrigatória

O artefato final é `laudo-tecnico-output/diagnostico-consolidado.md`, validado por um script (`scripts/validar_diagnostico.py`) antes de ser apresentado.

## Componentes

| Componente | Local | Descrição |
|---|---|---|
| Skill | `skills/laudo-tecnico/SKILL.md` | Skill principal — orquestra as 4 fases |
| Referências | `skills/laudo-tecnico/references/*.md` | Prompts detalhados de cada fase, incluindo setup do graphify |
| Script | `skills/laudo-tecnico/scripts/validar_diagnostico.py` | Gate de validação do diagnóstico consolidado |

## Pré-requisitos

- CLI **graphify** instalado e configurado ([github.com/Graphify-Labs/graphify](https://github.com/Graphify-Labs/graphify)) — obrigatório para qualquer análise de repositório
- Python 3 (recomendado) para rodar o script de validação

## Uso

A skill dispara quando o usuário fornece uma transcrição/demanda em texto junto com um repositório para analisar, diz que "herdou" um repositório, ou precisa levar um projeto de dev para produção e justificar valor/custo. Veja `skills/laudo-tecnico/SKILL.md` para o fluxo completo.
