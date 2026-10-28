# Strands Agents — Tópico 7: tools via MCP

Oct 28, 2026 · @Jéssica Coelho

## Resumo e como ler

Nos tópicos anteriores, as tools eram funções escritas por você, no mesmo arquivo do agente. Este tópico mostra outro caminho: usar tools que **moram em outro programa**, chamado de **servidor MCP**, e que o agente "pega emprestadas". Você não precisa saber programar para acompanhar. Cada termo técnico é explicado na primeira vez em que aparece, e no fim há um glossário.

**Como ler:**

- Se tiver pouco tempo, leia só as três primeiras seções depois deste resumo: a ideia central, o mínimo para funcionar e as formas de conexão.
- A seção "Para ir mais fundo" é opcional. Pule sem culpa e volte quando quiser.
- O exercício no final leva uns 20 minutos e roda no seu computador, **sem modelo de IA e sem chave de acesso**.

**As marcas de origem.** Para você saber em quem confiar, algumas frases começam com uma etiqueta:

- **\[Oficial\]**: está na documentação do Strands ou do MCP.
- **\[Testado\]**: eu rodei o código com `strands-agents` 1.62.0 e `mcp` 2.1.1 e vi o resultado.
- **\[Recomendação\]**: é um conselho meu, sem fonte oficial. Trate como opinião.

**Um aviso que vale ouro.** **\[Testado\]** Alguns exemplos da página oficial do Strands sobre MCP **não funcionam numa instalação nova**, porque o pacote `mcp` mudou de versão e renomeou duas peças (explico na seção "O mínimo para funcionar"). Os exemplos deste documento foram rodados na versão nova e funcionam nela.

## A ideia central

**MCP** é a sigla de *Model Context Protocol* ("protocolo de contexto para modelos"). Pense numa **tomada padrão**: se todo aparelho e toda parede seguem o mesmo formato de tomada, qualquer aparelho liga em qualquer parede, sem adaptador feito sob medida. O MCP é esse formato combinado entre quem **oferece** ferramentas e quem **usa** ferramentas. *(Essa definição geral é do meu conhecimento; não consegui abrir a página oficial do protocolo nesta pesquisa. A página do Strands, que li, descreve o uso.)*

| Palavra | Na analogia | No Strands |
| --- | --- | --- |
| **Servidor MCP** | Uma loja com vitrine: tem um catálogo de serviços e atende pedidos | Um programa à parte (seu, de terceiros ou da AWS) que oferece tools |
| **Cliente MCP** | O balcão pelo qual o seu agente fala com a loja | `MCPClient`, uma peça do próprio Strands |
| **Tool MCP** | Um item do catálogo | Aparece para o agente igual a uma tool normal, com nome, descrição e valores |

&#91;embedded content: quem fala com quem · 2 programas, 1 conexão\]

**Por que isso importa para você.** A grande diferença em relação aos tópicos anteriores é **onde o código da tool roda**: não no seu programa, mas no servidor. Duas consequências práticas:

- Você pode usar tools que outra pessoa escreveu e mantém, sem copiar o código dela.
- A conexão precisa estar **aberta** enquanto o agente trabalha. Esse é o ponto que mais dá erro para quem está começando, e a próxima seção mostra como cuidar disso.

**\[Oficial\]** O `MCPClient` segue a interface `ToolProvider` do Strands. Em linguagem simples: ele pode ser entregue ao agente na lista `tools=[...]`, e o agente cuida de abrir e fechar a conexão sozinho. **\[Testado\]** Isso funcionou, e as tools do servidor apareceram em `agent.tool_names`, misturadas às demais.

## O mínimo para funcionar

Você precisa de **dois arquivos** na mesma pasta: o servidor (a "loja") e o programa que o usa (o "cliente"). Como no Tópico 1, os comandos de instalação vão no terminal e os códigos são salvos como arquivos `.py`.

**\[Testado\]** `pip install strands-agents` já traz o pacote `mcp` junto. Você não precisa instalar mais nada para este tópico.

### Arquivo 1: `servidor_mcp.py` (a loja)

Este programa **só oferece tools**. Ele não tem agente nem modelo. Cada função marcada com `@servidor.tool(...)` vira um item do catálogo, e o texto de `description` é a ficha que o modelo vai ler (a mesma ideia do Tópico 2).

```python
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
```

