# Strands Agents — Tópico 2: criar tools customizadas

Oct 27, 2026 · @Jéssica Coelho

## Resumo

Uma tool é um pequeno programa que o agente pode decidir usar. Para criá-la, você escreve uma **função** em Python, cola a etiqueta `@tool` em cima dela e escreve um texto explicando o que ela faz. O Strands transforma isso numa "ficha" que o modelo de IA lê para escolher quando usar a tool. Este documento ensina a criar tools e a decidir o que merece virar uma.

**Como ler:**

- Se tiver pouco tempo, leia as seis primeiras seções depois deste resumo. Elas trazem o essencial, com exemplos que você pode rodar.
- A seção "Para ir mais fundo" é opcional. Consulte quando precisar.
- Se você não fez o tópico 1, rode primeiro os passos de "Preparar o computador" daquele documento. Aqui não repito a instalação.

**As marcas de origem.** Algumas frases começam com uma etiqueta para você saber em quem confiar:

- **\[Oficial\]**: está na documentação do Strands Agents.
- **\[Testado\]**: eu rodei o código com `strands-agents` versão 1.62.0 e vi o resultado.
- **\[Recomendação\]**: é um conselho meu, sem fonte oficial. Trate como opinião.

## A ideia central: o cardápio do restaurante

Pense num restaurante. O cliente escolhe o prato pelo **cardápio**: nome, descrição, ingredientes. Ele nunca entra na cozinha. Quem prepara é a cozinha.

| No restaurante | No Strands |
| --- | --- |
| O cliente | O modelo de IA |
| O cardápio (nome, descrição, o que precisa saber) | A **ficha** da tool |
| A cozinha | O código da função |
| O prato pedido | A tool |

A consequência mais importante deste documento: **o modelo nunca lê o código da sua tool. Ele só lê a ficha.** Se a ficha for confusa, o modelo escolhe o prato errado ou nem pede o prato certo, mesmo que a cozinha seja excelente.

Criar uma tool tem, então, duas partes:

1. Escrever a **função** que faz o trabalho (a cozinha).
2. Escrever a **ficha** que explica o que ela faz (o cardápio).

**\[Oficial\]** O Strands monta a ficha sozinho a partir do que você escreveu na função: o nome, o texto de explicação logo abaixo do nome e os tipos de dados. A documentação reforça que os modelos dependem muito das descrições para decidir quando e como usar cada tool.

## O mínimo de Python para ler os exemplos

Você não precisa aprender Python para criar tools simples, mas precisa reconhecer cinco peças. Vamos montá-las uma a uma, a partir de uma função comum.

### Peça 1: a função

Uma **função** é uma receita com nome: recebe informações, faz alguma coisa e devolve um resultado.

```python
def dobro(numero):
    return numero * 2

print(dobro(21))
```

Saída: `42`. Linha por linha:

- `def dobro(numero):` cria uma função chamada `dobro`. A palavra `def` quer dizer "defina". O `numero` entre parênteses é o **parâmetro**: a informação que a função recebe.
- `return numero * 2` é o que ela **devolve**. O `*` é multiplicação. Essa linha tem recuo (espaços no começo) porque pertence à função. No Python, o recuo faz parte da regra.
- `dobro(21)` **chama** a função com o valor 21.

### Peça 2: as dicas de tipo

Você pode avisar que tipo de dado a função recebe e devolve:

```python
def dobro(numero: int) -> int:
    return numero * 2
```

O `: int` diz "este parâmetro é um número inteiro". O `-> int` diz "a função devolve um número inteiro". Essas indicações se chamam **dicas de tipo** (*type hints*). Os tipos mais comuns:

| Tipo | O que é | Exemplo |
| --- | --- | --- |
| `int` | Número inteiro | `21` |
| `float` | Número com casas decimais | `36.6` |
| `str` | Texto | `"Lisboa"` |
| `bool` | Verdadeiro ou falso | `True` |

### Peça 3: a docstring

A **docstring** é um texto entre aspas triplas, colocado logo abaixo da linha `def`, que explica o que a função faz. Para quem programa, é um comentário. Para o Strands, é a **descrição que o modelo vai ler**.

```python
def dobro(numero: int) -> int:
    """Devolve o dobro de um número inteiro.

    Args:
        numero: O número a ser dobrado
    """
    return numero * 2
```

A primeira frase descreve a função. Depois, uma seção `Args:` (de "argumentos") explica cada parâmetro, um por linha, no formato `nome: explicação`.

### Peça 4: o decorator

Um **decorator** é uma etiqueta colada logo acima de uma função, que começa com `@` e dá a ela um poder extra. O decorator do Strands se chama `@tool` e dá à função o poder de ser uma tool:

```python
from strands import tool

@tool
def dobro(numero: int) -> int:
    """Devolve o dobro de um número inteiro.

    Args:
        numero: O número a ser dobrado
    """
    return numero * 2
```

A linha `from strands import tool` busca a etiqueta `tool` dentro do pacote `strands`, que você instalou no tópico 1.

### Peça 5: o dicionário

Um **dicionário** é uma lista de pares "nome: valor" entre chaves, como `{"status": "success", "content": "pronto"}`. Você vai encontrá-lo no retorno de algumas tools, mais adiante.

Se quiser, copie o código da Peça 1 num arquivo `.py` e rode. Se o resultado for `42`, seu ambiente Python está funcionando.

## Sua primeira tool, linha por linha

Agora juntamos as cinco peças numa tool útil: converter temperatura de Celsius para Fahrenheit. Salve em um arquivo chamado `minha_tool.py`:

```python
from strands import Agent, tool

@tool
def celsius_para_fahrenheit(celsius: float) -> float:
    """Converte uma temperatura de graus Celsius para Fahrenheit.

    Use quando o usuário pedir conversão de temperatura.

    Args:
        celsius: Temperatura em graus Celsius
    """
    return celsius * 9 / 5 + 32

agent = Agent(tools=[celsius_para_fahrenheit])

print(agent.tool_names)
print(agent.tool.celsius_para_fahrenheit(celsius=25))
```

Rode com `python minha_tool.py`. **\[Testado\]** A saída é parecida com esta (o campo `toolUseId` muda a cada execução):

```
['celsius_para_fahrenheit']
{'toolUseId': '...', 'status': 'success', 'content': [{'text': '77.0'}]}
```

### O que cada parte faz

| Trecho | Papel |
| --- | --- |
| `from strands import Agent, tool` | Busca as duas peças do Strands de que precisamos |
| `@tool` | A etiqueta que faz a função abaixo virar uma tool |
| `def celsius_para_fahrenheit(celsius: float) -> float:` | A função: recebe um número com casas decimais e devolve outro |
| O texto entre aspas triplas | A docstring: vira a descrição que o modelo lê |
| `return celsius * 9 / 5 + 32` | A conta em si. O modelo nunca a vê |
| `Agent(tools=[...])` | Cria o agente já com a tool anexada (assunto do tópico 1) |
| `agent.tool.celsius_para_fahrenheit(celsius=25)` | Chama a tool diretamente, sem modelo, só para testar (também do tópico 1) |

### A ficha que o Strands montou

**\[Oficial\]** O Strands gera a ficha automaticamente a partir da função. Para ver como ela ficou, acrescente ao arquivo:

```python
print(agent.tool_registry.get_all_tools_config())
```

**\[Testado\]** O resultado, reformatado para leitura:

```
{'celsius_para_fahrenheit': {
    'name': 'celsius_para_fahrenheit',
    'description': 'Converte uma temperatura de graus Celsius para Fahrenheit.\n\nUse quando o usuário pedir conversão de temperatura.',
    'inputSchema': {'json': {
        'properties': {'celsius': {
            'description': 'Temperatura em graus Celsius',
            'type': 'number'}},
        'required': ['celsius'],
        'type': 'object'}}}}
```

O que você escreveu vira:

| O que você escreve | Vira, na ficha |
| --- | --- |
| O nome da função | O nome da tool (`name`) |
| O texto da docstring antes de Args: | A descrição da tool (`description`) |
| A linha `celsius: ...` dentro de `Args:` | A descrição do parâmetro |
| A dica de tipo `float` | O tipo do parâmetro (`number`) |
| Parâmetro sem valor padrão | Parâmetro obrigatório (`required`) |

**\[Testado\]** Tudo o que está escrito na docstring **antes** da seção `Args:` vira a descrição, inclusive a frase "Use quando o usuário pedir conversão de temperatura". A documentação resume isso dizendo que "o primeiro parágrafo vira a descrição", mas no teste com a versão 1.62.0 os dois parágrafos entraram. A próxima seção mostra por que a descrição pesa tanto.

## A descrição é tudo: uma tool boa e uma ruim

Lembre do cardápio: o modelo escolhe pelo que está escrito na ficha. Esta seção mostra o que acontece quando a descrição falta e como escrever uma boa.

### O que acontece sem docstring

**\[Testado\]** Veja a mesma tool sem nenhum texto explicativo:

```python
@tool
def celsius_para_fahrenheit(celsius: float) -> float:
    return celsius * 9 / 5 + 32
```

A ficha que o Strands monta fica assim:

