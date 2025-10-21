# %%
import pandas as pd
import os

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)


anos=[2019,2020,2021]
semestres=[1,2]


path = '../../../planilhas/limpo/modulo_1/ofertas/'


arquivo= 'fies_{semestre}_ofertas_{year}_limpo.csv'


caminho_externo= f'../../../planilhas/externo/df_mestre_cadastro_cursos_2016_2024.csv'

df_externo_cine= pd.read_csv(caminho_externo,encoding='utf-8-sig',low_memory=False)

colunas_cine= [
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

# 1. Ordena por ano (assume que 'NU_ANO_CENSO' existe no seu .csv mestre)
df_mestre_deduplicado = df_externo_cine.sort_values(by='NU_ANO_CENSO', ascending=True)
    
    # 2. Remove duplicados em 'CO_CURSO', mantendo o último (mais recente)
df_mestre_deduplicado = df_mestre_deduplicado.drop_duplicates(subset=['CO_CURSO'], keep='last')

df_mestre_deduplicado = df_mestre_deduplicado[colunas_cine]


for ano in anos:


    for semestre in semestres:

        caminho= os.path.join(path,arquivo.format(semestre=semestre,year=ano))

        df_temp = pd.read_csv(caminho,encoding='utf-8-sig')


        df_temp['codigo_curso_ofertas'] = pd.to_numeric(
        df_temp['codigo_curso_ofertas'], 
        errors='coerce'
        )



        df_mergiado= pd.merge(
            df_temp,
            df_mestre_deduplicado,
            how='left',
            left_on='codigo_curso_ofertas',
            right_on='CO_CURSO',
            suffixes=['','_cine']
        )

        path_salvar= '../../../planilhas/limpo/modulo_1/ofertas_coluna_CINE/'
        nome_salvar = f'fies_{semestre}_ofertas_{ano}_limpo_cine.csv'

        caminho_salvar= os.path.join(path_salvar,nome_salvar)

        df_mergiado.to_csv(caminho_salvar,index=False,encoding='utf-8-sig')



#display(df_externo_cine.columns.to_list()) # type: ignore

'''
 'NO_CURSO',
 'CO_CURSO',
 'NO_CINE_ROTULO',
 'CO_CINE_ROTULO',
 'CO_CINE_AREA_GERAL',
 'NO_CINE_AREA_GERAL',
 'CO_CINE_AREA_ESPECIFICA',
 'NO_CINE_AREA_ESPECIFICA',
 'CO_CINE_AREA_DETALHADA',
 'NO_CINE_AREA_DETALHADA',
'''

# %%
