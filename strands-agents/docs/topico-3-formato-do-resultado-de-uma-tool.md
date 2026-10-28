# Strands Agents — Tópico 3: formato do resultado de uma tool

Oct 28, 2026 · @Jéssica Coelho

## Resumo e como ler

Toda tool devolve um "recibo" com três campos: `toolUseId` (o número do pedido), `status` (deu certo ou deu errado) e `content` (o conteúdo da resposta). Na prática, você quase nunca monta esse recibo: o Strands monta para você. Só precisa montá-lo quando quer controlar se o resultado conta como sucesso ou erro, ou quando quer devolver dados estruturados.

**Como ler:** as seções até "Sucesso e erro" são o mínimo. "Para ir mais fundo" é opcional. Marcações: **\[Oficial\]** está na documentação do Strands; **\[Testado\]** rodei na versão 1.62.0; **\[Recomendação\]** é opinião minha.

## A ideia central: o resultado é um recibo de entrega

Imagine pedir uma encomenda. Quando ela chega, vem um recibo com: o número do pedido, se a entrega deu certo ou não, e o que veio na caixa. É exatamente isso que o Strands guarda depois de rodar uma tool.

| Campo | No recibo da encomenda | Na tool |
| --- | --- | --- |
| `toolUseId` | número do pedido | identifica qual pedido de uso gerou este resultado |
| `status` | "entregue" ou "problema na entrega" | `"success"` ou `"error"` |
| `content` | o que veio na caixa | uma lista com o conteúdo (texto, dados etc.) |

Por que isso importa? Porque o modelo de IA (o "cérebro" que decide qual tool usar) lê esse recibo para saber se deu certo e o que fazer a seguir.

## O mínimo antes de começar

Você já viu esse recibo nos tópicos 1 e 2, sem ter o nome dele. Quando chamamos uma tool direto (`agent.tool.nome(...)`), o que voltava era isto:

```python
{'toolUseId': 'tooluse_simples_473431949', 'status': 'success', 'content': [{'text': '10'}]}
```

Esse pedaço entre chaves `{...}` é um **dicionário** (uma lista de pares "nome: valor", como uma ficha de cadastro). E `[...]` é uma **lista** (itens em fila). Então `content` é uma lista, e cada item dela é um pequeno dicionário com o tipo do conteúdo (`text`) e o conteúdo em si (`'10'`).

## Formato básico: o que o Strands faz com o que sua tool devolve

**\[Oficial\]** A página de custom tools diz que, numa tool feita com `@tool`, um valor simples vira texto (`{"text": str(resultado)}`), e um dicionário já no formato certo é usado como está. **\[Testado\]** Rodei oito tools diferentes para ver o recibo de cada uma:

| O que a tool devolve (`return`) | O que aparece em `content` | `status` |
| --- | --- | --- |
| um número: `return 10` | `[{'text': '10'}]` | success |
| um texto: `return "Oi, Jé!"` | `[{'text': 'Oi, Jé!'}]` | success |
| um dicionário comum: `{"dobro": 6, "ok": True}` | `[{'text': '{"dobro": 6, "ok": true}'}]` (virou texto) | success |
| um dicionário com `status` e `content` | usado como você montou | o que você escreveu |
| um dicionário com `content` mas **sem** `status` | `[{'text': '{"content": [{"text": "sem status"}]}'}]` (tratado como dicionário comum) | success |
| a tool quebra (exceção) | `[{'text': 'Error: ZeroDivisionError - ...'}]` | error |

A regra prática: **se você não precisa controlar nada, só dê `return` no valor. O Strands embrulha.** Se quiser controlar, devolva um dicionário com `status` e `content` (próxima seção).

Nota: o campo `toolUseId` não precisa ser escrito por você em tools `@tool`; o Strands preenche. **\[Oficial\]** A documentação o marca como opcional.

## O que pode ir dentro de `content`

`content` é uma lista de "itens da caixa". Cada item diz seu tipo. **\[Oficial\]** A página de custom tools documenta dois tipos:

| Tipo | O que é | Quando usar |
| --- | --- | --- |
| `text` | um texto | respostas simples, mensagens, erros |
| `json` | dados organizados (um dicionário ou lista) | quando o resultado tem várias partes, como uma tabela de resultados |

