# Strands Agents — Tópico 1: anexar e invocar tools

Oct 27, 2026 · @Jéssica Coelho

## Resumo

Este documento ensina duas coisas: como entregar uma tool a um agente (**anexar**) e como fazer essa tool rodar (**invocar**). Você não precisa saber programar para acompanhar. Cada termo técnico é explicado na primeira vez em que aparece, e no fim há um glossário.

**Como ler:**

- Se tiver pouco tempo, leia só as quatro primeiras seções depois deste resumo. Elas trazem o essencial e um exemplo completo.
- A seção "Para ir mais fundo" é opcional. Pule sem culpa e volte quando quiser.
- O exercício no final é para você rodar no seu computador. Ele leva uns 15 minutos.

**As marcas de origem.** Para você saber em quem confiar, algumas frases começam com uma etiqueta:

- **\[Oficial\]**: está na documentação do Strands Agents.
- **\[Testado\]**: eu rodei o código com `strands-agents` versão 1.62.0 e vi o resultado.
- **\[Recomendação\]**: é um conselho meu, sem fonte oficial. Trate como opinião.

## Três palavras antes de tudo

O Strands Agents é um conjunto de peças prontas, escritas em Python (uma linguagem de programação), para montar agentes de IA. Três palavras aparecem o tempo todo: agente, modelo e tool.

Imagine uma assistente de escritório que recebe pedidos e resolve.

| Palavra | Na analogia | No Strands |
| --- | --- | --- |
| **Modelo** | O cérebro da assistente: lê o pedido e decide o que fazer | A IA (por exemplo, o Claude). Ela só lê e escreve texto |
| **Tool** (ferramenta) | Uma ferramenta que ela sabe usar: calculadora, agenda, sistema da empresa | Uma função em Python, isto é, um pequeno trecho de código que faz uma coisa só |
| **Agente** | A assistente inteira: cérebro, mais a caixa de ferramentas, mais a memória da conversa | O objeto `Agent` do Strands, que junta o modelo, as tools e o histórico |

Uma consequência importante: o modelo **não executa nada sozinho**. Ele só escreve texto. Quando precisa de uma tool, ele escreve um pedido do tipo "chame a ferramenta X com estes valores", e quem executa de verdade é o Strands, no seu computador ou servidor.

Este documento trata de duas ações:

1. **Anexar**: colocar ferramentas na caixa do agente.
2. **Invocar**: fazer uma ferramenta da caixa rodar.

A documentação oficial do Strands organiza o tema nestas mesmas etapas: passar as tools ao agente, ver o que foi carregado e invocá-las.

## Preparar o computador

Para rodar os exemplos, você precisa de Python e do pacote do Strands. Um **pacote** é um conjunto de código pronto que você baixa e usa nos seus programas. Os comandos abaixo são digitados no **terminal**, a janela onde você escreve instruções em texto para o computador (no Windows, o "Prompt de Comando" ou o "PowerShell").

**\[Oficial\]** O guia de início rápido do Strands pede Python 3.10 ou superior.

### Passo 1: conferir se o Python está instalado

```bash
python --version
```

Se aparecer algo como `Python 3.12.4`, está certo (o número precisa ser 3.10 ou maior). Em alguns computadores o comando é `python3 --version`. Se der erro, instale o Python em python.org antes de seguir.

### Passo 2: criar um ambiente virtual (recomendado)

Um **ambiente virtual** é uma pasta isolada para os pacotes deste projeto, como uma bancada separada: o que você instala nela não bagunça o resto do computador. **\[Recomendação\]** É um hábito comum entre quem programa, mas não é obrigatório.

```bash
python -m venv .venv
```

Depois, ative o ambiente:

- Mac ou Linux: `source .venv/bin/activate`
- Windows: `.venv\Scripts\activate`

Quando funciona, o terminal passa a mostrar `(.venv)` no começo da linha.

### Passo 3: instalar o Strands

```bash
pip install strands-agents
```