O que cada trecho faz:

| Trecho | Em linguagem simples |
| --- | --- |
| `try: ... except ImportError: ...` | Tenta o nome novo das peças do pacote `mcp` e, se não existir, usa o nome antigo. Assim o arquivo funciona nas duas versões (explico logo abaixo). |
| `MCPServer("Servidor de Exemplo", ...)` | Cria a loja e dá um nome a ela. `log_level="CRITICAL"` só silencia os avisos técnicos do servidor, para não poluir a sua tela. |
| `@servidor.tool(description=...)` | A etiqueta que põe a função abaixo no catálogo. Parecida com o `@tool` dos tópicos anteriores. |
| `servidor.run(transport="stdio")` | Abre a loja e fica esperando pedidos. `stdio` é a forma mais simples de conversa (veja a próxima seção). |

### Arquivo 2: `primeiro_mcp.py` (o cliente)

```python
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
```

Rode com `python primeiro_mcp.py`. **\[Testado\]** A saída é:

```
['somar', 'dividir', 'dividir_claro', 'saudar']
[{'text': '5'}]
```

| Trecho | Em linguagem simples |
| --- | --- |
| `command=sys.executable, args=["servidor_mcp.py"]` | "Abra o servidor como um programa separado, usando o mesmo Python que está rodando este arquivo." O Strands liga o servidor para você; você não precisa abri-lo à mão. |
| `stdio_client(...)` | A conversa com o servidor acontece pelo teclado e pela tela do programa (a "entrada e saída padrão", *stdio*), sem rede. |
| `lambda: ...` | Uma função de uma linha, sem nome. Aqui serve de **receita**: o Strands guarda a receita de como abrir a conexão e a executa quando precisar. |
| `with cliente:` | Abre a conexão no começo do bloco e **fecha sozinha no fim**. Tudo que usa as tools MCP precisa ficar dentro dele. |
| `cliente.list_tools_sync()` | Pergunta ao servidor "o que você tem no catálogo?" e devolve a lista de tools. |
| `Agent(tools=tools)` | Igual aos tópicos anteriores: entrega a caixa de ferramentas ao agente. |

### Duas formas de entregar o cliente ao agente

**\[Oficial\]** A página do Strands chama a primeira de **gerenciada** (recomendada) e a segunda de **manual**:

```python
# Gerenciada: o Strands abre e fecha a conexão sozinho
agente = Agent(tools=[cliente])

# Manual: você controla o bloco with
with cliente:
    agente = Agent(tools=cliente.list_tools_sync())
```

**\[Testado\]** As duas funcionaram. Na gerenciada, eu até chamei `agente.tool.somar(a=1, b=2)` sem nenhum `with` e deu certo. E um agente com um modelo de mentira (o truque do Tópico 4) pediu a tool `somar` e recebeu `5` de volta, então o caminho completo "modelo pede, servidor executa, resultado volta" funciona.

### O aviso: dois nomes da página oficial não existem mais

**\[Testado\]** O pacote `mcp` lançou a versão 2, e uma instalação nova pega essa versão (o README do Strands diz o mesmo, e o Strands 1.62.0 aceita `mcp` até a 2.1). Nela:

| O que a página oficial do Strands usa | O que acontece no `mcp` 2.1.1 | O que usar |
| --- | --- | --- |
| `from mcp.server import FastMCP` | `ImportError` | `from mcp.server.mcpserver import MCPServer` |
| `from mcp.client.streamable_http import streamablehttp_client` | `ImportError` | `streamable_http_client` (com `_` extra) |

A mensagem de erro do próprio pacote já explica: *"FastMCP was renamed to MCPServer ... or pin 'mcp<2' to keep running v1 code"*, ou seja, "o FastMCP foi renomeado; ou fixe `mcp<2` para continuar com o código antigo". **\[Recomendação\]** Se você copiar exemplos da internet e aparecer esse erro, esse é o motivo. O `try/except` do arquivo 1 existe justamente para funcionar nas duas versões.

**\[Testado\]** Instalei também o `mcp` 1.30.0 (a última da família 1.x) para comparar. Nele, o nome novo do cliente HTTP (`streamable_http_client`) **existe junto** com o antigo, mas o `MCPServer` **não existe**: só o `FastMCP`. Por isso o `try/except` do arquivo 1 é necessário, e o exercício deste tópico rodou inteiro nas duas versões.