Exemplo oficial de uma tool que devolve os dois tipos juntos:

```python
{"status": "success", "content": [
    {"text": "Operation completed successfully"},
    {"json": {"results": [1, 2, 3], "total": 3}}
]}
```

**\[Testado\]** Rodei uma versão disso (`text` + `json`) e o Strands devolveu exatamente os dois itens, sem alterar nada: `[{'text': 'veja abaixo'}, {'json': {'dobro': 8}}]`.

**\[Oficial\]** A página de referência da API (`strands.types.tools`) lista quatro tipos: `text`, `json`, `image` e `document`. Mas não explica como montar `image` e `document`, e eu não testei. Por isso, neste documento, só ensino `text` e `json`.

## Sucesso e erro

O campo `status` é o que avisa o modelo (e você) se a tool funcionou. Só existem dois valores: `"success"` e `"error"`.

Há dois caminhos para chegar a `"error"`:

1. **A tool quebra sozinha.** **\[Testado\]** Uma tool com `1 // a` chamada com `a=0` não derruba o programa: o Strands captura e devolve `status: 'error'` com o texto `Error: ZeroDivisionError - integer division or modulo by zero`.
2. **Você decide que é erro.** **\[Testado\]** Se a tool não quebrou mas o pedido não faz sentido (por exemplo, um número não aceito), você devolve você mesmo:

```python
return {"status": "error", "content": [{"text": "Número não aceito"}]}
```

Por que o segundo caminho importa? Se você só devolver o texto `"Número não aceito"` com `return`, o recibo diz `status: 'success'`, e o modelo entende que deu tudo certo. Marcar `error` é como carimbar "problema na entrega": o modelo percebe e pode tentar outra coisa.

**\[Recomendação\]** Escreva a mensagem de erro dizendo o que deu errado e o que o modelo pode fazer (ex.: "o número precisa ser maior que zero").

## Para ir mais fundo (opcional)

Pode pular esta seção e voltar quando precisar.

**1. Cuidado com o dicionário "quase certo".** **\[Testado\]** Se você devolver `{"content": [{"text": "oi"}]}` sem o campo `status`, o Strands não reconhece como recibo montado: trata como dicionário comum e o transforma em texto. O resultado fica `[{'text': '{"content": [{"text": "oi"}]}'}]`, com as chaves e aspas aparecendo no meio da resposta. Sem erro, sem aviso. Por isso, quando montar o recibo à mão, escreva sempre `status` **e** `content`.

**2. Tools de módulo (TOOL\_SPEC) montam o recibo inteiro.** **\[Oficial\]** Nesse formato (visto no tópico 2), a função recebe o pedido e devolve `toolUseId`, `status` e `content`, copiando o `toolUseId` do pedido:

```python
return {
    "toolUseId": tool["toolUseId"],
    "status": "success",
    "content": [{"text": result}],
}
```

**3. Dois nomes parecidos na referência da API.** **\[Oficial\]** `ToolResult` usa `toolUseId` (camelCase). `ToolResultBlock`, uma classe separada, usa `tool_use_id` (snake\_case). Se você ler código do Strands e achar os dois, é a mesma ideia com grafias diferentes.

**4. `outputSchema` (opcional).** **\[Oficial\]** A definição de uma tool (`ToolSpec`) tem um campo opcional `outputSchema` que descreve o formato da saída, mas nem todos os provedores de modelo suportam. Não testei.

**5. TypeScript.** **\[Oficial\]** A mesma página descreve o formato para TypeScript, com nomes um pouco diferentes (`toolResultBlock`, `jsonBlock`). Como você está em Python, ignorei.

## Exercício guiado

Objetivo: ver com seus olhos os três casos: valor simples, recibo montado à mão com `json`, e erro decidido por você.

**Passo 1.** Na pasta `C:\Users\jecoe\strands`, crie o arquivo `exercicio_t3.py` com este conteúdo:

