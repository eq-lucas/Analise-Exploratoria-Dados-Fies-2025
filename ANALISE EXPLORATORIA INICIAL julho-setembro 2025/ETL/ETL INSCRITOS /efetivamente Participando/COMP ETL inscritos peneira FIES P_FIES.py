# %%

import pandas as pd
import os

pd.set_option('display.max_columns', None)


ano = [2019, 2020, 2021]
sem = [1, 2]



caminho_inscricoes = '../../../../planilhas ETL/GERAL ETL inscritos peneira FIES P_FIES.csv'

df_bruto = pd.read_csv(caminho_inscricoes)


#Filtra o DataFrame para manter apenas os cursos de computação
cursosComputacao = [

    'ANÁLISE E DESENVOLVIMENTO DE SISTEMAS',
    'CIÊNCIA DA COMPUTAÇÃO',
    'SISTEMAS DE INFORMAÇÃO',
    'REDES DE COMPUTADORES',
    'ENGENHARIA DA COMPUTAÇÃO',
    'ENGENHARIA DE SOFTWARE'
]

filtro_computacao = df_bruto['Nome do curso'].isin(cursosComputacao)

df_temporario = df_bruto[filtro_computacao]



# Define a ordem de classificação, com UF em primeiro, como solicitado
desempate = [
'Ano',
'Semestre',
'UF do Local de Oferta',
'Cod. do Grupo de preferência',
'Código do curso',
'Turno'
]

df_organizado = df_temporario.sort_values(by=desempate, ascending=True)

df_organizado

# %%
df_organizado.to_csv('../../../../planilhas ETL/COMP ETL inscritos peneira FIES P_FIES.csv',index=False)

# %%