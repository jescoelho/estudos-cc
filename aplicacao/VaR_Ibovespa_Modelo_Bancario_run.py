# -*- coding: utf-8 -*-
"""
VaR_Ibovespa_Modelo_Bancario_run.py
Script executável standalone — carrega dados da planilha e executa o modelo.

Uso:
    python VaR_Ibovespa_Modelo_Bancario_run.py

Dependências:
    VaR_Ibovespa_Modelo_Bancario.py (mesmo diretório)
    openpyxl, pandas, numpy, scipy
"""
import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

import os
import numpy as np
import pandas as pd

from VaR_Ibovespa_Modelo_Bancario import (
    ModelConfig,
    var_ibovespa_modelo_bancario,
)

# ---------------------------------------------------------------------------
# CONFIGURAÇÃO — ajuste aqui sem tocar no modelo
# ---------------------------------------------------------------------------

_DIR         = os.path.dirname(os.path.abspath(__file__))
ARQUIVO_XLSX = os.path.join(_DIR, "VaR_Ibovespa_Modelo_Bancario.xlsx")

# Parâmetros do modelo (espelham PARÂMETROS!B4:B30)
CONF_99        = 0.99
CONF_95        = 0.95
HORIZ_10D      = 10
DU_ANO         = 252
LAMBDA_EWMA    = 0.94
NOCIONAL       = 10_000_000.0
N_BACKTESTING  = 250
ZONA_VERDE     = 4
ZONA_VERMELHA  = 10

# Monte Carlo — aba original contém VALORES FIXOS (sem fórmula de geração)
# Reproduzido aqui com seed para garantir reprodutibilidade.
# MC original usa valores fixos — gerado aqui com seed para reprodutibilidade
N_MC  = 1_000
SEED  = 42

# ---------------------------------------------------------------------------
# 1. CARREGAR PREÇOS (RETORNOS_HIST!A:B)
# ---------------------------------------------------------------------------

df = pd.read_excel(
    ARQUIVO_XLSX,
    sheet_name="RETORNOS_HIST",
    usecols="A:B",
    skiprows=1,       # pula linha de título da aba
    header=0,
    engine="openpyxl",
)
df.columns = ["DATA", "PRECO"]
df = df[pd.to_datetime(df["DATA"], errors="coerce").notna()].copy()
df["DATA"] = pd.to_datetime(df["DATA"])
df = df.set_index("DATA")
prices = df["PRECO"].dropna()

print(f"Preços carregados : {len(prices)} obs  "
      f"({prices.index[0].date()} → {prices.index[-1].date()})")

# ---------------------------------------------------------------------------
# 2. GERAR CENÁRIOS MONTE CARLO com numpy (seed fixo)
# ---------------------------------------------------------------------------

# mu e sigma calculados a partir dos preços carregados (replicam RETORNOS_HIST!B526:B527)
import numpy as _np_inner, math as _math
_log_ret = [_math.log(float(prices.iloc[i]) / float(prices.iloc[i-1]))
            for i in range(1, len(prices))]
_mu_seed    = float(_np_inner.mean(_log_ret))
_sigma_seed = float(_np_inner.std(_log_ret, ddof=1))

rng = np.random.default_rng(SEED)
cenarios_mc = rng.normal(_mu_seed, _sigma_seed, N_MC)

# ---------------------------------------------------------------------------
# 3. CENÁRIOS DE ESTRESSE (STRESS_TEST!B4:C9 — lidos da planilha)
# ---------------------------------------------------------------------------

cenarios_stress = pd.DataFrame([
    {"nome": "Set/2008 – Mar/2009", "retorno_shock": -0.602},
    {"nome": "Jul/2011 – Ago/2011", "retorno_shock": -0.272},
    {"nome": "Jan/2015 – Set/2015", "retorno_shock": -0.341},
    {"nome": "Fev/2020 – Mar/2020", "retorno_shock": -0.466},
    {"nome": "Jan/2023",            "retorno_shock": -0.038},
    {"nome": "Out/2022",            "retorno_shock": -0.052},
])

# ---------------------------------------------------------------------------
# 4. CONFIGURAÇÃO E EXECUÇÃO DO MODELO
# ---------------------------------------------------------------------------

