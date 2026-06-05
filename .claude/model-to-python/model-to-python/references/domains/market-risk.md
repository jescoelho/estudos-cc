# Domain Reference — Market Risk

## Library Signals
```
numpy              → vectorised operations, matrix algebra
pandas             → time series, market data indexed by date
scipy.stats        → distributions, statistical tests, parametric VaR
scipy.optimize     → parameter calibration
scipy.linalg       → Cholesky decomposition → correlated MC
statsmodels        → GARCH, econometric models
QuantLib           → derivative pricing
pyfolio/empyrical  → portfolio risk metrics
numba/cython       → performance-critical MC
arch               → ARCH/GARCH, filtered HS
```

## Excel Formula Signals
```
=PERCENTIL / =PERCENTILE     → VaR quantile
=DESVPAD / =STDEV            → volatility σ
=PRODUTO / =PRODUCT(1+range) → compounded return
=LN(Pt/Pt-1)                 → log return
=INV.NORM / =NORM.INV        → z-score (parametric VaR)
=DIST.NORM / =NORM.DIST      → CDF normal
=CONT.SE / =COUNTIF(<VaR)    → exception count (backtesting)
=MÉDIA(SE(...)) / AVERAGEIF  → Expected Shortfall
σ²ₜ=λσ²+(1-λ)r²             → EWMA volatility
```

## Named Range Signals
```
conf_99, conf_95, alpha      → confidence level ∈ (0,1)
horizon, horiz_10d           → holding period (days)
lookback, du_ano             → lookback window (business days)
lambda_ewma                  → EWMA decay factor ∈ (0,1)
nocional, notional           → position notional value
z_alpha                      → z-score for confidence level
zona_verde, zona_vermelha    → Basel traffic light thresholds
serie_rt, returns            → return series (pd.Series)
```

## Domain Segments
```
VaR / ES           → Historical Simulation, Parametric, MC, Filtered HS
Greeks             → Delta, Gamma, Vega, Theta, Rho via finite difference
PnL Attribution    → Taylor expansion decomposition
Stress Testing     → scenario shocks, factor perturbations
Backtesting        → Kupiec, Christoffersen, traffic light
FRTB               → ES_R, ES_F, NMRF, PLAT, liquidity horizons
```

## Universal Edge Cases (Market Risk)
```
□ Empty return series
□ Single-element series
□ NaN or Inf in input
□ Zero denominator
□ Lookback > series length
□ alpha outside (0,1)
□ horizon ≤ 0
□ Non-positive-definite covariance matrix
□ Empty tail (ES undefined)
□ Constant series (σ = 0)
```

## Pattern Notes
```
P4 (Parallel): branches are typically
  HISTORICAL × PARAMETRIC × EWMA × MONTE_CARLO × BACKTESTING
  Each branch independent; all converge to summary aggregator.

P9 (Projected cash flow): rare in pure market risk;
  appears in bond pricing sub-models.
```
