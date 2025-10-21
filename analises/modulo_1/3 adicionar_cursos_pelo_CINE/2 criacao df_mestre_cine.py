# %%
import pandas as pd


colunas_cine= [
'NU_ANO_CENSO',
'NO_CURSO',
'CO_CURSO',
# 'NO_CINE_ROTULO',
# 'CO_CINE_ROTULO',
'CO_CINE_AREA_GERAL',
'NO_CINE_AREA_GERAL',
# 'CO_CINE_AREA_ESPECIFICA',
# 'NO_CINE_AREA_ESPECIFICA',
# 'CO_CINE_AREA_DETALHADA',
# 'NO_CINE_AREA_DETALHADA',
]


lista_dfs= []


for ano in range(2016,2025): # 2025 nao eh incluso entao vai ate 2024
 
    caminho_externo= f'../../../planilhas/externo/MICRODADOS_CADASTRO_CURSOS_{ano}.csv'


    df_externo_cine= pd.read_csv(
        caminho_externo,
        encoding='latin-1',
        sep=';',
        low_memory=False,
        decimal=',',
        usecols=colunas_cine)

    
    lista_dfs.append(df_externo_cine)

df_concat= pd.concat(lista_dfs)

display(df_concat) #type: ignore


caminho_salvar= '../../../planilhas/externo/df_mestre_cadastro_cursos_2016_2024.csv'

df_concat.to_csv(caminho_salvar,index=0,encoding='utf-8-sig')
# %%
