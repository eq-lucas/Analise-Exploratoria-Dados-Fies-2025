# o objetivo deste, eh que , para o FIES eh necessario voce atender certos requisitos
# para tal logo faremos uma criacao de nova coluna chamada filtro_renda_fies
# q analisa POR ano de cada linha se tal linha atende as condicoes necessarias de renda deste respectivo ano
# ou seja ter ate  salarios minimo atraves da coluna:  'renda_mensal_bruta_per_capita'

# %%
import pandas as pd
import os


pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)

path_save= '../../../planilhas/limpo/modulo_2/inscritos_coluna_filtro_renda/inscritos_filtro_renda.csv'

path_inscritos= '../../../planilhas/limpo/modulo_2/ajustar_nan_cine_inscritos/inscritos_agrupado_limpo_CORRIGIDO.csv'

pathof = '../../../planilhas/limpo/modulo_2/ajustar_nan_cine_ofertas/ofertas_agrupado_limpo_CORRIGIDO.csv'



df = pd.read_csv(path_inscritos)

filtro_elegiveis = (df['possivel_candidato'] == 'FIES') | (df['possivel_candidato'] == 'P-FIES')

df = df[filtro_elegiveis].copy()

dfo = pd.read_csv(pathof)

# Chaves de junção para cada DataFrame
colunas_ofertas = [

'ano',
'semestre',
'codigo_grupo_preferencia',
'codigo_curso',
'turno',

]

colunas_inscricoes = [

'ano_processo_seletivo',
'semestre_processo_seletivo',
'codigo_grupo_preferencia',
'codigo_curso',
'turno',

]

colunas_necessarias_ofertas = [
    'ano',
    'semestre',
    'codigo_grupo_preferencia',
    'codigo_curso',
    'turno',
    'Participa do P-FIES'  # A única coluna extra que precisamos para o filtro
]

dfo=dfo[colunas_necessarias_ofertas].copy()

# Realiza o merge
df_verificar = df.merge(
    right=dfo,
    right_on=colunas_ofertas,
    left_on=colunas_inscricoes,
    how='inner',
    suffixes=('', '_oferta') # <-- A SOLUÇÃO ESTÁ AQUI
)  

# Cria o filtro para encontrar inconsistências
filtro_verificar = (df_verificar['possivel_candidato'] == 'P-FIES') & ((df_verificar['Participa do P-FIES'] == 'NAO') | (df_verificar['Participa do P-FIES'].isna()))

# APLICA O FILTRO CORRETO (filtro_verificar)
df_somente_quem_pertence_fies_ou_pfies = df_verificar[~filtro_verificar].copy()


# Exibe o resultado
df_final=df_somente_quem_pertence_fies_ou_pfies[df.columns.to_list()]

df_final

# %%
df_final.to_csv('../../../../planilhas/limpo/modulo_2/inscritos_coluna_filtro_renda/inscritos_coluna_fies_pfies.csv',index=False)


# %%
