# o objetivo deste, eh que , para o FIES eh necessario voce atender certos requisitos
# para tal logo faremos uma criacao de nova coluna chamada filtro_renda_fies
# q analisa POR ano de cada linha se tal linha atende as condicoes necessarias de renda deste respectivo ano
# ou seja ter ate  salarios minimo atraves da coluna:  'renda_mensal_bruta_per_capita'




# %%
import numpy as np
import pandas as pd

path_save= '../../../planilhas/limpo/modulo_2/inscritos_coluna_filtro_renda_regiao/1 inscritos_coluna_passou_peneira_renda.csv'

path_inscritos= '../../../planilhas/limpo/modulo_2/ajustar_nan_cine_inscritos/inscritos_agrupado_limpo_CORRIGIDO.csv'


df= pd.read_csv(path_inscritos,encoding='utf-8-sig')

print('shape antes: ',df.shape,'\n')



# 1. Garante que a coluna de renda é numérica (necessário para a comparação)
df['renda_mensal_bruta_per_capita_inscricao'] = pd.to_numeric(
    df['renda_mensal_bruta_per_capita_inscricao'].astype(str).str.replace(',', '.'), 
    errors='coerce'
)







df2=df
# --- BLOCO DE VERIFICAÇÃO "ANTES" (REVISADO PARA MODALIDADES) ---
print("\n--- ANÁLISE PRÉ-CRIAÇÃO DA COLUNA 'modalidade_fies' ---")
print("   (Calculando contagem manual de 'eliminado')")

# --- A. Definições Iniciais (Replicadas para cálculo manual) ---
# Valores do Salário Mínimo (SM) nacional por ano
salario_minimo_ano_antes = {
    2019: 998.00, 2020: 1045.00, 2021: 1100.00
}
# Limite de Renda MÁXIMO (5 SM) por ano
limite_5sm_antes = {ano: sm * 5 for ano, sm in salario_minimo_ano_antes.items()}
# Mapa UF -> Região (Necessário para garantir que a UF é válida)
mapa_uf_regiao_antes = {
    'AC': 'Norte', 'AP': 'Norte', 'AM': 'Norte', 'PA': 'Norte', 'RO': 'Norte', 'RR': 'Norte', 'TO': 'Norte',
    'AL': 'Nordeste', 'BA': 'Nordeste', 'CE': 'Nordeste', 'MA': 'Nordeste', 'PB': 'Nordeste', 'PE': 'Nordeste', 'PI': 'Nordeste', 'RN': 'Nordeste', 'SE': 'Nordeste',
    'DF': 'Centro-Oeste', 'GO': 'Centro-Oeste', 'MT': 'Centro-Oeste', 'MS': 'Centro-Oeste',
    'ES': 'Sudeste', 'MG': 'Sudeste', 'RJ': 'Sudeste', 'SP': 'Sudeste',
    'PR': 'Sul', 'RS': 'Sul', 'SC': 'Sul'
}
# Nomes das colunas
coluna_ano_antes = 'ano_processo_seletivo_inscricao'
coluna_renda_antes = 'renda_mensal_bruta_per_capita_inscricao'
coluna_uf_antes = 'uf_residencia_inscricao'

# --- B. Preparação (Temporária para o Bloco Antes) ---
# Cria cópias temporárias das colunas necessárias para o cálculo manual
df2['limite_5sm_temp_antes'] = df2[coluna_ano_antes].map(limite_5sm_antes)
df2['regiao_temp_antes'] = df2[coluna_uf_antes].map(mapa_uf_regiao_antes)

# --- C. Filtro Manual para 'eliminado' ---
# Um candidato é 'eliminado' se:
# 1. A Renda for MAIOR que o limite de 5 SM do seu ano.
# 2. OU a Renda for Nula (NaN).
# 3. OU o Ano não estiver mapeado (ex: 2018), fazendo o limite ser NaN.
# 4. OU a UF não estiver mapeada (ex: inválida), fazendo a região ser NaN.
filtro_eliminado_antes = (
    (df2[coluna_renda_antes] > df2['limite_5sm_temp_antes']) |
    (df2[coluna_renda_antes].isna()) |
    (df2['limite_5sm_temp_antes'].isna()) |
    (df2['regiao_temp_antes'].isna())
)

