# %%
import pandas as pd
import os
pd.set_option('display.max_columns', None)


path="../../../csv originais/inscricoes CORRIGIDAS/fies_2_inscricao_2020.csv"

df =pd.read_csv(path)

df[['ID do estudante','Renda mensal bruta per capita']]
# %%

dfzao=df

dfzao['Renda mensal bruta per capita'] = pd.to_numeric(
    dfzao['Renda mensal bruta per capita'].astype(str).str.replace(',', '.'), 
    errors='coerce'
)
dfzao[['ID do estudante','Renda mensal bruta per capita']]
# %%
filtro= df['ID do estudante'] == 203950972
filtrob= df['ID do estudante'] == 203950972

# %%
dfzao[filtrob][['ID do estudante','Renda mensal bruta per capita']]

# %%
df[filtro][['ID do estudante','Renda mensal bruta per capita']]
# %%
