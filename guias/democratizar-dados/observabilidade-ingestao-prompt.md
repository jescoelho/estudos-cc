# Prompt de desenvolvimento: observabilidade de ingestão

Um único prompt para o agente construir, em dev, os 5 checks de observabilidade e a tabela de resultados.

## Premissas

O piloto começa em dev (depois hml e prod), e cada ambiente tem as próprias tabelas de log: nenhuma tabela tem coluna de ambiente.

- **Ambiente por configuração, não por dado.** A variável `AMBIENTE` (dev|hml|prod) só resolve banco, caminho S3 e tópico SNS. Ela nunca é gravada nas linhas.
- **Baseline isolado por construção.** Como cada ambiente lê e grava só nas suas tabelas, o histórico dos checks HISTORICO não atravessa ambientes. Limiar calibrado em hml precisa ser revisado na promoção (nova `versao_check`).
- **FAIL:** o check mediu e o dado violou a regra. Roteia ao owner do dado.
- **ERRO:** o check não conseguiu medir. Roteia ao owner do pipeline. ERRO nunca vira PASS.
- **NAO_AVALIADO:** não há base para avaliar (histórico insuficiente e sem limiar fixo). É registrado, mas não alerta nem bloqueia.
- **Entradas do usuário:** apenas o dataset de exemplo e o local dos dados no S3. O restante vem do output do graphify; se não estiver lá, o agente procura no repositório e, se não achar, pergunta.
- **Sem backfill.** Painel e modo sombra ficam para depois, só se o piloto funcionar.

## Prompt (dev)

Cole no agente com acesso ao repositório e preencha os campos entre `<>` (dataset, local no S3 e caminho do graphify).

