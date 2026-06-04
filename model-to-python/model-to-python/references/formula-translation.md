# Formula Translation — Phase 4.1

---

## 4.1 — Domain-Aware Formula Translation

**Prompt:**
```
For each node becoming a Python function (from Phase 3):
  (a) Original Excel formula from enriched node metadata (2.3)
  (b) Input types from enriched node metadata (2.3)
  (c) Edge-case risks from enriched node metadata (2.3)

Translate each formula to Python using the rules below.
Apply correct types. Add edge-case treatments from A.6.

═══════════════════════════════════════════════════════
TRANSLATION RULES — STATISTICS / RISK
═══════════════════════════════════════════════════════

=PERCENTIL(range, p) / =PERCENTILE
  IF pd.Series AND no NaN guaranteed → series.quantile(p)
  IF np.ndarray                      → np.percentile(array, p*100)
  IF NaN possible (edge-case risk=YES) → np.nanpercentile(array, p*100)
  CONVENTION NOTE: Excel p ∈ [0,1]; numpy uses [0,100] — always multiply

=MÉDIA(SE(range < limiar, range)) / Expected Shortfall pattern
  → tail = array[array < threshold]
  → IF tail empty → return np.nan + warnings.warn(...)
  → ELSE → np.mean(tail) or tail.mean()

=DESVPAD / =STDEV   → np.std(array, ddof=1) OR series.std(ddof=1)
=DESVPADP / =STDEVP → np.std(array, ddof=0)
  ALWAYS specify ddof explicitly — Python default is ddof=0, Excel default is ddof=1

=INV.NORM(p, μ, σ)  → scipy.stats.norm.ppf(p, loc=mu, scale=sigma)
=DIST.NORM(x,μ,σ,1) → scipy.stats.norm.cdf(x, loc=mu, scale=sigma)
=DIST.NORM(x,μ,σ,0) → scipy.stats.norm.pdf(x, loc=mu, scale=sigma)

=CONT.SE(range,"<"&ref) → int(np.sum(array < ref))

═══════════════════════════════════════════════════════
TRANSLATION RULES — FINANCIAL MATHEMATICS (PRODUCT)
═══════════════════════════════════════════════════════

ALWAYS import numpy_financial as npf for these formulas.

=PGTO(taxa, nper, pv [, vf, tipo])
  → npf.pmt(rate=taxa, nper=nper, pv=-pv)
  NOTE: Excel pv sign convention differs — use -pv

=NPER(taxa, pgto, pv)
  → npf.nper(rate=taxa, pmt=pgto, pv=-pv)

=TAXA(nper, pgto, pv)
  → npf.rate(nper=nper, pmt=pgto, pv=-pv)
  EDGE CASE: solver may not converge → wrap in try/except, return np.nan

=VPL(taxa, cf_range)
  → npf.npv(rate=taxa, values=cashflows_array)
  NOTE: Excel VPL excludes period 0; npf.npv includes index 0
  CORRECTION: npf.npv(taxa, np.concatenate([[0], cashflows]))

=TIR(fluxos)
  → npf.irr(values=cashflows_array)
  EDGE CASE: non-monotone cash flows → multiple IRR solutions → warn user

=VP(taxa, nper, pgto)
  → npf.pv(rate=taxa, nper=nper, pmt=-pgto)

Rate conversion formulas:
  =(1+taxa_anual)^(1/12)-1    → (1 + annual_rate) ** (1/12) - 1
  =(1+taxa_mensal)^12-1        → (1 + monthly_rate) ** 12 - 1

SAC amortisation loop (P9):
  → saldo = pv
  → amortizacao = pv / n
  → results = []
  → for t in range(1, n+1):
        juros = saldo * taxa
        instalment = amortizacao + juros
        saldo -= amortizacao
        results.append({"periodo": t, "saldo": saldo,
                         "juros": juros, "amortizacao": amortizacao,
                         "prestacao": instalment})
  → return pd.DataFrame(results)

═══════════════════════════════════════════════════════
TRANSLATION RULES — RETURNS / COMPOUNDING
═══════════════════════════════════════════════════════

=LN(Pt/Pt-1)
  IF pd.Series → np.log(prices / prices.shift(1))  → returns pd.Series
  IF np.ndarray → np.log(prices[1:] / prices[:-1]) → returns np.ndarray
  EDGE CASE: prices containing 0 → np.log produces -inf → pre-check

=(Pt-Pt-1)/Pt-1
  IF pd.Series → prices.pct_change()
  IF np.ndarray → np.diff(prices) / prices[:-1]

=PRODUTO(1+range)-1
  IF pd.Series → (1 + series).prod() - 1
  IF np.ndarray → np.prod(1 + array) - 1

═══════════════════════════════════════════════════════
TRANSLATION RULES — MATRIX
═══════════════════════════════════════════════════════

=MMULT(A, B)   → np.dot(A, B)
=TRANSPOR(A)   → A.T
=INVMAT(A)     → np.linalg.inv(A)
  EDGE CASE: singular matrix → raises LinAlgError → wrap in try/except

═══════════════════════════════════════════════════════
TRANSLATION RULES — LOGIC
═══════════════════════════════════════════════════════

=SE(cond, v1, v2) on SCALAR → v1 if cond else v2
=SE(cond, v1, v2) on ARRAY  → np.where(cond, v1, v2)

NESTED =SE (P7 — Decision Tree):
  → Translate as if/elif/else chain
  → Label each branch with domain meaning as comment
  → Do NOT use nested np.where — unreadable and error-prone
  Example:
    if score >= limiar_alto:
        return "ALTO"
    elif score >= limiar_medio:
        return "MÉDIO"
    else:
        return "BAIXO"

=E(c1,c2) → c1 & c2 (array) | c1 and c2 (scalar)
=OU(c1,c2) → c1 | c2 (array) | c1 or c2 (scalar)

═══════════════════════════════════════════════════════
TRANSLATION RULES — LOOKUP / AGGREGATION
═══════════════════════════════════════════════════════

=ÍNDICE(arr, l, c) → arr[l-1, c-1]   (Excel is 1-indexed)

P8 — Lookup Pricing Table:
  =ÍNDICE(tabela, CORRESP(prazo, prazos, 0), CORRESP(seg, segs, 0))
  → tabela_df.at[prazo, segmento]
  Where tabela_df is pd.DataFrame with prazo as index, segment as columns.
  EDGE CASE: key not in index → raise KeyError with informative message.

=DESLOC / =OFFSET dynamic reference:
  → Translate as explicit index calculation on array or DataFrame
  → Never replicate the dynamic reference directly — materialise the logic

=PROCV / =VLOOKUP → dict(zip(keys, values)).get(lookup_key)
  EDGE CASE: key not found → .get returns None → add default or raise

=SOMASES / =SUMIFS → df.loc[condition_mask, value_col].sum()
  or df.query("col1 == val1 and col2 == val2")["value_col"].sum()

=SOMAPRODUTO / =SUMPRODUCT → np.dot(array1, array2)
  or (series1 * series2).sum()

═══════════════════════════════════════════════════════
EDGE-CASE TREATMENT RULES (APPLY TO ALL DOMAINS)
═══════════════════════════════════════════════════════

IF edge-case risk = YES from enriched node metadata:
  zero denominator    → if denominator == 0: return np.nan (or raise)
  NaN in input        → use nan-safe variant (nanmean, nanpercentile)
  empty array         → if len(array) == 0: raise ValueError(...)
  invalid domain      → assert at function entry
  solver non-convergence → try/except returning np.nan + warning

IF case was NOT COVERED in original artefact:
  → Add treatment + comment:
    # EDGE CASE NOT COVERED IN ORIGINAL ARTEFACT — added in derivation

═══════════════════════════════════════════════════════
CONFIDENCE LEVELS
═══════════════════════════════════════════════════════

ALTA  → direct unambiguous mapping, type confirmed from metadata
MÉDIA → complex formula, translation requires attention to edge cases,
        OR formula partially simplified (document what was simplified)
BAIXA → no direct equivalent, domain-specific formula not in mapping,
        OR type ambiguous → flag for user confirmation

FOR EACH TRANSLATED FORMULA RECORD:
  Node           :
  Excel formula  :
  Python expr    :
  Type applied   :
  Edges treated  :
  Edges added (not in original):
  Confidence     : [ALTA / MÉDIA / BAIXA]
```

