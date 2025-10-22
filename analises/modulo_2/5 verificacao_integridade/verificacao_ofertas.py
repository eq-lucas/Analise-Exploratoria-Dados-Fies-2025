# %%
import pandas as pd
import os

path='../../../planilhas/limpo/modulo_2/ajustar_nan_cine_ofertas/ofertas_agrupado_limpo_CORRIGIDO.csv'


PK = [
'codigo_e_mec_mantenedora_ofertas',
'codigo_local_oferta_ofertas',
'codigo_grupo_preferencia_ofertas',
'codigo_curso_ofertas',
'turno_ofertas',
]

df_limpo= pd.read_csv(path)

print(df_limpo.shape)

qtde_linhas_antes= df_limpo.shape[0]

df_agrupando_por_pk= df_limpo.groupby(by=PK,as_index=False).count()

qtde_linhas_depois= df_agrupando_por_pk.shape[0]

print(f'antes : {qtde_linhas_antes}')
print(f'depois: {qtde_linhas_depois}')

if qtde_linhas_antes != qtde_linhas_depois:

    print('\nERRO PROVAVEL DUPLICAÇÃO DE LINHA: ')
    
    filtro= df_limpo.duplicated(subset=df_limpo.columns.to_list(),keep='first')

    linhas_duplicadas= df_limpo[filtro].shape[0]

    print(f'Total de linhas duplicadas: {linhas_duplicadas}\n')

    if linhas_duplicadas == 0:

        print('ERRO PROVAVEL LINHA VAZIA:')

        df_sem_linha_vazia= df_limpo.dropna(subset=df_limpo.columns.to_list(),how='all')

        qtde_linhas_antes= df_sem_linha_vazia.shape[0]

        df_agrupando_por_pk= df_limpo.groupby(by=PK,as_index=False).count()

        qtde_linhas_depois= df_agrupando_por_pk.shape[0]

        print(f'\nantes : {qtde_linhas_antes}')
        print(f'depois: {qtde_linhas_depois}\n')


# --- Bloco de Verificação de Colunas ---
print("\n--- Verificando Nomes e Total de Colunas ---")

# Pega a lista de colunas
lista_colunas = df_limpo.columns.to_list()
total_colunas = len(lista_colunas)

print(f"Total de colunas: {total_colunas}\n")
print("Nomes das colunas:")

# Imprime uma por linha para facilitar a leitura
for coluna in lista_colunas:
    print(coluna)

print("--- Fim da Verificação de Colunas ---")
# %%
