# Guia de Construção e Storytelling
## Curvas em Risco e Tesouraria: o que dados e analytics precisam entender para entregar valor

---

## Premissas de construção

**Tese central**
Entender a construção matemática de curvas é o que transforma analytics de suporte técnico em parceiro estratégico.

**Fio condutor narrativo**
As mesas negociam. O mercado liquida. O risco mede. A tesouraria decide. A curva atravessa tudo isso — e quem a entende age antes que o mercado se mova.

**Princípio de linguagem**
Intuição antes de formalismo. Conceito antes de sigla. Negócio antes de modelo. Em todo slide, a primeira frase deve ser compreensível por alguém sem formação técnica.

**Público**
Pares e coordenadora de área de dados e analytics que atende risco de mercado e tesouraria bancária.

**Duração**
20 a 30 minutos. 15 slides. Abertura para perguntas ao final.

---

## Estrutura macro

```
Bloco 0 — Abertura          Slides 01–02    Criar tensão narrativa
Bloco 1 — O que é curva     Slides 03–05    Construir vocabulário comum
Bloco 2 — Negócio           Slides 06–10    Mostrar a cadeia de valor
Bloco 3 — Analytics         Slides 11–13    Posicionar o papel da área
Bloco 4 — Fechamento        Slides 14–15    Fechar o loop narrativo
```

---

## Bloco 0 — Abertura

### Slide 01 — Título

**Intenção**
Estabelecer o recorte e a tese antes de qualquer palavra ser dita. O slide precisa trabalhar sozinho enquanto a audiência se acomoda.

**Objetivo**
A audiência deve sair desse slide sabendo exatamente o que vai ser apresentado e sentindo que o tema é relevante para ela.

**Elementos obrigatórios**
- Título principal: recorte explícito em risco e tesouraria
- Subtítulo: tese enunciada sem ser desenvolvida
- Nenhum elemento decorativo que distraia

**Tom de abertura oral**
Ativar o histórico profissional da apresentadora de forma orgânica — não como currículo, mas como fundamento da autoridade sobre o tema. A conexão entre experiência em clearing e atuação atual em analytics deve ser feita em no máximo três frases.

**Armadilhas**
- Não colocar data, área ou nome de quem solicitou no slide de título
- Não colocar subtítulo que responda a tese antes de desenvolvê-la
- Não ler o slide em voz alta

**Referências para embasar**
Nenhuma referência formal nesse slide.

---

### Slide 02 — Problema de negócio

**Intenção**
Fazer a audiência se reconhecer nas perguntas antes de saber que você vai respondê-las. Criar desconforto produtivo — o silêncio do não-respondido é o que segura a atenção.

**Objetivo**
A audiência deve terminar esse slide com uma pergunta na cabeça, não com uma resposta. A tensão narrativa criada aqui precisa ser sustentada até o Slide 14.

**Elementos obrigatórios**
- Três perguntas em linguagem de negócio puro, sem jargão técnico
- As perguntas em ordem crescente de sofisticação
- Uma frase de fechamento que sinalize conexão entre as três perguntas
- Nenhuma resposta — nem implícita

**Estrutura das perguntas**
Cada pergunta deve tocar em um domínio diferente da cadeia de valor:
- Primeira: impacto direto de movimento de mercado na carteira
- Segunda: resultado por área e custo de funding
- Terceira: validade dos cenários de stress

**Tom oral**
Fazer pausa de dois segundos entre cada pergunta. Não comentar. Não antecipar. A frase de fechamento é dita devagar.

**Armadilhas**
- Não usar siglas nas perguntas (sem MTM, FTP, stress testing, VaR)
- Não colocar bullet points com sub-explicações
- Não responder parcialmente para "adiantar" o conteúdo
- Não colocar mais de três perguntas

**Referências para embasar**
Nenhuma referência formal nesse slide.

---

## Bloco 1 — O que é uma curva

### Slide 03 — Intuição: o que toda curva representa

**Intenção**
Quebrar a resistência de quem ouve "curva" e pensa imediatamente em complexidade matemática. Estabelecer que o conceito é familiar antes de formalizá-lo.

