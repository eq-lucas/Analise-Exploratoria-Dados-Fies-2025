# %%
import pandas as pd
import os

pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)

# --- 1. CAMINHOS ---

# Caminho de LEITURA (o arquivo que você quer renomear)
path_leitura_ofertas= '../../../planilhas/limpo/modulo_2/inscritos_coluna_filtro_renda_regiao/ajustado_fies_pfies_inscritos.csv'

# Caminho de SAÍDA (onde salvar o arquivo com nomes novos)
path_salvar_ofertas = '../../../planilhas/limpo/modulo_3/limpar_e_padronizar_colunas/inscritos_limpo.csv'


mapa_nomes_curto = {
    # Chaves de processo
    'ano_processo_seletivo_inscricao': 'ano',
    'semestre_processo_seletivo_inscricao': 'semestre',
    'codigo_grupo_preferencia_inscricao': 'codigo_grupo_preferencia',
    'classificacao_inscricao': 'classificacao',
    'opcoes_cursos_inscricao_inscricao': 'opcao_curso',
    
    # Dados do Estudante
    'id_estudante_inscricao': 'id_estudante',
    'sexo_inscricao': 'sexo',
    'data_nascimento_inscricao': 'data_nascimento',
    'uf_residencia_inscricao': 'uf_residencia',
    'municipio_residencia_inscricao': 'municipio_residencia',
    'etnia_cor_inscricao': 'etnia_cor',
    'pessoa_com_deficiencia_inscricao': 'pessoa_com_deficiencia',
    
    # Escolaridade
    'concluiu_ensino_medio_escola_publica_inscricao': 'ensino_medio_escola_publica',
    'ano_conclusao_ensino_medio_inscricao': 'ano_conclusao_em',
    'concluiu_curso_superior_inscricao': 'concluiu_curso_superior',
    'professor_rede_publica_ensino_inscricao': 'professor_rede_publica',
    
    # Renda e Grupo Familiar
    'numero_membros_grupo_familiar_inscricao': 'membros_grupo_familiar',
    'renda_familiar_mensal_bruta_inscricao': 'renda_familiar_bruta',
    'renda_mensal_bruta_per_capita_inscricao': 'renda_per_capita',
    
    # Detalhes da Vaga (Grupo de Preferência)
    'regiao_grupo_preferencia_inscricao': 'regiao_gp',
    'uf_grupo_preferencia_inscricao': 'uf_gp',
    'codigo_microrregiao_inscricao': 'codigo_microrregiao_gp',
    'microrregiao_inscricao': 'microrregiao_gp',
    'codigo_mesorregiao_inscricao': 'codigo_mesorregiao_gp',
    'mesorregiao_inscricao': 'mesorregiao_gp',
    'conceito_curso_gp_inscricao': 'conceito_curso_gp',
    'nota_corte_grupo_preferencia_inscricao': 'nota_corte_gp',
    
    # Detalhes da IES
    'nome_mantenedora_inscricao': 'nome_mantenedora',
    'natureza_juridica_mantenedora_inscricao': 'natureza_juridica_mantenedora',
    'cnpj_mantenedora_inscricao': 'cnpj_mantenedora',
    'codigo_e_mec_mantenedora_inscricao': 'codigo_mec_mantenedora',
    'nome_ies_inscricao': 'nome_ies',
    'codigo_e_mec_ies_inscricao': 'codigo_mec_ies',
    'organizacao_academica_ies_inscricao': 'organizacao_academica_ies',
    'municipio_ies_inscricao': 'municipio_ies',
    'uf_ies_inscricao': 'uf_ies',
    
    # Detalhes do Local de Oferta
    'nome_local_oferta_inscricao': 'nome_local_oferta',
    'codigo_local_oferta_inscricao': 'codigo_local_oferta',
    'municipio_local_oferta_inscricao': 'municipio_local_oferta',
    'uf_local_oferta_inscricao': 'uf_local_oferta',
    
    # Detalhes do Curso
    'codigo_curso_inscricao': 'codigo_curso',
    'nome_curso_inscricao': 'nome_curso',
    'turno_inscricao': 'turno',
    'grau_inscricao': 'grau',
    'conceito_curso_inscricao': 'conceito_curso',
    'area_conhecimento_inscricao': 'area_conhecimento',
    'subarea_conhecimento_inscricao': 'subarea_conhecimento',

    # Notas ENEM
    'media_nota_enem_inscricao': 'media_enem',
    'ano_enem_inscricao': 'ano_enem',
    'nota_redacao_inscricao': 'nota_redacao',
    'nota_matematica_inscricao': 'nota_matematica',
    'nota_linguagens_inscricao': 'nota_linguagens',
    'nota_ciencias_natureza_inscricao': 'nota_ciencias_natureza',
    'nota_ciencias_humanas_inscricao': 'nota_ciencias_humanas',
    
    # Financiamento
    'beneficiado_creduc_ou_fies_inscricao': 'beneficiado_creduc_fies',
    'situacao_inscricao_fies_inscricao': 'situacao_fies',
    'percentual_financiamento_inscricao': 'percentual_financiamento',
    'semestre_financiamento_inscricao': 'semestre_financiamento',
    'qtde_semestre_financiado_inscricao': 'qtde_semestre_financiado',
    
    # Colunas CINE
    'NO_CURSO': 'nome_curso_cine',
    'CO_CURSO': 'codigo_curso_cine',
    'CO_CINE_AREA_GERAL': 'codigo_cine_area_geral',
    'NO_CINE_AREA_GERAL': 'nome_cine_area_geral',

}

# --- 3. PROCESSAMENTO ---
print(f"Lendo arquivo de ofertas: {path_leitura_ofertas}")



df_ofertas = pd.read_csv(path_leitura_ofertas, low_memory=False) # Adicionado low_memory=False

#df_ofertas= df_ofertas.drop(columns=['limite_temp']).copy()

print("Renomeando colunas...")
df_ofertas_renomeado = df_ofertas.rename(columns=mapa_nomes_curto)

# Cria o diretório se ele não existir
os.makedirs(os.path.dirname(path_salvar_ofertas), exist_ok=True)

print(f"Salvando arquivo renomeado em: {path_salvar_ofertas}")
df_ofertas_renomeado.to_csv(path_salvar_ofertas, index=False)

print("\n--- Processo Concluído (Ofertas) ---")

print("\nNovos nomes de colunas:")
print(df_ofertas_renomeado.columns.to_list())


pd.set_option('display.max_rows', None) # Para mostrar todos os nomes
pd.set_option('display.max_columns', None)

display(df_ofertas_renomeado.head())#type: ignore
# %%
