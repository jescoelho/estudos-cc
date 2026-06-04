---
name: model-to-python
description: >
  Derives structured, auditable Python from quantitative model artefacts
  (Excel .xlsx/.xlsm/.xls and/or Python .py) via four-phase pipeline:
  inventory, graph enrichment, architecture, translation and audit.
  Use whenever user uploads a model file and wants to generate Python from
  Excel, convert spreadsheet to code, document model logic, derive
  pseudoalgorithm, translate formulas to Python, audit model completeness,
  or map model dependencies. Covers all domains EXCEPT credit risk:
  market risk (VaR/ES/Greeks/PnL/stress/FRTB), product pricing (loans,
  mortgages, leasing, FX), ALM (duration gap, NII, EVE, NMD), insurance
  (premium, severity, reserving), profitability/FTP/spread, and behavioural
  scoring/propensity. Always trigger for .xlsx, .xlsm, .xls, or .py model
  files even when the request is phrased casually.
compatibility: "claude.ai, Claude Desktop, Cowork — requires bash_tool for file reading"
---

# Model-to-Python Skill

Derives structured, auditable Python from any quantitative model artefact
(Excel and/or Python), using inventory + graph analysis + architecture + audit.

**Excluded domain:** credit risk models (PD/LGD/EAD/ECL/IFRS9 scoring).

---

## EXECUTION ORDER — MANDATORY

```
Phase 1 → Phase 2 → Phase 3 → Phase 4
Each phase requires the previous phase output to be COMPLETE before starting.
Blockers anywhere halt the full pipeline — escalate to user before proceeding.
```

---

## GLOBAL RULES

```
R1 — Every decision cites its evidence
     Structural: cite graph metric | Semantic: cite inventory field

R2 — Missing information → "NOT FOUND" — never omit, never infer silently
     Inferences must be tagged [INFERENCE]

R3 — Cycle in graph = BLOCKER — do not generate code until resolved

R4 — The enriched graph (Phase 2 output) is the single source of truth
     for Phases 3 and 4 — never return to raw artefacts after Phase 2
```

---

## PHASE 1 — TECHNICAL INVENTORY

Read the domain reference BEFORE starting inventory:

```
Step 1a: Identify likely domain from filename, imports (if .py visible),
         or user context.
Step 1b: Read the corresponding domain reference:
         references/domains/market-risk.md
         references/domains/product-pricing.md
         references/domains/alm.md
         references/domains/insurance.md
         references/domains/profitability.md
         references/domains/scoring-behavioural.md
         references/domains/generic.md   ← use if domain unclear
Step 1c: Proceed with inventory using domain-specific signal tables.
```

### BLOCK A — PYTHON INVENTORY

Follow all prompts in `references/inventory-python.md` in order:
A.1 Physical recognition → A.2 Dependency map → A.3 Function structure map →
A.4 Entry point → A.5 Input/parameter/output separation → A.6 Exception cases

### BLOCK B — EXCEL INVENTORY

Follow all prompts in `references/inventory-excel.md` in order:
B.1 Physical recognition of workbook → B.2 Tab classification →
B.3 Named ranges → B.4 Key formulas → B.5 Inter-tab dependencies →
B.6 VBA/macros detection

### BLOCK C — RECONCILIATION (both artefacts only)

Follow prompts in `references/inventory-reconciliation.md`:
C.1 Input reconciliation → C.2 Output reconciliation → C.3 Primary source

### INVENTORY COMPLETION GATE

```
[ ] All applicable blocks executed
[ ] Inventory Consolidated Sheet filled (see references/inventory-python.md)
[ ] No blank fields — all gaps marked NOT FOUND
[ ] No open blockers
[ ] STATUS = COMPLETE
```

---

## PHASE 2 — GRAPH ENRICHMENT

### 2.1 Build dependency graph
Read `references/graph-construction.md` → prompts 2.1-A through 2.1-C
(cell-level L1 → named-range level L2 → tab level L3)
**Work with L2 in all subsequent phases.**

