# %%
import pandas as pd
import os

pathins = '../../../../planilhas ETL/GERAL ETL inscritos.csv'
df = pd.read_csv(pathins)

filtro_elegiveis = (df['possivel_candidato'] == 'FIES') | (df['possivel_candidato'] == 'P-FIES')
df = df[filtro_elegiveis].copy()

pathof = '../../../../planilhas ETL/GERAL ETL ofertas.csv'
dfo = pd.read_csv(pathof)

# Chaves de junção para cada DataFrame
colunas_ofertas = ['Ano', 'Semestre', 'Código do Grupo de Preferência', 'Código do Curso', 'Turno']
colunas_inscricoes = ['Ano', 'Semestre', 'Cod. do Grupo de preferência', 'Código do curso', 'Turno']

# Realiza o merge
df_verificar = df.merge(
    right=dfo,
    right_on=colunas_ofertas,
    left_on=colunas_inscricoes,
    how='inner',
    suffixes=('', '_oferta') # <-- A SOLUÇÃO ESTÁ AQUI
)  

# Cria o filtro para encontrar inconsistências
filtro_verificar = (df_verificar['possivel_candidato'] == 'P-FIES') & ((df_verificar['Participa do P-FIES'] == 'NAO') | (df_verificar['Participa do P-FIES'].isna()))

# APLICA O FILTRO CORRETO (filtro_verificar)
df_somente_quem_pertence_fies_ou_pfies = df_verificar[~filtro_verificar].copy()



# Exibe o resultado
df_final=df_somente_quem_pertence_fies_ou_pfies[df.columns.to_list()]

df_final

# %%
df_final.to_csv('../../../../planilhas ETL/GERAL ETL inscritos peneira FIES P_FIES.csv',index=False)


# %%
