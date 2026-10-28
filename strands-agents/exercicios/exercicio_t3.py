from strands import Agent, tool


@tool
def dobro(numero: float) -> float:
    """Calcula o dobro de um número.

    Args:
        numero: o número a dobrar
    """
    return numero * 2


@tool
def raiz_quadrada(numero: float) -> dict:
    """Calcula a raiz quadrada de um número (só aceita zero ou positivo).

    Args:
        numero: o número (zero ou maior)
    """
    if numero < 0:
        return {
            "status": "error",
            "content": [{"text": "O número precisa ser zero ou maior."}],
        }
    return {
        "status": "success",
        "content": [
            {"text": "Cálculo feito."},
            {"json": {"numero": numero, "raiz": numero ** 0.5}},
        ],
    }


agent = Agent(tools=[dobro, raiz_quadrada])

print("--- Parte 1 ---")
print(agent.tool.dobro(numero=4))

print("--- Parte 2 ---")
print(agent.tool.raiz_quadrada(numero=9))

print("--- Parte 3 ---")
r = agent.tool.raiz_quadrada(numero=-1)
print(r["status"])
print(r["content"][0]["text"])
