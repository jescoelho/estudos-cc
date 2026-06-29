# Curvas em Risco e Tesouraria: o que dados e analytics precisam entender para entregar valor

Material-base para apresentação de 20–30 minutos, 15 slides. Cada slide abaixo traz três blocos: **o que aparece na tela**, **o roteiro oral** (texto literal, palavra por palavra) e as **referências** que sustentam o conteúdo. Trechos entre colchetes no roteiro oral são notas de produção (pausas, tom) — não são falados.

**Tese central:** Entender a construção matemática de curvas é o que transforma analytics de suporte técnico em parceiro estratégico.

**Fio condutor:** As mesas negociam. O mercado liquida. O risco mede. A tesouraria decide. A curva atravessa tudo isso — e quem a entende age antes que o mercado se mova.

---

## Bloco 0 — Abertura

### Slide 01 — Título
*(tempo estimado: 30–40s)*

**O que aparece na tela**

Título: **Curvas em Risco e Tesouraria**
Subtítulo (tese enunciada, sem desenvolvimento): *Entender a construção matemática de curvas é o que transforma analytics de suporte técnico em parceiro estratégico.*

Sem data, sem nome de área, sem logotipo decorativo. Nenhum outro elemento no slide.

**Roteiro oral (texto literal)**

"Antes de trabalhar com dados e analytics, passei alguns anos dentro da infraestrutura que garante a liquidação das operações do mercado financeiro brasileiro — vendo de perto o que acontece depois que uma mesa fecha um negócio. Essa experiência me ensinou que, por trás de cada preço, cada ajuste e cada risco medido, existe uma curva fazendo o trabalho pesado. É esse olhar — de quem viu a engrenagem por dentro — que eu trago hoje para falar sobre o papel de analytics em risco e tesouraria."

**Referências**

Nenhuma referência formal neste slide.

---

### Slide 02 — Problema de negócio
*(tempo estimado: 45–60s)*

**O que aparece na tela**

Três perguntas, em linguagem de negócio, sem siglas, em ordem crescente de sofisticação:

1. Quando as taxas de juros se movem, quanto isso realmente custa para a nossa carteira — e quem consegue responder isso no mesmo dia?
2. Se um produto parece dar lucro para uma área e prejuízo para outra, isso é resultado real ou só um efeito de como dividimos o custo do dinheiro entre as áreas do banco?
3. Quando dizemos que o banco está preparado para um cenário de estresse, que garantia temos de que esse cenário é sequer possível de acontecer?

Frase de fechamento: *As três perguntas têm uma coisa em comum — e essa coisa está debaixo do nosso nariz todos os dias.*

Nenhuma resposta no slide.

**Roteiro oral (texto literal)**

"Quando as taxas de juros se movem, quanto isso realmente custa para a nossa carteira — e quem consegue responder isso no mesmo dia? [pausa de 2 segundos]

Se um produto parece dar lucro para uma área e prejuízo para outra, isso é resultado real ou só um efeito de como dividimos o custo do dinheiro entre as áreas do banco? [pausa de 2 segundos]

Quando dizemos que o banco está preparado para um cenário de estresse, que garantia temos de que esse cenário é sequer possível de acontecer? [pausa de 2 segundos]

[dito devagar] As três perguntas têm uma coisa em comum — e essa coisa está debaixo do nosso nariz todos os dias."

**Referências**

Nenhuma referência formal neste slide.

---

## Bloco 1 — O que é uma curva

### Slide 03 — Intuição: o que toda curva representa
*(tempo estimado: 60–90s)*

**O que aparece na tela**

Exemplo cotidiano: a curva de febre de uma pessoa doente — o médico não olha para um único número de temperatura, olha para como a temperatura se comporta ao longo das horas: subindo, estabilizando, caindo.

Frase âncora (destaque visual): **"Curva é a história que um número sozinho não conta."**

Transição para finanças (uma frase, sem detalhar tipos de curva ainda).

Frase de fechamento generalizando o conceito para qualquer domínio.

**Roteiro oral (texto literal)**

"Quando alguém está com febre, o médico não olha para um único número de temperatura. Ele olha para como essa temperatura se comporta ao longo das horas — se está subindo, se estabilizou, se está caindo. Um número isolado diz pouco. A forma como ele se comporta no tempo é que conta a história: se o quadro está melhorando ou piorando.

Isso é uma curva. E essa é a frase que eu quero que fique: curva é a história que um número sozinho não conta.

Em finanças, a curva mais presente no nosso dia a dia é a curva de juros. Ela também não é um número — é como a taxa de juros se comporta dependendo do prazo. E, assim como a febre, ela conta uma história sobre o que está acontecendo, e sobre o que pode vir a acontecer.

No fim, não importa se é a febre de uma criança, o ritmo cardíaco de um atleta ou a taxa de juros de um título: sempre que algo se comporta de forma diferente dependendo de uma dimensão — tempo, prazo, distância — existe uma curva por trás. E entender essa curva é entender a história, não só o número."

**Referências**

Nenhuma referência formal neste slide.

---

### Slide 04 — O ecossistema de curvas no banco
*(tempo estimado: 90–120s)*

**O que aparece na tela**

Mapa visual com as curvas relevantes para risco e tesouraria, cada uma com uma linha descritiva:

