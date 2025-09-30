#%%
import pandas as pd
import os

# = "==========================================================================="
# MENTOR'S NOTES:
# Script ajustado para consolidar todos os cursos de Computação em uma
# única visão ("Computação Geral"). A principal mudança é a remoção do
# 'Nome do Curso' da cláusula de agrupamento (groupby).
# =============================================================================

# =============================================================================
# SETUP: Constantes e Mapeamentos
# =============================================================================

CURSOS_COMPUTACAO = [
    'ANÁLISE E DESENVOLVIMENTO DE SISTEMAS', 'CIÊNCIA DA COMPUTAÇÃO',
    'SISTEMAS DE INFORMAÇÃO', 'REDES DE COMPUTADORES',
    'ENGENHARIA DA COMPUTAÇÃO', 'ENGENHARIA DE SOFTWARE'
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

def calcular_metricas_agregadas_geral(df):
    """
    Agrupa o DataFrame por Região e Período, somando todos os cursos,
    e calcula as métricas de ocupação.
    """
    colunas_numericas = ['Vagas ocupadas', 'Candidatos_Unicos_Validados', 'Inscritos_Validados']
    
    for col in colunas_numericas:
        df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)
    
    # AQUI ESTÁ A MUDANÇA: agrupamos apenas por Região e Período
    df_agregado = df.groupby(['Regiao', 'Periodo'])[colunas_numericas].sum()
    
    # Calcula as taxas de ocupação para o total agregado
    numerador = df_agregado['Vagas ocupadas']
    denominador_candidato = df_agregado['Candidatos_Unicos_Validados']
    df_agregado['Taxa_Ocupacao_por_Candidato'] = (numerador / denominador_candidato).fillna(0).clip(0, 1)
    
    denominador_inscrito = df_agregado['Inscritos_Validados']
    df_agregado['Taxa_Ocupacao_por_Inscrito'] = (numerador / denominador_inscrito).fillna(0).clip(0, 1)
    
    return df_agregado.reset_index()


# =============================================================================
# EXECUÇÃO PRINCIPAL
# =============================================================================

print("Iniciando script para gerar DataFrame agregado de Computação Geral...")

# --- 1. Carga e Preparação dos Dados ---
df_comp_raw = carregar_e_preparar_dados('../../../planilhas/COMP DF_funil 12 etapas.csv')

if df_comp_raw is not None:
    # --- 2. Filtra apenas para os cursos de interesse ---
    df_computacao = df_comp_raw[df_comp_raw['Nome do Curso'].isin(CURSOS_COMPUTACAO)].copy()
    print(f"Filtrados {len(df_computacao)} registros para os cursos de Computação.")
    
    if not df_computacao.empty:
        # --- 3. Calcula as métricas agregadas para "Computação Geral" ---
        print("Agregando dados para 'Computação Geral'...")
        df_final = calcular_metricas_agregadas_geral(df_computacao)
        
        # --- 4. Organiza e Exibe o Resultado ---
        colunas_ordenadas = [
            'Regiao', 'Periodo',
            'Vagas ocupadas', 'Candidatos_Unicos_Validados', 'Inscritos_Validados',
            'Taxa_Ocupacao_por_Candidato', 'Taxa_Ocupacao_por_Inscrito'
        ]
        df_final = df_final[colunas_ordenadas]
        
        print("\n--- Amostra do DataFrame Final (Computação Geral) ---")
        print(df_final.head(10))
        print(f"\nTotal de {len(df_final)} linhas de resumo geradas.")

        # --- 5. Salva o DataFrame em um arquivo CSV ---
        caminho_salvar = '../../../planilhas/COMP taxa ocupacao regiao.csv'
        print(f"\nSalvando o DataFrame final em '{caminho_salvar}'...")
        
        df_final.to_csv(caminho_salvar, index=False, sep=';', decimal=',')
        
        print("Arquivo salvo com sucesso!")
        
    else:
        print("AVISO: Nenhum registro encontrado para os cursos de computação especificados.")
else:
    print("\nO script não pôde continuar porque os dados não foram carregados.")
# %%
df_final
# %%
