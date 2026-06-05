# -*- coding: utf-8 -*-
"""
run_model.py -- Execucao do modelo VaR com dados da planilha
Uso: python run_model.py
Dependencias: var_ibovespa.py na mesma pasta, openpyxl, pandas, numpy, scipy
"""
import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

import os
import pandas as pd
import numpy as np
from var_ibovespa import var_ibovespa

# == 1. CONFIGURACAO =======================================================
_DIR = os.path.dirname(os.path.abspath(__file__))
ARQUIVO_EXCEL = os.path.join(_DIR, "VaR_Ibovespa_Modelo_Bancario.xlsx")

CONF_99           = 0.99
CONF_95           = 0.95
DU_ANO            = 252
HORIZ_10D         = 10
LAMBDA_EWMA       = 0.94
NOCIONAL          = 10_000_000.0
ZONA_VERDE        = 4
ZONA_VERMELHA     = 10
N_MC              = 1_000
SEED              = 42          # None para simulacao nao deterministica
BUFFER_CAPITAL    = 1.25
LIMITE_ALERTA_PCT = 0.05

CENARIOS_STRESS = np.array([
    -0.1207,   # Crise COVID  (mar/2020)
    -0.0736,   # Brexit       (jun/2016)
    -0.0992,   # Lehman       (set/2008)
    -0.0550,   # Eleicoes BR  (out/2022)
    -0.2000,   # Hipotetico extremo
])
# CENARIOS_STRESS = None  # descomente para desativar stress test

# == 2. CARREGAR PRECOS ====================================================
df = pd.read_excel(
    ARQUIVO_EXCEL,
    sheet_name = "RETORNOS_HIST",
    usecols    = "A:B",
    skiprows   = 1,
    header     = 0,
    engine     = "openpyxl",
)
df.columns = ["DATA", "PRECO"]

# Manter apenas linhas com data valida (descarta rodape de estatisticas)
df = df[pd.to_datetime(df["DATA"], errors="coerce").notna()].copy()
df["DATA"] = pd.to_datetime(df["DATA"])
df         = df.set_index("DATA")
prices     = df["PRECO"].dropna()

print(f"Serie carregada : {len(prices)} precos")
print(f"Periodo         : {prices.index[0].date()} -> {prices.index[-1].date()}")
print(f"P0              : {prices.iloc[0]:>12,.2f} pts")
print(f"P_final         : {prices.iloc[-1]:>12,.2f} pts")

# == 3. EXECUTAR MODELO ====================================================
resultado = var_ibovespa(
    prices,
    conf_99           = CONF_99,
    conf_95           = CONF_95,
    du_ano            = DU_ANO,
    horiz_10d         = HORIZ_10D,
    lambda_ewma       = LAMBDA_EWMA,
    nocional          = NOCIONAL,
    zona_verde_lim    = ZONA_VERDE,
    zona_vermelha_lim = ZONA_VERMELHA,
    n_mc              = N_MC,
    seed              = SEED,
    cenarios_stress   = CENARIOS_STRESS,
    buffer_capital    = BUFFER_CAPITAL,
    limite_alerta_pct = LIMITE_ALERTA_PCT,
)

# == 4. EXIBIR RESULTADOS ==================================================
rel = resultado["relatorio"]
h   = resultado["historico"]
p   = resultado["parametrico"]
e   = resultado["ewma"]
mc  = resultado["montecarlo"]
bt  = resultado["backtesting"]
st  = resultado["stress"]

L  = "=" * 60
L2 = "-" * 60

print(f"\n{L}")
print(f"  PAINEL EXECUTIVO -- {rel['data_relatorio']}")
print(f"{L}")
print(f"  Nocional          : R$ {rel['nocional_brl']:>15,.2f}")
print(f"  Retorno acumulado : {rel['retorno_acumulado']*100:>+8.2f}%")

print(f"\n  VaR 1d / 99% por metodo")
print(f"  {L2}")
print(f"  {'Metodo':<18} {'%':>10}   {'BRL':>16}")
print(f"  {L2}")
print(f"  {'Historico':<18} {h['var_pct_99']*100:>9.4f}%   R$ {h['var_brl_99']:>13,.2f}")
print(f"  {'Parametrico':<18} {p['var_pct_99']*100:>9.4f}%   R$ {p['var_brl_99']:>13,.2f}")
print(f"  {'EWMA (lam={:.2f})':<18} {e['var_ewma_final_pct']*100:>9.4f}%   R$ {e['var_ewma_final_brl']:>13,.2f}".format(LAMBDA_EWMA))
print(f"  {'Monte Carlo':<18} {mc['var_mc_pct']*100:>9.4f}%   R$ {mc['var_mc_brl']:>13,.2f}")
print(f"  {L2}")
print(f"  {'Maximo':<18} {rel['max_var_pct']*100:>9.4f}%")

print(f"\n  Expected Shortfall 99% (CVaR)")
print(f"  {L2}")
print(f"  {'ES Historico':<18} {h['es_pct_99']*100:>9.4f}%   R$ {h['es_brl_99']:>13,.2f}")
print(f"  {'ES Monte Carlo':<18} {mc['es_mc_pct']*100:>9.4f}%   R$ {mc['es_mc_brl']:>13,.2f}")

print(f"\n  VaR 10d regulatorio (Basileia)")
print(f"  {L2}")
print(f"  {'Historico 10d':<18} {h['var_10d_pct_99']*100:>9.4f}%")
print(f"  {'EWMA 10d':<18} {e['var_ewma_10d_brl']/NOCIONAL*100:>9.4f}%   R$ {e['var_ewma_10d_brl']:>13,.2f}")

print(f"\n  Backtesting -- Basileia II (janela 250 dias uteis)")
print(f"  {L2}")
print(f"  Excecoes          : {bt['n_excecoes']:>3}  ({bt['taxa_excecao']*100:.2f}%  esperado ~1%)")
print(f"  Semaforo          : {bt['semaforo']}")

if st is not None:
    print(f"\n  Stress Test -- cenarios avaliados")
    print(f"  {L2}")
    print(f"  {'Retorno':>10}  {'Perda BRL':>16}  {'Mult. VaR':>10}  Classificacao")
    for i in range(len(CENARIOS_STRESS)):
        print(
            f"  {CENARIOS_STRESS[i]*100:>9.2f}%"
            f"  R$ {st['perda_brl'][i]:>13,.2f}"
            f"  {st['multiplo_var'][i]:>9.2f}x"
            f"  {st['classificacao'][i]}"
        )

print(f"\n  {rel['alerta_limite']}")
print(f"{L}\n")