```python
from strands import Agent, tool


@tool
def dobro(numero: float) -> float:
    """Calcula o dobro de um número.

    Args:
        numero: o número a dobrar
    """
    return numero * 2


@tool
def raiz_quadrada(numero: float) -> dict:
    """Calcula a raiz quadrada de um número (só aceita zero ou positivo).

    Args:
        numero: o número (zero ou maior)
    """
    if numero < 0:
        return {
            "status": "error",
            "content": [{"text": "O número precisa ser zero ou maior."}],
        }
    return {
        "status": "success",
        "content": [
            {"text": "Cálculo feito."},
            {"json": {"numero": numero, "raiz": numero ** 0.5}},
        ],
    }


agent = Agent(tools=[dobro, raiz_quadrada])

print("--- Parte 1 ---")
print(agent.tool.dobro(numero=4))

print("--- Parte 2 ---")
print(agent.tool.raiz_quadrada(numero=9))

print("--- Parte 3 ---")
r = agent.tool.raiz_quadrada(numero=-1)
print(r["status"])
print(r["content"][0]["text"])
```

**Passo 2.** No terminal, na mesma pasta, rode `python exercicio_t3.py`.

**Resultado esperado** **\[Testado\]** (o número depois de `tooluse_` muda a cada execução, é normal):

```text
--- Parte 1 ---
{'toolUseId': 'tooluse_dobro_466127980', 'status': 'success', 'content': [{'text': '8.0'}]}
--- Parte 2 ---
{'status': 'success', 'content': [{'text': 'Cálculo feito.'}, {'json': {'numero': 9.0, 'raiz': 3.0}}], 'toolUseId': 'tooluse_raiz_quadrada_206704789'}
--- Parte 3 ---
error
O número precisa ser zero ou maior.
```

**O que observar:**

- Parte 1: você só deu `return numero * 2` e o Strands montou o recibo inteiro; o `8.0` virou texto.
- Parte 2: `content` tem dois itens, um `text` e um `json`; o `json` manteve a estrutura (não virou texto).
- Parte 3: `r["status"]` lê o campo `status` do recibo, e `r["content"][0]["text"]` lê o primeiro item (o "0" é a posição: o computador começa a contar do zero).

**Desafio:** na `dobro`, troque `return numero * 2` por `return {"content": [{"text": "oi"}]}` (sem `status`) e rode de novo. O que aparece em `content`? Dica: releia o item 1 de "Para ir mais fundo".

## Glossário

| Termo | Em palavras simples |
| --- | --- |
| Resultado da tool (`ToolResult`) | o "recibo" que o Strands guarda depois de rodar uma tool |
| `toolUseId` | o número do pedido; liga o resultado ao pedido que o gerou |
| `status` | se deu certo (`"success"`) ou errado (`"error"`) |
| `content` | a lista com o que a tool devolveu |
| `text` | um item de `content` que é só texto |
| `json` | um item de `content` com dados organizados (dicionário ou lista) |
| Dicionário (`{...}`) | uma ficha com pares "nome: valor" |
| Lista (`[...]`) | itens em fila, numerados a partir do zero |
| Exceção | um erro que acontece enquanto o código roda; o Strands captura e transforma em `status: "error"` |
| Embrulhar | o que o Strands faz com um `return` simples: coloca dentro de um recibo completo |

## Fontes e o que não foi verificado

**Páginas que abri e li:**

- [Creating Custom Tools](https://strandsagents.com/docs/user-guide/concepts/tools/custom-tools/): seções "Tool Response Format", "Tool Result Handling" e "Custom Return Type" (o nome "Tool result format" que usei como título do tópico não é o título exato da seção).
- [strands.types.tools (referência da API)](https://strandsagents.com/docs/api/python/strands.types.tools/): `ToolResult`, `ToolResultContent`, `ToolSpec`.

**Testado por mim** em strands-agents 1.62.0, chamando as tools direto (`agent.tool.nome(...)`): todos os resultados mostrados neste documento.

**Não verificado:**

- Como o modelo de IA reage a `status: error` na prática (precisa de um provedor de modelo configurado, que não tenho aqui). A frase "o modelo percebe e pode tentar outra coisa" é minha dedução, não um teste.
- Os tipos `image` e `document` em `content`: listados na referência da API, sem exemplos nas páginas que li.
- `outputSchema`.
- O formato em TypeScript (só li a descrição).
- A página "Tool result format" citada no seu roteiro não foi encontrada com esse nome; usei as seções acima, que cobrem o mesmo assunto.
