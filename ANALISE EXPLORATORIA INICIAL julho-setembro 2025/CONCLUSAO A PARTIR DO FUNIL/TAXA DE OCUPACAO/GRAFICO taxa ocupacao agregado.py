#%%
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import seaborn as sns
import os
import re

# =============================================================================
# MENTOR'S NOTES:
# Script ajustado conforme solicitado. A única mudança é o local e o nome
# dos arquivos .csv de resumo nacional, que agora serão salvos em
# '../../../planilhas/'. A geração de gráficos permanece inalterada.
# =============================================================================

# =============================================================================
# SETUP: Funções Auxiliares
# =============================================================================

def criar_estrutura_pastas_graficos():
    """Cria a estrutura de pastas de saída para os GRÁFICOS nacionais."""
    print("Verificando/criando estrutura de pastas para os gráficos...")
    base_path = os.path.join('GRAFICOS', 'TERRITORIO NACIONAL')
    subfolders = ['COMP CURSOS', 'COMP AGREGADO', 'TODOS OS CURSOS FIES']
    for folder in subfolders:
        os.makedirs(os.path.join(base_path, folder), exist_ok=True)
    print("Estrutura de pastas de gráficos pronta.\n")
    return {folder: os.path.join(base_path, folder) for folder in subfolders}

def carregar_resumo_regional(caminho_arquivo):
    """Carrega um dos DataFrames de resumo regional."""
    print(f"Carregando resumo regional de: {caminho_arquivo}")
    try:
        df = pd.read_csv(caminho_arquivo, sep=';', decimal=',')
        print(f" -> Sucesso: {len(df)} linhas carregadas.")
        return df
    except FileNotFoundError:
        print(f" -> ERRO CRÍTICO: O arquivo '{caminho_arquivo}' não foi encontrado.")
        return None

def recalcular_taxas_agregadas(df_agregado):
    """Recalcula as taxas de ocupação a partir de um DataFrame já somado."""
    numerador = df_agregado['Vagas ocupadas']
    denominador_candidato = df_agregado['Candidatos_Unicos_Validados']
    df_agregado['Taxa_Ocupacao_por_Candidato'] = (numerador / denominador_candidato).fillna(0).clip(0, 1)
    
    denominador_inscrito = df_agregado['Inscritos_Validados']
    df_agregado['Taxa_Ocupacao_por_Inscrito'] = (numerador / denominador_inscrito).fillna(0).clip(0, 1)
    return df_agregado

def gerar_grafico_nacional_barras(df_plot, titulo, caminho_salvar):
    """Gera e salva um gráfico de BARRAS da evolução nacional."""
    df_melted = df_plot.melt(
        id_vars=['Periodo'],
        value_vars=['Taxa_Ocupacao_por_Candidato', 'Taxa_Ocupacao_por_Inscrito'],
        var_name='Métrica',
        value_name='Taxa de Ocupação'
    )
    df_melted['Métrica'] = df_melted['Métrica'].map({
        'Taxa_Ocupacao_por_Candidato': 'Por Candidato Único',
        'Taxa_Ocupacao_por_Inscrito': 'Por Inscrito Validado'
    })
    df_melted_sorted = df_melted.sort_values('Periodo')
    
    plt.style.use('ggplot')
    fig, ax = plt.subplots(figsize=(16, 9))
    
    sns.barplot(data=df_melted_sorted, x='Periodo', y='Taxa de Ocupação', hue='Métrica', ax=ax, palette='viridis')
    
    ax.set_title(titulo, fontsize=16, pad=20, weight='bold')
    ax.set_xlabel('Período', fontsize=12)
    ax.set_ylabel('Taxa de Ocupação', fontsize=12)
    ax.yaxis.set_major_formatter(mticker.PercentFormatter(xmax=1.0))
    ax.legend(title='Métrica')
    ax.grid(True, which='major', axis='y', linestyle='--', linewidth=0.5)
    
    plt.tight_layout()
    plt.savefig(caminho_salvar, dpi=300)
    plt.close(fig)
    print(f"   -> Gráfico salvo em: {caminho_salvar}")

def slugify(text):
    return re.sub(r'[\s\W-]+', '_', text).lower()

# =============================================================================
# EXECUÇÃO PRINCIPAL
# =============================================================================

pastas_graficos = criar_estrutura_pastas_graficos()
pasta_base_dfs = '../../../planilhas'

# Garante que a pasta de destino para os DataFrames exista
os.makedirs(pasta_base_dfs, exist_ok=True)

