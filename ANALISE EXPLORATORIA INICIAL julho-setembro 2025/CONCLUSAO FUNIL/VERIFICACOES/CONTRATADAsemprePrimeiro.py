# %%
import pandas as pd
import os
import numpy as np

pd.set_option('display.max_columns', None)

caminho_inscricoes = '../../../planilhas ETL/GERAL ETL inscritos peneira FIES P_FIES.csv'

dfi = pd.read_csv(caminho_inscricoes)


df_final= dfi.sort_values('Situação Inscrição Fies').groupby('Situação Inscrição Fies')['ID do estudante'].count().reset_index().head(50)

df_final
# %%
df_final.to_csv('../../../planilhas/DF qtde de ESTUDANTES em cada situcao.csv',index=False)
# %%