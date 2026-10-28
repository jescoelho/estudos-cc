# Strands Agents — Tópico 6: tools prontas

Oct 28, 2026 · @Jéssica Coelho

## Resumo e como ler

Existem **dois conjuntos de tools prontas** para Python: as que vêm **dentro do SDK** (`strands.vended_tools`, poucas e mais novas) e as do **pacote da comunidade** `strands-agents-tools` (mais de 40, várias já descontinuadas). Elas servem para você não precisar escrever do zero coisas comuns como ler arquivo, rodar comando ou chamar uma API. O ponto de atenção: **várias dessas tools têm acesso amplo ao seu computador e não têm limite de pasta**. Por isso este documento diz, para cada uma, o que ela faz, o que ela não faz e o que merece cuidado.

**Como ler:** as seções até "Cuidados" são o mínimo. "Para ir mais fundo" é opcional. Marcações: **\[Oficial\]** está na documentação ou no código da biblioteca; **\[Testado\]** rodei no pacote `strands-agents-tools` 0.8.10 e no `strands-agents` 1.62.0 (Linux); **\[Recomendação\]** é opinião minha. Tudo que é **\[Testado\]** foi em Linux: **não testei no Windows**, que é o seu sistema.

## A ideia central: uma caixa de ferramentas já montada

Comprar uma caixa de ferramentas pronta é mais rápido do que ir comprando peça por peça. Mas a caixa pronta tem duas pegadinhas:

- **Cada ferramenta tem um alcance.** Uma chave de fenda não serve para cortar madeira. Saber o que cada tool faz e **o que ela não faz** evita esperar dela algo que ela não entrega.
- **Algumas são ferramentas elétricas.** Um martelo só machuca o que você acertar. Uma serra elétrica corta o que estiver na frente. Tools como `shell` (rodar comandos) e `file_write` (gravar arquivos) são as serras elétricas: fazem o que o modelo de IA pedir, em qualquer pasta que sua conta consiga alcançar.

**Escopo** quer dizer o espaço de atuação de uma tool: o que ela foi feita para fazer. **Dentro do escopo** é o que a descrição dela promete. **Fora do escopo** é o que ela não faz, ou não foi feita para fazer. Neste documento também destaco, quando testei, o que ela faz **sem avisar**, porque isso pesa tanto quanto a descrição.

## O mínimo antes de começar

**Dois pacotes, duas formas de importar.**

| Conjunto | Instalação | Importação |
| --- | --- | --- |
| Vended tools (dentro do SDK) | já vem com `pip install strands-agents` | `from strands.vended_tools import file_editor` |
| Pacote da comunidade | `pip install strands-agents-tools` | `from strands_tools import file_read, file_write` |

