# %%
import pandas as pd
import os
import numpy as np

pd.set_option('display.max_columns', None)

# --- 1. CARREGAMENTO DOS DADOS MESTRES ---
# Usando os arquivos que você já validou e organizou
caminho_inscricoes = 'planilhas ETL/COMP ETL inscritos peneira FIES P_FIES.csv'
pathof = 'planilhas ETL/COMP ETL ofertas.csv'

dfo = pd.read_csv(pathof)
dfi = pd.read_csv(caminho_inscricoes)

# --- 2. CÁLCULO DAS 7 ETAPAS DO FUNIL ---

Filtro_Periodo = ['Ano', 'Semestre']

# Etapa 1: Vagas Ofertadas (da fonte de Ofertas)
df1 = dfo.groupby(Filtro_Periodo, as_index=False)['Vagas ofertadas FIES'].sum()

# Etapa 7: Vagas Ocupadas (da fonte de Ofertas)
df7 = dfo.groupby(Filtro_Periodo, as_index=False)['Vagas ocupadas'].sum()

# Etapa 2: Inscritos (Total de inscrições)
df2 = dfi.groupby(Filtro_Periodo, as_index=False).size().rename(columns={'size': 'Inscritos'})

# Etapa 3: Candidatos Únicos (Sua lógica refinada)
# Ordena para garantir que a inscrição mais importante de um candidato (ex: CONTRATADO) venha primeiro
OrdemCorretaCandidatosUnicos = ['Ano', 'Semestre', 'ID do estudante', 'Situação Inscrição Fies']
dfi_ordenado = dfi.sort_values(by=OrdemCorretaCandidatosUnicos, ascending=[True, True, True, True])
df_candidatos_unicos_base = dfi_ordenado.drop_duplicates(subset=['Ano', 'Semestre', 'ID do estudante'], keep='first')
df3 = df_candidatos_unicos_base.groupby(Filtro_Periodo, as_index=False).size().rename(columns={'size': 'Candidatos Unicos'})


dfi[['Situação Inscrição Fies']].sort_values('Situação Inscrição Fies').groupby('Situação Inscrição Fies',as_index=False).count().head(50)
# %%
