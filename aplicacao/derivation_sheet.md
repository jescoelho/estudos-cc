# Planilha de Derivação Consolidada — VaR Ibovespa Modelo Bancário

**Artefato de origem:** `VaR_Ibovespa_Modelo_Bancario.xlsx`
**Artefato gerado:** `VaR_Ibovespa_Modelo_Bancario.py`
**Domínio:** Risco de Mercado

---

## FASE 1 — INVENTÁRIO

| Aba | Linhas | Colunas | Tipo | Observação |
|---|---|---|---|---|
| CAPA | 28 | 8 | Auxiliar | Capa descritiva, sem fórmulas |
| PARÂMETROS | 30 | 6 | Parâmetros | Sem named ranges — coordenadas frágeis |
| RETORNOS_HIST | 533 | 6 | Entrada/Cálculo | 519 obs log-retornos Jan/2022–Dez/2023 |
| VaR_HISTÓRICO | 39 | 7 | Cálculo | VaR Hist 99%/95% 1d+10d + ES |
| VaR_PARAMÉTRICO | 22 | 7 | Cálculo | Delta-Normal; z-scores hardcoded |
| EWMA_VOL | 529 | 8 | Cálculo | Recursão EWMA linha a linha |
| BACKTESTING | 265 | 7 | Cálculo/Saída | 252 dias OOS + semáforo Basileia |
| STRESS_TEST | 29 | 8 | Cálculo | Cenários históricos e hipotéticos |
| MONTE_CARLO | 1024 | 11 | Cálculo | 1000 cenários FIXOS pré-gerados |
| RESUMO_EXEC | 28 | 8 | Saída | Dashboard agregador |

**Named Ranges:** NÃO ENCONTRADO — risco de documentação

**VBA/Macros:** NÃO DETECTADO (.xlsx)

---

## FASE 2 — GRAFO ENRIQUECIDO

| Métrica | Valor |
|---|---|
| Total de nós L2 | 14 |
| Total de arestas | 25 |
| Nós INPUT | config, prices, z_scores |
| Nós OUTPUT | dashboard, stress_test, returns_stats |
| Nós CRÍTICOS (betweenness > 0,30) | config (~0,55), log_returns (~0,48), var_param (~0,35) |
| Nós ISOLADOS | NENHUM |
| Ciclos | NENHUM |

---

## FASE 3 — ARQUITETURA

| Padrão | Nós |
|---|---|
| P2 Hub Central | config, log_returns, var_param |
| P3 Agregador | dashboard |
| P4 Branches Paralelas | var_hist / var_param / ewma / backtest / stress / mc → dashboard |
| P7 Árvore de Decisão | backtest (semáforo), stress_test (severidade), resumo (alerta) |
| P9 Loop Série Temporal | ewma_variance |

**Funções derivadas:** 8 sub-funções + 1 ponto de entrada (`var_ibovespa_modelo_bancario`)

---

## FASE 4 — TRADUÇÃO E AUDITORIA

### 4.3 — Completude

| Nó L2 | Coberto no código | Confiança |
|---|---|---|
| config | `ModelConfig` (dataclass) | ALTA |
| prices | argumento de entrada | ALTA |
| log_returns | `calcular_retornos_log()` | ALTA |
| returns_stats | `calcular_estatisticas_retornos()` | ALTA |
| var_hist | `calcular_var_historico()` | ALTA |
| sigma_daily | `calcular_var_parametrico()` → sigma_diaria | ALTA |
| z_scores | `ModelConfig.z_99 / z_95` (hardcoded) | ALTA |
| var_param | `calcular_var_parametrico()` | ALTA |
| ewma_variance | `calcular_ewma_volatilidade()` → loop P9 | ALTA |
| ewma_var | `calcular_ewma_volatilidade()` → var_series | ALTA |
| backtest | `calcular_backtesting()` | ALTA |
| stress_test | `calcular_stress_test()` | ALTA |
| monte_carlo | `calcular_var_monte_carlo()` | ALTA |
| dashboard | `calcular_resumo_executivo()` | ALTA |

**Cobertura: 14/14 (100%)**

### 4.4 — Ordem de Execução

Ordem topológica respeitada em `var_ibovespa_modelo_bancario()`:
1. `calcular_retornos_log` → 2. `calcular_estatisticas_retornos` → 3. `calcular_var_historico`
→ 4. `calcular_var_parametrico` → 5. [branches paralelas C/D/E/F] → 6. `calcular_resumo_executivo`

**Violações: NENHUMA**

### 4.5 — Arquitetura

| Critério | Resultado |
|---|---|
| C1 Acoplamento | BAIXO — cada função recebe apenas predecessores diretos do grafo |
| C2 Coesão | ALTA — cada função implementa exatamente um nó L2 |
| C3 Comprimento | Todas as funções ≤ 60 linhas |
| C4 Variáveis globais | NENHUMA |
| C5 Rastreabilidade | Comentários inline com referência Excel em cada linha de cálculo |
| C6 Cobertura de casos-borda | 100% dos casos de A.6 documentados; 6 casos adicionados |

### Casos-borda adicionados (não na planilha original)

| Caso | Localização | Motivo |
|---|---|---|
| Preço ≤ 0 → raise | `calcular_retornos_log` | ln(0) = -∞ |
| NaN em prices → raise | `calcular_retornos_log` | propagação silenciosa |
| σ̂ = 0 → raise | `calcular_var_parametrico` | VaR=0 sem sentido econômico |
| Cauda ES vazia → warn + nan | `calcular_var_historico`, `calcular_var_monte_carlo` | ES indefinido |
| σ_stress ≤ 0 → raise | `calcular_stress_test` | divisão por zero em NORM.DIST |
| du_ano ≤ 0, h ≤ 0 → raise | `ModelConfig.__post_init__` | raiz quadrada de negativo |

---

## ITENS PARA O USUÁRIO

| Tipo | Item |
|---|---|
| Observação | Planilha não usa named ranges — `ModelConfig` é a abstração equivalente |
| Observação | z-scores (2,326 / 1,645) são hardcoded na planilha; reproduzidos como constantes |
| Observação | Cenários Monte Carlo são FIXOS na planilha; código espera o array como input |
| Observação | Seed EWMA σ²₀=0 reproduz comportamento da planilha; afeta ~11 primeiros períodos |
| Sugestão | Substituir z_scores hardcoded por `scipy.stats.norm.ppf(conf)` para maior flexibilidade |
| Sugestão | Adicionar índice de datas à série `prices` para rastreabilidade temporal completa |

---

## STATUS FINAL

```
╔══════════════════════════════════════════════════════╗
║  DERIVATION — PHASE 4                               ║
╠══════════════════════════════════════════════════════╣
║ Fórmulas traduzidas  : 14 nós → 8 funções + 1 main ║
║  Confiança ALTA      : 14/14                        ║
║  Confiança MÉDIA     : 0                            ║
║  Confiança BAIXA     : 0                            ║
║  Casos-borda cobertos: todos os de A.6              ║
║  Casos-borda adicionados: 6                         ║
╠══════════════════════════════════════════════════════╣
║ AUDIT 4.3 — Nós cobertos: 14/14 (100%)             ║
║ AUDIT 4.4 — Violações de ordem: NENHUMA             ║
║ AUDIT 4.5 — Blockers: NENHUM                       ║
╠══════════════════════════════════════════════════════╣
║ STATUS PHASE 4: COMPLETO                            ║
╚══════════════════════════════════════════════════════╝
```
