## Competitive Pokémon Mindgames

Relatório do primeiro trabalho de Inteligência Computacional, por Victor Hernandes Silva Maia.

## Introdução

Pokémon é um jogo de estratégia 1-contra-1 baseado em turnos. Ao início de uma partida, cada jogador monta uma equipe de 6 Pokémon (dentre quase 1000 possíveis) e seleciona um destes como "ativo". A cada turno, cada jogador opta, secretamente, por uma dentre duas opções: atacar o Pokémon ativo de seu oponente ou substituir o seu por outro em sua equipe. Alguns ataques causam dano. Um Pokémon é eliminado ao sofrer determinada quantidade de dano. Vence aquele que eliminar toda a equipe adversária.

!["hail heil trump" ataca seu adversário com o golpe Thunderbolt](https://github.com/MaiaVictor/Trabalho-IC-UFRJ/blob/master/images/gameplay.png?raw=true)

Em níveis mais altos, como o de torneios pela internet, esta se torna, essencialmente, uma competição preditiva. Suponha que, por exemplo, você esteja enfrentando um Pokémon de fogo. O instinto mais natural seria usar um golpe d'água. Na prática, porém, seu oponente anteciparia essa jogada e enviaria, por exemplo, um Pokémon de planta, que é forte contra água. Seria prudente, portanto, antecipar a antecipação e trocar para um de fogo; a não ser, é claro, que seu oponente antecipe a antecipação de sua antecipação e mantenha o de água. Esse tipo de jogo mental é fundamental e, em geral, se sobressai o jogador com maior capacidade de emular o pensamento adversário.

O objetivo deste trabalho é usar métodos de inteligência computacional para, dado um determinado estado de jogo, prever o próximo movimento de um oponente. Especificamente, tentaremos determinar se ele atacará ou substituirá seu Pokémon, tendo em vista que essa informação traz enorme vantagem competitiva. Temos, portanto, um problema de classificação binária.

### Captação dos Dados

Os dados foram combinados de variadas fontes: do site [Kaggle](https://www.kaggle.com/abcsds/pokemon), foi obtida uma tabela com todos os Pokémon existentes, inclusive atributos relevantes para as batalhas. Do site [Smogon](http://www.smogon.com/), a maior comunidade de Pokémon competitivo do mundo, foi obtida a estatística referente ao uso de cada Pokémon em batalhas rankeadas. Finalmente, foi criado um script para:

1. Acessar o site [pokemonshowdown.com](http://pokemonshowdown.com/), o emulador de batalhas online mais popular;

2. Baixar os jogos rankeados mais recentes na categoria principal ("OU format"), disponíveis no link [http://replay.pokemonshowdown.com/](http://replay.pokemonshowdown.com/);

3. Extrair, do HTML obtido, o log da batalha, em texto;

4. Processar este log de forma a computar o estado do jogo em cada turno, do início até o final;

5. Para cada jogo, para cada turno, salvar dois registros, armazenando ao estado do jogo naquele momento, sob o ponto de vista de cada jogador.

Esse script rodou por cerca de 10 horas, obtendo, no total, 73998 registros, provenientes de 1508 batalhas, a uma média de 24.53 turnos por batalha. As informações relevantes de cada Pokémon ativo, previamente obtidas, foram agregadas a cada registro. O resultado foi salvo no formato CSV.

### Descrição dos Dados

O dataset gerado consiste em uma matriz de números de ponto flutuante onde cada linha é um registro contendo o estado de um determinado momento de um determinado jogo sob o ponto de vista de um determinado jogador. Ele contém as seguintes variáveis:

Var | Desc.
--- | ---
turn | Número do turno (0 = primeiro, 1 = segundo, etc.).
a_elo | [score estatístico](https://pokemonshowdown.com/users/eloratings) da plataforma Showdown que estima a habilidade competitiva do jogador.
a_health | Quantidade de pontos de vida de seu Pokémon ativo, que começa em 1 (vida cheia) e pode descer até 0 (eliminado).
a_hp | Atributo HP do Pokémon ativo, que influencia o quanto de vida aquele Pokémon tem inicialmente.
a_atk | Atributo ATK do Pokémon ativo, que influencia positivamente o dano causado por seus golpes físicos.
a_def | Atributo DEF do Pokémon ativo, que influencia negativamente o dano recebido por golpes físicos.
a_spa | Atributo SPA do Pokémon ativo, que influencia positivamente o dano causado por seus golpes especiais.
a_spd | Atributo SPD do Pokémon ativo, que influencia negativamente o dano recebido por golpes especiais.
a_spe | O atributo SPE do Pokémon ativo, que influencia qual Pokémon atacará primeiro em um turno.
a_usage | Percentual de vezes que esse Pokémon apareceu em uma batalha no formato principal no mês de Outubro.
a_boost | Somatório de boosts. Cada boost aumenta em 50% o valor de um atributo deste Pokémon.
a_status | 1 se o Pokémon ativo está afetado por algum status negativo (burn, poison, etc.).
a_party | Somatório da quantidade de pontos de vida de todos os Pokémon em sua equipe (variando de 0 a 6).
b_elo | Vide acima, mas referente ao seu adversário.
b_health | Vide acima.
b_hp | Vide acima.
b_atk | Vide acima.
b_def | Vide acima.
b_spa | Vide acima.
b_spd | Vide acima.
b_spe | Vide acima.
b_usage | Vide acima.
b_boost | Vide acima.
b_status | Vide acima.
b_party | Vide acima.
switch | Variável de saída, sendo 1 se o próximo movimento do adversário foi substituir seu Pokémon, 0 se foi um ataque.

Apesar de essencial para o decorrer do jogo, não foram consideradas as informações de [tipo](https://img.pokemondb.net/images/typechart.png?raw=true) de ambos os Pokémon, por não ser óbvia a melhor maneira de representá-las de forma útil.

### Análise exploratória

Inicialmente, realizamos uma caracterização estatística das variáveis envolvidas:

x | mean | std | min | 25% | 50% | 75% | max
--- | --- | --- | --- | --- | --- | --- | ---
turn | 16.380956 | 18.854810 | 0.0000 | 6.000000 | 13.000000 | 22.000000 | 283.00000
a_elo | 1309.212708 | 230.060295 | 1000.0000 | 1125.000000 | 1255.000000 | 1446.000000 | 2014.00000
a_health | 0.702033 | 0.306867 | 0.0000 | 0.490856 | 0.791123 | 1.000000 | 1.00000
a_hp | 86.233290 | 32.706629 | 1.0000 | 70.000000 | 80.000000 | 95.000000 | 255.00000
a_atk | 91.061123 | 30.084034 | 5.0000 | 70.500000 | 90.000000 | 112.000000 | 170.00000
a_def | 88.589840 | 28.559892 | 5.0000 | 73.000000 | 85.000000 | 100.000000 | 230.00000
a_spa | 86.419173 | 28.441092 | 10.0000 | 60.000000 | 95.000000 | 105.000000 | 150.00000
a_spd | 89.172626 | 21.877420 | 20.0000 | 75.000000 | 90.000000 | 100.000000 | 230.00000
a_spe | 79.726074 | 26.408954 | 5.0000 | 60.000000 | 80.000000 | 100.000000 | 160.00000
a_usage | 5.541367 | 5.302560 | 0.0008 | 0.999400 | 3.850690 | 9.717020 | 21.39034
a_boost | 0.314819 | 1.401398 | -6.0000 | 0.000000 | 0.000000 | 0.000000 | 6.00000
a_status | 0.116260 | 0.320538 | 0.0000 | 0.000000 | 0.000000 | 0.000000 | 1.00000
a_party | 3.820999 | 1.654648 | 0.0000 | 2.623765 | 4.015708 | 5.184263 | 6.00000
b_elo | 1309.212708 | 230.060295 | 1000.0000 | 1125.000000 | 1255.000000 | 1446.000000 | 2014.00000
b_health | 0.702033 | 0.306867 | 0.0000 | 0.490856 | 0.791123 | 1.000000 | 1.00000
b_hp | 86.233290 | 32.706629 | 1.0000 | 70.000000 | 80.000000 | 95.000000 | 255.00000
b_atk | 91.061123 | 30.084034 | 5.0000 | 70.500000 | 90.000000 | 112.000000 | 170.00000
b_def | 88.589840 | 28.559892 | 5.0000 | 73.000000 | 85.000000 | 100.000000 | 230.00000
b_spa | 86.419173 | 28.441092 | 10.0000 | 60.000000 | 95.000000 | 105.000000 | 150.00000
b_spd | 89.172626 | 21.877420 | 20.0000 | 75.000000 | 90.000000 | 100.000000 | 230.00000
b_spe | 79.726074 | 26.408954 | 5.0000 | 60.000000 | 80.000000 | 100.000000 | 160.00000
b_usage | 5.541367 | 5.302560 | 0.0008 | 0.999400 | 3.850690 | 9.717020 | 21.39034
b_boost | 0.314819 | 1.401398 | -6.0000 | 0.000000 | 0.000000 | 0.000000 | 6.00000
b_status | 0.116260 | 0.320538 | 0.0000 | 0.000000 | 0.000000 | 0.000000 | 1.00000
b_party | 3.820999 | 1.654648 | 0.0000 | 2.623765 | 4.015708 | 5.184263 | 6.00000
switch | 0.169167 | 0.374902 | 0.0000 | 0.000000 | 0.000000 | 0.000000 | 1.00000

Podemos, através dessa tabela, observar alguns fatos interessantes. Na primeiro atributo, `turn`, observamos um valor esperado de cerca de 16 e um desvio padrão de cerda de 18, o que significa que a maior parte dos jogos costuma durar não mais que 50 turnos. O que chama a atenção, porém, é o valor máximo de 283, cerca de 14 desvios padrões acima da média. Isso motiva a suspeita da existência de outliers. Geramos o box plot desta variável:

![Turn outliers](https://github.com/MaiaVictor/Trabalho-IC-UFRJ/blob/master/images/turn_boxplot.png?raw=true)

Através deste é possível constatar, claramente, que uma quantidade ínfima de registros possui a contagem de turno muito acima dos demais. Em alguns casos, outliers podem conter informações importantes. Do ponto de vista do dataset estudado, porém, esse não é o caso: uma batalha competitiva, de fato, raramente ultrapassa 70 turnos. Esses registros pertencem, muito provavelmente, a batalhas onde ambos os jogadores não estavam, de fato, competindo, como é de se esperar em um jogo rankeado. Sendo assim, pouco podemos aprender sobre a estratégia do jogo estudando esses casos e é justificável removê-los do dataset, que passa, então, a ter 73102 registros (896, ou 1.2%, a menos). 

Observando o registro `a_hp`, encontramos uma situação parecida: o valor máximo encontra-se a mais de 5 desvios padrões acima da média. Novamente, gerando seu box plot, é possível visualizar melhor a situação:

![HP outliers](https://github.com/MaiaVictor/Trabalho-IC-UFRJ/blob/master/images/a_hp_boxplot.png?raw=true)

Interessantemente, temos alguns outliers moderados em torno de 150 pontos, e dois extremos perto dos 250 pontos! Seria extremamente tentador remover essas claras aberrações estatísticas. Refletindo sobre a semântica destes dados, porém, notamos a necessidade de cautela.

![Chansey](https://github.com/MaiaVictor/Trabalho-IC-UFRJ/blob/master/images/fairy_lord.png?raw=true)
![Blissey](https://github.com/MaiaVictor/Trabalho-IC-UFRJ/blob/master/images/fairy_overlord.png?raw=true)

Chansey e Blissey são dois Pokémon únicos justamente pelas suas distribuições de stats notavelmente desproporcionais, concentrando uma enorme quantidade de HP (pontos de vida) e SPE (defesa especial), a troco de quantidades ínfimas de ATK (ataque) e DEF (defesa). Devido a essa rara combinação, ambos possuem uma capacidade incomparável de bloquear golpes especiais e são, portanto, peças fundamentais no time de muitos jogadores, aparecendo em nada menos que 8% de todas as batalhas realizadas no último mês. 

A presença desses outliers aponta, simplesmente, o uso de uma Chansey ou Blissey naquele turno. Registros contendo esses Pokémon podem carregar informações valiosas a respeito do comportamento dos jogadores diante de uma postura altamente defensiva do adversário e, portanto, removê-los seria um erro grave. De fato, realizar uma análise de outliers em qualquer um dos atributos de stats isoladamente não faria sentido dada a semântica desses dados. Sendo assim, precisamos de um método mais robusto.

![Distance matrix](https://github.com/MaiaVictor/Trabalho-IC-UFRJ/blob/master/images/dist_matrix.png?raw=true)

A matriz de distâncias é uma forma bem eficaz fe visualizar outliers. Neste plot, normalizado pelos valores max/min e ordenado por classe, é possível reparar que membros de uma mesma classe estão levemente mais próximos entre si que com relação aos da classe oposta. Devido a grande quantia de registros, porém, não foi possível computar a matriz completa com as ferramentas disponíveis. Para a detecção de outliers, portanto, optamos por gerar uma lista de registros ordenada pela distância média:

![Distance list](https://github.com/MaiaVictor/Trabalho-IC-UFRJ/blob/master/images/dists.png?raw=true)

A partir desta visualização, é possível constatar que, apesar de alguns poucos registros acima de 2.2, não existe nenhum com uma distância extremamente acima da esperada. Sendo assim, mantivemos o dataset sem mais alterações. Para prosseguir com a exploração dos dados, geramos um histograma de cada variável.

![Histograms](https://github.com/MaiaVictor/Trabalho-IC-UFRJ/blob/master/images/histograms.png?raw=true)

A análise destes gráficos permite um melhor entendimento das característica do problema. As variáveis relacionadas a vida, `a_health`, `b_health`, `a_party` e `b_party`, por exemplo, se destacam por terem uma concentração muito grande de registros com o valor inicial (1 ou 6). Isso é de se esperar, pois a quantidade de vida de um Pokémon permanece imutável por diversos turnos, até que este seja finalmente atacado. As variáveis `a_boost` e `b_boost`, referentes à quantidade de power-ups recebidos por determinado Pokémon são, de forma parecida, altamente concentradas no estado padrão, 0. 

Nas variáveis de stats, `a_hp`, `a_atk`, `a_def`, `a_spa`, `a_spd`, `a_spe`, `b_hp`, `b_atk`, `b_def`, `b_spa`, `b_spd`, `b_spe`, encontramos, em geral, uma distribuição aproximadamente normal, o que reflete a dispersão destes stats nos Pokémon criados pela Nintendo. Notavelmente, é possível observar claramente a presença da Chansey e da Blissey no canto direito dos histogramas `a_hp` e `b_hp`.

A variável `turn` segue quase perfeitamente a distribuição normal, o que é de se esperar, já que, a cada turno, há uma probabilidade similar do jogo terminar. As variáveis `a_elo` e `b_elo` nos permitem refletir sobre o critério de rankeamento que jogadores adotado pelo Showdown que, por exemplo, devido ao chão de 1000 designado para proteger novatos, causa um corte artificial na curva.

As variáveis `a_status` e `b_status` nos mostram o quão incomum é ser afetado por um status e, por fim, a variável `switch` nos mostra que a classe que desejamos identificar é aproximadamente 5x menos comum que a padrão. Não há, em geral, nenhuma grande anomalia nos histogramas.

Uma próxima pergunta natural a se fazer é: existem variáveis correlacionadas? Esse seria o caso se, por exemplo, um Pokémon com um alto ataque geralmente fosse acompanhado de uma alta velocidade. Podemos procurar essa resposta na matriz de correlações:

![Correlations](https://github.com/MaiaVictor/Trabalho-IC-UFRJ/blob/master/images/corr_matrix.png?raw=true)

Observamos uma forte correlação negativa entre o turno e a quantidade de vida total na equipe de cada jogador. Isso faz sentido dado que, quanto mais turnos passam, mais dano é causado. Observamos também uma forte correlação positiva entre a quantidade de vida total na equipe do jogador e na de seu oponente, pelo mesmo motivo. Finalmente, observamos uma forte correlação entre o elo de cada jogador. Isso pode ser explicado devido ao algoritmo de matchmaking do Showdown, que procura gerar batalhas entre jogadores com nível de habilidade similares. Estas correlações, que deverão ser posteriormente tratadas, são refletidas nas matrizes de dispersão:

![sc00](https://github.com/MaiaVictor/Trabalho-IC-UFRJ/blob/master/images/scatter_matrix_0_0.png?raw=true)

![sc01](https://github.com/MaiaVictor/Trabalho-IC-UFRJ/blob/master/images/scatter_matrix_0_1.png?raw=true)

![sc10](https://github.com/MaiaVictor/Trabalho-IC-UFRJ/blob/master/images/scatter_matrix_0_1.png?raw=true)

![sc11](https://github.com/MaiaVictor/Trabalho-IC-UFRJ/blob/master/images/scatter_matrix_1_1.png?raw=true)

Além da clara correlação linear entre as variáveis citadas, podemos utilizar essa matriz para refletir sobre a geometria do problema. Para tal, utilizamos a cor vermelha nos registros da classe que queremos identificar (switch = 1) e ciano nos demais (switch = 0). Devido ao grande número de registros, porém, muitos pontos se sobrescrevem. Para resolver esse problema, utilizamos valores alfa inversamente proporcionais à probabilidade de se encontrar um registro daquela classe. Deste modo, nesta visualização, pontos predominantemente vermelhos apontam a existência de um número de registros com a classe desejada acima do esperado, e vice-versa.

Repare, por exemplo, na variável `b_boost`: em todos os plots há uma forte tendência da cor verde aparecer no canto direito, o que indica que, claramente, oponentes com boosts positivos tendem a permanecer em campo. O mesmo não ocorre com `a_boost`. Com a vida ocorre, curiosamente, o oposto: quanto mais saudável um Pokémon, maior sua tendência de ser substituído. O valor do `elo` de um jogador parece influenciar positivamente suas chances de substituir seu Pokémon a qualquer momento. Isso faz sentido pois, de fato, jogadores mais experientes apostam mais em substituições, enquanto jogadores novatos apostam em ataques diretos. O formato curioso da relação entre as variáveis `party` e `health` reflete o fato de que o somatório dessas é sempre 6. 

No que diz respeito a stats, podemos observar que, os comparando entre seu próprio Pokémon ativo, obtemos, naturalmente, a sua distribuição normal tal como designada pela Nintendo. Mais interessante para nossa análise é a comparação entre os stats de seu Pokémon ativo com os de seu oponente. Observe, por exemplo, a dispersão entre `a_spe` e `b_spe`. Existe uma visível tendencia da cor vermelha aparecer nos casos onde `b_spe < a_spe`. Isso faz sentido, pois este atributo determina quem ataca primeiro. É natural que um oponente em vantagem de velocidade tenha maior tendência a atacar já que, em muitos casos, essa vantagem pode ser convertida em um nocaute, o que, por sua vez, protege o adversário de um eventual ataque seu, removendo a necessidade de uma substituição. Outros plots como o `a_atk` e `b_atk` não apresentam uma polaridade visível, indicando que a interação destes não afeta consideravelmente a tendência do oponente de recuar.

### Tecnologias utilizadas

Para captação dos dados, foi utilizado JavaScript, Node.js e Superagent. Para análise e visualização dos dados, foi utilizado Python com as libs Pandas, Numpy e matplotlib. Para o plot das matrizes de dispersão, foi necessário modificar o código original tendo em vista que este acusava erro de memória para plotar a matriz 26x26, e não permitia comparar grupos de atributos diferentes para que se dividisse o mesmo em 4 sub-plots 13x13, como feito. Para o plot das distâncias médias, foi necessário realizar a computação separadamente tendo em vista que a lib de Python, novamente, demorava demais. Todo o código escrito está disponível no repositório [https://github.com/MaiaVictor/Trabalho-IC-UFRJ/](https://github.com/MaiaVictor/Trabalho-IC-UFRJ/).
