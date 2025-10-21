# ==============================================================================
# --- 1. CONFIGURAÇÃO (Altere apenas as variáveis desta seção) ---
# ==============================================================================

# Caminho para o arquivo CSV que você quer carregar.
CAMINHO_DO_CSV = '2020/relatorio_resultado_fies_1_2020.csv'

# Nome que a tabela terá dentro do seu banco de dados MySQL.
NOME_DA_TABELA_SQL = "RESULTADOfies_1_inscricoes_2020_regular"

# Quantas linhas do CSV serão lidas e enviadas para o MySQL de cada vez.
# Experimente valores como 50000 ou 100000.
TAMANHO_DO_PEDACO = 1000000 

# --- Configurações da sua conexão com o MySQL ---
DB_USUARIO = "root"
DB_SENHA = "root"
DB_HOST = "localhost"
DB_NOME = "banco-dados-inscricoes"

# ==============================================================================
# --- 2. EXECUÇÃO DO SCRIPT (Não precisa alterar nada daqui para baixo) ---
# ==============================================================================

import pandas as pd
from sqlalchemy import create_engine
import time

# --- Conexão com o Banco de Dados ---
print("Iniciando o processo de carga de dados...")
try:
    db_porta = "3306"
    connection_string = f"mysql+pymysql://{DB_USUARIO}:{DB_SENHA}@{DB_HOST}:{db_porta}/{DB_NOME}"
    engine = create_engine(connection_string)
    print("Conexão com o MySQL estabelecida com sucesso.")
except Exception as e:
    print(f"ERRO: Falha ao conectar com o MySQL. Verifique suas credenciais. Erro: {e}")
    exit()

# --- Leitura e Carga em Pedaços (Chunks) ---
start_time = time.time()
print(f"Lendo o arquivo '{CAMINHO_DO_CSV}' e enviando para a tabela '{NOME_DA_TABELA_SQL}'...")

try:
    # Cria o 'iterador' que vai ler o CSV em pedaços, sem carregar tudo na memória.
    df_iterator = pd.read_csv(
        CAMINHO_DO_CSV,
        sep=';',
        encoding='latin-1',
        chunksize=TAMANHO_DO_PEDACO,
        low_memory=False,
        on_bad_lines="skip"
    )

    # --- Tratando o primeiro pedaço de forma especial ---
    # A função 'next()' pega o primeiro item do iterador (o primeiro carrinho de mão).
    primeiro_chunk = next(df_iterator)
    
    # Enviamos o primeiro pedaço usando 'replace' para (re)criar a tabela do zero.
    print("Criando/Recriando a tabela com o primeiro pedaço...")
    primeiro_chunk.to_sql(NOME_DA_TABELA_SQL, engine, if_exists='replace', index=False)
    print("Primeiro pedaço enviado.")

    # --- Loop para os pedaços restantes ---
    # O 'for' loop agora começa automaticamente do SEGUNDO pedaço em diante.
    i = 1
    for chunk in df_iterator:
        i += 1
        # A partir de agora, usamos 'append' para adicionar os dados à tabela já criada.
        chunk.to_sql(NOME_DA_TABELA_SQL, engine, if_exists='append', index=False)
        
        # Imprime o progresso em uma única linha que se atualiza.
        print(f"  -> Peça número {i} enviada...", end='\r')

    # Limpa a linha de progresso no final.
    print("\nTodos os pedaços foram enviados com sucesso!")

except FileNotFoundError:
    print(f"ERRO: O arquivo não foi encontrado no caminho: '{CAMINHO_DO_CSV}'")
except Exception as e:
    print(f"Ocorreu um erro durante o processo de carga: {e}")

finally:
    end_time = time.time()
    print(f"Tempo total de execução: {end_time - start_time:.2f} segundos.")
