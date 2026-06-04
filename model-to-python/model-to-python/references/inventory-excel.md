# Excel Inventory — Full Prompts (Phase 1 Block B)

---

## B.1 — Physical Recognition of Workbook

**Prompt:**
```
You have received a raw Excel file (.xlsx, .xlsm, or .xls).
Perform complete physical recognition BEFORE interpreting content.

STEP 1 — EXTRACT RAW STRUCTURE
  For each tab in the workbook, extract and record:
  → Exact tab name
  → Number of used rows (last row with content)
  → Number of used columns (last column with content)
  → Content of cell A1 (first value or label)
  → Content of cell B1
  → Formulas present: YES / NO / UNCERTAIN
    (check if any cell value starts with "=")
  → Charts present: YES / NO

  RAW TABLE:
  Tab name | Rows | Cols | A1 | B1 | Formulas | Charts

STEP 2 — CLASSIFY EACH TAB
  Using the raw data from Step 1, classify each tab.
  For each classification, cite the Step 1 evidence.

  Input       → no formulas, manual cells, descriptive labels,
                names like "Dados", "Preços", "Inputs", "Série"
  Parameters  → few rows (< 20), two columns (name + value),
                names like "Config", "Params", "Parâmetros",
                single numeric values per row
  Calculation → formulas present, many rows,
                names like "Cálculo", "Retornos", "Fluxo", "MC"
  Output      → charts present, few summary rows,
                names like "Resultado", "VaR", "Report", "Dashboard"
  Auxiliary   → lookup tables, calendars, reference data,
                names like "Lookup", "Feriados", "Tabela_Taxas"

  IF classification is ambiguous from Step 1 alone:
  → Mark as [UNCERTAIN — read first 10 rows before classifying]
  → Do NOT proceed to B.2 until all tabs are classified.

OUTPUT:
  RAW STRUCTURE:
  Tab | Rows | Cols | A1 | B1 | Formulas | Charts

  CLASSIFICATION:
  Tab | Type | Step 1 evidence

  UNCERTAIN TABS : [list / NONE]
  BLOCKERS       : [tabs needing additional reading / NONE]
```

---

## B.2 — Named Ranges

**Prompt:**
```
You have the workbook tab classification from B.1.

Extract and document all named ranges in the workbook.

FOR EACH NAMED RANGE record:
  → Exact name
  → Tab and cell reference
  → Current value stored
  → Inferred type: float, int, str, pd.Series, np.ndarray
  → Scalar or vector/table
  → Domain constraints inferrable from name and value
    Examples:
      "conf_99 = 0.99" → float ∈ (0,1)
      "taxa_juros = 0.015" → float, monthly rate
      "prazo = 360" → int, periods > 0
      "n_parcelas = 24" → int > 0
      "segmento = 'VAREJO'" → str, categorical
  → Category: EXTERNAL INPUT / HARDCODED PARAMETER / CONFIG PARAMETER

  IF no named ranges found:
  → Record: NOT FOUND
  → Note: model parameters referenced by coordinate only (e.g., PARAMS!B2)
  → This is a documentation risk — flag for user

OUTPUT:
  Name | Reference | Value | Type | Scalar/Vector | Constraint | Category
```

---

## B.3 — Key Formulas

**Prompt:**
```
You have tab classification from B.1.

Extract all formulas from Calculation and Output tabs.
For each formula, produce logical and mathematical interpretation
using the domain formula signal table from the active domain reference,
PLUS the universal mapping below.

UNIVERSAL FORMULA MAPPING:

STATISTICS / RISK:
  =PERCENTIL(range, p) / =PERCENTILE
    → quantile(series, p) — verify if p = 1−α (VaR convention)
  =MÉDIA(SE(range<0,range)) / AVERAGEIF below threshold
    → mean of tail losses — Expected Shortfall signal
  =DESVPAD(range) / =STDEV     → std(array, ddof=1)
  =DESVPADP(range) / =STDEVP   → std(array, ddof=0)
  =DIST.NORM / =NORM.DIST      → scipy.stats.norm.cdf
  =INV.NORM / =NORM.INV        → scipy.stats.norm.ppf
  =CONT.SE(range,"<"&ref)      → np.sum(array < ref)

FINANCIAL MATHEMATICS:
  =PGTO(taxa,nper,pv)          → numpy_financial.pmt(rate,nper,-pv)
  =NPER(taxa,pgto,pv)          → numpy_financial.nper(rate,pmt,-pv)
  =TAXA(nper,pgto,pv)          → numpy_financial.rate(nper,pmt,-pv)
  =VPL(taxa,cf_range)          → numpy_financial.npv(rate,cashflows)
  =TIR(fluxos)                 → numpy_financial.irr(cashflows)
  =VP(taxa,nper,pgto)          → numpy_financial.pv(rate,nper,-pmt)
  =IPGTO(taxa,per,nper,pv)     → interest component in period per
  =PPGTO(taxa,per,nper,pv)     → principal component in period per
  =(1+taxa_anual)^(1/12)-1     → (1+annual_rate)**(1/12)-1
  =(1+taxa_mensal)^12-1        → (1+monthly_rate)**12-1

RETURNS / COMPOUNDING:
  =PRODUTO(1+range)-1          → np.prod(1+array)-1
  =LN(Pt/Pt-1)                 → np.log(prices/prices.shift(1))
  =(Pt-Pt-1)/Pt-1              → prices.pct_change()

MATRIX:
  =MMULT(A,B)                  → np.dot(A,B)
  =TRANSPOR(A)                 → A.T
  =INVMAT(A)                   → np.linalg.inv(A)

LOOKUP / AGGREGATION:
  =ÍNDICE(arr,l,c)/=INDEX      → arr[l-1,c-1]
  =CORRESP(v,range,0)/=MATCH   → np.where(array==v)[0][0]
  =PROCV/=VLOOKUP              → dict or DataFrame lookup
  =DESLOC/=OFFSET              → dynamic reference — flag for P8
  =SOMASES/=SUMIFS             → conditional sum by segment
  =SOMAPRODUTO/=SUMPRODUCT     → np.dot or element-wise product

LOGIC:
  =SE(cond,v1,v2)/=IF          → v1 if cond else v2 (scalar)
                                  np.where(cond,v1,v2) (array)
  Nested =SE(=SE(...))         → P7 (Decision Tree) signal
  {array formula}              → operates on entire vector

FOR EACH FORMULA RECORD:
  Cell | Tab | Excel formula | Logical interpretation |
  Input types | Edge-case risk [YES/NO/UNCERTAIN]

OUTPUT:
  Cell | Tab | Formula | Interpretation | Types | Risk
```

