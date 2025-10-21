# %%
import pandas as pd
import os

# --- 1. Configuração ---
pd.set_option('display.max_rows', None) # Para mostrar todas as áreas
pd.set_option('display.max_columns', None)

# Caminho para os arquivos que seu script anterior GEROU
path_leitura = '../../../planilhas/limpo/modulo_2/ajustar_nan_cine_ofertas/ofertas_agrupado_limpo_CORRIGIDO.csv'

# Coluna que você quer analisar
coluna_para_analisar = 'NO_CINE_AREA_GERAL' 



df_temp = pd.read_csv(path_leitura, low_memory=False)
                
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
        


    print(f"\n{'='*80}")
    print("--- Análise individual de todos os arquivos concluída. ---")
    print(f"{'='*80}")

# %%