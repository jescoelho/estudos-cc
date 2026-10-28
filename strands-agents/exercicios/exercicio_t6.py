import os
from strands import Agent
from strands_tools import calculator, current_time, file_read, file_write

# Garante que a confirmação está LIGADA (o padrão seguro)
os.environ.pop("BYPASS_TOOL_CONSENT", None)

agent = Agent(tools=[calculator, current_time, file_read, file_write], callback_handler=None)


def mostrar(titulo, r):
    texto = " ".join(c.get("text", "") for c in r["content"]).replace("\n", " ")
    print(f"{titulo}\n   status = {r['status']}\n   texto  = {texto[:150]}")


print("--- Parte 1: tools que só calculam ---")
mostrar("calculator: 2+2*3", agent.tool.calculator(expression="2+2*3"))
mostrar("current_time: São Paulo", agent.tool.current_time(timezone="America/Sao_Paulo"))
mostrar("calculator: nome que não existe", agent.tool.calculator(expression="preco_petr4"))

print("\n--- Parte 2: gravar (vai pedir confirmação; responda y) ---")
mostrar("file_write", agent.tool.file_write(path="nota_t6.txt", content="linha 1\nlinha 2\n"))

print("\n--- Parte 3: ler de volta ---")
mostrar("file_read", agent.tool.file_read(path="nota_t6.txt", mode="view"))

print("\n--- Parte 4: ler um arquivo de OUTRA pasta ---")
OUTRO_ARQUIVO = r"C:\Windows\win.ini"   # arquivo comum do Windows, só leitura
# (no Linux/Mac, troque por "/etc/hostname")
mostrar("file_read fora da pasta", agent.tool.file_read(path=OUTRO_ARQUIVO, mode="view"))
