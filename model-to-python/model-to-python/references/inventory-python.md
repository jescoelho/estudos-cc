# Python Inventory — Full Prompts (Phase 1 Block A)

---

## A.1 — Physical Recognition

**Prompt:**
```
You have received a Python file. Before interpreting any logic,
perform the complete physical recognition below.

1. LINE COUNT AND READING STRATEGY
   Count total lines and define strategy:
     < 150 lines   → read entire file at once
     150–500 lines → read in blocks: imports / each function / main
     > 500 lines   → imports + function signatures + entry point +
                     critical functions by name only

2. FILE METADATA
   Read first 30 lines and record:
   → module docstring content (or NOT FOUND)
   → author, date, version if declared

3. DEFINITION INVENTORY
   Extract all definitions with line number:
   → root-level functions (def at column 0)
   → root-level classes (class at column 0)
   → class methods (def with 4-space indent)

OUTPUT:
  Total lines      :
  Strategy adopted :
  Module docstring : [summary / NOT FOUND]
  Functions        : [name — line]
  Classes          : [name — line]
```

---

## A.2 — Dependency Map

**Prompt:**
```
You have the Python file read per A.1 strategy.
Extract and interpret all external dependencies.

1. EXTRACT ALL IMPORTS with line, form, alias.

2. FOR EACH LIBRARY record domain signal from the active domain
   reference file. Also apply these cross-domain signals:

   numpy              → vectorised / matrix operations
   pandas             → time series / tabular data
   scipy.stats        → distributions, statistical tests
   scipy.optimize     → parameter calibration, root finding
   scipy.linalg       → matrix decomposition
   scipy.interpolate  → curve interpolation (ALM, FTP)
   statsmodels        → econometric models, GARCH
   sklearn            → ML pipeline
   xgboost/lightgbm   → gradient boosting
   tensorflow/torch   → deep learning
   shap               → model explainability
   QuantLib           → derivative / bond pricing
   numpy_financial    → PMT, NPV, IRR, NPER (product pricing)
   arch               → ARCH/GARCH volatility
   numba/cython       → performance-critical loops
   lifetimes          → survival / LTV models
   openpyxl/xlrd      → Excel I/O
   sqlalchemy         → database I/O
   requests/httpx     → external API data source
   matplotlib/seaborn → visualisation only — no logic impact

3. UNRECOGNISED LIBRARIES
   → list separately; may be internal modules with proprietary logic
   → attempt to locate corresponding file

OUTPUT:
  Library | Line | Alias | Domain signal
  ─────────────────────────────────────
  Unrecognised: [list / NONE]
```

---

## A.3 — Function Structure Map

**Prompt:**
```
For each function identified in A.1, extract the items below.
Then build the call graph and compute depth.

FOR EACH FUNCTION:
  a) Full signature: name, parameters, defaults, type hints
  b) Docstring: full content or ABSENT
  c) Return value: all return statements; if none → NONE/SIDE EFFECT
  d) Internal calls: other functions in same file +
     relevant library calls (np.percentile, pmt, norm.ppf...)
  e) Domain variables: names representing model quantities
     (returns, sigma, saldo, score, premio...) — exclude loop counters
  f) Control flow:
     FOR loops: count, what they iterate over
     WHILE: termination condition
     IF/ELSE: branching condition

CALL GRAPH:
  → For every A that calls B: record A → B
  → Functions with no callers: entry-point candidates

DEPTH:
  → level 0 = entry point
  → level N = recursive

OUTPUT:
  Function: name(params)
  ├── Docstring  :
  ├── Parameters : name (type, default if any)
  ├── Returns    :
  ├── Calls      :
  ├── Variables  :
  └── Control    :

  Call graph:
    entry_point()
      └── level1_func()
            └── level2_func()

  Depth          :
  Entry point    :
```

---

## A.4 — Entry Point

