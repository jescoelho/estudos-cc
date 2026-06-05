# Phase 3.3 — Pseudoalgorithm Generator

**Position in pipeline:** executes immediately after Phase 3.2 (function signatures),
before Phase 4 (formula translation). Consumes Phase 3.2 output and enriched graph
from Phase 2.3. Produces two deliverables: high-level and detailed pseudoalgorithm
in Unicode text format, suitable for .docx rendering.

**Design principle:** Phase 3.2 already produced the complete contract of every
function (name, args with types, return, validations, call hierarchy). Phase 3.3
does not re-read the artefact — it translates that contract into pseudocode notation.
All information is sourced from the enriched graph and Phase 3.2 signatures.

---

## INPUTS TO THIS PHASE

```
FROM Phase 2.3 (enriched graph):
  → node.type             — Python type of each variable
  → node.constraint       — domain restriction (∈(0,1), >0, len>N...)
  → node.formula          — original Excel formula for annotation
  → node.interpretation   — mathematical meaning in domain language
  → node.edge_case_risk   — YES/NO/UNCERTAIN
  → topological_order     — execution sequence from 2.2-B
  → domain reference      — active domain file (market-risk, product-pricing...)

FROM Phase 3.1 (patterns):
  → pattern per node group — P1..P9 with prescribed translation

FROM Phase 3.2 (signatures):
  → function.name
  → function.arguments    — [(name, type, constraint, default)]
  → function.returns      — (name, type)
  → function.docstring
  → function.validations  — [(condition, error_type, message)]
  → function.calls        — upstream sub-functions
  → function.called_by    — downstream consumers
  → main_entry_point      — orchestrator function
```

---

## NOTATION RULES (domain-aware)

Read the active domain reference before generating any pseudocode.
Apply the notation table from `references/domains/<domain>.md`.
For symbols not covered by the domain reference, apply the universal table below.

### Universal symbol mapping

```
PYTHON CONSTRUCT        PSEUDOCODE NOTATION
─────────────────────────────────────────────────────────────────
variable = value        variable ← value
np.mean(x)              μ(x)  or  mean(x)
np.std(x, ddof=1)       σ(x)
np.percentile(x, p)     q_p(x)  or  Quantile(x, p)
np.sqrt(x)              √x
np.prod(1+x)-1          ∏(1+xⱼ) − 1
np.sum(x)               ∑ xᵢ
np.dot(A, B)            A · B
A.T                     Aᵀ
np.linalg.inv(A)        A⁻¹
np.where(c, a, b)       IF c THEN a ELSE b  (array context)
x if c else y           IF c THEN x ELSE y  (scalar context)
for i in range(n):      FOR i ← 0 TO n−1 DO
while condition:        WHILE condition DO
assert x > 0            REQUIRE x > 0
raise ValueError        RAISE ValueError
return x                RETURN x
len(x) == 0             |x| = 0
np.nan                  ∅  or  undefined
```

### Domain-specific notation supplements

```
DOMAIN             ADDITIONAL SYMBOLS
────────────────────────────────────────────────────────────────
market-risk        VaR_{α,h}, ES_{α,h}, σ̂, λ, ⌊·⌋
product-pricing    PMT(r,n,PV), NPV(r,CF), IRR(CF), SAC_t, Price_t
alm                D_mod, DV01, EVE, NII, Δr, bucket_t
insurance          f_freq, s_sev, E[L], IBNR_t, LR
profitability      NIM, RAROC, FTP_t, spread, K_alloc
scoring            P(churn), score, β·x, Φ(·), elasticity
```

---

## PROMPT 3.3-A — HIGH-LEVEL PSEUDOALGORITHM

**Audience:** model owners, risk committees, MRM reviewers, auditors.
**Target length:** 10–20 lines. No internal loops. No sub-function bodies.
**Rule:** if a step is implemented by a sub-function, write it as a single
`CALL FunctionName(args)` line — never expand the body.

