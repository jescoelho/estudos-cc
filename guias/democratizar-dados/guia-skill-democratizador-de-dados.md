# Guia: criando a skill "democratizador-de-dados" com Claude Code

Este guia assume que você está começando do zero, dentro do ambiente
corporativo (SageMaker), usando o Claude Code como copiloto dentro do
repositório container que já hospeda a skill `nota-tecnica` e a skill
`laudo-tecnico`.

Cada passo tem um prompt pronto para copiar e colar no Claude Code.
Ajuste nomes de pastas/arquivos conforme a convenção real do seu
repositório, se for diferente do que está descrito aqui.

---

## Passo 1 — Abrir o Claude Code no repositório certo

No terminal do SageMaker:

```bash
cd /caminho/para/o/repositorio-container
bash setup.sh
claude
```

Confirme que você está na raiz do repositório container — a skill nova
vai precisar ler a estrutura das skills já existentes ali dentro
(`nota-tecnica`, `laudo-tecnico`).

---

## Passo 2 — Localizar e usar a skill-creator

**Prompt:**

```
Existe uma skill-creator disponível nesse ambiente? Se sim, use-a para
criar a estrutura inicial de uma nova skill chamada
"democratizador-de-dados", seguindo o mesmo padrão de pastas e
metadados usado pelas skills já existentes neste repositório.
```

Se o Claude Code confirmar que a skill-creator existe, ele vai gerar a
pasta e o SKILL.md inicial (ainda vazio de lógica). Se não existir,
peça a ele para criar a estrutura manualmente, espelhando a pasta da
`laudo-tecnico` como modelo de organização de arquivos.

---

## Passo 3 — Descrever as fases do processo, em linguagem natural

**Prompt:**

```
Vou te descrever um processo em fases que quero que a skill
"democratizador-de-dados" implemente. Não escreva código ainda —
primeiro me devolva um rascunho de SKILL.md descrevendo essas fases em
texto, para eu revisar antes de qualquer implementação.

A skill recebe como entrada apenas uma URL de um site público que
expõe dados. As fases são:

1. DISCOVERY: navegação automatizada do site (via Playwright ou
   equivalente), capturando todas as requisições de rede do tipo
   xhr/fetch, e classificando cada endpoint encontrado por padrão
   (ex: JSON estático, API paginada, arquivo zip, precisa de
   autenticação).

2. HIPÓTESES E TESTES: para cada endpoint candidato a fonte de dados,
   formular hipóteses sobre seu comportamento (ex: "isso pode ser uma
   janela deslizante por contagem fixa, não por tempo") e desenhar
   testes empíricos que confirmem ou refutem essas hipóteses antes de
   recomendar qual endpoint usar como fonte de verdade.

3. CHECKPOINT HUMANO: a skill para aqui, apresenta um resumo do que
   foi descoberto e testado, e aguarda minha confirmação explícita
   antes de prosseguir. Ela nunca deve gerar código de pipeline sem
   essa confirmação.

4. RETRIEVAL NO GRAFO: consultar o graphify para recuperar, entre os
   pipelines já existentes em produção neste repositório, qual é o
   mais parecido estruturalmente com a fonte nova (mesmo tipo de
   resposta, mesma estratégia de granularidade intradiária/batch).

5. INSTANCIAÇÃO DO PIPELINE: gerar o novo pipeline dentro deste
   repositório, seguindo a mesma estrutura do pipeline recuperado na
   fase anterior — não inventando uma estrutura nova.

6. GERAÇÃO DE INFRAESTRUTURA: gerar o módulo Terraform correspondente
   (Lambda + regras de EventBridge), seguindo o padrão dos módulos já
   existentes no repositório de infra.

7. ABERTURA DE PR: a skill abre um Pull Request em cada repositório
   afetado (container e infra), mas NUNCA faz merge ou
   `terraform apply` sozinha — isso fica sempre para revisão humana.

Me devolva o rascunho do SKILL.md com essas 7 fases documentadas.
```

---

## Passo 4 — Usar a laudo-tecnico como referência de estilo

**Prompt:**

```
Leia o SKILL.md da skill "laudo-tecnico" neste mesmo repositório e use-a
como referência de estilo e estrutura para a "democratizador-de-dados"
— ela também depende do graphify como pré-requisito e já resolveu
problemas parecidos de organização em fases com checkpoint humano.

Ajuste o rascunho da democratizador-de-dados para seguir convenções
semelhantes (formato de seções, forma de documentar pré-requisitos,
forma de descrever cada fase), mantendo as 7 fases que já definimos.
```

---

## Passo 5 — Marcar o checkpoint humano como parada explícita

**Prompt:**

