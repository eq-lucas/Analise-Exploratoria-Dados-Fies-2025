# %%
import pandas as pd
import os
import numpy as np

pd.set_option('display.max_columns', None)

# --- 1. CARREGAMENTO DAS TRÊS FONTES DE DADOS ---
caminho_ofertas = '../../../planilhas ETL/GERAL ETL ofertas.csv'
caminho_inscricoes_geral = '../../../planilhas ETL/GERAL ETL inscritos.csv'
caminho_inscricoes_validado = '../../../planilhas ETL/GERAL ETL inscritos peneira FIES P_FIES.csv'
caminho_candidatos_validado= '../../../planilhas ETL/GERAL ETL candidatos peneira FIES P_FIES.csv'

dfo = pd.read_csv(caminho_ofertas)
dfi_geral = pd.read_csv(caminho_inscricoes_geral)
dfi_validado = pd.read_csv(caminho_inscricoes_validado)
dfc_validado= pd.read_csv(caminho_candidatos_validado)


# --- PADRONIZAÇÃO DAS COLUNAS-CHAVE ---
mapa_nomes_padrao = {
    'Nome do curso': 'Nome do Curso',
    'UF do Local de Oferta': 'UF do Local de Oferta'
}
dfo.rename(columns=mapa_nomes_padrao, inplace=True)
dfi_geral.rename(columns=mapa_nomes_padrao, inplace=True)
dfi_validado.rename(columns=mapa_nomes_padrao, inplace=True)
dfc_validado.rename(columns=mapa_nomes_padrao, inplace=True)










'''
APENAS DE COMPUTACAO LOGO NAO COMENTAR ESTAS LINHAS
'''
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

# 2. DEPOIS DE FILTRAR, PADRONIZA OS NOMES NA TABELA RESULTANTE
mapa_nomes_corretos = {
    'ANÃLISE E DESENVOLVIMENTO DE SISTEMAS': 'ANÁLISE E DESENVOLVIMENTO DE SISTEMAS',
    'CIÊNCIAS DA COMPUTAÇÃO': 'CIÊNCIA DA COMPUTAÇÃO',
    'SISTEMA DE INFORMAÇÃO': 'SISTEMAS DE INFORMAÇÃO',
    'ENGENHARIA DE COMPUTAÇÃO': 'ENGENHARIA DA COMPUTAÇÃO'
}
dfo['Nome do Curso'] = dfo['Nome do Curso'].replace(mapa_nomes_corretos)




























# --- 2. CÁLCULO DE CADA ETAPA DO FUNIL ---
chave_agrupamento = ['Ano', 'Semestre', 'Nome do Curso', "UF do Local de Oferta"]
ordem_sort = ['Ano', 'Semestre', 'ID do estudante', 'Situação Inscrição Fies']
subset_drop = ['Ano', 'Semestre', 'ID do estudante']





# --- Etapas de Ofertas ---
df_vagas_ofertadas = dfo.groupby(chave_agrupamento, as_index=False)['Vagas ofertadas FIES'].sum()
df_vagas_ocupadas = dfo.groupby(chave_agrupamento, as_index=False)['Vagas ocupadas'].sum()



# --- Etapas de Inscrições (Gerais) ---
df_inscritos_geral = (dfi_geral
                      .groupby(chave_agrupamento, as_index=False)
                      .size()
                      .rename(columns={'size': 'Inscritos_Geral'}))



FILTRO_TAL= dfi_geral['possivel_candidato'] == 'Eliminado'
df_eliminados_base_geral = dfi_geral[FILTRO_TAL].copy()


df_inscritos_eliminados = (df_eliminados_base_geral
                           .groupby(chave_agrupamento, as_index=False)
                           .size()
                           .rename(columns={'size': 'Inscritos_Eliminados'}))




# --- Etapas de Candidatos Únicos (Gerais)


df_candidatos_unicos_geral = (dfc_validado
                              .groupby(chave_agrupamento, as_index=False)
                              .size()
                              .rename(columns={'size': 'Candidatos_Unicos_Geral'}))



FILTRO_TAL= dfc_validado['possivel_candidato'] == 'Eliminado'

df_cand_eliminados_base_geral = dfc_validado[FILTRO_TAL].copy()