**Objetivo**
A audiência deve terminar esse slide com uma definição intuitiva de curva que funcione para qualquer domínio — não apenas para finanças. Essa definição será o framework tácito para todos os slides seguintes.

**Elementos obrigatórios**
- Exemplo completamente fora de finanças que qualquer pessoa já viveu
- Transição do exemplo cotidiano para finanças sem quebra de lógica
- Frase de fechamento que generalize o conceito para qualquer domínio

**Frase âncora**
Deve haver uma frase curta e memorável que sintetize o conceito. Essa frase será o ponto de retorno implícito toda vez que um novo tipo de curva for introduzido nos slides seguintes.

**Tom oral**
Conversacional. Esse é o slide mais informal da apresentação — é o momento de baixar a guarda da audiência antes de elevar a complexidade.

**Armadilhas**
- Não colocar definição formal matemática
- Não introduzir múltiplos tipos de curva — isso vem no Slide 04
- Não usar o termo ETTJ ainda
- Não colocar fórmulas

**Referências para embasar**
Nenhuma referência formal nesse slide.

---

### Slide 04 — O ecossistema de curvas no banco

**Intenção**
Mostrar que o banco vive em um espaço multidimensional de curvas — cada fator de risco relevante tem a sua. Demonstrar visão sistêmica antes de afunilar para juros.

**Objetivo**
A audiência deve terminar esse slide com a clareza de que o aprofundamento em juros é uma escolha de recorte, não uma limitação de escopo. E deve entender que analytics serve todas essas curvas, não apenas uma.

**Elementos obrigatórios**
- Mapa visual com todas as curvas relevantes para risco e tesouraria
- Uma linha descritiva para cada curva — onde aparece no banco e o que representa
- Destaque visual explícito para curvas de juros como caso base
- Frase oral que justifica o recorte sem pedir desculpa por ele
- Semente plantada sobre o papel de analytics em relação ao ecossistema

**Curvas a incluir**
Juros prefixados, cupom de IPCA, câmbio e cupom cambial, crédito e spread sobre DI, inflação implícita, commodities, volatilidade. Nota sobre volatilidade: tecnicamente é uma superfície — dois parâmetros — não uma curva.

**Tom oral**
Panorâmico e seguro. Esse slide demonstra amplitude de visão — o tom deve refletir isso. Não é um slide de listagem, é um slide de mapeamento.

**Armadilhas**
- Não entrar em detalhe de nenhuma curva além de juros
- Não usar siglas sem explicar na primeira menção
- Não tentar cobrir todas as curvas com o mesmo nível de profundidade
- Não omitir a justificativa do recorte — a audiência vai notar se faltar

**Referências para embasar**
- Souza, I.A. (2017) — Dissertação UnB: cobre fatores de risco no banco, trading book e banking book
- `https://repositorio.unb.br/bitstream/10482/31108/1/2017_IramAlvesdeSouza.pdf`

---

### Slide 05 — Construção matemática: curva de juros

**Intenção**
Entregar o núcleo técnico da apresentação de forma que qualquer pessoa na sala entenda o que os parâmetros significam — sem precisar saber resolver a equação.

**Objetivo**
A audiência deve terminar esse slide sabendo responder: o que é Nelson-Siegel, o que cada parâmetro controla em linguagem econômica, e por que a ANBIMA usa esse modelo. O slide deve criar o vocabulário técnico que será acionado nos Blocos 2 e 3.

**Elementos obrigatórios**
- Camada 1: intuição sobre o que a curva de juros representa economicamente
- Camada 2: tabela de parâmetros com significado econômico em linguagem simples
- Camada 3: fórmula de Nelson-Siegel com cada termo rotulado em português coloquial diretamente no slide
- Menção oral ao modelo Svensson como extensão usada pela ANBIMA
- Frase de fechamento que conecta a construção matemática para o uso em negócio

**Sobre a fórmula**
A equação deve aparecer. As legendas de cada termo devem estar no slide — não em nota de rodapé. Quem não sabe matemática lê as legendas. Quem sabe matemática lê a equação. Os dois grupos são atendidos pelo mesmo elemento visual.