- **Juros prefixados (curva DI):** o preço do dinheiro sem inflação embutida — base de desconto para quase todo fluxo de caixa do banco. *(destaque visual: caso base de hoje)*
- **Cupom de IPCA:** o retorno real, depois de remover a inflação — usada em títulos indexados.
- **Câmbio e cupom cambial:** o preço do dólar no tempo — relevante para captação e operações em moeda estrangeira.
- **Crédito e spread sobre DI:** quanto se paga além do "livre de risco" para compensar a chance de um tomador não pagar.
- **Inflação implícita:** a expectativa de inflação que o próprio mercado precifica, extraída ao cruzar a curva prefixada com a curva de IPCA.
- **Commodities:** preços futuros de produtos como petróleo e soja — relevantes para crédito setorial e clientes exportadores.
- **Volatilidade:** *tecnicamente uma superfície, não uma curva* — depende de dois parâmetros (prazo e strike) — usada para precificar opções.

**Roteiro oral (texto literal)**

"O banco vive dentro de um conjunto de curvas, não de uma curva só. Cada fator de risco relevante para o negócio tem a sua: juros, câmbio, crédito, inflação, commodities. [aponta para o mapa] Juros prefixados é o preço do dinheiro sem inflação embutida — é a base de desconto de quase tudo que o banco faz. Cupom de IPCA é o mesmo preço do dinheiro, mas já líquido de inflação. Câmbio e cupom cambial fazem o mesmo papel para operações em moeda estrangeira. Crédito e spread sobre DI medem o quanto se cobra além do livre de risco para compensar a chance de um tomador não pagar. Inflação implícita é a expectativa de inflação que o próprio mercado precifica — e ela nasce exatamente do cruzamento entre a curva prefixada e a curva de IPCA, vamos ver isso de novo mais adiante. Commodities têm a curva de preços futuros de produtos como petróleo e soja. E volatilidade, tecnicamente, nem é uma curva — é uma superfície, porque depende de dois parâmetros, prazo e strike — mas vive no mesmo ecossistema porque precifica opção.

Hoje eu vou ficar na curva de juros. Não porque as outras importem menos, mas porque é nela que a maior parte das decisões de risco e tesouraria do banco se apoia — e porque, entendendo essa, o raciocínio se generaliza para as demais. E quero que vocês guardem uma coisa: analytics não serve só a curva de juros. Ela serve esse ecossistema inteiro. O recorte de hoje é metodológico — não é o limite do nosso trabalho."

**Referências**

- Souza, I.A. (2017) — *Estudo do Value at Risk... no mercado financeiro brasileiro*, Dissertação de Mestrado, Universidade de Brasília. Grounding: o trabalho descreve os fatores de risco de mercado como "as variáveis que alteram o valor de um instrumento financeiro, tais como taxas de juros, os preços de ações, os preços de mercadorias (commodities) e as taxas de câmbio" e detalha a distinção entre carteira de negociação (trading book) e carteira bancária (banking book) — base para o mapeamento de curvas por tipo de exposição.

---

### Slide 05 — Construção matemática: curva de juros
*(tempo estimado: 120–150s)*

**O que aparece na tela**

**Camada 1 — Intuição:** a curva de juros descreve o preço do dinheiro para cada prazo — não existe "a taxa de juros", existem taxas diferentes para prazos diferentes, porque risco e expectativa mudam com o horizonte.

**Camada 2 — Tabela de parâmetros (significado econômico):**

| Parâmetro | Nome técnico | Significado econômico |
|---|---|---|
| β₁ | Nível | Para onde a taxa converge no longuíssimo prazo |
| β₂ | Inclinação | Diferença entre juros curtos e longos — leitura do ciclo monetário |
| β₃ | Curvatura | A "barriga" da curva no meio do prazo |
| λ | Decaimento | Onde, no prazo, a curvatura é mais forte |

**Camada 3 — Fórmula de Nelson-Siegel** (única equação do slide, com cada termo rotulado em português ao lado, não em nota de rodapé):

$$y_t(\tau) = \underbrace{\beta_{1,t}}_{\text{nível}} + \underbrace{\beta_{2,t}\left[\frac{1-e^{-\lambda\tau}}{\lambda\tau}\right]}_{\text{inclinação}} + \underbrace{\beta_{3,t}\left[\frac{1-e^{-\lambda\tau}}{\lambda\tau}-e^{-\lambda\tau}\right]}_{\text{curvatura}}$$

Versão em texto simples, para o slide (caso o template não renderize LaTeX):

```
y(τ) =      β1       +       β2 · [(1 − e^(−λτ)) / (λτ)]      +      β3 · [(1 − e^(−λτ)) / (λτ) − e^(−λτ)]
          (nível)                    (inclinação)                                (curvatura)
```

*y(τ) = taxa de juros no instante t para o prazo τ*

**Roteiro oral (texto literal)**

"Vou construir isso em três camadas, e quero que todo mundo acompanhe, mesmo quem não tem formação em matemática — vai dar tempo.

Primeira camada: intuição. A curva de juros descreve o preço do dinheiro para cada prazo. Não existe 'a' taxa de juros — existem taxas diferentes para prazos diferentes, porque risco e expectativa de mercado mudam com o horizonte.

Segunda camada: o modelo usado para descrever essa curva tem só três números com significado econômico direto. O primeiro, chamado de nível, é para onde a taxa converge no longuíssimo prazo. O segundo, inclinação, é a diferença entre os juros de curto e de longo prazo — e isso é, na prática, uma leitura do ciclo monetário. O terceiro, curvatura, é a 'barriga' que a curva faz no meio do prazo. Existe ainda um quarto parâmetro, de decaimento, que controla em qual prazo essa barriga é mais forte.

Terceira camada: a fórmula. [aponta para a equação] Essa é a equação de Nelson-Siegel. Quem não precisa da matemática, lê as legendas ao lado de cada termo — nível, inclinação, curvatura. Quem quer a matemática, lê a equação. Os dois grupos saem servidos pelo mesmo slide.