# Caminhos de LEITURA dos resumos regionais
path_comp_cursos_regional = os.path.join(pasta_base_dfs, 'COMP taxa ocupacao cursos regiao.csv')
path_comp_agregado_regional = os.path.join(pasta_base_dfs, 'COMP taxa ocupacao regiao.csv')
path_fies_geral_regional = os.path.join(pasta_base_dfs, 'resumo_taxas_ocupacao_FIES_GERAL.csv')

df_comp_cursos_regional = carregar_resumo_regional(path_comp_cursos_regional)
df_comp_agregado_regional = carregar_resumo_regional(path_comp_agregado_regional)
df_fies_geral_regional = carregar_resumo_regional(path_fies_geral_regional)

# --- ANÁLISE 1: COMPUTAÇÃO POR CURSO (Nacional) ---
if df_comp_cursos_regional is not None:
    print("\n--- Iniciando Análise 1: Computação por Curso (Nacional) ---")
    df_nacional_cursos = df_comp_cursos_regional.groupby(['Nome do Curso', 'Periodo']).sum(numeric_only=True)
    df_nacional_cursos = recalcular_taxas_agregadas(df_nacional_cursos).reset_index()
    
    # AJUSTE NO CAMINHO DE SAÍDA DO CSV
    caminho_csv = os.path.join(pasta_base_dfs, 'NACIONAL_resumo_por_curso_comp.csv')
    df_nacional_cursos.to_csv(caminho_csv, index=False, sep=';', decimal=',')
    print(f" -> DataFrame salvo em: {caminho_csv}")
    
    for curso in df_nacional_cursos['Nome do Curso'].unique():
        print(f"  - Gerando gráfico para: {curso}")
        df_plot = df_nacional_cursos[df_nacional_cursos['Nome do Curso'] == curso]
        titulo = f'Taxa de Ocupação Nacional - {curso}'
        caminho_grafico = os.path.join(pastas_graficos['COMP CURSOS'], f'grafico_nacional_{slugify(curso)}.png')
        gerar_grafico_nacional_barras(df_plot, titulo, caminho_grafico)

# --- ANÁLISE 2: COMPUTAÇÃO AGREGADO (Nacional) ---
if df_comp_agregado_regional is not None:
    print("\n--- Iniciando Análise 2: Computação Agregado (Nacional) ---")
    df_nacional_agregado = df_comp_agregado_regional.groupby('Periodo').sum(numeric_only=True)
    df_nacional_agregado = recalcular_taxas_agregadas(df_nacional_agregado).reset_index()

    # AJUSTE NO CAMINHO DE SAÍDA DO CSV
    caminho_csv = os.path.join(pasta_base_dfs, 'NACIONAL_resumo_AGREGADO_comp.csv')
    df_nacional_agregado.to_csv(caminho_csv, index=False, sep=';', decimal=',')
    print(f" -> DataFrame salvo em: {caminho_csv}")

    titulo = 'Taxa de Ocupação Nacional - Computação (Agregado)'
    caminho_grafico = os.path.join(pastas_graficos['COMP AGREGADO'], 'grafico_nacional_comp_agregado.png')
    gerar_grafico_nacional_barras(df_nacional_agregado, titulo, caminho_grafico)

# --- ANÁLISE 3: TODOS OS CURSOS FIES (Nacional) ---
if df_fies_geral_regional is not None:
    print("\n--- Iniciando Análise 3: Todos os Cursos FIES (Nacional) ---")
    df_nacional_fies = df_fies_geral_regional.groupby('Periodo').sum(numeric_only=True)
    df_nacional_fies = recalcular_taxas_agregadas(df_nacional_fies).reset_index()

    # AJUSTE NO CAMINHO DE SAÍDA DO CSV
    caminho_csv = os.path.join(pasta_base_dfs, 'NACIONAL_resumo_AGREGADO_fies_geral.csv')
    df_nacional_fies.to_csv(caminho_csv, index=False, sep=';', decimal=',')
    print(f" -> DataFrame salvo em: {caminho_csv}")

    titulo = 'Taxa de Ocupação Nacional - FIES Geral (Todos os Cursos)'
    caminho_grafico = os.path.join(pastas_graficos['TODOS OS CURSOS FIES'], 'grafico_nacional_fies_geral.png')
    gerar_grafico_nacional_barras(df_nacional_fies, titulo, caminho_grafico)

print("\n\nAnálise Nacional concluída com sucesso!")
# %%
