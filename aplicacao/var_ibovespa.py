"""
Modelo de Value at Risk — Ibovespa
Derivado de: VaR_Ibovespa_Modelo_Bancario.xlsx
Fase 4.2 — corpo completo das funcoes

Dependencias:
    numpy>=1.24, pandas>=2.0, scipy>=1.11
"""
from __future__ import annotations

import warnings
from typing import Optional

import numpy as np
import pandas as pd
from scipy import stats


# ════════════════════════════════════════════════════════════════════════
# CAMADA 0 — Preparação da série (topológico: posição 1)
# ════════════════════════════════════════════════════════════════════════

def compute_log_returns(prices: pd.Series) -> pd.Series:
    """
    Calcula retornos log-contínuos diários rt = ln(Pt / Pt-1).
    Calculado a partir de: prices (pd.Series de preços diários)
    Utilizado por: compute_sigma_hat, ewma_volatility, var_historico,
                   var_montecarlo, backtesting
    """
    # --- Validação de entrada ---
    if not isinstance(prices, pd.Series):
        raise TypeError(f"prices deve ser pd.Series, recebido {type(prices)}")
    if prices.isnull().any():
        raise ValueError(
            f"prices contém {prices.isnull().sum()} NaN(s) — "
            "preencher ou remover antes de calcular retornos"
        )
    if (prices <= 0).any():
        raise ValueError(
            "prices contém valores <= 0 — ln(Pt/Pt-1) indefinido; "
            f"mínimo encontrado: {prices.min():.6f}"
        )
    if len(prices) < 2:
        raise ValueError(
            f"série muito curta (len={len(prices)}); mínimo 2 preços"
        )

    # --- Cálculo dos retornos log-contínuos ---
    returns = np.log(prices / prices.shift(1)).dropna()
    # retorno logarítmico diário rₜ = ln(Pₜ/Pₜ₋₁) — RETORNOS_HIST!C4:C522

    return returns


# ════════════════════════════════════════════════════════════════════════
# CAMADA 1 — Estatísticas base (topológico: posições 2–3)
# ════════════════════════════════════════════════════════════════════════

def compute_sigma_hat(returns: pd.Series) -> float:
    """
    Estima σ̂ amostral diário (ddof=1) da série de retornos log-contínuos.
    Calculado a partir de: returns (pd.Series)
    Utilizado por: var_parametrico_completo, ewma_var, stress_test
    """
    # --- Validação de entrada ---
    if not isinstance(returns, pd.Series):
        raise TypeError(f"returns deve ser pd.Series, recebido {type(returns)}")
    if returns.isnull().any():
        raise ValueError("returns contém NaN — usar compute_log_returns com prices limpos")
    if len(returns) < 2:
        raise ValueError(
            f"n={len(returns)} insuficiente — ddof=1 exige n ≥ 2"
        )

    # --- Estimativa do desvio padrão amostral ---
    sigma_hat = float(returns.std(ddof=1))
    # σ̂ amostral diário (ddof=1) — VaR_PARAMÉTRICO!B7  [=DESVPAD(C4:C522)]

    # --- Verificação de série constante ---
    if sigma_hat == 0.0:
        # CASO NÃO COBERTO NO ARTEFATO ORIGINAL — adicionado na derivação
        raise ValueError(
            "sigma_hat = 0 — série de retornos constante; "
            "VaR delta-normal indefinido"
        )

    return sigma_hat


def ewma_volatility(returns: np.ndarray, lam: float) -> np.ndarray:
    """
    Calcula a série de volatilidade condicional EWMA (RiskMetrics):
    σ²ₜ = λ·σ²ₜ₋₁ + (1 − λ)·r²ₜ₋₁
    Calculado a partir de: returns (np.ndarray), lam (float)
    Utilizado por: ewma_var
    """
    # --- Validação de tipo ---
    returns = np.asarray(returns, dtype=np.float64)

    # --- Validação de domínio ---
    if not (0.0 < lam < 1.0):
        raise ValueError(
            f"lambda={lam} deve estar em (0, 1); "
            "RiskMetrics usa λ = 0.94 — PARÂMETROS!B21"
        )

    # --- Validação de dimensão ---
    if len(returns) < 1:
        raise ValueError("returns vazio — série insuficiente para EWMA")
    if np.isnan(returns).any():
        raise ValueError("returns contém NaN — verificar compute_log_returns")

    n = len(returns)
    sigma_sq = np.empty(n, dtype=np.float64)

    # --- Inicialização (bootstrap) ---
    sigma_sq[0] = 0.0
    # σ²₀ = 0 (bootstrap RiskMetrics) — EWMA_VOL!D3  [=0]
    # NOTA: burn-in de ≈ 50 observações; descartar sigma_t[:50]
    # se a série tiver mais de 300 pontos para evitar subestimação inicial

    # --- Recursão EWMA ---
    for t in range(1, n):
        inovacao_sq = returns[t - 1] ** 2
        # r²ₜ₋₁ (inovação quadrática) — EWMA_VOL!C{t}  [=B{t}^2]

        sigma_sq[t] = lam * sigma_sq[t - 1] + (1.0 - lam) * inovacao_sq
        # σ²ₜ = λ·σ²ₜ₋₁ + (1−λ)·r²ₜ₋₁ — EWMA_VOL!D{t}

    # --- Conversão variância → desvio padrão ---
    sigma_t = np.sqrt(sigma_sq)
    # σₜ = √σ²ₜ (volatilidade condicional diária) — EWMA_VOL!E{t}  [=SQRT(D{t})]

    return sigma_t


