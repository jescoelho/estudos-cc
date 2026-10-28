# Estudo guiado: tools no Strands Agents

Material de estudo em português sobre **tools** (as "ferramentas" que um agente pode usar) no [Strands Agents](https://strandsagents.com). Cada tópico é um documento didático (mínimo primeiro, aprofundamento opcional, exercício guiado com saída esperada, glossário e fontes) e tem um script de exercício nesta pasta.

## Ordem de estudo

| # | Tópico | Documento | Script |
|---|--------|-----------|--------|
| 1 | O que é uma tool e como criar a primeira | [Tópico 1](https://claude.ai/artifact/HWz8fKjsbGTR1AtH76mo8Z) | `exercicios/exercicio_t1.py` (+ `t1_tools_exemplo/`) |
| 2 | Como o modelo "enxerga" a tool (descrição, parâmetros, erros) | [Tópico 2](https://claude.ai/artifact/LxxHcAxidxY4GkWFRw5TYz) | `exercicios/exercicio_t2.py` |
| 3 | Tools assíncronas e contexto da tool | [Tópico 3](https://claude.ai/artifact/TpShr5Jn4uohmSL483KnHo) | `exercicios/exercicio_t3.py` |
| 4 | Execução de várias tools (concorrente x sequencial) | [Tópico 4](https://claude.ai/artifact/5MskwbRXfUMfk8BYeSDPcA) | `exercicios/exercicio_t4.py` |
| 5 | Agentes como tools | [Tópico 5](https://claude.ai/artifact/SpCPqyAnnMwzSpViTFT46G) | `exercicios/exercicio_t5.py` |
| 6 | Tools prontas (o que está e o que não está no escopo de cada uma) | [Tópico 6](https://claude.ai/artifact/JMTU9z9hXY7gLPfbTdH5vv) | `exercicios/exercicio_t6.py` |

Próximos tópicos planejados: tools via MCP, estado nas tools, boas práticas de design de tools.

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
- O tópico 6 grava um arquivo (`nota_t6.txt`) e pede confirmação antes; responda `y`.
- `t1_tools_exemplo/` mostra a pasta `./tools/` carregada automaticamente (`triplo.py` precisa ficar numa pasta chamada `tools`, ao lado de onde você roda o Python).

## Sobre os testes

Os scripts foram testados com `strands-agents` 1.62.0 e `strands-agents-tools` 0.8.10, em Linux. No Windows, o caminho do tópico 6 (`C:\Windows\win.ini`) é o recomendado, mas **não foi rodado no Windows**; algumas tools prontas (`shell`, `cron`) também não funcionam lá. Cada documento marca o que foi `[Oficial]` (vem da documentação), `[Testado]` (rodei) e `[Recomendação]`.
