# %%
# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
# SETUP E CARREGAMENTO DOS DADOS GERAIS
# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# --- 1. CARREGANDO O DATASET GERAL ---
# Usando o caminho para o seu arquivo com todos os cursos.
path = '../../../../planilhas/GERAL DF_funil 12 etapas.csv'


df = pd.read_csv(path)
print(f"Dataset GERAL '{path}' carregado com sucesso.")

# --- 2. PREPARAÇÃO DO DATAFRAME ---
# Criação da coluna 'Regiao'
mapa_regioes = {
    'AC': 'Norte', 'AP': 'Norte', 'AM': 'Norte', 'PA': 'Norte', 'RO': 'Norte', 'RR': 'Norte', 'TO': 'Norte',
    'AL': 'Nordeste', 'BA': 'Nordeste', 'CE': 'Nordeste', 'MA': 'Nordeste', 'PB': 'Nordeste', 'PE': 'Nordeste', 'PI': 'Nordeste', 'RN': 'Nordeste', 'SE': 'Nordeste',
    'DF': 'Centro-Oeste', 'GO': 'Centro-Oeste', 'MT': 'Centro-Oeste', 'MS': 'Centro-Oeste',
    'ES': 'Sudeste', 'MG': 'Sudeste', 'RJ': 'Sudeste', 'SP': 'Sudeste',
    'PR': 'Sul', 'RS': 'Sul', 'SC': 'Sul'
}
df['Regiao'] = df['UF do Local de Oferta'].map(mapa_regioes)

# Criação da coluna 'Periodo' para agrupar nos gráficos
df['Periodo'] = df['Ano'].astype(str) + '/' + df['Semestre'].astype(str)

# --- 3. DEFINIÇÃO DAS 11 ETAPAS DO FUNIL (LÓGICA DO SEU 1º SCRIPT) ---
# Identifica as colunas do funil de forma automática, excluindo as de agrupamento.
colunas_de_agrupamento = ['Ano', 'Semestre', 'Nome do Curso', 'UF do Local de Oferta', 'Regiao', 'Periodo']
COLUNAS_FUNIL_11_ETAPAS = [col for col in df.columns if col not in colunas_de_agrupamento]

print("\nAs 11 etapas do funil foram identificadas:")
print(COLUNAS_FUNIL_11_ETAPAS)


# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
# PREPARAÇÃO PARA GERAÇÃO DOS GRÁFICOS
# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=

# --- Criação da pasta de saída ---
output_dir = '../GRAFICOS/FUNIL 12 ETAPAS REGIAO GERAL'
os.makedirs(output_dir, exist_ok=True)
print(f"\nPasta '{output_dir}' pronta para salvar os gráficos.")

# Define um estilo visual
sns.set_style("whitegrid")

# Pega a lista de regiões diretamente do dataframe
regioes = sorted([r for r in df['Regiao'].unique() if pd.notna(r)])
print(f"Análise será feita para as regiões: {regioes}")

# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
# FUNÇÃO DE PLOTAGEM
# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
def plotar_e_salvar_funil_barras(dataframe, titulo, nome_base_arquivo, pasta_destino, colunas_funil):
    # Agrupa os dados por Período e soma as colunas do funil definidas
    df_agg = dataframe.groupby('Periodo')[colunas_funil].sum().reset_index()
    
    # Prepara o dataframe para o formato de plotagem
    df_melted = df_agg.melt(id_vars='Periodo', var_name='Etapa_Funil', value_name='Quantidade')
    df_melted['Etapa_Funil'] = pd.Categorical(df_melted['Etapa_Funil'], categories=colunas_funil, ordered=True)
    
    # Gera o gráfico
    plt.figure(figsize=(22, 10)) # Aumentei um pouco o tamanho para as 11 etapas
    sns.barplot(
        data=df_melted,
        x='Etapa_Funil',
        y='Quantidade',
        hue='Periodo',
        palette='viridis'
    )
    
    # Formatação
    plt.title(titulo, fontsize=20, weight='bold')
    plt.xlabel('Etapas do Funil de Seleção', fontsize=14)
    plt.ylabel('Quantidade', fontsize=14)
    plt.xticks(rotation=45, ha='right', fontsize=11)
    plt.tight_layout()
    
    # Salva o arquivo
    nome_arquivo_seguro = "".join([c if c.isalnum() else "_" for c in nome_base_arquivo]) + ".png"
    caminho_salvar = os.path.join(pasta_destino, nome_arquivo_seguro)
    
    plt.savefig(caminho_salvar, dpi=300)
    print(f"-> Gráfico salvo em: {caminho_salvar}")
    plt.close()

print("\nFunção de plotagem pronta.")

# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
# LÓGICA PRINCIPAL PARA ANÁLISE GERAL
# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=

# --- A) GERANDO OS 5 GRÁFICOS POR REGIÃO ---
print("\n--- INICIANDO GERAÇÃO DOS GRÁFICOS POR REGIÃO (12 ETAPAS) ---")

for regiao in regioes:
    df_filtrado = df[df['Regiao'] == regiao]
    
    if not df_filtrado.empty:
        titulo_grafico = f'Funil Geral do FIES com 12 Etapas (Região {regiao})'
        nome_arquivo = f'funil_geral_12_etapas_{regiao}'
        plotar_e_salvar_funil_barras(df_filtrado, titulo_grafico, nome_arquivo, output_dir, COLUNAS_FUNIL_11_ETAPAS)
    else:
        print(f"-> Aviso: Não há dados para a região '{regiao}'. Gráfico não gerado.")

# --- B) GERANDO O GRÁFICO NACIONAL COMPLETO ---
print("\n--- INICIANDO GERAÇÃO DO GRÁFICO NACIONAL (12 ETAPAS) ---")

titulo_nacional = 'Funil Nacional do FIES com 12 Etapas (Todas as Regiões)'
nome_arquivo_nacional = 'funil_nacional_12_etapas_total'
plotar_e_salvar_funil_barras(df, titulo_nacional, nome_arquivo_nacional, output_dir, COLUNAS_FUNIL_11_ETAPAS)


print("\n\n--- PROCESSO CONCLUÍDO! ---")
print(f"Todos os gráficos gerais de 12 etapas foram salvos na pasta '{output_dir}'.")

# %%