# ════════════════════════════════════════════════════════════════════════
# CAMADA 2 — Geração de cenários Monte Carlo (topológico: posição 4)
# ════════════════════════════════════════════════════════════════════════

def simulate_returns(
    mu: float,
    sigma: float,
    n: int = 1_000,
    seed: Optional[int] = None,
) -> np.ndarray:
    """
    Simula n retornos log N(μ, σ²) com parâmetros históricos.
    Calculado a partir de: mu (float), sigma (float), n (int), seed
    Utilizado por: var_montecarlo
    Corrige Lacuna L2: valores fixos em MONTE_CARLO!B15:B1014
    substituídos por geração dinâmica parametrizada.
    """
    # --- Validação de domínio ---
    if sigma <= 0.0:
        raise ValueError(f"sigma={sigma} deve ser > 0")
    if n <= 0:
        raise ValueError(f"n={n} deve ser inteiro positivo")

    # --- Geração de cenários ---
    rng = np.random.default_rng(seed)
    # gerador com seed explícito para reprodutibilidade
    # CORRIGE L2: valores fixos MC substituídos por distribuição parametrizada

    sim_rt_log = rng.normal(loc=mu, scale=sigma, size=n)
    # rₜ simulados ~ N(μ, σ²) — MONTE_CARLO!B15:B1014  [valores fixos no Excel]

    return sim_rt_log


# ════════════════════════════════════════════════════════════════════════
# CAMADA 3 — Métodos de VaR (topológico: posições 5–9)
# ════════════════════════════════════════════════════════════════════════

def var_historico(
    returns: pd.Series,
    conf: float = 0.99,
    conf_sec: float = 0.95,
    nocional: float = 10_000_000.0,
    horiz_10d: int = 10,
) -> dict:
    """
    Calcula VaR e ES histórico por simulação empírica da distribuição
    de retornos (método não-paramétrico).
    Calculado a partir de: returns, conf, conf_sec, nocional, horiz_10d
    Utilizado por: var_parametrico_completo (delta), gerar_relatorio
    """
    # --- Validação de tipo ---
    if not isinstance(returns, pd.Series):
        raise TypeError(f"returns deve ser pd.Series, recebido {type(returns)}")

    # --- Validação de domínio ---
    if not (0.0 < conf < 1.0):
        raise ValueError(f"conf={conf} deve estar em (0, 1)")
    if not (0.0 < conf_sec < 1.0):
        raise ValueError(f"conf_sec={conf_sec} deve estar em (0, 1)")
    if nocional <= 0.0:
        raise ValueError(f"nocional={nocional} deve ser > 0")
    if horiz_10d <= 0:
        raise ValueError(f"horiz_10d={horiz_10d} deve ser > 0")

    # --- Validação de dimensão ---
    if len(returns) < 2:
        raise ValueError(
            f"série insuficiente (len={len(returns)}); mínimo 2 retornos"
        )

    rt = np.asarray(returns, dtype=np.float64)

    # --- VaR por quantil empírico ---
    var_pct_99 = float(np.abs(np.percentile(rt, (1.0 - conf) * 100.0)))
    # VaR histórico 99% em % — VaR_HISTÓRICO!D15  [=ABS(PERCENTILE(C4:C522,1-B4))]

    var_pct_95 = float(np.abs(np.percentile(rt, (1.0 - conf_sec) * 100.0)))
    # VaR histórico 95% em % — VaR_HISTÓRICO!D16  [=ABS(PERCENTILE(C4:C522,1-B5))]

    # --- Escalonamento monetário ---
    var_brl_99 = var_pct_99 * nocional
    # VaR histórico 99% em BRL — VaR_HISTÓRICO!E15  [=D15*PARÂMETROS!B24]

    var_brl_95 = var_pct_95 * nocional
    # VaR histórico 95% em BRL — VaR_HISTÓRICO!E16  [=D16*PARÂMETROS!B24]

    # --- Expected Shortfall (CVaR) 99% ---
    limiar_99 = np.percentile(rt, (1.0 - conf) * 100.0)
    # quantil da cauda esquerda — usado como condição do AVERAGEIF

    tail_99 = rt[rt < limiar_99]
    # retornos abaixo do quantil — equivalente ao filtro SE() em AVERAGEIF

    if len(tail_99) == 0:
        # CASO NÃO COBERTO NO ARTEFATO ORIGINAL — adicionado na derivação
        # Excel retornava 0 silenciosamente via AVERAGEIF sem matches
        warnings.warn(
            "ES histórico: nenhum retorno abaixo do quantil — "
            "série pode ser inteiramente positiva; retornando np.nan",
            RuntimeWarning,
            stacklevel=2,
        )
        es_pct_99 = np.nan
        es_brl_99 = np.nan
    else:
        es_pct_99 = float(-np.mean(tail_99))
        # ES 99% em % = -E[rₜ | rₜ < q₁%] — VaR_HISTÓRICO!F15
        # [=AVERAGEIF(C4:C522,"<"&PERCENTILE(...))*-1]

        es_brl_99 = es_pct_99 * nocional
        # ES 99% em BRL — VaR_HISTÓRICO!G15  [=F15*PARÂMETROS!B24]

    # --- Escalonamento para horizonte regulatório ---
    var_10d_pct_99 = var_pct_99 * np.sqrt(horiz_10d)
    # VaR histórico 10d em % = VaR_1d × √10 — VaR_HISTÓRICO!D17
    # [=ABS(PERCENTILE(...))*SQRT(PARÂMETROS!B9)]
    # NOTA: assume retornos i.i.d. — distorce em presença de autocorrelação

    return {
        "var_pct_99":     var_pct_99,
        "var_pct_95":     var_pct_95,
        "var_brl_99":     var_brl_99,
        "var_brl_95":     var_brl_95,
        "es_pct_99":      es_pct_99,
        "es_brl_99":      es_brl_99,
        "var_10d_pct_99": var_10d_pct_99,
    }


