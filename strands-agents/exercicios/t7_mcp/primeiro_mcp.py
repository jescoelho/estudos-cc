import sys

from mcp import StdioServerParameters, stdio_client
from strands import Agent
from strands.tools.mcp import MCPClient

cliente = MCPClient(
    lambda: stdio_client(
        StdioServerParameters(command=sys.executable, args=["servidor_mcp.py"])
    )
)

with cliente:
    tools = cliente.list_tools_sync()
    agente = Agent(tools=tools)
    print(agente.tool_names)
    print(agente.tool.somar(a=2, b=3)["content"])