O `pip` é o instalador de pacotes do Python. Atenção ao nome: **instala-se `strands-agents`, mas no código escreve-se `strands`** (por exemplo, `from strands import Agent`). **\[Testado\]** No catálogo oficial de pacotes do Python (PyPI), `pip install strands` instala outra coisa, uma biblioteca de matemática sem relação com agentes.

### Passo 4: ter um arquivo para rodar

Um programa em Python é um arquivo de texto com final `.py`. Você cria o arquivo em qualquer editor de texto (o Bloco de Notas serve), salva, e roda no terminal, na mesma pasta do arquivo:

```bash
python nome_do_arquivo.py
```

Se você já trabalha em um ambiente com Python pronto, como um notebook, pode usar ele: basta colar o código numa célula.

### E o modelo de IA?

As partes deste documento marcadas como **\[Testado\]** rodam **sem** modelo e sem senha nenhuma, porque só mexem nas tools. A única parte que precisa de um **provedor de modelo** configurado (o serviço que fornece a IA, como Amazon Bedrock ou Anthropic, com sua chave de acesso) é pedir algo ao agente em linguagem natural. Ela vem avisada na hora.

## Seu primeiro agente: criar uma tool e anexar

Vamos usar um exemplo pequeno e útil: converter temperatura de Celsius para Fahrenheit. Salve o código abaixo em um arquivo chamado `primeiro_agente.py`:

```python
from strands import Agent, tool

@tool
def celsius_para_fahrenheit(celsius: float) -> float:
    """Converte uma temperatura de graus Celsius para Fahrenheit.

    Args:
        celsius: Temperatura em graus Celsius
    """
    return celsius * 9 / 5 + 32

agent = Agent(tools=[celsius_para_fahrenheit])

print(agent.tool_names)
```

Rode com `python primeiro_agente.py`. **\[Testado\]** A saída é:

```
['celsius_para_fahrenheit']
```

Essa lista é a caixa de ferramentas do agente: ele agora tem uma tool.

### O que cada parte faz

| Trecho | Em linguagem simples |
| --- | --- |
| `from strands import Agent, tool` | Pega duas peças do Strands: o `Agent` (a assistente) e o `tool` (uma etiqueta, explicada a seguir) |
| `@tool` | A etiqueta que transforma a função logo abaixo em uma tool que o agente reconhece |
| `def celsius_para_fahrenheit(...)` | A função em si: recebe um número e devolve outro |
| O texto entre aspas triplas | A **ficha da ferramenta**: o que ela faz e o que cada valor significa. O modelo lê essa ficha para decidir se e como usar a tool |
| `Agent(tools=[...])` | **Anexar**: cria o agente já com a caixa de ferramentas. A lista pode ter quantas tools você quiser |
| `agent.tool_names` | Pergunta ao agente quais tools ele tem |

Como criar tools boas é o assunto do tópico 2. Aqui o que importa é: **a ficha escrita por você é o que o modelo enxerga**. Ele nunca lê o código da função.

### Ver a ficha que o modelo recebe

**\[Oficial\]** O agente guarda essa ficha em `agent.tool_registry.get_all_tools_config()` (o "registro de tools" é a lista interna onde ele guarda as tools anexadas). Acrescente ao arquivo:

```python
print(agent.tool_registry.get_all_tools_config())
```

**\[Testado\]** O resultado, reformatado para leitura:

```
{'celsius_para_fahrenheit': {
    'name': 'celsius_para_fahrenheit',
    'description': 'Converte uma temperatura de graus Celsius para Fahrenheit.',
    'inputSchema': {'json': {
        'properties': {'celsius': {
            'description': 'Temperatura em graus Celsius',
            'type': 'number'}},
        'required': ['celsius'],
        'type': 'object'}}}}
```

Repare que o nome, a descrição e a explicação do valor `celsius` saem direto do que você escreveu na função.

## Usar a tool: duas formas de invocar

Com a tool anexada, há dois jeitos de fazê-la rodar. Voltando à analogia da assistente:

