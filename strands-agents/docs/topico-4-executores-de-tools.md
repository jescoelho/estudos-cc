# Strands Agents — Tópico 4: executores de tools

Oct 28, 2026 · @Jéssica Coelho

## Resumo e como ler

Um **executor** decide como o Strands roda as tools quando o modelo pede mais de uma ao mesmo tempo: todas juntas (concorrente, o padrão) ou uma de cada vez, na ordem (sequencial). Você escolhe ao criar o agente: `Agent(tool_executor=SequentialToolExecutor())`. Se não escolher nada, vale o concorrente.

**Como ler:** as seções até "Quando uma tool dá erro" são o mínimo. "Para ir mais fundo" é opcional. Marcações: **\[Oficial\]** está na documentação do Strands; **\[Testado\]** rodei na versão 1.62.0; **\[Recomendação\]** é opinião minha.

## A ideia central: caixas de supermercado

Imagine duas compras na fila de um supermercado: uma pessoa precisa passar o leite e o pão.

- **Concorrente** = dois caixas abertos. O leite e o pão são passados ao mesmo tempo. Termina mais rápido, mas os dois caixas não sabem o que o outro está fazendo.
- **Sequencial** = um caixa só. Passa o leite, depois o pão. Mais lento, mas cada passo só começa quando o anterior acabou.

Para itens independentes (leite e pão), dois caixas ganham tempo. Para passos que dependem um do outro (tirar uma foto e só depois enviar a foto por e-mail), tem que ser um de cada vez.

O ponto fácil de esquecer: **quem pede as tools é o modelo de IA**, não o executor. O executor só decide como rodar o que o modelo pediu.

## O mínimo antes de começar

Nos tópicos 1 e 2 você viu duas formas de usar uma tool:

- **Chamar direto** (`agent.tool.nome(...)`): você manda rodar uma tool específica, uma vez.
- **Linguagem natural** (`agent("...")`): você escreve uma frase e o modelo de IA decide quais tools usar.

Executor só importa no segundo caso, porque é quando o modelo pode pedir várias tools numa mesma resposta. Quando você chama uma tool sozinha, não há fila para organizar.

Também vale lembrar: o executor é uma configuração de quem **monta o agente** (o código do programa), e vale para todas as tools daquele agente. Quem usa o programa não escolhe.

## Os dois executores

