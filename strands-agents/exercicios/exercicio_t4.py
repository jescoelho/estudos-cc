import time
from strands import Agent, tool
from strands.models.model import Model
from strands.tools.executors import ConcurrentToolExecutor, SequentialToolExecutor

inicio = time.time()


def log(msg):
    print(f"[{time.time() - inicio:.0f}s] {msg}")


@tool
def tool_a() -> str:
    """Tool A: demora 2 segundos."""
    log("A começou")
    time.sleep(2)
    log("A terminou")
    return "A pronta"


@tool
def tool_b() -> str:
    """Tool B: demora 2 segundos."""
    log("B começou")
    time.sleep(2)
    log("B terminou")
    return "B pronta"


class ModeloDeMentira(Model):
    """Finge ser um modelo de IA: pede as tools A e B de uma vez e depois
    responde 'Fim'. Serve só para este teste, sem precisar de conta na AWS."""

    def update_config(self, **k): pass
    def get_config(self): return {}
    async def structured_output(self, *a, **k):
        yield {}

    async def stream(self, messages, tool_specs=None, system_prompt=None, **kw):
        yield {"messageStart": {"role": "assistant"}}
        ja_tem_resultado = any(
            "toolResult" in bloco
            for m in messages if m["role"] == "user"
            for bloco in m["content"] if isinstance(bloco, dict)
        )
        if ja_tem_resultado:
            yield {"contentBlockStart": {"start": {}}}
            yield {"contentBlockDelta": {"delta": {"text": "Fim."}}}
            yield {"contentBlockStop": {}}
            yield {"messageStop": {"stopReason": "end_turn"}}
            return
        for i, nome in enumerate(["tool_a", "tool_b"]):
            yield {"contentBlockStart": {"start": {"toolUse": {"toolUseId": f"id{i}", "name": nome}}}}
            yield {"contentBlockDelta": {"delta": {"toolUse": {"input": "{}"}}}}
            yield {"contentBlockStop": {}}
        yield {"messageStop": {"stopReason": "tool_use"}}


# >>> TROQUE AQUI para comparar: ConcurrentToolExecutor() ou SequentialToolExecutor()
executor = ConcurrentToolExecutor()

agent = Agent(
    model=ModeloDeMentira(),
    tools=[tool_a, tool_b],
    tool_executor=executor,
    callback_handler=None,
)
agent("teste")
log("agente terminou")
