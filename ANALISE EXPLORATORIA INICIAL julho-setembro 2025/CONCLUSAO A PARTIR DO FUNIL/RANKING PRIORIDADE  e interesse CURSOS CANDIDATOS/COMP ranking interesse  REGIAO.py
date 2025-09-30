#%%
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import seaborn as sns
import os
import re

# =============================================================================
# MENTOR'S NOTES:
# Este script executa a "Análise de Interesse" por região, utilizando como
# base os CANDIDATOS ÚNICOS VALIDADOS. Ele itera sobre cada região,
# calcula a distribuição e gera um gráfico para cada uma.
# =============================================================================

# --- 1. SETUP E CARGA DOS DADOS ---
print("Carregando o DataFrame GERAL para a análise de interesse (Candidatos) por região...")
try:
    df_geral = pd.read_csv('../../../planilhas/GERAL DF_funil 12 etapas.csv')
    df_geral['Periodo'] = df_geral['Ano'].astype(str) + '/' + df_geral['Semestre'].astype(str)
    
    MAPA_REGIAO = {
        'AC': 'NORTE', 'AP': 'NORTE', 'AM': 'NORTE', 'PA': 'NORTE', 'RO': 'NORTE', 'RR': 'NORTE', 'TO': 'NORTE',
        'AL': 'NORDESTE', 'BA': 'NORDESTE', 'CE': 'NORDESTE', 'MA': 'NORDESTE', 'PB': 'NORDESTE', 'PE': 'NORDESTE', 'PI': 'NORDESTE', 'RN': 'NORDESTE', 'SE': 'NORDESTE',
        'DF': 'CENTRO-OESTE', 'GO': 'CENTRO-OESTE', 'MT': 'CENTRO-OESTE', 'MS': 'CENTRO-OESTE',
        'ES': 'SUDESTE', 'MG': 'SUDESTE', 'RJ': 'SUDESTE', 'SP': 'SUDESTE',
        'PR': 'SUL', 'RS': 'SUL', 'SC': 'SUL'
    }
    df_geral['Regiao'] = df_geral['UF do Local de Oferta'].map(MAPA_REGIAO)
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

# --- 2. LOOP DE ANÁLISE POR REGIÃO ---
if df_geral is not None:
    lista_resultados_regionais = []
    
    output_folder_graficos = os.path.join('GRAFICOS', 'COMP regiao', 'ANALISE DE INTERESSE (CANDIDATOS)')
    os.makedirs(output_folder_graficos, exist_ok=True)
    
    regioes = df_geral['Regiao'].dropna().unique()
    print(f"\nRegiões encontradas: {', '.join(regioes)}")

    for regiao in regioes:
        print(f"\n--- Processando Região: {regiao} ---")
        df_regional = df_geral[df_geral['Regiao'] == regiao].copy()
        
        # --- Lógica de cálculo (Comp vs. Outros) ---
        df1_computacao = df_regional[df_regional['Nome do Curso'].isin(CURSOS_COMPUTACAO)]
        df2_outros = df_regional[~df_regional['Nome do Curso'].isin(CURSOS_COMPUTACAO)]

        # Usando 'Candidatos_Unicos_Validados'
        agregado_comp = df1_computacao.groupby('Periodo')['Candidatos_Unicos_Validados'].sum().reset_index()
        agregado_comp.rename(columns={'Candidatos_Unicos_Validados': 'Candidatos_em_Comp'}, inplace=True)

        agregado_outros = df2_outros.groupby('Periodo')['Candidatos_Unicos_Validados'].sum().reset_index()
        agregado_outros.rename(columns={'Candidatos_Unicos_Validados': 'Candidatos_em_Outros'}, inplace=True)

        df_resultado_regiao = pd.merge(agregado_comp, agregado_outros, on='Periodo', how='outer').fillna(0)
        
        df_resultado_regiao['Total_Candidatos'] = df_resultado_regiao['Candidatos_em_Comp'] + df_resultado_regiao['Candidatos_em_Outros']
        df_resultado_regiao = df_resultado_regiao[df_resultado_regiao['Total_Candidatos'] > 0]
        
        if df_resultado_regiao.empty:
            print(f"  -> AVISO: Não há dados de candidatos para a região {regiao}. Gráfico não será gerado.")
            continue

        df_resultado_regiao['Percentual_Comp'] = (df_resultado_regiao['Candidatos_em_Comp'] / df_resultado_regiao['Total_Candidatos'])
        df_resultado_regiao['Percentual_Outros'] = (df_resultado_regiao['Candidatos_em_Outros'] / df_resultado_regiao['Total_Candidatos'])
        
        df_resultado_regiao['Regiao'] = regiao
        lista_resultados_regionais.append(df_resultado_regiao)
        
        # --- Geração do Gráfico para a Região ---
        df_plot = df_resultado_regiao[['Periodo', 'Percentual_Comp', 'Percentual_Outros']].set_index('Periodo')
        
        plt.style.use('ggplot')
        fig, ax = plt.subplots(figsize=(16, 9))
        
        df_plot.plot(kind='bar', stacked=True, ax=ax, color=['#1f77b4', '#aec7e8'])

        ax.yaxis.set_major_formatter(mticker.PercentFormatter(xmax=1.0))
        for c in ax.containers:
            labels = [f'{v.get_height():.1%}' if v.get_height() > 0 else '' for v in c]
            ax.bar_label(c, labels=labels, label_type='center', color='white', weight='bold', fontsize=12)

        ax.set_title(f'Distribuição de Interesse dos Candidatos - Região {regiao.upper()}', fontsize=18, pad=20, weight='bold')
        ax.set_xlabel('Período', fontsize=14)
        ax.set_ylabel('Percentual de Candidatos', fontsize=14)
        ax.tick_params(axis='x', rotation=45)
        handles, labels = ax.get_legend_handles_labels()
        ax.legend(handles, ['Cursos de Computação', 'Outros Cursos'], title='Candidato inscrito em:', fontsize=12)

        plt.tight_layout()
        
        caminho_grafico = os.path.join(output_folder_graficos, f'distribuicao_interesse_CANDIDATOS_regiao_{slugify(regiao)}.png')
        plt.savefig(caminho_grafico, dpi=300)
        plt.close(fig)
        print(f"  -> Gráfico para a região {regiao} salvo com sucesso.")

    # --- 3. CONSOLIDAÇÃO E SALVAMENTO DO CSV FINAL ---
    if lista_resultados_regionais:
        df_final_todas_regioes = pd.concat(lista_resultados_regionais, ignore_index=True)
        
        colunas_ordenadas = ['Regiao', 'Periodo', 'Candidatos_em_Comp', 'Candidatos_em_Outros', 'Total_Candidatos', 'Percentual_Comp', 'Percentual_Outros']
        df_final_todas_regioes = df_final_todas_regioes[colunas_ordenadas]

        pasta_planilhas = '../../../planilhas'
        os.makedirs(pasta_planilhas, exist_ok=True)
        caminho_csv = os.path.join(pasta_planilhas, 'analise_interesse_CANDIDATOS_POR_REGIAO.csv')
        df_final_todas_regioes.to_csv(caminho_csv, index=False, sep=';', decimal=',')
        print(f"\nDataFrame consolidado com todas as regiões salvo em: {caminho_csv}")
        print("\n\nAnálise de interesse (Candidatos) por região concluída com sucesso!")
    else:
        print("\nNenhuma região com dados válidos foi processada. Nenhum CSV foi gerado.")
else:
    print("\nO script não pôde continuar porque os dados não foram carregados.")
# %%
