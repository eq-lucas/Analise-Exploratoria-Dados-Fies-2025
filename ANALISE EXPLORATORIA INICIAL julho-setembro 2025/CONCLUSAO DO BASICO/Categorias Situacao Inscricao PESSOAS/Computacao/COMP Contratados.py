# %%
import pandas as pd

ano=[2019,2020,2021]
sem=[1,2]

lista_DF=[]

for year in ano: 
    for semestre in sem:

        caminho_inscricoes = f'../../../../csv originais/inscricoes CORRIGIDAS/fies_{semestre}_inscricao_{year}.csv'

        df_bruto= pd.read_csv(caminho_inscricoes)

        


        pd.set_option('display.max_columns', None)

        ordem_inscricoes= [

        'Situação Inscrição Fies',
        'Cod. do Grupo de preferência',
        'Código do curso',
        'Turno',

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

        df_sort_1= (df_bruto.sort_values(by=ordem_inscricoes,
        ascending=[True,True,True,True]))
        
        filtro= df_sort_1['Situação Inscrição Fies'] == 'CONTRATADA'
        df_sort_1= df_sort_1[filtro].copy()

        
        
        #se quiser especificar apenas para um unico candidato usar a pk e fazer a limpa,
        #mas antes organizar o sort com situacao inscricao pra cima e keep= first

        df_agrupar_cursos= (df_sort_1.
        groupby(['Nome do curso'],as_index=False).size())

        df_agrupar_cursos['ano']=year

        df_agrupar_cursos['semestre']=semestre


        filtro= (df_agrupar_cursos['Nome do curso'].isin(cursosComputacao))
        df_temporario= df_agrupar_cursos[filtro]

        lista_DF.append(df_temporario)

df_concat= pd.concat(lista_DF)


desempate=['Nome do curso','ano','semestre']

ordem=[True,True,True]

df_organizado= (df_concat
.sort_values(by=desempate,ascending=ordem))





df_final= pd.pivot(
data=df_organizado,
index=['ano','semestre'],
columns='Nome do curso',
values='size'
)
df_final.columns.name=None


df_final= df_final.reset_index().fillna(0)


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
    'CIÊNCIAS DA COMPUTAÇÃO'
]



df_salvar=df_limpo.drop(columns=colunas_erradas)

df_salvar
# %%
salvar_caminho= '../../planilhas basico/COMP CONTRATADOS.csv'

df_salvar.to_csv(salvar_caminho,index=False)

# %%
