# %%
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import os

# --- Caminho dos dados ---
path = '../../../planilhas/processado/modulo_4/taxas_por_uf_regiao_cine/taxas_por_regiao.csv'
df = pd.read_csv(path)

# --- Criar coluna de período (ex: 2021.1) ---
df['periodo'] = df['ano'].astype(str) + '.' + df['semestre'].astype(str)

# --- Linha NACIONAL: total de todas as regiões para cada área CINE ---
df_nacional = (
    df.groupby(['ano', 'semestre', 'nome_cine_area_geral'], as_index=False)
    .mean(numeric_only=True)
)
df_nacional['regiao'] = 'Nacional'
df_nacional['periodo'] = df_nacional['ano'].astype(str) + '.' + df_nacional['semestre'].astype(str)

# --- Linha TOTAL: total de todas as áreas e regiões (única linha global) ---
df_total = (
    df.groupby(['ano', 'semestre'], as_index=False)
    .mean(numeric_only=True)
)
df_total['regiao'] = 'Total'
df_total['nome_cine_area_geral'] = 'Todas as Áreas do CINE'
df_total['periodo'] = df_total['ano'].astype(str) + '.' + df_total['semestre'].astype(str)

# --- Unir tudo ---
df_completo = pd.concat([df, df_nacional, df_total], ignore_index=True)

# --- Lista das taxas ---
taxas = [
    'taxa_inscricao',
    'taxa_aprovacao_por_inscritos',
    'taxa_aprovacao_por_candidato',
    'taxa_ocupacao',
    'taxa_conversao_inscritos',
    'taxa_conversao_candidatos',
    'taxa_inscritos_capacitados',
    'taxa_candidatos_capacitados'
]

# --- Converter para porcentagem ---
df_completo[taxas] = df_completo[taxas] * 100

# --- Pasta base para os gráficos ---
base_dir = "./graficos_analise_taxas"
os.makedirs(base_dir, exist_ok=True)

# --- Cores por região ---
cores = {
    'Norte': '#1f77b4',
    'Nordeste': '#ff7f0e',
    'Centro-Oeste': '#2ca02c',
    'Sudeste': '#d62728',
    'Sul': '#9467bd',
    'Nacional': '#000000',     # Preto
    'Total': '#808080'         # Cinza
}

# --- Estilos de linha (para evitar erro) ---
dashes = {
    'Norte': '',
    'Nordeste': '',
    'Centro-Oeste': '',
    'Sudeste': '',
    'Sul': '',
    'Nacional': (3, 2),  # Pontilhado curto
    'Total': (5, 3)      # Tracejado longo
}

sns.set_theme(style="whitegrid", palette="deep")

# --- Loop para gerar e salvar gráficos ---
for taxa in taxas:
    taxa_dir = os.path.join(base_dir, taxa)
    os.makedirs(taxa_dir, exist_ok=True)

    for area in df['nome_cine_area_geral'].unique():
        df_area = df_completo[
            df_completo['nome_cine_area_geral'].isin([area, 'Todas as Áreas do CINE'])
        ]

        plt.figure(figsize=(8, 5))

        # Plot principal
        g = sns.lineplot(
            data=df_area,
            x='periodo',
            y=taxa,
            hue='regiao',
            style='regiao',
            dashes=dashes,
            palette=cores,
            markers=True,
            linewidth=2.2
        )

        # Aumentar espessura das linhas “Nacional” e “Total”
        for line, label in zip(g.lines, g.get_legend_handles_labels()[1]):
            if label in ['Nacional', 'Total']:
                line.set_linewidth(3)

        plt.title(f"Evolução temporal - {taxa}\nÁrea CINE: {area}", fontsize=14, weight='bold')
        plt.xlabel('Ano.Semestre')
        plt.ylabel('Valor da taxa (%)')  # <-- agora mostra que está em %
        plt.xticks(rotation=45)
        plt.legend(title='Região', bbox_to_anchor=(1.02, 1), loc='upper left')
        plt.tight_layout()

        # Caminho do arquivo
        file_name = f"grafico_{area.replace('/', '_').replace(' ', '_')}.png"
        file_path = os.path.join(taxa_dir, file_name)
        plt.savefig(file_path, dpi=300, bbox_inches='tight')
        plt.close()

print("✅ Gráficos gerados e salvos em ./graficos_analise_taxas/ (valores em %)")

# %%
