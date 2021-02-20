# krakenpy

Hey there, friend.<br>
This project is a wrapper for the [Kraken API](https://www.kraken.com/features/api).

This is still a work in progress, and I'm not an expert, so I just hope it works.

Initialisation :
```py
from krakenpy import Krakenpy

# Creates the object
k = Krakenpy()
```

### Example

```py
import pandas as pd
from krakenpy import Krakenpy

k = Krakenpy()

ohlc_data = k.public.get_ohlc('ETHEUR', interval=21600)

df = pd.DataFrame(ohlc_data)
print(df)
```

Output :

```
           time     open     high      low    close     vwap            volume    count    pair
0    1438560000     2.87     3.80     0.52     1.07     1.23    59156.09090879      824  ETHEUR
1    1439856000     1.06     1.40     0.93     1.23     1.15    47159.80816480      551  ETHEUR
2    1441152000     1.20     1.24     0.76     0.81     1.04    31273.71863507      406  ETHEUR
3    1442448000     0.79     0.85     0.50     0.62     0.64    22974.03451287      338  ETHEUR
4    1443744000     0.60     0.64     0.42     0.46     0.54    17564.81166384      404  ETHEUR
..          ...      ...      ...      ...      ...      ...               ...      ...     ...
131  1608336000   533.51   637.10   451.32   624.34   557.90   923886.60569569   354501  ETHEUR
132  1609632000   624.00  1079.99   613.72  1019.71   911.52  2660882.85467999  1037334  ETHEUR
133  1610928000  1019.68  1208.17   855.01  1139.29  1075.56  1550773.87520979   635493  ETHEUR
134  1612224000  1139.00  1545.00  1128.23  1474.34  1391.00  1240698.60806868   677113  ETHEUR
135  1613520000  1474.34  1669.26  1436.40  1656.80  1576.50   204609.06231452   127003  ETHEUR

[136 rows x 9 columns]
```
