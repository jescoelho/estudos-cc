"""
VaR Ibovespa — Modelo Bancário
Derivado de: VaR_Ibovespa_Modelo_Bancario.xlsx
Pipeline: Inventário (Fase 1) → Grafo (Fase 2) → Arquitetura (Fase 3) → Tradução (Fase 4)

Metodologias cobertas:
  - VaR por Simulação Histórica (VaR_HISTÓRICO)
  - VaR Paramétrico Delta-Normal   (VaR_PARAMÉTRICO)
  - Volatilidade EWMA RiskMetrics  (EWMA_VOL)
  - Backtesting Semáforo Basileia  (BACKTESTING)
  - Testes de Estresse             (STRESS_TEST)
  - Monte Carlo (cenários fixos)   (MONTE_CARLO)
  - Resumo Executivo               (RESUMO_EXEC)
"""
from __future__ import annotations

import warnings
from dataclasses import dataclass, field
from typing import Any

import numpy as np
import pandas as pd
from scipy import stats


# ---------------------------------------------------------------------------
# Configuração do modelo (substitui PARÂMETROS — referenciados por coordenada)
# ---------------------------------------------------------------------------

@dataclass
class ModelConfig:
    """
    Parâmetros de configuração do modelo VaR Ibovespa.
    Fonte: PARÂMETROS!B4:B30.
    Nota: planilha original não usa named ranges — coordenadas são frágeis.
    """
    conf_99: float = 0.99           # PARÂMETROS!B4
    conf_95: float = 0.95           # PARÂMETROS!B5
    conf_es: float = 0.975          # PARÂMETROS!B6 — CVaR interno
    horiz_1d: int = 1               # PARÂMETROS!B8
    horiz_10d: int = 10             # PARÂMETROS!B9
    du_ano: int = 252               # PARÂMETROS!B10
    jan_curta: int = 252            # PARÂMETROS!B12
    jan_longa: int = 500            # PARÂMETROS!B13
    n_backtesting: int = 250        # PARÂMETROS!B14
    lambda_ewma: float = 0.94       # PARÂMETROS!B21 — fator de decaimento RiskMetrics
    nocional: float = 10_000_000.0  # PARÂMETROS!B24 — BRL
    zona_verde: int = 4             # PARÂMETROS!B28 — máx. exceções Basileia zona verde
    zona_amarela: int = 9           # PARÂMETROS!B29
    zona_vermelha: int = 10         # PARÂMETROS!B30 — mín. exceções zona vermelha

    # Z-scores hardcoded conforme planilha (NÃO derivados de NORM.INV)
    # VaR_PARAMÉTRICO!B12:B15
    z_99: float = field(default=2.326, init=False)
    z_975: float = field(default=1.960, init=False)
    z_95: float = field(default=1.645, init=False)
    z_90: float = field(default=1.282, init=False)

    def __post_init__(self) -> None:
        if not 0 < self.conf_99 < 1:
            raise ValueError(f"conf_99={self.conf_99} fora de (0,1)")
        if not 0 < self.conf_95 < 1:
            raise ValueError(f"conf_95={self.conf_95} fora de (0,1)")
        if not 0 < self.lambda_ewma < 1:
            raise ValueError(f"lambda_ewma={self.lambda_ewma} fora de (0,1)")
        if self.du_ano <= 0:
            raise ValueError(f"du_ano={self.du_ano} deve ser positivo")
        if self.horiz_10d <= 0:
            raise ValueError(f"horiz_10d={self.horiz_10d} deve ser positivo")
        if self.nocional <= 0:
            raise ValueError(f"nocional={self.nocional} deve ser positivo")
        if self.zona_verde >= self.zona_vermelha:
            raise ValueError("zona_verde deve ser menor que zona_vermelha")


# ---------------------------------------------------------------------------
# Camada 1 — Retornos Logarítmicos
# ---------------------------------------------------------------------------

