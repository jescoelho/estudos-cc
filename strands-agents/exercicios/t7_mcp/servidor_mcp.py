try:  # mcp 2.x (instalação nova)
    from mcp.server.mcpserver import MCPServer
    from mcp.server.mcpserver.exceptions import ToolError
except ImportError:  # mcp 1.x
    from mcp.server import FastMCP as MCPServer
    from mcp.server.fastmcp.exceptions import ToolError

servidor = MCPServer("Servidor de Exemplo", log_level="CRITICAL")


@servidor.tool(description="Soma dois números inteiros.")
def somar(a: int, b: int) -> int:
    return a + b


@servidor.tool(description="Divide a por b. Falha se b for zero.")
def dividir(a: float, b: float) -> float:
    if b == 0:
        raise ValueError("o denominador não pode ser zero")
    return a / b


@servidor.tool(description="Divide a por b, com mensagem de erro clara se b for zero.")
def dividir_claro(a: float, b: float) -> float:
    if b == 0:
        raise ToolError("o denominador não pode ser zero")
    return a / b


@servidor.tool(description="Devolve uma saudação em português.")
def saudar(nome: str) -> str:
    return f"Olá, {nome}!"


if __name__ == "__main__":
    servidor.run(transport="stdio")
