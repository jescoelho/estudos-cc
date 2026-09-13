# Planejamento — Skill: Documentação Técnica de Modelos

## Estado atual

Skill original gera `.docx` a partir de modelos quantitativos (Excel, Python, VBA).
Expansão em andamento: 6 módulos novos com extração única compartilhada entre todos.
Nenhum módulo concluído. Trabalho iniciado em `feature/pseudoalgoritmo`.

---

## Demandas

| ID | Módulo | Status | Branch |
|---|---|---|---|
| M01 | Pseudoalgoritmo | em andamento | `feature/pseudoalgoritmo` |
| M02 | Calculadora Excel | aguardando | — |
| M03 | Análise de performance | aguardando | — |
| M04 | Painel de simulações | aguardando | — |
| M05 | Versionamento Git | aguardando | — |
| M06 | Artefato OOP/MaaS | aguardando | — |

Status possíveis: `aguardando` · `em andamento` · `em revisão` · `concluído`

---

<!-- O Claude lê abaixo apenas ao trabalhar em uma demanda específica -->

## Detalhamento

### M01 — Pseudoalgoritmo
**Objetivo:** gerar representação algorítmica legível da lógica extraída do modelo.
**Entrada:** objeto de contexto produzido pela extração da skill original.
**Saída:** `.md` com pseudoalgoritmo estruturado por função/bloco lógico.
**Decisões abertas:**
- Granularidade: por função individual ou por fluxo geral do modelo?
- Nomenclatura: português ou inglês nas variáveis do pseudoalgoritmo?

### M02 — Calculadora Excel
**Objetivo:** gerar planilha exemplo navegável com inputs/outputs do modelo.
**Entrada:** objeto de contexto da extração + parâmetros identificados.
**Saída:** `.xlsx` com abas separadas para inputs, cálculos e outputs.
**Decisões abertas:**
- Escopo: replicar toda a lógica ou apenas exemplificar os principais parâmetros?

### M03 — Análise de performance
**Objetivo:** avaliar comportamento e limites do modelo sob diferentes condições.
**Entrada:** objeto de contexto da extração + fixtures de teste.
**Saída:** `.py` com métricas, gráficos e sumário de resultados.
**Decisões abertas:**
- Quais métricas são obrigatórias vs. opcionais por domínio?

### M04 — Painel de simulações
**Objetivo:** interface para simular o modelo variando parâmetros interativamente.
**Entrada:** objeto de contexto da extração.
**Saída:** `.py` (Streamlit ou similar) com controles por parâmetro e visualização.
**Decisões abertas:**
- Tecnologia: Streamlit, Gradio ou outro?
- Deve rodar localmente ou ser deployável?

### M05 — Versionamento Git
**Objetivo:** rastrear alterações em documentações técnicas já geradas.
**Entrada:** artefatos gerados em sessões anteriores + estado atual do repo.
**Saída:** entrada no `CHANGELOG.md` da documentação + commit automático.
**Decisões abertas:**
- Onde vive o `CHANGELOG.md` — no repo de modelagem ou no repo das documentações?
- Integração com o GitHub Pages (wiki em construção pela equipe)?

### M06 — Artefato OOP/MaaS
**Objetivo:** gerar classe Python com interface padronizada para consumo via API.
**Entrada:** objeto de contexto da extração.
**Saída:** `.py` com classe estruturada (interface a definir).
**Decisões abertas:**
- Interface da classe: `fit` / `predict` / `validate` ou outra convenção?
- O que significa "Modeling as a Service" no contexto do banco — API REST, SDK interno?
