# %%
import pandas as pd
import os
import numpy as np

pd.set_option('display.max_columns', None)

# --- 1. CARREGAMENTO DAS TRÊS FONTES DE DADOS ---
caminho_ofertas = '../../../planilhas/limpo/modulo_3/limpar_e_padronizar_colunas/ofertas_limpo.csv'
caminho_inscricoes_geral = '../../../planilhas/limpo/modulo_3/limpar_e_padronizar_colunas/inscritos_limpo.csv'
caminho_candidatos_validado= "../../../planilhas/processado/modulo_3/funil_e_candidatos_unicos/candidatos_unicos_processado.csv"

dfo = pd.read_csv(caminho_ofertas)
dfi_geral = pd.read_csv(caminho_inscricoes_geral)
dfi_candidatos_unicos= pd.read_csv(caminho_candidatos_validado)





'''
APENAS nome das 10 areas gerais CINE
'''






# --- 2. CÁLCULO DE CADA ETAPA DO FUNIL ---
chave_agrupamento = ['ano', 'semestre', 'nome_cine_area_geral', "uf_local_oferta"]
ordem_sort = ['ano', 'semestre', 'id_estudante', 'situacao_fies']
subset_drop = ['ano', 'semestre', 'id_estudante']





# --- Etapas de Ofertas ---
df_vagas_ofertadas = dfo.groupby(chave_agrupamento, as_index=False)['vagas_fies'].sum()

df_vagas_ocupadas = dfo.groupby(chave_agrupamento, as_index=False)['vagas_ocupadas'].sum()



# --- Etapas de Inscrições (Gerais) ---
df_inscritos_geral = (dfi_geral
                      .groupby(chave_agrupamento, as_index=False)
                      .size()
                      .rename(columns={'size': 'Inscritos_Geral'}))





# --- Etapas de Candidatos Únicos (Gerais)


df_candidatos_unicos_geral = (dfi_candidatos_unicos
                              .groupby(chave_agrupamento, as_index=False)
                              .size()
                              .rename(columns={'size': 'Candidatos_Unicos_Geral'}))



# --- Etapas "CONCORRENDO por nota enem > nota corte grupo" de múltiplas fontes ---

# garantir que sao numeros media do enem e a nota de corte e padrao brasileiro
for df_temp in [dfi_geral, dfi_candidatos_unicos]:

    df_temp['media_enem'] = (pd
                                  .to_numeric(df_temp['media_enem']
                                              .astype(str)
                                              .str
                                              .replace(',', '.'), errors='coerce'))
    

    df_temp['nota_corte_gp'] = (pd
                                               .to_numeric(df_temp['nota_corte_gp']
                                                           .astype(str)
                                                           .str
                                                           .replace(',', '.'), errors='coerce'))




# --- Etapa: candidatos unicos com nt suficiente (Candidatos Únicos)-

FILTRO_TAL= dfi_candidatos_unicos['media_enem'] >= dfi_candidatos_unicos['nota_corte_gp']

df_base_candidatos_unicos_nota_suficiente = dfi_candidatos_unicos[FILTRO_TAL].copy()



df_candidatos_unicos_nota_suficiente = (df_base_candidatos_unicos_nota_suficiente
                        .groupby(chave_agrupamento, as_index=False)
                        .size()
                        .rename(columns={'size': 'candidatos_unicos_com_nota_suficiente'}))






# --- Etapa: Inscritos  com Nota Suficiente ---

FILTRO_TAL= dfi_geral['media_enem'] >= dfi_geral['nota_corte_gp']

df_inscritos_com_nota_base = dfi_geral[FILTRO_TAL].copy()

df_inscritos_com_nota = (df_inscritos_com_nota_base
                         .groupby(chave_agrupamento, as_index=False)
                         .size()
                         .rename(columns={'size': 'inscritos_com_nota_suficiente'}))




# --- 3. JUNÇÃO FINAL ---

df_final = df_vagas_ofertadas


dfs_para_juntar = [

#df_vagas_ofertadas, pq df_final o primeiro ja eh df vagas ofertas
df_inscritos_geral,
df_inscritos_com_nota,
df_candidatos_unicos_geral,
df_candidatos_unicos_nota_suficiente,
df_vagas_ocupadas,
]


for df_etapa in dfs_para_juntar:
    df_final = pd.merge(df_final, df_etapa, on=chave_agrupamento, how='outer')

df_final = df_final.fillna(0)

df_final

# %%
df_final.to_csv('../../../planilhas/processado/modulo_3/funil_e_candidatos_unicos/funil_por_uf.csv', index=False)

# %%