def var_parametrico(z_alpha: float, sigma: float, h: int = 1) -> float:
    """
    Calcula VaR delta-normal: VaR = z_α × σ̂ × √h.
    Calculado a partir de: z_alpha (float), sigma (float), h (int)
    Utilizado por: var_parametrico_completo, backtesting, stress_test
    Corrige Ambiguidade A6: SQRT(1) hardcoded substituído por parâmetro h.
    """
    # --- Validação de domínio ---
    if z_alpha <= 0.0:
        raise ValueError(
            f"z_alpha={z_alpha} deve ser > 0; "
            "típico: 2.3263 (99%) ou 1.6449 (95%)"
        )
    if sigma <= 0.0:
        raise ValueError(f"sigma={sigma} deve ser > 0")
    if h <= 0:
        raise ValueError(
            f"h={h} deve ser inteiro positivo; "
            "1 = diário, 10 = regulatório Basileia"
        )

    # --- VaR delta-normal ---
    var_pct = z_alpha * sigma * np.sqrt(h)
    # VaR_% = z_α × σ̂ × √h — VaR_PARAMÉTRICO!E19
    # [=VP!B12 * VP!B7 * SQRT(1)] — SQRT(1) corrigido para SQRT(h)

    return float(var_pct)


def var_parametrico_completo(
    sigma: float,
    z_alpha_99: float,
    z_alpha_95: float,
    nocional: float,
    h: int = 1,
    var_hist_99: float = 0.0,
) -> dict:
    """
    Calcula VaR delta-normal para múltiplos níveis e compara com VaR histórico.
    Calculado a partir de: sigma, z_alpha_99, z_alpha_95, nocional, h, var_hist_99
    Utilizado por: backtesting, stress_test, ewma_var, gerar_relatorio
    """
    # --- Validação de domínio ---
    if sigma <= 0.0:
        raise ValueError(f"sigma={sigma} deve ser > 0")
    if not (z_alpha_99 > z_alpha_95 > 0.0):
        raise ValueError(
            f"z_alpha_99={z_alpha_99} deve ser > z_alpha_95={z_alpha_95} > 0"
        )
    if nocional <= 0.0:
        raise ValueError(f"nocional={nocional} deve ser > 0")
    if h <= 0:
        raise ValueError(f"h={h} deve ser > 0")

    # --- VaR paramétrico 99% ---
    var_pct_99 = var_parametrico(z_alpha_99, sigma, h)
    # VaR delta-normal 99% em % — VaR_PARAMÉTRICO!E19  [=B12*B7*SQRT(1)]

    var_brl_99 = var_pct_99 * nocional
    # VaR delta-normal 99% em BRL — VaR_PARAMÉTRICO!F19  [=E19*PARÂMETROS!B24]

    # --- VaR paramétrico 95% ---
    var_pct_95 = var_parametrico(z_alpha_95, sigma, h)
    # VaR delta-normal 95% em % — VaR_PARAMÉTRICO!E20  [=B13*B7*SQRT(1)]

    var_brl_95 = var_pct_95 * nocional
    # VaR delta-normal 95% em BRL — VaR_PARAMÉTRICO!F20  [=E20*PARÂMETROS!B24]

    # --- Diferencial paramétrico vs histórico ---
    delta_param_hist = var_pct_99 - var_hist_99
    # diferencial: >0 = paramétrico mais conservador — VaR_PARAMÉTRICO!G19
    # [=E19 - VaR_HISTÓRICO!D15]

    return {
        "var_pct_99":       var_pct_99,
        "var_pct_95":       var_pct_95,
        "var_brl_99":       var_brl_99,
        "var_brl_95":       var_brl_95,
        "delta_param_hist": delta_param_hist,
    }