def calcular_retornos_log(prices: pd.Series) -> pd.Series:
    """
    Retornos logarítmicos diários ln(Pt / Pt-1).
    Computed from: prices (RETORNOS_HIST!B3:B522)
    Used by: var_hist, sigma_daily, ewma_variance, backtest, stress_test, monte_carlo
    """
    # --- Validação de entrada ---
    if len(prices) <= 1:
        raise ValueError("série de preços requer ao menos 2 observações")
    if (prices <= 0).any():
        # EDGE CASE NOT IN ORIGINAL ARTEFACT — added in derivation
        raise ValueError("preços devem ser estritamente positivos (evitar ln(0) ou ln negativo)")
    if prices.isna().any():
        # EDGE CASE NOT IN ORIGINAL ARTEFACT — added in derivation
        raise ValueError("série de preços contém NaN")

    # --- Retornos log --- RETORNOS_HIST!C4:C522
    log_returns = np.log(prices / prices.shift(1)).dropna()
    return log_returns


# ---------------------------------------------------------------------------
# Camada 2 — Estatísticas Descritivas
# ---------------------------------------------------------------------------

def calcular_estatisticas_retornos(
    log_returns: pd.Series,
    du_ano: int = 252,
    prices: pd.Series | None = None,
) -> dict[str, Any]:
    """
    Estatísticas descritivas da série de retornos.
    Computed from: log_returns, du_ano (RETORNOS_HIST!B525:B533)
    Used by: documentação / returns_stats
    """
    # --- Validação ---
    if len(log_returns) <= 1:
        raise ValueError("série de retornos requer ao menos 2 observações")
    if du_ano <= 0:
        raise ValueError("du_ano deve ser positivo")

    # --- Estatísticas --- RETORNOS_HIST!B525:B533
    n = len(log_returns)                                    # RETORNOS_HIST!B525
    mu = log_returns.mean()                                 # RETORNOS_HIST!B526
    sigma_diaria = log_returns.std(ddof=1)                  # RETORNOS_HIST!B527
    retorno_min = log_returns.min()                         # RETORNOS_HIST!B528
    retorno_max = log_returns.max()                         # RETORNOS_HIST!B529
    sigma_anual = sigma_diaria * np.sqrt(du_ano)            # RETORNOS_HIST!B530

    retorno_total = None
    if prices is not None and len(prices) >= 2:
        retorno_total = prices.iloc[-1] / prices.iloc[0] - 1  # RETORNOS_HIST!B533

    return {
        "n": n,
        "mu": mu,
        "sigma_diaria": sigma_diaria,
        "sigma_anual": sigma_anual,
        "retorno_min": retorno_min,
        "retorno_max": retorno_max,
        "retorno_total": retorno_total,
    }


# ---------------------------------------------------------------------------
# Camada 3 — VaR por Simulação Histórica [branch A — P4]
# ---------------------------------------------------------------------------

def calcular_var_historico(
    log_returns: pd.Series,
    conf_99: float,
    conf_95: float,
    horiz_10d: int,
    nocional: float,
) -> dict[str, float]:
    """
    VaR e ES por Simulação Histórica (distribuição empírica).
    Computed from: log_returns, config (VaR_HISTÓRICO!D15:F18)
    Used by: var_param (comparação G19/G20), dashboard
    """
    # --- Validação ---
    if len(log_returns) == 0:
        raise ValueError("série de retornos vazia")
    if not 0 < conf_99 < 1:
        raise ValueError(f"conf_99={conf_99} fora de (0,1)")
    if not 0 < conf_95 < 1:
        raise ValueError(f"conf_95={conf_95} fora de (0,1)")
    if horiz_10d <= 0:
        raise ValueError(f"horiz_10d={horiz_10d} deve ser positivo")
    if nocional <= 0:
        raise ValueError(f"nocional={nocional} deve ser positivo")

    r = log_returns.to_numpy()

    def _var_es(alpha: float) -> tuple[float, float]:
        q = np.percentile(r, (1 - alpha) * 100)    # VaR_HISTÓRICO!D15
        var_1d = abs(q)
        tail = r[r < q]
        if len(tail) == 0:
            # EDGE CASE NOT IN ORIGINAL ARTEFACT — cauda vazia (ES indefinido)
            warnings.warn(f"cauda vazia para conf={alpha:.3f}: ES indefinido, retornando np.nan")
            es_1d = np.nan
        else:
            es_1d = abs(tail.mean())                # VaR_HISTÓRICO!F15 — AVERAGEIF < PERCENTILE
        return var_1d, es_1d

    # --- VaR/ES 99% ---
    var_99_1d, es_99_1d = _var_es(conf_99)
    var_99_1d_brl = var_99_1d * nocional           # VaR_HISTÓRICO!E15
    var_99_10d = var_99_1d * np.sqrt(horiz_10d)    # VaR_HISTÓRICO!D17 — escala √T
    es_99_10d = es_99_1d * np.sqrt(horiz_10d)      # VaR_HISTÓRICO!F17

    # --- VaR/ES 95% ---
    var_95_1d, es_95_1d = _var_es(conf_95)
    var_95_1d_brl = var_95_1d * nocional
    var_95_10d = var_95_1d * np.sqrt(horiz_10d)
    es_95_10d = es_95_1d * np.sqrt(horiz_10d)

    return {
        "var_99_1d_pct": var_99_1d,
        "var_99_1d_brl": var_99_1d_brl,
        "es_99_1d": es_99_1d,
        "var_99_10d_pct": var_99_10d,
        "es_99_10d": es_99_10d,
        "var_95_1d_pct": var_95_1d,
        "var_95_1d_brl": var_95_1d_brl,
        "es_95_1d": es_95_1d,
        "var_95_10d_pct": var_95_10d,
        "es_95_10d": es_95_10d,
    }


