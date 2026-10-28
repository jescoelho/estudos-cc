from strands import Agent, tool


@tool
def celsius_para_fahrenheit(celsius: float) -> float:
    """Converte uma temperatura de graus Celsius para Fahrenheit.

    Args:
        celsius: Temperatura em graus Celsius
    """
    return celsius * 9 / 5 + 32


agent = Agent(tools=[celsius_para_fahrenheit])

# Passo 1: o que o agente tem na caixa
print("1:", agent.tool_names)

# Passo 2: chamada direta
r = agent.tool.celsius_para_fahrenheit(celsius=25)
print("2:", r["status"], r["content"])

# Passo 3: histórico, chamada gravada x não gravada
print("3a:", len(agent.messages))
agent.tool.celsius_para_fahrenheit(celsius=0)
print("3b:", len(agent.messages))
agent.tool.celsius_para_fahrenheit(celsius=0, record_direct_tool_call=False)
print("3c:", len(agent.messages))

# Passo 4: erro de propósito, valor sem nome
r = agent.tool.celsius_para_fahrenheit(25)
print("4:", r["status"])


# Passo 5: adicionar outra tool depois
@tool
def dobro(x: int) -> int:
    """Devolve o dobro de um número inteiro.

    Args:
        x: Número inteiro
    """
    return x * 2


agent.tool_registry.process_tools([dobro])
print("5a:", agent.tool_names)
print("5b:", agent.tool.dobro(x=21)["content"])

# Passo 6: erro de propósito, tool que não existe (o programa para aqui)
agent.tool.nao_existe(x=1)
