#%%
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
import re

# =============================================================================
# MENTOR'S NOTES:
# Script CORRIGIDO para seguir a SUA DEFINIÇÃO de "Ranking de Prioridade".
# O ranking agora é baseado PURAMENTE na contagem de 'Inscritos_Validados',
# sem usar 'Vagas ofertadas FIES'. A lógica está correta conforme sua instrução.
# =============================================================================

# --- 1. SETUP E CARGA DOS DADOS ---
print("Carregando o DataFrame GERAL para a análise de ranking...")
try:
    df_geral = pd.read_csv('../../../planilhas/GERAL DF_funil 12 etapas.csv')
    print("DataFrame carregado com sucesso.")
except FileNotFoundError:
    print("ERRO: Arquivo '../../../planilhas/GERAL DF_funil 12 etapas.csv' não encontrado.")
    df_geral = None

CURSOS_COMPUTACAO = [
    'ANÁLISE E DESENVOLVIMENTO DE SISTEMAS', 'CIÊNCIA DA COMPUTAÇÃO',
    'SISTEMAS DE INFORMAÇÃO', 'REDES DE COMPUTADORES',
    'ENGENHARIA DA COMPUTAÇÃO', 'ENGENHARIA DE SOFTWARE'
]

def slugify(text):
    return re.sub(r'[\s\W-]+', '_', text).lower()

# --- 2. CÁLCULO E RANKING (LÓGICA CORRIGIDA) ---
if df_geral is not None:

    df_geral['Periodo'] = df_geral['Ano'].astype(str) + '/' + df_geral['Semestre'].astype(str)

    print("\n--- Passo 1: Agregando o total de 'Inscritos_Validados' por curso e período...")
    # Agrupa e soma apenas a coluna de interesse: Inscritos_Validados
    df_agregado = df_geral.groupby(['Periodo', 'Nome do Curso'])['Inscritos_Validados'].sum().reset_index()
    
    print("--- Passo 2: Criando o ranking baseado no volume de candidatos DENTRO de cada Período...")
    # O ranking agora é feito diretamente sobre a contagem de 'Inscritos_Validados'
    df_agregado['Posicao_Ranking_Geral'] = df_agregado.groupby('Periodo')['Inscritos_Validados'].rank(method='dense', ascending=False).astype(int)

    # --- 3. FILTRAGEM E EXTRAÇÃO DOS DADOS DE COMPUTAÇÃO ---
    print("--- Passo 3: Filtrando e extraindo a posição dos cursos de Computação...")
    
    df_ranking_comp = df_agregado[df_agregado['Nome do Curso'].isin(CURSOS_COMPUTACAO)]
    df_ranking_comp = df_ranking_comp.sort_values(['Periodo', 'Posicao_Ranking_Geral'])
    
    # Define o caminho para salvar o CSV na pasta de planilhas
    pasta_planilhas = '../../../planilhas'
    os.makedirs(pasta_planilhas, exist_ok=True)
    # Nome do arquivo ajustado para clareza
    caminho_csv = os.path.join(pasta_planilhas, 'ranking_prioridade_CANDIDATOS_cursos_comp.csv')
    
    df_ranking_comp.to_csv(caminho_csv, index=False, sep=';', decimal=',')
    print(f"\nDataFrame com o ranking (lógica correta) salvo em: {caminho_csv}")
    
    # --- 4. VISUALIZAÇÃO DA EVOLUÇÃO DO RANKING ---
    print("--- Passo 4: Gerando o gráfico da evolução da posição no ranking...")
    
    output_folder_graficos = 'GRAFICOS/ANALISE DE PRIORIDADE (CANDIDATOS)'
    os.makedirs(output_folder_graficos, exist_ok=True)
    
    plt.style.use('ggplot')
    fig, ax = plt.subplots(figsize=(18, 10))
    
    sns.lineplot(
        data=df_ranking_comp,
        x='Periodo',
        y='Posicao_Ranking_Geral',
        hue='Nome do Curso',
        style='Nome do Curso',
        markers=True,
        markersize=10,
        linewidth=2.5,
        ax=ax
    )
    
    ax.set_title('Evolução da Posição dos Cursos de Computação no Ranking de Prioridade (por INSCRITOS)', fontsize=16, pad=20, weight='bold')
    ax.set_xlabel('Período', fontsize=12)
    ax.set_ylabel('Posição no Ranking Geral (Menor = Mais Prioritário)', fontsize=12)
    
    ax.invert_yaxis()
    
    ax.legend(title='Curso de Computação', bbox_to_anchor=(1.05, 1), loc='upper left')
    ax.grid(True, which='both', linestyle='--', linewidth=0.5)
    
    plt.tight_layout()
    caminho_grafico = os.path.join(output_folder_graficos, 'evolucao_ranking_prioridade_CANDIDATOS_comp.png')
    plt.savefig(caminho_grafico, dpi=300, bbox_inches='tight')
    plt.close(fig)
    print(f"Gráfico de evolução salvo em: {caminho_grafico}")

    print("\n\nAnálise de prioridade (lógica correta) concluída!")
else:
    print("\nO script não pôde continuar porque os dados não foram carregados.")
# %%
