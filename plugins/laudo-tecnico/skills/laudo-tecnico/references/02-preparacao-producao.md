# Fase 2 — Preparação para Produção (dev → hml → prod)

Frameworks: Production Readiness Review (PRR) para 2.1, RAID log para 2.2.
Depende de: output da Fase 1 (1.2 e 1.3).

## 2.1 — Production Readiness Review (PRR): mapeamento de ambientes

```
Com base no grafo graphify do repositório — consulte com `graphify query`,
`graphify explain` e `graphify path` em vez de abrir arquivos brutos — e no
fluxo mapeado na Fase 1, produza um checklist de Production Readiness.
Organize a resposta em uma tabela com uma linha por item, usando estes
rótulos exatos na coluna "Item PRR":

[Item PRR | Situação atual | Evidência no repositório]
- Estágio atual — estágio (dev/hml/prod) de cada componente hoje
- Promoção — o que falta para promover cada componente ao próximo estágio
  (testes, aprovações, configs específicas de ambiente, credenciais)
- Dependências de infraestrutura — por ambiente (armazenamento, permissões,
  segredos/credenciais, filas); quais já existem e quais precisam ser criadas
- Gates — gates de qualidade/validação exigidos entre estágios (testes
  automatizados, aprovação manual, etc.)
- Observabilidade — monitoramento, alertas, ou plano de rollback
  documentado no repositório

Não invente. Para cada linha, se a evidência não existir no repositório —
seja um processo de promoção entre ambientes, um gate de qualidade,
monitoramento, ou qualquer outro item da lista — a linha correspondente
recebe "não encontrado no repositório" em vez de assumir um padrão
genérico de mercado. Isso vale para as 5 linhas, não só para "Promoção".
```

## 2.2 — RAID log: riscos e dependências críticas

```
Consultando o grafo graphify do repositório (`graphify query`, `graphify
path`) e a demanda, produza um RAID log:

1. Risks — pontos únicos de falha (single points of failure); o que pode
   falhar se uma dependência externa mudar formato de resposta, limite de
   uso, ou ficar indisponível durante uma carga crítica (ex: carga histórica
   única)
2. Assumptions — premissas que o código ou a demanda dão como certas mas
   não estão validadas (ex: formato de dado estável, disponibilidade de
   API, volume esperado)
3. Issues — problemas já identificados e não resolvidos no repositório
   (bugs conhecidos, débito técnico explícito, TODOs relevantes)
4. Dependencies — dependências de terceiros/times (quem precisa aprovar,
   prover acesso, ou revisar antes de ir para produção)

Separe itens verificados no código/documentação de itens hipotéticos
levantados por precaução — marque os hipotéticos como tal.
```

## Critério de qualidade

- Tabela de 2.1 tem todas as linhas preenchidas — linha ausente = item não checado, não item "não aplicável" por omissão
- RAID log cobre as 4 categorias — não colapsar em uma lista única de "riscos"
- Sem itens genéricos de boas práticas de DevOps sem evidência no repositório — se não há CI/CD, apontar a ausência, não sugerir pipeline genérico
