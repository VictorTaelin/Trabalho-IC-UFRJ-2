## Introdução

O objetivo deste trabalho é tentar prever o tipo de um Pokémon baseado em seus atributos.

## Dataset

O dataset utilizado foi obtido do site [Kaggle](https://www.kaggle.com/mylesoneill/d/mylesoneill/pokemon-sun-and-moon-gen-7-stats/new-sun-and-moon-pokemon-analysis), e posteriormente filtrado para remover campos irrelevantes. Ele contém os seguitnes dados:

| Variável | Significado |
| --- | --- |
| type | Tipo do Pokémon |
| HP | Pontos de vida |
| ATK | Pontos de ataque físico |
| DEF | Pontos de defesa física |
| SPA | Pontos de ataque especial |
| SPD | Pontos de defesa especial |
| SPE | Pontos de velocidade |
| weight | Peso, em quilogramas. |
| height | Altura, em metros. |

## Análise exploratória

### Estatísticas dos dados

var | count | mean | std | min | 25% | 50% | 75% | max
--- | --- | --- | --- | --- | --- | --- | --- | --- | 
hp | 1061.0 | 70.041470 | 25.893508 | 1.000000 | 50.00000 | 68.000000 | 80.000000 | 255.000000
atk | 1061.0 | 79.602262 | 31.378369 | 5.000000 | 55.00000 | 75.000000 | 100.000000 | 190.000000
def | 1061.0 | 73.730443 | 30.394899 | 5.000000 | 50.00000 | 70.000000 | 91.000000 | 230.000000
spa | 1061.0 | 74.550424 | 31.975146 | 10.000000 | 50.00000 | 70.000000 | 95.000000 | 194.000000
spd | 1061.0 | 72.911404 | 27.995681 | 20.000000 | 50.00000 | 70.000000 | 90.000000 | 230.000000
spe | 1061.0 | 70.321395 | 29.328288 | 5.000000 | 48.00000 | 68.000000 | 93.000000 | 180.000000
weight | 1061.0 | 67.115712 | 118.840958 | 0.090718 | 8.48217 | 27.986626 | 71.486099 | 999.898205
height | 1061.0 | 1.248694 | 1.241338 | 0.101600 | 0.50800 | 0.990600 | 1.498600 | 14.503400

Temos um total de 1061 Pokémon, contando formas diferentes como Pokémon diferentes. Com relação aos stats, podemos observar que todos tem comportamentos bem similares, com uma média de 70 a 80, e desvio padrão na casa dos 30. O peso fica em torno de 67kg, com o mínimo de cerca de 90g e o máximo de quase 1 tonelada. O pokémon mais curto mede 10cm, o maior chega a 14.5m, e a média é de 1.24m.
