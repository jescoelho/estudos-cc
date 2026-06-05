# -*- coding: utf-8 -*-
"""Script temporario para inspecionar estrutura do Excel."""
import pandas as pd, openpyxl, json, sys

ARQUIVO = r"C:\Users\jecoe\grafos\aplicacao\VaR_Ibovespa_Modelo_Bancario.xlsx"

wb = openpyxl.load_workbook(ARQUIVO, read_only=True, data_only=True)
print("=== ABAS ===")
for sh in wb.sheetnames:
    ws = wb[sh]
    print(f"\n--- {sh} ({ws.max_row} linhas x {ws.max_column} cols) ---")
    for r in ws.iter_rows(min_row=1, max_row=min(5, ws.max_row), values_only=True):
        print(r)
wb.close()
