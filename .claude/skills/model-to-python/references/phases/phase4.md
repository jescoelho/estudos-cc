# Fase 4 — Tradução e Auditoria
*Pipeline: Fase 1 → Fase 2 → Fase 3 → **FASE 4***
*Entrada: Assinaturas de funções + Pseudoalgoritmo (Gate 3 aprovado) — não retornar aos artefatos brutos (R4)*

---

## Carregue

```
references/formula-translation.md  → prompts 4.1, 4.2 e regras de tradução
```

---

## Modo de Preparo

**4.1 — Tradução de fórmulas**
Seguir `references/formula-translation.md` prompt 4.1.
Para cada nó que se torna função Python: traduzir fórmula Excel com tipos do grafo enriquecido.
Adicionar tratamentos de caso-borda de A.6. Registrar nível de confiança (ALTA / MÉDIA / BAIXA).

**4.2 — Montagem do corpo de função**
Seguir `references/formula-translation.md` prompt 4.2.
Ordem dentro de cada função: validações de entrada → ordem topológica → comentários inline
com referências de célula Excel → handlers de caso-borda → return.

**4.3 — Auditoria de completude**
Verificar que 100% dos nós L2 do grafo enriquecido estão cobertos no código gerado.

**4.4 — Auditoria de ordem de execução**
Verificar que a ordenação topológica é respeitada em cada função.

**4.5 — Auditoria de arquitetura**
Verificar: acoplamento, coesão, comprimento de função, ausência de variáveis globais,
rastreabilidade e cobertura de casos-borda.

**4.6 — Script executável (`<nome_modelo>_run.py`)**

Gerar um script standalone que, ao ser executado com `python <nome_modelo>_run.py`, carrega
os dados e chama o ponto de entrada sem nenhuma dependência manual.

```
REGRAS:

1. CARREGAMENTO DE DADOS (usar bash_tool para inspecionar estrutura se necessário)
   → Preços / série principal: pd.read_excel(PATH, sheet_name=..., usecols=...) 
     filtrar linhas com datas válidas; descartar rodapé de estatísticas.
   → Cenários de estresse: montar pd.DataFrame com colunas ['nome','retorno_shock']
     a partir dos valores lidos na aba STRESS_TEST (B e C) ou hardcoded da Fase 1.

2. MONTE CARLO
   → Se a aba MC contém VALORES FIXOS (detectado em B.1 pelo título ou ausência de fórmulas):
       Gerar com numpy: rng = np.random.default_rng(SEED); cenarios_mc = rng.normal(mu, sigma, N_MC)
       Expor SEED como constante configurável no topo do script.
       Adicionar comentário: # MC original usa valores fixos — gerado aqui com seed para reprodutibilidade
   → Se a aba MC contém fórmulas de geração: extrair lógica e replicar.

3. CONFIGURAÇÃO NO TOPO DO SCRIPT
   Expor como constantes nomeadas (MAIÚSCULAS) todos os parâmetros que o usuário
   pode querer ajustar: ARQUIVO_EXCEL, SEED, N_MC, NOCIONAL, CONF_99, etc.

4. BLOCO __main__
   if __name__ == "__main__":
       → carregar dados
       → instanciar config
       → chamar ponto de entrada
       → imprimir painel de resultados legível (sem dependências externas de visualização)

5. NOMES DE CHAVES
   O script deve usar EXATAMENTE as chaves do dict retornado pelo ponto de entrada
   gerado em 4.2 — nunca inventar nomes. Verificar antes de escrever cada acesso.
```

---

## Verificação — Gate 4

```
[ ] Todas as fórmulas traduzidas com tipo correto
[ ] Todos os casos-borda tratados (A.6 cobertos + novos adicionados e marcados)
[ ] Auditoria 4.3 aprovada — 100% dos nós L2 cobertos
[ ] Auditoria 4.4 aprovada — ordem topológica respeitada em todas as funções
[ ] Auditoria 4.5 aprovada — sem bloqueadores de arquitetura
[ ] 4.6 — runner gerado; chaves de acesso conferidas contra dict de retorno de 4.2
[ ] Planilha de Derivação Consolidada preenchida
[ ] STATUS = COMPLETO → entregar todos os artefatos listados em SKILL.md
```

> **GATE FAIL** → aplicar Protocolo de Bloqueio (SKILL.md) e listar refatorações pendentes para o usuário.