1. **Pedir um resultado.** Você diz "quanto é 25 °C em Fahrenheit?" e a assistente escolhe sozinha qual ferramenta usar. É a **invocação em linguagem natural**.
2. **Pegar a ferramenta você mesma.** Você abre a caixa e usa a calculadora direto, sem pedir a ninguém. É a **chamada direta**.

### Forma 1: pedir em linguagem natural

**\[Oficial\]** O agente decide quando e como usar as tools com base no seu pedido. Você não diz qual tool usar nem com quais valores.

```python
agent("Quanto é 25 graus Celsius em Fahrenheit?")
```

O que acontece por trás (uma explicação minha, não uma citação da documentação):

1. O modelo lê o seu pedido e as fichas das tools anexadas.
2. Ele percebe que a tool de conversão ajuda e escreve um pedido: "chame `celsius_para_fahrenheit` com `celsius` igual a 25".
3. O Strands executa a função de verdade e devolve o resultado ao modelo.
4. O modelo escreve a resposta final, algo como "25 °C equivalem a 77 °F".

**Não testado aqui.** Esta forma precisa de um provedor de modelo configurado (veja "Preparar o computador"), e eu não configurei nenhum no ambiente de teste. Por isso o código desta forma não foi executado.

### Forma 2: chamada direta

**\[Oficial\]** Toda tool anexada vira um método de `agent.tool`. Você escolhe a tool e os valores, e ela roda sem o modelo decidir nada:

```python
resultado = agent.tool.celsius_para_fahrenheit(celsius=25)
print(resultado["status"], resultado["content"])
```

**\[Testado\]** A saída é:

```
success [{'text': '77.0'}]
```

**\[Testado\]** Essa chamada funcionou sem nenhum provedor de modelo configurado. A chamada direta não depende do modelo.

### Duas regras da chamada direta

- **Escreva sempre o nome do valor.** Escreva `celsius=25`, e não só `25`. Isso se chama *argumento nomeado*. **\[Oficial\]** A documentação diz que o formato sem nome (*argumento posicional*) não é suportado.
- **Hífen vira sublinhado.** **\[Oficial\]** Uma tool registrada como `ler-tudo` é chamada como `agent.tool.ler_tudo(...)`, porque o hífen não é aceito em nomes no Python.

### O que volta de uma tool

**\[Testado\]** O resultado é um *dicionário*, isto é, uma lista de pares "nome: valor". Ele traz três campos:

| Campo | O que é |
| --- | --- |
| `status` | `success` se deu certo, `error` se deu errado |
| `content` | A resposta em si: uma lista com o texto ou os dados |
| `toolUseId` | Um número de identificação da chamada (você raramente precisa dele) |

Por isso o exemplo mostra `resultado["content"]` e não só `77.0`. O formato completo é o assunto do tópico 3.

## Quando algo dá errado

Errar faz parte, e vale ver como o erro aparece. Na chamada direta, há dois casos comuns, e eles se comportam de jeitos diferentes. **\[Testado\]** Ambos foram executados com `strands-agents` 1.62.0.

### Caso 1: esquecer o nome do valor

```python
r = agent.tool.celsius_para_fahrenheit(25)   # faltou escrever celsius=
print(r["status"])
print(r["content"])
```

O programa **não para**. O erro chega dentro do resultado:

```
error
[{'text': 'Error: Validation failed for input parameters: 1 validation error for Celsius_para_fahrenheitTool\ncelsius\n  Field required [...]'}]
```

"Field required" quer dizer "o campo `celsius` é obrigatório e não chegou". Como o programa segue em frente, **confira o `status`** depois de uma chamada direta, em vez de supor que deu certo.

### Caso 2: errar o nome da tool

```python
agent.tool.nao_existe(x=1)
```

Aqui o programa **para** com uma *exceção* (um erro que interrompe tudo):

```
AttributeError: Tool 'nao_existe' not found
```

Leia como "não achei nenhuma tool com esse nome". Confira a grafia com `agent.tool_names`.

### Resumo dos dois casos