---

## 4.2 — Function Body Assembly

**Prompt:**
```
You have:
  (a) Function signatures from Phase 3.2
  (b) Formula translations from 4.1
  (c) Topological order from Phase 2.2

Assemble the complete body of each Python function.

RULES:

1. LINE ORDER
   Follow topological order of nodes within each function.
   Never use a variable before it is computed.

2. VARIABLE NAMES
   → Named range in snake_case as variable name
   → If no named range: semantically descriptive name from domain
   → Never use generic names: resultado, valor, temp, x, y

3. ENTRY VALIDATIONS (first block in function body)
   Insert all assertions and raises from Phase 3.2 signatures.
   Order: type check → domain constraint → shape/dimension

4. INLINE TRACEABILITY COMMENTS
   For each calculation line: add comment with financial meaning
   and Excel cell reference.
   Format: # [quantity computed] — [Excel cell reference]
   Example:
     retornos = np.log(precos / precos.shift(1))
     # log daily return — Cálculo!C2:C253

5. SECTION COMMENTS
   For each logical stage change:
   # --- [stage name] ---

6. EDGE-CASE HANDLERS
   Insert after entry validations, before operations with identified risk.
   Mark new cases (not in original):
   # EDGE CASE NOT IN ORIGINAL ARTEFACT — added in derivation

7. RETURN
   → Return exactly what Phase 3.2 defined
   → Multiple outputs: named dict
     return {"var_hist": var_hist, "var_param": var_param, ...}

FORMAT:
  def function_name(arg1: type, arg2: type = default) -> return_type:
      """
      [docstring from 3.2]
      Computed from: [predecessors]
      Used by: [successors]
      """
      # --- Entry validation ---
      [asserts and raises]

      # --- [stage 1 name] ---
      variable_1 = [expression from 4.1]  # meaning — ExcelCell

      # --- [stage N name] ---
      variable_n = [expression from 4.1]  # meaning — ExcelCell

      return [output]
```

