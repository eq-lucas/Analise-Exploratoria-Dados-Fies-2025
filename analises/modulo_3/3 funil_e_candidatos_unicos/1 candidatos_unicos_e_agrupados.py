# %% 

import pandas as pd

path= '../../../planilhas/limpo/modulo_3/limpar_e_padronizar_colunas/inscritos_limpo.csv'

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
'ano',
'semestre',
'nome_cine_area_geral',
"uf_local_oferta",
]


ordem_sort = [

'ano',
'semestre',
'id_estudante',
'opcao_curso',
'situacao_fies'

]

ordem_sort_opcao_em_ultimo = [

'ano',
'semestre',
'id_estudante',
'situacao_fies',
'opcao_curso',

]

subset_drop = [
    
'ano',
'semestre',
'id_estudante'

]




ascending_sort=[True,True,True,False,True]

ascending_ordem_sort_opcao_em_ultimo=[True,True,True,True,False]


df_convertido= df

# converter a coluna no DataFrame existente ('df_convertido').
#para usar a ordem que eu customizei
df_convertido['situacao_fies'] = pd.Categorical(
    df['situacao_fies'],
    categories=ordem_de_prioridade,
    ordered=True
)

#ordene o DataFrame por ano e desempate semstre, com desmpate ...
#ate que qnd odesempate for situacao_fies:
#sera por tal ordem, com a prioridade correta.
df_situacaoInscricaoOrdenadaPorPrioridades = (df_convertido
                                            .sort_values(
                                            by=ordem_sort,
                                            ascending=True))


colunacandidatos={
    'id_estudante': 'qtde_candidato_unico_por_area_cine_e_regiao'
}


df_candidatos_unicos=(df_situacaoInscricaoOrdenadaPorPrioridades
                      .drop_duplicates(subset=subset_drop,keep='first'))

df_candidatos_unicos_agrupados= (df_candidatos_unicos
                                   .groupby(chave_agrupamento,as_index=False)['id_estudante']
                                   .count().
                                   sort_values('id_estudante',ascending=False)
                                   .rename(columns=colunacandidatos))

df_candidatos_unicos_agrupados= (df_candidatos_unicos_agrupados
                       .sort_values(['ano', 'semestre','uf_local_oferta']))

qtde= df_candidatos_unicos_agrupados['qtde_candidato_unico_por_area_cine_e_regiao'].sum()

display(qtde) #type: ignore
display(df_candidatos_unicos_agrupados.groupby('nome_cine_area_geral')[['nome_cine_area_geral']].count()) #type: ignore
display(df_candidatos_unicos_agrupados) #type: ignore
print("esta faltnado apenas 1 dos 11, que eh o de programas genericos e disciplinas interdisciplinares!")

df_candidatos_unicos.to_csv('../../../planilhas/processado/modulo_3/funil_e_candidatos_unicos/candidatos_unicos_processado.csv',index=False)
df_candidatos_unicos_agrupados.to_csv('../../../planilhas/processado/modulo_3/funil_e_candidatos_unicos/candidatos_unicos_agrupado_por_cine_e_uf_processado.csv',index=False)

# %%
import pandas as pd

path = '../../../../../../planilhas/processado/modulo_3/funil_e_candidatos_unicos/candidatos_unicos_processado.csv'

df=pd.read_csv(path)

df.head(50)

# %%
