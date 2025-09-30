# %%
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import seaborn as sns
import os

# =============================================================================
# MENTOR'S NOTES:
# Este script implementa sua metodologia para medir a "retenção de interesse"
# dos candidatos com foco em Computação. Ele calcula a distribuição percentual
# de onde esses candidatos se inscrevem (Comp vs. Outros) a cada período.
# =============================================================================

# --- 1. SETUP E CARGA DOS DADOS ---
print("Carregando o DataFrame GERAL para a análise de interesse...")
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

# --- 2. DIVISÃO, AGREGAÇÃO E CÁLCULO (se os dados foram carregados) ---
if df_geral is not None:
    df_geral['Periodo'] = df_geral['Ano'].astype(str) + '/' + df_geral['Semestre'].astype(str)

    # Passo 1 e 2: Criar df1 (só Computação) e df2 (sem Computação)
    print("\nDividindo o DataFrame em 'Computação' e 'Outros Cursos'...")
    
    # df1: Mantendo apenas os cursos de Computação
    df1_computacao = df_geral[df_geral['Nome do Curso'].isin(CURSOS_COMPUTACAO)].copy()
    
    # df2: Removendo os cursos de Computação (usando o operador ~ que significa 'não')
    df2_outros = df_geral[~df_geral['Nome do Curso'].isin(CURSOS_COMPUTACAO)].copy()

    # Passo 3: Agregar cada grupo para somar os candidatos únicos
    print("Agregando os candidatos únicos para cada grupo por período...")
    agregado_comp = df1_computacao.groupby('Periodo')['Candidatos_Unicos_Validados'].sum().reset_index()
    agregado_comp.rename(columns={'Candidatos_Unicos_Validados': 'Candidatos_em_Comp'}, inplace=True)

    agregado_outros = df2_outros.groupby('Periodo')['Candidatos_Unicos_Validados'].sum().reset_index()
    agregado_outros.rename(columns={'Candidatos_Unicos_Validados': 'Candidatos_em_Outros'}, inplace=True)

    # Passo 4: Juntar os resultados e calcular as porcentagens
    print("Juntando os resultados e calculando os percentuais de interesse...")
    df_final = pd.merge(agregado_comp, agregado_outros, on='Periodo', how='outer').fillna(0)
    
    df_final['Total_Candidatos'] = df_final['Candidatos_em_Comp'] + df_final['Candidatos_em_Outros']
    
    # Evita divisão por zero se um período não tiver candidatos
    df_final = df_final[df_final['Total_Candidatos'] > 0]
    
    df_final['Percentual_Comp'] = (df_final['Candidatos_em_Comp'] / df_final['Total_Candidatos'])
    df_final['Percentual_Outros'] = (df_final['Candidatos_em_Outros'] / df_final['Total_Candidatos'])

    # --- 5. SALVAR O DATAFRAME NA PASTA 'PLANILHAS' ---
    pasta_planilhas = '../../../planilhas'
    os.makedirs(pasta_planilhas, exist_ok=True)
    caminho_csv = os.path.join(pasta_planilhas, 'analise_interesse_candidatos_comp_vs_outros.csv')
    df_final.to_csv(caminho_csv, index=False, sep=';', decimal=',')
    print(f"\nDataFrame da análise de interesse salvo em: {caminho_csv}")

    # --- 6. GERAR GRÁFICO 100% EMPILHADO ---
    print("Gerando o gráfico da distribuição de interesse...")
    
    # Preparar dados para plotagem
    df_plot = df_final[['Periodo', 'Percentual_Comp', 'Percentual_Outros']].set_index('Periodo')
    
    plt.style.use('ggplot')
    fig, ax = plt.subplots(figsize=(16, 9))
    
    # Plotar o gráfico de barras 100% empilhado
    df_plot.plot(
        kind='bar',
        stacked=True,
        ax=ax,
        color=['#1f77b4', '#aec7e8'] # Azul para Comp, azul claro para Outros
    )

    # Formatar o eixo Y para mostrar porcentagens
    ax.yaxis.set_major_formatter(mticker.PercentFormatter(xmax=1.0))
    
    # Adicionar rótulos de porcentagem no meio das barras
    for c in ax.containers:
        labels = [f'{v.get_height():.1%}' if v.get_height() > 0 else '' for v in c]
        ax.bar_label(c, labels=labels, label_type='center', color='white', weight='bold', fontsize=12)

    ax.set_title('Distribuição de Interesse dos Candidatos Focados em Computação', fontsize=18, pad=20, weight='bold')
    ax.set_xlabel('Período', fontsize=14)
    ax.set_ylabel('Percentual de Candidatos', fontsize=14)
    ax.tick_params(axis='x', rotation=45)
    
    # Melhorar a legenda
    handles, labels = ax.get_legend_handles_labels()
    ax.legend(handles, ['Cursos de Computação', 'Outros Cursos'], title='Inscrito em:', fontsize=12)

    plt.tight_layout()
    
    # Salvar o gráfico
    output_folder_graficos = 'GRAFICOS/ANALISE DE INTERESSE'
    os.makedirs(output_folder_graficos, exist_ok=True)
    caminho_grafico = os.path.join(output_folder_graficos, 'distribuicao_interesse_candidatos.png')
    plt.savefig(caminho_grafico, dpi=300)
    plt.close(fig)
    print(f"Gráfico da análise de interesse salvo em: {caminho_grafico}")

    print("\n\nAnálise de interesse concluída com sucesso!")
else:
    print("\nO script não pôde continuar porque os dados não foram carregados.")
# %%