---

## B.4 — Inter-Tab Dependencies

**Prompt:**
```
You have the formula list from B.3.

1. BUILD TAB DEPENDENCY GRAPH
   For each cross-tab reference (pattern TabName!Cell):
   → record: SOURCE_TAB → DESTINATION_TAB → referenced cell

2. TOPOLOGICAL ORDERING
   List tabs in calculation order: every source tab appears
   before its destination tab.

3. CYCLE DETECTION
   Identify any tab pairs with mutual references.
   IF cycle found → BLOCKER: record and escalate to user.

OUTPUT:
  Graph:
    SOURCE_TAB → DESTINATION_TAB

  Calculation sequence: [ordered list]
  Cycles: [pairs / NONE]
  Blockers: [list / NONE]
```

---

## B.5 — Inter-Cell Dependencies (L1 Graph Seed)

**Prompt:**
```
You have all formulas from B.3.

Build the cell-level dependency list (input to Phase 2 graph construction).

FOR EACH FORMULA CELL (destination):
  → identify all referenced cells (origins)
  → for local references (no tab prefix), add current tab name
  → expand ranges (B2:B253) into individual cells
  → for named ranges, use the name as node identifier

RECORD FORMAT:
  ORIGIN → DESTINATION

ALSO RECORD:
  Cells with no predecessors (appear only as origins): INPUT CANDIDATES
  Cells with no successors (appear only as destinations
  and referenced by nothing else): OUTPUT CANDIDATES

OUTPUT:
  DEPENDENCY LIST:
  Origin | Destination

  INPUT CANDIDATES  : [list]
  OUTPUT CANDIDATES : [list]
```

---

## B.6 — VBA and Macros Detection

**Prompt:**
```
Check whether the Excel file contains VBA code or macros.

VBA SIGNALS:
  → .xlsm extension (macro-enabled workbook)
  → .bas or .cls files inside workbook zip
  → cell formulas calling macros (e.g., =RUN_MACRO())
  → presence of "Developer" tab references in structure

IF VBA DETECTED:
  → Record as BLOCKER
  → Message to user:
    "VBA code detected in this file. Macros frequently contain
     critical calculation logic invisible in cells. Please export
     and provide the VBA module contents before proceeding.
     The inventory and graph cannot be considered complete without
     this content."

IF NOT DETECTED:
  → Record: "Logic entirely in cells — no VBA"

OUTPUT:
  VBA/Macros: [DETECTED — BLOCKER / NOT DETECTED]
```

---

## EXCEL INVENTORY CONSOLIDATED SHEET

```
╔══════════════════════════════════════════════════════╗
║  EXCEL INVENTORY — PHASE 1 BLOCK B                  ║
╠══════════════════════════════════════════════════════╣
║ Domain identified   :                               ║
║ Domain reference    :                               ║
╠══════════════════════════════════════════════════════╣
║ TABS (B.1)                                          ║
║  name | rows | cols | type | evidence               ║
╠══════════════════════════════════════════════════════╣
║ NAMED RANGES (B.2)                                  ║
║  name | ref | value | type | constraint | category  ║
║  Named ranges found: [YES / NOT FOUND]              ║
╠══════════════════════════════════════════════════════╣
║ KEY FORMULAS (B.3)                                  ║
║  cell | tab | formula | interpretation | types | risk║
╠══════════════════════════════════════════════════════╣
║ TAB DEPENDENCY GRAPH (B.4)                          ║
║ Calculation sequence:                               ║
║ Cycles: [list / NONE]                               ║
╠══════════════════════════════════════════════════════╣
║ VBA/MACROS (B.6): [DETECTED / NOT DETECTED]         ║
╠══════════════════════════════════════════════════════╣
║ BLOCKERS            :                               ║
║ STATUS BLOCK B: [COMPLETE / INCOMPLETE — reason]    ║
╚══════════════════════════════════════════════════════╝
```
