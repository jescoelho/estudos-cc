# Strands Agents — Tópico 5: agentes como tools

Oct 28, 2026 · @Jéssica Coelho

## Resumo e como ler

No Strands, você pode colocar um **agente dentro da lista de tools de outro agente**. O agente de fora (o **orquestrador**) decide quando chamar o agente de dentro (o **especialista**), do mesmo jeito que decide chamar uma tool comum. Na forma mais simples é uma linha: `Agent(tools=[especialista])`.

**Como ler:** as seções até "O que volta e quando o especialista erra" são o mínimo. "Para ir mais fundo" é opcional. Marcações: **\[Oficial\]** está na documentação do Strands; **\[Testado\]** rodei na versão 1.62.0; **\[Recomendação\]** é opinião minha.

## A ideia central: gerente e especialistas

Pense numa empresa pequena. Você fala com **uma gerente**. Ela não sabe de tudo, mas sabe quem sabe: o especialista em câmbio, a especialista em curvas, o especialista em títulos. Você faz a pergunta, ela escolhe a pessoa certa, repassa o pedido, recebe a resposta e te devolve.

| Na empresa | No Strands |
| --- | --- |
| gerente | agente orquestrador |
| especialistas | agentes usados como tools |
| cartão de visita de cada especialista ("quem sou e do que cuido") | nome e descrição do agente |
| o pedido que a gerente repassa | o texto de entrada (`input`) da tool |
| a resposta que o especialista devolve | o recibo da tool (`content`, tópico 3) |

Por que fazer assim? Cada especialista tem suas próprias instruções e suas próprias tools, e o orquestrador não precisa carregar todas as tools de todo mundo. **\[Oficial\]** A documentação lista como benefícios: separação de responsabilidades, modularidade (adicionar ou tirar especialistas sem mexer nos outros) e instruções sob medida para cada tarefa.

## O mínimo antes de começar

Três ideias já vistas servem de base aqui:

- **Um agente** é o conjunto: um modelo de IA, instruções (o `system_prompt`) e uma lista de tools. Você chama com `agent("pergunta")`.
- **Uma tool** tem nome, descrição e parâmetros. O modelo lê o nome e a descrição para decidir se deve chamá-la (tópico 2).
- **O resultado da tool** volta como um recibo com `status` e `content` (tópico 3).

Usar um agente como tool junta essas três: o agente-especialista é embrulhado numa tool, o orquestrador lê o nome e a descrição dessa tool, e a resposta do especialista volta como o recibo.

Um lembrete que vale também aqui: para ver o orquestrador de fato escolher e chamar um especialista, precisa de um modelo de IA de verdade (por padrão, o Amazon Bedrock, com credenciais da AWS). Nos testes deste documento usei um "modelo de mentira" que chama a tool que eu determinei, só para mostrar o que o Strands faz em volta.

## Como transformar um agente em tool

