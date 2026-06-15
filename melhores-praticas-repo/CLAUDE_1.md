# CLAUDE.md — Skill: Documentação Técnica de Modelos

@../repo-equipe/CLAUDE.md

---

## Leitura obrigatória antes de qualquer tarefa

Leia na ordem antes de iniciar qualquer trabalho:

1. `docs/contexto.md` — contexto da área e do workflow de modelagem
2. `docs/planejamento.md` — demandas de expansão e estado do projeto

Se algum arquivo não for encontrado, interromper e alertar antes de prosseguir.

---

## Higiene do repositório

### Ao iniciar a sessão

1. Nomear a sessão com a branch ativa: `claude -n <branch-ativa>`
2. Verificar branch ativa — se for `main` ou `develop`, interromper e alertar
3. Verificar se a branch está atualizada em relação à origem — se não, alertar
4. Se branch pessoal sem PR aberto, abrir PR com prefixo `WIP:` antes de prosseguir

### Ao iniciar merge ou atualização de branch

Commitar o estado atual antes de qualquer merge — cria ponto de retorno explícito.

### Durante a tarefa

Fazer push ao final de cada etapa significativa — não só ao final da tarefa completa.

### Ao final de qualquer tarefa

1. Commitar e fazer push com mensagem no padrão abaixo
2. Confirmar que saídas de teste estão em `tests/outputs/`
3. Confirmar que nenhum modelo real foi adicionado
4. Se a tarefa concluiu uma demanda, atualizar status em `docs/planejamento.md`
5. Verificar se `.claude/README.md` e `tests/fixtures/README.md` precisam atualização

### Verificação de saúde — ao receber "verifica o repositório"

Via MCP GitHub, checar e listar:

1. Branches abertas há mais de 7 dias sem commit recente
2. Branches pessoais sem PR aberto
3. Divergências entre arquivos em `.claude/` e o README dessa pasta
4. Demandas concluídas em `docs/planejamento.md` com branches ainda abertas

---

## Como trabalhar neste repositório

**Ao receber uma demanda:**

1. Ler `docs/planejamento.md` para localizar a demanda
2. Inspecionar arquivos relevantes em `.claude/` antes de propor alteração
3. Propor e aguardar aprovação antes de implementar
4. Nunca modificar mais de um módulo por vez sem confirmação explícita

**Ao testar:**

1. Usar apenas `tests/fixtures/` — nunca modelos reais
2. Salvar saídas em `tests/outputs/`
3. Comportamento inesperado → registrar em `docs/planejamento.md` antes de corrigir

**Ao encontrar ambiguidade:**

Consultar `docs/contexto.md`. Se persistir, escalar ao usuário — nunca inferir.

---

## Padrão de commits

| Prefixo | Quando usar |
|---|---|
| `feat:` | nova funcionalidade na skill |
| `fix:` | correção de comportamento |
| `docs:` | só documentação |
| `test:` | fixtures ou casos de teste |
| `refactor:` | reestruturação sem mudar comportamento |
