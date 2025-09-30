# %%
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.ticker import FuncFormatter
import os

path='../../../../planilhas/COMP DF_funil 12 etapas.csv'

df=pd.read_csv(path)

colunasnot=['Nome do Curso','UF do Local de Oferta','Ano','Semestre']

colunas=[coluna for coluna in df.columns.to_list() if coluna not in colunasnot]

df2=df.groupby(['Ano','Semestre'],as_index=False)[colunas].sum()

df2.columns.to_list()



# --- PREPARAÇÃO DOS DADOS PARA PLOTAGEM ---
df2['periodo'] = df2['Ano'].astype(int).astype(str) + '-' + df2['Semestre'].astype(int).astype(str)
etapas_do_funil = [col for col in df2.columns if col not in ['Ano', 'Semestre', 'periodo']]
df_plot = df2.melt(
    id_vars='periodo', 
    value_vars=etapas_do_funil,
    var_name='Etapa do Funil', 
    value_name='Quantidade'
)

# --- GERAÇÃO DO GRÁFICO DE BARRAS AGRUPADAS ---
plt.figure(figsize=(22, 12))
sns.set_theme(style="whitegrid")
ax = sns.barplot(
    data=df_plot,
    x='Etapa do Funil', 
    y='Quantidade',
    hue='periodo',
    palette='viridis'
)

# --- FORMATAÇÃO E TÍTULOS ---
ax.set_title('Funil de Seleção Detalhado para Cursos de Computação (Agregado)', fontsize=20)
ax.set_xlabel('Etapa do Processo', fontsize=14)
ax.set_ylabel('Quantidade (Escala Normal)', fontsize=14)
plt.xticks(rotation=45, ha='right', fontsize=12)
plt.yticks(fontsize=12)
ax.get_yaxis().set_major_formatter(FuncFormatter(lambda x, p: format(int(x), ',')))
plt.legend(title='Período', fontsize=12)
plt.tight_layout()

# --- SALVANDO A IMAGEM ---
pasta_saida = '../GRAFICOS/FUNIL 5 E 12 ETAPAS CURSOS COMP regiao'
os.makedirs(pasta_saida, exist_ok=True)
caminho_salvar = os.path.join(pasta_saida, 'funil_detalhado_computacao_agregado.png')
plt.savefig(caminho_salvar, dpi=300)

plt.show()
# %%