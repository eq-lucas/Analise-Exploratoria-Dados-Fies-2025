# %%
import pandas as pd
import os

# --- 1. Configuração ---
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)

# CAMINHO BASE onde estão os arquivos individuais de OFERTAS com CINE
path_leitura_base = '../../../planilhas/limpo/modulo_1/ofertas_coluna_CINE/' # <-- Ajustado para OFERTAS

# COLUNAS QUE VAMOS USAR (Verifique os nomes!)
coluna_chave = 'nome_curso_ofertas' # <-- Ajustado para OFERTAS (VERIFIQUE!)
coluna_valor1 = 'NO_CINE_AREA_GERAL'
coluna_valor2 = 'CO_CINE_AREA_GERAL'

# --- 2. Ler e Concatenar os arquivos de OFERTAS ---
print(f"Lendo arquivos individuais de OFERTAS de: {path_leitura_base}")
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
        if arquivo.endswith('.csv') and 'ofertas' in arquivo: # Garante que estamos pegando os de ofertas
            caminho_completo = os.path.join(path_leitura_base, arquivo)
            print(f"Lendo {arquivo}...")
            try:
                df_temp = pd.read_csv(caminho_completo, low_memory=False)
                
                # Checagem mínima de colunas
                colunas_necessarias = [coluna_chave, coluna_valor1, coluna_valor2]
                if not all(col in df_temp.columns for col in colunas_necessarias):
                    print(f"  Aviso: Colunas essenciais não encontradas em {arquivo}. Pulando.")
                    print(f"  Colunas encontradas: {df_temp.columns.to_list()}")
                    continue
                    
                lista_dfs.append(df_temp)
            except Exception as e:
                print(f"Erro ao ler {arquivo}: {e}")

if not lista_dfs:
    print("Nenhum dataframe de OFERTAS foi lido. Análise encerrada.")
else:
    # Junta todos os arquivos de ofertas em um só
    df_ofertas_agrupado = pd.concat(lista_dfs, ignore_index=True)
    print("Todos os arquivos de OFERTAS foram concatenados.")

    # --- 3. Criar o Dataset Auxiliar para OFERTAS ---
    
    colunas_para_manter = [coluna_chave, coluna_valor1, coluna_valor2]
    
    print("Criando o dataset auxiliar para OFERTAS...")

    # 1. Manter apenas as colunas que precisamos
    df_mapa = df_ofertas_agrupado[colunas_para_manter]

    # 2. Remover todas as linhas onde a classificação (o NOME da área) é NaN
    df_mapa_sem_nans = df_mapa.dropna(subset=[coluna_valor1])
    
    print(f"Total de linhas válidas (sem NaN) encontradas nas ofertas: {len(df_mapa_sem_nans)}")

    # 3. Fazer o "group by" (drop_duplicates com 'subset' na chave)
    #    Isso garante UMA linha única por 'nome_curso_ofertas'
    df_auxiliar_ofertas = df_mapa_sem_nans.drop_duplicates(subset=[coluna_chave]).reset_index(drop=True)

    # 4. Salvar o novo dataset auxiliar
    nome_salvar = 'dataset_auxiliar_curso_area_ofertas.csv' # <-- Nome ajustado
    # Salvar na mesma pasta do auxiliar de inscrição
    path_save= '../../../planilhas/limpo/modulo_2/ajustar_nan_cine_ofertas' 
    os.makedirs(path_save, exist_ok=True) 
    caminho_salvar = os.path.join(path_save, nome_salvar)
    
    df_auxiliar_ofertas.to_csv(caminho_salvar, index=False, encoding='utf-8')

    # 5. Mostrar o resultado
    print(f"\n--- Dataset Auxiliar de OFERTAS Criado (sem NaNs) ---")
    print(f"Total de mapeamentos únicos (cursos únicos) encontrados: {len(df_auxiliar_ofertas)}")
    print(f"Dataset auxiliar salvo em: {caminho_salvar}")
    
    display(df_auxiliar_ofertas) # O display mostrará as 3 colunas

# %%