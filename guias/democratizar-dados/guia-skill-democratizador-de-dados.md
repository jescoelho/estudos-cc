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