**Sobre os parâmetros**
Cada parâmetro tem duas representações no slide: o símbolo matemático e o significado econômico em linguagem direta. O significado econômico é o que a audiência vai lembrar.

**Tom oral**
Três camadas explicitadas em voz alta. A apresentadora deve sinalizar para a audiência que está construindo em camadas — isso reduz a ansiedade de quem não tem formação técnica.

**Armadilhas**
- Não derivar a fórmula
- Não explicar bootstrap nem calibração numérica
- Não colocar Nelson-Siegel e Svensson no mesmo slide com mesmo nível de detalhe
- Não colocar mais de uma equação
- Não colocar legendas em nota de rodapé

**Referências para embasar**
- ANBIMA — Estrutura a Termo das Taxas de Juros Estimada e Inflação Implícita: Metodologia
- `https://www.anbima.com.br/data/files/18/42/65/50/4169E510222775E5A8A80AC2/est-termo_metodologia.pdf`
- Caldeira, J.F. (2011) — Estimação da Estrutura a Termo da Curva de Juros no Brasil
- `https://seer.ufrgs.br/AnaliseEconomica/article/view/13198`

---

## Bloco 2 — Como o negócio usa curvas

### Slide 06 — A cadeia de valor: mesas → mercado → risco → tesouraria

**Intenção**
Estabelecer o mapa narrativo do bloco inteiro antes de entrar em qualquer detalhe. A audiência vai usar esse diagrama como referência para os quatro slides seguintes.

**Objetivo**
A audiência deve terminar esse slide com uma imagem mental clara da cadeia — quem faz o quê, em que ordem, e onde analytics se encaixa. Esse slide também é onde o histórico profissional da apresentadora entra de forma mais natural e direta.

**Elementos obrigatórios**
- Diagrama linear com quatro elos: mesas, mercado, risco, tesouraria
- Uma frase descritiva para cada elo — função, não detalhe operacional
- Conexão explícita entre o elo de mercado e a experiência em clearing
- Posicionamento de analytics como servidora de toda a cadeia — não de um elo específico
- Frase de fechamento que planta a pergunta: o que analytics precisa entender para servir bem?

**Sobre o histórico B3**
Esse é o momento mais natural para ativar a experiência em clearing. Não como dado de currículo, mas como argumento: quem trabalhou na infraestrutura que garante a liquidação entende o que as mesas geram e o que o mercado exige.

**Tom oral**
Fluido e seguro. Esse slide é o mais narrativo do bloco — não tem fórmulas, não tem tabelas. É pura condução oral apoiada em um diagrama simples.

**Armadilhas**
- Não detalhar o funcionamento interno das mesas
- Não usar setas bidirecionais no diagrama — a cadeia tem um fluxo dominante
- Não mencionar middle office ou back office como elos separados
- Não colocar texto demais no slide — o diagrama faz o trabalho visual

**Referências para embasar**
- Souza, I.A. (2017) — Dissertação UnB: modelo de três linhas de defesa, mesas de tesouraria e limites de risco
- `https://repositorio.unb.br/bitstream/10482/31108/1/2017_IramAlvesdeSouza.pdf`
- BACEN — Circular 3.082/2002: registro e avaliação de instrumentos financeiros derivativos
- `https://normativos.bcb.gov.br/Lists/Normativos/Attachments/46969/Circ_3082_v5_P.pdf`

---

### Slide 07 — Tesouraria: MTM e FTP

**Intenção**
Mostrar como a curva calibrada vira preço justo de carteira e custo interno de funding. Esse slide responde as perguntas 1 e 2 do Slide 02 — sem anunciar que está fazendo isso.

**Objetivo**
A audiência deve terminar esse slide entendendo que MTM e FTP são dois usos distintos da mesma curva — e que sem curva nenhum dos dois funciona corretamente.