# ---------------------------------------------------------------------------
# Camada 4 — VaR Paramétrico Delta-Normal [branch B — P4]
# ---------------------------------------------------------------------------

def calcular_var_parametrico(
    log_returns: pd.Series,
    conf_99: float,
    conf_95: float,
    horiz_10d: int,
    nocional: float,
    var_hist_99_1d: float,
    var_hist_95_1d: float,
    cfg: ModelConfig | None = None,
) -> dict[str, float]:
    """
    VaR Delta-Normal: VaR = z_α · σ · √h.
    Computed from: log_returns, z_scores (hardcoded), config (VaR_PARAMÉTRICO!E19:F22)
    Used by: ewma_var, backtest, stress_test, dashboard
    Note: z-scores são valores hardcoded na planilha (B12=2.326, B14=1.645) —
          NÃO derivados de scipy.stats.norm.ppf.
    """
    # --- Validação ---
    if len(log_returns) <= 1:
        raise ValueError("série de retornos requer ao menos 2 observações")
    if nocional <= 0:
        raise ValueError(f"nocional={nocional} deve ser positivo")

    _cfg = cfg or ModelConfig()
    z_99 = _cfg.z_99    # VaR_PARAMÉTRICO!B12 — hardcoded 2.326
    z_95 = _cfg.z_95    # VaR_PARAMÉTRICO!B14 — hardcoded 1.645

    # --- Volatilidade diária ---
    sigma_diaria = log_returns.std(ddof=1)          # VaR_PARAMÉTRICO!B7
    if sigma_diaria == 0:
        # EDGE CASE NOT IN ORIGINAL ARTEFACT — série constante, VaR=0
        raise ValueError("desvio padrão dos retornos é zero (série constante)")

    mu = log_returns.mean()                         # VaR_PARAMÉTRICO!B6
    n_obs = len(log_returns)                        # VaR_PARAMÉTRICO!B9

    # --- VaR 99% ---
    var_99_1d = z_99 * sigma_diaria * np.sqrt(1)    # VaR_PARAMÉTRICO!E19
    var_99_1d_brl = var_99_1d * nocional            # VaR_PARAMÉTRICO!F19
    var_99_10d = z_99 * sigma_diaria * np.sqrt(horiz_10d)   # VaR_PARAMÉTRICO!E21
    var_99_10d_brl = var_99_10d * nocional          # VaR_PARAMÉTRICO!F21
    diff_99 = var_99_1d - var_hist_99_1d            # VaR_PARAMÉTRICO!G19

    # --- VaR 95% ---
    var_95_1d = z_95 * sigma_diaria * np.sqrt(1)    # VaR_PARAMÉTRICO!E20
    var_95_1d_brl = var_95_1d * nocional            # VaR_PARAMÉTRICO!F20
    var_95_10d = z_95 * sigma_diaria * np.sqrt(horiz_10d)   # VaR_PARAMÉTRICO!E22
    var_95_10d_brl = var_95_10d * nocional
    diff_95 = var_95_1d - var_hist_95_1d            # VaR_PARAMÉTRICO!G20

    return {
        "sigma_diaria": sigma_diaria,
        "mu": mu,
        "n_obs": n_obs,
        "var_99_1d_pct": var_99_1d,
        "var_99_1d_brl": var_99_1d_brl,
        "var_99_10d_pct": var_99_10d,
        "var_99_10d_brl": var_99_10d_brl,
        "var_95_1d_pct": var_95_1d,
        "var_95_1d_brl": var_95_1d_brl,
        "var_95_10d_pct": var_95_10d,
        "var_95_10d_brl": var_95_10d_brl,
        "diff_99_hist_param": diff_99,
        "diff_95_hist_param": diff_95,
    }


