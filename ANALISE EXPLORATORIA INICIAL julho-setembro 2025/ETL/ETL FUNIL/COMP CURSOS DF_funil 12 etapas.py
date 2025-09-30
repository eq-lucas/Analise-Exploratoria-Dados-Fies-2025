# %% 

import pandas as pd

path='../../../planilhas/COMP DF_funil 12 etapas.csv'

df_bruto=pd.read_csv(path)

colunasRuimSomar=["Ano","Semestre","UF do Local de Oferta","Nome do Curso"]

colunas=[col for col in df_bruto.columns.to_list() if col not in colunasRuimSomar]

df=df_bruto.groupby(["Ano","Semestre","Nome do Curso"],as_index=False)[colunas].sum()

df

# %%
df.to_csv('../../../planilhas/COMP CURSOS DF_funil 12 etapas.csv',index=False)
# %%
