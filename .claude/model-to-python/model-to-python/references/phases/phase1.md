# Fase 1 — Inventário Técnico
*Pipeline: → **FASE 1** → Fase 2 → Fase 3 → Fase 4*

---

## Localizar Artefato

Execute este passo antes de qualquer outro. O inventário só começa com o artefato acessível.

```
PASSO 0 — Confirme o modo de acesso:

  Caminho fornecido na mensagem + bash_tool disponível
    → .py   : ler com open() / cat via bash
    → .xlsx / .xlsm / .xls : extrair estrutura com openpyxl ou xlrd via bash
              comando mínimo: python -c "import openpyxl; wb = openpyxl.load_workbook('<path>'); print(wb.sheetnames)"

  Arquivo enviado como upload (Claude.ai)
    → conteúdo já visível na conversa — prosseguir diretamente

  Nenhum dos dois
    → solicitar ao usuário: caminho completo do arquivo ou upload antes de continuar

Resultado esperado: conteúdo do artefato acessível e confirmado antes do PASSO 1.
```

---

## Carregue

```
PASSO 1 — Identifique o domínio provável:
  nome do arquivo + imports visíveis + contexto do usuário

PASSO 2 — Carregue o arquivo de domínio correspondente:
  risco de mercado      → references/domains/market-risk.md
  precificação produto  → references/domains/product-pricing.md
  ALM / balanço         → references/domains/alm-insurance-profitability-scoring-generic.md  § seção "ALM / Balance Sheet"
  seguros               → references/domains/alm-insurance-profitability-scoring-generic.md  § seção "Insurance"
  lucratividade / FTP   → references/domains/alm-insurance-profitability-scoring-generic.md  § seção "Profitability / FTP"
  scoring / propensão   → references/domains/alm-insurance-profitability-scoring-generic.md  § seção "Scoring / Behavioural"
  domínio indefinido    → references/domains/alm-insurance-profitability-scoring-generic.md  § seção "Generic"

PASSO 3 — Carregue apenas os blocos aplicáveis:
  Artefato .py presente    → references/inventory-python.md
  Artefato Excel presente  → references/inventory-excel.md
  Ambos presentes          → references/inventory-reconciliation.md
```

---

## Modo de Preparo

Execute os blocos em ordem. Não avançar para o próximo bloco com bloqueadores abertos.

**Bloco A — Inventário Python** *(se artefato .py presente)*
Seguir todos os prompts de `references/inventory-python.md` em sequência:
A.1 Reconhecimento físico → A.2 Mapa de dependências → A.3 Mapa de estrutura de funções →
A.4 Ponto de entrada → A.5 Separação input/parâmetro/output → A.6 Casos de exceção

**Bloco B — Inventário Excel** *(se artefato Excel presente)*
Seguir todos os prompts de `references/inventory-excel.md` em sequência:
B.1 Reconhecimento físico → B.2 Classificação de abas → B.3 Named ranges →
B.4 Fórmulas-chave → B.5 Dependências inter-abas → B.6 VBA/macros

**Bloco C — Reconciliação** *(apenas se ambos os artefatos presentes)*
Seguir prompts de `references/inventory-reconciliation.md`:
C.1 Reconciliação de inputs → C.2 Reconciliação de outputs → C.3 Fonte primária

---

## Verificação — Gate 1

```
[ ] Todos os blocos aplicáveis executados
[ ] Planilha de Inventário Consolidado preenchida (ver inventory-python.md)
[ ] Nenhum campo em branco — lacunas marcadas NÃO ENCONTRADO
[ ] Nenhum bloqueador aberto
[ ] STATUS = COMPLETO → carregar references/phases/phase2.md e iniciar Fase 2
```

> **GATE FAIL** → aplicar Protocolo de Bloqueio (SKILL.md) antes de avançar.