## Formas de conexão: como o agente chega ao servidor

Até aqui usamos a forma mais simples (`stdio`). Mas um servidor pode estar em outro lugar, e cada lugar pede um jeito de conversar, chamado de **transporte**. Pense em escolher entre falar com a loja pessoalmente, por telefone ou por um balcão corporativo com crachá.

**\[Oficial\]** A página do Strands lista quatro:

| Transporte | Quando o servidor está... | Como o Strands conecta | Testei? |
| --- | --- | --- | --- |
| **stdio** | Na sua máquina, como um programa que o Strands liga | `stdio_client(StdioServerParameters(command=..., args=[...]))` | Sim |
| **Streamable HTTP** | Já ligado em um endereço (URL), na sua máquina ou na internet | `streamable_http_client("http://...")` | Sim, local |
| **SSE** (*Server-Sent Events*) | Já ligado em um endereço, em um formato mais antigo de HTTP | `sse_client("http://...")` | Sim, local |
| **AWS IAM (SigV4)** | Num serviço da AWS que exige assinatura de credenciais | `aws_iam_streamablehttp_client(...)`, do pacote `mcp-proxy-for-aws` | Não |

"Local" aqui significa que o servidor rodou no mesmo computador onde fiz o teste. Não testei servidores remotos, nem o da AWS.

### stdio: o servidor é um programa que o Strands liga

É a forma do tópico anterior. Não abre porta de rede e não precisa de endereço. É a melhor para aprender e para tools que ficam no seu computador.

**\[Oficial\]** O exemplo rápido da página do Strands liga um servidor pronto da AWS usando `uvx`:

```python
MCPClient(lambda: stdio_client(
    StdioServerParameters(
        command="uvx",
        args=["awslabs.aws-documentation-mcp-server@latest"]
    )
))
```

`uvx` é um comando da ferramenta `uv`, que baixa e executa um programa Python pronto sem você instalar nada à mão. Ele só existe se você tiver o `uv` instalado. **\[Oficial\]** No Windows, a página mostra uma variação com `"--from", "awslabs.aws-documentation-mcp-server@latest", "awslabs.aws-documentation-mcp-server.exe"`. **Não testei esse exemplo**, porque o ambiente onde trabalho não alcança o pacote da AWS. Por isso os testes deste documento usam o seu próprio `servidor_mcp.py`.

### Streamable HTTP: o servidor já está ligado numa URL

Primeiro, ligue o servidor em modo HTTP. No `servidor_mcp.py`, troque a última linha por `servidor.run(transport="streamable-http")` e rode `python servidor_mcp.py` (ele fica esperando; deixe esse terminal aberto). **\[Testado\]** O endereço padrão foi `http://127.0.0.1:8000/mcp`. Em outro terminal, o cliente:

```python
from mcp.client.streamable_http import streamable_http_client
from strands.tools.mcp import MCPClient

cliente = MCPClient(lambda: streamable_http_client("http://127.0.0.1:8000/mcp"))

with cliente:
    print([t.tool_name for t in cliente.list_tools_sync()])
```

**\[Testado\]** Isso listou as tools do servidor. `127.0.0.1` é o endereço "do próprio computador"; para um servidor na internet, você troca pela URL dele.

### Como mandar uma senha (token) para o servidor

Servidores na internet costumam exigir um **token**: uma senha longa enviada junto de cada pedido, num campo chamado *cabeçalho* (*header*). **\[Oficial\]** A página do Strands mostra isso com `streamablehttp_client(url=..., headers={"Authorization": f"Bearer {os.getenv('MCP_PAT')}"})`. **\[Testado\]** Esse código **não funciona com o `mcp` 2.x**: a função nova não aceita `headers` e dá `TypeError: streamable_http_client() got an unexpected keyword argument 'headers'`. Na versão nova, os cabeçalhos entram por um cliente HTTP à parte:

```python
import os
from mcp.client.sse import create_mcp_http_client
from mcp.client.streamable_http import streamable_http_client
from strands.tools.mcp import MCPClient

cliente = MCPClient(lambda: streamable_http_client(
    "http://127.0.0.1:8000/mcp",
    http_client=create_mcp_http_client(
        headers={"Authorization": f"Bearer {os.getenv('MCP_TOKEN')}"}
    ),
))
```