Atenção ao nome: o pacote da comunidade se instala com hífens (`strands-agents-tools`) e se importa com sublinhado (`strands_tools`). **\[Oficial\]** A página [Community Tools Package](https://strandsagents.com/docs/user-guide/concepts/tools/community-tools-package/index.md) diz que ele é opcional, mantido pela comunidade, "para experimentar agentes durante o desenvolvimento", e só para Python. Algumas tools exigem extras, como `pip install 'strands-agents-tools[mem0_memory]'`.

**Anexar é igual a qualquer tool** (tópico 1):

```python
from strands import Agent
from strands_tools import file_read, calculator

agent = Agent(tools=[file_read, calculator])
print(agent.tool_names)   # ['file_read', 'calculator']
```

**\[Testado\]** Isso funcionou. E chamar direto também (`agent.tool.calculator(expression="2+2*3")` devolveu `Result: 8`).

**A regra da confirmação.** **\[Oficial\]** Tools que mexem em arquivo, rodam comando ou executam código (`shell`, `file_write`, `python_repl`) pedem sua confirmação antes de agir, a menos que a variável de ambiente `BYPASS_TOOL_CONSENT` esteja como `true`. **\[Testado\]** Chamei `file_write` sem a variável e sem terminal interativo: apareceu `Do you want to proceed with the file write? [y/*]`, a tool devolveu `File write cancelled by the user` e o arquivo **não foi criado**. Ou seja, o padrão é seguro. Depois que a variável é `true`, a confirmação some.

## Catálogo: o que cada tool faz e o que não faz

Como ler as tabelas: **Faz** = dentro do escopo. **Não faz** = fora do escopo, ou comportamento que testei e que surpreende. **Origem** aparece entre parênteses depois do nome da tool: **SDK** (`strands.vended_tools`) ou **Com.** (pacote da comunidade). Onde não há **\[Testado\]**, a informação vem só da descrição oficial da tool ou do README, e eu não rodei.

### A. Arquivos e anotações

| Tool (origem) | Faz | Não faz |
| --- | --- | --- |
| `file_read` (Com.) | Lê arquivos em vários modos: listar (`find`), mostrar (`view`), linhas (`lines`), trechos (`chunk`), buscar (`search`), estatísticas (`stats`), comparar (`diff`), histórico do git (`time_machine`) e, segundo a descrição, PDF/docx (`document`) **\[Oficial\]** | Não escreve nada. **\[Testado\]** Não limita a pasta: leu `/etc/hostname`, fora da pasta de trabalho. Arquivo que não existe dá `status: error` |
| `file_write` (Com.) | Cria ou grava um arquivo e cria as pastas que faltam **\[Testado\]** | **\[Testado\]** Não tem limite de pasta (gravou em `/tmp/...`, fora da pasta de trabalho). Sobrescreve arquivo existente e responde só "File written successfully". Não edita trecho: só grava o conteúdo inteiro. Pede confirmação por padrão |
| `file_editor` (SDK) | Ver arquivo (com faixa de linhas), criar, trocar um trecho (`str_replace`) e inserir linhas **\[Oficial\]** | **\[Testado\]** Exige caminho absoluto: caminho relativo dá `status: error` e sugere o absoluto. Sem sandbox, cria arquivo fora da pasta de trabalho. **\[Oficial\]** Não tem `pattern_replace`, `find_line` nem `undo_edit` (que existiam no `editor`) |
| `editor` (Com.) | Editor com vários comandos e backup automático **\[Oficial\]** | **Descontinuada** no README; o substituto é `file_editor` |
| `notebook` (SDK) | Bloco de notas do agente: criar, listar, ler, escrever (acrescentar, trocar, inserir) e limpar **\[Oficial\]** | Só escreve em notebook que já existe. `create` **sobrescreve** o conteúdo existente **\[Oficial\]**. As notas fazem parte do estado do agente, não são um arquivo seu no disco |

## Cuidados: o que cada tool pode alcançar

A regra prática: **a tool pode tudo o que a sua conta pode**. Nenhuma das tools de arquivo que testei limita a pasta, e as de comando e código não têm limite nenhum além do que o seu usuário já pode fazer. Quem decide o que chamar é o modelo de IA, não você.

| Nível | Tools | O que pode acontecer |
| --- | --- | --- |
| 1. Só lê | `file_read`, `calculator`, `current_time` | Ler arquivos sensíveis que você não previu (o `file_read` não limita pasta) |
| 2. Grava | `file_write`, `file_editor`, `notebook` | Criar ou sobrescrever arquivos em qualquer pasta que você alcance |
| 3. Executa | `shell`, `python_repl`, `load_tool`, `mcp_client`, `code_interpreter` | Rodar comandos ou código arbitrário no seu computador (exceto `code_interpreter`, que é isolado) |
| 4. Fala com o mundo | `http_request`, `web_fetch`, `use_aws`, `browser` | Enviar dados para fora ou alterar recursos na nuvem, com as suas credenciais |

**O que protege você, em ordem de importância:**

1. **Confirmação antes de agir.** **\[Testado\]** Por padrão `file_write` cancela quando não há quem confirme. **\[Oficial\]** `BYPASS_TOOL_CONSENT=true` e `STRANDS_NON_INTERACTIVE=true` desligam isso; a documentação diz para evitar `BYPASS_TOOL_CONSENT` em produção. Nos meus testes eu o liguei de propósito, numa sandbox descartável.
2. **Sandbox.** **\[Oficial\]** Um sandbox é um ambiente separado onde comandos e arquivos acontecem (Docker ou SSH). Você o liga com `Agent(sandbox=DockerSandbox("id-do-container"))`, e a página de sandbox chama o acesso irrestrito ao computador de "a serious security risk". **\[Testado\]** Sem sandbox, o agente reportou o tipo `NotASandboxLocalEnvironment` e as tools do SDK agiram direto no computador.
3. **Lista curta de tools.** **\[Recomendação\]** Entregue ao agente só as tools de que ele precisa. Uma tool que não está na lista não pode ser chamada.
4. **Credenciais com poucas permissões.** **\[Recomendação\]** Para `use_aws`, use uma credencial só de leitura e do serviço necessário.

**Windows (o seu caso).** **\[Oficial\]** Segundo o README, não funcionam no Windows: `shell` e `python_repl` do pacote da comunidade, e `cron`. A página de vended tools indica Unix/Linux/macOS para o `bash`. **Não testei o `shell` do SDK no Windows.** Por isso, para praticar no Windows, comece com `file_read`, `file_write`, `calculator` e `current_time`, que não aparecem na lista de incompatibilidades.

## Como escolher e quando criar a sua própria

Use esta ordem de decisão:

1. **Existe uma tool do SDK para isso?** Prefira ela: vem no mesmo pacote do `strands-agents`, tem atualização conjunta e, como vimos, várias tools da comunidade já apontam o SDK como substituto (`shell`, `http_request`, `editor`).
2. **Só existe no pacote da comunidade?** Verifique se não está marcada como descontinuada e se funciona no Windows. **\[Oficial\]** O próprio pacote se descreve como "para experimentar agentes durante o desenvolvimento", não como solução de produção.
3. **O escopo da tool é maior que o da sua tarefa?** Então crie a sua. Um exemplo: você só precisa que o agente leia arquivos de **uma** pasta. O `file_read` lê qualquer pasta, mas uma tool sua (tópico 2) pode checar o caminho antes de ler e recusar o que estiver fora.

```python
from pathlib import Path
from strands import tool

PASTA_PERMITIDA = Path("dados").resolve()

@tool
def ler_relatorio(nome: str) -> str:
    """Lê um relatório de texto da pasta 'dados'. Não lê nada fora dela.

    Args:
        nome: nome do arquivo dentro da pasta dados
    """
    caminho = (PASTA_PERMITIDA / nome).resolve()
    if PASTA_PERMITIDA not in caminho.parents:
        return {"status": "error", "content": [{"text": "Arquivo fora da pasta permitida."}]}
    return caminho.read_text(encoding="utf-8")
```

**\[Recomendação\]** Esse tipo de tool pequena, com escopo estreito e recibo `status: error` quando recusa algo (tópico 3), costuma ser mais segura do que entregar uma tool geral e confiar na descrição dela. **\[Testado\]** Neste exemplo, `rel.txt` foi lido; `../segredo.txt` e `/etc/hostname` foram recusados com `status: error`; um arquivo inexistente também deu erro, mas a mensagem mostra o caminho completo da pasta no seu computador, que vai para o modelo. Se isso importa, capture o erro e devolva uma mensagem curta.

## Para ir mais fundo (opcional)

Pode pular esta seção e voltar quando precisar.

**1. As tools prontas seguem as regras dos tópicos anteriores.** **\[Testado\]** Elas aparecem em `agent.tool_names`, você as chama direto com `agent.tool.nome(...)` e o resultado é o recibo do tópico 3. Mas o recibo nem sempre conta a história toda: o `shell` do SDK devolve `status: success` mesmo quando o comando falha (veja `exit_code`), e o `http_request` da comunidade devolve `success` para um 404. Quem decide se é erro é cada tool, não o Strands.

**2. A pasta de trabalho importa.** **\[Testado\]** Caminhos relativos (`area/nota.txt`) valem a partir da pasta onde você rodou o Python, a mesma pegadinha da pasta `./tools/` do tópico 1. O `file_editor` do SDK recusa caminho relativo e sugere o absoluto.

**3. As descrições que o modelo lê.** Cada tool traz uma descrição (como as docstrings do tópico 2). **\[Testado\]** Li as descrições das tools prontas no código; algumas têm dezenas de linhas (a do `file_read` lista dez modos). Descrições longas custam espaço na conversa a cada pedido ao modelo. **\[Recomendação\]** Mais um motivo para entregar uma lista curta.

**4. Versões e divergências.** **\[Oficial\]** A página de vended tools (que li) cita só quatro tools e usa `bash`. **\[Testado\]** No `strands-agents` 1.62.0 existem 13 módulos em `strands.vended_tools`, e `bash` já avisa que está descontinuada em favor de `shell`. A documentação está atrás do código; na dúvida, confie no que a sua versão instalada faz. Para ver a sua: `pip show strands-agents strands-agents-tools`.

**5. Calendário de descontinuação.** **\[Oficial\]** Os avisos começam na v0.8.6 do pacote da comunidade e viram erro de log na v0.9.0. Um projeto que dependa dessas tools precisará migrar.

**6. TypeScript.** **\[Oficial\]** As vended tools também existem em TypeScript (`bash`, `fileEditor`, `httpRequest`, `notebook`). O pacote da comunidade é só Python.

## Exercício guiado

Objetivo: usar quatro tools prontas, ver a confirmação de gravação funcionando e comprovar que o `file_read` não limita a pasta. Não precisa de conta na AWS nem de modelo: você chama as tools direto, como no tópico 1.

**Passo 1.** No terminal, na pasta `C:\Users\jecoe\strands`, instale o pacote: `pip install strands-agents-tools`.

**Passo 2.** Crie `exercicio_t6.py`:

```python
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
mostrar("file_read fora da pasta", agent.tool.file_read(path=OUTRO_ARQUIVO, mode="view"))
```

**Passo 3.** Rode `python exercicio_t6.py`. Na Parte 2 aparece `Do you want to proceed with the file write? [y/*]`. Digite `y` e Enter.

**Resultado esperado** **\[Testado em Linux, não no Windows\]** (as horas e o arquivo da Parte 4 mudam; avisos `DEPRECATION WARNING` aparecem a cada uso de `calculator` e `current_time`, é normal):

```text
--- Parte 1: tools que só calculam ---
calculator: 2+2*3
   status = success
   texto  = Result: 8
current_time: São Paulo
   status = success
   texto  = 2026-10-28T01:02:04.643112-03:00
calculator: nome que não existe
   status = success
   texto  = Result: preco_petr4

--- Parte 2: gravar (vai pedir confirmação; responda y) ---
file_write
   status = success
   texto  = File write success: File written successfully to nota_t6.txt

--- Parte 3: ler de volta ---
file_read
   status = success
   texto  = Content of nota_t6.txt: linha 1 linha 2

--- Parte 4: ler um arquivo de OUTRA pasta ---
file_read fora da pasta
   status = success
   texto  = Content of /etc/hostname: vm
```

**O que observar:**

- Parte 1, terceira linha: o `calculator` não dá erro para um nome que ele não conhece. Ele devolve o próprio nome. Ele não busca dados.
- Parte 2: a tool só gravou depois do seu `y`. Se você responder qualquer outra coisa (ou só Enter), o recibo vem com `File write cancelled by the user` e o arquivo não é criado.
- Parte 4: o `file_read` leu um arquivo que não está na sua pasta de trabalho. Esse é o ponto do tópico: a tool não limita onde lê.

**Desafio:** na Parte 2, troque `agent.tool.file_write(...)` por um `file_write` com `path="subpasta/nota.txt"` e responda `y`. A pasta `subpasta` existia? O que isso diz sobre o escopo do `file_write`? Dica: releia a linha dele no catálogo.

## Glossário

| Termo | Em palavras simples |
| --- | --- |
| Tool pronta | tool que alguém já escreveu e você só importa e anexa ao agente |
| Vended tool ("tool entregue") | tool pronta que vem dentro do próprio SDK `strands-agents`, em `strands.vended_tools` |
| Pacote da comunidade (`strands-agents-tools`) | coleção separada de tools prontas, mantida pela comunidade, instalada com `pip` e importada de `strands_tools` |
| Escopo | o que uma tool foi feita para fazer; dentro do escopo é o prometido, fora do escopo é o que ela não faz |
| Descontinuada (deprecated) | ainda funciona, mas vai ser removida ou virar erro numa versão futura; o código mostra um aviso |
| Consentimento (`BYPASS_TOOL_CONSENT`) | a confirmação `[y/*]` que a tool pede antes de gravar ou executar; a variável `true` desliga o pedido |
| Sandbox | ambiente separado (como um container Docker) onde comandos e arquivos do agente acontecem, para não mexerem no seu computador |
| `exit_code` | número que um comando devolve ao terminar: `0` significa que deu certo, qualquer outro número indica falha |
| PTY | terminal simulado; deixa um comando interativo funcionar dentro da tool |
| Extra (`pip install 'pacote[extra]'`) | instala dependências adicionais que só algumas tools usam |
| MCP | protocolo para ligar o agente a servidores que oferecem tools (assunto de outro tópico) |

## Fontes e o que não foi verificado

**Páginas que abri e li:**

- [Community Tools Package](https://strandsagents.com/docs/user-guide/concepts/tools/community-tools-package/index.md): o que é o pacote, extras, lista por categoria, consentimento.
- [Strands Agents Tools (README no GitHub)](https://github.com/strands-agents/tools): lista de tools, descontinuações, Windows, variáveis de ambiente (li até o ponto em que o texto foi cortado, cerca de 96%).
- [Vended Tools](https://strandsagents.com/docs/user-guide/concepts/tools/vended-tools/): quatro tools descritas, importação.
- [Sandbox](https://strandsagents.com/docs/user-guide/concepts/sandbox/): o que é, Docker e SSH, tools `sandbox_bash` e `sandbox_file_editor`.

**Testado por mim** em Linux, com `strands-agents` 1.62.0 e `strands-agents-tools` 0.8.10: `calculator`, `current_time`, `file_read`, `file_write`, a confirmação, `shell`, `python_repl`, `file_editor` e `http_request` do SDK, `http_request` da comunidade (contra um servidor local) e o exemplo `ler_relatorio`. As descrições de cada tool foram lidas no código instalado.

**Não verificado:**

- **Windows.** Nada foi testado lá. Em particular, `current_time` com `America/Sao_Paulo` pode exigir `pip install tzdata` no Windows **\[Recomendação, não testado\]**; a Parte 4 do exercício lê `C:\Windows\win.ini`, que eu não conferi.
- As tools que precisam de extras, chaves ou serviços: `use_aws`, `browser`, `use_computer`, `code_interpreter`, memórias, Tavily, Exa, imagens e vídeo, `a2a_client`. Sobre elas, só há descrição oficial.
- `web_fetch`, `subagent`, `swarm`, `notebook`, `handoff_to_user` e `stop` do SDK: só a descrição no código.
- O `http_request` do SDK com autenticação ou na internet aberta.
- O `shell` do SDK no Windows.
- A lista de descontinuadas: a do README é a referência; vi que o código avisa também sobre `http_request`, que o README não marca. Pode haver outras.
- O README foi lido até cerca de 96%: a parte final (contribuição, licença) não foi lida.
- As dicas marcadas **\[Recomendação\]** são minhas.

### B. Comandos, código e cálculo

| Tool (origem) | Faz | Não faz |
| --- | --- | --- |
| `shell` (SDK) | Executa um comando e devolve `output`, `error` e `exit_code` **\[Testado\]** | **\[Testado\]** Cada chamada abre um shell novo: `cd /tmp` numa chamada não vale na seguinte. **Comando que falha volta com `status: success`**; o erro está em `exit_code` (ex.: `2`) e em `error`. Sem sandbox, roda direto no seu computador |
| `shell` (Com.) | Shell interativo com PTY, comandos em lote **\[Oficial\]** | **Descontinuada.** Não funciona no Windows **\[Oficial\]**. O substituto é o `shell` do SDK |
| `python_repl` (SDK) | Executa Python e devolve `output`, `error` e `exit_code` **\[Oficial\]** | Cada chamada é um interpretador novo: variáveis e imports não persistem. `input()` não funciona. Arquivos gravados na pasta de trabalho persistem **\[Oficial\]** |
| `python_repl` (Com.) | Executa Python **mantendo o estado** entre chamadas; mostra o código e pede confirmação **\[Oficial\]** | Não funciona no Windows (depende do módulo `fcntl`) **\[Oficial\]** |
| `code_interpreter` (Com.) | Executa Python, JavaScript ou TypeScript num ambiente isolado, com sessões **\[Oficial\]** | Precisa do extra `agent_core_code_interpreter` e do serviço AWS AgentCore. Não testei |
| `calculator` (Com.) | Conta com SymPy: `evaluate`, `solve`, derivadas, integrais, limites, matrizes **\[Oficial\]**. **\[Testado\]** `2+2*3` → 8; `sqrt(16)` → 4; resolver `x**2 - 4` → ±2 | **Descontinuada.** **\[Testado\]** Não consulta dados: `preco_petr4` voltou como `Result: preco_petr4`, sem erro (tratou como símbolo). Expressão mal escrita dá `status: error`. Cada chamada imprime um aviso de descontinuação |
| `current_time` (Com.) | Hora atual em ISO 8601 para um fuso **\[Testado\]**: `America/Sao_Paulo` → `2026-10-28T00:58:09-03:00` | **Descontinuada.** **\[Testado\]** Fuso inválido dá `status: error`. O README manda injetar a hora como contexto em vez de usar tool |
| `environment` (Com.) | Lista, lê, define e apaga variáveis de ambiente; esconde valores de nomes com TOKEN, SECRET, PASSWORD, KEY, AUTH **\[Oficial\]** | **Descontinuada.** Um shell filho não altera o ambiente do agente **\[Oficial\]**. `python_repl` e `shell` ainda conseguem gravar variáveis sensíveis **\[Oficial\]** |
| `load_tool` (Com.) | Carrega um arquivo `.py` como tool em tempo de execução; pede consentimento **\[Oficial\]** | Executa o código do arquivo (o mesmo cuidado da pasta `./tools/` do tópico 1) |

### C. Web e conexões externas

| Tool (origem) | Faz | Não faz |
| --- | --- | --- |
| `http_request` (SDK) | Faz chamadas GET, POST, PUT, DELETE, PATCH, HEAD e OPTIONS e devolve status, cabeçalhos e corpo **\[Oficial\]**. **\[Testado\]** GET num servidor local → `status: 200` com corpo | **\[Testado\]** Resposta HTTP de erro (404, 501) volta como `status: error`. Não testei autenticação nem a internet aberta |
| `http_request` (Com.) | Autenticação (Bearer, Basic, JWT, AWS SigV4, Digest), sessões e cookies; converte HTML em texto limpo se pedir **\[Oficial\]**. **\[Testado\]** `<h1>Titulo</h1>` virou `# Titulo` | **Descontinuada** (o código avisa, embora a tabela do README não marque). **\[Testado\]** Resposta 404 volta como `status: success`, com `Status Code: 404` só dentro do texto, ao contrário da versão do SDK |
| `web_fetch` (SDK) | Busca uma URL e responde a uma pergunta sobre o conteúdo; a página inteira não entra no contexto do agente principal **\[Oficial\]** | O parâmetro `prompt` é obrigatório. Pela descrição, um "analista" lê a página, então provavelmente usa um modelo de IA. Não testei |
| `tavily_*`, `exa_*` (Com.) | Busca, extração e rastreamento de sites **\[Oficial\]** | Exigem chave de API (`TAVILY_API_KEY`, `EXA_API_KEY`), serviços de terceiros |
| `browser`, `use_computer` (Com.) | Automação de navegador Chromium e do desktop (mouse, teclado, capturas, apps) **\[Oficial\]** | Alcance muito amplo. Exigem extras. Não testei |
| `mcp_client` (Com.) | Conecta a servidores MCP e carrega as tools deles em tempo de execução **\[Oficial\]** | **Alto risco, segundo o próprio código:** o agente pode se conectar a qualquer servidor e carregar código não confiável. Não é o MCP configurado por você (assunto de outro tópico) |
| `a2a_client` (SDK e Com.) | Descobre e conversa com agentes remotos pelo protocolo A2A **\[Oficial\]** | Exige o extra `a2a`; não instalei, não testei |

### D. AWS, memória e conteúdo

| Tool (origem) | Faz | Não faz |
| --- | --- | --- |
| `use_aws` (Com.) | Faz uma chamada boto3 com serviço, operação e parâmetros que o modelo escolher **\[Oficial\]** | Não limita a leitura: pode tentar qualquer operação que as **suas credenciais** permitam. Não testei (sem credenciais AWS) |
| `retrieve`, `memory` (Com.) | Consulta e gerencia documentos em Amazon Bedrock Knowledge Bases **\[Oficial\]** | **Descontinuadas** (o substituto indicado é `MemoryManager`). O armazenamento devolve pontuações, mas não filtra por elas **\[Oficial\]** |
| `mem0_memory`, `agent_core_memory`, `mongodb_memory`, `elasticsearch_memory` (Com.) | Guardam e buscam memórias entre execuções, cada uma num serviço diferente **\[Oficial\]** | Exigem extras e um serviço externo. Na `mem0_memory`, `user_id` e `agent_id` não ficam expostos ao agente, de propósito **\[Oficial\]** |
| `generate_image`, `generate_image_stability`, `nova_reels`, `image_reader`, `speak`, `diagram` (Com.) | Gerar imagem, gerar vídeo, ler imagem, falar texto e desenhar diagramas **\[Oficial\]** | Dependem de serviços (Bedrock, Stability AI, Polly) e de extras. `diagram` está descontinuada, sem substituto direto **\[Oficial\]**. Não testei |

### E. Controle do agente e vários agentes

| Tool (origem) | Faz | Não faz |
| --- | --- | --- |
| `handoff_to_user` (SDK) | Faz uma pergunta ao usuário e espera a resposta; ela volta como resultado da tool **\[Oficial\]** | Não serve para entregar resposta final nem relatório de progresso **\[Oficial\]**. A versão da comunidade foi pensada para terminal; em produção você precisa montar o seu próprio mecanismo de interface **\[Oficial\]** |
| `stop` (SDK) | Encerra o ciclo do agente quando a tarefa acabou, com mensagem final opcional **\[Oficial\]** | É uma parada "cooperativa", não um corte: tools já pedidas naquele turno ainda rodam **\[Oficial\]** |
| `sleep` (SDK) | Pausa a execução por até 60 segundos; pode ser cancelada **\[Oficial\]** | Recusa duração negativa, infinita ou acima de 60 s **\[Oficial\]**. A versão da comunidade está descontinuada |
| `subagent` (SDK) | Delega uma tarefa a um subagente com contexto próprio e recebe só o relatório final **\[Oficial\]** | Pense em "agente como tool" (tópico 5), mas criado na hora pela própria tool |
| `swarm` (SDK e Com.) | Monta uma equipe de subagentes que passam a tarefa entre si **\[Oficial\]** | Não testei |
| `use_agent`, `use_llm`, `workflow`, `graph`, `agent_graph` (Com.) | Agentes aninhados, fluxos de várias etapas e grafos de agentes **\[Oficial\]** | Nenhuma está marcada como descontinuada na tabela do README. Só li as descrições; não testei nenhuma. |

**Outras tools marcadas como descontinuadas no README** **\[Oficial\]**: `think`, `batch` (o SDK já roda tools em paralelo), `cron` (não funciona no Windows), `slack` (usar o servidor MCP oficial do Slack) e `rss`. Não as detalho por isso. **\[Testado\]** O código também avisa sobre descontinuação em tools que o README não marca (vimos `http_request`), então trate a lista do README como mínima.