- **Descrição da tool:** `celsius_para_fahrenheit` (só o nome da função repetido).
- **Descrição do parâmetro:** `Parameter celsius` (uma frase genérica).

O programa roda normalmente, sem aviso de erro. Mas o modelo fica sem nenhuma pista de **quando** usar a tool e do que o valor `celsius` significa. É um erro silencioso, por isso vale conferir a ficha (como na seção anterior).

### Como escrever uma boa descrição

**\[Oficial\]** A documentação lista cinco coisas que uma boa descrição faz:

1. Explica com clareza o propósito da tool.
2. Diz **quando** ela deve ser usada.
3. Detalha os parâmetros que ela aceita e seus formatos.
4. Descreve o formato da saída esperada.
5. Registra limitações ou restrições.

A mesma tool, com uma descrição fraca e com uma boa. O exemplo é nosso; a estrutura é a da documentação:

```python
# Fraca: o modelo não sabe o formato, nem o que vem de volta
@tool
def resumo_vendas(mes: str) -> list:
    """Resumo de vendas."""
    ...

# Boa: cobre as cinco coisas
@tool
def resumo_vendas(mes: str) -> list:
    """Devolve o resumo de vendas de um mês.

    Use quando o usuário pedir números de vendas de um mês específico.

    Args:
        mes: Mês no formato AAAA-MM (ex.: 2026-09)

    Returns:
        Lista com uma linha por produto: nome, unidades e receita.

    Notes:
        - Não inclui devoluções.
    """
    ...
```

(As reticências `...` marcam código omitido neste exemplo.)

Veja como a versão boa responde às cinco coisas:

| O que a descrição precisa dizer | Onde está no exemplo |
| --- | --- |
| Propósito | "Devolve o resumo de vendas de um mês." |
| Quando usar | "Use quando o usuário pedir números de vendas de um mês específico." |
| Parâmetros e formatos | A linha `mes: Mês no formato AAAA-MM (ex.: 2026-09)` |
| Formato da saída | A seção `Returns:` |
| Limitações | A seção `Notes:` (não inclui devoluções) |

**\[Testado\]** O Strands trata a seção `Args:` à parte: cada linha dela vira a descrição de um parâmetro. **Todo o resto da docstring, inclusive `Returns:` e `Notes:`, entra no texto da descrição da tool.** É assim que o modelo fica sabendo o formato da saída e as limitações. Confira rodando `agent.tool_registry.get_all_tools_config()`.

## Nem toda função vira tool

Toda tool é uma função, mas **nem toda função deve virar tool**. Uma tool é uma função que o modelo pode decidir chamar.

**\[Oficial\]** Em Python, uma tool pode nascer de uma função com `@tool`, de um método de classe com `@tool` ou de um módulo com uma especificação escrita à mão. Nos três casos há uma função fazendo o trabalho.

Voltando ao restaurante: a cozinha tem muitas tarefas internas (cortar, temperar, lavar a louça), mas o cardápio lista só os pratos que o cliente pode pedir. No código:

```python
# Funções comuns: o modelo nunca as vê
def _buscar_dados(mes: str) -> list:
    ...

def _formatar(dados: list) -> str:
    ...

# Tool: a única "porta" que o modelo enxerga
@tool
def resumo_vendas(mes: str) -> str:
    """Devolve o resumo de vendas de um mês.

    Use quando o usuário pedir números de vendas.

    Args:
        mes: Mês no formato AAAA-MM (ex.: 2026-09)
    """
    return _formatar(_buscar_dados(mes))
```

(As reticências `...` marcam código omitido. O sublinhado no começo do nome, como em `_buscar_dados`, é uma convenção do Python para dizer "função interna".)

São três funções e uma só tool. O modelo enxerga só `resumo_vendas`.

**\[Recomendação\]** Para decidir o que vira tool, pergunte: "o modelo precisa escolher chamar isto, com base no pedido de alguém?". Se sim, tool. Se é um passo interno de uma tarefa, deixe como função comum. Essa regra é minha, não da documentação.

## O que a tool devolve, e como avisar um erro

Depois que a tool roda, o resultado volta para o agente. Há duas formas de devolvê-lo.

### Forma simples: devolver o valor

**\[Oficial\]** Por padrão, o valor que a função devolve vira uma resposta em texto. **\[Testado\]** Veja o que chegou ao agente em três casos:

| A função devolve | O que o agente recebe (`content`) |
| --- | --- |
| O número `77.0` | `[{'text': '77.0'}]` |
| A lista `[1, 2]` | `[{'text': '[1, 2]'}]` |
| O dicionário `{"a": 1}` | `[{'text': '{"a": 1}'}]` |

