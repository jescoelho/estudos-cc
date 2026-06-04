# Domain Reference — Product Pricing

Covers: consumer loans, mortgages, auto financing, leasing,
        FX spot/forward, structured products, trade finance.

## Library Signals
```
numpy              → amortisation schedule vectorisation
pandas             → payment schedule as DataFrame
scipy.optimize     → implied rate solver (TIR/IRR)
numpy_financial    → npv, irr, pmt, nper, rate (direct equivalents)
QuantLib           → FX forward, structured bond pricing
sympy              → symbolic rate equations (rare)
```

## Excel Formula Signals — CRITICAL FOR THIS DOMAIN
```
=PGTO(taxa, nper, pv)         → instalment (PMT): fixed periodic payment
=NPER(taxa, pgto, pv)         → number of periods
=TAXA(nper, pgto, pv)         → implied rate per period
=VPL(taxa, cf1:cfN)           → net present value (NPV)
=TIR(fluxos)                  → internal rate of return (IRR)
=VP(taxa, nper, pgto)         → present value of annuity
=VF(taxa, nper, pgto)         → future value
=IPGTO(taxa, per, nper, pv)   → interest portion of instalment
=PPGTO(taxa, per, nper, pv)   → principal portion of instalment
=DESLOC(ref, rows, cols)      → dynamic reference to rate table
=PROCV / =VLOOKUP             → pricing table lookup by segment
=SOMASES / =SUMIFS            → conditional aggregation by band/segment
=SE aninhado / nested IF      → eligibility / decision tree
=(1+taxa_anual)^(1/12)-1      → annual → monthly rate conversion
=(1+taxa_mensal)^12-1         → monthly → annual rate conversion
=taxa*(1+taxa)^n/((1+taxa)^n-1) → PMT formula expanded
```

## Named Range Signals
```
taxa_juros, spread, taxa_base → interest rate (decimal)
prazo, nper, n_parcelas        → term in periods
valor_presente, pv, vp         → present value / principal
amortizacao                    → amortisation system: SAC or Price
tabela_taxas                   → pricing matrix (prazo × segment)
segmento_cliente               → client segment for pricing lookup
iof, tac, tarifa               → fees and charges
custo_captacao, cdi, selic     → funding cost rate
spread_credito                 → credit spread over benchmark
nocional, vgv                  → notional / asset value
```

## Amortisation Systems
```
PRICE (French)    → constant instalment, decreasing principal
  instalment = pv * taxa / (1 - (1+taxa)^-n)
  Python: numpy_financial.pmt(rate, nper, -pv)

SAC (Constant)    → constant principal, decreasing instalment
  principal_t = pv / n
  interest_t  = saldo_t * taxa
  Python: loop over periods with saldo -= amortizacao

AMERICAN          → interest-only until final bullet
  interest_t  = saldo * taxa
  principal_t = 0 (except last period)
```

## Universal Edge Cases (Product Pricing)
```
□ Rate = 0 (zero-interest product or promotional period)
□ Rate < 0 (negative rates in some jurisdictions)
□ Term = 0 or Term < 0
□ PV = 0 (zero-value contract)
□ Requested term not in pricing table
□ Client segment not mapped in lookup table
□ Operation value below minimum or above maximum
□ Past maturity date (contract already expired)
□ IOF / fees result in effective rate above legal cap
□ NPV solver non-convergence (IRR undefined for non-monotone flows)
```

## Pattern Notes
```
P8 (Lookup pricing table): extremely common in this domain.
  Excel: ÍNDICE(tabela_taxas, CORRESP(prazo,prazos,0), CORRESP(seg,segs,0))
  Python: pd.DataFrame.at[prazo, segmento] or dict lookup

P9 (Projected cash flow loop): core pattern for SAC and balloon schedules.
  Each row references previous saldo → loop with accumulated state.
  NOT a cycle in the graph-theory sense — it is forward-only iteration.

P7 (Decision tree): eligibility rules nested SE/IF are common.
  Translate as: if/elif/else chain or lookup dict, not np.where,
  since conditions are typically categorical, not array-wise.
```