**\[Testado\]** Essa forma conectou e listou as tools. **Não verifiquei** se o servidor de teste recebeu o cabeçalho, porque ele não exige token. **\[Recomendação\]** Nunca escreva o token direto no código (ele iria junto se você subisse o arquivo para o GitHub). Guarde numa variável de ambiente, como no exemplo.

### SSE: o formato mais antigo

**\[Testado\]** `sse_client("http://127.0.0.1:8000/sse")`, com o servidor ligado por `servidor.run(transport="sse")`, conectou, listou as tools e executou uma delas. **\[Oficial\]** A página do Strands lista o SSE ao lado dos outros. **Não verifiquei** se ele está sendo aposentado em favor do Streamable HTTP; para um servidor novo seu, comece pelo Streamable HTTP. Isso é uma **\[Recomendação\]** minha.

### Vários servidores ao mesmo tempo

**\[Oficial\]** É só colocar mais de um cliente na lista:

```python
agente = Agent(tools=[cliente_a, cliente_b])
```

Se dois servidores tiverem uma tool com o mesmo nome, use um prefixo (veja a próxima seção).

## O que volta de uma tool MCP, e como erros aparecem

No Tópico 3 você viu que todo resultado de tool é um "recibo" com `status` e `content`. Com tools MCP é o mesmo recibo, mais alguns campos.

### O recibo de uma tool MCP

Chamando `cliente.call_tool_sync(tool_use_id="p3", name="somar", arguments={"a": 2, "b": 3})`, **\[Testado\]** o recibo foi:

```
{'status': 'success', 'toolUseId': 'x1', 'content': [{'text': '5'}],
 'structuredContent': {'result': 5},
 'metadata': {'io.modelcontextprotocol/serverInfo': {'name': 'Servidor de Exemplo', 'version': ''}},
 'isError': False}
```

| Campo | O que é |
| --- | --- |
| `status`, `toolUseId`, `content` | Os mesmos do Tópico 3 |
| `structuredContent` | O mesmo resultado em formato de dados (aqui, `{'result': 5}`), além do texto |
| `metadata` | Informações de qual servidor respondeu |
| `isError` | `True` se o servidor marcou a resposta como erro. Acompanha o `status` |

O modelo lê o `content`. Os outros campos são para o seu programa.

### Como os erros aparecem: quatro casos

**\[Testado\]** Estes resultados são do `mcp` 2.1.1 (a diferença para a versão 1.30 vem logo depois da tabela). Em três deles o programa **não para**: o erro chega dentro do recibo, com `status: error`.

| Situação | O que o recibo diz | O modelo consegue entender o motivo? |
| --- | --- | --- |
| A tool do servidor dá um erro comum (`raise ValueError("o denominador não pode ser zero")`) | `Error executing tool dividir` | **Não.** O motivo foi escondido |
| A tool dá um erro do tipo `ToolError` com mensagem | `Error executing tool dividir_claro: o denominador não pode ser zero` | **Sim** |
| Valor com tipo errado (`a="x"` onde se espera inteiro) | `Error executing tool somar: 1 validation error ... Input should be a valid integer` | Sim, com detalhes técnicos |
| Usar o cliente fora do bloco `with` | **Exceção** `MCPClientInitializationError: the client session is not running...` | Não se aplica: o programa para |

O primeiro caso merece atenção. Se você é quem escreve o servidor, **\[Recomendação\]** use `ToolError` quando quiser que o agente saiba o que deu errado. Do contrário, ele só recebe "deu erro" e pode tentar de novo às cegas. Essa diferença depende da versão do pacote. **\[Testado\]** No `mcp` 1.30.0, o mesmo erro comum mostra o motivo (`Error executing tool dividir: o denominador não pode ser zero`); no 2.1.1, não. Com `ToolError`, a mensagem aparece nas duas. Ou seja, `ToolError` é o jeito que funciona nas duas versões testadas; o erro comum, não.

Um quinto caso é uma armadilha antiga. **\[Testado\]** Uma tool que **devolve** o texto `"ERRO: o denominador não pode ser zero"` (em vez de dar erro) volta com `status: success` e `isError: False`. Para o Strands, é uma resposta normal, igual ao que aconteceu no Tópico 3 com texto que parece erro.

### Nomes, prefixo e filtros