Em todos os casos, o resultado vira texto dentro de uma lista, junto com `status: success`.

### Forma controlada: devolver `status` e `content`

**\[Oficial\]** Para controlar o formato, a função devolve um dicionário com dois campos: `status` (`"success"` ou `"error"`) e `content` (uma lista com o texto ou os dados). Isso permite **avisar um erro de forma clara**:

```python
@tool
def dividir(a: float, b: float) -> dict:
    """Divide a por b.

    Args:
        a: Numerador
        b: Denominador (não pode ser zero)
    """
    if b == 0:
        return {"status": "error", "content": [{"text": "Erro: o denominador não pode ser zero"}]}
    return {"status": "success", "content": [{"text": str(a / b)}]}
```

**\[Testado\]** Chamando diretamente:

```
dividir(a=10, b=4)  ->  success [{'text': '2.5'}]
dividir(a=10, b=0)  ->  error   [{'text': 'Erro: o denominador não pode ser zero'}]
```

A mensagem de erro volta para o agente, que pode ler, explicar a quem perguntou ou tentar outra coisa. Por isso, **escreva mensagens de erro que digam o que deu errado e como corrigir**.

### E se o código da tool quebrar?

**\[Testado\]** Se a função der um erro que você não previu (por exemplo, dividir por zero sem a verificação acima), o Strands **não interrompe o programa**. Ele captura o erro e devolve `status: error` com a mensagem:

```
error [{'text': 'Error: ZeroDivisionError - float division by zero'}]
```

O ideal, ainda assim, é tratar os erros que você espera e devolver uma mensagem clara, como no exemplo `dividir`.

A estrutura completa do resultado de uma tool é o assunto do tópico 3 ("Tool result format").

## Tools que lembram: tools dentro de uma classe

Até aqui, cada tool era uma função solta, que não guarda nada de uma chamada para a outra. Mas e se várias tools precisarem **compartilhar algo**, como uma conexão com um banco de dados ou uma chave de acesso? Para isso existem as **classes**.

Uma **classe** é como uma pasta que guarda dados e as funções que usam esses dados. Cada função dentro de uma classe se chama **método**. A informação que a classe guarda é o seu **estado**.

**\[Oficial\]** A documentação indica classes quando as tools compartilham recursos, precisam manter contexto entre chamadas ou precisam ser configuradas antes de ir para o agente.

### Um exemplo para ver o estado funcionando

Um contador simples: guarda um número e a tool soma a ele.

```python
from strands import Agent, tool

class Contador:
    def __init__(self, inicio):
        self.valor = inicio          # o estado: o número guardado

    @tool
    def somar(self, n: int) -> int:
        """Soma n ao valor guardado e devolve o novo valor.

        Args:
            n: Quanto somar
        """
        self.valor += n
        return self.valor

c = Contador(10)                     # cria o contador começando em 10
agent = Agent(tools=[c.somar])       # entrega o método ao agente

print(agent.tool.somar(n=5)["content"])
print(agent.tool.somar(n=5)["content"])
```

**\[Testado\]** A saída é:

```
[{'text': '15'}]
[{'text': '20'}]
```

O segundo resultado é 20 porque a classe **lembrou** do 15 da primeira chamada. Uma função solta não faria isso.

### As peças novas

| Trecho | O que significa |
| --- | --- |
| `class Contador:` | Cria a classe, que é o molde |
| `def __init__(self, inicio):` | A função de partida: roda uma vez, quando você cria um contador, e guarda os dados iniciais |
| `self` | "Este contador específico". É como o método acessa o que a classe guarda (`self.valor`) |
| `Contador(10)` | Cria um contador de verdade, começando em 10 |
| `Agent(tools=[c.somar])` | Entrega o método `somar` ao agente. Note o `c.` na frente |

O parâmetro `self` não aparece na ficha da tool: o modelo só vê o parâmetro `n`.

### O exemplo da documentação

**\[Oficial\]** O exemplo oficial usa uma classe `DatabaseTools`, que guarda uma conexão com um banco de dados e oferece dois métodos como tools (`query_database` e `insert_record`). A ideia é a mesma do contador: a conexão é criada uma vez e compartilhada pelas duas tools. Funciona como uma configuração que não muda entre pedidos, como uma chave de API, a string de conexão com um banco ou o endereço de um serviço.

## Para ir mais fundo (opcional)

Tudo aqui é complemento. Você não precisa de nada disso para criar boas tools; volte quando surgir a necessidade.

### Trocar o nome e a descrição

Por padrão, o nome da tool é o nome da função. Para usar outro, passe-o ao decorator:

