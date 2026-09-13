# tests/fixtures/

Modelos sintéticos usados para testar a skill durante o desenvolvimento.
Nenhum arquivo aqui contém dados reais de mercado ou de clientes.

## Fixtures disponíveis

> Atualize esta seção sempre que adicionar uma nova fixture.

| Arquivo | O que representa | Cobre |
|---|---|---|
| `modelo_simples.xlsx` | Modelo Excel com uma aba de inputs e uma de cálculo | Extração básica de Excel |
| `modelo_simples.py` | Script Python equivalente ao modelo_simples.xlsx | Extração básica de Python |

## Como usar uma fixture para testar

Peça ao Claude Code:

> "Testa a skill com `tests/fixtures/modelo_simples.xlsx` e salva o resultado
> em `tests/outputs/`"

O resultado gerado vai para `tests/outputs/` — essa pasta não é versionada,
então os arquivos gerados não entram no repositório.

## Como criar uma nova fixture

Uma boa fixture é **mínima** — cobre exatamente o caso que você quer testar,
sem complexidade desnecessária. Ao criar:

1. Use valores numéricos arbitrários (ex: retornos de 0.01, 0.02, -0.01)
2. Nomeie o arquivo descrevendo o que ele testa: `modelo_vba_macros_aninhadas.xlsm`
3. Adicione uma linha na tabela acima descrevendo a fixture
4. Commite a fixture junto com a alteração na skill que ela passou a testar