```
Revise a fase 3 (CHECKPOINT HUMANO) do SKILL.md que você gerou. Quero
que fique explícito, no próprio texto do SKILL.md, que essa fase é um
ponto de parada obrigatório — a skill deve apresentar um resumo
estruturado do que foi descoberto e testado nas fases 1 e 2, e
aguardar minha resposta explícita de confirmação antes de executar
qualquer fase seguinte. Isso não pode ser uma etapa que você executa e
segue adiante automaticamente.

Me mostre como ficou essa seção depois do ajuste.
```

---

## Passo 6 — Mapear as propriedades necessárias no graphify

**Prompt:**

```
Antes de implementar a fase 4 (RETRIEVAL NO GRAFO), inspecione o
schema atual do graphify neste repositório: quais nós e relações já
existem hoje? Ele já captura, para cada pipeline em produção, o tipo
de fonte de dado (API REST paginada, JSON estático, etc.), o formato
do dado bruto (JSON, CSV, zip) e a estratégia de deduplicação usada?

Se essas propriedades não existirem ainda no grafo, não implemente a
fase 4 ainda — em vez disso, me proponha um plano para enriquecer o
grafo com essas propriedades primeiro, listando os pipelines
existentes que precisariam ser retroativamente anotados.
```

> Esse passo pode gerar uma tarefa própria (enriquecer o grafo) antes
> de você conseguir seguir para o passo 7. Trate isso como um
> pré-requisito, não como algo opcional.

---

## Passo 7 — Testar com o caso conhecido (DTCC)

**Prompt:**

```
Rode a skill "democratizador-de-dados" apontando para a URL
https://pddata.dtcc.com/ppd/cftcdashboard e siga o processo completo
até o checkpoint humano. Me apresente o resumo que a skill produziria
nesse ponto.
```

Depois de ver o resumo, compare manualmente com o que já sabemos:

- A skill deveria identificar `Slice.json`, `Ticker.json` e
  `Cumulative.json` como candidatos
- Deveria formular e (idealmente) testar a hipótese de que o
  `Ticker.json` é uma janela deslizante por contagem fixa (100
  registros), não por tempo
- Deveria recomendar `Slice.json` como fonte de verdade para o
  intradiário, com `Cumulative.json` para reconciliação diária

Se a skill chegar a uma conclusão diferente, use o prompt abaixo para
ajustar:

**Prompt (caso o resultado esteja incorreto):**

```
O resultado que você chegou para a fase de hipóteses está incorreto.
[explique aqui o que deveria ter sido testado ou concluído].
Ajuste o SKILL.md para que a fase 2 (HIPÓTESES E TESTES) capture essa
instrução de forma mais explícita, e rode o teste novamente.
```

---

## Passo 8 — Documentar e versionar

**Prompt:**

```
Crie uma feature branch para a skill "democratizador-de-dados", faça
commit de todos os arquivos gerados, e abra um Pull Request em modo
WIP, seguindo o mesmo padrão que usamos nas demandas do
nota-tecnica (eu serei a aprovadora).

Também adicione uma seção ao README deste repositório explicando
quando usar a "democratizador-de-dados" (democratização de uma fonte
de dado externa nova, a partir de uma URL) versus quando usar a
"laudo-tecnico" (diagnóstico de um repositório ou demanda herdada) —
são skills parecidas em estrutura de fases, mas para gatilhos
diferentes.
```

---

## Expansão: comando guarda-chuva com múltiplas sub-skills

Depois que a primeira sub-skill (`democratizador-dados:site-publico`) estiver
validada com o caso da DTCC, o desenho evolui para um comando pai que
classifica a fonte automaticamente e despacha para a sub-skill certa —
em vez de você escolher manualmente qual rodar a cada nova fonte.

### Cenários identificados e sub-skills correspondentes

| Sub-skill | Cenário | Entrada exige credencial? |
|---|---|---|
| `site-publico` | Site com API oculta, descoberta via engenharia reversa de rede | Não, no caso conhecido (DTCC) |
| `api-documentada` | API REST/GraphQL com documentação oficial (Swagger/OpenAPI) | Geralmente sim (API key) |
| `portal-dados-abertos` | Portal estruturado (CKAN, Socrata, dados.gov.br) | Não |
| `relatorio-pdf` | Dados publicados periodicamente em PDF (boletins, atas) | Não |
| `scraping-html` | Site sem API por trás — só HTML renderizado | Não |
| `arquivo-ftp-sftp` | Dados publicados via FTP/SFTP | Sim (usuário/senha ou chave) |
| `feed-tempo-real` | WebSocket / streaming contínuo | Parcial (token de canal, às vezes) |

### Esquema de entrada do comando pai

O comando `democratizador-dados` recebe dois parâmetros — a URL é
sempre obrigatória, a credencial nunca é passada em texto puro, só a
referência de onde buscá-la:

```
url: <string, obrigatório>
secret_ref: <string, opcional>   # nome do secret no Secrets Manager —
                                  # nunca o valor da credencial em si
```

### Lógica de classificação (funil de decisão)

A classificação roda em duas camadas, da verificação mais barata para
a mais cara, seguida de um gate comum de credencial antes do dispatch:

**Camada 1 — verificações estáticas (sem abrir navegador):**
1. Esquema da URL é `ftp://`/`sftp://`? → `arquivo-ftp-sftp`
2. URL aponta pra `.pdf` ou `Content-Type: application/pdf`? → `relatorio-pdf`
3. Existe endpoint conhecido de portal de dados abertos (CKAN, Socrata, DCAT)? → `portal-dados-abertos`
4. Existe endpoint conhecido de documentação de API (`/swagger.json`, `/openapi.json`)? → `api-documentada`

**Camada 2 — discovery via navegador (só roda se a Camada 1 não bateu):**
- Captura de rede encontra conexão WebSocket? → `feed-tempo-real`
- Captura encontra chamadas xhr/fetch retornando JSON? → `site-publico`
- Nenhuma chamada de dados por trás, só HTML? → `scraping-html`

**Gate de credencial (roda depois de qualquer classificação acima):**
- A sub-skill identificada exige `secret_ref`?
  - Não exige, ou exige e foi fornecido → prossegue com o dispatch normalmente
  - Exige e não foi fornecido → a skill **para** e pede a credencial, em vez de tentar prosseguir sem ela

**Prompt:**

```
Quero expandir a skill "democratizador-dados" para funcionar como um
comando guarda-chuva que classifica automaticamente o cenário de uma
fonte de dado nova e despacha para a sub-skill correta, em vez de
executar sempre a mesma lógica.

Crie a estrutura de comando com sub-skills, seguindo o padrão
"democratizador-dados:<sub-skill>", para os seguintes cenários:
site-publico, api-documentada, portal-dados-abertos, relatorio-pdf,
scraping-html, arquivo-ftp-sftp, feed-tempo-real.

O comando pai recebe dois parâmetros: "url" (obrigatório) e
"secret_ref" (opcional — referência de um secret no gerenciador de
credenciais, nunca o valor da credencial em texto puro).

Implemente a lógica de classificação em duas camadas, da verificação
mais barata para a mais cara:

CAMADA 1 (verificações estáticas, sem abrir navegador), nesta ordem:
1. Esquema da URL é ftp:// ou sftp://? -> arquivo-ftp-sftp
2. URL aponta para .pdf ou Content-Type é application/pdf? -> relatorio-pdf
3. Existe endpoint conhecido de portal de dados abertos (padrão CKAN
   como /api/3/action/package_list, Socrata, ou feed DCAT)? ->
   portal-dados-abertos
4. Existe endpoint conhecido de documentação de API (/swagger.json,
   /openapi.json, /docs)? -> api-documentada

CAMADA 2 (discovery via navegador, só roda se a Camada 1 não
encontrou nada), reaproveitando a lógica de captura de rede que já
implementamos na sub-skill site-publico:
- Encontrou conexão WebSocket? -> feed-tempo-real
- Encontrou chamadas xhr/fetch retornando JSON? -> site-publico
- Não encontrou nenhuma chamada de dados por trás, só HTML? ->
  scraping-html

Depois de qualquer classificação acima, antes de despachar para a
sub-skill, rode um gate comum: verifique se a sub-skill identificada
exige credencial (arquivo-ftp-sftp e api-documentada exigem por
padrão; feed-tempo-real pode exigir dependendo da fonte). Se exigir e
"secret_ref" não tiver sido informado, pare a execução e me peça a
credencial explicitamente, em vez de tentar prosseguir sem ela.

Me mostre primeiro como ficaria essa lógica de classificação
documentada no SKILL.md do comando pai, antes de implementar
qualquer sub-skill nova.
```

### Componentes Python vs. instrução em markdown

Nem toda a lógica acima deveria virar só texto no SKILL.md. As partes
determinísticas — a Camada 1 inteira, a captura de rede da Camada 2 e
o gate de credencial — ganham em confiabilidade e custo de token
sendo scripts reutilizáveis, em vez de reescritas via tool calls a
cada execução. O que continua sendo instrução em markdown é só a
parte que exige julgamento: qual hipótese testar na Fase 2 de cada
sub-skill, e como interpretar um resultado ambíguo — a mesma
separação entre dado bruto e interpretação que você já usa no
nota-tecnica.