```python
@tool(name="obter_clima", description="Retorna o clima de uma cidade")
def f_clima(cidade: str) -> str:
    return f"Sol em {cidade}"
```

**\[Testado\]** Com esse código, `agent.tool_names` devolveu `['obter_clima']`, e a chamada `agent.tool.obter_clima(cidade="Recife")` devolveu `Sol em Recife`. Esse exemplo não tem docstring: o nome e a descrição vieram do decorator.

**\[Oficial\]** A documentação diz que nomes de tool devem usar só letras, números, `_` e `-`, com 1 a 64 caracteres, e que nomes fora desse formato são trocados por `INVALID_TOOL_NAME`. Eu não confirmei se essa regra vale também para Python (ela aparece depois do exemplo em TypeScript).

### Trocar o schema dos parâmetros

O **schema** é a ficha técnica dos parâmetros: nomes, tipos e opções válidas. **\[Oficial\]** Se o schema automático não bastar, você escreve o seu com `@tool(inputSchema=...)`. A documentação mostra, por exemplo, um parâmetro `shape` restrito às opções `circle` e `rectangle`.

### Parâmetro opcional

**\[Testado\]** Um parâmetro com valor padrão vira opcional na ficha:

```python
@tool
def saudacao(nome: str, formal: bool = False) -> str:
    """Cumprimenta uma pessoa pelo nome.

    Args:
        nome: Nome da pessoa
        formal: Se verdadeiro, usa tratamento formal
    """
    return f"Prezado(a) {nome}" if formal else f"Oi, {nome}!"
```

Na ficha, apenas `nome` aparece como obrigatório, e `formal` ganha `default: false`. As chamadas `saudacao(nome="Jé")` e `saudacao(nome="Jé", formal=True)` devolveram `Oi, Jé!` e `Prezado(a) Jé`.

### Escrever a ficha à mão: módulo com `TOOL_SPEC`

**\[Oficial\]** A terceira forma de criar uma tool. Em vez do decorator, você escreve a ficha como um dicionário chamado `TOOL_SPEC` e uma função com o mesmo nome da tool, em um arquivo `weather_forecast.py`. É útil quando você quer mais controle ou não quer depender do Strands na definição.

```python
from typing import Any

TOOL_SPEC = {
    "name": "weather_forecast",
    "description": "Get weather forecast for a city.",
    "inputSchema": {
        "json": {
            "type": "object",
            "properties": {
                "city": {"type": "string", "description": "The name of the city"},
                "days": {"type": "integer", "description": "Number of days for the forecast", "default": 3},
            },
            "required": ["city"],
        }
    },
}

def weather_forecast(tool, **kwargs: Any):
    tool_use_id = tool["toolUseId"]
    tool_input = tool["input"]
    city = tool_input.get("city", "")
    days = tool_input.get("days", 3)
    result = f"Weather forecast for {city} for the next {days} days..."
    return {"toolUseId": tool_use_id, "status": "success", "content": [{"text": result}]}
```

Para usar, importe o módulo e passe-o ao agente: `import weather_forecast` e `Agent(tools=[weather_forecast])`. Também dá para passar o caminho do arquivo: `Agent(tools=["./weather_forecast.py"])`.

**\[Testado\]** Com o módulo importado, `agent.tool_names` devolveu `['weather_forecast']`, e a chamada `agent.tool.weather_forecast(city="Lisboa", days=2)` devolveu `Weather forecast for Lisboa for the next 2 days...`. Repare que aqui o resultado precisa ser montado à mão, com `toolUseId`, `status` e `content`.

### Funções assíncronas e resultados parciais

Uma função **assíncrona** (`async def`) não trava tudo enquanto espera algo lento, como uma consulta a uma API. **\[Oficial\]** O Strands chama todas as tools assíncronas de forma concorrente, isto é, ao mesmo tempo. Elas também podem enviar resultados parciais com `yield`: cada valor enviado vira um evento de *streaming*, e o último é o resultado final. Não testei este recurso.

### O "crachá" da chamada: ToolContext

**\[Oficial\]** Com `@tool(context=True)` e um parâmetro `tool_context: ToolContext`, a tool consegue acessar o agente que a chamou e os dados da chamada atual.

```python
from strands import tool, Agent, ToolContext

@tool(context=True)
def meu_nome(tool_context: ToolContext) -> str:
    """Diz o nome do agente."""
    return f"O agente se chama {tool_context.agent.name}"

agent = Agent(tools=[meu_nome], name="Agente Teste")
```

**\[Testado\]** `agent.tool.meu_nome()` devolveu `O agente se chama Agente Teste`.