**Elementos obrigatórios**
- Intuição de MTM: o que acontece com o valor de um título quando a taxa sobe
- Mecanismo formal de MTM em uma linha: desconto de fluxo pela curva vigente
- Menção à ANBIMA como fonte de taxas indicativas para MaM
- Intuição de FTP: o que acontece quando o custo de funding não é transferido corretamente
- Consequência prática de FTP mal calculado: resultado distorcido por área
- Transição oral para o próximo slide

**Sobre a sequência MTM → FTP**
MTM e FTP são apresentados no mesmo slide porque compartilham o mesmo insumo — a curva — e porque juntos respondem às duas primeiras perguntas do Slide 02. A ordem é proposital: MTM é mais concreto e abre o conceito, FTP é mais sofisticado e aprofunda.

**Tom oral**
Dois movimentos claramente separados. A transição entre MTM e FTP deve ser sinalizada com uma pergunta retórica que crie o vínculo entre os dois conceitos.

**Armadilhas**
- Não entrar na fórmula de desconto de fluxo de caixa
- Não explicar duration aqui — ela aparece no Slide 08
- Não usar a sigla MTM antes de explicar o que significa
- Não tratar MTM e FTP como conceitos independentes — o vínculo é a curva

**Referências para embasar**
- ANBIMA — Metodologias ANBIMA de Precificação 2023
- `https://www.anbima.com.br/data/files/9E/67/9D/6F/382788107D83F688EA2BA2A8/Metodologias-ANBIMA-de%20Precificacao-2023.pdf`
- ANBIMA — Regras e Procedimentos para Apuração de Valores de Referência
- `https://www.anbima.com.br/data/files/5F/A6/3B/BE/9BB2E710C19FACD7882BA2A8/metodologia-curvas_20credito_20131104_v2_1_.pdf`
- Artigo FTP — UFSC (2008)
- `https://periodicos.ufsc.br/index.php/contabilidade/article/view/2175-8069.2008v5n9p95`
- Checoli, A.G. — Dissertação FGV
- `https://repositorio.fgv.br/bitstreams/1ddc13f2-cd19-4b15-93b3-e09aa1f0d15d/download`

---

### Slide 08 — Tesouraria: ALM e posicionamento

**Intenção**
Elevar o argumento de precificação para decisão estratégica. Mostrar que tesouraria não apenas calcula — ela decide com base na leitura da curva.

**Objetivo**
A audiência deve terminar esse slide entendendo que o descasamento de ativos e passivos é o risco estrutural do banco — e que a curva é o instrumento que o tesoureiro usa para gerenciá-lo e se posicionar antes dos movimentos de mercado.

**Elementos obrigatórios**
- Descrição intuitiva do descasamento estrutural banco: captação curta, empréstimo longo
- Conceito de gap de reprecificação em linguagem simples
- Menção às métricas regulatórias ∆EVE e ∆NII como exigência — não como detalhe técnico
- Introdução de steepener e flattener como leituras de ciclo monetário
- Semente da tese de antecipação: posicionamento antes do COPOM, não depois
- Transição oral para risco de mercado

**Sobre ALM e regulação**
A CMN 4.557 e a Circular 3.876 precisam aparecer aqui — não para detalhar as métricas, mas para mostrar que a gestão do descasamento é exigência regulatória. Isso ancora o argumento no mundo real do banco, não em teoria.

**Tom oral**
Dois movimentos: primeiro o problema estrutural, depois a resposta estratégica. O tom sobe no segundo movimento — é onde a dimensão de antecipação aparece pela primeira vez.

**Armadilhas**
- Não entrar nas fórmulas de ∆EVE e ∆NII
- Não abrir hedge com derivativos como subtema
- Não tratar duration como tópico autônomo — menção de passagem apenas
- Não confundir ALM com trading — são carteiras e riscos distintos

**Referências para embasar**
- BACEN — Resolução CMN 4.557/2017
- `https://normativos.bcb.gov.br/Lists/Normativos/Attachments/50344/Res_4557_v4_P.pdf`
- BACEN — Circular 3.876/2018 — Metodologias para mensuração do IRRBB
- `https://www.bcb.gov.br/pre/normativos/busca/normativo.asp?tipo=Circular&ano=2018&numero=3876`

