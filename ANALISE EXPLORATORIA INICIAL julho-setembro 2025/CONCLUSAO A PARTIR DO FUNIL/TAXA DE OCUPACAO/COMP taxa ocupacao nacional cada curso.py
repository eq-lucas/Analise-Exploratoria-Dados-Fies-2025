#%%
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import seaborn as sns
import os

# =============================================================================
# MENTOR'S NOTES:
# Script ajustado conforme sua solicitação. Agora ele salva os gráficos na
# pasta 'GRAFICOS/COMP cursos nacional' e gera duas visualizações separadas:
# uma para cada métrica de taxa de ocupação.
# =============================================================================

# =============================================================================
# SETUP: Constantes e Funções Auxiliares
# =============================================================================

CURSOS_COMPUTACAO = [
    'ANÁLISE E DESENVOLVIMENTO DE SISTEMAS', 'CIÊNCIA DA COMPUTAÇÃO',
    'SISTEMAS DE INFORMAÇÃO', 'REDES DE COMPUTADORES',
    'ENGENHARIA DA COMPUTAÇÃO', 'ENGENHARIA DE SOFTWARE'
]

def carregar_e_preparar_dados(caminho_arquivo):
    """Carrega e prepara o DataFrame inicial."""
    print(f"Carregando dados de: {caminho_arquivo}")
    try:
        df = pd.read_csv(caminho_arquivo)
        print(f"Dados carregados com sucesso. Total de {len(df)} linhas.")
        df['Periodo'] = df['Ano'].astype(str) + '/' + df['Semestre'].astype(str)
        return df
    except FileNotFoundError:
        print(f"ERRO CRÍTICO: O arquivo '{caminho_arquivo}' não foi encontrado.")
        return None

def calcular_metricas_nacional_por_curso(df):
    """
    Agrupa o DataFrame por CURSO e PERÍODO, somando todas as regiões,
    e calcula as métricas de ocupação.
    """
    colunas_numericas = ['Vagas ocupadas', 'Candidatos_Unicos_Validados', 'Inscritos_Validados']
    
    for col in colunas_numericas:
        df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)
    
    df_agregado = df.groupby(['Nome do Curso', 'Periodo'])[colunas_numericas].sum()
    
    numerador = df_agregado['Vagas ocupadas']
    denominador_candidato = df_agregado['Candidatos_Unicos_Validados']
    df_agregado['Taxa_Ocupacao_por_Candidato'] = (numerador / denominador_candidato).fillna(0).clip(0, 1)
    
    denominador_inscrito = df_agregado['Inscritos_Validados']
    df_agregado['Taxa_Ocupacao_por_Inscrito'] = (numerador / denominador_inscrito).fillna(0).clip(0, 1)
    
    return df_agregado.reset_index()

def gerar_grafico_comparativo_cursos(df_plot, metrica_y, titulo, caminho_salvar):
    """Gera o gráfico de barras agrupadas comparando os cursos."""
    plt.style.use('ggplot')
    fig, ax = plt.subplots(figsize=(20, 10))
    
    sns.barplot(
        data=df_plot,
        x='Nome do Curso',
        y=metrica_y,
        hue='Periodo',
        ax=ax,
        palette='magma'
    )
    
    # Define o título do eixo Y dinamicamente
    if 'Candidato' in metrica_y:
        ylabel_text = 'Taxa de Ocupação (por Candidato)'
    else:
        ylabel_text = 'Taxa de Ocupação (por Inscrito)'
        
    ax.set_title(titulo, fontsize=18, pad=20, weight='bold')
    ax.set_xlabel('Curso de Computação', fontsize=14)
    ax.set_ylabel(ylabel_text, fontsize=14)
    ax.yaxis.set_major_formatter(mticker.PercentFormatter(xmax=1.0))
    ax.legend(title='Período', fontsize=11)
    
    plt.xticks(rotation=45, ha='right')
    
    plt.tight_layout()
    plt.savefig(caminho_salvar, dpi=300)
    plt.close(fig)
    print(f"Gráfico salvo com sucesso em: {caminho_salvar}")


# =============================================================================
# EXECUÇÃO PRINCIPAL
# =============================================================================

print("Iniciando script para gerar análise nacional por curso de Computação...")

df_comp_raw = carregar_e_preparar_dados('../../../planilhas/COMP DF_funil 12 etapas.csv')

if df_comp_raw is not None:
    df_computacao = df_comp_raw[df_comp_raw['Nome do Curso'].isin(CURSOS_COMPUTACAO)].copy()
    
    if not df_computacao.empty:
        print("Agregando dados nacionalmente para cada curso...")
        df_final = calcular_metricas_nacional_por_curso(df_computacao)
        
        pasta_planilhas = '../../../planilhas'
        os.makedirs(pasta_planilhas, exist_ok=True)
        caminho_csv = os.path.join(pasta_planilhas, 'NACIONAL_taxa_ocupacao_por_curso.csv')
        df_final.to_csv(caminho_csv, index=False, sep=';', decimal=',')
        print(f"\nDataFrame de resumo salvo em: {caminho_csv}")

        # --- GERAÇÃO DOS GRÁFICOS (AJUSTADO) ---
        print("\nGerando os gráficos comparativos entre os cursos...")
        
        # AJUSTE 1: Define a pasta de saída correta
        output_folder_graficos = 'GRAFICOS/COMP cursos nacional'
        os.makedirs(output_folder_graficos, exist_ok=True)
        
        # AJUSTE 2: Gera o primeiro gráfico (por Candidato)
        titulo_grafico_cand = 'Comparativo Nacional: Taxa de Ocupação por Curso (Base: Candidatos Únicos)'
        caminho_grafico_cand = os.path.join(output_folder_graficos, 'comparativo_nacional_POR_CANDIDATO.png')
        gerar_grafico_comparativo_cursos(df_final, 'Taxa_Ocupacao_por_Candidato', titulo_grafico_cand, caminho_grafico_cand)

        # AJUSTE 2: Gera o segundo gráfico (por Inscrito)
        titulo_grafico_insc = 'Comparativo Nacional: Taxa de Ocupação por Curso (Base: Inscritos Validados)'
        caminho_grafico_insc = os.path.join(output_folder_graficos, 'comparativo_nacional_POR_INSCRITO.png')
        gerar_grafico_comparativo_cursos(df_final, 'Taxa_Ocupacao_por_Inscrito', titulo_grafico_insc, caminho_grafico_insc)
        
        print("\n\nAnálise concluída com sucesso!")
        
    else:
        print("AVISO: Nenhum registro encontrado para os cursos de computação especificados.")
else:
    print("\nO script não pôde continuar porque os dados não foram carregados.")
# %%
