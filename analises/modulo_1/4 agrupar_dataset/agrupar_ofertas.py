# %%
import pandas as pd
import os

pd.set_option('display.max_columns', None)

path = '../../../planilhas/limpo/modulo_1/ofertas_coluna_CINE'

lista_nomes_arquivos= os.listdir(path=path)

lista_dfs= []

for arquivo in lista_nomes_arquivos:

    if arquivo.endswith('.csv'):

        caminho= os.path.join(path,arquivo) 

        df_temp= pd.read_csv(caminho)

        lista_dfs.append(df_temp)

df_concat= pd.concat(lista_dfs)

ordem= [    
'ano_ofertas',
'semestre_ofertas', 
]

df_concat_ordenado_ano_semestre= df_concat.sort_values(by=ordem)

caminho_salvar= '../../../planilhas/limpo/modulo_1/agrupado/'

nome_salvar=os.path.join(caminho_salvar,'ofertas_agrupado.csv')

df_concat_ordenado_ano_semestre.to_csv(nome_salvar,index=False,encoding='utf-8-sig')

display(df_concat_ordenado_ano_semestre) # type: ignore

# %%