# --- D. Contagem e Impressão ---
print("Contagem 'ANTES' de 'eliminado' (manual) por ano:")
try:
    contagem_elim_antes = df2[filtro_eliminado_antes][coluna_ano_antes].value_counts().sort_index()
    print(contagem_elim_antes)
except KeyError as e:
     print(f"!!! ERRO no Bloco Antes: Não foi possível contar. Verifique o nome da coluna: {e}")
except Exception as e:
     print(f"!!! ERRO no Bloco Antes ao contar eliminados: {e}")


# --- E. Limpeza das Colunas Temporárias do Bloco Antes ---
df2.drop(columns=['limite_5sm_temp_antes', 'regiao_temp_antes'], inplace=True)

print("----------------------------------------------------------\n")
# --- FIM DO BLOCO "ANTES" REVISADO ---











# --- NOVO BLOCO: CLASSIFICAÇÃO POR MODALIDADE FIES (I, II, III) ---

# --- A. Definições Iniciais ---

# Valores do Salário Mínimo (SM) nacional por ano
salario_minimo_ano = {
    2019: 998.00,
    2020: 1045.00,
    2021: 1100.00
    # Adicione outros anos se o seu df tiver
}

# Limites de Renda (em R$) por ano
limite_3sm = {ano: sm * 3 for ano, sm in salario_minimo_ano.items()}
limite_5sm = {ano: sm * 5 for ano, sm in salario_minimo_ano.items()}

# Mapeamento UF -> Região (Apenas N, NE, CO são relevantes para Mod II)
# (Pode completar com Sul/Sudeste se quiser a coluna Região completa)
mapa_uf_regiao = {
    'AC': 'Norte', 'AP': 'Norte', 'AM': 'Norte', 'PA': 'Norte', 'RO': 'Norte', 'RR': 'Norte', 'TO': 'Norte',
    'AL': 'Nordeste', 'BA': 'Nordeste', 'CE': 'Nordeste', 'MA': 'Nordeste', 'PB': 'Nordeste', 'PE': 'Nordeste', 'PI': 'Nordeste', 'RN': 'Nordeste', 'SE': 'Nordeste',
    'DF': 'Centro-Oeste', 'GO': 'Centro-Oeste', 'MT': 'Centro-Oeste', 'MS': 'Centro-Oeste',
    'ES': 'Sudeste', 'MG': 'Sudeste', 'RJ': 'Sudeste', 'SP': 'Sudeste',
    'PR': 'Sul', 'RS': 'Sul', 'SC': 'Sul'
}

# Nomes exatos das colunas no seu DataFrame 'df' (ANTES de renomear)
coluna_ano = 'ano_processo_seletivo_inscricao'
coluna_renda = 'renda_mensal_bruta_per_capita_inscricao'
coluna_uf = 'uf_residencia_inscricao'

# --- B. Preparação dos Dados ---

# 1. Garante que a coluna de renda é numérica
df[coluna_renda] = pd.to_numeric(
    df[coluna_renda].astype(str).str.replace(',', '.'),
    errors='coerce'
)
# 2. Garante que a coluna de ano é numérica (int)
df[coluna_ano] = pd.to_numeric(df[coluna_ano], errors='coerce').fillna(0).astype(int)

# 3. Cria coluna temporária com o limite de 3 SM do ano da linha
df['limite_3sm_ano'] = df[coluna_ano].map(limite_3sm)
# 4. Cria coluna temporária com o limite de 5 SM do ano da linha
df['limite_5sm_ano'] = df[coluna_ano].map(limite_5sm)
# 5. Cria coluna temporária com a Região do candidato
df['regiao_residencia'] = df[coluna_uf].map(mapa_uf_regiao)


