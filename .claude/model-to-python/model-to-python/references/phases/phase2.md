# Fase 2 — Enriquecimento do Grafo
*Pipeline: Fase 1 → **FASE 2** → Fase 3 → Fase 4*
*Entrada: Planilha de Inventário Consolidado (Gate 1 aprovado)*

---

## Carregue

```
references/inventory-reconciliation.md  → seção "Graph Construction — Phase 2.1"  (prompts 2.1-A/B/C)
                                           seção "Graph Metrics — Phase 2.2"       (prompts 2.2-A/B/C)
                                           seção "Graph Enrichment — Phase 2.3"    (prompt 2.3)
```

*(Se inventory-reconciliation.md já estava em contexto pelo Bloco C da Fase 1, não é necessário recarregar.)*

---

## Modo de Preparo

**2.1 — Construção do grafo de dependências**
Seguir `references/inventory-reconciliation.md` seção "Graph Construction — Phase 2.1" prompts 2.1-A → 2.1-C:
Nível célula L1 → Nível named range L2 → Nível aba L3
**Trabalhar com L2 em todas as fases subsequentes.**

**2.2 — Cálculo de métricas de grafo**
Seguir `references/inventory-reconciliation.md` seção "Graph Metrics — Phase 2.2" prompts 2.2-A → 2.2-C:
In-degree, out-degree, betweenness, ordenação topológica, detecção de ciclos

**2.3 — Enriquecimento de nós**
Seguir `references/inventory-reconciliation.md` seção "Graph Enrichment — Phase 2.3" prompt 2.3:
Para cada nó L2: anexar tipo, restrição, fórmula, interpretação de domínio,
risco de caso-borda proveniente do inventário da Fase 1.

---

## Verificação — Gate 2

```
[ ] Grafo construído nos níveis L1, L2, L3
[ ] Métricas calculadas para todos os nós L2
[ ] Todos os nós enriquecidos com metadados de inventário
[ ] Nenhum ciclo não resolvido
[ ] Planilha de Grafo Enriquecido preenchida
[ ] STATUS = COMPLETO → carregar references/phases/phase3.md e iniciar Fase 3
```

> **GATE FAIL** → aplicar Protocolo de Bloqueio (SKILL.md) antes de avançar.
