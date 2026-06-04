# Domain Reference — ALM / Balance Sheet

Covers: IRRBB, NII, EVE, duration gap, NMD modelling, repricing gap,
        liquidity buffer, funding gap.

## Library Signals
```
numpy              → vectorised gap calculations, cash flow arrays
pandas             → balance sheet as DataFrame indexed by maturity bucket
scipy.optimize     → rate sensitivity solvers
scipy.interpolate  → yield curve interpolation
```

## Excel Formula Signals
```
=SOMAPRODUTO(saldo, duration)  → weighted average duration
=DESLOC(ref, bucket, 0)        → dynamic reference to maturity bucket
=SOMASES(saldo, tipo, "NMD")   → conditional balance aggregation
=VP(taxa, prazo, fluxo)        → present value of repricing cash flow
=SOMA(gap_bucket_1:gap_bucket_N) → cumulative gap
Δ EVE = Σ ΔPVBP × Δtaxa       → EVE sensitivity
```

## Named Range Signals
```
saldo_ativo, saldo_passivo     → asset / liability balances
duration_ativo, duration_passivo → portfolio duration
taxa_repricing                 → repricing rate
bucket_prazo                   → maturity bucket labels
beta_deposito, decay_nmd       → NMD behavioural parameters
choque_paralelo, choque_inclinacao → rate shock scenarios (IRRBB)
nii_base, nii_stress           → net interest income
eve_base, eve_stress           → economic value of equity
```

## Universal Edge Cases (ALM)
```
□ Maturity bucket with zero balance
□ NMD decay rate = 0 or = 1
□ Rate shock producing negative rates
□ Duration gap = 0 (immunised portfolio)
□ Missing repricing data for a bucket
□ FTP curve not available for given tenor
```

---

# Domain Reference — Insurance

Covers: premium pricing, frequency/severity, IBNR reserving,
        loss ratio, combined ratio, reinsurance.

## Library Signals
```
scipy.stats        → frequency/severity distributions (Poisson, Pareto, LogNormal)
numpy              → claim simulation
lifelines          → survival analysis for claim development
```

## Excel Formula Signals
```
=POISSON(k, lambda, FALSE)     → Poisson PMF (claim frequency)
=LOGNORM.DIST(x, mu, sigma)    → log-normal CDF (claim severity)
=SOMA(sinistros)/SOMA(premios) → loss ratio
sinistro_esperado = freq × sev → pure premium formula
IBNR = reserva - pago          → incurred but not reported
=TAXA_CRESCIMENTO(serie, n)    → trend factor for claim development
```

## Named Range Signals
```
frequencia_sinistro            → claim frequency rate
severidade_media               → average claim severity
premio_puro                    → pure premium
loading_despesa, loading_lucro → expense and profit loadings
triangulo_desenvolvimento      → claims development triangle
fator_IBNR                     → IBNR development factor
```

## Universal Edge Cases (Insurance)
```
□ Frequency = 0 (no claims in period)
□ Severity distribution with heavy tail (infinite variance)
□ Premium below technical minimum
□ Development triangle with missing cells
□ Reinsurance attachment = 0 (full cession)
```

---

# Domain Reference — Profitability / FTP / Rentability

Covers: transfer pricing, spread decomposition, product margin,
        cost allocation, risk-adjusted return (RAROC).

## Library Signals
```
numpy              → spread and margin vectorisation
pandas             → P&L by product/segment as DataFrame
scipy.interpolate  → FTP curve interpolation by tenor
```

## Excel Formula Signals
```
=spread_cliente - custo_captacao - custo_risco - custo_op
  → net margin decomposition
=PROCV(prazo, curva_ftp, 2, 1) → FTP rate lookup by tenor
=resultado/capital_alocado     → RAROC
=receita_financeira - despesa_captacao → NIM (net interest margin)
=SOMASES(resultado, produto, "CC") → P&L by product
```

## Named Range Signals
```
taxa_cliente, spread_cliente   → client rate / spread
custo_captacao, ftp_rate       → funding cost / FTP rate
custo_risco, provisao_esperada → expected loss charge
custo_operacional              → operating cost per unit
capital_alocado                → allocated regulatory/economic capital
raroc, nim, margem_liquida     → return metrics
```

## Universal Edge Cases (Profitability)
```
□ FTP rate not available for exact tenor (interpolation needed)
□ Allocated capital = 0 (RAROC undefined)
□ Negative net margin (below floor — regulatory concern)
□ Operating cost allocation with zero denominator (no volume)
□ Missing segment mapping for cost allocation
```

---

# Domain Reference — Scoring / Behavioural Propensity

Covers: churn models, LTV estimation, product propensity,
        price elasticity, customer lifetime value, attrition.
NOTE: credit scoring (PD models) is EXCLUDED from this skill.

## Library Signals
```
sklearn            → LogisticRegression, RandomForest, GradientBoosting
xgboost/lightgbm   → gradient boosted scoring models
tensorflow/torch   → deep learning propensity
shap               → feature importance / explainability
lifetimes          → BG/NBD, Pareto/NBD for LTV
statsmodels        → logistic regression with statistical inference
pandas             → feature engineering pipeline
```

## Excel Formula Signals
```
=SE(score > limiar, "Alto", SE(score > limiar2, "Médio", "Baixo"))
  → score banding / segmentation
=SOMAPRODUTO(pesos, features)  → linear scoring
=EXP(logit)/(1+EXP(logit))     → logistic transformation
=FREQUÊNCIA(scores, bandas)    → score distribution
```

## Named Range Signals
```
score, prob_churn, prob_compra → output probability ∈ [0,1]
limiar_alto, limiar_medio      → decision thresholds
pesos_modelo                   → model coefficients
features                       → input feature vector
ltv, receita_esperada          → lifetime value metrics
elasticidade_preco             → price elasticity
```

## Universal Edge Cases (Scoring)
```
□ Score outside [0,1] (logistic output clipping)
□ Feature with all-zero values (constant predictor)
□ Missing feature value (imputation or rejection rule)
□ Threshold producing 0 positives or 0 negatives
□ LTV with negative margin per period
□ Elasticity = 0 (perfectly inelastic demand)
```

---

# Domain Reference — Generic (Domain Unclear or Mixed)

Use when domain cannot be determined from library signals,
named ranges, or formula patterns, or when model spans multiple domains.

## Library Signals — Broad
```
numpy, pandas      → any quantitative model
scipy              → optimisation, statistics, signal processing
sklearn            → machine learning
matplotlib         → visualisation only — does not affect logic
openpyxl/xlrd      → Excel I/O layer
sqlalchemy         → database-connected model
requests/httpx     → API-connected model (external data source)
```

## Universal Edge Cases (Generic)
```
□ Empty input array / DataFrame
□ NaN in any numeric input
□ Division by zero
□ Negative value where positive expected
□ Array shape mismatch in matrix operations
□ Lookup key not found in mapping
□ Date in the past where future date expected
□ Denominator = 0 in rate or ratio calculations
```

## Pattern Notes
```
When domain is unclear, apply all 9 structural patterns (P1–P9)
and flag any that require domain confirmation before translation.
Produce function stubs with TODO comments for domain-specific logic
rather than guessing the correct formula mapping.
```
