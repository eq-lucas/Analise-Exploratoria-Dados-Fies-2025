# %%
import pandas as pd

pd.set_option('display.max_columns', None)

path= '../../../planilhas/GERAL DF_funil 12 etapas.csv'

df=pd.read_csv(path)



#PARTE PARA DEIXAR APENAS OS DE COMPUTACAO
cursosComputacao = [
    'ANÁLISE E DESENVOLVIMENTO DE SISTEMAS',
    'CIÊNCIA DA COMPUTAÇÃO',
    'SISTEMAS DE INFORMAÇÃO',
    'REDES DE COMPUTADORES',
    'ENGENHARIA DA COMPUTAÇÃO',
    'ENGENHARIA DE SOFTWARE'
]

filtro_computacao = df['Nome do Curso'].isin(cursosComputacao)
df_comp = df[filtro_computacao].copy()


df_comp
# %%
df_comp.to_csv('../../../planilhas/COMP DF_funil 12 etapas.csv', index=False)
# %%