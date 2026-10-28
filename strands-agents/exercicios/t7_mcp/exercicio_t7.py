import re
import sys

from mcp import StdioServerParameters, stdio_client
from strands import Agent
from strands.tools.mcp import MCPClient


def novo_cliente(**opcoes):
    """Cria um cliente que liga o servidor_mcp.py como um programa à parte."""
    return MCPClient(
        lambda: stdio_client(
            StdioServerParameters(command=sys.executable, args=["servidor_mcp.py"])
        ),
        **opcoes,
    )


# Passo 1: conectar e listar o que o servidor oferece
cliente = novo_cliente()
with cliente:
    tools = cliente.list_tools_sync()
    print("1:", [t.tool_name for t in tools])

    # Passo 2: a ficha de uma tool (escrita no servidor, lida aqui)
    ficha = tools[0].tool_spec
    print("2:", ficha["name"], "|", ficha["description"])

    # Passo 3: chamar uma tool, sem agente e sem modelo
    r = cliente.call_tool_sync(tool_use_id="p3", name="somar", arguments={"a": 2, "b": 3})
    print("3:", r["status"], r["content"])

    # Passo 4: erro comum x erro com mensagem clara
    r = cliente.call_tool_sync(tool_use_id="p4a", name="dividir", arguments={"a": 1, "b": 0})
    print("4a:", r["status"], r["content"])
    r = cliente.call_tool_sync(tool_use_id="p4b", name="dividir_claro", arguments={"a": 1, "b": 0})
    print("4b:", r["status"], r["content"])

    # Passo 5: dar as tools a um agente e chamar pelo agente
    agente = Agent(tools=tools)
    print("5a:", agente.tool_names)
    print("5b:", agente.tool.saudar(nome="Jé")["content"])

# Passo 6: prefixo e filtro
cliente2 = novo_cliente(
    prefix="ex",
    tool_filters={"allowed": [re.compile(r"^(somar|dividir)")], "rejected": ["dividir"]},
)
with cliente2:
    print("6:", [t.tool_name for t in cliente2.list_tools_sync()])

# Passo 7: erro de propósito, usar o cliente fora do bloco "with"
cliente3 = novo_cliente()
cliente3.list_tools_sync()