O nome que o agente enxerga é o nome da função no servidor (`somar`). Se você liga dois servidores com uma tool de mesmo nome, ou quer deixar claro de onde cada tool vem, dê um **prefixo** ao cliente. E se o servidor oferece mais do que você quer dar ao agente, use **filtros**. **\[Oficial\]** Os dois são do Python (a página diz que não existem na versão TypeScript):

```python
import re

cliente = MCPClient(
    lambda: stdio_client(
        StdioServerParameters(command=sys.executable, args=["servidor_mcp.py"])
    ),
    prefix="ex",
    tool_filters={
        "allowed": [re.compile(r"^(somar|dividir)")],
        "rejected": ["dividir"],
    },
)
```

**\[Testado\]** Com o servidor de exemplo (`somar`, `dividir`, `dividir_claro`, `saudar`), a lista ficou `['ex_somar', 'ex_dividir_claro']`. Leia o resultado com calma:

- `allowed` guarda só quem passa no filtro: `saudar` caiu fora, e `somar`, `dividir` e `dividir_claro` ficaram. **\[Oficial\]** O `allowed` é aplicado primeiro, e o `rejected` depois.
- `rejected: ["dividir"]`, escrito como texto, tirou **só** a tool chamada exatamente `dividir`. A `dividir_claro` continuou. Se quisesse tirar as duas, o filtro teria que ser uma expressão como `re.compile(r"^dividir")`.
- O prefixo entrou na frente de tudo.

**Uma pegadinha do prefixo.** **\[Testado\]** O agente enxerga `ex_somar` e `agente.tool.ex_somar(...)` funciona; `agente.tool.somar(...)` não existe mais. Porém, na chamada direta ao cliente, `cliente.call_tool_sync(name="somar", ...)` usa o **nome original do servidor**: com `name="ex_somar"` o recibo volta `status: error` com `Unknown tool: ex_somar`. Dois nomes para a mesma tool, conforme quem chama.

## Cuidados: você está ligando o código de outra pessoa ao seu agente

No Tópico 1 você viu a analogia da chave do escritório: anexar uma tool é entregar a chave. Com MCP isso fica mais importante, porque o código costuma ser **de terceiros**. Três pontos concretos:

### 1. Quem escreve a ficha da tool é o servidor

**\[Testado\]** A descrição que o modelo lê vem pronta do servidor. No exercício, `tools[0].tool_spec["description"]` devolveu exatamente o texto do `servidor_mcp.py`: "Soma dois números inteiros.". Ou seja, **quem controla o servidor controla o que o modelo lê** sobre a tool. Um servidor confiável escreve fichas honestas. Um servidor malicioso poderia escrever instruções disfarçadas de descrição. **\[Recomendação\]** Essa preocupação é minha, a partir do que o teste mostrou; não li uma fonte oficial sobre o assunto e não simulei um ataque.

### 2. No stdio, o Strands executa um comando no seu computador

`command="uvx"` ou `command=sys.executable` não são enfeites: o Strands roda esse programa, com as **suas permissões**. O exemplo oficial usa `awslabs.aws-documentation-mcp-server@latest`, e `@latest` significa "a versão mais nova, seja qual for". **\[Recomendação\]** Em algo que importe, fixe a versão (por exemplo, `...-server@1.2.3`, com o número que você revisou), para que uma atualização surpresa não mude o que roda na sua máquina.

**\[Oficial\]** A página do Strands resume as boas práticas em: descrições claras, mensagens de erro informativas, atenção à segurança (principalmente em servidores acessíveis pela rede), sempre usar `with` e definir limites de tempo (*timeouts*) para chamadas demoradas.

### 3. Dê ao agente só o que ele precisa

Se o servidor oferece vinte tools e o seu caso usa duas, entregue duas. O filtro `allowed` da seção anterior serve para isso. **\[Testado\]** No exemplo, `saudar` ficou invisível ao agente porque não passou no filtro. **\[Recomendação\]** Prefira listar o que **pode** (`allowed`) a listar o que **não pode** (`rejected`): se o servidor ganhar uma tool nova amanhã, com `allowed` ela não entra sozinha.

### Cinco perguntas antes de conectar um servidor

**\[Recomendação\]** São critérios meus, não regras oficiais.