### 2.2 Compute graph metrics
Read `references/graph-metrics.md` → prompts 2.2-A through 2.2-C
(in-degree, out-degree, betweenness, topological sort, cycle detection)

### 2.3 Enrich nodes with inventory metadata
Read `references/graph-enrichment.md` → prompt 2.3
For each node: attach type, restriction, formula, domain interpretation,
edge-case risk from Phase 1 inventory.

### GRAPH COMPLETION GATE

```
[ ] Graph built at L1, L2, L3
[ ] Metrics computed for all L2 nodes
[ ] All nodes enriched with inventory metadata
[ ] No unresolved cycles
[ ] Enriched Graph Sheet filled
[ ] STATUS = COMPLETE
```

---

## PHASE 3 — PYTHON ARCHITECTURE DERIVATION

Read `references/architecture.md` for full prompts.

### 3.1 Structural pattern identification
Apply patterns P1–P9 (P7–P9 are domain-specific additions):
P1 Linear pipeline | P2 Central hub | P3 Aggregator | P4 Parallel components |
P5 Cycle | P6 Isolated node | P7 Decision tree | P8 Lookup pricing table |
P9 Projected cash flow loop

### 3.2 Function signature derivation
For each CRITICAL/AGGREGATOR/OUTPUT node → derive name, args, return, docstring,
entry validations. Derive main entry-point function.

### ARCHITECTURE COMPLETION GATE

```
[ ] All patterns identified and cited with graph evidence
[ ] All function signatures derived with correct types from enriched graph
[ ] No unresolved blockers
[ ] STATUS = COMPLETE
```

---

## PHASE 4 — TRANSLATION AND AUDIT

### 4.1 Formula translation
Read `references/formula-translation.md` → domain-aware translation rules.
Apply types from enriched graph. Add edge-case treatments from A.6.

### 4.2 Function body assembly
Follow ordering: validations → topological order → inline comments
with Excel cell references → edge-case handlers → return.

### 4.3 Completeness audit
Verify 100% of L2 graph nodes covered in generated code.

### 4.4 Execution order audit
Verify topological ordering respected in every function.

### 4.5 Architecture audit
Verify coupling, cohesion, length, global variables, traceability, edge coverage.

### PHASE 4 COMPLETION GATE

```
[ ] All formulas translated at correct type
[ ] All edge cases treated (A.6 covered + new ones added)
[ ] Audits 4.3, 4.4, 4.5 pass with no blockers
[ ] Derivation Consolidated Sheet filled
[ ] STATUS = COMPLETE
```

---

## DELIVERABLES

```
Primary  : <model_name>.py — complete structured Python
Secondary: derivation_sheet.md — filled consolidated sheet
Optional : graph_L2.md — enriched graph if user requests
```

---

## REFERENCE FILES

| File | Read when |
|------|-----------|
| `references/domains/market-risk.md` | Domain = market risk |
| `references/domains/product-pricing.md` | Domain = product pricing |
| `references/domains/alm.md` | Domain = ALM / balance sheet |
| `references/domains/insurance.md` | Domain = insurance |
| `references/domains/profitability.md` | Domain = profitability / FTP |
| `references/domains/scoring-behavioural.md` | Domain = propensity / scoring |
| `references/domains/generic.md` | Domain unclear or mixed |
| `references/inventory-python.md` | Phase 1 Block A |
| `references/inventory-excel.md` | Phase 1 Blocks B (B.1–B.6) |
| `references/inventory-reconciliation.md` | Phase 1 Block C |
| `references/graph-construction.md` | Phase 2.1 |
| `references/graph-metrics.md` | Phase 2.2 |
| `references/graph-enrichment.md` | Phase 2.3 |
| `references/architecture.md` | Phase 3 |
| `references/formula-translation.md` | Phase 4.1 |
