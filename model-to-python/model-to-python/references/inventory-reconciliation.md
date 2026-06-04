# Reconciliation — Phase 1 Block C

*Execute only when BOTH Python and Excel artefacts provided.*

## C.1 — Input Reconciliation

**Prompt:**
```
Compare Python inputs (Block A A.5) with Excel named ranges (Block B B.2).
For each item classify:
  [CONSISTENT]   → present and equivalent in both
  [PYTHON ONLY]  → Excel probably feeds Python
  [EXCEL ONLY]   → data not consumed by Python — investigate
  [DIVERGENT]    → same name, different type or scale → BLOCKER

Also reconcile hardcoded parameters:
  → Hardcoded values in Python (A.5) must match named ranges or
    fixed cells in Excel (B.2). Divergences recorded explicitly.

OUTPUT:
  Item | Python | Excel | Status
  Blockers: [list / NONE]
```

## C.2 — Output Reconciliation

**Prompt:**
```
Compare Python outputs (A.5) with Excel Output tabs (B.1 classification).
  → Both compute same value: Python = implementation, Excel = validation
  → Different values → BLOCKER: critical divergence

OUTPUT:
  Item | Python output | Excel output | Status
  Blockers: [list / NONE]
```

## C.3 — Primary Source Decision

**Prompt:**
```
Determine which artefact leads the Python derivation:
  → Python has explicit functions, Excel only visualises → SOURCE = Python
  → Excel has complex formulas, Python only reads/writes → SOURCE = Excel
  → Both have equivalent logic → SOURCE = Python (more traceable);
    Excel documented as parallel validation

Record decision and justification.

OUTPUT:
  Primary source: [Python / Excel] — reason:
```

---

# Graph Construction — Phase 2.1

## Prompt 2.1-A — Cell-Level Graph (L1)

**Prompt:**
```
You have the cell dependency list from B.5 (and B.3 formulas).

Build the complete cell-level directed graph:
  NODES: every unique cell that appears as origin or destination
  EDGES: ORIGIN → DESTINATION for every dependency

For named ranges: use the name as node identifier.
For unnamed cells: use TAB!COORDINATE format.
Expand all ranges to individual cells.

OUTPUT:
  NODES: [complete list]
  EDGES: [complete list ORIGIN → DESTINATION]
  INPUT NODES (no predecessors) : [list]
  OUTPUT NODES (no successors)  : [list]
```

## Prompt 2.1-B — Named Range Level Graph (L2)

**Prompt:**
```
Using the L1 graph and named ranges from B.2:

1. Replace cell references with named range names where available.
2. Group unnamed cells by tab: "TAB (intermediate cells)"
3. Record edge between named ranges when any path exists in L1.

WORK WITH L2 IN ALL SUBSEQUENT PHASES.

OUTPUT:
  NODES: [named ranges + tab groups]
  EDGES: [ORIGIN → DESTINATION with named ranges as nodes]
```

## Prompt 2.1-C — Tab Level Graph (L3)

**Prompt:**
```
Collapse all nodes of the same tab into a single node.
Record edge between Tab A and Tab B if any cell of B references any cell of A.

OUTPUT:
  NODES: [tab list]
  EDGES: [TAB_A → TAB_B]
  CALCULATION SEQUENCE: [topological order of tabs]
  CYCLES: [list / NONE]
```

---

# Graph Metrics — Phase 2.2

## Prompt 2.2-A — Degree and Betweenness

**Prompt:**
```
You have the L2 graph (named range level).

For each node compute:

1. IN-DEGREE: count of edges arriving at the node (node as DESTINATION)
2. OUT-DEGREE: count of edges leaving the node (node as ORIGIN)
3. BETWEENNESS CENTRALITY (approximated):
   For each node N: count pairs (source, destination) in graph
   that have N on some path between them.
   Normalise by total possible pairs. Result ∈ [0,1].

4. STRUCTURAL CLASSIFICATION:
   in-degree = 0                    → INPUT
   out-degree = 0                   → OUTPUT
   in-degree = 0 AND out-degree = 0 → ISOLATED — flag
   betweenness > 0.30               → CRITICAL
   betweenness 0.10–0.30            → INTERMEDIATE
   betweenness < 0.10               → AUXILIARY

OUTPUT:
  Node | In | Out | Betweenness | Classification
  ─────────────────────────────────────────────
```

