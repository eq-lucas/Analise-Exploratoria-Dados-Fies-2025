# %%
import pandas as pd

ano=[2019,2020,2021,2022]
sem=[1,2]

lista_DF=[]

for year in ano: 
    for semestre in sem:

        if (year == 2022 and semestre == 1) | (year == 2022 and semestre == 2):
            break

        caminho_inscricoes= f'../../../../../csv originais/OFERTAS/{year}_ofertas_{semestre}.csv'

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


        cursosComputacao=[
            
        'ANÃLISE E DESENVOLVIMENTO DE SISTEMAS',
        'ANÁLISE E DESENVOLVIMENTO DE SISTEMAS',
        'CIÊNCIA DA COMPUTAÇÃO',
        'CIÊNCIAS DA COMPUTAÇÃO',

        'SISTEMAS DE INFORMAÇÃO',
        'SISTEMA DE INFORMAÇÃO',

        'REDES DE COMPUTADORES',


        'ENGENHARIA DE COMPUTAÇÃO',
        'ENGENHARIA DA COMPUTAÇÃO',

        'ENGENHARIA DE SOFTWARE'

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

            Total_Vagas_Ofertadas=('Vagas ofertadas FIES','sum'),

        ))

        df_agrupar_cursos['ano']=year

        df_agrupar_cursos['semestre']=semestre


        filtro= (df_agrupar_cursos['Nome do Curso'].isin(cursosComputacao))
        df_temporario= df_agrupar_cursos[filtro]

        lista_DF.append(df_temporario)

df_concat= pd.concat(lista_DF)


desempate=['Nome do Curso','ano','semestre']

ordem=[True,True,True]

df_organizado= (df_concat
.sort_values(by=desempate,ascending=ordem))


df_final = pd.pivot(
    data=df_organizado,
    index=['ano', 'semestre'],
    columns='Nome do Curso',
    values='Total_Vagas_Ofertadas'
)





df_final.columns.name=None

df_final= df_final.reset_index().fillna(0)

df_final


def AjusarnomeErrado(x: pd.Series):
        
    x['ANÁLISE E DESENVOLVIMENTO DE SISTEMAS']= x['ANÃLISE E DESENVOLVIMENTO DE SISTEMAS']+x['ANÁLISE E DESENVOLVIMENTO DE SISTEMAS']
    x['ENGENHARIA DA COMPUTAÇÃO']=  x['ENGENHARIA DA COMPUTAÇÃO']+x['ENGENHARIA DE COMPUTAÇÃO']
    x['SISTEMAS DE INFORMAÇÃO']= x['SISTEMA DE INFORMAÇÃO']+ x['SISTEMAS DE INFORMAÇÃO']
    x['CIÊNCIA DA COMPUTAÇÃO']= x['CIÊNCIAS DA COMPUTAÇÃO'] + x['CIÊNCIA DA COMPUTAÇÃO']
    return x

df_limpo= df_final.apply(AjusarnomeErrado,axis=1)


colunas_erradas=[

    'SISTEMA DE INFORMAÇÃO',
    'ENGENHARIA DE COMPUTAÇÃO',
    'ANÃLISE E DESENVOLVIMENTO DE SISTEMAS',
    'CIÊNCIAS DA COMPUTAÇÃO',
]



df_salvar=df_limpo.drop(columns=colunas_erradas)
df_salvar
# %%
salvar_caminho= '../../../planilhas basico/Total_Vagas_OfertadasComp.csv'

df_salvar.to_csv(salvar_caminho,index=False)

# %%