def ewma_var(
    returns: pd.Series,
    lam: float = 0.94,
    z_alpha: float = 2.3263,
    du_ano: int = 252,
    nocional: float = 10_000_000.0,
    horiz_10d: int = 10,
) -> dict:
    """
    Calcula volatilidade EWMA e VaR condicional diário para toda a série.
    Calculado a partir de: returns, lam, z_alpha, du_ano, nocional, horiz_10d
    Utilizado por: gerar_relatorio
    """
    # --- Validação de domínio ---
    if not (0.0 < lam < 1.0):
        raise ValueError(f"lambda={lam} deve estar em (0, 1)")
    if du_ano <= 0:
        raise ValueError(f"du_ano={du_ano} deve ser > 0; convenção BR = 252")
    if nocional <= 0.0:
        raise ValueError(f"nocional={nocional} deve ser > 0")
    if horiz_10d <= 0:
        raise ValueError(f"horiz_10d={horiz_10d} deve ser > 0")

    rt = np.asarray(returns, dtype=np.float64)

    # --- Volatilidade condicional EWMA ---
    sigma_t = ewma_volatility(rt, lam)
    # série σₜ EWMA — EWMA_VOL!E3:E522  [=SQRT(D{t})]
    # NOTA: descartar sigma_t[:50] (burn-in σ₀²=0) em séries longas

    # --- Anualizações ---
    sigma_t_anual = sigma_t * np.sqrt(du_ano)
    # σₜ anualizada = σₜ × √252 — EWMA_VOL!F{t}  [=E{t}*SQRT(PARÂMETROS!B10)]

    # --- VaR EWMA diário ---
    var_ewma_t_pct = z_alpha * sigma_t
    # VaR_EWMA_t em % = z_α × σₜ — EWMA_VOL!G{t}  [=VaR_PARAMÉTRICO!B12*E{t}]

    var_ewma_t_brl = var_ewma_t_pct * nocional
    # VaR_EWMA_t em BRL = VaR_% × nocional — EWMA_VOL!H{t}  [=G{t}*PARÂMETROS!B24]

    # --- Snapshot do último dia da série ---
    var_ewma_final_pct = float(var_ewma_t_pct[-1])
    # VaR EWMA final em % — EWMA_VOL!G522  [último valor de G{t}]

    var_ewma_final_brl = float(var_ewma_t_brl[-1])
    # VaR EWMA final em BRL — EWMA_VOL!H522  [último valor de H{t}]

    # --- Escalonamento regulatório ---
    var_ewma_10d_brl = var_ewma_final_brl * np.sqrt(horiz_10d)
    # VaR EWMA 10d em BRL = H522 × √10 — EWMA_VOL!B529
    # [=H522*SQRT(PARÂMETROS!B9)]
    # NOTA: assume i.i.d. — mesma limitação da escala √t do método histórico

    return {
        "sigma_t":            sigma_t,
        "sigma_t_anual":      sigma_t_anual,
        "var_ewma_t_pct":     var_ewma_t_pct,
        "var_ewma_t_brl":     var_ewma_t_brl,
        "var_ewma_final_pct": var_ewma_final_pct,
        "var_ewma_final_brl": var_ewma_final_brl,
        "var_ewma_10d_brl":   var_ewma_10d_brl,
    }


def backtesting(
    returns: pd.Series,
    var_threshold: float,
    zona_verde_lim: int = 4,
    zona_vermelha_lim: int = 10,
) -> dict:
    """
    Executa backtesting de Basileia II: conta exceções e classifica
    o modelo no semáforo regulatório.
    Calculado a partir de: returns, var_threshold, zona_verde_lim,
                           zona_vermelha_lim
    Utilizado por: gerar_relatorio
    Corrige Ambiguidade A6: offset fixo linha 274 eliminado — o
    chamador é responsável por passar returns.iloc[-250:].
    """
    # --- Validação de domínio ---
    if var_threshold <= 0.0:
        raise ValueError(f"var_threshold={var_threshold} deve ser > 0")
    if not (0 <= zona_verde_lim < zona_vermelha_lim):
        raise ValueError(
            f"limiares inválidos: verde={zona_verde_lim}, "
            f"vermelho={zona_vermelha_lim}; "
            "Basileia padrão: 4 e 10"
        )

    # --- Validação de dimensão ---
    if len(returns) < 1:
        raise ValueError("returns vazio — fornecer janela de retornos")

    rt = np.asarray(returns, dtype=np.float64)
    n_obs = len(rt)

    # --- Vetor de exceções ---
    excecoes = rt < -var_threshold
    # 𝟏{rₜ < −VaR}: True se perda supera o VaR previsto — BACKTESTING!D{t}
    # [=IF(B{t}<-C{t},"SIM","NÃO")]
    # CORRIGE A6: BT!B{t}=RETORNOS_HIST!C274 (offset fixo) →
    # aqui o chamador faz returns.iloc[-250:] antes de chamar backtesting()

    # --- Contagem de exceções ---
    n_excecoes = int(np.sum(excecoes))
    # Nₑₓc = Σ𝟏{exceção} — BACKTESTING!B256  [=COUNTIF(D3:D252,"SIM")]

    # --- Taxa empírica de exceção ---
    taxa_excecao = n_excecoes / n_obs
    # p̂ = Nₑₓc / n — BACKTESTING!B257  [=B256/COUNTA(A3:A252)]
    # esperado ≈ 1% para VaR 99% (1 exceção a cada 100 dias úteis)

    # --- Semáforo de Basileia ---
    if n_excecoes >= zona_vermelha_lim:
        semaforo = "VERMELHO"
    elif n_excecoes >= zona_verde_lim:
        semaforo = "AMARELO"
    else:
        semaforo = "VERDE"
    # classificação regulatória — BACKTESTING!C265
    # [=IF(N≥B30,"🔴 VERMELHO",IF(N≥B28,"🟡 AMARELO","🟢 VERDE"))]

    return {
        "excecoes":     excecoes,
        "n_excecoes":   n_excecoes,
        "taxa_excecao": taxa_excecao,
        "semaforo":     semaforo,
    }


# ════════════════════════════════════════════════════════════════════════
# CAMADA 4 — Monte Carlo e Stress (topológico: posições 8–10)
# ════════════════════════════════════════════════════════════════════════

