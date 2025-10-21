# %%
import pandas as pd
import os

# --- 1. Configuração ---
pd.set_option('display.max_rows', None) # Para mostrar todos os nomes
pd.set_option('display.max_columns', None)

# Caminho para os arquivos de OFERTAS JÁ MESCLADOS (com NaNs)
path_leitura_base = '../../../planilhas/limpo/modulo_1/ofertas_coluna_CINE/' # <-- Ajustado para OFERTAS

# Coluna que queremos CHECAR se é NaN
coluna_nan = 'NO_CINE_AREA_GERAL' 

# Coluna de NOME do curso das OFERTAS que queremos AGRUPAR
# !!! VERIFIQUE SE ESTE É O NOME CORRETO NO SEU ARQUIVO !!!
coluna_nome_curso_fies = 'nome_curso_ofertas' 

# --- 2. Ler e Concatenar todos os arquivos de OFERTAS ---
print(f"Lendo arquivos de OFERTAS de: {path_leitura_base}")
lista_dfs = []
try:
    lista_nomes_arquivos = os.listdir(path_leitura_base)
except FileNotFoundError:
    print(f"ERRO: Diretório não encontrado: {path_leitura_base}")
    lista_nomes_arquivos = []

if not lista_nomes_arquivos:
    print("Nenhum arquivo encontrado no diretório.")
else:
    for arquivo in lista_nomes_arquivos:
        # Garante que estamos lendo os CSVs corretos de ofertas
        if arquivo.endswith('.csv') and 'ofertas' in arquivo: 
            caminho_completo = os.path.join(path_leitura_base, arquivo)
            print(f"Lendo {arquivo}...")
            try:
                df_temp = pd.read_csv(caminho_completo, low_memory=False)
                
                # Checagem mínima de colunas
                if not coluna_nan in df_temp.columns:
                    print(f"  Aviso: Coluna '{coluna_nan}' não encontrada em {arquivo}. Pulando.")
                    continue
                if not coluna_nome_curso_fies in df_temp.columns:
                    print(f"  Aviso: Coluna '{coluna_nome_curso_fies}' não encontrada em {arquivo}. Pulando.")
                    print(f"  Colunas disponíveis: {df_temp.columns.to_list()}")
                    continue
                    
                lista_dfs.append(df_temp)
            except Exception as e:
                print(f"Erro ao ler {arquivo}: {e}")

if not lista_dfs:
    print("Nenhum dataframe de OFERTAS foi lido. Análise encerrada.")
else:
    # Junta todos os arquivos de ofertas em um só
    df_agrupado = pd.concat(lista_dfs, ignore_index=True)
    print("Todos os arquivos de OFERTAS foram concatenados.")

    # --- 3. ANÁLISE SOLICITADA PARA OFERTAS ---
    
    # 1. Filtra mantendo APENAS as linhas onde o merge falhou (NaN)
    print(f"\nFiltrando por NaNs na coluna '{coluna_nan}'...")
    df_nans = df_agrupado[df_agrupado[coluna_nan].isnull()].copy()

    total_nans = len(df_nans)
    
    if total_nans > 0:
        print(f"Total de NaNs encontrados em todos os arquivos de OFERTAS: {total_nans}")
        
        # 2. Faz o "group by" (value_counts) destes NaNs pela coluna de nome do curso
        print(f"\n--- Groupby dos NaNs por '{coluna_nome_curso_fies}' ---")
        
        contagem_nomes_nan = df_nans[coluna_nome_curso_fies].value_counts(dropna=False)
        
        # 3. Mostra o resultado (é uma Série do Pandas)
        display(contagem_nomes_nan)
        
        # Salvar esta análise em um CSV
        # Salva na mesma pasta dos auxiliares, mas com nome diferente
        path_save_analise = '../../../planilhas/limpo/modulo_2/ajustar_nan_cine_ofertas'
        os.makedirs(path_save_analise, exist_ok=True)
        nome_arquivo_analise = 'analise_nomes_nan_ofertas.csv' # <-- Nome ajustado
        caminho_salvar_analise = os.path.join(path_save_analise, nome_arquivo_analise)
        
        contagem_nomes_nan.to_csv(caminho_salvar_analise, header=['contagem'])
        print(f"\nAnálise também salva em: {caminho_salvar_analise}")

    else:
        print("Nenhum NaN encontrado na coluna '{coluna_nan}'.")

print("\n--- Análise de NaNs para OFERTAS concluída ---")
# %%