| Pergunta | Por que importa |
| --- | --- |
| Quem mantém este servidor? | Código de fonte desconhecida merece mais cuidado que o do seu time |
| Que comando o Strands vai rodar na minha máquina? | No stdio, é código rodando com as suas permissões |
| A versão está fixada? | `@latest` muda sem aviso |
| Preciso de todas as tools dele? | Menos tools, menos estrago possível |
| Onde está o token? | Em variável de ambiente, nunca escrito no código nem enviado ao GitHub |

## Para ir mais fundo (opcional)

Tudo o que vem aqui é complemento. Você pode pular e voltar quando precisar.

### Quando o servidor pergunta algo a você (*elicitation*)

**\[Oficial\]** Um servidor MCP pode **pausar** uma tool no meio do caminho para pedir uma confirmação ou uma informação ao usuário, como "posso apagar estes arquivos?". O servidor declara o que quer saber, e o seu programa fornece uma função (`elicitation_callback`) que responde. Pense num atendente da loja que, antes de fechar a compra, vem ao balcão perguntar "confirma?".

O cliente do exemplo oficial:

```python
async def elicitation_callback(context, params):
    print(f"ELICITATION: {params.message}")
    return ElicitResult(action="accept", content={"username": "myname"})

client = MCPClient(
    lambda: stdio_client(StdioServerParameters(command="python", args=["/path/to/server.py"])),
    elicitation_callback=elicitation_callback,
)
```

**\[Testado\]** Rodei um servidor e um cliente nesse formato, adaptados. Resultado:

| Versão do `mcp` | O que aconteceu |
| --- | --- |
| 1.30.0 | **Funcionou.** A pergunta chegou ao cliente (`Apagar ['a.txt']?`) e a tool respondeu `Jé aprovou apagar ['a.txt']` |
| 2.1.1 | **O código do servidor do exemplo oficial quebra** (`s.get_context()` não existe mais). Tentei a forma nova, pedindo o contexto como parâmetro da tool (`ctx: Context`), e a chamada falhou com `Cannot send 'elicitation/create': this transport context has no back-channel for server-initiated requests` |

**Não consegui fazer a elicitation funcionar na 2.1.1.** Pode haver uma forma de configurar que eu não achei, então não conclua que a função foi removida: concluo só que o exemplo oficial, do jeito que está, não roda nela. **\[Recomendação\]** Se precisar de elicitation, fixe `mcp<2` (`pip install "mcp<2"`) e use o exemplo oficial.

### O que a versão do Strands aceita

**\[Testado\]** Pelos metadados do pacote, o `strands-agents` 1.62.0 exige `mcp>=1.23.0,<2.2`. Ou seja, aceita da 1.23 à 2.1. O README do Strands cita um arquivo `docs/MCP_VERSIONS.md` com as diferenças na 2.x; **não consegui abrir** esse arquivo (meu acesso à internet é limitado), então não sei o que ele diz.

### Chamar uma tool MCP direto, sem agente

Você já usou: `cliente.call_tool_sync(tool_use_id=..., name=..., arguments={...})`. **\[Oficial\]** A página mostra esse formato para chamar tools sem o agente. É o equivalente da chamada direta do Tópico 1, mas no cliente. Lembre a pegadinha do prefixo: aqui vale o nome original do servidor.

### O que eu não cobri

- Servidores remotos reais, com token de verdade (testei só servidores locais).
- O transporte da AWS (`mcp-proxy-for-aws`) e o servidor de documentação da AWS do exemplo oficial.
- Outros recursos do protocolo MCP além de tools. A página do Strands que li trata só de tools e elicitation.

## Exercício guiado

Tempo estimado: 20 minutos. Você precisa ter feito os passos do Tópico 1 (Python e `pip install strands-agents`). **Não precisa de modelo de IA nem de chave de acesso.**

**\[Testado\]** O código e as saídas abaixo foram executados em Linux com Python 3.13, `strands-agents` 1.62.0 e `mcp` 2.1.1. O exercício também rodou com `mcp` 1.30.0 (a única diferença está no passo 4a, explicada abaixo). **Não testei no Windows.**

### Parte 1: ligar, listar, chamar e errar

1. Crie uma pasta nova (por exemplo, `exercicio_mcp`).
2. Salve nela o `servidor_mcp.py` da seção "O mínimo para funcionar" (o código completo, com as quatro tools).
3. Na **mesma pasta**, salve o código abaixo como `exercicio_t7.py`.
4. No terminal, entre nessa pasta e rode `python exercicio_t7.py`. Precisa ser de dentro da pasta, porque o programa procura o `servidor_mcp.py` pelo nome.

