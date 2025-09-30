#%%
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import seaborn as sns
import os
import re

# =============================================================================
# MENTOR'S NOTES:
# Este script foi feito para carregar o DataFrame "resumo_taxas_ocupacao_computacao_GERAL.csv"
# e gerar os gráficos de barras agrupadas para as duas métricas de ocupação.
# =============================================================================

# =============================================================================
# SETUP: Constantes e Mapeamentos
# =============================================================================

METRICAS_PLOT = {
    'por_candidato': 'Taxa_Ocupacao_por_Candidato',
    'por_inscrito': 'Taxa_Ocupacao_por_Inscrito'
}

# =============================================================================
# Funções Auxiliares
# =============================================================================

def criar_pastas_graficos(base_folder='GRAFICOS/COMP regiao'):
    """Cria a estrutura de pastas de saída para os gráficos."""
    print("Verificando/criando estrutura de pastas para gráficos...")
    if not os.path.exists(base_folder):
        os.makedirs(base_folder)
    # Criar subpastas para cada métrica
    for metrica_key in METRICAS_PLOT.keys():
        path = os.path.join(base_folder, f'taxas_ocupacao_{metrica_key}')
        if not os.path.exists(path):
            os.makedirs(path)
    print("Estrutura de pastas pronta.\n")
    return base_folder

def carregar_dataframe_resumo(caminho_arquivo):
    """Carrega o DataFrame de resumo gerado anteriormente."""
    print(f"Tentando carregar o DataFrame de resumo de: {caminho_arquivo}")
    try:
        # Usamos separador ';' e decimal ',' porque foi assim que salvamos
        df = pd.read_csv(caminho_arquivo, sep=';', decimal=',')
        print(f"DataFrame carregado com sucesso. Total de {len(df)} linhas.")
        print("Colunas do DataFrame carregado:", df.columns.tolist())
        return df
    except FileNotFoundError:
        print(f"ERRO CRÍTICO: O arquivo '{caminho_arquivo}' não foi encontrado.")
        print("Certifique-se de que o script 'resumo_taxas_ocupacao_computacao_GERAL.csv' foi executado primeiro e o arquivo está na pasta correta.")
        return None
    except Exception as e:
        print(f"ERRO ao carregar o arquivo CSV: {e}")
        return None

def gerar_grafico_agrupado(df_plot, titulo, coluna_taxa, caminho_salvar):
    """Gera e salva o gráfico de barras agrupado."""
    ordem_regioes = ['NORTE', 'NORDESTE', 'CENTRO-OESTE', 'SUDESTE', 'SUL']
    ordem_periodos = sorted(df_plot['Periodo'].unique())
    ordem_regioes_presentes = [r for r in ordem_regioes if r in df_plot['Regiao'].unique()]
    
    plt.style.use('ggplot') 
    
    fig, ax = plt.subplots(figsize=(18, 10))
    sns.barplot(
        data=df_plot, x='Regiao', y=coluna_taxa, hue='Periodo',
        ax=ax, palette='viridis', order=ordem_regioes_presentes, hue_order=ordem_periodos
    )
    ax.set_title(titulo, fontsize=16, pad=20, weight='bold')
    ax.set_xlabel('Região', fontsize=12)
    ax.set_ylabel('Taxa de Ocupação', fontsize=12)
    ax.yaxis.set_major_formatter(mticker.PercentFormatter(xmax=1.0))
    ax.legend(title='Período')
    ax.set_ylim(0, max(0.1, df_plot[coluna_taxa].max() * 1.2 if not df_plot.empty else 0.1))
    
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

print("Iniciando script para gerar gráficos do DataFrame de Computação Geral...")

# --- 1. Define o caminho do DataFrame de entrada ---
caminho_df_entrada = '../../../planilhas/COMP taxa ocupacao regiao.csv'

# --- 2. Carrega o DataFrame de resumo ---
df_geral_computacao = carregar_dataframe_resumo(caminho_df_entrada)

# --- 3. Gera os gráficos se o DataFrame foi carregado com sucesso ---
if df_geral_computacao is not None and not df_geral_computacao.empty:
    output_folder = criar_pastas_graficos()
    
    for metrica_key, coluna_taxa_plot in METRICAS_PLOT.items():
        print(f"\n--- Gerando gráfico para: {metrica_key.replace('_', ' ')} ---")
        pasta_destino = os.path.join(output_folder, f'taxas_ocupacao_{metrica_key}')
        
        titulo_grafico = f'Taxa de Ocupação ({metrica_key.replace("_", " ")}) por Região\nComputação Geral'
        nome_arquivo = f'taxa_ocupacao_geral_computacao_{slugify(metrica_key)}.png'
        caminho_completo = os.path.join(pasta_destino, nome_arquivo)
        
        gerar_grafico_agrupado(df_geral_computacao, titulo_grafico, coluna_taxa_plot, caminho_completo)

    print("\n\nTodos os gráficos para Computação Geral foram gerados com sucesso!")
else:
    print("\nNão foi possível gerar os gráficos porque o DataFrame de entrada estava vazio ou não foi carregado.")
# %%
