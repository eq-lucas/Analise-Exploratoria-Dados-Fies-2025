# %%
import pandas as pd

ano=[2019,2020,2021]
sem=[1,2]

lista_DF=[]

for year in ano: 
    for semestre in sem:

        caminho_inscricoes = f'../../../csv originais/inscricoes CORRIGIDAS/fies_{semestre}_inscricao_{year}.csv'

        ins_df= pd.read_csv(caminho_inscricoes)


        pd.set_option('display.max_columns', None)




        #Define a ordem de classificação CANDIDATOS UNICOS CORRETAMENTE
        OrdemCorretaCandidatosUnicos = [
        'ID do estudante',
        'Situação Inscrição Fies'
        ] 

        ins_df_sort=(ins_df.sort_values(by=OrdemCorretaCandidatosUnicos, ascending=True)
                     .drop_duplicates(subset='ID do estudante',keep='first'))
        



        ordem_inscricoes= [

        'Situação Inscrição Fies',
        'Cod. do Grupo de preferência',
        'Código do curso',
        'Turno'

        ]

        ins_df_sort= (ins_df_sort.sort_values(by=ordem_inscricoes,ascending=[True,True,True,True]))



        opcoes=(ins_df_sort.groupby(by='Situação Inscrição Fies',as_index=False)
                .agg(quantidade=('Situação Inscrição Fies','count')))

        opcoes['ano']=year
        opcoes['semestre']=semestre
        lista_DF.append(opcoes)

df_bruto= pd.concat(lista_DF)


# O seu df_bruto, gerado pelo loop, está correto.
# A mudança é apenas na chamada do pivot_table.


df_final = df_bruto.pivot_table(
    index=['ano', 'semestre'],
    columns='Situação Inscrição Fies',
    values='quantidade',  # <-- A LINHA QUE RESOLVE TUDO
    fill_value=0
).astype(int) # se passar com dict, sera nome da coluna e dps o tipo com aspas tb

# Agora, o reset_index() e a limpeza do nome funcionarão como você espera
df_final = df_final.reset_index() # ano e semestre viraram index por conta do index no pivot
df_final.columns.name = None # pois quando pivotamos a coluna situacao inscricao fies vira um name pras colunas ' contratada etc'



df= df_final

df.columns.tolist()

colunas= [

 'CONTRATADA',
 'INSCRIÇÃO POSTERGADA',
 'LISTA DE ESPERA',
 'NÃO CONTRATADO',
 'OPÇÃO NÃO CONTRATADA',
 'PARTICIPACAO CANCELADA PELO CANDIDATO',
 'PRÉ-SELECIONADO',
 'REJEITADA PELA CPSA'
 ]

def total(x:pd.Series):
    return x.sum()


Linha= pd.DataFrame({'total':df.apply(total)})


Linha= Linha.pivot_table(

    
    columns=Linha.index,
    values='total'
)


Linha= Linha.astype(int)



df=pd.concat([df,Linha])




import numpy as np
c=df


colunas = [
    'CONTRATADA',
    'INSCRIÇÃO POSTERGADA',
    'LISTA DE ESPERA',
    'NÃO CONTRATADO',
    'OPÇÃO NÃO CONTRATADA',
    'PARTICIPACAO CANCELADA PELO CANDIDATO',
    'PRÉ-SELECIONADO',
    'REJEITADA PELA CPSA'
]

c['TOTAL CANDIDATOS']= c[colunas].apply(sum,axis=1)


a= '../planilhas basico/inscricoesDuplicatas.csv'

a=pd.read_csv(a)


valores= a['pk'].to_list()


valores.append(np.nan)


c['TOTAL INSCRITOS - PK']= valores



c.loc['total',['ano','semestre','TOTAL CANDIDATOS']]= np.nan

c.loc['total','TOTAL INSCRITOS - PK']= c['TOTAL INSCRITOS - PK'].sum()


c
# %%
c.to_csv('../planilhas basico/Categorias Situacao CANDIDATOS GERAL.csv')


# %%
z=pd.read_csv('../planilhas basico/situacaoCANDIDATOSTotalTUDO.csv',index_col='Unnamed: 0')
z
# %%