**\[Oficial\]** O `ToolContext` também dá acesso ao `invocation_state`: dados que você passa ao chamar o agente, como `agent("Pegue meu perfil", invocation_state={"user_id": "user123"})`. A tool os lê em `tool_context.invocation_state`, sem que eles apareçam nos prompts. Não testei esse trecho.

### Onde colocar cada tipo de informação

**\[Oficial\]** Segundo a documentação:

| Tipo de informação | Onde fica | Exemplo |
| --- | --- | --- |
| Dado que o modelo decide com base no pedido | Parâmetro da tool | Consulta de busca, caminho de arquivo, entradas de um cálculo |
| Contexto da requisição que não deve aparecer nos prompts e muda a cada chamada | `invocation_state` | ID do usuário, ID de sessão |
| Configuração que não muda entre requisições e exige inicialização | Tool em classe | Chave de API, conexão com banco, endereço de serviço |

## Segurança: cinco princípios para tools

Lembre da analogia da chave: anexar uma tool é dar à assistente acesso ao que o seu programa acessa. **\[Oficial\]** A documentação avisa que toda tool, seja sua, da comunidade ou do pacote de tools do Strands, executa código em nome do agente **com as permissões do programa que hospeda o agente**, e recomenda conferir o que cada tool faz (acesso a arquivos, chamadas pela internet, comandos no sistema).

**\[Oficial\]** A página de IA responsável do Strands lista cinco princípios de design, ilustrados com uma tool que lê arquivos de texto só em pastas permitidas:

| Princípio | Em linguagem simples | Exemplo |
| --- | --- | --- |
| 1. Privilégio mínimo | A tool recebe só a permissão de que precisa | Uma tool que lê arquivos enxerga apenas uma pasta específica, não o computador inteiro |
| 2. Validação de entradas | Conferir o que chegou antes de usar | Checar se o caminho recebido está dentro das pastas permitidas |
| 3. Documentação clara | Descrever propósito, limitações e entradas esperadas | A docstring da tool |
| 4. Tratamento de erros | Lidar com casos inesperados e devolver uma mensagem útil | Arquivo inexistente: devolver um aviso claro em vez de quebrar |
| 5. Log de auditoria | Anotar operações sensíveis para revisão posterior | Registrar a tentativa de acessar uma pasta proibida |

O princípio 3 é o que você já viu na seção sobre descrição, e o 4 é o que você viu na seção sobre erros.

### O que o Strands confere sozinho

**\[Testado\]** Chamar uma tool sem um parâmetro obrigatório devolveu `status: error` com uma mensagem de validação, em vez de interromper o programa. Ou seja, o Strands confere ao menos se os parâmetros obrigatórios chegaram. As regras do seu negócio (como "só esta pasta") continuam sendo responsabilidade da tool.

Para a questão de **quem escreveu o código** e da pasta `./tools/`, veja a seção de segurança do tópico 1.

## Recomendações práticas (não oficiais)

**\[Recomendação\]** São boas práticas gerais para tools de agentes, sugeridas por mim. Não constam nas páginas oficiais do Strands que li. Trate como opinião e ajuste ao seu caso.

| Prática | Exemplo | Por quê |
| --- | --- | --- |
| **Uma tarefa clara por tool** | Em vez de `gerenciar_vendas` (consulta, edita, apaga), três tools: `consultar_vendas`, `editar_venda`, `apagar_venda` | Se você não consegue descrever a tool em uma frase, ela provavelmente faz coisa demais |
| **Poucos parâmetros, com nomes que se explicam** | `mes` em vez de `p1` | Quanto mais simples a entrada, menor a chance de o modelo preenchê-la errado |
| **Sem tools que façam quase a mesma coisa** | Duas tools de busca com descrições parecidas | O modelo hesita entre elas. Junte-as ou diferencie as descrições ("use esta quando... use aquela quando...") |
| **Funções auxiliares ficam como funções comuns** | `_formatar`, `_buscar_dados` sem `@tool` | O modelo só precisa enxergar o que ele decide chamar |
| **Diga unidades e formatos no parâmetro** | "Taxa em decimal (0.1075), não em percentual (10.75)" | Evita um erro de escala que passa sem aviso |

**Em duas frases:** cada tool deve fazer uma coisa, ter um nome que diga o que é e uma descrição que diga quando usar. Se algo não couber nisso, provavelmente são duas tools.

## Exercício guiado

Tempo estimado: 20 minutos. Você precisa ter feito a preparação do computador (tópico 1). As partes 1 a 3 não exigem modelo de IA nem chave de acesso.

**\[Testado\]** O código e as saídas abaixo foram executados do jeito que estão, com `strands-agents` 1.62.0.

### Parte 1: criar duas tools e conferir tudo

