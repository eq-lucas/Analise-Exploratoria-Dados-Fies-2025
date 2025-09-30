# %%

import pandas as pd
import os

pd.set_option('display.max_columns', None)


path= '../../../../planilhas ETL/GERAL ETL inscritos peneira FIES P_FIES.csv'

df= pd.read_csv(path,decimal=',',low_memory=False)

pd.set_option('display.max_columns', None)



ordem_de_prioridade = [
    'CONTRATADA',
    'INSCRIÇÃO POSTERGADA',
    'PRÉ-SELECIONADO',
    'LISTA DE ESPERA',
    'OPÇÃO NÃO CONTRATADA',
    'NÃO CONTRATADO',
    'REJEITADA PELA CPSA',
    'PARTICIPACAO CANCELADA PELO CANDIDATO'
]

ordem_possivel_contrato = [
    'CONTRATADA',
    'INSCRIÇÃO POSTERGADA',
    'PRÉ-SELECIONADO',
    'LISTA DE ESPERA',
]


chave_agrupamento = [

'Ano',
'Semestre',
'Nome do curso',
"UF do Local de Oferta"

]


ordem_sort = [

'Ano',
'Semestre',
'ID do estudante',
'Opções de cursos da inscrição',
'Situação Inscrição Fies'

]

ordem_sort_sem_opcao_em_ultimo = [

'Ano',
'Semestre',
'ID do estudante',
'Situação Inscrição Fies',

'Opções de cursos da inscrição',

]


ascending_sort=[True,True,True,False,True]

ascending_ordem_sort_sem_opcao_em_ultimo=[True,True,True,True,False]


subset_drop = ['Ano', 'Semestre', 'ID do estudante']


df_semContratados=df.sort_values(by=ordem_sort)


# converter a coluna no DataFrame existente ('df_semContratados').
df_semContratados['Situação Inscrição Fies'] = pd.Categorical(
    df_semContratados['Situação Inscrição Fies'],
    categories=ordem_de_prioridade,
    ordered=True
)

#ordene o DataFrame que agora tem a coluna com a prioridade correta.
df_situacaoInscricaoOrdenadaPorPrioridades = (df_semContratados
                                              .sort_values(by=ordem_sort,
                                                           ascending=True))



df_candidatos_unicos=df_situacaoInscricaoOrdenadaPorPrioridades.drop_duplicates(subset=subset_drop,keep='first')




# Define a ordem de classificação, com UF em primeiro, como solicitado
desempate = [

'Ano',
'Semestre',
'UF do Local de Oferta',
'Cod. do Grupo de preferência',
'Código do curso',
'Turno'
]

df_final = df_candidatos_unicos.sort_values(by=desempate, ascending=True)

df_final
# %%
df_final.to_csv('../../../../planilhas ETL/GERAL ETL candidatos peneira FIES P_FIES.csv',index=False)

# %%