| Situação | O que acontece | Como notar |
| --- | --- | --- |
| Valor sem nome (`celsius_para_fahrenheit(25)`) | O programa continua | `status` vem como `error` |
| Tool que não existe (`nao_existe(...)`) | O programa pára | Mensagem `AttributeError` na tela |

**\[Oficial\]** A documentação afirma que valores sem nome geram erro. O teste mostrou que esse erro vem como `status: error` e não como exceção.

## Quando usar cada forma

**\[Recomendação\]** São critérios sugeridos por mim, não regras da documentação.

| Situação | Forma sugerida | Por quê |
| --- | --- | --- |
| Quem usa descreve o que quer e o agente deve escolher o caminho | Linguagem natural | É para isso que o agente existe: decidir qual tool usar e com quais valores |
| Testar uma tool que você acabou de criar | Chamada direta | Você controla os valores e vê o resultado sem depender da decisão do modelo |
| Entender por que o agente errou | Chamada direta | Repete a tool com os mesmos valores e mostra se o problema está na tool ou na escolha do modelo |
| Uma etapa fixa do seu programa, que sempre acontece | Chamada direta | Não há decisão a tomar, e você não gasta uma chamada ao modelo à toa |

**Dica prática para quem está começando:** crie a tool e teste primeiro com a chamada direta. Ela funciona sem modelo, é rápida e deixa claro se o problema, caso exista, está na tool. Só depois peça pela linguagem natural.

## Para ir mais fundo (opcional)

Tudo o que vem aqui é complemento. Você pode pular e voltar quando precisar.

### Outras formas de anexar tools

Além de passar a lista na criação do agente, há outras maneiras. **\[Oficial\]**

| Forma | Como fica | Observação |
| --- | --- | --- |
| Objetos importados | `Agent(tools=[minha_tool, outra_tool])` | A mais comum. Serve para tools prontas e para as suas |
| Caminho de arquivo | `Agent(tools=["/caminho/minha_tool.py"])` | O Strands carrega o arquivo Python indicado |
| Pasta `./tools/` | `Agent(load_tools_from_directory=True)` | Desligada por padrão. Carrega e recarrega sozinha as tools da pasta. Veja a seção de segurança |

**Adicionar depois de criar o agente.** **\[Oficial\]** A documentação diz que as tools podem ser passadas na criação ou adicionadas depois, mas o guia não mostra o código. **\[Testado\]** Este funcionou na versão 1.62.0:

```python
agent.tool_registry.process_tools([dobro])
print(agent.tool_names)   # ['celsius_para_fahrenheit', 'dobro']
```

Esse método aparece na referência técnica da API do Strands, não no guia, então pode mudar entre versões.

**Tools prontas.** O Strands traz *vended tools*, tools que já vêm com o pacote para tarefas comuns, como arquivos, requisições HTTP, notebooks e comandos de shell (segundo a visão geral da documentação; não li a página que lista todas).

### O histórico da conversa

O agente tem um **caderno de anotações** onde registra tudo o que aconteceu na conversa: o que foi pedido, quais tools rodaram e quais foram os resultados. Esse caderno é o **histórico**, e é a memória do agente. Em cada nova pergunta, o modelo lê o caderno para saber o que já foi feito.

**\[Oficial\]** Por padrão, uma chamada direta também é anotada no caderno, como se o agente mesmo tivesse usado a tool. Isso tem uma consequência prática: se você chama a tool direto e depois faz uma pergunta em linguagem natural, o agente já "sabe" o resultado daquela chamada.

**O comando que a documentação indica.** Se você quer usar a tool **sem anotar no caderno**, acrescente `record_direct_tool_call=False` à chamada:

```python
# Anota no caderno (o comportamento normal)
agent.tool.celsius_para_fahrenheit(celsius=0)

# Roda a tool, mas NÃO anota no caderno
agent.tool.celsius_para_fahrenheit(celsius=0, record_direct_tool_call=False)
```

O resultado volta igual nos dois casos. A única diferença é se o agente vai se "lembrar" da chamada depois. Isso serve, por exemplo, para chamadas de preparação ou teste, que não devem influenciar as respostas seguintes.