| Componente | Onde vive | Por quê |
|---|---|---|
| Camada 1 (checks estáticos) | `scripts/classify_scenario.py` | Testes booleanos fixos — mesma resposta sempre |
| Captura de rede (Camada 2) | `scripts/discovery.py` | Procedimento idêntico a cada execução |
| Rotinas de teste de hipótese | `scripts/hypothesis_toolkit.py` | A rotina é fixa; a escolha de qual hipótese testar continua sendo julgamento, documentado no SKILL.md |
| Gate de credencial | `scripts/credential_gate.py` | Lógica booleana trivial |
| Interpretação e geração do pipeline final | SKILL.md + templates | Depende do schema de cada fonte — não é repetível ao pé da letra |

Se nenhum script classificar a fonte com confiança, o processo volta
para investigação manual via ferramentas brutas — essa exceção deve
ficar documentada no SKILL.md, não escondida dentro do script.

**Prompt:**

```
Quero que a skill "democratizador-dados" tenha componentes Python
reutilizáveis para as partes mecânicas e determinísticas do processo,
em vez de reescrever essa lógica via instrução em markdown a cada
execução. Crie uma pasta scripts/ dentro da skill com:

1. classify_scenario.py — implementa a Camada 1 do funil de
   classificação que já documentamos no SKILL.md do comando pai (os
   checks de protocolo, extensão e endpoints conhecidos). Se nenhum
   check bater, retorna explicitamente "não classificado" para a
   Camada 2 assumir.

2. discovery.py — captura requisições de rede via Playwright para uma
   URL dada, reaproveitando a mesma lógica já usada na sub-skill
   site-publico, e retorna um resumo estruturado em JSON, sem
   interpretação — só dado bruto, incluindo se foi detectada conexão
   WebSocket.

3. hypothesis_toolkit.py — funções reutilizáveis de teste empírico
   (ex: comparar contagem/timestamps de duas consultas ao mesmo
   endpoint com intervalo, checar se uma resposta é paginada). A
   escolha de qual hipótese testar continua sendo decisão tomada via
   instrução em markdown no SKILL.md de cada sub-skill, não hardcoded
   no script.

4. credential_gate.py — implementa o gate de credencial já
   documentado: checa se a sub-skill classificada exige secret_ref e
   se ele foi fornecido.

Atualize o SKILL.md do comando pai para descrever QUANDO chamar cada
script e COMO interpretar o resultado, sem duplicar a lógica que já
está descrita dentro dos próprios scripts. Documente também que, se
classify_scenario.py e discovery.py não conseguirem classificar a
fonte com confiança, o processo volta para investigação manual via
ferramentas brutas, em vez de forçar uma classificação incerta.
```

### Ordem de priorização de desenvolvimento

Nem toda sub-skill vale a pena construir na mesma hora — a ordem
abaixo equilibra três critérios: o que já está pronto, o que valida
mais barato se o design está certo, e o que tem mais valor dado o seu
domínio (dados regulatórios e de mercado, contexto brasileiro).

1. **`site-publico`** — já em construção, validado com o caso DTCC.
   Vira o template de referência para as demais.
2. **`api-documentada`** — a mais simples de implementar a seguir.
   Como o contrato já é conhecido de antemão, ela testa se a skill
   sabe **pular** as fases de discovery/hipóteses quando não são
   necessárias, em vez de sempre executá-las em sequência — um teste
   de design mais barato que construir um cenário totalmente novo do
   zero.
3. **`portal-dados-abertos`** — complexidade moderada (o portal já
   expõe metadados formais, não precisa de engenharia reversa), e
   alta frequência esperada no seu domínio — dados.gov.br e portais
   estaduais de transparência são fontes recorrentes em contexto
   regulatório brasileiro.
4. **`relatorio-pdf`** — mais complexa (exige parsing de
   tabela/OCR), mas muito comum em fontes regulatórias brasileiras
   (atas do Copom, boletins Bacen/CVM) — vale o investimento antes
   das duas últimas, que são mais raras no seu contexto.
5. **`scraping-html`** — cenário de "sobra" (quando nada mais se
   aplica); construir depois das anteriores garante que ela só entra
   em jogo quando as fontes mais estruturadas já foram descartadas.
6. **`arquivo-ftp-sftp`** — mais comum em reguladores legados; baixa
   prioridade a menos que já exista uma demanda concreta esperando
   por essa fonte.
7. **`feed-tempo-real`** — arquitetura mais diferente das demais (
   conexão persistente, não request/response), maior mudança
   estrutural no pipeline gerado. Deixar por último minimiza o risco
   de essa complexidade contaminar o design das sub-skills mais
   simples.

---

## Regra de segurança para incluir desde o rascunho inicial

Vale adicionar isso já no Passo 3, ou revisar depois — mas não deixe
para depois de um incidente:

**Prompt:**

```
Adicione ao SKILL.md uma regra explícita: a skill
"democratizador-de-dados" nunca deve executar `terraform apply` nem
fazer merge de Pull Request de forma autônoma, em nenhuma
circunstância. A ação final da skill é sempre abrir o PR e parar.
```