---

### Slide 09 — Risco: DV01, sensibilidades e PCA

**Intenção**
Mostrar como risco de mercado transforma exposição em curva em número gerenciável. Fechar o loop com Nelson-Siegel: os componentes do PCA correspondem aos parâmetros β do Slide 05.

**Objetivo**
A audiência deve terminar esse slide entendendo DV01 como métrica operacional de risco e PCA como instrumento de redução de dimensionalidade — e reconhecendo que os três fatores do PCA são os mesmos três parâmetros que apareceram no Slide 05.

**Elementos obrigatórios**
- Intuição de DV01: quanto o portfólio perde para cada basis point de movimento
- DV01 por vértice como mapa de sensibilidade da carteira
- Problema de dimensionalidade: dezenas de vértices que se movem juntos
- PCA como solução: três componentes que explicam ~97% da variância histórica
- Interpretação econômica dos três componentes: nível, inclinação, curvatura
- Conexão explícita entre PC1/PC2/PC3 e β₀/β₁/β₂ do Nelson-Siegel

**Sobre o fechamento do loop**
A conexão entre PCA e Nelson-Siegel é o insight técnico mais sofisticado da apresentação. Ela não deve ser anunciada como "agora vou conectar" — deve ser apresentada como uma observação natural: "não é coincidência".

**Tom oral**
Dois movimentos com clareza: DV01 como métrica operacional, PCA como instrumento de gestão. A conexão com Nelson-Siegel é dita com confiança — não como curiosidade acadêmica, mas como argumento de negócio.

**Armadilhas**
- Não explicar a matemática do PCA — autovalores e autovetores ficam fora
- Não confundir DV01 com duration
- Não colocar gráfico de variância explicada sem tempo para comentá-lo
- Não deixar a conexão PCA-Nelson-Siegel implícita — ela precisa ser dita

**Referências para embasar**
- Caldeira, J.F. (2011) — Estimação da Estrutura a Termo da Curva de Juros no Brasil
- `https://seer.ufrgs.br/AnaliseEconomica/article/view/13198`
- BACEN — Resolução CMN 4.557/2017
- `https://normativos.bcb.gov.br/Lists/Normativos/Attachments/50344/Res_4557_v4_P.pdf`

---

### Slide 10 — Risco: stress testing regulatório

**Intenção**
Mostrar por que stress testing vai além do VaR — e por que a forma como os choques são aplicados na curva determina se o cenário é válido ou impossível. Fechar o Bloco 2 e abrir o Bloco 3.

**Objetivo**
A audiência deve terminar esse slide entendendo que chocar parâmetros β da curva é mais robusto que chocar vértices isolados — e que a regulação brasileira exige que o banco domine esse processo. A última frase deve criar expectativa para o Bloco 3.

**Elementos obrigatórios**
- Limitação do VaR: mede risco em condições normais, não em crise
- Três tipos de choque na curva: paralelo, inclinação, curvatura
- Argumento de por que chocar β é mais robusto que chocar vértices
- Âncora regulatória: CMN 4.557 e Relatório de Estabilidade Financeira do BACEN
- Frase de fechamento que abre o Bloco 3 com a dimensão de antecipação

**Sobre a conexão com blocos anteriores**
Os três tipos de choque correspondem aos três parâmetros β do Slide 05 e aos três componentes do PCA do Slide 09. A apresentadora deve fazer essa conexão de forma explícita — é o terceiro momento em que o mesmo conceito aparece, o que demonstra coerência do argumento.

**Tom oral**
Dois movimentos: primeiro a limitação do VaR, depois a solução pelo stress. O fechamento deve elevar o tom — é a última frase do bloco mais técnico da apresentação.

**Armadilhas**
- Não entrar em backtesting ou PLAT como subtema
- Não comparar métodos de VaR (histórico, Monte Carlo, paramétrico)
- Não colocar mais de três tipos de choque
- Não deixar a frase de fechamento no slide — deve ser dita oralmente

