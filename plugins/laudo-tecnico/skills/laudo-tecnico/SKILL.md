---
name: laudo-tecnico
description: Recebe uma transcrição de reunião ou demanda técnica em texto (e-mail, ticket, briefing) e cruza com um repositório existente para produzir um diagnóstico completo - o que é pedido, o que já existe no repositório, o que falta, o caminho até produção, o valor/custo de negócio e a ordem de execução. Use sempre que o usuário fornecer uma transcrição/demanda em texto E um repositório para analisar; quando disser que "herdou" um repositório ou projeto; que recebeu uma demanda em área que "nunca fez antes"; ou que precisa levar um projeto de dev para produção e justificar valor/custo. Não escreve código de produção - produz um diagnóstico estruturado que orienta o próximo passo.
compatibility: Requer o CLI graphify instalado e configurado (github.com/Graphify-Labs/graphify) para qualquer análise de repositório. Python 3 recomendado para rodar o script de validação em scripts/validar_diagnostico.py.
---

# Laudo Técnico do Repositório

## Entrada
- Demanda em texto: transcrição, e-mail, ticket, briefing — colada na conversa ou em arquivo, sem exigência de formato
- Repositório: por padrão, é aquele em que a skill foi invocada (diretório de trabalho atual) — não é preciso informar caminho nem URL nesse caso comum
- Repositórios adicionais (opcional): se a análise depender de outro repositório (ex: uma lib compartilhada, um serviço relacionado), o usuário pode fornecer caminho local ou URL desses repositórios extras — nesse caso, clonar primeiro (`git clone` ou `graphify clone <url>`) antes de rodar `/graphify .` neles
- Sem a demanda: perguntar diretamente — "Você tem a transcrição, e-mail ou outro registro dessa demanda?"
- Se o diretório de trabalho atual não for um repositório de código (ex: sem `.git`): perguntar diretamente — "Qual é o caminho local ou a URL do repositório que devo analisar?"
- Não prosseguir com suposição sobre o que ainda não foi fornecido

## Transcrição — regras
- Efêmera: usada só na Fase 1.1
- Nunca salvar como arquivo no repositório, nunca commitar, nunca referenciar por caminho de arquivo
- Persiste apenas o output da extração (resumo estruturado), nunca a transcrição bruta

## Pré-requisito obrigatório: graphify
- Obrigatório para qualquer análise de repositório — leitura manual arquivo por arquivo não é alternativa
- Escopos diferentes, não confundir:
  - `graphify install` — registra a skill do graphify no assistente. Configuração **global, uma única vez** (não repete por repositório)
  - `/graphify .` (build do grafo) — escopo por repositório, não por máquina: cada repositório precisa do próprio grafo (o de um não serve para outro), seja em sessões futuras num repositório diferente, seja num repositório adicional fornecido na mesma sessão (seção "Entrada"). "Repositório atual" = diretório de trabalho onde a skill foi invocada, por padrão. Rodar `/graphify .` na raiz de cada repositório antes de consultá-lo; rodar de novo com `--update` se o repositório mudou desde a última sessão
- Checar se o grafo já existe para o repositório atual (`graphify-out/graph.json`); se ausente, rodar `/graphify .` na raiz antes de prosseguir — não é preciso reinstalar o graphify se ele já está registrado globalmente
- Se o comando `graphify` não for encontrado, consultar `references/00-setup-graphify.md` antes de concluir que está indisponível — geralmente é PATH desatualizado, não instalação quebrada
- Só parar e avisar o usuário se, mesmo após consultar aquele arquivo, o comando `graphify` genuinamente não estiver disponível e não puder ser instalado nesta sessão — sem fallback silencioso para leitura manual
- Preferir sempre `graphify query`, `graphify explain`, `graphify path` em vez de ler arquivos brutos

## Princípio central
- Informação ausente na fonte (transcrição, repositório, documentação) → "não especificado" ou "requer validação com X"
- Nunca inferência genérica preenchendo a lacuna
- Vale também para a Fase 4: nenhum item de EAP é inventado — todo pacote de trabalho rastreia a um Gap/PRR/RAID já levantado
- Todo item numerado de um prompt precisa aparecer refletido no output — itens pulados ou combinados silenciosamente com outros contam como execução incompleta. Para os prompts 1.1, 1.2, 1.3, 2.1, 3.1, 3.2 e 4.1, isso agora é checável pelo script de validação (tabelas com rótulos fixos por linha). Para 2.2 (RAID), as 4 categorias já servem como marcador. O que o script não cobre: instruções de raciocínio dentro de um item (ex: "ordene por dependência técnica", "não estime a menos que a fonte informe") — essas continuam dependendo de disciplina na hora de responder, não de verificação automática.

## Fases e frameworks adotados

| Fase | Responde | Framework | Depende de | Pular quando |
|---|---|---|---|---|
| 1. Entendimento | O que é a demanda; o que já existe | Gap Analysis (As-Is/To-Be) + C4 Model + DoR (gate de entrada) | — | Nunca — base do processo |
| 2. Execução | O que falta para produção; o que pode falhar | Production Readiness Review (PRR) + RAID log | Fase 1 | Objetivo é só entender o código |
| 3. Justificativa | Por que importa; quanto custa | Business Case + TCO | Fase 1 (obrigatório); Fase 2 (idealmente, para custo de infraestrutura) | Objetivo é só mapeamento técnico |
| 4. Planejamento | Em que ordem executar | EAP (WBS) | Fase 1 (obrigatório); Fase 2 (idealmente); Fase 3 (opcional, só prioridade) | Nunca — obrigatória, como a Fase 1 |

