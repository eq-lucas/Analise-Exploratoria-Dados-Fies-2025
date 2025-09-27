# %%
import pandas as pd

ano=[2019,2020,2021,2022]
sem=[1,2]

lista_DF=[]

for year in ano: 
    for semestre in sem:

        if (year == 2022 and semestre == 1) | (year == 2022 and semestre == 2):
            break

        caminho_inscricoes= f'../../../csv originais/OFERTAS/{year}_ofertas_{semestre}.csv'

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



        if year == 2022:
            df_sort= (df_bruto.sort_values(by=ordem_ofertas2022,
        ascending=[True,True,True,True])) 
        else:

            df_sort= (df_bruto.sort_values(by=ordem_ofertas,
        ascending=[True,True,True,True])) 

        if year == 2020 and semestre == 1:
            df_sort=df_sort.drop_duplicates(subset=df_sort.columns.to_list())




        df_temporario=df_sort


        lista_DF.append(df_temporario)

df_concat= pd.concat(lista_DF)




desempate=['UF do Local de Oferta','Ano','Semestre']

ordem=[True,True,True]

df_organizado= (df_concat
.sort_values(by=desempate,ascending=ordem))


colunasunmd= ['Unnamed: 58', 'Unnamed: 59', 'Unnamed: 60']
 
#df_organizado.dropna(how='any',subset=colunasunmd)


df=df_organizado.drop(columns=colunasunmd)


df
# %%
salvar_caminho= '../../../planilhas ETL/GERAL ETL ofertas.csv'

df.to_csv(salvar_caminho,index=False)

# %%
