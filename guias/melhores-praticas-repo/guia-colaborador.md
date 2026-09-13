# Guia de colaboração — Skill de Documentação Técnica

Você não precisa saber Git para seguir este fluxo — o Claude Code com MCP GitHub
executa as operações por você.

---

## A lógica do repositório em uma frase

Ninguém trabalha diretamente na versão oficial. Todo trabalho acontece numa cópia
isolada (branch), e só entra na versão oficial depois de revisado e aprovado.

---

## Estrutura de branches

```
main          ← versão oficial e estável (ninguém toca diretamente)
└── develop   ← integração das demandas concluídas
    └── feature/pseudoalgoritmo            ← branch de uma demanda
        ├── feature/pseudoalgoritmo-jessica  ← branch pessoal
        └── feature/pseudoalgoritmo-ana      ← branch pessoal
```

---

## Fluxo de trabalho

### 1. Antes de começar

> "Qual é a branch da demanda que vou trabalhar hoje?"

Se a branch não existir:

> "Cria a branch `feature/[nome-da-demanda]` a partir de `develop`"

### 2. Criando sua branch pessoal

> "Cria minha branch `feature/[nome-da-demanda]-[seu-nome]` a partir de `feature/[nome-da-demanda]`"

### 3. Abrindo o PR com WIP — obrigatório ao iniciar

Logo após criar sua branch, antes de qualquer alteração:

> "Abre um PR em andamento da minha branch para `feature/[nome-da-demanda]`"

O Claude cria o PR com prefixo `WIP:` no título. Isso torna seu trabalho visível
ao time imediatamente — qualquer push que você fizer aparece automaticamente no PR,
sem nenhuma ação extra.

### 4. Durante o trabalho — push frequente

Ao final de cada etapa significativa (não só ao final da sessão):

> "Salva o que eu fiz com a mensagem: feat: [descrição do que mudou]"

Push frequente protege contra desligamento inesperado da instância e mantém
o PR atualizado em tempo real para o time.

### 5. Ao concluir a demanda

> "Remove o WIP do meu PR e marca como pronto para revisão"

---

## Como acompanhar o time

O PR com WIP de cada pessoa é atualizado automaticamente a cada push —
abrir a aba de PRs do GitHub já mostra o estado atual de todo mundo.

Para uma visão consolidada via Claude:

> "Mostra o estado atual das branches e PRs do repositório"

---

## Regras inegociáveis

**1. Nunca trabalhe direto na `main` ou na `develop`**
O GitHub bloqueia isso automaticamente.

**2. PR com WIP ao iniciar qualquer branch pessoal**
Trabalho sem PR é trabalho invisível para o time.

**3. Push ao final de cada etapa significativa**
Trabalho não pushed é perdido se a instância cair.

**4. Uma demanda por branch, uma pessoa por branch pessoal**
Não misture demandas. Fica impossível revisar e rastrear.

**5. Nunca use modelos reais nos testes**
Apenas `tests/fixtures/`. Modelos reais não entram no repositório.

**6. Apareceu conflito? Para tudo e chama**
Não tente resolver sozinho.

---

## Padrão de commits

| Prefixo | Quando usar |
|---|---|
| `feat:` | nova funcionalidade na skill |
| `fix:` | correção de comportamento |
| `docs:` | só documentação |
| `test:` | fixtures ou casos de teste |
| `refactor:` | reestruturação sem mudar comportamento |

---

## Dúvidas frequentes

**Posso trabalhar na mesma demanda que outra pessoa?**
Sim — cada um na sua branch pessoal. O Claude consolida no PR da demanda.

**Não sei o nome da branch que devo usar:**
> "Quais demandas estão abertas e quais são suas branches?"

**Preciso instalar alguma coisa?**
Não. O MCP GitHub está configurado. Tudo é feito via linguagem natural.

---

## Fluxo completo de um dia de trabalho

### Ligando a instância

1. Ligar a instância no SageMaker
2. Abrir terminal e rodar o setup do repo da equipe:
   ```
   cd ../repo-equipe && bash setup.sh
   ```
3. Entrar no repositório do projeto:
   ```
   cd ../repo-modelagem
   ```

### Iniciando a sessão

**Primeira vez trabalhando nesta demanda:**
```
claude -n feature/[nome-da-demanda]-[seu-nome]
```

**Retomando sessão anterior (instância reiniciada ou nova sessão):**
```
claude --resume feature/[nome-da-demanda]-[seu-nome]
```

O Claude faz o restante automaticamente: lê o contexto, verifica a branch,
verifica se está atualizada e abre o PR com WIP se ainda não existir.

### Durante o trabalho

Trabalhe normalmente — peça ao Claude alterações, testes, revisões.
O Claude faz push ao final de cada etapa significativa sem você precisar lembrar.

Se precisar de uma pausa longa (reunião, almoço), peça antes de sair:
> "Salva tudo antes de eu pausar"

### Encerrando o dia

Antes de desligar a instância, peça ao Claude:

> "Encerra a sessão do dia"

O Claude executa em sequência:
1. Commit e push de tudo que estiver pendente
2. Confirmação de que nenhum modelo real foi adicionado
3. Atualização do `docs/planejamento.md` se alguma demanda avançou
4. Resumo do que foi feito — útil para retomar amanhã

Só depois desse encerramento desligue a instância.

### Retomando no dia seguinte

```
cd ../repo-equipe && bash setup.sh
cd ../repo-modelagem
claude --resume feature/[nome-da-demanda]-[seu-nome]
```

O Claude retoma a sessão com contexto completo do dia anterior.
