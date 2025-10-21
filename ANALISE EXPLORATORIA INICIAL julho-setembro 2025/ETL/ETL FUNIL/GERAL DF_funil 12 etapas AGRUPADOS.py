# %% 

import pandas as pd

path='../../../planilhas/GERAL DF_funil 12 etapas.csv'

df_bruto=pd.read_csv(path)

colunasRuimSomar=["Ano","Semestre","UF do Local de Oferta","Nome do Curso"]

colunas=[col for col in df_bruto.columns.to_list() if col not in colunasRuimSomar]

df=df_bruto.groupby(["Ano","Semestre"],as_index=False)[colunas].sum()

df

# %%
df.to_csv('../../../planilhas/GERAL DF_funil 12 etapas AGRUPADOS.csv',index=False)
# %%
