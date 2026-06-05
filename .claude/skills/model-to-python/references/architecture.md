# Architecture Derivation — Phase 3

---

## 3.1 — Structural Pattern Identification

**Prompt:**
```
You have the Enriched Graph from Phase 2.

Identify all structural patterns present, applying the rules below.
For each pattern found: cite the nodes involved, the graph metrics
that evidence it, and the Python translation prescribed.

PATTERN 1 — LINEAR PIPELINE
  Definition: sequence of nodes where each has in-degree=1 and
  out-degree=1, forming chain A→B→C→D.
  Evidence: consecutive nodes with in=1 and out=1 in topological order.
  Translation: sequence of assignments inside a single function.
  Rule: do NOT create sub-functions for chains shorter than 7 nodes.

PATTERN 2 — CENTRAL HUB
  Definition: CRITICAL node (betweenness > 0.30) with clear domain name.
  Evidence: betweenness > 0.30 AND semantic check = YES (from 2.3).
  Translation: independent Python function with explicit return.
  Arguments: direct predecessors in enriched graph.
  IMPORTANT: if betweenness > 0.30 but semantic check = NO →
    accidental hub → keep inline → document as section comment.

PATTERN 3 — AGGREGATOR
  Definition: node with in-degree > 3 and out-degree ≤ 1.
  Evidence: in-degree > 3 in metrics table.
  Translation: function receiving multiple inputs, producing
  single aggregated result (portfolio_var, relatorio_final, etc.)

PATTERN 4 — PARALLEL BRANCHES
  Definition: two or more subgraphs with zero cross-edges,
  converging to a common downstream node.
  Evidence: nodes with no path between them pointing to same node.
  Translation: independent calculations — candidates for numpy
  vectorisation. Document as separate blocks before aggregation.

PATTERN 5 — CYCLE
  Definition: path returning to its origin node.
  Evidence: cycle recorded in 2.2-B.
  Translation: while loop with convergence criterion or numerical solver.
  BLOCKER: request termination criterion from user before continuing.

PATTERN 6 — ISOLATED NODE
  Definition: in-degree=0 AND out-degree=0.
  Evidence: ISOLATED classification in 2.2-A.
  Translation: unused constant — flag to user for confirmation.

PATTERN 7 — DECISION TREE
  Definition: node derived from nested IF/SE formulas (detected in B.3).
  Evidence: B.3 formula contains nested SE(SE(...)) or IF(IF(...)).
  Translation: if/elif/else chain for categorical conditions (scalar);
  NOT np.where (which is array-wise — wrong for eligibility trees).
  Rule: map each branch as named constant or dict, not as magic number.

PATTERN 8 — LOOKUP PRICING TABLE
  Definition: 2D matrix of values indexed by two categorical axes
  (e.g., tenor × segment, prazo × rating).
  Evidence: DESLOC/OFFSET or ÍNDICE+CORRESP on Auxiliary tab table (B.3).
  Translation: pd.DataFrame with named index and columns;
  access via .at[row_key, col_key] or .loc after validation.
  Rule: table itself becomes a parameter (loaded from config or CSV),
  not hardcoded in function body.

PATTERN 9 — PROJECTED CASH FLOW LOOP
  Definition: sequential rows each referencing previous period's balance.
  Evidence: formula in row N references row N-1 in same column (B.5 L1).
  Appears in: SAC, Price amortisation, IBNR development triangle, ALM gaps.
  Translation: for loop over periods with accumulated state variable.
  NOT a graph cycle — it is forward-only temporal iteration.
  Rule: initialise state before loop; append results to list, then
  convert to pd.DataFrame or np.ndarray after loop.

OUTPUT:
  Pattern | Nodes involved | Metrics evidence | Python translation
  ──────────────────────────────────────────────────────────────────
  Blockers before 3.2: [list / NONE]
```

---

## 3.2 — Function Signature Derivation

**Prompt:**
```
You have the Enriched Graph (Phase 2) and patterns from 3.1.

Derive the complete Python function signature for each function to create.

WHICH NODES BECOME FUNCTIONS:
  → Node classified CRITICAL with semantic check = YES (Pattern 2)
  → Node classified AGGREGATOR (Pattern 3)
  → Node that is a model OUTPUT
  → Node producing a P8 lookup table result
  → Node producing a P9 cash flow loop result
  → Any node explicitly marked "python function candidate: YES" in 2.3

FOR EACH FUNCTION:

  1. NAME
     → Named range in snake_case
     → If no named range: "calcular_" + tab + "_" + coordinate

  2. ARGUMENTS
     → Direct predecessors in enriched graph
     → Type from enriched node metadata (2.3):
       scalar float with constraint ∈(0,1) → float with assert
       scalar int > 0                       → int with assert
       time series                          → pd.Series
       matrix / array                       → np.ndarray
       2D pricing table                     → pd.DataFrame
       categorical string                   → str with validation
       cash flow schedule                   → pd.DataFrame or list

  3. RETURN VALUE
     → Financial quantity the node represents
     → Type from enriched node metadata

  4. DOCSTRING (one line)
     → What the function computes
     → "Computed from: [predecessors]"
     → "Used by: [successors]"

  5. ENTRY VALIDATIONS
     → One assertion or raise per argument constraint from 2.3 metadata
     → Shape checks for arrays
     → Lookup key existence check for P8 tables

MAIN ENTRY POINT FUNCTION:
  → Name: from model filename or "model()"
  → Arguments: ALL INPUT nodes from enriched graph
  → Return: ALL OUTPUT nodes as named dict
  → Body: calls all sub-functions in topological order

OUTPUT PER FUNCTION:
  FUNCTION: snake_case_name
  ├── Arguments  : arg1: type, arg2: type, ...
  ├── Returns    : name: type
  ├── Docstring  :
  ├── Validations: [asserts / raises from metadata]
  ├── Called by  : [downstream functions]
  └── Calls      : [upstream functions]
```

---

## ARCHITECTURE CONSOLIDATED SHEET

```
╔══════════════════════════════════════════════════════╗
║  ARCHITECTURE — PHASE 3                             ║
╠══════════════════════════════════════════════════════╣
║ Patterns identified :                               ║
║  P1 | P2 | P3 | P4 | P5 | P6 | P7 | P8 | P9        ║
║ Functions to create :                               ║
║ Main entry point    :                               ║
╠══════════════════════════════════════════════════════╣
║ FUNCTION SIGNATURES                                 ║
║  [one block per function per format above]          ║
╠══════════════════════════════════════════════════════╣
║ Blockers            :                               ║
║ STATUS PHASE 3: [COMPLETE / INCOMPLETE — reason]    ║
╚══════════════════════════════════════════════════════╝
```
