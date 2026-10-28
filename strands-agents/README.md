# Estudo guiado: tools no Strands Agents

Material de estudo em português sobre **tools** (as "ferramentas" que um agente pode usar) no [Strands Agents](https://strandsagents.com). Cada tópico é um documento didático em markdown (pasta `docs/`) (mínimo primeiro, aprofundamento opcional, exercício guiado com saída esperada, glossário e fontes) e tem um script de exercício nesta pasta.

## Ordem de estudo

| # | Tópico | Documento (markdown) | Script |
|---|--------|----------------------|--------|
| 1 | Anexar e invocar tools | [docs/topico-1-anexar-e-invocar-tools.md](docs/topico-1-anexar-e-invocar-tools.md) | `exercicios/exercicio_t1.py` (+ `t1_tools_exemplo/`) |
| 2 | Criar tools customizadas | [docs/topico-2-criar-tools-customizadas.md](docs/topico-2-criar-tools-customizadas.md) | `exercicios/exercicio_t2.py` |
| 3 | Formato do resultado de uma tool | [docs/topico-3-formato-do-resultado-de-uma-tool.md](docs/topico-3-formato-do-resultado-de-uma-tool.md) | `exercicios/exercicio_t3.py` |
| 4 | Executores de tools | [docs/topico-4-executores-de-tools.md](docs/topico-4-executores-de-tools.md) | `exercicios/exercicio_t4.py` |
| 5 | Agentes como tools | [docs/topico-5-agentes-como-tools.md](docs/topico-5-agentes-como-tools.md) | `exercicios/exercicio_t5.py` |
| 6 | Tools prontas | [docs/topico-6-tools-prontas.md](docs/topico-6-tools-prontas.md) | `exercicios/exercicio_t6.py` |
| 7 | Tools via MCP | [docs/topico-7-tools-via-mcp.md](docs/topico-7-tools-via-mcp.md) | `exercicios/t7_mcp/` (`servidor_mcp.py`, `primeiro_mcp.py`, `exercicio_t7.py`) |

Próximos tópicos planejados: estado nas tools, boas práticas de design de tools.

## Como rodar

Python 3.10 ou mais novo. Crie um ambiente isolado e instale:

```
python -m venv venv
venv\Scripts\activate          # Windows (Linux/Mac: source venv/bin/activate)
pip install strands-agents
pip install strands-agents-tools   # só necessário para o tópico 6
```

Depois, dentro de `exercicios/`:

```
python exercicio_t1.py
```

- Os exercícios 1 a 5 **não precisam de credenciais da AWS nem de internet**: os tópicos 4 e 5 usam um "modelo de mentira" (um modelo falso que só devolve pedidos de tools prontos) para testar a orquestração.
- Alguns scripts terminam de propósito com um erro (por exemplo, chamar uma tool que não existe). Isso está explicado em cada documento.
- No tópico 7, os três arquivos de `t7_mcp/` ficam na mesma pasta e o exercício roda de dentro dela. Testado com `mcp` 2.1.1 e 1.30.0.
- O tópico 6 grava um arquivo (`nota_t6.txt`) e pede confirmação antes; responda `y`.
- `t1_tools_exemplo/` mostra a pasta `./tools/` carregada automaticamente (`triplo.py` precisa ficar numa pasta chamada `tools`, ao lado de onde você roda o Python).

## Sobre os testes

Os scripts foram testados com `strands-agents` 1.62.0 e `strands-agents-tools` 0.8.10, em Linux. No Windows, o caminho do tópico 6 (`C:\Windows\win.ini`) é o recomendado, mas **não foi rodado no Windows**; algumas tools prontas (`shell`, `cron`) também não funcionam lá. Cada documento marca o que foi `[Oficial]` (vem da documentação), `[Testado]` (rodei) e `[Recomendação]`.