A ANBIMA, na prática, usa uma versão estendida dessa mesma ideia, proposta por Svensson, que adiciona um quarto parâmetro e uma segunda curvatura — para conseguir acomodar formatos de curva mais complexos do que os três fatores originais capturam. Mas o espírito é exatamente o mesmo: poucos números, com leitura econômica direta, descrevendo a curva inteira.

Esses três números — nível, inclinação e curvatura — não são abstração de modelo estatístico. Eles vão reaparecer no resto desta apresentação: é o que a tesouraria lê para decidir, é o que risco choca para medir estresse, e é o que toda a cadeia de negócio do banco usa, mesmo sem saber o nome."

**Referências**

- ANBIMA — *Estrutura a Termo das Taxas de Juros Estimada e Inflação Implícita: Metodologia*. Grounding: descreve o modelo de Svensson (1994) como o adotado pela ANBIMA para a ETTJ brasileira, com os fatores "interpretação de nível (β1t), inclinação (β2t) e curvaturas (β3t e β4t)".
- Caldeira, J.F. (2011) — *Estimação da Estrutura a Termo da Curva de Juros no Brasil através de Modelos Paramétricos e Não Paramétricos*, Análise Econômica, UFRGS. Grounding: apresenta a formulação de Nelson-Siegel (a partir de Diebold e Li, 2006, reinterpretando Nelson e Siegel, 1987) e sua extensão de Svensson (1994b), com a mesma decomposição em nível/inclinação/curvatura usada no slide.

---

## Bloco 2 — Como o negócio usa curvas

### Slide 06 — A cadeia de valor: mesas → mercado → risco → tesouraria
*(tempo estimado: 75–90s)*

**O que aparece na tela**

Diagrama linear, fluxo único (sem setas bidirecionais), quatro elos:

**Mesas** → **Mercado** → **Risco** → **Tesouraria**

- Mesas: negociam — compram e vendem instrumentos, gerando posições e preços.
- Mercado: liquida e referencia — todo negócio fechado precisa ser registrado, garantido e avaliado a um preço de referência comum.
- Risco: mede — transforma posições em números de exposição e perda potencial.
- Tesouraria: decide — usa essas informações para gerenciar caixa, funding e posicionamento estrutural do banco.

Analytics posicionada abaixo dos quatro elos, servindo a cadeia inteira.

Frase de fechamento: *o que analytics precisa entender para servir bem essa cadeia inteira?*

**Roteiro oral (texto literal)**

"Esse diagrama vai ser a nossa referência para os próximos quatro slides, então vale fixar. As mesas negociam — compram e vendem instrumentos financeiros, e dessa negociação nascem posições e preços. Esse negócio precisa virar liquidação — é preciso ser registrado, garantido e avaliado a um preço de referência comum, e é aqui que entra o mercado. Foi exatamente nessa parte da cadeia que eu trabalhei antes de migrar para dados: na infraestrutura que garante que, depois que a mesa aperta o botão, a operação realmente se liquida e é avaliada a um preço justo. Quem viu essa engrenagem por dentro entende com mais clareza o que as mesas geram e o que o mercado exige delas.

A partir daí, risco mede — transforma essas posições em números de exposição e perda potencial. E tesouraria decide — usa essas informações para gerenciar caixa, custo de funding e o posicionamento estrutural do banco.

Analytics não serve a um desses elos. Ela serve a cadeia inteira. E a pergunta que fica para os próximos slides é: o que analytics precisa entender da curva para servir bem essa cadeia inteira?"

**Referências**

- Souza, I.A. (2017) — Dissertação UnB. Grounding: descreve a estrutura de limites de risco e delegações por "mesas de operações/operadores" dentro da gestão de risco de mercado do banco.
- BACEN — Circular 3.082/2002 — *Registro e Avaliação de Instrumentos Financeiros Derivativos*. Grounding: exige que os instrumentos sejam "avaliados pelo valor de mercado, no mínimo, por ocasião dos balancetes" — base regulatória para o papel do elo "mercado" como fonte de referência de preço.

---

### Slide 07 — Tesouraria: MTM e FTP
*(tempo estimado: 110–130s)*

**O que aparece na tela**

**MTM (Marcação a Mercado):**
- Intuição: quando a taxa de juros sobe, o valor presente de um título cai — porque os mesmos fluxos futuros passam a ser descontados a uma taxa maior.
- Mecanismo (uma linha): valor do título = soma dos fluxos futuros descontados pela curva de juros vigente no dia.
- ANBIMA fornece as Taxas Indicativas — referência de preço justo usada para a marcação a mercado de todo o mercado.

**FTP (preço de transferência de fundos):**
- Intuição: o custo (ou ganho) de captar e emprestar dinheiro precisa ser distribuído internamente entre quem capta e quem empresta — e essa distribuição também usa a curva.
- Consequência de FTP mal calculado: resultado de área distorcido — uma área parece lucrativa ou deficitária por um efeito de precificação interna, não por desempenho real.

**Roteiro oral (texto literal)**

"Primeiro movimento: marcação a mercado. Quando a taxa de juros sobe, o valor de um título cai — mesmo que nada tenha mudado nesse título. Por quê? Porque os mesmos fluxos futuros passam a ser descontados a uma taxa maior, e isso reduz o valor presente. Em uma linha: o valor de um título é a soma dos seus fluxos futuros, descontados pela curva de juros vigente naquele dia. A ANBIMA entra exatamente aqui — ela publica o que chama de Taxas Indicativas, que são referências de preço justo, onde a oferta encontra a demanda, usadas para marcar a mercado o fechamento de todo o mercado. Sem a curva calibrada, essa marcação simplesmente não existe.

