#%%
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import seaborn as sns
import os
import re

# =============================================================================
# MENTOR'S NOTES:
# Script refeito para seguir sua especificação. O objetivo é analisar a
# "Distribuição de Interesse" (Market Share) entre os 6 cursos de Computação.
# A visualização usa BARRAS AGRUPADAS (lado a lado), conforme solicitado.
# =============================================================================

# --- 1. SETUP E CARGA DOS DADOS ---
print("Carregando o DataFrame de COMPUTAÇÃO para a análise de Distribuição de Interesse...")
try:
    # Usamos o arquivo COMP, pois nosso universo (o 100%) são apenas os cursos de TI
    df_comp = pd.read_csv('../../../planilhas/COMP DF_funil 12 etapas.csv')
    df_comp['Periodo'] = df_comp['Ano'].astype(str) + '/' + df_comp['Semestre'].astype(str)
    
    MAPA_REGIAO = {
        'AC': 'NORTE', 'AP': 'NORTE', 'AM': 'NORTE', 'PA': 'NORTE', 'RO': 'NORTE', 'RR': 'NORTE', 'TO': 'NORTE',
        'AL': 'NORDESTE', 'BA': 'NORDESTE', 'CE': 'NORDESTE', 'MA': 'NORDESTE', 'PB': 'NORDESTE', 'PE': 'NORDESTE', 'PI': 'NORDESTE', 'RN': 'NORDESTE', 'SE': 'NORDESTE',
        'DF': 'CENTRO-OESTE', 'GO': 'CENTRO-OESTE', 'MT': 'CENTRO-OESTE', 'MS': 'CENTRO-OESTE',
        'ES': 'SUDESTE', 'MG': 'SUDESTE', 'RJ': 'SUDESTE', 'SP': 'SUDESTE',
        'PR': 'SUL', 'RS': 'SUL', 'SC': 'SUL'
    }
    df_comp['Regiao'] = df_comp['UF do Local de Oferta'].map(MAPA_REGIAO)
    print("DataFrame carregado e preparado com sucesso.")
except FileNotFoundError:
    print("ERRO: Arquivo '../../../planilhas/COMP DF_funil 12 etapas.csv' não encontrado.")
    df_comp = None

def slugify(text):
    return re.sub(r'[\s\W-]+', '_', text).lower()

def calcular_distribuicao_interesse(df, groupby_cols):
    """Calcula a distribuição percentual de candidatos dentro do universo da Computação."""
    
    # Agrupa para obter o número de candidatos por curso (e outras chaves)
    df_agregado = df.groupby(groupby_cols + ['Nome do Curso'])['Inscritos_Validados'].sum().reset_index()
    
    # Calcula o TOTAL de candidatos em computação para o grupo principal (nacional ou regional)
    df_agregado['Total_Candidatos_Comp'] = df_agregado.groupby(groupby_cols)['Inscritos_Validados'].transform('sum')
    
    # Calcula a Distribuição de Interesse (Market Share)
    df_agregado = df_agregado[df_agregado['Total_Candidatos_Comp'] > 0]
    df_agregado['Distribuicao_Interesse'] = df_agregado['Inscritos_Validados'] / df_agregado['Total_Candidatos_Comp']
    
    return df_agregado

def gerar_grafico_distribuicao_agrupado(df_plot, titulo, caminho_salvar):
    """Gera o gráfico de barras agrupadas (X=Curso, Barras=Período)."""
    plt.style.use('ggplot')
    fig, ax = plt.subplots(figsize=(20, 10))
    
    sns.barplot(
        data=df_plot,
        x='Nome do Curso',
        y='Distribuicao_Interesse',
        hue='Periodo',
        ax=ax,
        palette='magma'
    )
    
    ax.set_title(titulo, fontsize=18, pad=20, weight='bold')
    ax.set_xlabel('Curso de Computação', fontsize=14)
    ax.set_ylabel('Distribuição de Interesse (%)', fontsize=14)
    ax.yaxis.set_major_formatter(mticker.PercentFormatter(xmax=1.0))
    ax.legend(title='Período', fontsize=11)
    
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.savefig(caminho_salvar, dpi=300)
    plt.close(fig)
    print(f" -> Gráfico salvo em: {caminho_salvar}")

# --- EXECUÇÃO PRINCIPAL ---
if df_comp is not None:
    pasta_planilhas = '../../../planilhas'
    os.makedirs(pasta_planilhas, exist_ok=True)

    # --- PARTE 1: ANÁLISE NACIONAL ---
    print("\n--- INICIANDO ANÁLISE NACIONAL ---")
    df_nacional = calcular_distribuicao_interesse(df_comp, ['Periodo'])
    
    caminho_csv_nacional = os.path.join(pasta_planilhas, 'NACIONAL_distribuicao_interesse_por_curso.csv')
    df_nacional.to_csv(caminho_csv_nacional, index=False, sep=';', decimal=',')
    print(f"DataFrame Nacional salvo em: {caminho_csv_nacional}")
    
    pasta_graficos_nacional = 'GRAFICOS/DISTRIBUICAO_INTERESSE/NACIONAL'
    os.makedirs(pasta_graficos_nacional, exist_ok=True)
    
    titulo_nac = 'Distribuição de Interesse de INSCRITOS entre Cursos de Computação (Nacional)'
    caminho_nac = os.path.join(pasta_graficos_nacional, 'nacional_distribuicao_interesse.png')
    gerar_grafico_distribuicao_agrupado(df_nacional, titulo_nac, caminho_nac)

    # --- PARTE 2: ANÁLISE REGIONAL ---
    print("\n--- INICIANDO ANÁLISE REGIONAL ---")
    df_regional = calcular_distribuicao_interesse(df_comp, ['Regiao', 'Periodo'])
    
    caminho_csv_regional = os.path.join(pasta_planilhas, 'REGIONAL_distribuicao_interesse_por_curso.csv')
    df_regional.to_csv(caminho_csv_regional, index=False, sep=';', decimal=',')
    print(f"DataFrame Regional salvo em: {caminho_csv_regional}")

    pasta_graficos_regional = 'GRAFICOS/DISTRIBUICAO_INTERESSE/REGIONAL'
    os.makedirs(pasta_graficos_regional, exist_ok=True)
    
    for regiao in df_regional['Regiao'].dropna().unique():
        print(f" - Gerando gráfico para a Região: {regiao}")
        df_plot_regional = df_regional[df_regional['Regiao'] == regiao]
        
        titulo_reg = f'Distribuição de Interesse de INSCRITOS em Computação - Região {regiao}'
        caminho_reg = os.path.join(pasta_graficos_regional, f'regional_{slugify(regiao)}_distribuicao_interesse.png')
        gerar_grafico_distribuicao_agrupado(df_plot_regional, titulo_reg, caminho_reg)

    print("\n\nAnálise completa de Distribuição de Interesse concluída com sucesso!")
else:
    print("\nO script não pôde continuar porque os dados não foram carregados.")
# %%