# ---------------------------------------------------------------------------
# Camada 5a — Volatilidade EWMA RiskMetrics [branch C — P4 + P9]
# ---------------------------------------------------------------------------

def calcular_ewma_volatilidade(
    log_returns: pd.Series,
    lambda_ewma: float,
    z_99: float,
    nocional: float,
    du_ano: int,
) -> dict[str, Any]:
    """
    Volatilidade EWMA RiskMetrics: σ²_t = λ·σ²_{t-1} + (1-λ)·r²_{t-1}.
    P9 (loop recursivo) — cada período referencia o anterior.
    Seed: σ²₀ = 0 (reproduz EWMA_VOL!D3).
    Computed from: log_returns, lambda_ewma (EWMA_VOL!D3:H528)
    Used by: ewma_var → dashboard
    """
    # --- Validação ---
    if not 0 < lambda_ewma < 1:
        raise ValueError(f"lambda_ewma={lambda_ewma} fora de (0,1)")
    if len(log_returns) == 0:
        raise ValueError("série de retornos vazia")
    if du_ano <= 0:
        raise ValueError("du_ano deve ser positivo")

    r = log_returns.to_numpy()
    n = len(r)

    sigma2 = np.empty(n)
    sigma2[0] = 0.0                             # EWMA_VOL!D3 — seed zero

    # --- Loop recursivo P9 ---
    for t in range(1, n):
        sigma2[t] = lambda_ewma * sigma2[t - 1] + (1 - lambda_ewma) * r[t - 1] ** 2
        # σ²_t = λ·σ²_{t-1} + (1-λ)·r²_{t-1} — EWMA_VOL!D5

    sigma = np.sqrt(sigma2)                     # EWMA_VOL!E — volatilidade condicional diária
    sigma_anual = sigma * np.sqrt(du_ano)        # EWMA_VOL!F — vol anualizada
    var_pct = z_99 * sigma                       # EWMA_VOL!G — VaR EWMA em %
    var_brl = var_pct * nocional                 # EWMA_VOL!H — VaR EWMA em BRL

    idx = log_returns.index
    return {
        "sigma2_series": pd.Series(sigma2, index=idx),
        "sigma_series": pd.Series(sigma, index=idx),
        "sigma_anual_series": pd.Series(sigma_anual, index=idx),
        "var_series": pd.Series(var_pct, index=idx),
        "var_brl_series": pd.Series(var_brl, index=idx),
        "sigma2_atual": float(sigma2[-1]),
        "sigma_atual": float(sigma[-1]),
        "var_atual": float(var_pct[-1]),
        "var_brl_atual": float(var_brl[-1]),
    }


# ---------------------------------------------------------------------------
# Camada 5b — Backtesting Semáforo Basileia [branch D — P4 + P7]
# ---------------------------------------------------------------------------

