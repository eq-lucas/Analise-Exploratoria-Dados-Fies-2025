#%%
import pandas as pd
import os

# =============================================================================
# MENTOR'S NOTES:
# Script ajustado para gerar o DataFrame consolidado do FIES Geral e salvá-lo
# diretamente, sem exibir uma amostra dos dados no final.
# =============================================================================

# =============================================================================
# SETUP: Constantes e Mapeamentos
# =============================================================================

MAPA_REGIAO = {
    'AC': 'NORTE', 'AP': 'NORTE', 'AM': 'NORTE', 'PA': 'NORTE', 'RO': 'NORTE', 'RR': 'NORTE', 'TO': 'NORTE',
    'AL': 'NORDESTE', 'BA': 'NORDESTE', 'CE': 'NORDESTE', 'MA': 'NORDESTE', 'PB': 'NORDESTE', 'PE': 'NORDESTE', 'PI': 'NORDESTE', 'RN': 'NORDESTE', 'SE': 'NORDESTE',
    'DF': 'CENTRO-OESTE', 'GO': 'CENTRO-OESTE', 'MT': 'CENTRO-OESTE', 'MS': 'CENTRO-OESTE',
    'ES': 'SUDESTE', 'MG': 'SUDESTE', 'RJ': 'SUDESTE', 'SP': 'SUDESTE',
    'PR': 'SUL', 'RS': 'SUL', 'SC': 'SUL'
}

# =============================================================================
# Funções Auxiliares
# =============================================================================

def carregar_e_preparar_dados(caminho_arquivo):
    """Carrega e prepara o DataFrame inicial."""
    print(f"Carregando dados de: {caminho_arquivo}")
    try:
        df = pd.read_csv(caminho_arquivo)
        print(f"Dados carregados com sucesso. Total de {len(df)} linhas.")
        df['Periodo'] = df['Ano'].astype(str) + '/' + df['Semestre'].astype(str)
        df['Regiao'] = df['UF do Local de Oferta'].map(MAPA_REGIAO)
        return df
    except FileNotFoundError:
        print(f"ERRO CRÍTICO: O arquivo '{caminho_arquivo}' não foi encontrado.")
        return None

def calcular_metricas_agregadas_geral(df):
    """
    Agrupa o DataFrame por Região e Período, somando todos os cursos,
    e calcula as métricas de ocupação.
    """
    colunas_numericas = ['Vagas ocupadas', 'Candidatos_Unicos_Validados', 'Inscritos_Validados']
    
    for col in colunas_numericas:
        df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)
    
    df_agregado = df.groupby(['Regiao', 'Periodo'])[colunas_numericas].sum()
    
    numerador = df_agregado['Vagas ocupadas']
    denominador_candidato = df_agregado['Candidatos_Unicos_Validados']
    df_agregado['Taxa_Ocupacao_por_Candidato'] = (numerador / denominador_candidato).fillna(0).clip(0, 1)
    
    denominador_inscrito = df_agregado['Inscritos_Validados']
    df_agregado['Taxa_Ocupacao_por_Inscrito'] = (numerador / denominador_inscrito).fillna(0).clip(0, 1)
    
    return df_agregado.reset_index()


# =============================================================================
# EXECUÇÃO PRINCIPAL
# =============================================================================

print("Iniciando script para gerar DataFrame agregado do FIES Geral...")

# --- 1. Carga e Preparação dos Dados ---
df_geral_raw = carregar_e_preparar_dados('../../../planilhas/GERAL DF_funil 12 etapas.csv')

if df_geral_raw is not None:
    # --- 2. Calcula as métricas agregadas para "FIES Geral" ---
    print("Agregando dados para 'FIES Geral' (todos os cursos)...")
    df_final = calcular_metricas_agregadas_geral(df_geral_raw)
    
    # --- 3. Organiza o Resultado ---
    colunas_ordenadas = [
        'Regiao', 'Periodo',
        'Vagas ocupadas', 'Candidatos_Unicos_Validados', 'Inscritos_Validados',
        'Taxa_Ocupacao_por_Candidato', 'Taxa_Ocupacao_por_Inscrito'
    ]
    df_final = df_final[colunas_ordenadas]
    
    # --- 4. Salva o DataFrame em um arquivo CSV ---
    caminho_salvar = '../../../planilhas/resumo_taxas_ocupacao_FIES_GERAL.csv'
    print(f"\nSalvando o DataFrame final em '{caminho_salvar}'...")
    
    df_final.to_csv(caminho_salvar, index=False, sep=';', decimal=',')
    
    print("Arquivo salvo com sucesso!")
        
else:
    print("\nO script não pôde continuar porque os dados não foram carregados.")
# %%
df_final
# %%