df_candidatos_unicos_eliminados = (df_cand_eliminados_base_geral
                                   .groupby(chave_agrupamento, as_index=False)
                                   .size()
                                   .rename(columns={'size': 'Candidatos_Unicos_Eliminados'}))



# --- Etapas de Inscrições (Validadas) ---

df_inscritos_validado_agg = (dfi_validado
                             .groupby(chave_agrupamento, as_index=False)
                             .size()
                             .rename(columns={'size': 'Inscritos_Validados'}))



df_candidatos_unicos_validado_agg = (dfc_validado
                                     .groupby(chave_agrupamento, as_index=False)
                                     .size()
                                     .rename(columns={'size': 'Candidatos_Unicos_Validados'}))



# --- Etapas "CONCORRENDO" de múltiplas fontes ---

# garantir que sao numeros media do enem e a nota de corte e padrao brasileiro
for df_temp in [dfi_geral, dfi_validado]:

    df_temp['Média nota Enem'] = (pd
                                  .to_numeric(df_temp['Média nota Enem']
                                              .astype(str)
                                              .str
                                              .replace(',', '.'), errors='coerce'))
    

    df_temp['Nota Corte Grupo Preferência'] = (pd
                                               .to_numeric(df_temp['Nota Corte Grupo Preferência']
                                                           .astype(str)
                                                           .str
                                                           .replace(',', '.'), errors='coerce'))




# --- Concorrendo Total (Candidatos Únicos)-

FILTRO_TAL= dfc_validado['Média nota Enem'] >= dfc_validado['Nota Corte Grupo Preferência']

df_concorrendo_base_geral = dfc_validado[FILTRO_TAL].copy()



df_concorrendo_total = (df_concorrendo_base_geral
                        .groupby(chave_agrupamento, as_index=False)
                        .size()
                        .rename(columns={'size': 'Concorrendo_Total'}))



# --- Concorrendo FIES/P-FIES (Candidatos Únicos Validados) 


FILTRO_TAL= dfc_validado['Média nota Enem'] >= dfc_validado['Nota Corte Grupo Preferência']

df_concorrendo_base_validado = dfc_validado[FILTRO_TAL].copy()


FILTRO_TAL= df_concorrendo_base_validado['possivel_candidato'] == 'FIES'

df_conc_fies_base = df_concorrendo_base_validado[FILTRO_TAL].copy()



df_concorrendo_fies = (df_conc_fies_base
                       .groupby(chave_agrupamento, as_index=False)
                       .size()
                       .rename(columns={'size': 'Concorrendo_FIES'}))



FILTRO_TAL= df_concorrendo_base_validado['possivel_candidato'] == 'P-FIES'

df_conc_pfies_base = df_concorrendo_base_validado[FILTRO_TAL].copy()


df_concorrendo_pfies = (df_conc_pfies_base
                        .groupby(chave_agrupamento, as_index=False)
                        .size()
                        .rename(columns={'size': 'Concorrendo_P_FIES'}))




# --- Etapa: Inscritos Validados com Nota Suficiente ---

FILTRO_TAL= dfi_geral['Média nota Enem'] >= dfi_geral['Nota Corte Grupo Preferência']

df_inscritos_com_nota_base = dfi_geral[FILTRO_TAL].copy()

df_inscritos_com_nota = (df_inscritos_com_nota_base
                         .groupby(chave_agrupamento, as_index=False)
                         .size()
                         .rename(columns={'size': 'Inscritos_Com_Nota_Suficiente'}))




# --- 3. JUNÇÃO FINAL ---

df_final = df_vagas_ofertadas


dfs_para_juntar = [

df_inscritos_geral,
df_inscritos_validado_agg,
df_inscritos_eliminados,
df_candidatos_unicos_geral,
df_candidatos_unicos_validado_agg,
df_candidatos_unicos_eliminados,
df_inscritos_com_nota,
df_concorrendo_total,
df_concorrendo_fies,
df_concorrendo_pfies,
df_vagas_ocupadas

]


for df_etapa in dfs_para_juntar:
    df_final = pd.merge(df_final, df_etapa, on=chave_agrupamento, how='outer')

df_final = df_final.fillna(0)

df_final

# %%
df_final.to_csv('../../../planilhas/GERAL DF_funil 12 etapas.csv', index=False)

# %%