Salve como `exercicio_t2.py` e rode com `python exercicio_t2.py`:

```python
from strands import Agent, tool


@tool
def celsius_para_fahrenheit(celsius: float) -> float:
    """Converte uma temperatura de graus Celsius para Fahrenheit.

    Use quando o usuário pedir conversão de temperatura.

    Args:
        celsius: Temperatura em graus Celsius
    """
    return celsius * 9 / 5 + 32


@tool
def dividir(a: float, b: float) -> dict:
    """Divide a por b.

    Args:
        a: Numerador
        b: Denominador (não pode ser zero)
    """
    if b == 0:
        return {"status": "error", "content": [{"text": "Erro: o denominador não pode ser zero"}]}
    return {"status": "success", "content": [{"text": str(a / b)}]}


agent = Agent(tools=[celsius_para_fahrenheit, dividir])

# Passo 1: quais tools o agente tem
print("1:", agent.tool_names)

# Passo 2: a ficha que o modelo lê
ficha = agent.tool_registry.get_all_tools_config()["celsius_para_fahrenheit"]
print("2a:", ficha["description"])
print("2b:", ficha["inputSchema"]["json"]["properties"]["celsius"]["description"])

# Passo 3: chamada direta
r = agent.tool.celsius_para_fahrenheit(celsius=25)
print("3:", r["status"], r["content"])

# Passo 4: erro, valor sem nome
r = agent.tool.celsius_para_fahrenheit(25)
print("4:", r["status"])

# Passo 5: tool que avisa o próprio erro
r = agent.tool.dividir(a=10, b=4)
print("5a:", r["status"], r["content"])
r = agent.tool.dividir(a=10, b=0)
print("5b:", r["status"], r["content"])

# Passo 6: nome que não existe (o programa para aqui)
agent.tool.nao_existe(x=1)
```

Saída esperada (depois da linha do `AttributeError` aparecem mais linhas de texto sobre o erro, que você pode ignorar):

```
1: ['celsius_para_fahrenheit', 'dividir']
2a: Converte uma temperatura de graus Celsius para Fahrenheit.

Use quando o usuário pedir conversão de temperatura.
2b: Temperatura em graus Celsius
3: success [{'text': '77.0'}]
4: error
5a: success [{'text': '2.5'}]
5b: error [{'text': 'Erro: o denominador não pode ser zero'}]
AttributeError: Tool 'nao_existe' not found
```

**O que observar:**

- **Passos 1 e 2:** a descrição da ficha vem da docstring, e a explicação do parâmetro vem da linha dentro de `Args:`.
- **Passo 4:** o valor sem nome não derruba o programa. O erro chega como `status` igual a `error`.
- **Passo 5:** a segunda chamada devolve o erro que **você** escreveu, com `status: error`. É assim que uma tool avisa o agente de um problema.
- **Passo 6:** o programa para, com a mensagem `Tool 'nao_existe' not found`. Isso é esperado.

### Parte 2: experimento: tire a docstring

Apague as linhas da docstring de `celsius_para_fahrenheit` (tudo entre as aspas triplas, inclusive as aspas), salve e rode de novo. **\[Testado\]** O passo 2 passa a mostrar a descrição igual ao nome da função (`celsius_para_fahrenheit`) e o parâmetro com a descrição genérica `Parameter celsius`. O programa continua rodando, sem aviso de erro. Isso mostra, na prática, por que a docstring importa: sem ela, o modelo não teria pistas.

### Parte 3: desafio: crie a sua tool

Crie uma tool `quilometros_para_milhas` que converte quilômetros em milhas (1 quilômetro é aproximadamente 0.621371 milha), com uma boa descrição e o parâmetro explicado em `Args:`. Teste com 10 quilômetros: o esperado é `6.21371`.

Se quiser conferir com uma resposta, aqui está uma:

```python
@tool
def quilometros_para_milhas(km: float) -> float:
    """Converte uma distância de quilômetros para milhas.

    Use quando o usuário pedir conversão de distância.

    Args:
        km: Distância em quilômetros
    """
    return km * 0.621371

agent = Agent(tools=[quilometros_para_milhas])
print(agent.tool.quilometros_para_milhas(km=10)["content"])
```

**\[Testado\]** A saída dessa resposta é `[{'text': '6.21371'}]`.

### Parte 4: usar com o agente de verdade (não testada aqui)

Com um provedor de modelo configurado, acrescente `agent("Quanto são 25 graus Celsius em Fahrenheit?")` e veja se o agente escolhe a tool sozinho. A configuração do provedor está explicada no tópico 1.

## Glossário