E se a marcação a mercado responde quanto vale a carteira, quem responde quanto custa o dinheiro por dentro do banco?

Segundo movimento: preço de transferência de fundos, o FTP. A mesma curva que usamos para marcar a mercado também define o custo interno de captar e de emprestar dinheiro dentro do banco. Quando esse custo não é transferido corretamente entre quem capta e quem empresta, o resultado por área fica distorcido — uma área pode parecer lucrativa, ou deficitária, só por um efeito de como dividimos o custo do dinheiro, não porque ela performou bem ou mal de fato.

MTM e FTP não são conceitos separados. Eles são dois usos diferentes da mesma curva — e é por isso que estão juntos neste slide."

**Referências**

- ANBIMA — *Metodologias ANBIMA de Precificação 2023* e *Regras e Procedimentos para Apuração de Valores de Referência*. Grounding: definem as Taxas Indicativas como "referências de preço justo, onde a oferta encontra sua demanda, para negociação do ativo no fechamento dos mercados".
- Checoli, A.G. — *Preço de Transferência de Passivos sem Vencimento de Bancos Comerciais*, Dissertação FGV. Grounding: "o preço de transferência é uma medida interna e indica a contribuição no lucro de arrecadação de fundos e empréstimos feitos pelo banco" — e descreve como um FTP mal calibrado distorce os incentivos entre tesouraria e canais de captação/empréstimo.
- Morch, R.B.; Castro, G.S.; Castro, V.C.B.; Cogan, S. — *Preço de Transferência de Fundos: um estudo para o mercado financeiro*, UFSC (2008). Grounding: reforça a definição e a mecânica de transferência de custo de funding entre áreas do banco.

---

### Slide 08 — Tesouraria: ALM e posicionamento
*(tempo estimado: 110–130s)*

**O que aparece na tela**

- Descasamento estrutural do banco: capta curto, empresta longo.
- Gap de reprecificação: o descompasso entre o momento em que ativos e passivos "renovam" sua taxa.
- Exigência regulatória: gestão desse descasamento é medida pelas métricas **ΔEVE** e **ΔNII** — métricas de impacto de choques de juros no valor econômico e no resultado de juros do banco.
- Steepener e flattener como leitura de ciclo monetário:
  - *Steepener* — juros curtos caem e/ou longos sobem (curva inclina mais).
  - *Flattener* — juros curtos sobem e/ou longos caem (curva achata).
- Semente: posicionamento acontece **antes** do COPOM, não depois.

**Roteiro oral (texto literal)**

"Primeiro movimento, o problema estrutural. Todo banco vive de um descasamento: capta dinheiro no curto prazo — depósitos, CDBs de prazo curto — e empresta no longo prazo — financiamentos, crédito imobiliário. Esse descasamento entre quando os ativos e os passivos 'renovam' sua taxa é o que chamamos de gap de reprecificação. É o risco estrutural do banco, e ele existe em todo banco, sempre.

Isso não é só uma preocupação teórica. A regulação brasileira exige que esse risco seja medido — são as métricas ΔEVE e ΔNII, que capturam o impacto de um choque de juros no valor econômico do banco e no resultado de juros ao longo do tempo. Não vou entrar na fórmula — o que importa aqui é que gerenciar esse descasamento não é opcional, é exigência regulatória.

[tom sobe] Segundo movimento, e aqui a resposta estratégica entra. A curva não serve só para medir esse descasamento — ela serve para o tesoureiro se posicionar antes que o mercado se mova. Quando a curva inclina mais — o que chamamos de steepener, juros curtos caindo e longos subindo — isso é uma leitura de ciclo: o mercado está precificando uma virada. Quando ela achata — o flattener, curtos subindo e longos caindo — é a leitura oposta. Um tesoureiro que entende essas leituras se posiciona antes do COPOM decidir, não depois. E isso é o que separa gestão reativa de gestão estratégica.

Mas medir o descasamento estrutural é uma coisa. Medir quanto cada movimento específico de mercado custa para a carteira é outra — e é aí que entra risco de mercado."

**Referências**

- BACEN — Resolução CMN 4.557/2017. Grounding: exige estrutura de gerenciamento de risco que cubra o descasamento de prazos e a gestão de ALM como parte do programa de gerenciamento de riscos do banco.
- BACEN — Circular 3.876/2018 — *Metodologias para mensuração do IRRBB*. Grounding: define formalmente EVE como "a diferença entre o valor presente do somatório dos fluxos de reapreçamento... em um cenário-base e... em um cenário de choque nas taxas de juros" e NII de forma análoga para o resultado de intermediação financeira; e define os choques padronizados de *steepener* ("redução das taxas de juros de curto prazo e aumento das taxas de juros de longo prazo") e *flattener* ("aumento das taxas de juros de curto prazo e redução das taxas de juros de longo prazo").

---

### Slide 09 — Risco: DV01, sensibilidades e PCA
*(tempo estimado: 130–150s)*

**O que aparece na tela**

- DV01: quanto o portfólio perde (ou ganha) para cada 1 ponto-base de movimento na curva.
- DV01 por vértice: mapa de sensibilidade da carteira — quanto cada prazo da curva pesa no risco total.
- Problema de dimensionalidade: dezenas de vértices, que não se movem de forma independente — movem-se juntos.
- PCA: reduz esse problema a um pequeno número de componentes que concentram a maior parte da variação histórica da curva.
- Interpretação econômica dos componentes: **nível, inclinação, curvatura** — os mesmos três fatores do Slide 05.
- Conexão explícita: os componentes do PCA correspondem aos parâmetros β do Nelson-Siegel. *Não é coincidência.*