**Referências para embasar**
- BACEN — Resolução CMN 4.557/2017
- `https://normativos.bcb.gov.br/Lists/Normativos/Attachments/50344/Res_4557_v4_P.pdf`
- BACEN — Relatório de Estabilidade Financeira — Capítulo de Cenários de Estresse
- `https://www.bcb.gov.br/content/publicacoes/ref/200305/RELESTAB2003-PortuguesCapitulo4.pdf`
- BACEN — Circulares 3.634 a 3.645/2013 — RWA de risco de mercado
- `https://www.bcb.gov.br/pre/normativos/busca/normativo.asp?tipo=Circular&ano=2013&numero=3634`

---

## Bloco 3 — O papel de analytics na cadeia

### Slide 11 — O que analytics entrega para cada elo da cadeia

**Intenção**
Espelhar o Slide 06 — mesma cadeia, nova camada. Mostrar que analytics não é periférico à cadeia de valor, mas componente estrutural de cada elo.

**Objetivo**
A audiência deve terminar esse slide com uma imagem clara do que analytics entrega em cada etapa — não como lista de tarefas, mas como mapa de valor. O posicionamento deve ser de quem serve a cadeia com qualidade, não de quem a apoia operacionalmente.

**Elementos obrigatórios**
- Retomada visual do diagrama do Slide 06
- Para cada elo da cadeia: uma entrega específica de analytics
- As entregas devem ser descritas em termos de valor gerado, não de ferramenta usada
- Frase de fechamento que enuncia o argumento central: analytics transforma dado em capacidade de decisão

**Sobre o tom de posicionamento**
Esse slide é o primeiro do bloco de argumento de promoção. O vocabulário importa: usar "entrega", "transforma", "operacionaliza" — nunca "apoia", "suporta", "auxilia".

**Sobre as entregas por elo**
Cada entrega deve ser específica o suficiente para ser crível e genérica o suficiente para não revelar projetos confidenciais. O nível correto é o da capacidade entregue, não do projeto executado.

**Armadilhas**
- Não listar tecnologias ou ferramentas
- Não colocar exemplos de projetos por nome
- Não usar a palavra "suporte" em nenhuma forma
- Não colocar mais de uma entrega por elo — a síntese demonstra julgamento

**Referências para embasar**
Nenhuma referência formal nesse slide — o argumento é de posicionamento da área, não de embasamento técnico.

---

### Slide 12 — Por que a construção matemática importa para dados

**Intenção**
Materializar o argumento de promoção com situações concretas onde o conhecimento matemático muda a qualidade da entrega de analytics.

**Objetivo**
A audiência deve terminar esse slide convicta de que conhecer a construção da curva não é ornamento acadêmico — é o que determina se o resultado de analytics é confiável. Esse é o slide que mais diretamente sustenta o argumento de senioridade.

**Elementos obrigatórios**
- Três situações concretas onde o conhecimento de construção de curva muda o resultado
- Situação 1: validação de dado — distinguir erro de dado de movimento legítimo
- Situação 2: identificação de anomalia — reconhecer instabilidade numérica vs sinal real
- Situação 3: explicação para o cliente interno — traduzir resultado em linguagem de negócio
- Frase de fechamento que generaliza: dado → informação → decisão

**Sobre as situações**
As três situações devem soar reais sem depender de exemplos específicos. O nível de abstração correto é o de padrões recorrentes — situações que qualquer pessoa na sala já viveu ou pode imaginar.

**Sobre a frase de fechamento**
A frase que generaliza o argumento é o ponto mais alto do bloco. Deve ser dita devagar e com pausa depois — é a frase que a coordenadora vai lembrar.

**Armadilhas**
- Não transformar em lista de competências
- Não citar erros passados como exemplos
- Não usar exemplos tão específicos que pareçam inventados
- Não colocar a frase de fechamento como bullet — ela é o fechamento oral do slide

**Referências para embasar**
- ANBIMA — Estrutura a Termo das Taxas de Juros Estimada e Inflação Implícita: Metodologia
- `https://www.anbima.com.br/data/files/18/42/65/50/4169E510222775E5A8A80AC2/est-termo_metodologia.pdf`
- Caldeira, J.F. (2011)
- `https://seer.ufrgs.br/AnaliseEconomica/article/view/13198`
- BACEN Working Paper 186 — Previsão da Curva de Juros no Brasil
- `https://aprendervalor.bcb.gov.br/content/publicacoes/WorkingPaperSeries/wps186.pdf`