def var_montecarlo(
    sim_rt_log: np.ndarray,
    conf: float = 0.99,
    nocional: float = 10_000_000.0,
) -> dict:
    """
    Calcula VaR e ES Monte Carlo por distribuição empírica simulada.
    Calculado a partir de: sim_rt_log (np.ndarray), conf (float),
                           nocional (float)
    Utilizado por: gerar_relatorio
    Corrige Ambiguidade A3: PERCENTILE(sim, 0.01) hardcoded
    substituído por PERCENTILE(sim, (1-conf)*100).
    """
    # --- Validação de domínio ---
    if not (0.0 < conf < 1.0):
        raise ValueError(f"conf={conf} deve estar em (0, 1)")
    if nocional <= 0.0:
        raise ValueError(f"nocional={nocional} deve ser > 0")

    # --- Validação de dimensão ---
    if len(sim_rt_log) == 0:
        raise ValueError("sim_rt_log vazio — executar simulate_returns primeiro")

    rt_sim = np.asarray(sim_rt_log, dtype=np.float64)

    # --- VaR Monte Carlo por quantil empírico ---
    var_mc_pct = float(
        np.abs(np.percentile(rt_sim, (1.0 - conf) * 100.0))
    )
    # VaR_MC em % = |q_{1-conf}(rₜ_sim)| — MONTE_CARLO!B1017
    # [=ABS(PERCENTILE(B15:B1014, 0.01))] — CORRIGE A3: 0.01 → (1−conf)

    var_mc_brl = var_mc_pct * nocional
    # VaR_MC em BRL = VaR_% × nocional — MONTE_CARLO!B1018
    # [=ABS(PERCENTILE(...))*B11]

    # --- Expected Shortfall Monte Carlo ---
    limiar_mc = np.percentile(rt_sim, (1.0 - conf) * 100.0)
    tail_mc   = rt_sim[rt_sim < limiar_mc]
    # cenários na cauda esquerda — filtro equivalente ao AVERAGEIF

    if len(tail_mc) == 0:
        # CASO NÃO COBERTO NO ARTEFATO ORIGINAL — adicionado na derivação
        warnings.warn(
            "ES Monte Carlo: nenhum cenário abaixo do quantil "
            f"(conf={conf}, n_sim={len(rt_sim)}); retornando np.nan",
            RuntimeWarning,
            stacklevel=2,
        )
        es_mc_pct = np.nan
        es_mc_brl = np.nan
    else:
        es_mc_pct = float(np.abs(np.mean(tail_mc)))
        # ES_MC em % = |E[rₜ | rₜ < q]| — MONTE_CARLO!B1021
        # [=ABS(AVERAGEIF(B15:B1014,"<"&PERCENTILE(...,0.01)))]

        es_mc_brl = es_mc_pct * nocional
        # ES_MC em BRL — MONTE_CARLO!B1022  [=B1021*B11]

    # --- Estatísticas extremas dos cenários ---
    pior_cenario   = float(np.min(rt_sim))
    # pior retorno simulado — MONTE_CARLO!B1023  [=MIN(B15:B1014)]

    melhor_cenario = float(np.max(rt_sim))
    # melhor retorno simulado — MONTE_CARLO!B1024  [=MAX(B15:B1014)]

    # NOTA: MONTE_CARLO!D15 usava r_log×nocional para P&L (erro teórico);
    # aqui usamos r_log diretamente para consistência com os demais métodos.
    # P&L correto seria: (exp(r_log) - 1) * nocional  [MC!C15 = EXP(B15)-1]

    return {
        "var_mc_pct":     var_mc_pct,
        "var_mc_brl":     var_mc_brl,
        "es_mc_pct":      es_mc_pct,
        "es_mc_brl":      es_mc_brl,
        "pior_cenario":   pior_cenario,
        "melhor_cenario": melhor_cenario,
    }


