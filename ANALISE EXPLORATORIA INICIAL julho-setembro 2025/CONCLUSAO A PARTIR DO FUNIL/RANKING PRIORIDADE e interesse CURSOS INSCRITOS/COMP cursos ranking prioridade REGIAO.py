#%%
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
import re

# =============================================================================
# MENTOR'S NOTES:
# Script REGIONAL CORRIGIDO para seguir a SUA DEFINIÇÃO de "Ranking de Prioridade".
# O ranking agora é baseado PURAMENTE na contagem de 'Inscritos_Validados'
# dentro de cada região, sem usar 'Vagas ofertadas FIES'.
# =============================================================================

# --- 1. SETUP E CARGA DOS DADOS ---
print("Carregando o DataFrame GERAL para a análise de ranking por região...")
try:
    df_geral = pd.read_csv('../../../planilhas/GERAL DF_funil 12 etapas.csv')
    
    MAPA_REGIAO = {
        'AC': 'NORTE', 'AP': 'NORTE', 'AM': 'NORTE', 'PA': 'NORTE', 'RO': 'NORTE', 'RR': 'NORTE', 'TO': 'NORTE',
        'AL': 'NORDESTE', 'BA': 'NORDESTE', 'CE': 'NORDESTE', 'MA': 'NORDESTE', 'PB': 'NORDESTE', 'PE': 'NORDESTE', 'PI': 'NORDESTE', 'RN': 'NORDESTE', 'SE': 'NORDESTE',
        'DF': 'CENTRO-OESTE', 'GO': 'CENTRO-OESTE', 'MT': 'CENTRO-OESTE', 'MS': 'CENTRO-OESTE',
        'ES': 'SUDESTE', 'MG': 'SUDESTE', 'RJ': 'SUDESTE', 'SP': 'SUDESTE',
        'PR': 'SUL', 'RS': 'SUL', 'SC': 'SUL'
    }
    df_geral['Regiao'] = df_geral['UF do Local de Oferta'].map(MAPA_REGIAO)
    df_geral['Periodo'] = df_geral['Ano'].astype(str) + '/' + df_geral['Semestre'].astype(str)
    print("DataFrame carregado e preparado com sucesso.")
except FileNotFoundError:
    print("ERRO: Arquivo '../../../planilhas/GERAL DF_funil 12 etapas.csv' não encontrado.")
    df_geral = None

CURSOS_COMPUTACAO = [
    'ANÁLISE E DESENVOLVIMENTO DE SISTEMAS', 'CIÊNCIA DA COMPUTAÇÃO',
    'SISTEMAS DE INFORMAÇÃO', 'REDES DE COMPUTADORES',
    'ENGENHARIA DA COMPUTAÇÃO', 'ENGENHARIA DE SOFTWARE'
]

def slugify(text):
    """Converte texto em um nome de arquivo seguro."""
    return re.sub(r'[\s\W-]+', '_', text).lower()

# --- 2. CÁLCULO E RANKING POR REGIÃO (LÓGICA CORRIGIDA) ---
if df_geral is not None:
    print("\n--- Passo 1: Agregando o total de 'Inscritos_Validados' por curso, região e período...")
    
    # Agrupa e soma apenas a coluna de interesse: Inscritos_Validados
    df_agregado = df_geral.groupby(['Regiao', 'Periodo', 'Nome do Curso'])['Inscritos_Validados'].sum().reset_index()
    
    print("--- Passo 2: Criando o ranking baseado no volume de candidatos DENTRO de cada Região e Período...")
    # O ranking agora é feito diretamente sobre a contagem de 'Inscritos_Validados'
    df_agregado['Posicao_Ranking_Regional'] = df_agregado.groupby(['Regiao', 'Periodo'])['Inscritos_Validados'].rank(method='dense', ascending=False).astype(int)

    # --- 3. FILTRAGEM E SALVAMENTO DO CSV CONSOLIDADO ---
    print("--- Passo 3: Filtrando dados de Computação e salvando CSV consolidado...")
    df_ranking_comp_regional = df_agregado[df_agregado['Nome do Curso'].isin(CURSOS_COMPUTACAO)]
    df_ranking_comp_regional = df_ranking_comp_regional.sort_values(['Regiao', 'Periodo', 'Posicao_Ranking_Regional'])
    
    pasta_planilhas = '../../../planilhas'
    os.makedirs(pasta_planilhas, exist_ok=True)
    caminho_csv = os.path.join(pasta_planilhas, 'ranking_prioridade_CANDIDATOS_cursos_comp_POR_REGIAO.csv')
    df_ranking_comp_regional.to_csv(caminho_csv, index=False, sep=';', decimal=',')
    print(f"\nDataFrame com o ranking regional (lógica correta) salvo em: {caminho_csv}")

    # --- 4. VISUALIZAÇÃO - UM GRÁFICO POR REGIÃO ---
    print("\n--- Passo 4: Gerando um gráfico de evolução da posição no ranking para cada região...")
    
    output_folder_graficos = 'GRAFICOS/COMP regiao/ANALISE DE PRIORIDADE REGIONAL (CANDIDATOS)'
    os.makedirs(output_folder_graficos, exist_ok=True)
    
    regioes = df_ranking_comp_regional['Regiao'].dropna().unique()

    for regiao in regioes:
        print(f"  - Gerando gráfico para a Região: {regiao}")
        
        df_plot = df_ranking_comp_regional[df_ranking_comp_regional['Regiao'] == regiao]
        
        plt.style.use('ggplot')
        fig, ax = plt.subplots(figsize=(18, 10))
        
        sns.lineplot(
            data=df_plot,
            x='Periodo',
            y='Posicao_Ranking_Regional',
            hue='Nome do Curso',
            style='Nome do Curso',
            markers=True, markersize=10, linewidth=2.5,
            ax=ax
        )
        
        ax.set_title(f'Evolução da Posição no Ranking de Prioridade (por INSCRITOS) - REGIÃO {regiao.upper()}', fontsize=16, pad=20, weight='bold')
        ax.set_xlabel('Período', fontsize=12)
        ax.set_ylabel('Posição no Ranking Regional (Menor = Mais Prioritário)', fontsize=12)
        
        ax.invert_yaxis()
        
        ax.legend(title='Curso de Computação', bbox_to_anchor=(1.05, 1), loc='upper left')
        ax.grid(True, which='both', linestyle='--', linewidth=0.5)
        
        plt.tight_layout()
        caminho_grafico = os.path.join(output_folder_graficos, f'evolucao_ranking_CANDIDATOS_regiao_{slugify(regiao)}.png')
        plt.savefig(caminho_grafico, dpi=300, bbox_inches='tight')
        plt.close(fig)

    print("\n\nAnálise de prioridade por região (lógica correta) concluída!")
else:
    print("\nO script não pôde continuar porque os dados não foram carregados.")
# %%