---

## DERIVATION CONSOLIDATED SHEET

```
╔══════════════════════════════════════════════════════╗
║  DERIVATION — PHASE 4                               ║
╠══════════════════════════════════════════════════════╣
║ Formulas translated  :                              ║
║  Confidence ALTA     :                              ║
║  Confidence MÉDIA    :                              ║
║  Confidence BAIXA    :                              ║
║  Edge cases covered  :                              ║
║  Edge cases added    :                              ║
╠══════════════════════════════════════════════════════╣
║ AUDIT 4.3 — COMPLETENESS                            ║
║  Nodes covered       : [X / total] ([%])            ║
║  Inputs exposed      : [YES / gaps]                 ║
║  Outputs returned    : [YES / gaps]                 ║
║  Blockers            :                              ║
╠══════════════════════════════════════════════════════╣
║ AUDIT 4.4 — EXECUTION ORDER                         ║
║  Functions checked   :                              ║
║  Violations          : [list / NONE]                ║
║  Blockers            :                              ║
╠══════════════════════════════════════════════════════╣
║ AUDIT 4.5 — ARCHITECTURE                            ║
║  C1 Coupling         :                              ║
║  C2 Cohesion         :                              ║
║  C3 Length           :                              ║
║  C4 Global variables :                              ║
║  C5 Traceability     :                              ║
║  C6 Edge coverage    :                              ║
║  Refactorings        : [prioritised list / NONE]    ║
╠══════════════════════════════════════════════════════╣
║ ITEMS FOR USER                                      ║
║  Blockers            :                              ║
║  Pending confirmations:                             ║
║  Suggested refactors :                              ║
╠══════════════════════════════════════════════════════╣
║ STATUS PHASE 4: [COMPLETE / INCOMPLETE — reason]    ║
╚══════════════════════════════════════════════════════╝
```