```python
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
```

Saída esperada (mais um bloco de texto de erro no final, que termina na linha mostrada):

```
1: ['somar', 'dividir', 'dividir_claro', 'saudar']
2: somar | Soma dois números inteiros.
3: success [{'text': '5'}]
4a: error [{'text': 'Error executing tool dividir'}]
4b: error [{'text': 'Error executing tool dividir_claro: o denominador não pode ser zero'}]
5a: ['somar', 'dividir', 'dividir_claro', 'saudar']
5b: [{'text': 'Olá, Jé!'}]
6: ['ex_somar', 'ex_dividir_claro']
strands.types.exceptions.MCPClientInitializationError: the client session is not running. ...
```

**O que observar:**

- **Passo 1 e 2:** as tools e a ficha vieram do servidor. Você não escreveu nenhuma delas neste arquivo.
- **Passo 3:** a tool rodou **sem agente e sem modelo**. O recibo completo tem mais campos (veja a seção de resultados); aqui imprimimos só `status` e `content`.
- **Passo 4:** compare 4a e 4b. No `mcp` 2.1.1, o erro comum esconde o motivo e o `ToolError` mostra. No `mcp` 1.30.0, o 4a também mostra o motivo (`Error executing tool dividir: o denominador não pode ser zero`).
- **Passo 5:** as tools MCP entraram no agente como as tools dos tópicos anteriores, inclusive a chamada direta `agente.tool.saudar(...)`.
- **Passo 6:** `saudar` sumiu (filtro `allowed`), `dividir` sumiu (filtro `rejected`) e o prefixo `ex_` apareceu nas que sobraram.
- **Passo 7:** este erro é **de propósito**. O programa para com uma exceção porque o cliente foi usado fora do `with`.

### Parte 2: desafios (sem código pronto, de propósito)

1. **Tirar as duas divisões.** No passo 6, troque `"rejected": ["dividir"]` por uma expressão regular que tire `dividir` **e** `dividir_claro`. **\[Testado\]** O resultado esperado é `['ex_somar']`. Dica: o `allowed` já usa `re.compile(...)`.
2. **Listar só o que pode.** Crie um cliente com `tool_filters={"allowed": ["saudar"]}` e imprima a lista. **\[Testado\]** Esperado: `['saudar']`.
3. **Sua própria tool.** No `servidor_mcp.py`, acrescente uma tool `quilometros_para_milhas` (1 km = 0,621371 milha), com `description` e tipos nos parâmetros. Rode o exercício de novo: ela deve aparecer no passo 1 **sem você mexer no `exercicio_t7.py`**. Chame-a com `call_tool_sync` e confira `6.21371` para 10 km.
4. **Pela rede.** Troque a última linha do servidor por `servidor.run(transport="streamable-http")`, rode `python servidor_mcp.py` num terminal e, em outro, use o código de `streamable_http_client` da seção de conexões. Confirme que lista as mesmas tools.

## Glossário

