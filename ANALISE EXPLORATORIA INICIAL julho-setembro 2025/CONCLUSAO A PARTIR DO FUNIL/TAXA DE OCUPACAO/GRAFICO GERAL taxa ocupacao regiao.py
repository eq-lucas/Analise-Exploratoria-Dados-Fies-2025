#%%
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import seaborn as sns
import os
import re

# =============================================================================
# MENTOR'S NOTES:
# Este script lê o DataFrame consolidado do FIES Geral e gera os gráficos
# de taxa de ocupação, salvando na pasta 'GRAFICOS/GERAL regiao'.
# =============================================================================

METRICAS_PLOT = {
    'por_candidato': 'Taxa_Ocupacao_por_Candidato',
    'por_inscrito': 'Taxa_Ocupacao_por_Inscrito'
}

def criar_pastas_graficos(base_folder='GRAFICOS/GERAL regiao'):
    """Cria a estrutura de pastas de saída para os gráficos."""
    print("Verificando/criando estrutura de pastas para gráficos...")
    os.makedirs(base_folder, exist_ok=True)
    for metrica_key in METRICAS_PLOT.keys():
        path = os.path.join(base_folder, f'taxas_ocupacao_{metrica_key}')
        os.makedirs(path, exist_ok=True)
    print("Estrutura de pastas pronta.\n")
    return base_folder

def carregar_dataframe_resumo(caminho_arquivo):
    """Carrega o DataFrame de resumo gerado anteriormente."""
    print(f"Tentando carregar o DataFrame de resumo de: {caminho_arquivo}")
    try:
        df = pd.read_csv(caminho_arquivo, sep=';', decimal=',')
        print(f"DataFrame carregado com sucesso. Total de {len(df)} linhas.")
        return df
    except FileNotFoundError:
        print(f"ERRO CRÍTICO: O arquivo '{caminho_arquivo}' não foi encontrado.")
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
        ax=ax, palette='plasma', order=ordem_regioes_presentes, hue_order=ordem_periodos
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
    text = text.lower()
    text = re.sub(r'[\s\W-]+', '_', text)
    return text

# =============================================================================
# EXECUÇÃO PRINCIPAL
# =============================================================================

print("Iniciando script para gerar gráficos do DataFrame do FIES Geral...")

# AJUSTE NO CAMINHO PARA LER O ARQUIVO
caminho_df_entrada = '../../../planilhas/resumo_taxas_ocupacao_FIES_GERAL.csv'

df_fies_geral = carregar_dataframe_resumo(caminho_df_entrada)

if df_fies_geral is not None and not df_fies_geral.empty:
    output_folder = criar_pastas_graficos()
    
    for metrica_key, coluna_taxa_plot in METRICAS_PLOT.items():
        print(f"\n--- Gerando gráfico para: {metrica_key.replace('_', ' ')} ---")
        pasta_destino = os.path.join(output_folder, f'taxas_ocupacao_{metrica_key}')
        
        titulo_grafico = f'Taxa de Ocupação ({metrica_key.replace("_", " ")}) por Região\nFIES Geral (Todos os Cursos)'
        nome_arquivo = f'taxa_ocupacao_FIES_geral_{slugify(metrica_key)}.png'
        caminho_completo = os.path.join(pasta_destino, nome_arquivo)
        
        gerar_grafico_agrupado(df_fies_geral, titulo_grafico, coluna_taxa_plot, caminho_completo)

    print("\n\nTodos os gráficos para FIES Geral foram gerados com sucesso!")
else:
    print("\nNão foi possível gerar os gráficos porque o DataFrame de entrada estava vazio ou não foi carregado.")
# %%