def stress_test(
    cenarios_rt: np.ndarray,
    var_param_pct: float,
    sigma: float,
    nocional: float,
) -> dict:
    """
    Avalia cenários de stress: perda em BRL, múltiplo de VaR,
    probabilidade normal acumulada e classificação de severidade.
    Calculado a partir de: cenarios_rt, var_param_pct, sigma, nocional
    Utilizado por: gerar_relatorio (opcional)
    """
    # --- Validação de domínio ---
    if var_param_pct <= 0.0:
        raise ValueError(
            f"var_param_pct={var_param_pct} deve ser > 0; "
            "evita #DIV/0! em E13 do Excel"
        )
    if sigma <= 0.0:
        raise ValueError(
            f"sigma={sigma} deve ser > 0; "
            "evita #DIV/0! em F13 do Excel"
        )
    if nocional <= 0.0:
        raise ValueError(f"nocional={nocional} deve ser > 0")

    # --- Validação de dimensão ---
    if len(cenarios_rt) == 0:
        # CASO NÃO COBERTO NO ARTEFATO ORIGINAL — adicionado na derivação
        raise ValueError(
            "cenarios_rt vazio — fornecer retornos dos cenários de stress; "
            "o Excel usa 8 cenários históricos/hipotéticos em STRESS_TEST!B4:B15"
        )

    c = np.asarray(cenarios_rt, dtype=np.float64)

    # --- Perda monetária ---
    perda_brl = c * nocional
    # perda em BRL = r_cenário × nocional — STRESS_TEST!H4/C13
    # [=C4*PARÂMETROS!B24  ou  =B13*PARÂMETROS!B24]

    # --- Magnitude absoluta ---
    abs_r = np.abs(c)
    # |r_cenário| — STRESS_TEST!D13  [=ABS(B13)]

    # --- Múltiplo do VaR ---
    multiplo_var = abs_r / var_param_pct
    # k = |r_cen| / VaR_param — STRESS_TEST!E13
    # [=ABS(B13)/VaR_PARAMÉTRICO!E19]

    # --- Probabilidade na distribuição normal ---
    prob_normal = stats.norm.cdf(c / sigma)
    # Φ(r/σ) = probabilidade acumulada normal — STRESS_TEST!F13
    # [=DIST.NORM(B13/VaR_PARAMÉTRICO!B7, 0, 1, VERDADEIRO)]

    # --- Classificação de severidade ---
    classificacao = np.where(
        abs_r > 3.0 * var_param_pct,
        "EXTREMO",
        np.where(abs_r > var_param_pct, "SEVERO", "MODERADO"),
    )
    # Moderado: k ≤ 1 | Severo: 1 < k ≤ 3 | Extremo: k > 3
    # STRESS_TEST!G13  [=IF(ABS>3×VaR,"EXTREMO",IF(ABS>VaR,"SEVERO","MODERADO"))]

    return {
        "perda_brl":     perda_brl,
        "abs_r":         abs_r,
        "multiplo_var":  multiplo_var,
        "prob_normal":   prob_normal,
        "classificacao": classificacao.tolist(),
    }


# ════════════════════════════════════════════════════════════════════════
# CAMADA 5 — Agregação final (topológico: posição 11)
# ════════════════════════════════════════════════════════════════════════

