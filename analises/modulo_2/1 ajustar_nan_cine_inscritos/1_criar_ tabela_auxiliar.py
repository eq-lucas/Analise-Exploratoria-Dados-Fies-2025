# %%
import pandas as pd
import os

# --- 1. Configuração ---
pd.set_option('display.max_rows', None) # Para mostrar todos os nomes
pd.set_option('display.max_columns', None)

# Caminho para o arquivo que o seu script anterior CRIOU
path_agrupado_base = '../../../planilhas/limpo/modulo_1/agrupado/'
arquivo_agrupado = 'inscritos_agrupado.csv'
caminho_leitura = os.path.join(path_agrupado_base, arquivo_agrupado)

# Colunas que vamos usar
coluna_chave = 'nome_curso_inscricao'
coluna_valor1 = 'NO_CINE_AREA_GERAL'
coluna_valor2 = 'CO_CINE_AREA_GERAL' # <-- COLUNA ADICIONADA

# --- 2. Ler o arquivo agrupado principal ---
print(f"Lendo o arquivo agrupado principal: {caminho_leitura}")

try:
    df_principal = pd.read_csv(caminho_leitura, low_memory=False)
except FileNotFoundError:
    print(f"ERRO: Arquivo não encontrado: {caminho_leitura}")
    print("Por favor, rode o script de concatenação primeiro.")
    df_principal = None
except Exception as e:
    print(f"ERRO ao ler o arquivo: {e}")
    df_principal = None

# --- 3. Criar o Dataset Auxiliar (com 3 colunas) ---
if df_principal is not None:
    
    colunas_para_manter = [coluna_chave, coluna_valor1, coluna_valor2]
    
    # Verifica se as colunas necessárias existem
    if not all(col in df_principal.columns for col in colunas_para_manter):
        print(f"ERRO: Colunas essenciais não encontradas. Verifique a lista: {colunas_para_manter}")
        print(f"Colunas disponíveis: {df_principal.columns.to_list()}")
    else:
        print("Criando o dataset auxiliar...")

        # 1. Manter apenas as colunas que precisamos
        df_mapa = df_principal[colunas_para_manter]

        # 2. Remover todas as linhas onde a classificação (o NOME da área) é NaN
        #    Isso garante o que você disse: "nao teremos nenhum com nan aqui"
        df_mapa_sem_nans = df_mapa.dropna(subset=[coluna_valor1])
        
        print(f"Total de linhas válidas (sem NaN) encontradas: {len(df_mapa_sem_nans)}")

        # 3. Fazer o "group by" (drop_duplicates com 'subset' na chave)
        #    Isso garante UMA linha única por 'nome_curso_inscricao'
        df_auxiliar = df_mapa_sem_nans.drop_duplicates(subset=[coluna_chave]).reset_index(drop=True)

        # 4. Salvar o novo dataset auxiliar
        nome_salvar = 'dataset_auxiliar_curso_area.csv'
        # Novo caminho de salvamento que você especificou
        path_save= '../../../planilhas/limpo/modulo_2/ajustar_nan_cine_inscritos'
        
        # Garante que a pasta de destino exista
        os.makedirs(path_save, exist_ok=True) 

        caminho_salvar = os.path.join(path_save, nome_salvar)
        
        df_auxiliar.to_csv(caminho_salvar, index=False, encoding='utf-8-sig')

        # 5. Mostrar o resultado
        print(f"\n--- Dataset Auxiliar Criado (sem NaNs) ---")
        print(f"Total de mapeamentos únicos (cursos únicos) encontrados: {len(df_auxiliar)}")
        print(f"Dataset auxiliar salvo em: {caminho_salvar}")
        
        display(df_auxiliar) # O display mostrará as 3 colunas
else:
    print("Script encerrado devido a erro na leitura do arquivo.")

# %%