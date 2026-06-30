# Apresentação — Curva de Juros: da Intuição à Aplicação em Risco e Tesouraria

**Público:** Analistas de dados e analytics que atendem risco e tesouraria  
**Duração:** 30 minutos | **Total:** 16 slides

---

## Estrutura

| Ato | Título | Slides | Tempo |
|---|---|---|---|
| 0+1 | O banco acorda com uma pergunta | 2 | 4 min |
| 2a | De onde vêm os dados | 2 | 4 min |
| 2b | Como a taxa vira preço | 2 | 4 min |
| 2c | Interpolação e vida da curva | 2 | 4 min |
| 3 | A curva dentro do banco | 2 | 4 min |
| 4 | O que a forma diz | 2 | 3 min |
| 5 | Quando a curva se move | 2 | 3 min |
| 6 | Dado errado, decisão errada | 2 | 4 min |

---

## Descrição dos Atos

### Ato 0+1 — O banco acorda com uma pergunta
*(4 min, 2 slides)*

O banco fechou operações ontem com taxas de ontem. Hoje a curva subiu 50bps. Quanto vale agora tudo que foi prometido? Este ato abre a apresentação com o desconforto real do negócio — não uma pergunta abstrata, mas uma situação que acontece toda manhã nas mesas de tesouraria e risco. O segundo slide introduz a ideia de que esse problema não é exclusivo do mercado financeiro: qualquer relação que muda ao longo do tempo forma uma curva, e ler essa curva é ler o futuro implícito. A analogia aparece aqui como insight, não como introdução — o leitor já está dentro do problema quando a vê. O objetivo é criar tensão narrativa desde o primeiro segundo e posicionar a curva de juros como a ferramenta que resolve essa tensão.

---

### Ato 2a — De onde vêm os dados
*(4 min, 2 slides)*

A curva não é construída pelo banco — ela é descoberta no mercado. Os contratos de DI futuro negociados na B3 são o termômetro: cada vencimento negociado é um ponto de consenso entre compradores e vendedores sobre o preço do dinheiro naquele prazo. O primeiro slide mostra quais são esses instrumentos e por que são escolhidos (liquidez, transparência, padronização). O segundo mostra que esses pontos são esparsos — o mercado negocia 15 vencimentos, mas o banco precisa de muito mais. O objetivo é que o leitor entenda a distinção fundamental entre dado observado e dado inferido, e perceba que a qualidade da curva começa na qualidade da fonte.

---

### Ato 2b — Como a taxa vira preço
*(4 min, 2 slides)*

Uma taxa é uma instrução. Um fator de desconto é a execução dessa instrução. Este ato faz a ponte entre os dois: dado um vértice com taxa 12% a.a. para 252 dias úteis, como isso se transforma no peso que multiplica um fluxo futuro para trazê-lo a hoje? O primeiro slide constrói essa intuição com números redondos — R$ 1.000 prometidos daqui a 1 ano valem R$ X hoje, e por quê. O segundo mostra que quanto mais distante o prazo, mais o fator cresce e mais o valor presente encolhe — o tempo corrói o valor, e a curva mede essa corrosão ponto a ponto. O objetivo é que o leitor saia com a imagem mental de que a curva é uma régua de pesos, não uma linha de taxas.

---

### Ato 2c — Interpolação e vida da curva
*(4 min, 2 slides)*

Com 15 pontos ancoradores, o banco precisa inferir o preço de todos os outros. O flat forward é a hipótese mais conservadora: entre dois vértices, a taxa forward é constante — não se inventa variação onde o mercado não deu informação. O primeiro slide usa o gif da animação para mostrar esse processo em movimento: vértices aparecem, a curva spot se desenha, os segmentos forward emergem. O segundo slide mostra que esse resultado não é estático — a curva é reconstruída todo dia conforme novos negócios acontecem na B3, e uma curva de ontem já é história. O objetivo é que o leitor saia com a imagem de uma curva viva, que respira com o mercado, e comece a perceber o que significa depender dela operacionalmente.

---

### Ato 3 — A curva dentro do banco
*(4 min, 2 slides)*

A curva construída nos atos anteriores não fica num sistema isolado — ela atravessa o banco inteiro. O primeiro slide mapeia os três usos centrais: tesouraria a usa para precificar cada operação antes de fechar (se o spread não cobre o custo de funding, a operação não é viável); risco a usa para calcular a sensibilidade do portfólio a movimentos de mercado; contabilidade a usa para marcar a carteira a valor justo todo dia. O segundo slide mostra que esses três usos estão encadeados — a mesma curva, lida de formas diferentes, gera decisões diferentes em áreas diferentes ao mesmo tempo. O objetivo é que o leitor perceba que um erro na curva não é um problema localizado: ele se propaga pelas três áreas simultaneamente.

---

### Ato 4 — O que a forma diz
*(3 min, 2 slides)*

Uma curva não precisa ser calculada para ser lida — sua forma já comunica. O primeiro slide apresenta os três formatos clássicos lado a lado: normal (inclinada para cima), invertida, plana — cada um com uma frase sobre o que o mercado está dizendo. O segundo slide traz a aplicação prática: como um gestor de risco ou um tesoureiro lê a forma da curva antes de qualquer modelo para calibrar o apetite de risco do dia. O objetivo é mostrar que senioridade em mercado inclui leitura qualitativa — saber o que a curva está sinalizando antes de abrir qualquer sistema.

---

### Ato 5 — Quando a curva se move
*(3 min, 2 slides)*

A curva subiu 100bps. Qual é o impacto real no portfólio? O primeiro slide constrói a intuição de sensibilidade: um fluxo daqui a 6 meses perde pouco; um fluxo daqui a 10 anos perde muito mais — porque o fator de desconto se aplica por mais tempo. Prazo amplifica risco, e isso tem nome: duration. O conceito aparece aqui como consequência natural da intuição, não como definição. O segundo slide mostra dois portfólios com a mesma duration mas composições diferentes — um concentrado no curto prazo, outro no longo — e como eles reagem de forma distinta a uma mudança de forma da curva (não só de nível). O objetivo é que o leitor entenda que risco de curva não é um número, é um perfil.

---

### Ato 6 — Dado errado, decisão errada
*(4 min, 2 slides)*

Fechamento com o gancho direto para o público. A curva que o banco usa não nasce pronta — ela passa por um pipeline de dados antes de chegar em qualquer sistema de risco ou precificação. O primeiro slide mapeia esse fluxo: B3 → ingestão → validação → construção da curva → sistemas downstream. Em cada etapa há um ponto de falha: dado atrasado, vértice faltando, convenção de dia útil errada, versão desatualizada em produção. O segundo slide traz um caso hipotético concreto — uma curva desatualizada em 1 dia útil durante um movimento brusco de mercado — e mostra o efeito cascata: preço errado, P&L distorcido, hedge subdimensionado, decisão equivocada. O objetivo é que o leitor saia com a consciência de que a qualidade do dado de curva não é detalhe técnico — é risco operacional com impacto direto no resultado do banco. E que o trabalho de analytics está na fundação disso.
