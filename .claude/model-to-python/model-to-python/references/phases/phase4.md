# Fase 4 — Tradução e Auditoria
*Pipeline: Fase 1 → Fase 2 → Fase 3 → **FASE 4***
*Entrada: Assinaturas de funções + Pseudoalgoritmo (Gate 3 aprovado) — não retornar aos artefatos brutos (R4)*

---

## Carregue

```
references/formula-translation.md  → prompts 4.1, 4.2 e regras de tradução
```

---

## Modo de Preparo

**4.1 — Tradução de fórmulas**
Seguir `references/formula-translation.md` prompt 4.1.
Para cada nó que se torna função Python: traduzir fórmula Excel com tipos do grafo enriquecido.
Adicionar tratamentos de caso-borda de A.6. Registrar nível de confiança (ALTA / MÉDIA / BAIXA).

**4.2 — Montagem do corpo de função**
Seguir `references/formula-translation.md` prompt 4.2.
Ordem dentro de cada função: validações de entrada → ordem topológica → comentários inline
com referências de célula Excel → handlers de caso-borda → return.

**4.3 — Auditoria de completude**
Verificar que 100% dos nós L2 do grafo enriquecido estão cobertos no código gerado.

**4.4 — Auditoria de ordem de execução**
Verificar que a ordenação topológica é respeitada em cada função.

**4.5 — Auditoria de arquitetura**
Verificar: acoplamento, coesão, comprimento de função, ausência de variáveis globais,
rastreabilidade e cobertura de casos-borda.

---

## Verificação — Gate 4

```
[ ] Todas as fórmulas traduzidas com tipo correto
[ ] Todos os casos-borda tratados (A.6 cobertos + novos adicionados e marcados)
[ ] Auditoria 4.3 aprovada — 100% dos nós L2 cobertos
[ ] Auditoria 4.4 aprovada — ordem topológica respeitada em todas as funções
[ ] Auditoria 4.5 aprovada — sem bloqueadores de arquitetura
[ ] Planilha de Derivação Consolidada preenchida
[ ] STATUS = COMPLETO → entregar todos os artefatos listados em SKILL.md
```

> **GATE FAIL** → aplicar Protocolo de Bloqueio (SKILL.md) e listar refatorações pendentes para o usuário.
