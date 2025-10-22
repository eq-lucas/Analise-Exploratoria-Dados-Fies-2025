# o objetivo deste, eh que , para o FIES eh necessario voce atender certos requisitos
# para tal logo faremos uma criacao de nova coluna chamada filtro_renda_fies
# q analisa POR ano de cada linha se tal linha atende as condicoes necessarias de renda deste respectivo ano
# ou seja ter ate  salarios minimo atraves da coluna:  'renda_mensal_bruta_per_capita'




# %%
import numpy as np
import pandas as pd

path_save= '../../../planilhas/limpo/modulo_2/inscritos_coluna_filtro_renda/1 inscritos_coluna_passou_peneira_renda.csv'

path_inscritos= '../../../planilhas/limpo/modulo_2/ajustar_nan_cine_inscritos/inscritos_agrupado_limpo_CORRIGIDO.csv'


df= pd.read_csv(path_inscritos,encoding='utf-8-sig')

# 1. Garante que a coluna de renda é numérica (necessário para a comparação)
df['renda_mensal_bruta_per_capita_inscricao'] = pd.to_numeric(
    df['renda_mensal_bruta_per_capita_inscricao'].astype(str).str.replace(',', '.'), 
    errors='coerce'
)










# --- BLOCo DE VERIFICAÇÃO "ANTES" ---
print("\n--- ANÁLISE PRÉ-CRIAÇÃO DA COLUNA ---")

# Define os limites de renda APENAS para o 'FIES' (<= 3 SM)
limites_fies = {
    2019: 2994.00,
    2020: 3135.00,
    2021: 3300.00
}

# Mapeia o limite FIES para cada linha baseado no seu ano
# Linhas com anos != (2019, 2020, 2021) receberão NaN
df2=df
df2['limite_temp'] = df['ano_processo_seletivo_inscricao'].map(limites_fies)

# O filtro "Não FIES" (P-FIES ou Eliminado) pega quem:
# 1. Tem renda ACIMA do limite FIES (será P-FIES ou Eliminado)
# 2. Tem renda Nula (será Eliminado)
# 3. O ano não está nos nossos limites (ex: 2018, será Eliminado)
filtro_nao_fies_antes = (
    (df2['renda_mensal_bruta_per_capita_inscricao'] > df2['limite_temp']) |
    (df2['renda_mensal_bruta_per_capita_inscricao'].isna()) |
    (df2['limite_temp'].isna())
)

print("Contagem 'ANTES' de 'Não FIES' (P-FIES + Eliminados) por ano:")
print(df2[filtro_nao_fies_antes]['ano_processo_seletivo_inscricao'].value_counts().sort_index())

# Limpa a coluna temporária
df2 = df2.drop(columns=['limite_temp'])
print("---------------------------------------\n")
# --- FIM DO BLOCo "ANTES" ---










# 2. Define as condições baseadas no ano_processo_seletivo_inscricao e na Renda
condicoes = [
    (df['ano_processo_seletivo_inscricao'] == 2019) & (df['renda_mensal_bruta_per_capita_inscricao'] <= 2994.00),
    (df['ano_processo_seletivo_inscricao'] == 2019) & (df['renda_mensal_bruta_per_capita_inscricao'] > 2994.00) & (df['renda_mensal_bruta_per_capita_inscricao'] <= 4990.00),
    (df['ano_processo_seletivo_inscricao'] == 2020) & (df['renda_mensal_bruta_per_capita_inscricao'] <= 3135.00),
    (df['ano_processo_seletivo_inscricao'] == 2020) & (df['renda_mensal_bruta_per_capita_inscricao'] > 3135.00) & (df['renda_mensal_bruta_per_capita_inscricao'] <= 5225.00),
    (df['ano_processo_seletivo_inscricao'] == 2021) & (df['renda_mensal_bruta_per_capita_inscricao'] <= 3300.00)
]

# 3. Define as respostas para cada condição
respostas = ['FIES', 'P-FIES', 'FIES', 'P-FIES', 'FIES']

# a posicao repostas[0] corerpsonde a primeria linah de condicao ali o primeiro parenteses... entendeu?

# 4. Cria a nova coluna usando np.select, com o default ajustado para 'Eliminado'
df['possivel_candidato'] = np.select(condicoes, respostas, default='eliminado')

display(df[['renda_mensal_bruta_per_capita_inscricao','possivel_candidato']]) #type: ignore


df.to_csv(path_save,index=False)



# --- BLOCo DE VERIFICAÇÃO "DEPOIS" ---
print("\n--- ANÁLISE PÓS-CRIAÇÃO DA COLUNA ---")

# 1. Mostra o resumo completo da nova coluna
print("Contagem 'DEPOIS' (Resumo completo por Ano e Categoria):")
contagem_depois = df.groupby('ano_processo_seletivo_inscricao')['possivel_candidato'].value_counts().sort_index()
print(contagem_depois)

# 2. Mostra a soma de "Não FIES" (para comparar com o "ANTES")
print("\nContagem 'DEPOIS' de 'Não FIES' (P-FIES + Eliminados) por ano:")
# Filtra pela nova coluna
filtro_nao_fies_depois = (
    (df['possivel_candidato'] == 'P-FIES') | 
    (df['possivel_candidato'] == 'eliminado')
)
print(df[filtro_nao_fies_depois]['ano_processo_seletivo_inscricao'].value_counts().sort_index())
print("---------------------------------------\n")
# --- FIM DO BLOCo "DEPOIS" ---









# %%
