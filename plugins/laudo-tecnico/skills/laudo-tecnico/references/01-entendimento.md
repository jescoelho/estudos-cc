# Fase 1 — Entendimento

Frameworks: Gap Analysis (As-Is/To-Be) para 1.1/1.2, C4 Model para 1.3.
Ordem: 1.1 → 1.2 (depende do output de 1.1). 1.3 é independente, pode rodar em paralelo ou primeiro.

## 1.1 — Extrair a demanda (To-Be)

Insumo: transcrição, e-mail, ticket, ou registro da demanda (texto livre ou arquivo).
- Sem registro escrito: perguntar diretamente — "Você pode colar a transcrição, e-mail ou outro registro da demanda?" — antes de prosseguir. Não tratar relato de memória do usuário como fonte primária; se usado, marcar explicitamente no output que o resumo vem do relato do usuário, não de um documento
- Transcrição é efêmera: não salvar como arquivo no repositório, não commitar, não referenciar por caminho — ver regras em SKILL.md
- Output = o estado To-Be: o que a demanda exige que o repositório entregue

```
Leia [a transcrição/registro] e extraia, de forma objetiva, os seguintes
itens. Organize a resposta em uma tabela com uma linha por item, usando
estes rótulos exatos na coluna "Item" (não parafraseie os rótulos):

[Item | Resposta extraída | Status]
- Entregável — formato, destino, granularidade dos dados
- Escopo — elementos, período, particularidades técnicas (fuso horário,
  frequência de atualização, formato); cite trechos específicos que
  sustentam a resposta
- Prazos — marcos mencionados, mesmo que informais ("seria bom até...")
- Critérios de aceite — validação mencionada
- Responsáveis — pontos de contato para cada parte do processo
- Existente vs pendente — o que foi mencionado como "já existe"/"já está
  pronto" vs. "precisa ser feito"

Status = "especificado" ou "não especificado" — nunca inferido. Se algum
item não estiver claro na fonte, a linha correspondente recebe status "não
especificado", não uma suposição.
```

## Gate de entrada (Definition of Ready) — antes de 1.2

Se mais da metade dos 6 itens da tabela de 1.1 vier "não especificado", a
demanda não está pronta (DoR reprovado): parar e listar ao usuário,
especificamente, quais itens ficaram "não especificado" — nunca um pedido
genérico de "mais detalhes". Exemplo: "Preciso de mais informação sobre:
Prazos, Responsáveis e Critérios de aceite — pode complementar?" Não
seguir para o Gap Analysis com um To-Be majoritariamente vazio — a
incerteza se propaga por todas as fases seguintes.

## 1.2 — Gap Analysis: As-Is x To-Be

Insumo: output de 1.1 (To-Be) + grafo graphify construído (`/graphify .` na raiz).

```
Aqui está o To-Be (tabela do prompt 1.1): [cole o output do prompt 1.1]

Utilize graphify query para localizar, no grafo do repositório (diretório atual, ou o caminho/link informado se for outro), as partes
relevantes a cada item do To-Be (ex: `graphify query "carga histórica"`,
`graphify query "autenticação com API externa"`). Com base no que o grafo retornar,
informe o As-Is (estado atual):

1. Quais partes do fluxo descrito no To-Be já têm código correspondente no
   repositório (As-Is)
2. Quais partes estão ausentes ou incompletas (Gap)
3. Para cada parte já existente: o As-Is atende ao To-Be como está, ou
   precisa de adaptação? Cite o que especificamente precisa mudar.
4. Existem hardcodes, parâmetros fixos ou suposições no código que conflitam
   com o To-Be?

Organize a resposta em uma tabela: [Etapa do pipeline | As-Is (existe no
repositório?) | To-Be (exigido pela demanda) | Gap]
```

## 1.3 — Arquitetura (C4 Model — Context/Container)

Insumo: grafo graphify construído. Independente de 1.1/1.2.
- Nível Context: dependências externas, atores, sistemas de fronteira
- Nível Container: módulos/estágios principais do pipeline e como se conectam
- Não descer a nível Component/Code — fora do escopo deste diagnóstico

```
Com base no grafo graphify do repositório (diretório atual, ou o caminho/link informado se for outro) — consulte com
`graphify query`, `graphify explain` e `graphify path` em vez de ler arquivos
brutos — realize um mapeamento nos níveis Context e Container do C4 Model,
sem entrar em nível Component/Code. Organize a resposta em uma tabela com
uma linha por item, usando estes rótulos exatos na coluna "Item":

[Item | Achado | Evidência (EXTRACTED/INFERRED)]
- Context — dependências externas (APIs, bancos, serviços de nuvem) e
  atores envolvidos; use `graphify query "dependências externas"` ou
  equivalente
- Container — "god nodes" (mais conectados) do grafo, que indicam os
  módulos centrais/pontos de entrada do pipeline
- Fluxo de dados — origem, transformações entre containers (arestas
  `calls`/`imports`), destino final
- Configuração — arquivos de config, variáveis de ambiente, parâmetros
  prováveis de serem tocados
- Lógica similar — lógica já implementada (ex: carga incremental) que se
  conecta ao padrão do To-Be; use `graphify path` para checar a conexão

Evidência: `EXTRACTED` (explícita no código) ou `INFERRED` (resolvida pelo
graphify) — nunca apresente inferência como fato sem marcá-la.

Se um item genuinamente não existir no repositório (ex: repositório sem
nenhuma dependência externa relevante para "Context"), a linha recebe
"não identificado no repositório" na coluna Achado, e "N/A" na coluna
Evidência — nunca preencha com um achado plausível apenas para não deixar
a linha vazia.

Foque no que é específico deste repositório — não explique bibliotecas ou
conceitos gerais de infraestrutura.
```

## Critério de qualidade

- Alguém sem contexto prévio entende, em poucos parágrafos: o To-Be, o As-Is, e onde o Container principal começa
- Tabelas de 1.1, 1.2 e 1.3 têm todas as linhas de item preenchidas — linha ausente = item não respondido, não item "implicitamente coberto"
- Gap não identificado com clareza ("o que falta fazer, concretamente?") = Fase 1 incompleta; aprofundar 1.2 antes de avançar