**Roteiro oral (texto literal)**

"Primeiro movimento: DV01. É a métrica mais operacional do risco de mercado — quanto o portfólio perde, ou ganha, para cada um ponto-base de movimento na curva. E o risco calcula isso vértice por vértice: dois anos, cinco anos, dez anos — cada prazo da curva tem o seu DV01, formando um mapa de sensibilidade da carteira inteira.

O problema é que esse mapa tem dezenas de vértices. E eles não se movem de forma independente — eles se movem juntos, de forma correlacionada. Gerenciar dezenas de números que andam juntos é ineficiente e mascara o que realmente importa.

[tom de segurança] É aqui que entra a análise de componentes principais, o PCA. Estudos sobre os fatores de risco da curva mostram que um número pequeno de componentes — historicamente, em geral três — já concentra a grande maioria da variação histórica da curva inteira. E esses três componentes, quando você olha o que eles representam economicamente, são nível, inclinação e curvatura.

Nível, inclinação, curvatura. Vocês já ouviram esses três nomes antes — são os mesmos três parâmetros, β1, β2 e β3, que apareceram na fórmula de Nelson-Siegel, no Slide 5. Não é coincidência. Os componentes principais que explicam a maior parte do movimento histórico da curva são, na prática, a mesma decomposição econômica que o modelo de Nelson-Siegel usa para descrever a curva em um único instante. É o mesmo fenômeno, visto por dois caminhos diferentes — e isso significa que o vocabulário que construímos no início da apresentação serve tanto para descrever a curva quanto para gerenciar o seu risco."

**Referências**

- Caldeira, J.F. (2011) — *Estimação da Estrutura a Termo da Curva de Juros no Brasil*. Grounding: formaliza a decomposição de Nelson-Siegel/Svensson em nível, inclinação e curvatura.
- BACEN — *Previsão da Curva de Juros no Brasil: um modelo estatístico com variáveis macroeconômicas* (Working Paper 186). Grounding: relata que "Almeida e outros (2007b) fixam λ1 de tal sorte que o máximo do loading da primeira curvatura coincida com aquele extraído via componentes principais" e que "choques nas variáveis β1t, β2t, β3t e β4t representam mudanças no nível, na inclinação e em duas curvaturas da ETTJ" — base direta para a conexão PCA ↔ parâmetros β do Nelson-Siegel feita no slide.
- BACEN — Resolução CMN 4.557/2017. Grounding: exige sensibilidades e mensuração de risco de mercado como parte do programa de gerenciamento de riscos.

*Nota de transparência: a literatura consultada localmente não traz um percentual exato e único de variância explicada pelos três primeiros componentes para a curva brasileira; por isso o slide usa a formulação qualitativa "a grande maioria da variação histórica", em vez de um número pontual não verificado nas referências salvas.*

---

### Slide 10 — Risco: stress testing regulatório
*(tempo estimado: 110–130s)*

**O que aparece na tela**

- Limitação do VaR: mede risco em condições normais de mercado — pressupõe continuidade estatística e subestima eventos extremos ("caudas pesadas").
- Três tipos de choque na curva: **paralelo, inclinação, curvatura** — os mesmos três fatores dos Slides 05 e 09.
- Por que chocar β é mais robusto que chocar vértices isolados: choques coordenados nos parâmetros preservam uma curva economicamente coerente; choques independentes em vértices isolados podem gerar formatos de curva internamente inconsistentes.
- Âncora regulatória: CMN 4.557/2017 (programa de testes de estresse) e Relatório de Estabilidade Financeira do BACEN (cenários aplicados na prática).

**Roteiro oral (texto literal)**

"Primeiro movimento: a limitação do VaR. O VaR é uma métrica poderosa, mas ele mede risco em condições normais de mercado — ele pressupõe uma certa continuidade estatística, e a literatura mostra, de forma consistente, que a distribuição dos retornos financeiros tem caudas mais pesadas do que a distribuição normal assume. Isso quer dizer que o VaR tende a subestimar exatamente os eventos extremos — que são os que mais importam em uma crise. Por isso a regulação brasileira não se contenta com VaR: ela exige um programa de testes de estresse.

[tom sobe] Segundo movimento: como esse programa lida com a curva. A própria definição regulatória de análise de cenários exige 'variações simultâneas e coerentes' em um conjunto de parâmetros — não choques isolados e desconectados. E é exatamente aqui que o que construímos nos slides anteriores faz diferença: em vez de chocar vértice por vértice, de forma independente, o jeito robusto é chocar os parâmetros da curva — paralelo, inclinação e curvatura, os mesmos três fatores do Nelson-Siegel e do PCA. Por quê? Porque chocar vértices isolados pode gerar formatos de curva que não fazem sentido econômico — uma curva que sobe, desce e sobe de novo sem nenhuma lógica de mercado. Chocar os parâmetros preserva uma curva coerente, e é isso que torna o cenário de estresse economicamente possível, não só matematicamente possível.

A regulação brasileira já formaliza dois desses três movimentos dentro da metodologia de IRRBB — choques paralelos e choques de inclinação. E o Relatório de Estabilidade Financeira do Banco Central mostra isso sendo aplicado na prática: em um dos exercícios de cenário de estresse, o cenário de alta considerou um deslocamento paralelo da curva de juros futura de treze vírgula dois pontos percentuais, e o cenário de baixa, de cinco pontos percentuais.

[última frase do bloco, dita devagar, não está no slide] E se até aqui falamos de medir e de chocar a curva depois que o mercado se move... a pergunta que fica é: o que ela já está nos dizendo agora, antes de o movimento acontecer?"

**Referências**

