# Fase 4 — Planejamento (EAP / WBS)

Framework: EAP (Estrutura Analítica de Projeto) — equivalente em português do WBS (Work Breakdown Structure).
Fase obrigatória — não é pulável, mesmo quando o objetivo inicial era só diagnóstico. Sempre roda com pelo menos o Gap da Fase 1.2; PRR (2.1) e RAID (2.2) enriquecem quando disponíveis.
Depende de: Gap da Fase 1.2 (obrigatório); checklist PRR (2.1) e RAID log (2.2) idealmente. Fase 3 é opcional — se executada, pode informar prioridade, mas não altera a ordem técnica.

Regra: todo pacote de trabalho deve ser rastreável a um item do Gap (1.2), do PRR (2.1) ou do RAID (2.2) já levantado. Nenhuma tarefa nova é inventada nesta fase — ela decompõe e sequencia o que as fases anteriores já identificaram.

## 4.1 — Decompor e sequenciar em EAP

```
Com base no Gap (Fase 1.2) e, se disponíveis, no checklist PRR (2.1) e no
RAID log (2.2) — e, se disponível, na prioridade indicada pelo Business
Case (3.1) — produza uma EAP (Estrutura Analítica de Projeto) do trabalho
restante:

1. Decomponha cada item do Gap ("o que falta") em pacotes de trabalho
   concretos e executáveis. Um pacote não deve depender de uma decisão
   externa ainda não tomada — se depender, isso é uma entrada do RAID
   (Dependency), não um pacote de trabalho
2. Numere no formato EAP hierárquico (1, 1.1, 1.2, 2, 2.1...), agrupando
   pacotes relacionados sob o mesmo item de primeiro nível
3. Ordene os pacotes por dependência técnica (o que precisa ser feito antes
   do quê) — não por prioridade de negócio nem por familiaridade
4. Para cada pacote, indique: origem (qual item do Gap/PRR/RAID ele
   resolve), pré-requisitos (quais outros pacotes precisam estar prontos
   antes), critério de conclusão (como confirmar que o pacote terminou)
5. Marque explicitamente pacotes bloqueados por um item do RAID (Risk,
   Assumption não validada, Dependency externa) — não sequencie um pacote
   bloqueado como se pudesse começar imediatamente
6. Não estime prazo ou esforço a menos que a demanda (Fase 1.1) tenha
   fornecido informação explícita sobre isso — ausência de estimativa é
   preferível a estimativa inventada

Não decomponha em nível de linha de código ou função — o nível de detalhe é
de "tarefa que alguém pode assumir e executar", não de implementação.

Se a Fase 2 não foi executada, preencha pré-requisitos e a coluna "Bloqueado
por (RAID)?" apenas com o que for inferível diretamente do Gap, e marque
explicitamente como "não disponível — Fase 2 não executada" em vez de
inventar ou deixar em branco.

Se algum item do Gap/PRR/RAID não gerar pacote correspondente, informe isso
explicitamente — pode indicar que já está coberto por outro pacote, ou que
ficou sem tratamento.

Organize como tabela: [# EAP | Pacote de trabalho | Origem | Pré-requisitos
| Critério de conclusão | Bloqueado por (RAID)?]
```

## Critério de qualidade

- Todo pacote rastreia a um item concreto do Gap/PRR/RAID — nenhuma tarefa "genérica de boas práticas"
- EAP é executável sem retrabalho de sequenciamento — cada pacote tem pré-requisito e critério de conclusão explícitos
- Pacotes bloqueados por RAID nunca aparecem como prontos para início
- Sem estimativa de prazo/esforço inventada — só se a fonte da demanda informou
