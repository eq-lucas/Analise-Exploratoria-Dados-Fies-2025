# %%
import pandas as pd


# Dicionário para guardar o conjunto (set) de colunas de cada ano
colunas_por_ano = {}

print("Iniciando verificação dos cabeçalhos...\n")

# --- ETAPA 1: Ler os cabeçalhos de cada arquivo ---
for ano in range(2016,2025): # 2025 nao eh incluso entao vai ate 2024
    caminho_externo = f'../../../planilhas/externo/MICRODADOS_CADASTRO_CURSOS_{ano}.csv'
    
    print(f"--- Processando {ano} ---")
    try:
        # Usamos nrows=0 para ler APENAS o cabeçalho.
        # É extremamente rápido e economiza memória.
        df_header = pd.read_csv(
            caminho_externo,
            encoding='latin-1',
            sep=';',
            decimal=',',
            nrows=5 
        )
        
        # Armazena as colunas como um 'set' para facilitar a comparação
        colunas_por_ano[ano] = set(df_header.columns)
        print(f"Arquivo {ano} lido com sucesso. Total: {len(df_header.columns)} colunas.")
        
    except FileNotFoundError:
        print(f"!!! ERRO: Arquivo não encontrado em: {caminho_externo}")
        colunas_por_ano[ano] = None # Marca que este ano falhou
    except Exception as e:
        print(f"!!! ERRO ao ler o arquivo {ano}: {e}")
        colunas_por_ano[ano] = None

print("\n--- Verificação Concluída ---")


# --- ETAPA 2: Comparar os conjuntos de colunas ---
anos_validos = [ano for ano, colunas in colunas_por_ano.items() if colunas is not None]

if len(anos_validos) >= 2:
    print("\n--- Comparando Conjuntos de Colunas ---")
    
    # Pega o primeiro ano lido com sucesso como nossa referência
    ano_referencia = anos_validos[0]
    colunas_referencia = colunas_por_ano[ano_referencia]
    
    print(f"Usando {ano_referencia} como referência ({len(colunas_referencia)} colunas).")
    
    # Compara os outros anos com a referência
    for i in range(1, len(anos_validos)):
        ano_comparar = anos_validos[i]
        colunas_comparar = colunas_por_ano[ano_comparar]
        
        print(f"\nComparando {ano_referencia} vs {ano_comparar}:")
        
        # Colunas que estão na referência mas não no outro
        diferenca_1 = colunas_referencia - colunas_comparar
        if diferenca_1:
            print(f"  > Colunas em {ano_referencia} que NÃO estão em {ano_comparar}: {diferenca_1}")
        
        # Colunas que estão no outro mas não na referência
        diferenca_2 = colunas_comparar - colunas_referencia
        if diferenca_2:
            print(f"  > Colunas em {ano_comparar} que NÃO estão em {ano_referencia}: {diferenca_2}")
        
        if not diferenca_1 and not diferenca_2:
            print("  > Os conjuntos de colunas são IDÊNTICOS.")
else:
    print("\nNão foi possível comparar os arquivos (menos de 2 arquivos lidos com sucesso).")


# --- ETAPA 3: Listagem completa (para você me enviar) ---
print("\n\n--- Listagem Bruta das Colunas (para você me enviar) ---")
for ano, colunas in colunas_por_ano.items():
    if colunas is not None:
        print(f"\n====================\nCOLUNAS {ano}\n====================")
        # Imprime uma por linha, em ordem alfabética, para facilitar a leitura
        for col in sorted(list(colunas)):
            print(col)
    else:
        print(f"\n====================\nCOLUNAS {ano}\n====================\n(Falha na leitura)")
# %%