---

### Slide 13 — O que a curva sinaliza antes do evento

**Intenção**
Consolidar a tese de antecipação com sinais verificáveis que a curva carrega todos os dias. Mostrar que analytics que entende a construção consegue extrair esses sinais e transformá-los em insumo para decisão antes do evento.

**Objetivo**
A audiência deve terminar esse slide com a tese central completamente materializada — e com o eco do Slide 01 na cabeça, mesmo que não perceba conscientemente. A última frase do slide retoma a tese sem anunciá-la.

**Elementos obrigatórios**
- Três sinais concretos que a curva carrega: inflação implícita, inclinação como proxy de ciclo, prêmio de risco no longo prazo
- Para cada sinal: o que ele indica e quando indica antes do evento
- Conexão entre cada sinal e uma ação de risco ou tesouraria
- Papel de analytics na extração e monitoramento desses sinais
- Frase de fechamento que retoma a tese do Slide 01 sem apontar para isso

**Sobre os sinais**
Cada sinal deve ter uma âncora de referência verificável — inflação implícita na metodologia ANBIMA, inclinação no Relatório de Estabilidade Financeira, prêmio de risco nos Working Papers do BACEN. Os sinais não são especulação — são objetos mensuráveis.

**Sobre o fechamento**
A última frase do Slide 13 é a frase que fecha o arco narrativo de toda a apresentação. Ela não está no slide — é oral. E ela deve ecoar a tese do Slide 01 sem copiá-la literalmente.

**Armadilhas**
- Não citar eventos históricos específicos com datas
- Não usar modelos de previsão como argumento
- Não usar a palavra "previsão" — usar "sinal", "antecipação", "posicionamento"
- Não anunciar que está retomando a tese — deixar o eco acontecer

**Referências para embasar**
- ANBIMA — Estrutura a Termo das Taxas de Juros Estimada e Inflação Implícita: Metodologia
- `https://www.anbima.com.br/data/files/18/42/65/50/4169E510222775E5A8A80AC2/est-termo_metodologia.pdf`
- BACEN Working Paper 359 — Decompondo a Inflação Implícita
- `https://www.bcb.gov.br/pec/wps/port/TD359.pdf`
- BACEN — Relatório de Estabilidade Financeira (edição mais recente)
- `https://www.bcb.gov.br/publicacoes/ref`

---

## Bloco 4 — Fechamento

### Slide 14 — Voltando às três perguntas

**Intenção**
Fechar o loop narrativo aberto no Slide 02. Mostrar que o caminho percorrido foi intencional e chegou a algum lugar — e que a audiência agora tem as respostas que não tinha no começo.

**Objetivo**
A audiência deve terminar esse slide com a sensação de que o argumento foi completo e coerente — e com a tese central dita de forma direta pela apresentadora pela primeira vez em voz alta.

**Elementos obrigatórios**
- Retomada visual do Slide 02 — mesmo layout, mesmas três perguntas
- Uma resposta de uma linha para cada pergunta
- Pausa depois da terceira resposta
- Frase de fechamento das três perguntas no slide
- Frase de fechamento do argumento central dita oralmente — não no slide

**Sobre o efeito de espelho**
Usar o mesmo layout do Slide 02 é um recurso retórico deliberado. A audiência reconhece o padrão e o efeito é de completude — o círculo se fechou. Não é preciso apontar para isso — acontece automaticamente.

**Sobre a frase oral de fechamento**
Essa é a frase mais importante da apresentação inteira. É onde o argumento de promoção é dito de forma mais direta. Deve ser preparada e ensaiada — não improvisada.

**Armadilhas**
- Não colocar um quarto ponto depois das três respostas
- Não abrir para perguntas nesse slide — perguntas vêm depois do Slide 15
- Não colocar a frase de fechamento do argumento no slide — deve ser oral
- Não resumir o conteúdo dos blocos anteriores — as respostas já fazem isso