- BACEN — Resolução CMN 4.557/2017. Grounding: define formalmente teste de estresse, análise de sensibilidade, análise de cenários (exigindo "variações simultâneas e coerentes em um conjunto de parâmetros relevantes") e teste de estresse reverso como parte obrigatória do programa de gerenciamento de riscos.
- BACEN — Relatório de Estabilidade Financeira — Capítulo de Cenários de Estresse. Grounding: relata cenário de estresse aplicado com "deslocamento paralelo da curva de juros futura em 13,2 p.p." (cenário de alta) e "em 5 p.p." (cenário de baixa).
- BACEN — Circulares 3.634/2013 e 3.645/2013. Grounding: estabelecem o cálculo das parcelas RWAJUR (RWAJUR1 a RWAJUR4) dos ativos ponderados pelo risco para exposições a taxas de juros prefixadas — base do requerimento de capital regulatório associado ao risco de curva.
- Souza, I.A. (2017) — Dissertação UnB. Grounding: discute as limitações estatísticas do VaR, incluindo a presença de "caudas gordas" nos retornos financeiros e a subestimação de eventos extremos pela distribuição normal.

---

## Bloco 3 — O papel de analytics na cadeia

### Slide 11 — O que analytics entrega para cada elo da cadeia
*(tempo estimado: 60–75s)*

**O que aparece na tela**

Retomada do diagrama do Slide 06 — mesmos quatro elos, nova camada de entregas:

- **Mesas:** entrega leitura de risco e precificação validada em tempo real.
- **Mercado:** entrega dados consistentes que sustentam uma marcação a mercado confiável.
- **Risco:** entrega sensibilidades e cenários calculados com rigor e rastreabilidade.
- **Tesouraria:** entrega sinais consolidados que transformam dado disperso em decisão de funding e posicionamento.

Frase de fechamento: *Analytics transforma dado em capacidade de decisão.*

**Roteiro oral (texto literal)**

"Esse é o mesmo diagrama do início do bloco anterior — mas agora com uma camada nova. Para as mesas, analytics entrega leitura de risco e precificação validada em tempo real. Para o mercado, entrega dados consistentes que sustentam uma marcação confiável. Para risco, entrega sensibilidades e cenários calculados com rigor e rastreabilidade. E para tesouraria, entrega sinais consolidados que transformam dado disperso em decisão de funding e de posicionamento.

Reparem que em nenhum desses quatro pontos eu disse 'apoia' ou 'suporta'. Analytics entrega. Analytics transforma dado em capacidade de decisão — em cada um dos quatro elos dessa cadeia."

**Referências**

Nenhuma referência formal neste slide — o argumento é de posicionamento da área.

---

### Slide 12 — Por que a construção matemática importa para dados
*(tempo estimado: 110–130s)*

**O que aparece na tela**

Três situações concretas:

1. **Validação de dado:** distinguir um erro de dado de um movimento legítimo de mercado.
2. **Identificação de anomalia:** reconhecer instabilidade numérica do modelo versus sinal real de mercado.
3. **Explicação para o cliente interno:** traduzir um resultado técnico em linguagem de negócio.

*(a frase de fechamento não aparece no slide como um quarto item — ela é dita apenas oralmente, devagar, com pausa depois, conforme o roteiro abaixo)*

**Roteiro oral (texto literal)**

"Três situações que qualquer pessoa nessa sala já viveu, ou vai viver.

Primeira: validação de dado. Um vértice da curva chega com um valor estranho. Erro de carga, ou movimento real de mercado? Quem entende como os parâmetros da curva se relacionam consegue checar se aquele valor é coerente com o resto da curva — ou se é, de fato, um erro.

Segunda: identificação de anomalia. A própria metodologia da ANBIMA descreve isso diretamente: a estimação ingênua dos parâmetros de uma curva como essa pode gerar, nas palavras do documento, 'alta volatilidade da série histórica dos parâmetros' e 'abundância de valores anômalos' — não porque o mercado mudou, mas porque o modelo está instável. Foi exatamente para resolver isso que a ANBIMA passou a usar um algoritmo mais robusto de estimação. Quem não conhece essa construção corre o risco de tratar um problema de modelo como se fosse um sinal real de mercado — e vice-versa.

Terceira: explicação para o cliente interno. Quando o resultado de risco ou tesouraria muda, alguém vai perguntar por quê. E a resposta que convence não é 'o modelo retornou esse número' — é 'a inclinação da curva aumentou, e isso eleva o custo de funding de prazo mais longo'. Isso só é possível para quem entende o que está por dentro do número.

[devagar, com pausa depois] No fim, essas três situações mostram a mesma coisa: dado se torna informação. Informação se torna decisão. E a construção matemática da curva é o que garante essa passagem."

**Referências**

- ANBIMA — *Estrutura a Termo das Taxas de Juros Estimada e Inflação Implícita: Metodologia*. Grounding: descreve explicitamente que a estimação tradicional dos parâmetros do modelo de Svensson gera "alta volatilidade da série histórica dos parâmetros, à abundância de valores anômalos e à grande frequência de mudanças estruturais, não justificáveis pela evolução do mercado" — motivo pelo qual a ANBIMA adotou um algoritmo genético de estimação.
- Caldeira, J.F. (2011). Grounding: compara diferentes métodos de estimação da ETTJ, reforçando que a escolha e a estabilidade do método afetam diretamente a qualidade do resultado.
- BACEN — *Previsão da Curva de Juros no Brasil* (Working Paper 186). Grounding: trata da relação entre os parâmetros estimados da curva e seu uso para leitura econômica.

---

### Slide 13 — O que a curva sinaliza antes do evento
*(tempo estimado: 130–150s)*