**Prompt:**
```
Using the call graph from A.3, identify the entry point
by checking patterns in this order — stop at first match:

  1. if __name__ == "__main__": → standalone script
  2. def main(): with no callers → conventional main
  3. Top-level function with no callers → implicit candidate
  4. Statements outside any function → procedural script

From the identified entry point, trace:
  → variables created first
  → function call order
  → values passed between functions
  → final value produced

OUTPUT:
  Entry point      :
  Pattern matched  :
  Data flow        : [raw input → ... → final output]
```

---

## A.5 — Input / Parameter / Output Separation

**Prompt:**
```
From full file reading and call graph, classify each data item below.

EXTERNAL INPUTS — data arriving at runtime
  Signals: args without default, pd.read_csv/excel/sql, sys.argv,
           argparse, os.environ, requests.get, cursor.execute
  Record: name / inferred type / probable source / constraints

HARDCODED PARAMETERS — literal values controlling model behaviour
  Search for: decimal floats (0.99, 0.05), control integers (252, 12,
  360), config strings ("SAC","Price","log"), boolean flags
  Record: name / value / line / function

CONFIG PARAMETERS — values from external structure
  Signals: config["key"], params["key"], .json/.yaml/.ini reads
  Record: key / expected type / default if any

INTERMEDIATE DATA — computed internally, not received or returned
  → do NOT appear in REQUIRE
  Record: name / what it represents / which function

OUTPUTS — returned to caller or written externally
  Signals: return statements, to_csv/excel, write(), print of results
  Record: name / type / unit if inferrable / destination

OUTPUT TABLE:
  EXTERNAL INPUTS     : name | type | source | constraints
  HARDCODED PARAMS    : name | value | line | function
  CONFIG PARAMS       : key | type | default
  INTERMEDIATE DATA   : name | represents | function
  OUTPUTS             : name | type | unit | destination
```

---

## A.6 — Exception Cases

**Prompt:**
```
Identify all special-case handling in the code and coverage gaps.

1. EXISTING TREATMENTS — search for and record condition/action/line:
   → null check: if x is None / == None
   → exception blocks: try / except
   → explicit raises: raise
   → assertions: assert
   → NaN: np.nan, math.nan, isnan()
   → Inf: np.isinf, math.isinf
   → dimension checks: if len() / .shape / .size
   → empty checks: .empty / if not array
   → divisions: / and /= operators (zero risk)

2. UNIVERSAL CASES — check coverage using the list from the active
   domain reference file. Mark each: [COVERED] or [NOT COVERED]

OUTPUT:
  EXISTING TREATMENTS:
    Condition | Action | Line

  DOMAIN UNIVERSAL CASES:
    Case | Status [COVERED / NOT COVERED]
```

---

## PYTHON INVENTORY CONSOLIDATED SHEET

```
╔══════════════════════════════════════════════════════╗
║  PYTHON INVENTORY — PHASE 1 BLOCK A                 ║
╠══════════════════════════════════════════════════════╣
║ Domain identified   :                               ║
║ Domain reference    :                               ║
║ Lines / Strategy    :                               ║
║ Module docstring    :                               ║
╠══════════════════════════════════════════════════════╣
║ LIBRARIES                                           ║
║  name | line | alias | signal                       ║
║ UNRECOGNISED: [list / NONE]                         ║
╠══════════════════════════════════════════════════════╣
║ FUNCTIONS                                           ║
║  name | params | returns | calls | control          ║
╠══════════════════════════════════════════════════════╣
║ CALL GRAPH                                          ║
║ ENTRY POINT         :                               ║
╠══════════════════════════════════════════════════════╣
║ EXTERNAL INPUTS                                     ║
║  name | type | source | constraints                 ║
║ HARDCODED PARAMS                                    ║
║  name | value | line | function                     ║
║ CONFIG PARAMS                                       ║
║  key | type | default                               ║
║ OUTPUTS                                             ║
║  name | type | unit | destination                   ║
╠══════════════════════════════════════════════════════╣
║ EXCEPTIONS COVERED  :                               ║
║ CASES NOT COVERED   :                               ║
╠══════════════════════════════════════════════════════╣
║ STATUS BLOCK A: [COMPLETE / INCOMPLETE — reason]    ║
╚══════════════════════════════════════════════════════╝
```