```
PROMPT:

You have the main entry-point function from Phase 3.2 and the enriched graph.

Generate the HIGH-LEVEL pseudoalgorithm following these rules:

1. HEADER BLOCK
   Algorithm N — <MODEL_NAME> (Overview)
   (one blank line)
   REQUIRE: <list every INPUT node from enriched graph>
            Format: variable_name : type [constraint] — source reference
   ENSURE:  <list every OUTPUT node from enriched graph>
            Format: variable_name : type — what it represents

2. BODY — follow topological layers from Phase 2.2-B
   Layer 0 (inputs): do not write assignments — inputs are in REQUIRE
   Layer 1+: one line per topological layer, written as:
     // --- Layer N: <layer name from Phase 3.1 pattern> ---
     result ← CALL function_name(arg1, arg2, ...)

   Rules:
   → Use domain notation from active domain reference, not Python names
   → Write mathematical expression for simple assignments (≤ 1 operation)
   → Write CALL for anything that is a named sub-function in Phase 3.2
   → For P4 (parallel branches): write each branch on its own line
     with comment // [branch name] — independent
   → For P7 (decision tree): write IF/ELIF/ELSE with domain-meaningful labels
   → For P9 (cash flow loop): write single line
     FOR t ← 1 TO n DO  CALL compute_period(t, saldo_t)  END FOR

3. RETURN LINE
   RETURN { key1: value1, key2: value2, ... }
   (use all OUTPUT nodes from enriched graph, in topological order)

4. VALIDATION
   After generating, verify:
   [ ] All REQUIRE items match INPUT nodes in enriched graph
   [ ] All ENSURE items match OUTPUT nodes in enriched graph
   [ ] No sub-function body is expanded (only CALL references)
   [ ] No Python-specific syntax (no np., pd., dtype names)
   [ ] Length between 10 and 20 lines (excluding REQUIRE/ENSURE block)
```

---

## PROMPT 3.3-B — DETAILED PSEUDOALGORITHM

**Audience:** independent validators, developers, technical auditors.
**Target length:** 20–60 lines for main algorithm + one block per sub-function.
**Rule:** every logical step explicit, every exception covered, every
sub-function expanded in its own numbered block.

```
PROMPT:

You have all function signatures from Phase 3.2, the enriched graph from
Phase 2.3, and the exception list from Phase 1 A.6.

Generate the DETAILED pseudoalgorithm in two parts:

═══ PART 1 — MAIN ALGORITHM ═══

Follow the same header format as 3.3-A (REQUIRE / ENSURE).

BODY — follow this fixed section structure for every function:

  // --- 1. Entry Validation ---
  For each argument with constraint in Phase 3.2 validations:
    IF NOT <constraint> THEN RAISE <ErrorType>("<message>") END IF
  For each NOT COVERED case from Phase 1 A.6:
    IF <condition> THEN
      RAISE ValueError("<case description>")  // added — not in original artefact
    END IF

  // --- 2. <Layer name> ---
  For each node in this topological layer:
    variable ← <mathematical expression using domain notation>
                // <Excel cell reference from enriched node>

  // --- 3. <Next layer name> ---
  ... repeat for each layer ...

  // --- N. Output assembly ---
  RETURN { key: value, ... }

NOTATION RULES FOR DETAILED LEVEL:
  → Expand every formula to its mathematical form, not function call
    Example: σ̂ ← σ(serie_rt) becomes:
      σ̂ ← √( (1/(N−1)) · ∑ᵢ(rᵢ − μ̂)² )
  → For array operations: use Σ, ∏, index notation
  → For conditionals derived from P7: expand all branches with ELIF
  → For loops derived from P9: expand initialisation + loop body
  → Edge cases from A.6 marked [COVERED] appear as IF blocks
  → Edge cases marked [NOT COVERED] appear with comment:
    // NOT IN ORIGINAL ARTEFACT — added in derivation

═══ PART 2 — SUB-FUNCTION BLOCKS ═══

For each sub-function in Phase 3.2 (ordered by topological depth,
shallowest first):

  FUNCTION <name>(<arg1>: <type>, <arg2>: <type>, ...) → <return_type>
  """<docstring from Phase 3.2>
     Computed from: <predecessors>
     Used by: <successors>"""

    // --- Entry Validation ---
    [validations from Phase 3.2]

    // --- <stage name> ---
    [mathematical steps with Excel references]

    RETURN <output>

  END FUNCTION

VALIDATION CHECKLIST:
  [ ] Every INPUT node appears in REQUIRE with type and constraint
  [ ] Every OUTPUT node appears in ENSURE and in RETURN
  [ ] Every A.6 [COVERED] case has a corresponding IF block
  [ ] Every A.6 [NOT COVERED] case has a block marked as added
  [ ] All IF have END IF; all FOR have END FOR; all WHILE have END WHILE
  [ ] All CALL references in main algorithm have corresponding
      FUNCTION blocks in Part 2
  [ ] No Python-specific syntax anywhere
  [ ] Domain notation consistent with active domain reference
  [ ] Each calculation line has // Excel cell reference comment
```

---

## PROMPT 3.3-C — NOTATION REFERENCE TABLE

**Always generate this table** as the third deliverable of Phase 3.3.
It documents every symbol used, enabling a reader to interpret the
pseudoalgorithm without prior domain knowledge.