## Persistência — evitar truncamento em sessões longas
- Declarar instruções em texto não garante execução completa sem truncamento — ver salvaguardas abaixo
- Conforme cada fase é executada, salvar o output em disco: `laudo-tecnico-output/01-entendimento.md`, `02-execucao.md`, `03-justificativa.md`, `04-planejamento.md` (conforme aplicável)
- Não depender só da memória da conversa para consolidar ao final — reler os arquivos salvos ao montar o diagnóstico consolidado
- Salvar o diagnóstico consolidado final em `laudo-tecnico-output/diagnostico-consolidado.md`

## Fluxo de execução
1. Verificar graphify (seção acima) antes de qualquer prompt que toque o repositório
2. Levantar inputs faltantes: demanda (se ainda não fornecida), repositório adicional (se aplicável — ver "Entrada"; o repositório principal já é o diretório atual por padrão), e output de prompts anteriores quando um prompt depender deles
3. Ler o arquivo de referência da fase antes de rodar seus prompts:
   - `references/00-setup-graphify.md` — só se o comando `graphify` não for encontrado
   - `references/01-entendimento.md` — demanda (To-Be), gate DoR, gap analysis (As-Is), arquitetura (C4)
   - `references/02-execucao.md` — PRR (dev→hml→prod), RAID (riscos/dependências)
   - `references/03-justificativa.md` — Business Case, TCO
   - `references/04-planejamento.md` — EAP (tarefas ordenadas, síntese das fases anteriores)
4. Ordem de dependência: Fase 1 sempre primeiro; Fases 2 e 3 podem rodar em paralelo depois; Fase 4 requer apenas Fase 1 (obrigatório) e Fase 2 (idealmente) para iniciar — não é necessário aguardar a Fase 3, que só contribui prioridade opcional se já estiver disponível
5. Salvar o output de cada fase em disco (seção "Persistência" acima) conforme é produzido
6. Consolidar no formato abaixo em `laudo-tecnico-output/diagnostico-consolidado.md`
7. **Gate de conclusão — antes de apresentar ao usuário:**
   - Rodar `python scripts/validar_diagnostico.py laudo-tecnico-output/diagnostico-consolidado.md [--fase2] [--fase3]`, marcando as flags das fases opcionais de fato executadas (Fase 1 e Fase 4 são sempre obrigatórias, não têm flag)
   - O script checa presença de seções e, para as tabelas com rótulos fixos por linha (Demanda, As-Is/To-Be/Gap, Arquitetura, Production Readiness, RAID, Business Case, TCO, EAP), se cada linha/item esperado está presente — não cobre instruções de raciocínio dentro de um item (ver "Princípio central" acima)
   - Se o script reprovar (`REPROVADO`), completar os itens listados como `[FALTA]` antes de apresentar o diagnóstico
   - Se Python não estiver disponível para rodar o script, conferir manualmente cada seção e marcador esperado do formato abaixo contra as fases executadas — não pular esta checagem
8. **Entrega — o artefato final desta skill é `laudo-tecnico-output/diagnostico-consolidado.md`:**
   - Após o gate aprovar, informar ao usuário o caminho do arquivo como entregável desta execução — não apenas colar o conteúdo no chat sem apontar para o arquivo persistido
   - O conteúdo do chat e o arquivo em disco devem ser idênticos — o arquivo não é um rascunho paralelo, é a mesma consolidação salva

## Formato do diagnóstico consolidado

```
# Diagnóstico: [nome do projeto/repositório]

## Demanda (To-Be)
[Tabela da Fase 1.1: Item | Resposta extraída | Status — Entregável, Escopo,
Prazos, Critérios de aceite, Responsáveis, Existente vs pendente]

## As-Is — Estado atual do repositório
[Tabela da Fase 1.2: As-Is | To-Be | Gap]

## Arquitetura (C4 — Context/Container)
[Tabela da Fase 1.3: Item | Achado | Evidência (EXTRACTED/INFERRED) —
Context, Container, Fluxo de dados, Configuração, Lógica similar]

## Production Readiness (se Fase 2 executada)
[Tabela da Fase 2.1: Item PRR | Situação atual | Evidência no repositório —
Estágio atual, Promoção, Dependências de infraestrutura, Gates,
Observabilidade]

## RAID — Riscos e Dependências (se Fase 2 executada)
[Fase 2.2, nas 4 categorias: Risks | Assumptions | Issues | Dependencies]

## Business Case (se Fase 3 executada)
[Tabela da Fase 3.1: Item | Resposta | Status — Problema/oportunidade,
Custo de não agir, Métricas de sucesso]

## TCO — Custo (se Fase 3 executada)
[Tabela da Fase 3.2: Item | Valor/Cálculo | Fato ou Estimativa? — Serviços
e cobrança, Volume de dados, Custo de implementação, Custo operacional]

## EAP — Estrutura Analítica de Projeto
[Tabela da Fase 4.1: # EAP | Pacote de trabalho | Origem | Pré-requisitos |
Critério de conclusão | Bloqueado por (RAID)? — sempre presente, a Fase 4
é obrigatória]
```