def calcular_backtesting(
    log_returns: pd.Series,
    var_param_1d_pct: float,
    n_dias: int,
    zona_verde: int,
    zona_vermelha: int,
) -> dict[str, Any]:
    """
    Backtesting Basileia: conta exceções e classifica semáforo de tráfego.
    Computed from: log_returns OOS, var_param (BACKTESTING!B3:C265)
    Used by: dashboard
    """
    # --- Validação ---
    if len(log_returns) < n_dias:
        raise ValueError(
            f"série ({len(log_returns)} obs) menor que janela de backtesting ({n_dias})"
        )
    if var_param_1d_pct <= 0:
        raise ValueError("var_param_1d_pct deve ser positivo")
    if zona_verde >= zona_vermelha:
        raise ValueError("zona_verde deve ser menor que zona_vermelha")

    # --- Janela out-of-sample ---
    r_oos = log_returns.iloc[-n_dias:].to_numpy()       # BACKTESTING!B3:B254

    # --- Flags de exceção ---
    excecoes = r_oos < -var_param_1d_pct                # BACKTESTING!D3 — IF(r < -VaR)
    n_excecoes = int(excecoes.sum())                    # BACKTESTING!B256
    taxa_excecao = n_excecoes / n_dias                  # BACKTESTING!B257

    # --- Semáforo Basileia (P7 — decisão aninhada) --- BACKTESTING!C265
    if n_excecoes >= zona_vermelha:
        semaforo = "ZONA VERMELHA – MODELO SOB REVISÃO"
    elif n_excecoes >= zona_verde:
        semaforo = "ZONA AMARELA – ATENÇÃO"
    else:
        semaforo = "ZONA VERDE – MODELO APROVADO"

    return {
        "n_excecoes": n_excecoes,
        "taxa_excecao": taxa_excecao,
        "semaforo": semaforo,
        "serie_excecoes": pd.Series(excecoes, index=log_returns.index[-n_dias:]),
        "descricao": f"{n_excecoes} exceções em {n_dias} dias",  # BACKTESTING!B258
    }


# ---------------------------------------------------------------------------
# Camada 5c — Testes de Estresse [branch E — P4]
# ---------------------------------------------------------------------------

def calcular_stress_test(
    cenarios: pd.DataFrame,
    var_param_1d_pct: float,
    sigma_diaria: float,
    nocional: float,
) -> pd.DataFrame:
    """
    Testes de estresse históricos e hipotéticos com classificação de severidade.
    Computed from: cenarios, var_param, sigma (STRESS_TEST!B4:H29)
    Used by: output terminal (sem referência downstream)
    Espera cenarios com colunas ['nome', 'retorno_shock'].
    """
    # --- Validação ---
    if len(cenarios) == 0:
        raise ValueError("nenhum cenário de estresse fornecido")
    if var_param_1d_pct <= 0:
        raise ValueError("var_param_1d_pct deve ser positivo")
    if sigma_diaria <= 0:
        # EDGE CASE NOT IN ORIGINAL ARTEFACT — added in derivation
        raise ValueError("sigma_diaria deve ser positivo")
    if nocional <= 0:
        raise ValueError("nocional deve ser positivo")

    resultados = cenarios.copy()

    # --- Perda absoluta e BRL --- STRESS_TEST!D13 / H4
    resultados["perda_absoluta"] = resultados["retorno_shock"].abs()
    resultados["perda_brl"] = resultados["perda_absoluta"] * nocional  # STRESS_TEST!H4

    # --- Razão estresse / VaR --- STRESS_TEST!E13
    resultados["ratio_var"] = resultados["perda_absoluta"] / var_param_1d_pct

    # --- Probabilidade na distribuição normal --- STRESS_TEST!F13
    resultados["prob_normal"] = stats.norm.cdf(
        resultados["retorno_shock"] / sigma_diaria
    )

    # --- Classificação de severidade (P7) --- STRESS_TEST!G13
    def _classificar(ratio: float) -> str:
        if ratio > 3.0:
            return "EXTREMO"
        elif ratio > 1.0:
            return "SEVERO"
        else:
            return "MODERADO"

    resultados["severidade"] = resultados["ratio_var"].apply(_classificar)

    return resultados[
        ["nome", "retorno_shock", "perda_absoluta", "perda_brl",
         "ratio_var", "prob_normal", "severidade"]
    ]


# ---------------------------------------------------------------------------
# Camada 5d — VaR Monte Carlo (cenários pré-gerados) [branch F — P4]
# ---------------------------------------------------------------------------

