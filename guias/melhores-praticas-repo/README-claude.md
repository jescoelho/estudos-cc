# .claude/

Código-fonte da skill de documentação técnica. O Claude Code lê estes arquivos
ao executar a skill — qualquer alteração aqui afeta diretamente o comportamento
em produção.

## O que cada arquivo faz

> Atualize esta seção sempre que adicionar, remover ou renomear um arquivo.

| Arquivo | Responsabilidade |
|---|---|
| `SKILL.md` | Ponto de entrada — define o pipeline e a ordem de execução |
| _(demais arquivos da skill)_ | _(descreva aqui conforme a estrutura real)_ |

## Como a skill é executada

A skill recebe um modelo de entrada (Excel, Python, VBA ou combinação), executa
as fases em sequência definida no `SKILL.md` e produz a documentação técnica
seguindo o template institucional.

## Antes de alterar qualquer arquivo aqui

1. Confirme em qual branch pessoal você está trabalhando
2. Leia o arquivo que vai alterar por completo antes de editar
3. Teste a alteração com uma fixture em `tests/fixtures/` antes de commitar
4. Nunca altere mais de um módulo por commit
