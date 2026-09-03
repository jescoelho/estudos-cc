# Ciclo de Vida de um Dado Externo Democratizado

## O olhar técnico do todo — da demanda até o dado disponível

-----

## Por que pensar em “ciclo de vida”

Um dado externo não é um evento único (“extraí e acabou”) — é um processo com estágios,
cada um com entrada, saída, e um tipo de decisão diferente. Entender o ciclo de vida é
entender **onde cada estágio começa e termina**, e **o que muda de mãos** entre eles
(de negócio pra dados, de dados pra infra, de infra pra governança, etc.).

O olhar técnico que você precisa ter não é “eu sei escrever o código de cada etapa” — é
**“eu sei nomear as etapas, sei o que entra e sai de cada uma, e sei dizer se aquela etapa
foi mecânica ou exigiu julgamento humano.”** Isso é suficiente pra desenhar automação.

-----

## Os 6 Estágios Universais

Todo dado externo — não importa se é API, arquivo, scraping ou webhook — passa por estes
estágios, em alguma forma:

### 1. Demanda e Descoberta da Fonte

**O que é**: alguém precisa de um dado que vem de fora da empresa. A fonte é identificada
(URL, API, arquivo, sistema de terceiro).

**Entrada**: um pedido de negócio (às vezes vago: “precisamos dos dados de X”)
**Saída**: uma fonte concreta e localizável (link, endpoint, protocolo de acesso)

**Perguntas que definem esse estágio**:

- A fonte já é conhecida ou precisa ser pesquisada?
- Existe documentação da fonte (API docs, layout de arquivo)?
- Qual é o tipo de acesso (público, autenticado, pago, via convênio)?

**🔎 Se sua empresa opera em DataMesh, observe aqui**:

- Esse dado pertence a um data product que já existe, ou vai nascer um data product novo?
- Existe um domínio de negócio já definido como “dono” natural desse dado, ou isso ainda
  precisa ser decidido?

-----

### 2. Exploração e Caracterização da Fonte

**O que é**: entender a “forma” do dado antes de construir qualquer coisa — schema,
frequência de atualização, volume, formato, estabilidade.

**Entrada**: a fonte identificada
**Saída**: um entendimento do padrão — schema esperado, frequência, tipo de fonte (pull/push)

**Perguntas que definem esse estágio**:

- O schema é fixo ou muda com frequência?
- A fonte é confiável (uptime, documentação precisa) ou instável?
- Existe algum tipo de rate limit, autenticação, ou restrição de acesso?
- O dado já se parece com algo que a empresa já processa (posso reaproveitar padrão)?

Este é o estágio onde mais aparece **incerteza real** — é aqui que humano (ou agente)
precisa investigar, não seguir receita.

**🔎 Se sua empresa opera em DataMesh, observe aqui**:

- Em qual camada esse dado vai cair (raw, processed, curated) segundo a convenção da empresa?
- Já existe um SLA padrão esperado pra dados externos desse tipo, ou isso é definido caso a caso?

-----

### 3. Extração e Processamento

**O que é**: pegar o dado bruto da fonte e transformá-lo em algo estruturado e utilizável
(parsing, limpeza, normalização de schema, validação).

**Entrada**: dado bruto (JSON, CSV, HTML, XML — o que a fonte entregar)
**Saída**: dado estruturado, validado, num formato consumível (ex: Parquet)

**Perguntas que definem esse estágio**:

- O parsing é genérico (reaproveitável) ou específico daquela fonte?
- Há necessidade de enriquecimento (juntar com outro dado)?
- Como é feita a validação de qualidade (schema, nulos, duplicados)?
- O que acontece se o schema mudar de uma execução pra outra?

Este é tipicamente o estágio **mais mecânico** quando o padrão já existe — e o mais
manual/trabalhoso quando é a primeira vez com aquele tipo de fonte.

-----

### 4. Provisionamento de Infraestrutura

**O que é**: criar os recursos técnicos que vão hospedar e orquestrar esse dado de forma
recorrente — armazenamento, agendamento, permissões, monitoramento.

**Entrada**: o dado processado + o padrão de acesso definido no estágio 2
**Saída**: infraestrutura viva (buckets, jobs agendados, permissões, alertas configurados)

**Perguntas que definem esse estágio**:

- Existe um template/módulo reutilizável ou cada fonte exige infra sob medida?
- Quem aprova a criação de novos recursos (custo, segurança, compliance)?
- Como fica documentado o “dono” técnico desse recurso?

Este estágio costuma ser o mais **regrado e burocrático** — é onde entram políticas de
governança, custo e segurança da empresa.

**🔎 Se sua empresa opera em DataMesh, observe aqui**:

- O template de infra que você reaproveita é agnóstico, ou já carrega convenções de
  DataMesh embutidas (nomenclatura por domínio, tags de data product, etc.)?
- A aprovação de novo recurso passa só por infra/segurança, ou também por alguém do
  domínio de negócio dono do data product?

-----

### 5. Catalogação e Governança

**O que é**: registrar formalmente que esse dado existe, o que ele significa, quem pode
acessar, e sob quais regras — pra que outras pessoas o encontrem e usem corretamente.

**Entrada**: o dado + a infraestrutura já provisionada
**Saída**: um registro público (dentro da empresa) do dado, com metadados, classificação
de sensibilidade, e regras de acesso

**Perguntas que definem esse estágio**:

- Quem tem autoridade pra aprovar a publicação desse dado?
- Existe classificação obrigatória (sensível, público, restrito)?
- O catálogo é só documentação ou também controla acesso técnico (permissões)?

Este é o estágio onde **decisão humana é quase sempre obrigatória** — envolve
responsabilidade e compliance, não só técnica.

**🔎 Se sua empresa opera em DataMesh, observe aqui — é o ponto mais crítico**:

- Quem fica registrado como data product owner desse dado?
- Que informação de “contrato de dados” (schema garantido, SLA, forma de acesso) você
  precisa registrar pra quem for consumir?
- Existe campo de linhagem (de onde veio, quem processou) exigido pelo catálogo?

-----

### 6. Disponibilização e Consumo

**O que é**: o dado está, de fato, acessível pra quem precisa — via consulta SQL,
dashboard, API interna, ou outro canal.

**Entrada**: o dado catalogado e com infraestrutura ativa
**Saída**: alguém de negócio consegue usar o dado sem precisar entender como ele chegou ali

**Perguntas que definem esse estágio**:

- Como o consumidor final descobre que esse dado existe?
- Existe SLA de atualização (o dado é atualizado com que frequência, e isso é confiável)?
- Existe canal de feedback se o dado parar de funcionar ou mudar?

-----

## O olhar técnico que amarra tudo

Pra cada estágio, pergunte sempre as mesmas 3 coisas:

1. **Isso é mecânico ou exige julgamento?** (Mecânico = repetível, sem ambiguidade.
   Julgamento = exige contexto, negociação, ou decisão de risco.)
1. **Isso muda por tipo de fonte, ou é igual não importa a fonte?** (Se muda muito,
   um agente precisa de lógica específica por tipo. Se é igual, é mais fácil generalizar.)
1. **Quem teria que aprovar isso, mesmo que um agente fizesse todo o resto?** (Aponta
   onde humano fica no loop, não importa o quão autônomo o agente seja.)

-----

## Como isso se conecta com a POC

Quando você documentar o que fez com a DTCC (ou qualquer outra fonte), a pergunta não é
“quanto tempo levei” — é: **“em qual desses 6 estágios eu vivi mais fricção, e aquela
fricção era mecânica (automatizável) ou exigia julgamento (fica com humano)?”**

Isso te dá, estágio por estágio, um mapa de onde o agente orquestrador realmente ajudaria —
e onde ele sempre vai precisar te chamar de volta.

-----

## Nota sobre DataMesh

Os marcadores 🔎 acima não são um estágio a mais — DataMesh não é uma etapa do ciclo de
vida, é um **modelo de organização que atravessa todo o ciclo**: define quem é dono do
dado, como ele é oferecido a quem consome, e que governança descentralizada existe por
trás disso. Por isso ele aparece dentro de vários estágios, não como um estágio próprio.

Os 4 pontos que mais valem observação direta na prática (não dá pra responder de forma
genérica, precisa ver como o Itaú implementou):

1. **Estágio 1** — quem é/será o data product owner
1. **Estágio 2** — em qual camada o dado cai e qual SLA é esperado
1. **Estágio 4** — se o template de infra já embute convenções de DataMesh
1. **Estágio 5** — que informação de contrato/linhagem o catálogo exige