| Termo | Em linguagem simples |
| --- | --- |
| Agente (`Agent`) | A "assistente" inteira: modelo, caixa de ferramentas e memória da conversa |
| Modelo | A IA que lê o pedido e decide o que fazer. Só escreve texto |
| Tool | Uma função que o agente pode decidir chamar |
| Ficha da tool | O nome, a descrição e a explicação dos parâmetros. É tudo o que o modelo enxerga |
| Função (`def`) | Uma receita com nome: recebe informações, faz algo e devolve um resultado |
| Parâmetro | Uma informação que a função (ou a tool) recebe |
| `return` | A palavra que marca o que a função devolve |
| Dicas de tipo (*type hints*) | A indicação do tipo de cada dado: `int` (inteiro), `float` (número com casas decimais), `str` (texto), `bool` (verdadeiro ou falso) |
| Docstring | O texto entre aspas triplas logo abaixo do nome da função. Para o Strands, é a descrição que o modelo lê |
| `Args:` | A seção da docstring que explica cada parâmetro, no formato `nome: explicação` |
| Decorator (`@tool`) | Uma etiqueta colada acima de uma função para dar a ela um poder extra; aqui, o de virar tool |
| Dicionário | Uma lista de pares "nome: valor" entre chaves, como `{"status": "success"}` |
| `status` e `content` | Os dois campos de um resultado controlado: se deu certo ou errado, e o conteúdo |
| Classe | Uma "pasta" que guarda dados e as funções que usam esses dados |
| Método | Uma função que está dentro de uma classe |
| Estado | A informação que a classe (ou a tool) guarda de uma chamada para a outra |
| `self` | "Este objeto específico": como um método acessa o que a classe guarda |
| Schema | A ficha técnica dos parâmetros de uma tool: nomes, tipos e opções válidas |
| Módulo | Um arquivo Python que pode ser importado por outro |
| Assíncrona (`async`) | Função que não trava tudo enquanto espera algo lento, como uma API |
| Concorrente | Várias coisas andando ao mesmo tempo |
| Streaming | Receber resultados parciais enquanto a tool ainda trabalha |
| `ToolContext` | Um "crachá" opcional que dá à tool acesso ao agente e aos dados da chamada atual |
| `invocation_state` | Dados que você passa ao chamar o agente e que a tool lê sem que apareçam nos prompts |
| Exceção | Um erro que interrompe o programa, como o `AttributeError` |

## Fontes e o que não foi verificado

Consultado em 27/10/2026.

### Páginas oficiais lidas na íntegra

- [Create custom tools](https://strandsagents.com/docs/user-guide/sdk/tools/custom-tools/): base das seções sobre formas de criar tools, opções do decorator e descrições eficazes.
- [Responsible AI](https://strandsagents.com/docs/user-guide/safety-security/responsible-ai/): base dos cinco princípios de design.
- [Add tools to your agent](https://strandsagents.com/docs/user-guide/sdk/tools/): base do aviso de segurança e da visão geral.

### Páginas oficiais vistas apenas em trechos

- [Attach and invoke tools](https://strandsagents.com/docs/user-guide/sdk/tools/using-tools/)
- [Python Quickstart](https://strandsagents.com/docs/user-guide/sdk/quickstart/python/): origem do requisito de Python 3.10 ou superior e da instalação com `pip install strands-agents`.

### O que não foi verificado

- A regra de formato dos nomes de tool (letras, números, `_` e `-`, de 1 a 64 caracteres) aparece na página oficial logo após o exemplo em TypeScript. Presumi que vale também para Python, sem confirmar.
- A documentação diz que o primeiro parágrafo da docstring vira a descrição. No teste com a versão 1.62.0, todo o texto antes de `Args:` entrou, inclusive `Returns:` e `Notes:`. Se a sua versão for outra, confira com `get_all_tools_config()`.
- Os testes rodaram só na versão 1.62.0. Em outras versões o comportamento pode diferir; documentações antigas, por exemplo, usam `agent.tool_config` e `strands_tools`.
- Testei com exemplos meus: tool com `@tool`, parâmetro opcional, retorno com `status` e `content`, tool dentro de uma classe (um contador), módulo com `TOOL_SPEC`, `@tool(name=..., description=...)` e `@tool(context=True)`. O exemplo `DatabaseTools` da documentação não foi executado.
- Não testei `@tool(inputSchema=...)`, funções assíncronas com `yield` (streaming) nem o uso de `invocation_state`. Esses trechos seguem a documentação.
- A Parte 4 do exercício (pedido em linguagem natural) não foi executada, pois exige um modelo configurado.
- A página "Tool result format" ainda não foi lida; ela é o assunto do tópico 3.
