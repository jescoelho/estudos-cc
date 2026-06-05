---
name: model-to-python
description: >
  Deriva Python estruturado e auditável a partir de artefatos de modelo quantitativo
  (Excel .xlsx/.xlsm/.xls e/ou Python .py) via pipeline de 4 fases:
  inventário → grafo → arquitetura → tradução e auditoria.
  ATIVAR quando: usuário envia .xlsx, .xlsm, .xls ou .py e solicita gerar Python,
  converter planilha em código, documentar lógica de modelo, derivar pseudoalgoritmo,
  traduzir fórmulas para Python, auditar completude de modelo, ou mapear dependências.
  Domínios cobertos: risco de mercado (VaR/ES/Greeks/PnL/stress/FRTB), precificação
  de produto (empréstimos, financiamentos, leasing, FX), ALM (duration gap, NII, EVE,
  NMD), seguros (prêmio, sinistro, IBNR), lucratividade/FTP/spread, scoring
  comportamental/propensão. EXCLUÍDO: risco de crédito (PD/LGD/EAD/ECL/IFRS9).
  Ativar sempre para arquivos .xlsx, .xlsm, .xls ou .py mesmo quando a solicitação
  for expressa informalmente.
compatibility: "claude.ai, Claude Desktop, Cowork — requer bash_tool para leitura de arquivo"
---

# Model-to-Python — Receita de Bolo

Pipeline de derivação de Python auditável a partir de artefatos quantitativos.
**Domínio excluído:** modelos de risco de crédito (PD/LGD/EAD/ECL/IFRS9).

---

## INGREDIENTES

| Ingrediente | Obrigatório | Como fornecer |
|---|---|---|
| Artefato Excel (.xlsx / .xlsm / .xls) | Pelo menos 1 dos 2 | Caminho do arquivo (Claude Code/Desktop) ou upload (Claude.ai) |
| Artefato Python (.py) | Pelo menos 1 dos 2 | Caminho do arquivo (Claude Code/Desktop) ou upload (Claude.ai) |
| Contexto de domínio | SIM | Nome do arquivo, imports visíveis, ou descrição do usuário |

Resolução de acesso ao artefato: ver `references/phases/phase1.md` → seção "Localizar Artefato".

---

## REGRAS GLOBAIS

```
R1 — Toda decisão cita sua evidência
     Estrutural: citar métrica de grafo | Semântica: citar campo de inventário

R2 — Informação ausente → "NÃO ENCONTRADO" — nunca omitir, nunca inferir silenciosamente
     Inferências obrigatoriamente marcadas [INFERÊNCIA]

R3 — Ciclo no grafo = BLOQUEADOR — não gerar código até resolver (ver Protocolo de Bloqueio)

R4 — O grafo enriquecido (saída da Fase 2) é a única fonte de verdade para Fases 3 e 4
     — nunca retornar aos artefatos brutos após a Fase 2
```

---

## PROTOCOLO DE BLOQUEIO

Aplica-se a qualquer fase. Ao encontrar um bloqueador:

```
1. Registrar o bloqueador com evidência (célula, nó, linha de código)
2. Classificar: ESTRUTURAL (ciclo, aba indefinida) |
                SEMÂNTICO  (fórmula ambígua, tipo incerto) |
                EXTERNO    (dados ausentes, artefato ilegível)
3. Escalar ao usuário com pergunta específica e objetiva
4. Aguardar resposta antes de prosseguir para a próxima fase
5. Registrar resolução na planilha de consolidação da fase corrente
```

---

## SEQUÊNCIA DE EXECUÇÃO

Carregar o arquivo de fase antes de iniciar cada fase. Não pular fases.

```
FASE 1 → references/phases/phase1.md → Gate 1 aprovado → FASE 2
FASE 2 → references/phases/phase2.md → Gate 2 aprovado → FASE 3
FASE 3 → references/phases/phase3.md → Gate 3 aprovado → FASE 4
FASE 4 → references/phases/phase4.md → Gate 4 aprovado → ENTREGAR
```

---

## ENTREGÁVEIS

| Tipo | Arquivo | Quando |
|---|---|---|
| Principal | `<nome_modelo>.py` — Python completo e estruturado | Sempre |
| Runner | `<nome_modelo>_run.py` — script executável standalone com carregamento de dados e `__main__` | Sempre |
| Documentação | `derivation_sheet.md` — planilha consolidada preenchida | Sempre |
| Pseudocódigo | `pseudoalgorithm_highlevel.txt` | Sempre |
| Pseudocódigo | `pseudoalgorithm_detailed.txt` | Sempre |
| Notação | `notation_table.md` | Sempre |
| Opcional | `pseudoalgorithm_<nome_modelo>.docx` | Se usuário solicitar |
| Opcional | `graph_L2.md` — grafo enriquecido exportado | Se usuário solicitar |

---

## ÍNDICE DE REFERÊNCIAS

| Arquivo | Carregado em |
|---|---|
| `references/phases/phase1.md` | Início da Fase 1 |
| `references/phases/phase2.md` | Início da Fase 2 |
| `references/phases/phase3.md` | Início da Fase 3 |
| `references/phases/phase4.md` | Início da Fase 4 |
| `references/domains/market-risk.md` | Fase 1 — domínio risco de mercado |
| `references/domains/product-pricing.md` | Fase 1 — domínio precificação de produto |
| `references/domains/alm-insurance-profitability-scoring-generic.md` | Fase 1 — domínio ALM, seguros, lucratividade, scoring ou indefinido |
| `references/inventory-python.md` | Fase 1 — Bloco A (artefato .py) |
| `references/inventory-excel.md` | Fase 1 — Bloco B (artefato Excel) |
| `references/inventory-reconciliation.md` | Fase 1 Bloco C + Fase 2 (seções Graph) |
| `references/architecture.md` | Fase 3 — prompts 3.1, 3.2 |
| `references/pseudoalgorithm-generator.md` | Fase 3 — prompts 3.3-A/B/C/D |
| `references/formula-translation.md` | Fase 4 — prompts 4.1, 4.2 |
