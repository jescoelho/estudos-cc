from strands import Agent, tool


@tool
def celsius_para_fahrenheit(celsius: float) -> float:
    """Converte uma temperatura de graus Celsius para Fahrenheit.

    Use quando o usuário pedir conversão de temperatura.

    Args:
        celsius: Temperatura em graus Celsius
    """
    return celsius * 9 / 5 + 32


@tool
def dividir(a: float, b: float) -> dict:
    """Divide a por b.

    Args:
        a: Numerador
        b: Denominador (não pode ser zero)
    """
    if b == 0:
        return {"status": "error", "content": [{"text": "Erro: o denominador não pode ser zero"}]}
    return {"status": "success", "content": [{"text": str(a / b)}]}


agent = Agent(tools=[celsius_para_fahrenheit, dividir])

# Passo 1: quais tools o agente tem
print("1:", agent.tool_names)

# Passo 2: a ficha que o modelo lê
ficha = agent.tool_registry.get_all_tools_config()["celsius_para_fahrenheit"]
print("2a:", ficha["description"])
print("2b:", ficha["inputSchema"]["json"]["properties"]["celsius"]["description"])

# Passo 3: chamada direta
r = agent.tool.celsius_para_fahrenheit(celsius=25)
print("3:", r["status"], r["content"])

# Passo 4: erro, valor sem nome
r = agent.tool.celsius_para_fahrenheit(25)
print("4:", r["status"])

# Passo 5: tool que avisa o próprio erro
r = agent.tool.dividir(a=10, b=4)
print("5a:", r["status"], r["content"])
r = agent.tool.dividir(a=10, b=0)
print("5b:", r["status"], r["content"])

# Passo 6: nome que não existe (o programa para aqui)
agent.tool.nao_existe(x=1)
