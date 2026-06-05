# Fase 3 — Derivação da Arquitetura Python
*Pipeline: Fase 1 → Fase 2 → **FASE 3** → Fase 4*
*Entrada: Grafo Enriquecido L2 (Gate 2 aprovado) — não retornar aos artefatos brutos (R4)*

---

## Carregue

```
references/architecture.md               → prompts 3.1, 3.2
references/pseudoalgorithm-generator.md  → prompts 3.3-A, 3.3-B, 3.3-C, 3.3-D
Arquivo de domínio ativo                 → tabela de notação (usar em 3.3)
```

---

## Modo de Preparo

**3.1 — Identificação de padrões estruturais**
Seguir `references/architecture.md` prompt 3.1.
Aplicar padrões P1–P9 com evidência do grafo enriquecido.
Para cada padrão encontrado: nós envolvidos, evidência de métrica, tradução Python prescrita.

**3.2 — Derivação de assinaturas de funções**
Seguir `references/architecture.md` prompt 3.2.
Para cada nó CRÍTICO/AGREGADOR/OUTPUT → derivar nome, args com tipos, retorno, docstring, validações.
Derivar função de ponto de entrada principal com todos os INPUTs e retorno como dict nomeado.

**3.3 — Geração de pseudoalgoritmo**
Seguir `references/pseudoalgorithm-generator.md` em ordem:
- 3.3-A → pseudoalgoritmo alto nível (10–20 linhas, sem corpos de subfunções, audiência executiva)
- 3.3-B → pseudoalgoritmo detalhado + blocos de subfunção (com referências de célula Excel)
- 3.3-C → tabela de referência de notação (todos os símbolos definidos)
- 3.3-D → gate de validação cruzada (consistência entre fases)

---

## Verificação — Gate 3

```
[ ] Todos os padrões P1–P9 avaliados e identificados com evidência de grafo
[ ] Todas as assinaturas de funções derivadas com tipos corretos do grafo enriquecido
[ ] 3.3-A: pseudoalgoritmo alto nível produzido e validado
[ ] 3.3-B: pseudoalgoritmo detalhado + subfunções produzido e validado
[ ] 3.3-C: tabela de notação produzida
[ ] 3.3-D: todos os checks de validação aprovados — sem sintaxe Python, todos os nós cobertos
[ ] Nenhum bloqueador aberto
[ ] STATUS = COMPLETO → carregar references/phases/phase4.md e iniciar Fase 4
```

> **GATE FAIL** → aplicar Protocolo de Bloqueio (SKILL.md) antes de avançar.
