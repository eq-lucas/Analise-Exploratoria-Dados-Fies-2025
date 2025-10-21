# %%
import pandas as pd
import os

# --- 1. Configuração ---
pd.set_option('display.max_rows', None) # Para mostrar todas as áreas
pd.set_option('display.max_columns', None)

# Caminho para os arquivos que seu script anterior GEROU
path_leitura = '../../../planilhas/limpo/modulo_1/ofertas_coluna_CINE/'

# Coluna que você quer analisar
coluna_para_analisar = 'NO_CINE_AREA_GERAL' 

# --- 2. Verificar o diretório ---
print(f"Iniciando leitura dos arquivos em: {path_leitura}\n")

if not os.path.exists(path_leitura):
    print(f"ERRO: O diretório não existe: {path_leitura}")
else:
    try:
        lista_nomes_arquivos = os.listdir(path_leitura)
        # Ordenar a lista ajuda a ver os resultados em ordem cronológica
        lista_nomes_arquivos.sort() 
    except Exception as e:
        print(f"ERRO ao ler o diretório: {e}")
        lista_nomes_arquivos = []

    if not lista_nomes_arquivos:
        print("Nenhum arquivo encontrado no diretório.")

    # --- 3. Loop de Análise Individual ---
    for arquivo in lista_nomes_arquivos:
        
        if arquivo.endswith('.csv'):
            caminho_completo = os.path.join(path_leitura, arquivo)
            
            # Imprime um cabeçalho para cada arquivo
            print(f"\n{'='*80}")
            print(f"--- Iniciando Análise do Arquivo: {arquivo} ---")
            print(f"{'='*80}")
            
            try:
                # Lê o dataframe individual
                df_temp = pd.read_csv(caminho_completo, low_memory=False)
                
                # Verifica se a coluna de análise realmente existe neste arquivo
                if coluna_para_analisar not in df_temp.columns:
                    print(f"  ERRO: A coluna '{coluna_para_analisar}' não foi encontrada neste arquivo!")
                    print(f"  Colunas disponíveis: {df_temp.columns.to_list()}")
                else:
                    # --- 4. Executar o "Group By + Count" (com value_counts) ---
                    print(f"\n  Contagem de valores para '{coluna_para_analisar}':")
                    
                    # value_counts(dropna=False) faz o groupby+count, INCLUINDO NaNs
                    contagem = df_temp[coluna_para_analisar].value_counts(dropna=False)
                    
                    # Imprime a contagem
                    print(contagem)

                    # --- 5. Resumo explícito dos NaNs para ESTE arquivo ---
                    print("\n  --- Resumo dos NaNs (para este arquivo) ---")
                    
                    total_linhas = len(df_temp)
                    total_nans = df_temp[coluna_para_analisar].isnull().sum()
                    
                    if total_linhas > 0:
                        percentual_nans = (total_nans / total_linhas) * 100
                        print(f"  Total de ofertas (linhas): {total_linhas}")
                        print(f"  Total de NaNs (cursos não encontrados): {total_nans}")
                        print(f"  Percentual de NaNs: {percentual_nans:.2f}%")
                    else:
                        print("  Arquivo está vazio.")
                        
            except Exception as e:
                print(f"  *** ERRO GERAL ao processar o arquivo {arquivo}: {e} ***")

    print(f"\n{'='*80}")
    print("--- Análise individual de todos os arquivos concluída. ---")
    print(f"{'='*80}")

# %%