**\[Testado\]** Para ver o caderno, use `agent.messages`, a lista de mensagens guardadas. `len(agent.messages)` conta quantas há. Para comparar, rode o código abaixo em um arquivo novo, com um agente recém-criado:

```python
agent = Agent(tools=[celsius_para_fahrenheit])
print(len(agent.messages))   # print 1: agente novo

agent.tool.celsius_para_fahrenheit(celsius=0)
print(len(agent.messages))   # print 2: depois da chamada normal

agent.tool.celsius_para_fahrenheit(celsius=0, record_direct_tool_call=False)
print(len(agent.messages))   # print 3: depois da chamada sem anotar

agent.tool.celsius_para_fahrenheit(celsius=0)
print(len(agent.messages))   # print 4: depois de outra chamada normal
```

(Antes disso, o arquivo precisa ter a definição da tool `celsius_para_fahrenheit`, como nos exemplos anteriores.) A saída é:

```
0
4
4
8
```

| Print | Momento | Mensagens no caderno |
| --- | --- | --- |
| 1 | Agente recém-criado | 0 |
| 2 | Depois de uma chamada normal | 4 |
| 3 | Depois de uma chamada com `record_direct_tool_call=False` | 4 (**não mudou**: nada foi anotado) |
| 4 | Depois de outra chamada normal | 8 |

**O que importa é o print 3.** Se o número não sobe, o comando funcionou. Ver o mesmo número duas vezes seguidas (4 e 4) é o resultado certo, e não um defeito. Se o seu arquivo já tem chamadas diretas anteriores, a contagem não começa em 0, porque elas também foram anotadas.

As 4 mensagens de uma chamada anotada são: o aviso de chamada direta com os valores, o pedido da tool, o resultado e uma frase final. O número exato por chamada é um detalhe interno e pode mudar entre versões. Nos exercícios, o contador começa em 4 e não em 0 porque o Passo 2 já fez uma chamada normal antes da contagem.

### Várias tools ao mesmo tempo: executores

Quando o modelo pede mais de uma tool na mesma resposta, um **executor** decide se elas rodam ao mesmo tempo ou uma de cada vez. **\[Oficial\]** O Strands traz dois:

| Executor | Comportamento | Quando serve |
| --- | --- | --- |
| `ConcurrentToolExecutor` (o padrão) | As tools rodam ao mesmo tempo | Tools independentes, como consultar o clima e a hora de uma cidade |
| `SequentialToolExecutor` | Uma depois da outra, na ordem pedida | Quando uma depende da anterior, como tirar uma captura de tela e só depois enviá-la por e-mail |

Para usar o sequencial, passe-o na criação do agente (exemplo adaptado da documentação; `screenshot_tool` e `email_tool` precisariam existir no seu código):

```python
from strands import Agent
from strands.tools.executors import SequentialToolExecutor

agent = Agent(
    tool_executor=SequentialToolExecutor(),
    tools=[screenshot_tool, email_tool],
)
```

**\[Testado\]** Na versão 1.62.0, esse parâmetro foi aceito, e um agente criado sem ele usou o `ConcurrentToolExecutor`.

Três observações da documentação:

- Rodar ao mesmo tempo só acontece se o modelo pedir várias tools numa única resposta. Se pedir uma por vez, elas rodam em fila mesmo com o executor concorrente.
- Alguns provedores de modelo têm configuração própria para permitir ou forçar o uso paralelo de tools.
- Executores personalizados ainda não são suportados, segundo a página (acompanhamento na GitHub Issue #762).

## Segurança: de onde vem o código das tools

Uma tool é um programa que o agente roda. Por isso, antes de anexar uma, vale perguntar: **quem escreveu este código e o que ele consegue fazer?**

### A analogia da chave

Anexar uma tool é como entregar a chave do escritório a uma assistente: ela entra em todo lugar onde você entraria. **\[Oficial\]** A documentação avisa que toda tool, seja sua, da comunidade ou do pacote de tools do Strands, executa código em nome do agente **com as mesmas permissões do programa que hospeda o agente**.

Na prática: se o seu programa consegue ler uma pasta de relatórios, apagar arquivos ou abrir o banco de dados, qualquer tool anexada também consegue.

### O problema: a ficha não mostra o que o código faz

Lembre que o modelo só lê a **ficha** da tool (nome, descrição, valores). Ele não lê o código. Veja uma tool que, pela ficha, é inocente:

```python
@tool
def somar(a: int, b: int) -> int:
    """Soma dois números."""
    # ...aqui poderia haver código extra que a ficha não menciona,
    # como ler arquivos ou enviar dados pela internet...
    return a + b
```

A ficha diz "soma dois números", e o resultado aparece certo. Mas só quem lê o código sabe o que mais ele faz. Esse é o motivo de a documentação pedir que você mesma confira o que cada tool faz.

### Quatro perguntas antes de anexar uma tool

| Pergunta | Por que importa |
| --- | --- |
| Quem escreveu esta tool? | Código de fonte desconhecida merece mais cuidado que código do seu time |
| Eu li o código? | É a única forma de saber o que ele acessa: arquivos, internet, comandos no sistema |
| Ela precisa mesmo de tudo isso? | Uma tool de conversão de temperatura não precisa de acesso à internet. Quanto menos ela pode, menor o estrago se algo der errado |
| O que acontece com valores estranhos? | Uma tool deve recusar entradas inválidas em vez de executá-las |

**\[Oficial\]** A documentação de segurança do Strands cita, entre seus princípios, o **privilégio mínimo** (dar só as permissões necessárias) e a **validação de entradas**. Elas correspondem à terceira e à quarta pergunta.

### A pasta `./tools/` é o ponto mais delicado

Lembra da terceira forma de anexar, `load_tools_from_directory=True`? Pense numa caixa de correio na porta do escritório: qualquer papel deixado ali, a assistente lê e executa o que estiver escrito, sem você ver.

- **\[Oficial\]** Todo arquivo Python colocado na pasta `./tools/` é executado pelo agente. É você quem garante que só entra código seguro e confiável ali.
- **\[Oficial\]** A opção vem desligada por padrão. Ligada, ajuda no desenvolvimento: você muda o código de uma tool e o agente já usa a versão nova.
- **\[Testado\]** Numa pasta de teste com um arquivo `tools/triplo.py`, `Agent()` carregou `[]` (nenhuma tool) e `Agent(load_tools_from_directory=True)` carregou `['triplo']`. Ou seja, bastou colocar o arquivo lá e ligar a opção.

**\[Recomendação\]** Deixe esse recurso desligado fora do desenvolvimento. Se várias pessoas ou processos gravam arquivos no mesmo lugar, qualquer um que consiga escrever na pasta passa a executar código pelo agente. Em uma aplicação real, prefira a lista explícita no código (`Agent(tools=[...])`).

### Resumindo em uma frase

Anexe só tools cujo código você leu ou em quem confia, dê ao programa só as permissões de que ele precisa, e mantenha a pasta `./tools/` desligada fora dos testes.

## Exercício guiado

Tempo estimado: 15 minutos. Você precisa ter feito os passos de "Preparar o computador". As três partes abaixo não exigem modelo de IA nem chave de acesso.

**\[Testado\]** O código e as saídas abaixo foram executados do jeito que estão, com `strands-agents` 1.62.0 e Python 3.13. Se a sua saída for diferente, confira primeiro a versão com `pip show strands-agents`.

### Parte 1: anexar, ver, chamar e errar

Salve como `exercicio.py` e rode com `python exercicio.py`:

```python
from strands import Agent, tool


@tool
def celsius_para_fahrenheit(celsius: float) -> float:
    """Converte uma temperatura de graus Celsius para Fahrenheit.

    Args:
        celsius: Temperatura em graus Celsius
    """
    return celsius * 9 / 5 + 32


agent = Agent(tools=[celsius_para_fahrenheit])

# Passo 1: o que o agente tem na caixa
print("1:", agent.tool_names)

# Passo 2: chamada direta
r = agent.tool.celsius_para_fahrenheit(celsius=25)
print("2:", r["status"], r["content"])

# Passo 3: histórico, chamada gravada x não gravada
print("3a:", len(agent.messages))
agent.tool.celsius_para_fahrenheit(celsius=0)
print("3b:", len(agent.messages))
agent.tool.celsius_para_fahrenheit(celsius=0, record_direct_tool_call=False)
print("3c:", len(agent.messages))

# Passo 4: erro de propósito, valor sem nome
r = agent.tool.celsius_para_fahrenheit(25)
print("4:", r["status"])


# Passo 5: adicionar outra tool depois
@tool
def dobro(x: int) -> int:
    """Devolve o dobro de um número inteiro.

    Args:
        x: Número inteiro
    """
    return x * 2


agent.tool_registry.process_tools([dobro])
print("5a:", agent.tool_names)
print("5b:", agent.tool.dobro(x=21)["content"])

# Passo 6: erro de propósito, tool que não existe (o programa para aqui)
agent.tool.nao_existe(x=1)
```

Saída esperada (mais um bloco de texto de erro no final, que termina na linha mostrada):

```
1: ['celsius_para_fahrenheit']
2: success [{'text': '77.0'}]
3a: 4
3b: 8
3c: 8
4: error
5a: ['celsius_para_fahrenheit', 'dobro']
5b: [{'text': '42'}]
AttributeError: Tool 'nao_existe' not found
```

**O que observar:**

- **Passo 2:** a chamada direta devolve `status` e `content`.
- **Passo 3:** a chamada gravada acrescentou mensagens ao histórico (de 4 para 8), e a chamada com `record_direct_tool_call=False` não acrescentou nada (8 para 8).
- **Passo 4:** o valor sem nome não derruba o programa. O erro chega como `status` igual a `error`.
- **Passo 5:** a tool adicionada depois aparece na lista e responde à chamada direta.
- **Passo 6:** o programa para, com a mensagem `Tool 'nao_existe' not found`. Isso é esperado.

**Para testar sozinha:** troque o `25` do passo 2 por `100` e confira se o resultado é `212.0`.

### Parte 2: a pasta `./tools/`

1. Crie uma pasta nova chamada `experimento` e, dentro dela, uma subpasta chamada `tools`.
2. Em `experimento/tools/triplo.py`, salve:

```python
from strands import tool


@tool
def triplo(x: int) -> int:
    """Devolve o triplo de um número inteiro.

    Args:
        x: Número inteiro
    """
    return x * 3
```

3. Em `experimento/teste_pasta.py`, salve:

```python
from strands import Agent

print("A:", Agent().tool_names)
print("B:", Agent(load_tools_from_directory=True).tool_names)
```

4. No terminal, entre na pasta `experimento` e rode `python teste_pasta.py`. O Strands procura `./tools/` a partir da pasta em que você roda o comando.

Saída esperada:

```
A: []
B: ['triplo']
```

Isso mostra, na prática, que a pasta só é lida quando você liga `load_tools_from_directory=True`.

### Parte 3: pedir em linguagem natural (não testada aqui)

Só funciona com um provedor de modelo configurado. Se você tiver um, acrescente ao fim da Parte 1 (antes do passo 6, que interrompe o programa):

```python
agent("Quanto é 25 graus Celsius em Fahrenheit?")
```

O agente deve decidir sozinho usar a tool e responder algo como "77 °F". Compare com o passo 2: o cálculo vem da mesma tool, mas aqui quem escolheu usá-la foi o agente.

## Glossário

| Termo | Em linguagem simples |
| --- | --- |
| Agente (`Agent`) | A "assistente" inteira: junta o modelo, a caixa de ferramentas e a memória da conversa |
| Modelo | A IA que lê o pedido e decide o que fazer. Só escreve texto |
| Provedor de modelo | O serviço que fornece o modelo (por exemplo, Amazon Bedrock, Anthropic, OpenAI), geralmente com uma chave de acesso |
| Tool | Uma função que o agente pode usar para fazer algo no mundo real, como calcular, consultar ou gravar |
| Função | Um trecho de código com nome que recebe valores e devolve um resultado |
| Ficha da tool | O nome, a descrição e a explicação dos valores. É tudo o que o modelo enxerga sobre a tool |
| Anexar | Entregar tools ao agente, na criação ou depois |
| Invocar | Fazer uma tool rodar |
| Chamada direta | Você mesma roda a tool, com `agent.tool.nome(...)`, sem o modelo decidir |
| Linguagem natural | Pedir em frases comuns, como `agent("...")`, e deixar o modelo escolher a tool |
| Terminal | A janela onde você digita comandos em texto |
| Pacote | Código pronto que você instala e usa, como o `strands-agents` |
| `pip` | O instalador de pacotes do Python |
| Ambiente virtual | Uma pasta isolada para os pacotes de um projeto, para não bagunçar o resto do computador |
| Vended tools | Tools prontas que já vêm com o pacote do Strands |
| Registro de tools (`tool_registry`) | A lista interna onde o agente guarda as tools anexadas |
| Argumento nomeado | Passar um valor junto com o nome, como `celsius=25` |
| Argumento posicional | Passar o valor sem o nome, só pela ordem, como `25`. Não funciona na chamada direta |
| Dicionário | Uma lista de pares "nome: valor". É o formato do resultado de uma tool |
| Histórico da conversa | As mensagens que o agente guarda e usa como memória, incluindo as chamadas de tools |
| Exceção | Um erro que interrompe o programa, como o `AttributeError` |
| Executor | O componente que decide se várias tools pedidas juntas rodam ao mesmo tempo ou em fila |
| Concorrente | Várias coisas andando ao mesmo tempo |
| Sequencial | Uma coisa de cada vez, em ordem |

## Fontes e o que não foi verificado

Consultado em 27/10/2026.

### Páginas oficiais lidas

- [Attach and invoke tools](https://strandsagents.com/docs/user-guide/sdk/tools/using-tools/): base das seções sobre anexar, ver as tools carregadas, invocar e a pasta `./tools/`.
- [Tool Executors](https://strandsagents.com/docs/user-guide/concepts/tools/executors/): base da seção sobre executores concorrente e sequencial.
- [Add tools to your agent](https://strandsagents.com/docs/user-guide/sdk/tools/): visão geral, vended tools e aviso de segurança.
- [Create custom tools](https://strandsagents.com/docs/user-guide/sdk/tools/custom-tools/): carregamento de módulos importados.

### Páginas oficiais vistas apenas em trechos

- [State](https://strandsagents.com/docs/user-guide/sdk/agents/state/): origem da informação de que chamadas diretas são gravadas no histórico por padrão e do parâmetro `record_direct_tool_call` em Python.
- [Python Quickstart](https://strandsagents.com/docs/user-guide/sdk/quickstart/python/): requisitos de instalação (Python 3.10 ou superior). O nome do pacote (strands-agents) foi conferido por mim no PyPI, o catálogo público de pacotes Python.

### O que não foi verificado

- A invocação por linguagem natural ("Forma 1" e Parte 3 do exercício) não foi executada, pois exige um modelo configurado. O passo a passo do que acontece por trás é uma explicação minha.
- A página de executores consultada está no caminho `/concepts/` da documentação, que pode ser uma versão anterior da atual. Os testes confirmaram os nomes `ConcurrentToolExecutor` e `SequentialToolExecutor` e o parâmetro `tool_executor` na versão 1.62.0, mas não testei a execução paralela na prática.
- O método `agent.tool_registry.process_tools` para adicionar tools depois da criação funcionou nos testes, mas o guia lido não mostra o código desse caso. Ele aparece na referência da API.
- O número de mensagens acrescentadas por chamada direta (4) é um detalhe observado, não documentado.
- Todos os testes rodaram só na versão 1.62.0 do `strands-agents`.
- Não li a página de vended tools, então a lista de tools prontas vem apenas da visão geral.
