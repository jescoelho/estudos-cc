# Fase 3 — Justificativa (valor de negócio e custo)

Frameworks: Business Case para 3.1, TCO (Total Cost of Ownership) para 3.2.
Depende de: Fase 1 (demanda/To-Be); idealmente Fase 2 (dependências de infraestrutura do PRR 2.1, para custo).

## 3.1 — Business Case: valor para o negócio

```
Com base na demanda extraída (Fase 1) e no que o pipeline entrega, produza
um Business Case. Organize a resposta em uma tabela com uma linha por item,
usando estes rótulos exatos na coluna "Item":

[Item | Resposta | Status]
- Problema/oportunidade — que decisão de negócio ou processo depende
  desses dados/entregável (quem consome, para quê); cite trechos da
  transcrição/demanda que sustentem isso
- Custo de não agir — custo de não ter isso automatizado/entregue hoje
  (processo manual, atraso, risco de erro); inclua apenas se houver menção
  explícita na fonte da demanda
- Métricas de sucesso — métricas mencionadas ou implícitas na demanda

Status = "especificado" ou "não especificado" — nunca inferido. Se a fonte
da demanda não mencionar valor de negócio explicitamente, a linha recebe
"não especificado" — não infira benefício genérico do tipo "automação
sempre economiza tempo". Valor sem evidência na fonte é opinião, não
Business Case.
```

## 3.2 — TCO: custo baseado em fatos

```
Consultando o grafo graphify do repositório (`graphify query` sobre os
componentes de infraestrutura, em vez de reler arquivos) e, se disponível,
as dependências de infraestrutura por ambiente já levantadas na Fase 2.1
(PRR), identifique os componentes envolvidos e calcule o TCO. Organize a
resposta em uma tabela com uma linha por item, usando estes rótulos exatos
na coluna "Item":

[Item | Valor/Cálculo | Fato ou Estimativa?]
- Serviços e cobrança — serviços utilizados e modelo de cobrança de cada
  um (por requisição, por GB, por hora de execução, etc.). Buscar a
  documentação oficial atual de cada serviço/provedor (web search ou
  ferramenta equivalente) — não recitar preço de memória/treinamento, já
  que tabelas de cobrança mudam com o tempo e um valor lembrado não é o
  mesmo que um valor verificado agora. Se não for possível verificar,
  marcar como estimativa, nunca como fato
- Volume de dados — para cargas de grande volume (ex: histórico completo),
  volume aproximado com base no que está documentado no repositório/demanda
  (registros esperados, tamanho médio de registro); apresente o cálculo,
  não só o resultado
- Custo de implementação — custo do evento único (ex: carga histórica)
- Custo operacional — custo recorrente (ex: incremental)

Coluna "Fato ou Estimativa?": marque explicitamente cada linha. Para itens
verificados (ex: preços buscados agora), marcar "Fato (verificado em
[data])". Para estimativas, inclua a base da suposição (ex: "estimativa
baseada em X, requer validação com o time de infraestrutura").
```

## Critério de qualidade

- Tabelas de 3.1 e 3.2 têm todas as linhas preenchidas — linha ausente = item não respondido
- Todo número ou afirmação de valor tem fonte (demanda, doc oficial, cálculo) ou está marcado como estimativa não validada
- TCO sempre separado em implementação vs. operação — nunca um número único misturando os dois
- Fato e suposição misturados sem sinalização = não apresentar em conversa de negócio