**Referências para embasar**
Nenhuma referência formal nesse slide.

---

### Slide 15 — Referências

**Intenção**
Sinalizar que o argumento tem base verificável. Esse slide não é lido — é mostrado.

**Objetivo**
A audiência deve terminar a apresentação com a percepção de que o que foi apresentado tem sustentação em fontes primárias — documentos regulatórios e produção acadêmica brasileira.

**Elementos obrigatórios**
- Duas seções visuais distintas: documentos regulatórios e institucionais / artigos e dissertações acadêmicas
- Máximo de 14 referências — mais do que isso não cabe com legibilidade
- Nenhuma URL no slide — oferta oral de enviar links por e-mail
- Agradecimento oral apenas — não em texto no slide

**Referências a incluir**

*Documentos regulatórios e institucionais*
- ANBIMA — ETTJ Metodologia
- ANBIMA — Metodologias de Precificação 2023
- ANBIMA — Regras e Procedimentos MaM
- BACEN — Resolução CMN 4.557/2017
- BACEN — Circular 3.876/2018 — IRRBB
- BACEN — Circulares 3.634-3.645/2013 — RWA de mercado
- BACEN — Circular 3.082/2002 — Derivativos
- BACEN — Relatório de Estabilidade Financeira

*Artigos e dissertações acadêmicas*
- Caldeira, J.F. (2011) — Análise Econômica UFRGS
- Artigo FTP — UFSC (2008)
- Checoli, A.G. — Dissertação FGV
- Souza, I.A. (2017) — Dissertação UnB
- BACEN Working Paper 186 — Previsão da Curva de Juros
- BACEN Working Paper 359 — Inflação Implícita

**Sobre referências excluídas**
Fortuna (Mercado Financeiro) e Morettin & Toloi (Análise de Séries Temporais) foram excluídos porque não foram consultados diretamente durante a construção deste guia. Referências não verificadas não entram no slide de fechamento.

**Armadilhas**
- Não colocar URLs completas no slide
- Não ler as referências em voz alta
- Não colocar mais de 14 referências
- Não terminar com slide de agradecimento — agradeça oralmente

---

## Mapa de referências por slide

| Slide | Referências |
|---|---|
| 01 | Nenhuma |
| 02 | Nenhuma |
| 03 | Nenhuma |
| 04 | Souza UnB 2017 |
| 05 | ANBIMA ETTJ Metodologia + Caldeira UFRGS 2011 |
| 06 | Souza UnB 2017 + BACEN Circular 3.082 |
| 07 | ANBIMA Precificação 2023 + ANBIMA MaM + Artigo FTP UFSC + Checoli FGV |
| 08 | CMN 4.557 + BACEN Circular 3.876 |
| 09 | Caldeira UFRGS 2011 + CMN 4.557 |
| 10 | CMN 4.557 + REF BACEN + Circulares 3.634-3.645 |
| 11 | Nenhuma |
| 12 | ANBIMA ETTJ Metodologia + Caldeira UFRGS 2011 + BACEN WP 186 |
| 13 | ANBIMA ETTJ Metodologia + BACEN WP 359 + REF BACEN |
| 14 | Nenhuma |
| 15 | Todas — consolidado |

---

## Orientação para perguntas

Três tipos de pergunta prováveis e como abordá-las:

**Pergunta técnica sobre modelagem**
Responder com o mecanismo geral. Se a pergunta for mais específica do que o escopo, é legítimo indicar a fonte e oferecer aprofundamento depois.

**Pergunta sobre aplicação na área**
Conectar com o trabalho real sem entrar em detalhe confidencial. O nível correto é o da capacidade entregue — não do projeto executado.

**Pergunta sobre o que ficou de fora**
Reconhecer o recorte como escolha deliberada e oferecer o próximo capítulo natural como continuação possível. Demonstrar que o recorte foi julgamento, não limitação.

---

*Guia elaborado com base nas referências listadas no Slide 15. Nenhuma referência não verificada foi incluída.*
