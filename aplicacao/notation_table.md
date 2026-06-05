# Tabela de Notação — VaR Ibovespa Modelo Bancário

Modelo derivado de: `VaR_Ibovespa_Modelo_Bancario.xlsx`
Domínio: Risco de Mercado — VaR / ES / EWMA / Backtesting / Stress / Monte Carlo

| Símbolo | Tipo | Significado de domínio | Restrição | Fonte |
|---|---|---|---|---|
| {r_t} | vetor de reais | retornos logarítmicos diários: ln(Pt/Pt-1) | — | RETORNOS_HIST!C4:C522 |
| prices | vetor de reais | preços de fechamento do Ibovespa | > 0 | RETORNOS_HIST!B3:B522 |
| μ̂ | real | média amostral dos retornos log (ddof=1) | — | RETORNOS_HIST!B526 |
| σ̂ | real | desvio padrão amostral diário (ddof=1) | > 0 | RETORNOS_HIST!B527 / VaR_PARAMÉTRICO!B7 |
| σ̂_anual | real | volatilidade anualizada: σ̂·√N | > 0 | RETORNOS_HIST!B530 |
| n | inteiro | número de observações na série | > 1 | RETORNOS_HIST!B525 |
| N | inteiro | dias úteis por ano (convenção brasileira) | = 252 | PARÂMETROS!B10 |
| α₉₉ | real | nível de confiança principal | ∈ (0,1) | PARÂMETROS!B4 |
| α₉₅ | real | nível de confiança secundário | ∈ (0,1) | PARÂMETROS!B5 |
| h | inteiro | horizonte temporal em dias úteis | > 0 | PARÂMETROS!B9 |
| λ | real | fator de decaimento EWMA (RiskMetrics) | ∈ (0,1) | PARÂMETROS!B21 |
| V | real | valor nocional da posição em BRL | > 0 | PARÂMETROS!B24 |
| n_bt | inteiro | janela de backtesting (dias úteis) | > 0 | PARÂMETROS!B14 |
| z₉₉ | real | quantil normal padrão unilateral 99% | = 2,326 (HARDCODED) | VaR_PARAMÉTRICO!B12 |
| z₉₇₅ | real | quantil normal padrão bilateral 97,5% | = 1,960 (HARDCODED) | VaR_PARAMÉTRICO!B13 |
| z₉₅ | real | quantil normal padrão unilateral 95% | = 1,645 (HARDCODED) | VaR_PARAMÉTRICO!B14 |
| z₉₀ | real | quantil normal padrão unilateral 90% | = 1,282 (HARDCODED) | VaR_PARAMÉTRICO!B15 |
| VaR_{α,h} | real | Value at Risk ao nível α, horizonte h, em % do nocional | ≥ 0 | derivado |
| VaR_{α,h,V} | real | Value at Risk em BRL = VaR_{α,h} · V | ≥ 0 | derivado |
| ES_{α,h} | real | Expected Shortfall (CVaR) ao nível α: média da cauda | ≥ VaR_{α,h} | derivado |
| q_p(x) | real | quantil de probabilidade p da série x | p ∈ (0,1) | derivado |
| σ²_t | real | variância condicional EWMA no período t | ≥ 0 | EWMA_VOL!D |
| σ_t | real | volatilidade condicional EWMA: √σ²_t | ≥ 0 | EWMA_VOL!E |
| Φ(·) | função | CDF da distribuição normal padrão | imagem ∈ (0,1) | STRESS_TEST!F13 = NORM.DIST |
| zona_verde | inteiro | máximo de exceções permitido (semáforo verde Basileia) | = 4 | PARÂMETROS!B28 |
| zona_vermelha | inteiro | mínimo de exceções para rejeição (semáforo vermelho) | = 10 | PARÂMETROS!B30 |
| Σ | operador | somatório sobre índice | — | notação matemática |
| √ | operador | raiz quadrada (argumento ≥ 0) | — | notação matemática |
| \|·\| | operador | valor absoluto | — | notação matemática |
| ← | operador | atribuição de valor | — | notação pseudocódigo |
| ln(·) | função | logaritmo natural | argumento > 0 | RETORNOS_HIST!C4 = LN(B4/B3) |
| exp(·) | função | exponencial (inversa do ln) | — | MONTE_CARLO!C15 = EXP(B15)-1 |
| mean(·) | função | média aritmética simples | série não-vazia | RETORNOS_HIST!B526 = AVERAGE |
| std(·, ddof=1) | função | desvio padrão amostral (Bessel) | série com ≥ 2 obs | RETORNOS_HIST!B527 = STDEV |
| max(·) | função | valor máximo de um conjunto | — | RESUMO_EXEC!B23 |

---

## Notas de Auditoria

| Aspecto | Observação |
|---|---|
| z-scores hardcoded | z₉₉=2,326 e z₉₅=1,645 são valores fixos na planilha (VaR_PARAMÉTRICO!B12/B14). Na planilha original não são derivados via NORM.INV — reproduzidos como constantes no código. |
| Seed EWMA | σ²₀=0 reproduz EWMA_VOL!D3. Afeta os primeiros ~11 períodos (half-life de λ=0,94). |
| Cenários MC | MONTE_CARLO!B15:B1014 são valores fixos pré-gerados. O código Python os recebe como input — não há re-simulação. |
| Named ranges ausentes | A planilha não usa named ranges. Todos os parâmetros são referenciados por coordenada (ex: PARÂMETROS!B4). No Python, substituídos por `ModelConfig`. |
