# %% 

import pandas as pd

path= '../../../planilhas ETL/GERAL ETL inscritos.csv'

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

#1 etapa ordenar por ordem sort e filtrar quem tem contratada

#df1= df.sort_values(by=ordem_sort)
#
#filtro = (df1['Situação Inscrição Fies'] == 'CONTRATADA') | ( df1['Situação Inscrição Fies'] == 'INSCRIÇÃO POSTERGADA' )
#
#df_contratados= df1[filtro]['ID do estudante'].copy()
#
#filtro_quemEhContratado= df1['ID do estudante'].isin(df_contratados)
#
#df_semContratados= df1[~filtro_quemEhContratado]
#
#df_semContratados[ordem_sort].head(50)

# nao faz sentido, pois no final ele estara em primeri os com contratados ou postergados

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

# na ofaz sentido dropar , se quiser contar os candidatos unicos logo nao faz snetido dropar!
#df_situacaoInscricaoOrdenadaPorPrioridades= df_situacaoInscricaoOrdenadaPorPrioridades.dropna(subset='Situação Inscrição Fies')

#valor={'Situação Inscrição Fies':'zzz'}  #zzz pois eh para ficar la em baixo na ordenacao

#df_situacaoInscricaoOrdenadaPorPrioridades= (df_situacaoInscricaoOrdenadaPorPrioridades
#                                             .fillna(valor))


#df_Inscritos_por_semestre_regiao= (df_situacaoInscricaoOrdenadaPorPrioridades
#                                   .groupby(chave_agrupamento,as_index=False)['ID do estudante']
#                                   .count().
#                                   sort_values('ID do estudante',ascending=False))
# 
#colunaIDEstudante={
#    'ID do estudante': 'Inscritos_por_regiao_mas_sem_as_inscricoes_rejeitadas'
#}
#
#df_Inscritos_por_semestre_regiao.rename(columns=colunaIDEstudante)





colunacandidatos={
    'ID do estudante': 'candidatos_unicos_curso_regiao'
}


df_candidatos_unicos=df_situacaoInscricaoOrdenadaPorPrioridades.drop_duplicates(subset=subset_drop,keep='first')

df_candidatos_unicos= (df_candidatos_unicos
                                   .groupby(chave_agrupamento,as_index=False)['ID do estudante']
                                   .count().
                                   sort_values('ID do estudante',ascending=False)
                                   .rename(columns=colunacandidatos))

df_candidatos_unicos= (df_candidatos_unicos
                       .sort_values(['Ano', 'Semestre','UF do Local de Oferta']))


df_candidatos_unicos.to_csv('../../../planilhas/DF candidatos unicos regiao curso.csv',index=False)

# %%
import pandas as pd

path = '../../../planilhas/DF candidatos unicos regiao curso.csv'

df=pd.read_csv(path)

df.head(50)

# %%
