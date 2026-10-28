import json
from strands import Agent
from strands.models.model import Model


class ModeloDeMentira(Model):
    """Finge ser um modelo de IA, só para este teste (sem conta na AWS).

    - Se receber 'pede', pede essa tool uma vez e depois responde com o texto
      que a tool devolveu.
    - Se não receber 'pede', apenas responde com 'texto'.
    """

    def __init__(self, texto="", pede=None):
        self.texto = texto
        self.pede = pede  # (nome_da_tool, texto_de_entrada)

    def update_config(self, **k): pass
    def get_config(self): return {}
    async def structured_output(self, *a, **k):
        yield {}

    async def stream(self, messages, tool_specs=None, system_prompt=None, **kw):
        yield {"messageStart": {"role": "assistant"}}
        resultados = [
            b["toolResult"]["content"][0]["text"]
            for m in messages if m["role"] == "user"
            for b in m["content"] if isinstance(b, dict) and "toolResult" in b
        ]
        if self.pede and not resultados:
            nome, entrada = self.pede
            yield {"contentBlockStart": {"start": {"toolUse": {"toolUseId": "t1", "name": nome}}}}
            yield {"contentBlockDelta": {"delta": {"toolUse": {"input": json.dumps({"input": entrada})}}}}
            yield {"contentBlockStop": {}}
            yield {"messageStop": {"stopReason": "tool_use"}}
            return
        texto = f"Resposta final: {resultados[0].strip()}" if resultados else self.texto
        yield {"contentBlockStart": {"start": {}}}
        yield {"contentBlockDelta": {"delta": {"text": texto}}}
        yield {"contentBlockStop": {}}
        yield {"messageStop": {"stopReason": "end_turn"}}


# --- Dois especialistas (cada um com cartão de visita: name + description) ---
cambio = Agent(
    model=ModeloDeMentira(texto="Dólar a R$ 5,40 (valor de exemplo)."),
    name="cambio",
    description="Responde perguntas sobre câmbio e cotação de moedas.",
    callback_handler=None,
)
curvas = Agent(
    model=ModeloDeMentira(texto="Curva de juros inclinada para cima (exemplo)."),
    name="curvas",
    description="Responde perguntas sobre curvas de juros.",
    callback_handler=None,
)

# --- Orquestrador: aqui o modelo de mentira "decide" chamar o especialista 'cambio' ---
orquestrador = Agent(
    model=ModeloDeMentira(pede=("cambio", "Quanto está o dólar?")),
    tools=[cambio, curvas],
    callback_handler=None,
)

print("Tools do orquestrador:", orquestrador.tool_names)
resposta = orquestrador("Quanto está o dólar?")
print("Resposta:", str(resposta).strip())

for msg in orquestrador.messages:
    for bloco in msg["content"]:
        if "toolUse" in bloco:
            print("Pedido ao especialista:", bloco["toolUse"]["name"], bloco["toolUse"]["input"])
        if "toolResult" in bloco:
            print("Recibo:", bloco["toolResult"])
