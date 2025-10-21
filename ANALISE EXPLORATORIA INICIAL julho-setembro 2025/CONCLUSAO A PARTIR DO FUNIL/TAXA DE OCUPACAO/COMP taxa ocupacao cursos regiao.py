#%%
import pandas as pd
import os

# =============================================================================
# MENTOR'S NOTES:
# Este script foi modificado para gerar um único DataFrame consolidado com as
# taxas de ocupação para todos os cursos de computação, agrupados por
# região e período. Ao final, ele salva o resultado em um arquivo CSV.
# =============================================================================

# =============================================================================
# SETUP: Constantes e Mapeamentos
# =============================================================================

CURSOS_COMPUTACAO = [
    'ANÁLISE E DESENVOLVIMENTO DE SISTEMAS', 'CIÊNCIA DA COMPUTAÇÃO',
    'SISTEMAS DE INFORMAÇÃO', 'REDES DE COMPUTADORES',
    'ENGENHARia DA COMPUTAÇÃO', 'ENGENHARIA DE SOFTWARE'
]

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

def calcular_metricas_agregadas(df):
    """
    Agrupa o DataFrame por Curso, Região e Período, e calcula as métricas.
    """
    # Colunas que serão somadas
    colunas_numericas = ['Vagas ocupadas', 'Candidatos_Unicos_Validados', 'Inscritos_Validados']
    
    # Converte para numérico, tratando erros e valores nulos
    for col in colunas_numericas:
        df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)
    
    # Agrupa e soma os valores
    df_agregado = df.groupby(['Nome do Curso', 'Regiao', 'Periodo'])[colunas_numericas].sum()
    
    # Calcula as taxas de ocupação
    # Métrica 1: Por Candidato
    numerador = df_agregado['Vagas ocupadas']
    denominador_candidato = df_agregado['Candidatos_Unicos_Validados']
    df_agregado['Taxa_Ocupacao_por_Candidato'] = (numerador / denominador_candidato).fillna(0).clip(0, 1)
    
    # Métrica 2: Por Inscrito
    denominador_inscrito = df_agregado['Inscritos_Validados']
    df_agregado['Taxa_Ocupacao_por_Inscrito'] = (numerador / denominador_inscrito).fillna(0).clip(0, 1)
    
    return df_agregado.reset_index()


# =============================================================================
# EXECUÇÃO PRINCIPAL
# =============================================================================

print("Iniciando script para gerar DataFrame de análise...")

# --- 1. Carga e Preparação dos Dados ---
df_comp_raw = carregar_e_preparar_dados('../../../planilhas/COMP DF_funil 12 etapas.csv')

if df_comp_raw is not None:
    # --- 2. Filtra apenas para os cursos de interesse ---
    df_computacao = df_comp_raw[df_comp_raw['Nome do Curso'].isin(CURSOS_COMPUTACAO)].copy()
    print(f"Filtrados {len(df_computacao)} registros para os cursos de Computação.")
    
    if not df_computacao.empty:
        # --- 3. Calcula todas as métricas agregadas ---
        print("Calculando métricas agregadas...")
        df_final = calcular_metricas_agregadas(df_computacao)
        
        # --- 4. Organiza e Exibe o Resultado ---
        # Reordenando as colunas para melhor visualização
        colunas_ordenadas = [
            'Nome do Curso', 'Regiao', 'Periodo',
            'Vagas ocupadas', 'Candidatos_Unicos_Validados', 'Inscritos_Validados',
            'Taxa_Ocupacao_por_Candidato', 'Taxa_Ocupacao_por_Inscrito'
        ]
        df_final = df_final[colunas_ordenadas]
        
        print("\n--- Amostra do DataFrame Final ---")
        print(df_final.head(10))
        print(f"\nTotal de {len(df_final)} linhas de resumo geradas.")

        # --- 5. Salva o DataFrame em um arquivo CSV ---
        caminho_salvar = '../../../planilhas/COMP taxa ocupacao cursos regiao.csv'
        print(f"\nSalvando o DataFrame final em '{caminho_salvar}'...")
        
        # Usamos separador ';' e decimal ',' para compatibilidade com Excel em português
        df_final.to_csv(caminho_salvar, index=False, sep=';', decimal=',')
        
        print("Arquivo salvo com sucesso!")
        
    else:
        print("AVISO: Nenhum registro encontrado para os cursos de computação especificados.")
else:
    print("\nO script não pôde continuar porque os dados não foram carregados.")
# %%
df_final
# %%
