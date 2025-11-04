# %% Taxas FIES - Barras empilhadas (por região) e agrupadas (por período)
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# --- 1. Ler arquivo ---
path_taxas_regiao = '../../../planilhas/processado/modulo_4/taxas_por_uf_regiao_cine/taxas_por_regiao.csv'
df = pd.read_csv(path_taxas_regiao)

# --- 2. Criar coluna de período ---
df['periodo'] = df['ano'].astype(str) + '.' + df['semestre'].astype(str)

# --- 3. Definir colunas e nomes curtos ---
colunas_taxas = [
    'taxa_inscricao',
    'taxa_aprovacao_por_inscritos',
    'taxa_aprovacao_por_candidato',
    'taxa_ocupacao',
    'taxa_conversao_inscritos',
    'taxa_conversao_candidatos',
    'taxa_inscritos_capacitados',
    'taxa_candidatos_capacitados'
]

nomes_curto = {
    'taxa_inscricao': 'Taxa Inscrição',
    'taxa_aprovacao_por_inscritos': 'Aprovação Inscritos',
    'taxa_aprovacao_por_candidato': 'Aprovação Candidatos',
    'taxa_ocupacao': 'Ocupação',
    'taxa_conversao_inscritos': 'Conversão Inscritos',
    'taxa_conversao_candidatos': 'Conversão Candidatos',
    'taxa_inscritos_capacitados': 'Inscr. Capacit.',
    'taxa_candidatos_capacitados': 'Cand. Capacit.'
}

# --- 4. Parâmetros básicos ---
areas = sorted(df['nome_cine_area_geral'].unique())
periodos = sorted(df['periodo'].unique())
regioes = sorted(df['regiao'].unique())
largura_barra = 0.12
cores_regioes = plt.cm.Paired(np.linspace(0, 1, len(regioes)))  # paleta agradável

# --- 5. Gráficos por área do CINE ---
for area in areas:
    df_area = df[df['nome_cine_area_geral'] == area]

    df_area_grouped = (
        df_area.groupby(['periodo', 'regiao'])[colunas_taxas]
        .mean()
        .reset_index()
    )

    fig, ax = plt.subplots(figsize=(14, 6))
    x = np.arange(len(colunas_taxas))
    deslocamentos = np.linspace(-largura_barra * 2.5, largura_barra * 2.5, len(periodos))

    for desloc, periodo in zip(deslocamentos, periodos):
        df_periodo = df_area_grouped[df_area_grouped['periodo'] == periodo]
        base = np.zeros(len(colunas_taxas))

        for cor, regiao in zip(cores_regioes, regioes):
            valores = df_periodo[df_periodo['regiao'] == regiao][colunas_taxas]
            if valores.empty:
                valores = [0]*len(colunas_taxas)
            else:
                valores = valores.values[0]

            ax.bar(x + desloc, valores, width=largura_barra, bottom=base,
                   color=cor, label=regiao if periodo == periodos[0] else "")
            base += valores

    ax.set_xticks(x)
    ax.set_xticklabels([nomes_curto[c] for c in colunas_taxas], rotation=30, ha='right')
    ax.set_ylabel('Percentual (%)')
    ax.set_title(f'Taxas FIES – {area}', fontsize=14, fontweight='bold')
    ax.grid(axis='y', linestyle='--', alpha=0.4)
    ax.legend(title='Região', bbox_to_anchor=(1.02, 1), loc='upper left', ncol=1)

    plt.tight_layout()
    plt.show()

# --- 6. Gráfico Nacional (todas as áreas somadas) ---
df_total = df.groupby(['periodo', 'regiao'])[colunas_taxas].mean().reset_index()

fig, ax = plt.subplots(figsize=(14, 6))
x = np.arange(len(colunas_taxas))
deslocamentos = np.linspace(-largura_barra * 2.5, largura_barra * 2.5, len(periodos))
cores_regioes = plt.cm.Paired(np.linspace(0, 1, len(regioes)))

for desloc, periodo in zip(deslocamentos, periodos):
    df_periodo = df_total[df_total['periodo'] == periodo]
    base = np.zeros(len(colunas_taxas))

    for cor, regiao in zip(cores_regioes, regioes):
        valores = df_periodo[df_periodo['regiao'] == regiao][colunas_taxas]
        if valores.empty:
            valores = [0]*len(colunas_taxas)
        else:
            valores = valores.values[0]

        ax.bar(x + desloc, valores, width=largura_barra, bottom=base,
               color=cor, label=regiao if periodo == periodos[0] else "")
        base += valores

ax.set_xticks(x)
ax.set_xticklabels([nomes_curto[c] for c in colunas_taxas], rotation=30, ha='right')
ax.set_ylabel('Percentual (%)')
ax.set_title('Taxas FIES – Nacional (Todas as Áreas)', fontsize=14, fontweight='bold')
ax.grid(axis='y', linestyle='--', alpha=0.4)
ax.legend(title='Região', bbox_to_anchor=(1.02, 1), loc='upper left')

plt.tight_layout()
plt.show()

# %%
