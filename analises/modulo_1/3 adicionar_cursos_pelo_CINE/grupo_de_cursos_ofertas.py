# %%
import pandas as pd
import os

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)


anos=[2019,2020,2021]
semestres=[1,2]


path = '../../../planilhas/limpo/modulo_1/ofertas/'


arquivo= 'fies_{semestre}_ofertas_{year}_limpo.csv'



for ano in anos:


    caminho_externo= f'../../../planilhas/externo/MICRODADOS_CADASTRO_CURSOS_{ano}.CSV'


    df_externo_cine= pd.read_csv(caminho_externo,encoding='latin-1',sep=';',low_memory=False)


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

    df_externo = df_externo_cine[colunas_cine]


    for semestre in semestres:

        caminho= os.path.join(path,arquivo.format(semestre=semestre,year=ano))

        df_temp = pd.read_csv(caminho,encoding='utf-8-sig')


        df_temp['codigo_curso_ofertas'] = pd.to_numeric(
        df_temp['codigo_curso_ofertas'], 
        errors='coerce'
        )



        df_mergiado= pd.merge(
            df_temp,
            df_externo,
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
