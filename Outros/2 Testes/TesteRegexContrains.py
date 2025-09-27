# %%
import pandas as pd

ano=[2019,2020,2021]
sem=[1,2]

lista_DF=[]

for year in ano: 
    for semestre in sem:

        caminho_inscricoes= f'dataset/inscricoes CORRIGIDAS/fies_{semestre}_inscricao_{year}.csv'

        df_bruto= pd.read_csv(caminho_inscricoes)


        pd.set_option('display.max_columns', None)

        ordem_inscricoes= [

        'Cod. do Grupo de preferência',
        'Código do curso',
        'Turno',
        'Situação Inscrição Fies'

        ]

        df_sort= (df_bruto.sort_values(by=ordem_inscricoes,
        ascending=[True,True,True,True]))

        #se quiser especificar apenas para um unico candidato usar a pk e fazer a limpa,
        #mas antes organizar o sort com situacao inscricao pra cima e keep= first

        df_agrupar_cursos= df_sort.groupby('Nome do curso')


















# %% 
import pandas as pd

teste= 'dataset/inscricoes CORRIGIDAS/fies_1_inscricao_2019.csv'

pd.set_option('display.max_columns', None)


teste=pd.read_csv(teste)



ordem_inscricoes= [

'Cod. do Grupo de preferência',
'Código do curso',
'Turno',
'Situação Inscrição Fies'

]

teste_sort= (teste.sort_values(by=ordem_inscricoes,
ascending=[True,True,True,True]))

#se quiser especificar apenas para um unico candidato usar a pk e fazer a limpa,
#mas antes organizar o sort com situacao inscricao pra cima e keep= first

teste_agrupar_cursos= (teste_sort.
groupby(['Nome do curso'],as_index=False).size())

teste_agrupar_cursos

computacao= 'COMPUTAÇÃO|ENGENHARIA DE SOFTWARE|SISTEMA|DADO|REDE'

filtro= (teste_agrupar_cursos['Nome do curso'].
      str.contains(computacao,regex=True ))

# %%
teste_agrupar_cursos[filtro].sort_values('size',ascending=False)

# %%
cursosComputacao=[
    
'ANÃLISE E DESENVOLVIMENTO DE SISTEMAS',
'ANÁLISE E DESENVOLVIMENTO DE SISTEMAS',
'CIÊNCIA DA COMPUTAÇÃO',

'SISTEMAS DE INFORMAÇÃO',
'SISTEMA DE INFORMAÇÃO',

'REDES DE COMPUTADORES',


'ENGENHARIA DE COMPUTAÇÃO',
'ENGENHARIA DA COMPUTAÇÃO',

'ENGENHARIA DE SOFTWARE'

]