```
PROMPT:

Scan the high-level and detailed pseudoalgorithms generated in 3.3-A and 3.3-B.
For every symbol that is not plain English, generate a row in this table:

  Symbol | Type | Domain meaning | Constraint | Source
  ──────────────────────────────────────────────────────
  σ̂      | float | sample std dev of returns | >0 | Params!B4
  α      | float | confidence level | ∈(0,1) | Params!B2
  h      | int   | holding period in days | >0 | Params!B5
  ...

Rules:
  → Source = Excel cell reference from enriched node (Phase 2.3)
    or "derived" if computed internally
  → Constraint = from enriched node metadata
  → Type = from Phase 3.2 argument types, not Python type names
    (write "real number" not "float", "integer" not "int",
     "vector of reals" not "np.ndarray")
  → Include every Greek letter, subscript, operator, and
    domain acronym used in the pseudoalgorithms
```

---

## PROMPT 3.3-D — VALIDATION GATE

```
PROMPT:

You have the three outputs from Phase 3.3: high-level pseudoalgorithm (A),
detailed pseudoalgorithm with sub-functions (B), and notation table (C).

Run the full validation checklist before marking Phase 3.3 complete.

CONSISTENCY CHECKS (cross-phase):
  □ Every INPUT node in enriched graph (Phase 2.3) appears in REQUIRE of A and B
  □ Every OUTPUT node in enriched graph appears in ENSURE of A and B
  □ Every sub-function in Phase 3.2 has a FUNCTION block in B Part 2
  □ Every CALL in A refers to a function that exists in B Part 2
  □ Every symbol in A and B appears in notation table C

NOTATION CHECKS:
  □ No Python syntax: no np., pd., scipy., .shape, .iloc, dtype
  □ Domain notation matches active domain reference file
  □ All assignments use ← not =
  □ All array operations use Σ/∏/index notation, not loop syntax
    (unless the loop is semantically meaningful, e.g. P9 cash flow)

EXCEPTION CHECKS:
  □ Every [COVERED] case from A.6 has a corresponding IF block in B
  □ Every [NOT COVERED] case from A.6 has a block in B marked as added
  □ No exception case is silently dropped

STRUCTURAL CHECKS (detailed only):
  □ No FUNCTION block exceeds 30 logical lines
  □ No sub-function expanded inline in main algorithm body
  □ All IF/FOR/WHILE blocks have matching END IF/END FOR/END WHILE
  □ Return statement present in every FUNCTION block

OUTPUT:
  □ All checks: PHASE 3.3 = COMPLETE
  □ Failures present: list each failed check + location + correction needed
    → Do NOT mark complete until all failures resolved
```

---

## DELIVERABLES OF PHASE 3.3

```
D1 — pseudoalgorithm_highlevel.txt
     High-level pseudoalgorithm (Prompt 3.3-A output)
     → feeds Section 2 of .docx if docx generation requested

D2 — pseudoalgorithm_detailed.txt
     Detailed pseudoalgorithm + sub-function blocks (Prompt 3.3-B output)
     → feeds Section 3 and Section 4 of .docx

D3 — notation_table.md
     Symbol reference table (Prompt 3.3-C output)
     → feeds Section 5 of .docx

Optional D4 — pseudoalgorithm_<model_name>.docx
     Full document if user requested .docx output
     → use docx generation template from pseudo-risk-doc/references/templates.md
```

---

## PHASE 3.3 COMPLETION GATE

```
[ ] Prompt 3.3-A executed → high-level pseudoalgorithm produced
[ ] Prompt 3.3-B executed → detailed pseudoalgorithm + sub-functions produced
[ ] Prompt 3.3-C executed → notation table produced
[ ] Prompt 3.3-D executed → all validation checks passed
[ ] No Python syntax in any deliverable
[ ] All INPUT/OUTPUT nodes covered in REQUIRE/ENSURE
[ ] All A.6 exception cases documented
[ ] STATUS = COMPLETE → proceed to Phase 4
```

---

## INTEGRATION WITH PHASE 4

Phase 3.3 is a documentation phase — it does not block or modify Phase 4.
Phase 4 translates the same Phase 3.2 signatures into Python code.
The two outputs (pseudoalgorithm + Python) must be consistent:

```
CONSISTENCY RULE:
  Every FUNCTION block in pseudoalgorithm D2 must have a corresponding
  Python function in Phase 4.2 output with the same:
    → name (snake_case of pseudocode name)
    → argument count and order
    → return structure

  If Phase 4 adds a new sub-function not in Phase 3.2:
    → add a corresponding FUNCTION block to D2 retroactively
    → re-run Prompt 3.3-D validation gate

  This bidirectional consistency is the audit trail that links
  the mathematical specification (pseudoalgorithm) to the
  implementation (Python code).
```