**O que aparece na tela**

Três sinais que a curva carrega:

1. **Inflação implícita** — diferença entre a curva prefixada e a curva de IPCA; sinaliza a expectativa de inflação do mercado antes da divulgação de índices oficiais.
2. **Inclinação como proxy de ciclo** — steepener/flattener sinalizam a leitura do mercado sobre a direção futura da política monetária antes da decisão.
3. **Prêmio de risco no longo prazo** — a parcela da taxa que compensa a incerteza sobre a inflação futura; varia no tempo e tende a se ampliar antes que a incerteza se materialize em volatilidade realizada.

Para cada sinal: ação correspondente de risco ou tesouraria. Papel de analytics: extração e monitoramento contínuo desses sinais.

**Roteiro oral (texto literal)**

"Três sinais que a curva carrega todos os dias — não previsão, sinal.

Primeiro sinal: inflação implícita. Ela nasce de uma identidade simples — a taxa nominal é, aproximadamente, a taxa real mais a inflação esperada. Cruzando a curva prefixada com a curva de IPCA, extraímos essa expectativa de inflação que o próprio mercado está precificando, antes de qualquer índice oficial ser divulgado. Quando essa expectativa se move, tesouraria ajusta o mix de captação entre indexado e prefixado antes da inflação realizada confirmar o movimento.

Segundo sinal: inclinação como proxy de ciclo. Já vimos isso no bloco anterior — quando a curva inclina ou achata, ela está expressando a leitura do mercado sobre a próxima direção da política monetária. Essa leitura aparece na curva antes da decisão do Copom ser anunciada. É a mesma lógica de posicionamento que mencionei na tesouraria, agora vista como sinal de antecipação.

Terceiro sinal, e o mais sutil: prêmio de risco no longo prazo. A literatura do Banco Central mostra que esse prêmio — a parcela da taxa que compensa a incerteza sobre a inflação futura — é pequena em horizontes curtos, mas varia no tempo em horizontes longos, e está relacionada à percepção de risco e de volatilidade futura. Quando esse prêmio começa a se ampliar no longo prazo, isso tende a acontecer antes que a incerteza apareça nos números realizados de volatilidade. É um sinal de que o mercado está precificando mais incerteza — antes de ela se manifestar.

Esses três sinais não são especulação. São objetos mensuráveis, extraídos todos os dias da mesma curva que construímos desde o início desta apresentação. E o papel de analytics é justamente esse: extrair, monitorar e entregar esses sinais a tempo de virarem decisão.

[última frase do slide, dita devagar, não está no slide, eco da tese sem repeti-la] No fim, talvez a curva não seja só um insumo técnico. Ela é a forma como o mercado fala antes de agir. E quem souber escutar essa construção entende o que vai acontecer antes que aconteça."

**Referências**

- ANBIMA — *Estrutura a Termo das Taxas de Juros Estimada e Inflação Implícita: Metodologia*. Grounding: define a extração da inflação implícita via identidade de Fisher, cruzando curva prefixada e curva de IPCA, e descreve o prêmio de risco de inflação embutido nessa extração.
- BACEN — *Decompondo a Inflação Implícita* (Working Paper 359). Grounding: "o prêmio de risco de inflação é pequeno para horizontes curtos. Para horizontes longos este prêmio de risco é variável no tempo e relacionado com o consumo e a volatilidade" — base direta do terceiro sinal.
- BACEN — Relatório de Estabilidade Financeira. Grounding: contextualiza o monitoramento de inclinação e cenários de juros futuros como prática regulatória corrente de acompanhamento de risco sistêmico.

---

## Bloco 4 — Fechamento

### Slide 14 — Voltando às três perguntas
*(tempo estimado: 75–90s)*

**O que aparece na tela**

Mesmo layout do Slide 02, três perguntas, agora com uma resposta de uma linha cada:

1. *Quanto isso custa para a carteira?* → A curva, decomposta em nível, inclinação e curvatura, mede esse impacto em tempo real, com DV01 e sensibilidades por vértice.
2. *O resultado por área é real?* → MTM e FTP, construídos sobre a mesma curva, separam resultado real de efeito de precificação interna.
3. *O cenário de estresse é possível?* → Cenários que chocam os parâmetros da curva de forma coerente são os que resistem à pergunta: isso é economicamente possível?

Frase de fechamento das três perguntas (no slide): **Três perguntas, uma resposta em comum: a curva.**

**Roteiro oral (texto literal)**

"Voltamos para onde começamos. [pausa]

Primeira pergunta: quanto isso custa para a carteira? A curva, decomposta em nível, inclinação e curvatura, mede esse impacto em tempo real, com DV01 e sensibilidade por vértice.

Segunda pergunta: o resultado por área é real? MTM e FTP, construídos sobre essa mesma curva, separam o que é resultado real do que é só efeito de como dividimos o custo do dinheiro.

Terceira pergunta: o cenário de estresse é possível? Cenários que chocam os parâmetros da curva de forma coerente — não vértices isolados — são os que resistem a essa pergunta.

[pausa depois da terceira resposta]

Três perguntas, uma resposta em comum: a curva.

[frase final, dita devagar, não está no slide — a frase mais importante da apresentação] E é exatamente por isso que entender a construção da curva muda o que analytics entrega: deixa de ser quem processa o dado, e passa a ser quem participa da decisão."

**Referências**

Nenhuma referência formal neste slide.

---

### Slide 15 — Referências
*(tempo estimado: 30–45s)*

**O que aparece na tela**

*(Slide mostrado, não lido em voz alta. Sem URLs.)*

