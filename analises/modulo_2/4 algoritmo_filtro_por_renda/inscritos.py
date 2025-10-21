# o objetivo deste, eh que , para o FIES eh necessario voce atender certos requisitos
# para tal logo faremos uma criacao de nova coluna chamada filtro_renda_fies
# q analisa POR ano de cada linha se tal linha atende as condicoes necessarias de renda deste respectivo ano
# ou seja ter ate  salarios minimo atraves da coluna:  'renda_mensal_bruta_per_capita'

# %%
import pandas as pd

pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)

