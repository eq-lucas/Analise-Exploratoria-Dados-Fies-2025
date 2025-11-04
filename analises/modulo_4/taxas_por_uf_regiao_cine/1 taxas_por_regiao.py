# %%
import pandas as pd

path = '../../../planilhas/processado/modulo_3/funil_e_candidatos_unicos/funil_por_regiao.csv'
path_salvar = '../../../planilhas/processado/modulo_4/taxas_por_uf_regiao_cine/taxas_por_regiao.csv'

df = pd.read_csv(path)

# --- 1. Agregar somando os valores base (para cada regiao, área e período) ---
colunas_base = [
    'vagas_fies',
    'Inscritos_Geral',
    'inscritos_com_nota_suficiente',
    'Candidatos_Unicos_Geral',
    'candidatos_unicos_com_nota_suficiente',
    'vagas_ocupadas'
]

df_agg = (
    df.groupby(['ano', 'semestre', 'regiao', 'nome_cine_area_geral'], as_index=False)[colunas_base]
    .sum()
)

# --- 2. Calcular taxas CORRETAMENTE a partir dos somatórios ---
df_agg['taxa_inscricao'] = df_agg['Inscritos_Geral'] / df_agg['vagas_fies']
df_agg['taxa_aprovacao_por_inscritos'] = df_agg['inscritos_com_nota_suficiente'] / df_agg['Inscritos_Geral']
df_agg['taxa_aprovacao_por_candidato'] = df_agg['candidatos_unicos_com_nota_suficiente'] / df_agg['Candidatos_Unicos_Geral']
df_agg['taxa_ocupacao'] = df_agg['vagas_ocupadas'] / df_agg['vagas_fies']
df_agg['taxa_conversao_inscritos'] = df_agg['vagas_ocupadas'] / df_agg['Inscritos_Geral']
df_agg['taxa_conversao_candidatos'] = df_agg['vagas_ocupadas'] / df_agg['Candidatos_Unicos_Geral']
df_agg['taxa_inscritos_capacitados'] = df_agg['vagas_ocupadas'] / df_agg['inscritos_com_nota_suficiente']
df_agg['taxa_candidatos_capacitados'] = df_agg['vagas_ocupadas'] / df_agg['candidatos_unicos_com_nota_suficiente']


display(df_agg)#type: ignore
# --- 3. Exportar ---
df_agg.to_csv(path_salvar, index=False)
print("✅ Taxas salvas corretamente em:", path_salvar)
# %%
