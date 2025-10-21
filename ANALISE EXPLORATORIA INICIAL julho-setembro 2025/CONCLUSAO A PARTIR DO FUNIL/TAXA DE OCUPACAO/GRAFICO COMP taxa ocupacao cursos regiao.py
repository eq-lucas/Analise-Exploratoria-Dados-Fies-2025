#%%
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import seaborn as sns
import os
import re

# =============================================================================
# MENTOR'S NOTES:
# Este script foi refeito para focar apenas nos 6 cursos de Computação.
# Adicionei mensagens de status para podermos acompanhar o progresso e
# diagnosticar por que um gráfico poderia sair vazio.
# =============================================================================

# =============================================================================
# SETUP: Constantes, Mapeamentos e Funções Auxiliares
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

METRICAS = {
    'por_candidato': 'Candidatos_Unicos_Validados',
    'por_inscrito': 'Inscritos_Validados'
}

def criar_pastas(metricas_dict):
    """Cria a estrutura de pastas de saída."""
    print("Verificando/criando estrutura de pastas...")
    if not os.path.exists('GRAFICOS/cursos regiao'):
        os.makedirs('GRAFICOS/cursos regiao')
    for metrica in metricas_dict.keys():
        path = os.path.join('GRAFICOS/cursos regiao', f'taxas_ocupacao_{metrica}')
        if not os.path.exists(path):
            os.makedirs(path)
    print("Estrutura de pastas pronta.\n")

def carregar_e_preparar_dados(caminho_arquivo):
    """Carrega e prepara o DataFrame inicial."""
    print(f"Carregando dados de: {caminho_arquivo}")
    try:
        df = pd.read_csv(caminho_arquivo)
        print(f"Dados carregados com sucesso. Total de {len(df)} linhas.")
        df['Periodo'] = df['Ano'].astype(str) + '/' + df['Semestre'].astype(str)
        df['Regiao'] = df['UF do Local de Oferta'].map(MAPA_REGIAO)
        # Vamos usar todos os períodos disponíveis no arquivo por enquanto para não filtrar dados demais
        print(f"Períodos encontrados no arquivo: {sorted(df['Periodo'].unique())}")
        return df
    except FileNotFoundError:
        print(f"ERRO CRÍTICO: O arquivo '{caminho_arquivo}' não foi encontrado.")
        print("Verifique se o caminho está correto e se o arquivo existe.")
        return None

def calcular_taxa_agregada(df, denominador):
    """Agrupa por Região e Período e calcula a taxa de ocupação."""
    colunas_agregacao = ['Vagas ocupadas', denominador]
    for col in colunas_agregacao:
        df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)
        
    df_agregado = df.groupby(['Regiao', 'Periodo'])[colunas_agregacao].sum()
    
    numerador = df_agregado['Vagas ocupadas']
    denominador_valores = df_agregado[denominador]
    
    df_agregado['Taxa_Ocupacao'] = (numerador / denominador_valores).fillna(0)
    df_agregado['Taxa_Ocupacao'] = df_agregado['Taxa_Ocupacao'].clip(0, 1)
    
    return df_agregado.reset_index()

def gerar_grafico_agrupado(df_plot, titulo, caminho_salvar):
    """Gera e salva o gráfico de barras agrupado."""
    ordem_regioes = ['NORTE', 'NORDESTE', 'CENTRO-OESTE', 'SUDESTE', 'SUL']
    ordem_periodos = sorted(df_plot['Periodo'].unique())
    ordem_regioes_presentes = [r for r in ordem_regioes if r in df_plot['Regiao'].unique()]
    
    plt.style.use('ggplot') 
    
    fig, ax = plt.subplots(figsize=(18, 10))
    sns.barplot(
        data=df_plot, x='Regiao', y='Taxa_Ocupacao', hue='Periodo',
        ax=ax, palette='viridis', order=ordem_regioes_presentes, hue_order=ordem_periodos
    )
    ax.set_title(titulo, fontsize=16, pad=20, weight='bold')
    ax.set_xlabel('Região', fontsize=12)
    ax.set_ylabel('Taxa de Ocupação', fontsize=12)
    ax.yaxis.set_major_formatter(mticker.PercentFormatter(xmax=1.0))
    ax.legend(title='Período')
    ax.set_ylim(0, max(0.1, df_plot['Taxa_Ocupacao'].max() * 1.2 if not df_plot.empty else 0.1))
    
    plt.tight_layout()
    plt.savefig(caminho_salvar, dpi=300)
    plt.close(fig)
    print(f"  -> Gráfico salvo com sucesso em: {caminho_salvar}")

def slugify(text):
    """Converte texto em um nome de arquivo seguro."""
    text = text.lower()
    text = re.sub(r'[\s\W-]+', '_', text)
    return text

# =============================================================================
# EXECUÇÃO PRINCIPAL
# =============================================================================

# --- 1. Preparação do Ambiente e Carga de Dados ---
criar_pastas(METRICAS)
df_comp = carregar_e_preparar_dados('../../../planilhas/COMP DF_funil 12 etapas.csv')

# --- 2. Geração dos Gráficos (Apenas se os dados foram carregados) ---
if df_comp is not None:
    print("\nIniciando geração de gráficos para cada curso de Computação...")
    
    # Loop sobre as duas métricas (denominadores)
    for nome_metrica, coluna_denominador in METRICAS.items():
        print(f"\n--- Processando Métrica: Taxa de Ocupação {nome_metrica.replace('_', ' ')} ---")
        pasta_base = os.path.join('GRAFICOS/cursos regiao', f'taxas_ocupacao_{nome_metrica}')
        os.makedirs(pasta_base, exist_ok=True)

        # Loop sobre cada curso de computação
        for curso in CURSOS_COMPUTACAO:
            print(f"\n[CURSO]: {curso}")
            
            # Filtra o DataFrame principal para o curso atual
            df_curso_filtrado = df_comp[df_comp['Nome do Curso'] == curso].copy()
            
            # DIAGNÓSTICO: Verifica se encontramos dados para este curso
            if df_curso_filtrado.empty:
                print("  -> AVISO: Nenhum registro encontrado para este curso no arquivo. Gráfico não será gerado.")
                continue # Pula para o próximo curso
            else:
                print(f"  - Encontrados {len(df_curso_filtrado)} registros para este curso.")

            # Calcula os dados agregados para o gráfico
            df_plot = calcular_taxa_agregada(df_curso_filtrado, coluna_denominador)
            
            # DIAGNÓSTICO: Verifica se, após a agregação, ainda temos dados para plotar
            if df_plot.empty:
                print("  -> AVISO: Após o cálculo, não há dados válidos para plotar. Gráfico não será gerado.")
                continue # Pula para o próximo curso

            # Prepara os nomes e caminhos e gera o gráfico
            titulo_grafico = f'Taxa de Ocupação ({nome_metrica.replace("_", " ")}) por Região\nCurso: {curso}'
            nome_arquivo = f'taxa_ocupacao_curso_{slugify(curso)}.png'
            caminho_completo = os.path.join(pasta_base, nome_arquivo)
            
            gerar_grafico_agrupado(df_plot, titulo_grafico, caminho_completo)

    print("\n\nAnálise concluída!")

else:
    print("\nO script não pôde continuar porque os dados não foram carregados.")
# %%