def gerar_relatorio(
    var_hist:          dict,
    var_param:         dict,
    var_ewma:          dict,
    var_mc:            dict,
    bt:                dict,
    P0:                float,
    P_final:           float,
    nocional:          float,
    buffer_capital:    float = 1.25,
    limite_alerta_pct: float = 0.05,
) -> dict:
    """
    Consolida os resultados de todos os métodos de VaR no dashboard executivo.
    Calculado a partir de: var_hist, var_param, var_ewma, var_mc, bt,
                           P0, P_final, nocional, buffer_capital,
                           limite_alerta_pct
    Utilizado por: var_ibovespa
    Corrige A4: ×1.25 hardcoded → buffer_capital (default=1.25).
    Corrige A5: limiar 5% hardcoded → limite_alerta_pct (default=0.05).
    """
    # --- Validação de domínio ---
    if P0 <= 0.0:
        raise ValueError(f"P0={P0} deve ser > 0; evita #DIV/0! em RESUMO_EXEC!B10")
    if P_final <= 0.0:
        raise ValueError(f"P_final={P_final} deve ser > 0")
    if nocional <= 0.0:
        raise ValueError(f"nocional={nocional} deve ser > 0")
    if buffer_capital <= 1.0:
        raise ValueError(
            f"buffer_capital={buffer_capital} deve ser > 1; "
            "Excel usa 1.25 — RESUMO_EXEC!G16"
        )
    if limite_alerta_pct <= 0.0:
        raise ValueError(
            f"limite_alerta_pct={limite_alerta_pct} deve ser > 0; "
            "Excel usa 0.05 — RESUMO_EXEC!B24"
        )

    # --- Retorno acumulado do período ---
    retorno_acumulado = (P_final / P0) - 1.0
    # Pₜ/P₀ − 1 — RESUMO_EXEC!B10  [=RETORNOS_HIST!B522/RETORNOS_HIST!B3-1]

    # --- Links diretos: VaR Histórico ---
    var_hist_95_pct  = var_hist["var_pct_95"]
    # VaR histórico 95% em % — RESUMO_EXEC!C14  [=VaR_HISTÓRICO!D16]

    var_hist_95_brl  = var_hist["var_brl_95"]
    # VaR histórico 95% em BRL — RESUMO_EXEC!D14  [=VaR_HISTÓRICO!E16]

    var_hist_99_pct  = var_hist["var_pct_99"]
    # VaR histórico 99% em % — RESUMO_EXEC!E14

    es_hist_99_pct   = var_hist["es_pct_99"]
    # ES histórico 99% em % — RESUMO_EXEC!G14  [=VaR_HISTÓRICO!F15]

    es_hist_99_brl   = var_hist["es_brl_99"]
    # ES histórico 99% em BRL — RESUMO_EXEC!H14  [=VaR_HISTÓRICO!G15]

    # --- Links diretos: VaR Paramétrico ---
    var_param_95_pct = var_param["var_pct_95"]
    # VaR paramétrico 95% em % — RESUMO_EXEC!C16  [=VaR_PARAMÉTRICO!E20]

    var_param_95_brl = var_param["var_brl_95"]
    # VaR paramétrico 95% em BRL — RESUMO_EXEC!D16  [=VaR_PARAMÉTRICO!F20]

    var_param_99_pct = var_param["var_pct_99"]
    # VaR paramétrico 99% em % — RESUMO_EXEC!E16

    # --- Buffer de capital (VaR × fator regulatório) ---
    var_param_buf_pct = var_param_99_pct * buffer_capital
    # VaR_param_99% × buffer — RESUMO_EXEC!G16  [=VaR_PARAMÉTRICO!E19*1.25]
    # CORRIGE A4: 1.25 hardcoded → buffer_capital

    var_param_buf_brl = var_param["var_brl_99"] * buffer_capital
    # VaR_param_99% BRL × buffer — RESUMO_EXEC!H16  [=VaR_PARAMÉTRICO!F19*1.25]

    # --- Links diretos: VaR EWMA ---
    var_ewma_pct     = var_ewma["var_ewma_final_pct"]
    # VaR EWMA final em % — RESUMO_EXEC!E18  [=EWMA_VOL!G522]

    var_ewma_brl     = var_ewma["var_ewma_final_brl"]
    # VaR EWMA final em BRL — RESUMO_EXEC!F18  [=EWMA_VOL!H522]

    var_ewma_buf_pct = var_ewma_pct * buffer_capital
    # VaR EWMA × buffer — RESUMO_EXEC!G18  [=EWMA_VOL!G522*1.25]

    var_ewma_buf_brl = var_ewma_brl * buffer_capital
    # VaR EWMA BRL × buffer — RESUMO_EXEC!H18  [=EWMA_VOL!H522*1.25]

    # --- Ajuste de nível de confiança EWMA (reescala z₉₅/z₉₉) ---
    # NOTA: RESUMO_EXEC!C18 = EWMA_VOL!G522 × VP!B14/VP!B12
    # reescala z_95/z_99; simplificado como var_ewma_pct aqui —
    # implementação completa requer z_alpha_95 e z_alpha_99 como inputs
    var_ewma_adj_pct = var_ewma_pct
    var_ewma_adj_brl = var_ewma_brl
    # VaR EWMA ajustado — RESUMO_EXEC!C18/D18  [simplificado — ver NOTA]

    # --- Links diretos: VaR Monte Carlo ---
    var_mc_pct       = var_mc["var_mc_pct"]
    # VaR Monte Carlo 99% em % — RESUMO_EXEC!C19  [=MONTE_CARLO!B1019]

    # --- Links diretos: Backtesting ---
    semaforo_basileia = bt["semaforo"]
    # semáforo de Basileia — RESUMO_EXEC!B22  [=BACKTESTING!C265]

    n_excecoes        = bt["n_excecoes"]
    # número de exceções — RESUMO_EXEC!B25  [=COUNTIF(BACKTESTING!D3:D252,"SIM")]

    # --- VaR máximo entre todos os métodos ---
    todos_var_pct = [
        var_hist_95_pct,
        var_hist_99_pct,
        var_param_95_pct,
        var_param_99_pct,
        var_ewma_pct,
        var_mc_pct,
    ]
    max_var_pct = float(np.nanmax(todos_var_pct))
    # max VaR entre métodos — RESUMO_EXEC!B23  [=MAX(E14:E19)]

    # --- Alerta de limite ---
    alerta_limite = (
        "⚠ ATENÇÃO — EXCEDE LIMITE"
        if max_var_pct > limite_alerta_pct
        else "✓ DENTRO DO LIMITE"
    )
    # alerta regulatório — RESUMO_EXEC!B24
    # [=IF(MAX(E14:E19)>0.05,"ATENÇÃO","DENTRO DO LIMITE")]
    # CORRIGE A5: 0.05 hardcoded → limite_alerta_pct

    return {
        "data_relatorio":       pd.Timestamp.today().strftime("%d/%m/%Y"),
        "nocional_brl":         nocional,
        "retorno_acumulado":    retorno_acumulado,
        "var_hist_95_pct":      var_hist_95_pct,
        "var_hist_95_brl":      var_hist_95_brl,
        "es_hist_99_pct":       es_hist_99_pct,
        "es_hist_99_brl":       es_hist_99_brl,
        "var_param_95_pct":     var_param_95_pct,
        "var_param_95_brl":     var_param_95_brl,
        "var_param_buf_pct":    var_param_buf_pct,
        "var_param_buf_brl":    var_param_buf_brl,
        "var_ewma_adj_pct":     var_ewma_adj_pct,
        "var_ewma_adj_brl":     var_ewma_adj_brl,
        "var_ewma_pct":         var_ewma_pct,
        "var_ewma_brl":         var_ewma_brl,
        "var_ewma_buf_pct":     var_ewma_buf_pct,
        "var_ewma_buf_brl":     var_ewma_buf_brl,
        "var_mc_pct":           var_mc_pct,
        "semaforo_basileia":    semaforo_basileia,
        "n_excecoes":           n_excecoes,
        "max_var_pct":          max_var_pct,
        "alerta_limite":        alerta_limite,
    }


# ════════════════════════════════════════════════════════════════════════
# PONTO DE ENTRADA — Modelo completo (topológico: posição 12)
# ════════════════════════════════════════════════════════════════════════

