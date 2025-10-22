# %%
import pandas as pd
import os

pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)

# --- 1. CAMINHOS ---

# Caminho de LEITURA (o arquivo que você quer renomear)
path_leitura_ofertas = '../../../planilhas/limpo/modulo_2/ajustar_nan_cine_ofertas/ofertas_agrupado_limpo_CORRIGIDO.csv'

# Caminho de SAÍDA (onde salvar o arquivo com nomes novos)
path_salvar_ofertas = '../../../planilhas/limpo/modulo_3/limpar_e_padronizar_colunas/ofertas_limpo.csv'

mapa_nomes_curto = {
    'ano_ofertas': 'ano',
    'semestre_ofertas': 'semestre',
    'nome_mantenedora_ofertas': 'nome_mantenedora',
    'codigo_e_mec_mantenedora_ofertas': 'codigo_mec_mantenedora',
    'cnpj_mantenedora_ofertas': 'cnpj_mantenedora',
    'nome_ies_ofertas': 'nome_ies',
    'codigo_e_mec_ies_ofertas': 'codigo_mec_ies',
    'organizacao_academica_ies_ofertas': 'organizacao_academica_ies',
    'uf_ies_ofertas': 'uf_ies',
    'municipio_ies_ofertas': 'municipio_ies',
    'nome_local_oferta_ofertas': 'nome_local_oferta',
    'codigo_local_oferta_ofertas': 'codigo_local_oferta',
    'municipio_local_oferta_ofertas': 'municipio_local_oferta',
    'uf_local_oferta_ofertas': 'uf_local_oferta',
    'nome_microrregiao_ofertas': 'nome_microrregiao',
    'codigo_microrregiao_ofertas': 'codigo_microrregiao',
    'codigo_mesorregiao_ofertas': 'codigo_mesorregiao',
    'nome_mesorregiao_ofertas': 'nome_mesorregiao',
    'area_conhecimento_ofertas': 'area_conhecimento',
    'subarea_conhecimento_ofertas': 'subarea_conhecimento',
    'codigo_grupo_preferencia_ofertas': 'codigo_grupo_preferencia',
    'nota_corte_grupo_preferencia_ofertas': 'nota_corte_gp',
    'codigo_curso_ofertas': 'codigo_curso',
    'nome_curso_ofertas': 'nome_curso',
    'turno_ofertas': 'turno',
    'grau_ofertas': 'grau',
    'conceito_ofertas': 'conceito_curso',
    'vagas_autorizadas_e_mec_ofertas': 'vagas_autorizadas_mec',
    'vagas_ofertadas_fies_ofertas': 'vagas_fies',
    'vagas_alem_da_oferta_ofertas': 'vagas_alem_oferta',
    'vagas_ocupadas_ofertas': 'vagas_ocupadas',
    'participa_p_fies_ofertas': 'participa_p_fies',
    'vagas_ofertadas_p_fies_ofertas': 'vagas_p_fies',
    
    # Agentes Financeiros
    'banco_nordeste_brasil_004_ofertas': 'ag_banco_nordeste_004',
    'itau_unibanco_pravaler_341_ofertas': 'ag_itau_pravaler_341',
    'bv_financeira_pravaler_455_ofertas': 'ag_bv_pravaler_455',
    'banco_andbank_pravaler_65_ofertas': 'ag_andbank_pravaler_65',
    'banco_amazonia_sa_003_ofertas': 'ag_banco_amazonia_003',
    
    # Valores Brutos
    'valor_bruto_curso_ofertas': 'valor_bruto_curso',
    'semestre_1_bruto_ofertas': 'sem_1_bruto',
    'semestre_2_bruto_ofertas': 'sem_2_bruto',
    'semestre_3_bruto_ofertas': 'sem_3_bruto',
    'semestre_4_bruto_ofertas': 'sem_4_bruto',
    'semestre_5_bruto_ofertas': 'sem_5_bruto',
    'semestre_6_bruto_ofertas': 'sem_6_bruto',
    'semestre_7_bruto_ofertas': 'sem_7_bruto',
    'semestre_8_bruto_ofertas': 'sem_8_bruto',
    'semestre_9_bruto_ofertas': 'sem_9_bruto',
    'semestre_10_bruto_ofertas': 'sem_10_bruto',
    'semestre_11_bruto_ofertas': 'sem_11_bruto',
    'semestre_12_bruto_ofertas': 'sem_12_bruto',
    
    # Valores FIES
    'valor_curso_fies_ofertas': 'valor_curso_fies',
    'indice_correcao_ipca_ofertas': 'indice_correcao_ipca',
    'semestre_1_fies_ofertas': 'sem_1_fies',
    'semestre_2_fies_ofertas': 'sem_2_fies',
    'semestre_3_fies_ofertas': 'sem_3_fies',
    'semestre_4_fies_ofertas': 'sem_4_fies',
    'semestre_5_fies_ofertas': 'sem_5_fies',
    'semestre_6_fies_ofertas': 'sem_6_fies',
    'semestre_7_fies_ofertas': 'sem_7_fies',
    'semestre_8_fies_ofertas': 'sem_8_fies',
    'semestre_9_fies_ofertas': 'sem_9_fies',
    'semestre_10_fies_ofertas': 'sem_10_fies',
    'semestre_11_fies_ofertas': 'sem_11_fies',
    'semestre_12_fies_ofertas': 'sem_12_fies',
    
    # Colunas CINE
    'NO_CURSO': 'nome_curso_cine',
    'CO_CURSO': 'codigo_curso_cine',
    'CO_CINE_AREA_GERAL': 'codigo_cine_area_geral',
    'NO_CINE_AREA_GERAL': 'nome_cine_area_geral'
}

# --- 3. PROCESSAMENTO ---
print(f"Lendo arquivo de ofertas: {path_leitura_ofertas}")

df_ofertas = pd.read_csv(path_leitura_ofertas, low_memory=False) # Adicionado low_memory=False

print("Renomeando colunas...")
df_ofertas_renomeado = df_ofertas.rename(columns=mapa_nomes_curto)

# Cria o diretório se ele não existir
os.makedirs(os.path.dirname(path_salvar_ofertas), exist_ok=True)

print(f"Salvando arquivo renomeado em: {path_salvar_ofertas}")
df_ofertas_renomeado.to_csv(path_salvar_ofertas, index=False)

print("\n--- Processo Concluído (Ofertas) ---")

print("\nNovos nomes de colunas:")
print(df_ofertas_renomeado.columns.to_list())

# %%