| Termo | Em linguagem simples |
| --- | --- |
| MCP (*Model Context Protocol*) | Um padrão combinado (a "tomada universal") entre quem oferece tools e quem as usa |
| Servidor MCP | Um programa à parte que oferece um catálogo de tools e executa os pedidos. A "loja" |
| Cliente MCP (`MCPClient`) | A peça do Strands que fala com o servidor. O "balcão" |
| Tool MCP | Uma tool que mora no servidor e aparece para o agente como qualquer outra |
| Transporte | O jeito de conversar com o servidor: `stdio`, Streamable HTTP, SSE ou AWS IAM |
| `stdio` | Conversa pela entrada e saída padrão do programa, sem rede. O Strands liga o servidor para você |
| Streamable HTTP | Conversa por um endereço (URL) de um servidor que já está ligado |
| SSE (*Server-Sent Events*) | Outro jeito de falar por URL, mais antigo |
| URL / endereço | O "endereço" do servidor, como `http://127.0.0.1:8000/mcp`. `127.0.0.1` é o próprio computador |
| Token | Uma senha longa enviada junto de cada pedido para provar quem você é |
| Cabeçalho (*header*) | O campo do pedido onde o token vai, como `Authorization` |
| Variável de ambiente | Um valor guardado no seu sistema, fora do código, lido com `os.getenv(...)`. O lugar certo para tokens |
| `with` (bloco) | Abre algo no começo do bloco e fecha sozinho no fim. A conexão MCP precisa estar aberta enquanto você usa as tools |
| `lambda` | Uma função de uma linha, sem nome. No `MCPClient`, é a "receita" de como abrir a conexão |
| `sys.executable` | O caminho do Python que está rodando o seu arquivo |
| `uv` e `uvx` | Ferramenta que baixa e roda programas Python prontos sem instalação manual. O `uvx` só existe se o `uv` estiver instalado |
| `@latest` | "A versão mais nova, seja qual for." Conveniente, mas muda sem aviso |
| Prefixo (`prefix`) | Um texto colocado na frente do nome das tools de um cliente, para evitar nomes repetidos |
| Filtro (`tool_filters`) | Lista do que o agente pode (`allowed`) ou não pode (`rejected`) receber do servidor |
| Expressão regular (`re.compile`) | Um padrão de texto, como `^dividir` ("começa com dividir"). Serve para filtrar nomes de uma vez |
| `ToolError` | Um tipo de erro do servidor MCP cuja mensagem chega ao agente |
| Exceção | Um erro que interrompe o programa, como o `MCPClientInitializationError` |
| Elicitation | O servidor pausar uma tool para pedir uma confirmação ou dado ao usuário |
| `ToolProvider` | A interface que permite entregar o `MCPClient` direto na lista `tools=[...]` do agente |
| Versão maior (1.x e 2.x) | Uma mudança grande do pacote, que pode renomear ou remover peças. Foi o que quebrou os exemplos oficiais |
| Recibo | O resultado de uma tool (`status`, `content` e, no MCP, campos extras). Veja o Tópico 3 |

## Fontes e o que não foi verificado

Consultado em 28/10/2026.

### Fontes lidas

- [MCP tools, Strands Agents](https://strandsagents.com/docs/user-guide/concepts/tools/mcp-tools/): base de tudo que está marcado como \[Oficial\] (MCPClient, transportes, filtros, prefixo, chamada direta, elicitation, boas práticas, solução de problemas).
- Metadados do pacote [`strands-agents` 1.62.0 no PyPI](https://pypi.org/project/strands-agents/): a faixa de versões `mcp>=1.23.0,<2.2` e o trecho do README sobre `mcp` 2.x. Li pelos metadados baixados com `pip`, não pela página.
- A mensagem de erro do próprio pacote `mcp` 2.1.1, que informa a renomeação `FastMCP` → `MCPServer` e aponta para o guia de migração.

### O que não foi verificado

- **A definição geral de MCP** ("padrão", "tomada universal") vem do meu conhecimento. Não consegui abrir a página oficial do protocolo nem o guia de migração do `mcp` 2 (não estão liberados no meu acesso), nem o arquivo `docs/MCP_VERSIONS.md` do Strands.
- **O exemplo oficial com `uvx` e o servidor de documentação da AWS** não foram executados (sem acesso à rede necessária). Todos os testes usam o `servidor_mcp.py` deste documento.
- **O transporte AWS IAM** (`mcp-proxy-for-aws`) não foi testado.
- **Servidores remotos e tokens reais.** Testei apenas servidores locais. Com cabeçalho, só confirmei que a conexão abre; não confirmei que o servidor recebeu o `Authorization`.
- **SSE:** não sei se está sendo aposentado em favor do Streamable HTTP.
- **Elicitation no `mcp` 2.1.1:** o exemplo oficial não rodou e não achei uma forma que rodasse; pode existir uma que eu não encontrei.
- **Segurança:** a análise dos riscos (ficha escrita pelo servidor, comando rodando na sua máquina, `@latest`) é raciocínio meu a partir do que os testes mostraram. Não simulei um servidor malicioso.
- **Windows:** nada foi rodado no Windows. O `sys.executable` deve funcionar, mas não confirmei.
- **Versões:** tudo foi testado com `strands-agents` 1.62.0, `mcp` 2.1.1 e `mcp` 1.30.0. Outras versões podem se comportar diferente, principalmente nas mensagens de erro.
- Um agente com modelo de mentira usou uma tool MCP com sucesso, mas **nenhum modelo de IA real** foi usado.