```text
# PAPEL
Você é um engenheiro de dados sênior implementando um piloto de observabilidade de ingestão em AWS (S3, Glue, Athena, Iceberg), no ambiente DEV. Seja direto. Não crie nada além do que está pedido.

# CONTEXTO
1 dataset, 5 checks, 1 tabela de resultados. Cada check é uma pergunta de sim/não definida em um YAML; cada execução grava uma linha de resultado, ligada à pergunta por `check_id` + `versao_check`.
- FAIL = o check mediu e o dado violou a regra.
- ERRO = o check não conseguiu medir. ERRO nunca vira PASS.
- NAO_AVALIADO = não há base para avaliar (histórico insuficiente e sem limiar fixo). É registrado, mas não alerta nem bloqueia.
- A tabela não tem coluna de ambiente. A variável `AMBIENTE` (dev|hml|prod) só resolve banco e caminho S3.

# ENTRADAS DO USUÁRIO
- dataset: <nome>
- local dos dados no S3: <s3://...>

# ENTRADAS DERIVADAS
Leia o output do graphify (<caminho>) e monte a ficha da tabela: motor de consulta, tipo de carga (full ou incremental), periodicidade, partição, coluna de data de referência, schema do contrato, chave única, colunas críticas com limite de nulos, SLA de freshness, owner do dado, owner do pipeline, destino do alerta, convenção de IaC.
- Se o graphify não trouxer um item, procure no repositório. Se ainda não achar, PARE e me pergunte. Nunca invente.
- Registre a origem de cada item em comentário no `checks.yaml`.
- Antes de implementar, mostre a ficha da tabela (item, valor e origem) e, ao lado, quais checks se aplicam e quais não, com o motivo. Aguarde minha confirmação.

# TAREFAS (após minha confirmação)
1. `catalogo_perguntas.yaml` (único e genérico, vale para qualquer tabela da área) com os 5 tipos abaixo, cada um com `modelo_pergunta` (placeholders como {tabela}, {coluna}, {sla}, {chave}) e `requer` (o que a ficha precisa ter para o check se aplicar). Depois, `checks.yaml` da tabela, gerado só a partir do catálogo e da ficha (nenhuma pergunta escrita à mão), cada check com: tipo_check, etapa, coluna (se aplicável), pergunta (sim/não), modo (REGRA|HISTORICO), parametros, severidade (BLOQUEANTE), owner, versao_check=1.
   - FRESHNESS (REGRA): a última carga de {tabela} chegou dentro do SLA de {sla}? Requer: SLA ou periodicidade na ficha.
   - VOLUME (HISTORICO): a contagem de linhas de {tabela} na data de referência está dentro da faixa esperada? Sempre aplicável; a ficha define se a carga é full ou incremental, e a comparação usa só cargas do mesmo tipo. Histórico = resultados PASS anteriores do mesmo check_id e versao_check. Com 10 ou mais PASS e MAD maior que 0: mediana ± 3·MAD das últimas 30; se houver 4 ou mais PASS por dia da semana, restrinja ao mesmo dia da semana. Caso contrário, use o limiar fixo do YAML. Sem histórico suficiente e sem limiar fixo: NAO_AVALIADO. Registre em `detalhe` o método usado (HISTORICO_GERAL, HISTORICO_DIA_SEMANA ou LIMIAR_FIXO).
   - SCHEMA (REGRA): o schema de {tabela} é idêntico ao contrato? Requer: contrato ou DDL de referência.
   - UNICIDADE (REGRA): a chave {chave} de {tabela} é única? Requer: chave declarada.
   - NULOS (REGRA): um check por coluna crítica; a fração de nulos em {coluna} está dentro do limite? Requer: coluna obrigatória ou crítica declarada no contrato.
   - Aplicabilidade: se o `requer` de um check não for atendido pela ficha, o check NÃO é criado. Registre-o no `checks.yaml` como `aplicavel: false` com o `motivo`. Nunca infira chave, coluna crítica, SLA ou contrato.
   - Generalidade: nenhum nome de tabela, coluna ou valor fixo no código; tudo vem da ficha e do catálogo.
2. DDL Iceberg da tabela `obs_check_resultado`: run_id, dataset, check_id, versao_check, data_referencia, status (PASS|FAIL|ERRO|NAO_AVALIADO), valor_observado, limite_min, limite_max, baseline, ts_inicio, ts_fim, detalhe.
3. `run_check.py`: `montar_check_id` (`{dataset}.{etapa}.{tipo_check}[.{coluna}]`, nunca digitado à mão), uma função de medição por tipo_check em um REGISTRY, `run_check` (qualquer exceção vira ERRO com a mensagem em `detalhe`) e `run_all(dataset, run_id, ctx)` que retorna `(bloquear, resumo)`; `bloquear=True` só com FAIL ou ERRO de severidade BLOQUEANTE. Grave sempre valor observado e limites, mesmo em PASS. Reaproveite utilitários e padrões do repositório.
4. Testes (pytest): por tipo_check, um caso PASS, um FAIL e um ERRO; para VOLUME, também: histórico insuficiente com limiar fixo, histórico insuficiente sem limiar (NAO_AVALIADO), MAD igual a 0, e histórico suficiente com e sem filtro por dia da semana; no alerta, FAIL e ERRO roteados a destinos distintos e falha de envio propagada como erro.
5. Alerta AWS: `alerta.py` chamado após `run_all`. Se houver FAIL ou ERRO, publica no SNS dataset, run_id, check_id, pergunta, status, valor_observado, limites e severidade. FAIL vai ao owner do dado; ERRO vai ao owner do pipeline (dois tópicos ou filtro por atributo). Falha de envio é logada e propagada, nunca silenciada. Crie o tópico SNS e as permissões com o padrão de IaC do repositório, com menor privilégio e recursos exclusivos de DEV.
6. Execução real em DEV: rode `run_all` sobre uma carga real e confirme 1 linha por check, todas com o mesmo `run_id`; simule um FAIL e um ERRO e confirme que cada alerta chega ao destino correto.

# RESTRIÇÕES
- Fora do escopo: painel, backfill, catálogo em tabela, modo sombra.
- Sem credenciais no código. Reexecutar o mesmo run_id não duplica linhas (MERGE por run_id+check_id).
- Siga as convenções do repositório e liste cada arquivo criado com o caminho.

# ACEITE
Testes passam; a execução real grava 1 linha por check; o FAIL e o ERRO simulados geram alertas nos destinos corretos; um join entre o YAML e a tabela por check_id e versao_check retorna pergunta, status, valor e limites.

# RESPOSTA
1) Tabela de entradas com origem e pendências. 2) Após confirmação, arquivos criados. 3) Resultado da execução real. 4) Até 5 linhas do que ficou assumido ou pendente.
```
