# %%

import pandas as pd
import os

pd.set_option('display.max_columns', None)



caminho_inscricoes = '../../../../planilhas ETL/GERAL ETL inscritos peneira FIES P_FIES.csv'

df_organizado= pd.read_csv(caminho_inscricoes)


#Define a ordem de classificação CANDIDATOS UNICOS CORRETAMENTE
OrdemCorretaCandidatosUnicos = [
'ID do estudante',
'Situação Inscrição Fies'
] 
df_organizado = df_organizado.sort_values(by=OrdemCorretaCandidatosUnicos, ascending=True)
#descomente se quiser gerar apeans os candidatos unicos
df_organizado = df_organizado.drop_duplicates(subset=['Ano','Semestre','ID do estudante'],keep='first')




# Define a ordem de classificação, com UF em primeiro, como solicitado
desempate = [

'Ano',
'Semestre',
'UF do Local de Oferta',
'Cod. do Grupo de preferência',
'Código do curso',
'Turno'
]

df_final = df_organizado.sort_values(by=desempate, ascending=True)

df_final
# %%
df_final.to_csv('../../../../planilhas ETL/GERAL ETL candidatos peneira FIES P_FIES.csv',index=False)

# %%