**Documentos regulatórios e institucionais**
- ANBIMA — Estrutura a Termo das Taxas de Juros Estimada e Inflação Implícita: Metodologia
- ANBIMA — Metodologias de Precificação 2023
- ANBIMA — Regras e Procedimentos para Apuração de Valores de Referência
- BACEN — Resolução CMN 4.557/2017
- BACEN — Circular 3.876/2018 (IRRBB)
- BACEN — Circulares 3.634/2013 e 3.645/2013 (RWA de mercado)
- BACEN — Circular 3.082/2002 (Derivativos)
- BACEN — Relatório de Estabilidade Financeira

**Artigos e dissertações acadêmicas**
- Caldeira, J.F. (2011) — Análise Econômica, UFRGS
- Morch, Castro, Castro e Cogan — Artigo FTP, UFSC (2008)
- Checoli, A.G. — Dissertação, FGV
- Souza, I.A. (2017) — Dissertação, UnB
- BACEN — Working Paper 186 (Previsão da Curva de Juros)
- BACEN — Working Paper 359 (Decompondo a Inflação Implícita)

**Roteiro oral (texto literal)**

"Todo o conteúdo de hoje tem base em documentação regulatória do Banco Central e da ANBIMA, e em produção acadêmica brasileira sobre o tema — está tudo listado aqui. Não vou ler a lista. Quem quiser os links, me procura depois que eu mando por e-mail.

Muito obrigada pela atenção de todos. Fico à disposição para perguntas."

**Referências**

Lista consolidada acima — todas as 14 referências já citadas ao longo dos slides anteriores. Excluídos desta lista (por não terem sido consultados diretamente): Fortuna, *Mercado Financeiro*; Morettin & Toloi, *Análise de Séries Temporais*.

---

## Apêndice — Orientação para perguntas

**Pergunta técnica sobre modelagem:** responder com o mecanismo geral; se for mais específica do que o escopo da apresentação, é legítimo indicar a fonte e oferecer aprofundamento depois por e-mail.

**Pergunta sobre aplicação na área:** conectar com o trabalho real sem entrar em detalhe confidencial — nível de capacidade entregue, não de projeto executado.

**Pergunta sobre o que ficou de fora:** reconhecer o recorte como escolha deliberada (por exemplo, por que ficou em juros e não em câmbio ou crédito) e oferecer o próximo capítulo natural como continuação possível.

---

## Apêndice — Links das referências (uso interno, para envio por e-mail; não exibir no slide)

**Documentos regulatórios e institucionais**
- ANBIMA — Estrutura a Termo das Taxas de Juros Estimada e Inflação Implícita: Metodologia — `https://www.anbima.com.br/data/files/18/42/65/50/4169E510222775E5A8A80AC2/est-termo_metodologia.pdf`
- ANBIMA — Metodologias ANBIMA de Precificação 2023 — `https://www.anbima.com.br/data/files/9E/67/9D/6F/382788107D83F688EA2BA2A8/Metodologias-ANBIMA-de%20Precificacao-2023.pdf`
- ANBIMA — Regras e Procedimentos para Apuração de Valores de Referência — `https://www.anbima.com.br/data/files/5F/A6/3B/BE/9BB2E710C19FACD7882BA2A8/metodologia-curvas_20credito_20131104_v2_1_.pdf`
- BACEN — Resolução CMN 4.557/2017 — `https://normativos.bcb.gov.br/Lists/Normativos/Attachments/50344/Res_4557_v4_P.pdf`
- BACEN — Circular 3.876/2018 (IRRBB) — `https://www.bcb.gov.br/pre/normativos/busca/normativo.asp?tipo=Circular&ano=2018&numero=3876`
- BACEN — Circulares 3.634/2013 e 3.645/2013 (RWA de mercado) — `https://www.bcb.gov.br/pre/normativos/busca/normativo.asp?tipo=Circular&ano=2013&numero=3634`
- BACEN — Circular 3.082/2002 (Derivativos) — `https://normativos.bcb.gov.br/Lists/Normativos/Attachments/46969/Circ_3082_v5_P.pdf`
- BACEN — Relatório de Estabilidade Financeira — `https://www.bcb.gov.br/publicacoes/ref` (capítulo de cenários de estresse usado: `https://www.bcb.gov.br/content/publicacoes/ref/200305/RELESTAB2003-PortuguesCapitulo4.pdf`)

**Artigos e dissertações acadêmicas**
- Caldeira, J.F. (2011) — Análise Econômica, UFRGS — `https://seer.ufrgs.br/AnaliseEconomica/article/view/13198`
- Morch, Castro, Castro e Cogan — Artigo FTP, UFSC (2008) — `https://periodicos.ufsc.br/index.php/contabilidade/article/view/2175-8069.2008v5n9p95`
- Checoli, A.G. — Dissertação, FGV — `https://repositorio.fgv.br/bitstreams/1ddc13f2-cd19-4b15-93b3-e09aa1f0d15d/download`
- Souza, I.A. (2017) — Dissertação, UnB — `https://repositorio.unb.br/bitstream/10482/31108/1/2017_IramAlvesdeSouza.pdf`
- BACEN — Working Paper 186 (Previsão da Curva de Juros) — `https://aprendervalor.bcb.gov.br/content/publicacoes/WorkingPaperSeries/wps186.pdf`
- BACEN — Working Paper 359 (Decompondo a Inflação Implícita) — `https://www.bcb.gov.br/pec/wps/port/TD359.pdf`

---

*Material elaborado com base exclusivamente nas referências salvas na pasta do projeto, listadas no Slide 15. Tempo total estimado de fala: ~23 minutos, deixando 7 a 12 minutos de margem para perguntas dentro da janela de 30 minutos.*
