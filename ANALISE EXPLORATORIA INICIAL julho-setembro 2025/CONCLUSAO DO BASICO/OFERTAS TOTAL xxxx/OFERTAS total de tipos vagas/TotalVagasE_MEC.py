# %%
import pandas as pd

ano=[2019,2020,2021,2022]
sem=[1,2]

lista_DF=[]

for year in ano: 
    for semestre in sem:

        if (year == 2022 and semestre == 1) | (year == 2022 and semestre == 2):
            break

        caminho_inscricoes= f'../../../../csv originais/OFERTAS/{year}_ofertas_{semestre}.csv'


        df_bruto= pd.read_csv(caminho_inscricoes,
                              sep=';',
                              encoding='latin-1',
                              decimal=',')

        

        pd.set_option('display.max_columns', None)



        ordem_ofertas2022= [
        'Nome do Curso',
        'Cód. Do Grupo de Preferência',
        'Código do Curso',
        'Turno',

        ]

        ordem_ofertas= [
        'Nome do Curso',
        'Código do Grupo de Preferência',
        'Código do Curso',
        'Turno',

        ]

        vagas=[
        'Vagas autorizadas e-mec',
        'Vagas ofertadas FIES',
        'Vagas além da Oferta',
        'Vagas ocupadas'
        ]


        if year == 2022:
            df_sort= (df_bruto.sort_values(by=ordem_ofertas2022,
        ascending=[True,True,True,True])) 
        else:

            df_sort= (df_bruto.sort_values(by=ordem_ofertas,
        ascending=[True,True,True,True])) 

        if year == 2020 and semestre == 1:
            df_sort=df_sort.drop_duplicates(subset=df_sort.columns.to_list())





        df_agrupar_cursos= (df_sort.
        groupby(['Nome do Curso'],as_index=False).agg(

            Total_Vagas_EMEC=('Vagas autorizadas e-mec','sum'),

        ))

        df_agrupar_cursos['ano']=year

        df_agrupar_cursos['semestre']=semestre


   
        df_temporario= df_agrupar_cursos.copy()

        lista_DF.append(df_temporario)

df_concat= pd.concat(lista_DF)


desempate=['Nome do Curso','ano','semestre']

ordem=[True,True,True]

df_organizado= (df_concat
.sort_values(by=desempate,ascending=ordem))

df_organizado


df=(df_organizado
    .groupby(["ano","semestre"],as_index=False)
    .agg(

        VagasEMEC=("Total_Vagas_EMEC","sum")
        
    ))

df
# %%
salvar_caminho= '../../planilhas basico/Total_Vagas_EMEC_TUDO.csv'

df.to_csv(salvar_caminho,index=False)

# %%