**\[Oficial\]** A página [Tool Executors](https://strandsagents.com/docs/user-guide/concepts/tools/executors/) descreve dois executores embutidos:

| Executor | O que faz | Quando é usado |
| --- | --- | --- |
| `ConcurrentToolExecutor` | roda as tools pedidas ao mesmo tempo | é o padrão; não precisa escrever nada |
| `SequentialToolExecutor` | roda uma tool de cada vez, na ordem em que foram pedidas | só se você pedir, com `tool_executor=` |

Como configurar (exemplo da documentação, onde `screenshot_tool` e `email_tool` são tools de exemplo):

```python
from strands import Agent
from strands.tools.executors import SequentialToolExecutor

agent = Agent(
    tool_executor=SequentialToolExecutor(),
    tools=[screenshot_tool, email_tool],
)
```

**\[Testado\]** Sem passar `tool_executor`, `type(agent.tool_executor).__name__` mostra `ConcurrentToolExecutor`; passando o sequencial, mostra `SequentialToolExecutor`.

**Um detalhe importante** **\[Oficial\]**: a concorrência depende do modelo. Ela só acontece se o modelo pedir várias tools **na mesma resposta**. Se pedir uma por vez, roda uma por vez, mesmo com o executor concorrente.

## Como escolher

Faça uma pergunta: **uma tool precisa do resultado da outra, ou mexe no mesmo lugar que a outra?** Se sim, sequencial. Se não, deixe o padrão.

**\[Testado\]** Montei um modelo de mentira que pede duas tools de uma vez, cada uma demorando 2 segundos:

| Executor | A começou | B começou | Tempo total |
| --- | --- | --- | --- |
| Concorrente | 0 s | 0 s | 2 s |
| Sequencial | 0 s | 2 s | 4 s |

| Situação | Executor |
| --- | --- |
| consultar o clima e a hora de uma cidade (independentes) | concorrente |
| tirar uma foto e depois enviar a foto por e-mail (a segunda precisa da primeira) **\[Oficial\]** | sequencial |
| duas tools que gravam no mesmo arquivo ou na mesma tabela **\[Recomendação\]** | sequencial, para evitar que uma sobrescreva a outra |
| tools que consultam bases diferentes e só leem **\[Recomendação\]** | concorrente |

**\[Recomendação\]** Na dúvida, comece sequencial: é mais lento, mas previsível e mais fácil de entender quando algo dá errado. Troque para concorrente quando a lentidão incomodar e as tools forem independentes. Na documentação o padrão é o concorrente; essa dica de começar pelo sequencial é minha.

## Quando uma tool dá erro no meio de várias

A documentação de executores **não fala sobre erros**, então testei. **\[Testado\]** O modelo de mentira pediu duas tools: `quebra` (que dá erro de propósito) e `lenta_a` (que funciona).

| Executor | O que aconteceu |
| --- | --- |
| Concorrente | `quebra` virou `status: error` com o texto `Error: falhei de propósito`; `lenta_a` rodou normalmente e deu `success` |
| Sequencial | o mesmo resultado: `quebra` deu `error`, e **`lenta_a` ainda rodou** e deu `success` |

Ou seja: nos dois casos o erro de uma tool **não cancela as outras**, e o programa não para. Cada tool ganha o seu próprio recibo (o `status` e o `content` do tópico 3), e o modelo recebe todos juntos.

Isso importa na hora de escolher o sequencial: ele garante a **ordem**, mas não interrompe o resto quando um passo falha. Se a tool B só faz sentido depois que A deu certo, a tool B precisa verificar isso sozinha, ou você precisa contar com o modelo para perceber o erro de A e pedir B de novo mais tarde. Esse segundo cenário depende do comportamento do modelo e eu não o testei.

## Para ir mais fundo (opcional)

Pode pular esta seção e voltar quando precisar.

**1. Executor personalizado ainda não existe.** **\[Oficial\]** A página diz que não é suportado e que está previsto para uma versão futura, acompanhado na issue #762 do GitHub. Hoje só dá para escolher entre os dois embutidos.

**2. O resultado chega ao modelo na ordem do pedido.** **\[Testado\]** Nos meus testes, os recibos apareceram no histórico na mesma ordem em que o modelo pediu as tools (`id0`, `id1`), inclusive no concorrente, em que as duas terminaram juntas.

**3. Forçar o modelo a pedir várias de uma vez (ou não).** **\[Oficial\]** Alguns provedores de modelo têm uma configuração para permitir ou impedir uso paralelo de tools; a página cita a da Anthropic. Eu não testei com um modelo real.

**4. Tools lentas pedem atenção ao concorrente.** **\[Recomendação\]** Se duas tools usam o mesmo recurso limitado (um limite de requisições por minuto de uma API, uma conexão de banco de dados), rodar juntas pode estourar o limite. A documentação não trata disso.

**5. Executor e orquestrador.** **\[Oficial\]** O executor é configurado em cada `Agent`. Se um orquestrador usa outros agentes como tools (tema do tópico 1), cada agente tem o seu próprio executor. **\[Testado\]** Cada `Agent` guarda o seu em `agent.tool_executor`; não testei um orquestrador completo.

**6. Chamada direta não usa fila.** **\[Recomendação, não testado\]** Quando você chama `agent.tool.nome(...)`, você já está pedindo uma tool só; não há nada para ordenar. Por isso o exercício abaixo usa um modelo de mentira, que pede as duas tools de uma vez.

## Exercício guiado

Objetivo: ver com seus olhos a diferença entre os dois executores, medindo o tempo. Você não precisa de conta na AWS: o código traz um "modelo de mentira" que pede as duas tools de uma vez, como um modelo de IA de verdade faria.

**Passo 1.** Na pasta `C:\Users\jecoe\strands`, crie `exercicio_t4.py`:

```python
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
```

**Passo 2.** Rode `python exercicio_t4.py`.

**Resultado esperado com o concorrente** **\[Testado\]**:

```text
[0s] A começou
[0s] B começou
[2s] A terminou
[2s] B terminou
[2s] agente terminou
```

**Passo 3.** Troque a linha `executor = ConcurrentToolExecutor()` por `executor = SequentialToolExecutor()` e rode de novo.

**Resultado esperado com o sequencial** **\[Testado\]**:

```text
[0s] A começou
[2s] A terminou
[2s] B começou
[4s] B terminou
[4s] agente terminou
```

**O que observar:** no concorrente, A e B começam no mesmo segundo e tudo termina em 2 s. No sequencial, B só começa depois que A termina, e tudo leva 4 s.

**Desafio:** adicione uma terceira tool que dê erro (`raise ValueError("falhei")`), inclua o nome dela na lista `["tool_a", "tool_b"]` do modelo de mentira e rode com os dois executores. As outras tools ainda rodam? Dica: releia "Quando uma tool dá erro".

## Glossário

| Termo | Em palavras simples |
| --- | --- |
| Executor (`tool_executor`) | a regra que o Strands usa para rodar as tools que o modelo pediu: juntas ou em fila |
| `ConcurrentToolExecutor` | executor concorrente (padrão): roda as tools pedidas ao mesmo tempo |
| `SequentialToolExecutor` | executor sequencial: roda uma de cada vez, na ordem do pedido |
| Concorrência | várias coisas andando ao mesmo tempo, como dois caixas de supermercado abertos |
| Sequencial | uma coisa por vez, na ordem |
| Modelo de IA | o "cérebro" que lê sua frase e decide quais tools pedir |
| Modelo de mentira | um código que finge ser o modelo, usado só para testar sem conta na AWS |
| Orquestrador | agente que coordena outros agentes, usando-os como tools |
| Issue (GitHub) | um pedido ou aviso aberto na página de um projeto; a #762 é o pedido de executores personalizados |

## Fontes e o que não foi verificado

**Páginas que abri e li:**

- [Tool Executors](https://strandsagents.com/docs/user-guide/concepts/tools/executors/): os dois executores, quando usar cada um, dependência do modelo para a concorrência, executor personalizado não suportado (issue #762).
- [strands.tools.executors.concurrent (referência da API)](https://strandsagents.com/docs/api/python/strands.tools.executors.concurrent/): só confirma que a classe existe; não traz detalhes de funcionamento.

**Testado por mim** em strands-agents 1.62.0, com um modelo de mentira que pede duas tools numa resposta: tempos (2 s concorrente, 4 s sequencial), ordem dos recibos, e comportamento de erro nos dois executores.

**Não verificado:**

- Comportamento com um modelo real (Bedrock, Anthropic etc.): se ele de fato pede várias tools de uma vez e como reage a `status: error`.
- A configuração de uso paralelo de tools de provedores (citada pela documentação, não testada).
- Como o concorrente é implementado por dentro (a página da API não diz); só observei o resultado.
- Orquestrador completo com agentes como tools.
- As dicas marcadas **\[Recomendação\]** são minhas, não da documentação.
- Executores em TypeScript: a página não trouxe exemplos que eu pudesse ler.
