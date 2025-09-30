# %%
# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
# SETUP COM O NOVO DATASET GERAL
# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# --- CARREGANDO O NOVO DATASET GERAL ---
path = '../../../../planilhas/GERAL DF_funil 12 etapas.csv'


df = pd.read_csv(path)
print(f"Dataset GERAL '{path}' carregado com sucesso.")

# --- PREPARAÇÃO DO DATAFRAME (LÓGICA JÁ VALIDADA) ---
mapa_regioes = {
    'AC': 'Norte', 'AP': 'Norte', 'AM': 'Norte', 'PA': 'Norte', 'RO': 'Norte', 'RR': 'Norte', 'TO': 'Norte',
    'AL': 'Nordeste', 'BA': 'Nordeste', 'CE': 'Nordeste', 'MA': 'Nordeste', 'PB': 'Nordeste', 'PE': 'Nordeste', 'PI': 'Nordeste', 'RN': 'Nordeste', 'SE': 'Nordeste',
    'DF': 'Centro-Oeste', 'GO': 'Centro-Oeste', 'MT': 'Centro-Oeste', 'MS': 'Centro-Oeste',
    'ES': 'Sudeste', 'MG': 'Sudeste', 'RJ': 'Sudeste', 'SP': 'Sudeste',
    'PR': 'Sul', 'RS': 'Sul', 'SC': 'Sul'
}
df['Regiao'] = df['UF do Local de Oferta'].map(mapa_regioes)

COLUNAS_FUNIL_GRAFICAMENTE_SERA = [
    'Vagas ofertadas FIES',
    'Inscritos_Geral',
    'Inscritos_Com_Nota_Suficiente',
    'Candidatos_Unicos_Geral',
    'Concorrendo_Total', # CANDIDATOS UNICOS COM NOTA SUFICIENTE
    'Vagas ocupadas'
]

print("Setup inicial concluído. DataFrame GERAL carregado e coluna 'Regiao' criada.")


# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
# PREPARAÇÃO PARA GERAÇÃO DOS GRÁFICOS
# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=

# --- Criação de uma nova pasta para os gráficos GERAIS ---
output_dir_geral = '../GRAFICOS/FUNIL 6 ETAPAS  REGIAO GERAL'
os.makedirs(output_dir_geral, exist_ok=True)
print(f"Pasta '{output_dir_geral}' pronta para salvar os gráficos.")

# Define um estilo visual e cria a coluna 'Periodo'
sns.set_style("whitegrid")
df['Periodo'] = df['Ano'].astype(str) + '/' + df['Semestre'].astype(str)

# Pega a lista de regiões diretamente do dataframe
regioes = [r for r in df['Regiao'].unique() if pd.notna(r)]
print(f"Análise será feita para as regiões: {regioes}")



# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
# FUNÇÃO DE PLOTAGEM (EXATAMENTE A MESMA DE ANTES, 100% REUTILIZÁVEL)
# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
def plotar_e_salvar_funil_barras(dataframe, titulo, nome_base_arquivo, pasta_destino):
    df_agg = dataframe.groupby('Periodo')[COLUNAS_FUNIL_GRAFICAMENTE_SERA].sum().reset_index()
    df_melted = df_agg.melt(id_vars='Periodo', var_name='Etapa_Funil', value_name='Quantidade')
    df_melted['Etapa_Funil'] = pd.Categorical(df_melted['Etapa_Funil'], categories=COLUNAS_FUNIL_GRAFICAMENTE_SERA, ordered=True)
    
    plt.figure(figsize=(18, 9))
    sns.barplot(
        data=df_melted,
        x='Etapa_Funil',
        y='Quantidade',
        hue='Periodo',
        palette='viridis'
    )
    
    plt.title(titulo, fontsize=18, weight='bold')
    plt.xlabel('Etapas do Funil de Seleção', fontsize=14)
    plt.ylabel('Quantidade', fontsize=14)
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    
    nome_arquivo_seguro = "".join([c if c.isalnum() else "_" for c in nome_base_arquivo]) + ".png"
    caminho_salvar = os.path.join(pasta_destino, nome_arquivo_seguro)
    
    plt.savefig(caminho_salvar)
    print(f"-> Gráfico salvo em: {caminho_salvar}")
    plt.close()

print("\nFunção de plotagem pronta.")



# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
# LÓGICA PRINCIPAL SIMPLIFICADA PARA ANÁLISE GERAL
# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=

# --- A) GERANDO OS 5 GRÁFICOS POR REGIÃO ---
print("\n--- INICIANDO GERAÇÃO DOS GRÁFICOS POR REGIÃO ---")

for regiao in regioes:
    # Filtra o dataframe geral para a região atual
    df_filtrado = df[df['Regiao'] == regiao]
    
    if not df_filtrado.empty:
        # Cria um título e nome de arquivo dinâmicos
        titulo_grafico = f'Funil Geral do FIES (Região {regiao})'
        nome_arquivo = f'funil_geral_{regiao}'
        
        # Chama a função para gerar e salvar o gráfico
        plotar_e_salvar_funil_barras(df_filtrado, titulo_grafico, nome_arquivo, output_dir_geral)
    else:
        print(f"-> Aviso: Não há dados para a região '{regiao}'. Gráfico não gerado.")

# --- B) GERANDO O GRÁFICO NACIONAL COMPLETO ---
print("\n--- INICIANDO GERAÇÃO DO GRÁFICO NACIONAL ---")

# Para o gráfico nacional, simplesmente usamos o dataframe completo (df)
titulo_nacional = 'Funil Nacional do FIES (Todas as Regiões)'
nome_arquivo_nacional = 'funil_nacional_total'
plotar_e_salvar_funil_barras(df, titulo_nacional, nome_arquivo_nacional, output_dir_geral)


print("\n\n--- PROCESSO CONCLUÍDO! ---")
print(f"Todos os gráficos gerais foram salvos na pasta '{output_dir_geral}'.")


# %%