def calcular_var_monte_carlo(
    cenarios_log: pd.Series | np.ndarray,
    nocional: float,
) -> dict[str, float]:
    """
    VaR e ES Monte Carlo sobre 1 000 cenários pré-gerados (valores fixos).
    Nota: cenários são fixos na planilha — não há re-simulação em runtime.
    Computed from: MONTE_CARLO!B15:B1014
    Used by: dashboard
    """
    # --- Validação ---
    cenarios = np.asarray(cenarios_log, dtype=float)
    if len(cenarios) != 1000:
        raise ValueError(
            f"esperados 1000 cenários (VALORES FIXOS conforme MONTE_CARLO), "
            f"recebido {len(cenarios)}"
        )
    if nocional <= 0:
        raise ValueError("nocional deve ser positivo")

    # --- Retornos simples --- MONTE_CARLO!C15
    retornos_simples = np.exp(cenarios) - 1

    # --- PnL por cenário --- MONTE_CARLO!D15
    pnl = cenarios * nocional

    # --- Quantis VaR --- MONTE_CARLO!B1017:B1020
    var_99_pct = abs(np.percentile(cenarios, 1.0))      # MONTE_CARLO!B1017
    var_99_brl = var_99_pct * nocional                  # MONTE_CARLO!B1018
    var_95_pct = abs(np.percentile(cenarios, 5.0))      # MONTE_CARLO!B1019
    var_95_brl = var_95_pct * nocional                  # MONTE_CARLO!B1020

    # --- Expected Shortfall 99% --- MONTE_CARLO!B1021:B1022
    limiar_99 = np.percentile(cenarios, 1.0)
    cauda_99 = cenarios[cenarios < limiar_99]
    if len(cauda_99) == 0:
        # EDGE CASE NOT IN ORIGINAL ARTEFACT — cauda vazia
        warnings.warn("cauda MC 99% vazia: ES indefinido, retornando np.nan")
        es_99_pct = np.nan
        es_99_brl = np.nan
    else:
        es_99_pct = abs(cauda_99.mean())                # MONTE_CARLO!B1021
        es_99_brl = es_99_pct * nocional                # MONTE_CARLO!B1022

    return {
        "var_99_pct": var_99_pct,
        "var_99_brl": var_99_brl,
        "var_95_pct": var_95_pct,
        "var_95_brl": var_95_brl,
        "es_99_pct": es_99_pct,
        "es_99_brl": es_99_brl,
        "retorno_min": float(cenarios.min()),           # MONTE_CARLO!B1023
        "retorno_max": float(cenarios.max()),           # MONTE_CARLO!B1024
        "retornos_simples": retornos_simples,
        "pnl": pnl,
    }


# ---------------------------------------------------------------------------
# Camada 6 — Resumo Executivo [P3 — agregador]
# ---------------------------------------------------------------------------

def calcular_resumo_executivo(
    var_hist: dict[str, float],
    var_param: dict[str, float],
    ewma: dict[str, Any],
    monte_carlo: dict[str, float],
    backtest: dict[str, Any],
    nocional: float,
    limite_var_pct: float = 0.05,
) -> dict[str, Any]:
    """
    Agregação executiva de todas as métricas de risco de mercado.
    P3 — in-degree=6. Computed from: todos os branches (RESUMO_EXEC)
    Used by: output final
    """
    # --- Coleta VaRs 99% 1d de cada metodologia --- RESUMO_EXEC!C14:C19
    vars_99_1d = {
        "var_historico_99_1d":    var_hist["var_99_1d_pct"],    # RESUMO_EXEC!C14
        "var_parametrico_99_1d":  var_param["var_99_1d_pct"],   # RESUMO_EXEC!C16
        "var_ewma_atual":         ewma["var_atual"],             # RESUMO_EXEC!C18 (scaled)
        "var_mc_95":              monte_carlo["var_95_pct"],     # RESUMO_EXEC!C19
    }

    max_var_pct = max(vars_99_1d.values())                      # RESUMO_EXEC!B23
    max_var_brl = max_var_pct * nocional

    # --- Alerta de limite (P7) --- RESUMO_EXEC!B24
    if max_var_pct > limite_var_pct:
        alerta_limite = "⚠ ATENÇÃO – EXCEDE LIMITE"
    else:
        alerta_limite = "✓ DENTRO DO LIMITE"

    return {
        "vars_por_metodologia": vars_99_1d,
        "max_var_pct": max_var_pct,
        "max_var_brl": max_var_brl,
        "semaforo_backtesting": backtest["semaforo"],            # RESUMO_EXEC!B22
        "n_excecoes": backtest["n_excecoes"],                    # RESUMO_EXEC!B25
        "taxa_excecao": backtest["taxa_excecao"],
        "alerta_limite": alerta_limite,                          # RESUMO_EXEC!B24
        "limite_var_referencia": limite_var_pct,
    }