cfg = ModelConfig(
    conf_99       = CONF_99,
    conf_95       = CONF_95,
    horiz_10d     = HORIZ_10D,
    du_ano        = DU_ANO,
    lambda_ewma   = LAMBDA_EWMA,
    nocional      = NOCIONAL,
    n_backtesting = N_BACKTESTING,
    zona_verde    = ZONA_VERDE,
    zona_vermelha = ZONA_VERMELHA,
)

resultado = var_ibovespa_modelo_bancario(prices, cenarios_mc, cenarios_stress, cfg)

# ---------------------------------------------------------------------------
# 5. PAINEL DE RESULTADOS
# ---------------------------------------------------------------------------

h   = resultado["var_historico"]
p   = resultado["var_parametrico"]
e   = resultado["ewma"]
mc  = resultado["monte_carlo"]
bt  = resultado["backtesting"]
st  = resultado["stress_test"]
res = resultado["resumo_executivo"]
est = resultado["estatisticas"]

L  = "=" * 62
L2 = "-" * 62

print(f"\n{L}")
print(f"  PAINEL EXECUTIVO — VaR IBOVESPA MODELO BANCÁRIO")
print(f"{L}")
print(f"  Nocional          : R$ {NOCIONAL:>15,.2f}")
print(f"  Observações       : {est['n']} retornos log")
print(f"  Sigma diária      : {est['sigma_diaria']*100:.4f}%")
print(f"  Sigma anual       : {est['sigma_anual']*100:.2f}%")

print(f"\n  VaR 1d / 99% por metodologia")
print(f"  {L2}")
print(f"  {'Metodologia':<22} {'(%)'  :>10}   {'(R$)':>16}")
print(f"  {L2}")
print(f"  {'Histórico':<22} {h['var_99_1d_pct']*100:>9.4f}%   R$ {h['var_99_1d_brl']:>13,.2f}")
print(f"  {'Paramétrico':<22} {p['var_99_1d_pct']*100:>9.4f}%   R$ {p['var_99_1d_brl']:>13,.2f}")
print(f"  {'EWMA (λ={:.2f})':<22} {e['var_atual']*100:>9.4f}%   R$ {e['var_brl_atual']:>13,.2f}".format(LAMBDA_EWMA))
print(f"  {'Monte Carlo 99%':<22} {mc['var_99_pct']*100:>9.4f}%   R$ {mc['var_99_brl']:>13,.2f}")
print(f"  {L2}")
print(f"  {'Máximo':<22} {res['max_var_pct']*100:>9.4f}%   R$ {res['max_var_brl']:>13,.2f}")

print(f"\n  Expected Shortfall 99% (CVaR)")
print(f"  {L2}")
print(f"  {'ES Histórico':<22} {h['es_99_1d']*100:>9.4f}%   R$ {h['es_99_1d']*NOCIONAL:>13,.2f}")
print(f"  {'ES Monte Carlo':<22} {mc['es_99_pct']*100:>9.4f}%   R$ {mc['es_99_brl']:>13,.2f}")

print(f"\n  VaR 10d regulatório (Basileia √T)")
print(f"  {L2}")
print(f"  {'Histórico 10d':<22} {h['var_99_10d_pct']*100:>9.4f}%   R$ {h['var_99_10d_pct']*NOCIONAL:>13,.2f}")
print(f"  {'Paramétrico 10d':<22} {p['var_99_10d_pct']*100:>9.4f}%   R$ {p['var_99_10d_brl']:>13,.2f}")

print(f"\n  Backtesting — Semáforo Basileia ({N_BACKTESTING} dias úteis)")
print(f"  {L2}")
print(f"  Exceções          : {bt['n_excecoes']:>3}  ({bt['taxa_excecao']*100:.2f}%  esperado ~1%)")
print(f"  Semáforo          : {bt['semaforo']}")

print(f"\n  Testes de Estresse")
print(f"  {L2}")
print(f"  {'Cenário':<26} {'Choque':>8}  {'Perda (R$)':>16}  {'×VaR':>6}  Classificação")
for _, row in st.iterrows():
    print(
        f"  {row['nome']:<26} {row['retorno_shock']*100:>7.1f}%"
        f"  R$ {row['perda_brl']:>13,.2f}"
        f"  {row['ratio_var']:>5.1f}x"
        f"  {row['severidade']}"
    )

print(f"\n  {res['alerta_limite']}")
print(f"{L}\n")