**\[Oficial\]** A página [Agents as Tools](https://strandsagents.com/docs/user-guide/concepts/multi-agent/agents-as-tools/) mostra três formas, da mais simples à que dá mais controle.

**Forma 1: colocar o agente direto na lista de tools.**

```python
clima = Agent(name="clima", description="Responde perguntas sobre clima.")
orquestrador = Agent(tools=[clima])
```

**\[Testado\]** O Strands transforma o `clima` numa tool chamada `clima`, com a descrição `Responde perguntas sobre clima.` e um único parâmetro de entrada, `input` (texto), descrito como "The input to send to the agent tool."

**Forma 2: `.as_tool()`, quando você quer escolher nome, descrição e memória.**

```python
orquestrador = Agent(tools=[
    clima.as_tool(name="clima", description="Responde perguntas sobre clima.")
])
```

**Forma 3: embrulhar com `@tool`, quando você quer controle total** (por exemplo, criar o agente dentro da função e tratar erros). Exemplo no estilo da documentação:

```python
@tool
def clima_w(pergunta: str) -> str:
    """Responde perguntas sobre clima.

    Args:
        pergunta: a pergunta sobre o clima
    """
    especialista = Agent(system_prompt="Responda apenas sobre clima.")
    return str(especialista(pergunta))
```

**\[Testado\]** As três formas funcionaram: o orquestrador chamou o especialista, e a resposta dele voltou como recibo `status: 'success'` com o texto no `content`.

| Forma | Quando usar |
| --- | --- |
| 1. agente direto | o caso mais simples; nome e descrição vêm do próprio agente |
| 2. `.as_tool()` | quando precisa mudar nome ou descrição, ou lembrar conversas anteriores |
| 3. `@tool` | quando precisa de código em volta (validar a entrada, tratar erro, criar o agente na hora) **\[Recomendação\]** |

## Como o orquestrador escolhe qual especialista chamar

O orquestrador só enxerga o **cartão de visita** de cada especialista: nome e descrição. **\[Oficial\]** A documentação recomenda nomes e descrições que "explain the agent's expertise" e dar ao orquestrador critérios claros de quando usar cada um (no `system_prompt` dele). O texto não afirma que só a descrição decide; na prática, a descrição e o prompt do orquestrador são o que orienta a escolha.

**\[Testado\]** O que acontece se você não der cartão de visita ao agente:

| Agente criado como | Nome da tool | Descrição da tool |
| --- | --- | --- |
| `Agent(name="clima", description="Responde perguntas sobre clima.")` | `clima` | `Responde perguntas sobre clima.` |
| `Agent()` (sem nome nem descrição) | `Strands Agents` | `Use the Strands Agents agent as a tool by providing a natural language input` |

Sem erro e sem aviso: o agente vira uma tool, mas o orquestrador não tem como saber do que ele cuida. Com vários especialistas assim, todos ficariam com o mesmo nome genérico.

**\[Recomendação\]** Sempre defina `name` e `description` em cada especialista. Escreva a descrição como responderia à pergunta "quando devo chamar você, e quando não?" (ex.: "Responde sobre curvas de juros. Não responde sobre câmbio.").

**\[Oficial\]** Com `.as_tool(name=...)`, o nome precisa seguir o padrão `[a-zA-Z0-9_\-]{1,64}`: letras, números, `_` e `-`, de 1 a 64 caracteres, sem espaço.

## O que volta e quando o especialista erra

**O que volta.** **\[Testado\]** A resposta do especialista chega ao orquestrador como um recibo comum do tópico 3: `{'toolUseId': 't1', 'status': 'success', 'content': [{'text': 'Chove 80% hoje.\n'}]}`. O orquestrador lê esse texto e monta a resposta final para você.

**Quando o especialista erra.** **\[Testado\]** Simulei um especialista cujo modelo falha. O programa não parou: o recibo veio com `status: 'error'` e o texto `Agent error: modelo do especialista caiu`, e o orquestrador seguiu e terminou normalmente. É o mesmo comportamento das tools comuns: o erro vira recibo.

**E a memória do especialista?** O especialista lembra do que você falou nas chamadas anteriores? Depende. **\[Oficial\]** Com `preserve_context=True` em `.as_tool()`, ele lembra. **\[Testado\]** Nos meus testes, chamando o especialista duas vezes:

| `preserve_context` | Mensagens do especialista depois da 1ª chamada | Depois da 2ª chamada |
| --- | --- | --- |
| `False` (padrão) | 2 | 2 (começou do zero de novo) |
| `True` | 2 | 4 (guardou a conversa) |

**\[Recomendação\]** Deixe `False` por padrão: cada pergunta começa limpa e o resultado fica previsível. Use `True` só quando o especialista precisa continuar uma conversa (por exemplo, um assistente que refina uma análise passo a passo).

## Para ir mais fundo (opcional)

Pode pular esta seção e voltar quando precisar.

**1. `delegate=True`: o especialista responde direto ao usuário.** **\[Testado\]** Em `.as_tool(delegate=True)`, o orquestrador usa a resposta do especialista como resposta final, sem uma segunda chamada ao modelo para reescrever. No teste, a resposta saiu exatamente a do especialista. O Strands também acrescenta à descrição da tool: "Calling this tool will return its response directly to the user as the final answer. It should be the only tool called in the turn." Serve para roteadores simples (ex.: "dúvidas de cobrança vão para o especialista de cobrança").

**2. Na forma `@tool`, o especialista nasce a cada chamada.** **\[Oficial\]** No exemplo da documentação, o agente é criado dentro da função, então não guarda histórico entre chamadas (a própria página não diz isso com todas as letras; é o que o código mostra). A mesma forma traz um `try/except` que devolve o erro como texto. **\[Testado\]** Sem esse `try/except`, uma exceção dentro da função `@tool` também vira `status: error` (tópico 3).

**3. Cada agente tem o seu modelo e as suas tools.** **\[Oficial\]** A documentação destaca que cada especialista pode ter prompt e tools sob medida. Nada impede de usar modelos diferentes por agente (um mais barato para tarefas simples, por exemplo), mas isso é dedução minha e não testei com modelos reais.

**4. Executores se aplicam a esses agentes.** Do tópico 4: se o orquestrador pedir dois especialistas de uma vez, o executor dele decide se rodam juntos ou em fila. **\[Recomendação, não testado\]** Cada especialista tem o seu próprio executor para as tools dele.

**5. Agentes remotos.** **\[Oficial\]** A página menciona que um agente remoto pode ser usado via protocolo A2A (classe `A2AAgent`). Não li essa página.

**6. Custo e tempo.** **\[Recomendação\]** Cada chamada a um especialista é uma ou mais chamadas a um modelo de IA, então um orquestrador com muitos especialistas custa e demora mais do que um agente único com poucas tools. A documentação não trata de latência nem de custo.

**7. TypeScript.** **\[Oficial\]** A página tem os equivalentes (`asTool`, `preserveContext`). Como você está em Python, ignorei.

## Exercício guiado

Objetivo: ver um orquestrador com dois especialistas, o pedido que ele faz e o recibo que volta. Como nos tópicos anteriores, o código traz um "modelo de mentira" para você não precisar de conta na AWS. Aqui o modelo do orquestrador "decide" chamar o especialista de câmbio; num caso real, quem decide é o modelo de IA.

**Passo 1.** Na pasta `C:\Users\jecoe\strands`, crie `exercicio_t5.py`:

```python
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

# --- Orquestrador: o modelo de mentira "decide" chamar o especialista 'cambio' ---
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
```

**Passo 2.** Rode `python exercicio_t5.py`.

**Resultado esperado** **\[Testado\]**:

```text
Tools do orquestrador: ['cambio', 'curvas']
Resposta: Resposta final: Dólar a R$ 5,40 (valor de exemplo).
Pedido ao especialista: cambio {'input': 'Quanto está o dólar?'}
Recibo: {'toolUseId': 't1', 'status': 'success', 'content': [{'text': 'Dólar a R$ 5,40 (valor de exemplo).\n'}]}
```

**O que observar:**

- As duas linhas `Tools do orquestrador` mostram que cada especialista virou uma tool, com o nome que você deu em `name`.
- O pedido ao especialista tem um único campo, `input`, com o texto da pergunta.
- O recibo é o mesmo formato do tópico 3. O `\n` no fim do texto é uma quebra de linha que o Strands acrescenta.

**Desafio 1:** troque `pede=("cambio", ...)` por `pede=("curvas", ...)`. Qual especialista responde agora?

**Desafio 2:** apague `name="cambio"` e `description=...` do primeiro especialista e rode de novo. Que nome a tool recebe? **\[Testado\]** A primeira linha passa a mostrar `['Strands Agents', 'curvas']`, e o recibo volta com `status: 'error'` e o texto `Unknown tool: cambio`, porque o modelo de mentira pede `cambio` e essa tool não existe mais com esse nome. Sem `name`, o especialista continua funcionando, mas com um nome genérico que o orquestrador não associa ao assunto dele.

## Glossário

| Termo | Em palavras simples |
| --- | --- |
| Agente como tool | um agente colocado na lista de tools de outro agente, para ser chamado como se fosse uma tool |
| Orquestrador | o agente "gerente": fala com você, decide qual especialista chamar e junta as respostas |
| Especialista | o agente de uma área só (câmbio, curvas...), usado como tool pelo orquestrador |
| Cartão de visita | meu apelido para `name` + `description`: o que o orquestrador lê para decidir quem chamar |
| `input` | o texto que o orquestrador envia ao especialista; é o único parâmetro da tool-agente |
| `.as_tool()` | método que transforma um agente em tool escolhendo nome, descrição e memória |
| `preserve_context` | se `True`, o especialista lembra das chamadas anteriores; se `False` (padrão), começa do zero toda vez |
| `delegate` | se `True`, a resposta do especialista vira a resposta final, sem o orquestrador reescrever |
| `system_prompt` | as instruções fixas de um agente, que dizem o papel dele |
| A2A | protocolo para um agente falar com agentes remotos (não aprofundado aqui) |

## Fontes e o que não foi verificado

**Página que abri e li:**

- [Agents as Tools with Strands Agents SDK](https://strandsagents.com/docs/user-guide/concepts/multi-agent/agents-as-tools/): conceito, padrão orquestrador/especialistas, as três formas de código, boas práticas, `preserve_context`, A2A.
- [Tools Overview](https://strandsagents.com/docs/user-guide/concepts/tools/): onde "Agents as Tools" aparece na lista de formas de construir tools.

**Testado por mim** em strands-agents 1.62.0, com um modelo de mentira: as três formas, nome e descrição padrão, recibo de sucesso e de erro, `preserve_context` (2 e 4 mensagens), `delegate=True`, e os dois desafios. Os parâmetros de `.as_tool()` (`name`, `description`, `preserve_context`, `delegate`) e o padrão de nome vieram da documentação embutida no próprio código da biblioteca.

**Não verificado:**

- Como um modelo de IA real escolhe entre vários especialistas, e a qualidade da resposta final que ele monta. Nos testes, o "modelo de mentira" apenas repete o texto do especialista.
- Execução com Bedrock ou outro provedor real (sem credenciais aqui).
- Agentes remotos (A2A): só citados.
- Custo, tempo e falhas de roteamento: a página oficial não trata disso.
- Outros padrões multiagente do Strands (Swarm, Graph, Workflow): existem na documentação, mas não foram lidos aqui.
- As dicas marcadas **\[Recomendação\]** são minhas.