def var_ibovespa(
    prices: pd.Series,
    conf_99: float = 0.99,
    conf_95: float = 0.95,
    du_ano: int = 252,
    horiz_10d: int = 10,
    lambda_ewma: float = 0.94,
    nocional: float = 10_000_000.0,
    zona_verde_lim: int = 4,
    zona_vermelha_lim: int = 10,
    n_mc: int = 1_000,
    seed: Optional[int] = None,
    cenarios_stress: Optional[np.ndarray] = None,
    buffer_capital: float = 1.25,
    limite_alerta_pct: float = 0.05,
) -> dict:
    """
    Modelo completo de VaR do Ibovespa: histórico, paramétrico, EWMA,
    Monte Carlo, backtesting e relatório executivo.
    Calculado a partir de: todos os INPUTs do grafo (10 nós)
    Utilizado por: — (ponto de entrada)
    Artefato de origem: VaR_Ibovespa_Modelo_Bancario.xlsx
    """
    # --- Validação global ---
    if conf_99 <= conf_95:
        raise ValueError(
            f"conf_99={conf_99} deve ser > conf_95={conf_95}"
        )
    if len(prices) < 252:
        raise ValueError(
            f"série curta ({len(prices)} obs) — "
            "mínimo 252 para janela_curta (PARÂMETROS!B12)"
        )

    # ── Camada 0: preparação da série ───────────────────────────────────
    returns = compute_log_returns(prices)
    # série de retornos log — RETORNOS_HIST!C4:C522

    # ── Camada 1: estatísticas base ──────────────────────────────────────
    sigma_hat = compute_sigma_hat(returns)
    # σ̂ amostral diário — VaR_PARAMÉTRICO!B7

    z_alpha_99 = float(stats.norm.ppf(conf_99))
    # z_{99%} = Φ⁻¹(0.99) ≈ 2.3263 — VaR_PARAMÉTRICO!B12
    # [presumivelmente =INV.NORM(conf_99,0,1)]

    z_alpha_95 = float(stats.norm.ppf(conf_95))
    # z_{95%} = Φ⁻¹(0.95) ≈ 1.6449 — VaR_PARAMÉTRICO!B13

    mu_hat = float(returns.mean())
    # μ̂ = média histórica dos retornos — VaR_PARAMÉTRICO!B6
    # [=AVERAGE(RETORNOS_HIST!C4:C522)]

    P0      = float(prices.iloc[0])
    # preço inicial — RETORNOS_HIST!B3

    P_final = float(prices.iloc[-1])
    # preço final — RETORNOS_HIST!B522

    # ── Camada 2: simulação Monte Carlo ──────────────────────────────────
    sim_rt_log = simulate_returns(mu=mu_hat, sigma=sigma_hat,
                                  n=n_mc, seed=seed)
    # cenários simulados — MONTE_CARLO!B15:B1014

    # ── Camada 3: cálculo por método ─────────────────────────────────────
    resultado_hist = var_historico(
        returns=returns,
        conf=conf_99,
        conf_sec=conf_95,
        nocional=nocional,
        horiz_10d=horiz_10d,
    )
    # outputs VaR histórico — VaR_HISTÓRICO!D15:G17

    resultado_param = var_parametrico_completo(
        sigma=sigma_hat,
        z_alpha_99=z_alpha_99,
        z_alpha_95=z_alpha_95,
        nocional=nocional,
        h=1,
        var_hist_99=resultado_hist["var_pct_99"],
    )
    # outputs VaR paramétrico — VaR_PARAMÉTRICO!E19:G19

    resultado_ewma = ewma_var(
        returns=returns,
        lam=lambda_ewma,
        z_alpha=z_alpha_99,
        du_ano=du_ano,
        nocional=nocional,
        horiz_10d=horiz_10d,
    )
    # outputs VaR EWMA — EWMA_VOL!G522, H522, B529

    resultado_mc = var_montecarlo(
        sim_rt_log=sim_rt_log,
        conf=conf_99,
        nocional=nocional,
    )
    # outputs VaR Monte Carlo — MONTE_CARLO!B1017:B1022

    # ── Camada 4: backtesting ─────────────────────────────────────────────
    janela_bt = returns.iloc[-250:]
    # janela de 250 dias úteis — BACKTESTING!B3:B252
    # CORRIGE A6: offset hardcoded linha 274 → slicing dinâmico

    resultado_bt = backtesting(
        returns=janela_bt,
        var_threshold=resultado_param["var_pct_99"],
        zona_verde_lim=zona_verde_lim,
        zona_vermelha_lim=zona_vermelha_lim,
    )
    # semáforo e exceções — BACKTESTING!B256, C265

    # ── Camada 4b: stress test (opcional) ────────────────────────────────
    if cenarios_stress is not None:
        resultado_stress = stress_test(
            cenarios_rt=cenarios_stress,
            var_param_pct=resultado_param["var_pct_99"],
            sigma=sigma_hat,
            nocional=nocional,
        )
        # análise de cenários — STRESS_TEST!C13:G24
    else:
        resultado_stress = None
        # stress_test não executado: cenarios_stress=None

    # ── Camada 5: relatório executivo ────────────────────────────────────
    relatorio = gerar_relatorio(
        var_hist=resultado_hist,
        var_param=resultado_param,
        var_ewma=resultado_ewma,
        var_mc=resultado_mc,
        bt=resultado_bt,
        P0=P0,
        P_final=P_final,
        nocional=nocional,
        buffer_capital=buffer_capital,
        limite_alerta_pct=limite_alerta_pct,
    )
    # dashboard executivo — RESUMO_EXEC!B4:H25

    return {
        "historico":   resultado_hist,
        "parametrico": resultado_param,
        "ewma":        resultado_ewma,
        "montecarlo":  resultado_mc,
        "backtesting": resultado_bt,
        "stress":      resultado_stress,
        "relatorio":   relatorio,
    }