## Prompt 2.2-B — Topological Sort

**Prompt:**
```
Using the L2 graph edges, list all nodes in topological order:
every ORIGIN node must appear before its DESTINATION node.

IF a cycle exists: identify the participating nodes → BLOCKER.

OUTPUT:
  TOPOLOGICAL ORDER: [ordered node list]
  CYCLES: [participating nodes / NONE]
  BLOCKERS: [list / NONE]
```

## Prompt 2.2-C — Pattern Pre-detection

**Prompt:**
```
Using metrics from 2.2-A and L2 graph structure, pre-identify
which structural patterns are likely present (confirmed in Phase 3):

P1 Linear pipeline  : consecutive nodes with in=1, out=1
P2 Central hub      : betweenness > 0.30 with clear domain name
P3 Aggregator       : in-degree > 3, out-degree ≤ 1
P4 Parallel branches: two or more subgraphs with no cross-edges
                      converging to common downstream node
P5 Cycle            : already detected in 2.2-B
P6 Isolated node    : in=0 AND out=0
P7 Decision tree    : node derived from nested IF/SE formulas (B.3)
P8 Lookup table     : node derived from DESLOC/OFFSET or
                      ÍNDICE+CORRESP on a 2D rate table (B.3)
P9 Cash flow loop   : sequential rows each referencing previous
                      balance (SAC, Price, balloon)

OUTPUT:
  Pattern | Likely nodes | Evidence
```

---

# Graph Enrichment — Phase 2.3

## Prompt 2.3 — Enrich Each Node

**Prompt:**
```
You have the L2 graph with metrics and the Phase 1 inventory.

For each node in the L2 graph, attach metadata from inventory:

INPUT nodes (in-degree = 0):
  → type           : from B.2 named ranges or A.5 Python inputs
  → constraint     : from B.2 or A.5
  → current value  : from B.2
  → category       : EXTERNAL INPUT / HARDCODED PARAM / CONFIG PARAM
  → source         : Excel cell reference or Python argument
  → edge-case risk : from A.6 or B.3 edge-case risk column

INTERMEDIATE and OUTPUT nodes:
  → original formula  : from B.3
  → interpretation    : from B.3
  → input types       : from B.3 types column
  → edge-case risk    : from B.3 risk column
  → covered in A.6    : [YES / NO]

CRITICAL nodes (betweenness > 0.30):
  → python function candidate: YES
  → justification: betweenness = [value]
  → semantic check: does the name clearly represent a domain concept?
    [YES → confirm as sub-function]
    [NO  → possible accidental hub → keep inline]

ENRICHED NODE FORMAT:
  NODE: [named range name]
  ├── Structural
  │   ├── in-degree      :
  │   ├── out-degree     :
  │   ├── betweenness    :
  │   └── classification :
  ├── Semantic (inventory)
  │   ├── type           :
  │   ├── constraint     :
  │   ├── current value  :
  │   ├── category       :
  │   ├── source         :
  │   ├── formula        :
  │   ├── interpretation :
  │   └── edge-case risk :
  └── Python derivation
      ├── function candidate: [YES / NO]
      └── justification      :
```

---

## ENRICHED GRAPH CONSOLIDATED SHEET

```
╔══════════════════════════════════════════════════════╗
║  ENRICHED GRAPH — PHASE 2                           ║
╠══════════════════════════════════════════════════════╣
║ Total nodes / edges   :                             ║
║ INPUT nodes           :                             ║
║ OUTPUT nodes          :                             ║
║ CRITICAL nodes        :                             ║
║ ISOLATED nodes        :                             ║
║ Topological order     :                             ║
║ Cycles                :                             ║
║ Blockers              :                             ║
╠══════════════════════════════════════════════════════╣
║ ENRICHED NODE FICHES  :                             ║
║  [one fiche per node per format above]              ║
╠══════════════════════════════════════════════════════╣
║ STATUS PHASE 2: [COMPLETE / BLOCKED — reason]       ║
╚══════════════════════════════════════════════════════╝
```