# ---------------------------------------------------------------------------
# Ponto de entrada principal
# ---------------------------------------------------------------------------

def var_ibovespa_modelo_bancario(
    prices: pd.Series,
    cenarios_mc: pd.Series | np.ndarray,
    cenarios_stress: pd.DataFrame,
    cfg: ModelConfig | None = None,
) -> dict[str, Any]:
    """
    Modelo completo de VaR Ibovespa — Bancário.
    Executa todas as metodologias na ordem topológica derivada do grafo.

    Parâmetros
    ----------
    prices : pd.Series
        Série de preços de fechamento do Ibovespa, indexada por data.
        Fonte: RETORNOS_HIST!B3:B522
    cenarios_mc : pd.Series | np.ndarray
        1 000 log-retornos pré-gerados (valores fixos).
        Fonte: MONTE_CARLO!B15:B1014
    cenarios_stress : pd.DataFrame
        Cenários de estresse com colunas ['nome', 'retorno_shock'].
        Fonte: STRESS_TEST!B4:B29
    cfg : ModelConfig, opcional
        Parâmetros do modelo. Default usa valores da planilha PARÂMETROS.

    Retorna
    -------
    dict com chaves: retornos, estatisticas, var_historico, var_parametrico,
                     ewma, backtesting, stress_test, monte_carlo, resumo_executivo
    """
    _cfg = cfg or ModelConfig()

    # --- Camada 1: Retornos Logarítmicos ---
    log_returns = calcular_retornos_log(prices)

    # --- Camada 2: Estatísticas ---
    estatisticas = calcular_estatisticas_retornos(log_returns, _cfg.du_ano, prices)

    # --- Camada 3: VaR Histórico [branch A] ---
    var_hist = calcular_var_historico(
        log_returns, _cfg.conf_99, _cfg.conf_95, _cfg.horiz_10d, _cfg.nocional
    )

    # --- Camada 4: VaR Paramétrico [branch B] ---
    var_param = calcular_var_parametrico(
        log_returns,
        _cfg.conf_99, _cfg.conf_95,
        _cfg.horiz_10d, _cfg.nocional,
        var_hist["var_99_1d_pct"],
        var_hist["var_95_1d_pct"],
        _cfg,
    )

    # --- Camada 5 [branches paralelas C/D/E/F] ---
    ewma = calcular_ewma_volatilidade(
        log_returns, _cfg.lambda_ewma, _cfg.z_99, _cfg.nocional, _cfg.du_ano
    )

    backtest = calcular_backtesting(
        log_returns,
        var_param["var_99_1d_pct"],
        _cfg.n_backtesting,
        _cfg.zona_verde,
        _cfg.zona_vermelha,
    )

    stress = calcular_stress_test(
        cenarios_stress,
        var_param["var_99_1d_pct"],
        var_param["sigma_diaria"],
        _cfg.nocional,
    )

    mc = calcular_var_monte_carlo(cenarios_mc, _cfg.nocional)

    # --- Camada 6: Resumo Executivo [P3] ---
    resumo = calcular_resumo_executivo(
        var_hist, var_param, ewma, mc, backtest, _cfg.nocional
    )

    return {
        "retornos": log_returns,
        "estatisticas": estatisticas,
        "var_historico": var_hist,
        "var_parametrico": var_param,
        "ewma": ewma,
        "backtesting": backtest,
        "stress_test": stress,
        "monte_carlo": mc,
        "resumo_executivo": resumo,
    }