# --- C. Definição das Condições (IMPORTANTE A ORDEM!) ---
condicoes_modalidade = [
    # 1. MODALIDADE I: Renda <= 3 SM (Qualquer região)
    #    (Verifica também se a renda e o limite são válidos - não NaN)
    (df[coluna_renda].notna()) & (df['limite_3sm_ano'].notna()) & \
    (df[coluna_renda] <= df['limite_3sm_ano']),

    # 2. MODALIDADE II: Renda > 3 SM E <= 5 SM E Região N/NE/CO
    #    (Verifica também se a renda, limites e região são válidos)
    (df[coluna_renda].notna()) & (df['limite_3sm_ano'].notna()) & (df['limite_5sm_ano'].notna()) & (df['regiao_residencia'].notna()) & \
    (df[coluna_renda] > df['limite_3sm_ano']) & \
    (df[coluna_renda] <= df['limite_5sm_ano']) & \
    (df['regiao_residencia'].isin(['Norte', 'Nordeste', 'Centro-Oeste'])),

    # 3. MODALIDADE III (P-FIES): Renda > 3 SM E <= 5 SM E Região S/SE
    #    (Verifica também se a renda, limites e região são válidos)
     (df[coluna_renda].notna()) & (df['limite_3sm_ano'].notna()) & (df['limite_5sm_ano'].notna()) & (df['regiao_residencia'].notna()) & \
    (df[coluna_renda] > df['limite_3sm_ano']) & \
    (df[coluna_renda] <= df['limite_5sm_ano']) & \
    (df['regiao_residencia'].isin(['Sul', 'Sudeste']))
]

# --- D. Definição das Respostas ---
respostas_modalidade = [
    'Modalidade I',
    'Modalidade II',
    'Modalidade III (P-FIES)'
]

# --- E. Criação da Nova Coluna ---
# O default 'eliminado' pega:
# - Renda > 5 SM
# - Renda NaN
# - Ano fora do mapeamento (limites NaN)
# - UF fora do mapeamento (região NaN)
df['modalidade_fies'] = np.select(condicoes_modalidade, respostas_modalidade, default='eliminado')

# --- F. Limpeza das Colunas Temporárias ---
df.drop(columns=['limite_3sm_ano', 'limite_5sm_ano'], inplace=True)

# --- G. Verificação (Opcional) ---
print("\n--- Resultado da Classificação por Modalidade ---")
print(df['modalidade_fies'].value_counts(dropna=False))
print("-------------------------------------------------\n")



display(df[['renda_mensal_bruta_per_capita_inscricao','modalidade_fies']]) #type: ignore


df.to_csv(path_save,index=False)




# --- BLOCO DE VERIFICAÇÃO FINAL (MODALIDADES) ---
print("\n--- ANÁLISE PÓS-CRIAÇÃO DA COLUNA 'modalidade_fies' ---")

# Nomes das colunas (certifique-se que são os corretos neste ponto do script)
coluna_ano_final = 'ano_processo_seletivo_inscricao' # Ou o nome renomeado se já aplicou
coluna_modalidade = 'modalidade_fies'

# 1. Mostra o resumo completo da nova coluna por ano
print("Contagem 'FINAL' (Resumo completo por Ano e Modalidade):")
try:
    contagem_final_completa = df.groupby(coluna_ano_final)[coluna_modalidade].value_counts().sort_index()
    print(contagem_final_completa)
except KeyError as e:
    print(f"!!! ERRO: Não foi possível agrupar. Verifique o nome da coluna: {e}")
    print(f"Colunas disponíveis: {df.columns.to_list()}")

# 2. Mostra a soma apenas dos 'eliminado' por ano
#    Isso ajuda a verificar se os casos de Renda > 5 SM, Renda NaN, Ano/UF fora do mapa
#    foram corretamente classificados como 'eliminado'.
print(f"\nContagem 'FINAL' apenas de '{'eliminado'}' por ano:")
try:
    filtro_eliminado = (df[coluna_modalidade] == 'eliminado')
    contagem_eliminados = df[filtro_eliminado][coluna_ano_final].value_counts().sort_index()
    print(contagem_eliminados)
except KeyError as e:
     print(f"!!! ERRO: Não foi possível filtrar/contar. Verifique o nome da coluna: {e}")
except Exception as e:
     print(f"!!! ERRO ao contar eliminados: {e}")

print("----------------------------------------------------------\n")
# --- FIM DO BLOCO DE VERIFICAÇÃO FINAL ---
# %%







