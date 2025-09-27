# %%
import pandas as pd
import os
import numpy as np

pd.set_option('display.max_columns', None)

# --- 1. CARREGAMENTO DAS TRÊS FONTES DE DADOS ---
caminho_ofertas = '../../../planilhas ETL/COMP ETL ofertas.csv'
caminho_inscricoes_geral = '../../../planilhas ETL/GERAL ETL inscritos.csv'
caminho_inscricoes_validado = '../../../planilhas ETL/GERAL ETL inscritos peneira FIES P_FIES.csv'

dfo = pd.read_csv(caminho_ofertas)
dfi_geral = pd.read_csv(caminho_inscricoes_geral)
dfi_validado = pd.read_csv(caminho_inscricoes_validado)


# --- PADRONIZAÇÃO DAS COLUNAS-CHAVE ---
mapa_nomes_padrao = {
    'Nome do curso': 'Nome do Curso',
    'UF do Local de Oferta': 'UF do Local de Oferta'
}
dfo.rename(columns=mapa_nomes_padrao, inplace=True)
dfi_geral.rename(columns=mapa_nomes_padrao, inplace=True)
dfi_validado.rename(columns=mapa_nomes_padrao, inplace=True)






#PARTE PARA DEIXAR APENAS OS DE COMPUTACAO
cursosComputacao = [
    'ANÁLISE E DESENVOLVIMENTO DE SISTEMAS',
    'CIÊNCIA DA COMPUTAÇÃO',
    'SISTEMAS DE INFORMAÇÃO',
    'REDES DE COMPUTADORES',
    'ENGENHARIA DA COMPUTAÇÃO',
    'ENGENHARIA DE SOFTWARE'
]

filtro_computacao = dfi_validado['Nome do Curso'].isin(cursosComputacao)
dfi_validado = dfi_validado[filtro_computacao].copy()

filtro_computacao2 = dfi_geral['Nome do Curso'].isin(cursosComputacao)
dfi_geral = dfi_geral[filtro_computacao2].copy()






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
df_eliminados_base_geral = dfi_geral[FILTRO_TAL]


df_inscritos_eliminados = (df_eliminados_base_geral
                           .groupby(chave_agrupamento, as_index=False)
                           .size()
                           .rename(columns={'size': 'Inscritos_Eliminados'}))




# --- Etapas de Candidatos Únicos (Gerais)
dfi_geral_ordenado = dfi_geral.sort_values(by=ordem_sort, ascending=True)


df_cand_unicos_base_geral = dfi_geral_ordenado.drop_duplicates(subset=subset_drop, keep='first')


df_candidatos_unicos_geral = (df_cand_unicos_base_geral
                              .groupby(chave_agrupamento, as_index=False)
                              .size()
                              .rename(columns={'size': 'Candidatos_Unicos_Geral'}))



FILTRO_TAL= df_cand_unicos_base_geral['possivel_candidato'] == 'Eliminado'

df_cand_eliminados_base_geral = df_cand_unicos_base_geral[FILTRO_TAL]


df_candidatos_unicos_eliminados = (df_cand_eliminados_base_geral
                                   .groupby(chave_agrupamento, as_index=False)
                                   .size()
                                   .rename(columns={'size': 'Candidatos_Unicos_Eliminados'}))



# --- Etapas de Inscrições (Validadas) ---

df_inscritos_validado_agg = (dfi_validado
                             .groupby(chave_agrupamento, as_index=False)
                             .size()
                             .rename(columns={'size': 'Inscritos_Validados'}))


dfi_validado_ordenado = dfi_validado.sort_values(by=ordem_sort, ascending=True)

df_cand_unicos_base_validado = dfi_validado_ordenado.drop_duplicates(subset=subset_drop, keep='first')



df_candidatos_unicos_validado_agg = (df_cand_unicos_base_validado
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

FILTRO_TAL= dfi_geral['Média nota Enem'] >= dfi_geral['Nota Corte Grupo Preferência']

df_concorrendo_base_geral = dfi_geral[FILTRO_TAL]


df_conc_geral_ordenado = df_concorrendo_base_geral.sort_values(by=ordem_sort, ascending=True)

df_conc_unicos_base_geral = df_conc_geral_ordenado.drop_duplicates(subset=subset_drop, keep='first')



df_concorrendo_total = (df_conc_unicos_base_geral
                        .groupby(chave_agrupamento, as_index=False)
                        .size()
                        .rename(columns={'size': 'Concorrendo_Total'}))



# --- Concorrendo FIES/P-FIES (Candidatos Únicos Validados) 


FILTRO_TAL= dfi_validado['Média nota Enem'] >= dfi_validado['Nota Corte Grupo Preferência']

df_concorrendo_base_validado = dfi_validado[FILTRO_TAL]

df_conc_validado_ordenado = df_concorrendo_base_validado.sort_values(by=ordem_sort, ascending=True)

df_conc_unicos_base_validado = df_conc_validado_ordenado.drop_duplicates(subset=subset_drop, keep='first')



FILTRO_TAL= df_conc_unicos_base_validado['possivel_candidato'] == 'FIES'

df_conc_fies_base = df_conc_unicos_base_validado[FILTRO_TAL]



df_concorrendo_fies = (df_conc_fies_base
                       .groupby(chave_agrupamento, as_index=False)
                       .size()
                       .rename(columns={'size': 'Concorrendo_FIES'}))



FILTRO_TAL= df_conc_unicos_base_validado['possivel_candidato'] == 'P-FIES'

df_conc_pfies_base = df_conc_unicos_base_validado[FILTRO_TAL]


df_concorrendo_pfies = (df_conc_pfies_base
                        .groupby(chave_agrupamento, as_index=False)
                        .size()
                        .rename(columns={'size': 'Concorrendo_P_FIES'}))




# --- Etapa: Inscritos Validados com Nota Suficiente ---

FILTRO_TAL= dfi_geral['Média nota Enem'] >= dfi_geral['Nota Corte Grupo Preferência']

df_inscritos_com_nota_base = dfi_geral[FILTRO_TAL]

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
df_final.to_csv('../../../planilhas/COMP DF_funil 11 etapas.csv', index=False)
# %%