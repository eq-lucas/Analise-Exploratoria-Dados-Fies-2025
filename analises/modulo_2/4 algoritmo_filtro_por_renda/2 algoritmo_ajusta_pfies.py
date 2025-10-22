#o objetivo deste eh validar os inscritos q estao com pfies, se o curso q ele esta eh realmente pfies
# caso contrario ele eh considerado == eliminado




# %%
import pandas as pd
import os


pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)

path_save= '../../../planilhas/limpo/modulo_2/inscritos_coluna_filtro_renda/ajustado_fies_pfies_inscritos.csv'

path_inscritos= '../../../planilhas/limpo/modulo_2/inscritos_coluna_filtro_renda/1 inscritos_coluna_passou_peneira_renda.csv'

pathof = '../../../planilhas/limpo/modulo_2/ajustar_nan_cine_ofertas/ofertas_agrupado_limpo_CORRIGIDO.csv'



df = pd.read_csv(path_inscritos)

#filtro_elegiveis = (df['possivel_candidato'] == 'FIES') | (df['possivel_candidato'] == 'P-FIES')

#df = df[filtro_elegiveis].copy()



# Chaves de junção para cada DataFrame
colunas_ofertas = [

    'ano_ofertas',
    'semestre_ofertas',
    'codigo_e_mec_mantenedora_ofertas',
    'codigo_local_oferta_ofertas',
    'codigo_grupo_preferencia_ofertas',
    'codigo_curso_ofertas',
    'turno_ofertas',

]

colunas_inscricoes = [

'ano_processo_seletivo_inscricao',
'semestre_processo_seletivo_inscricao',
'codigo_e_mec_mantenedora_inscricao',
'codigo_local_oferta_inscricao',
'codigo_grupo_preferencia_inscricao',
'codigo_curso_inscricao',
'turno_inscricao',

]

colunas_necessarias_ofertas = [
    'ano_ofertas',
    'semestre_ofertas',
    'codigo_e_mec_mantenedora_ofertas',
    'codigo_local_oferta_ofertas',
    'codigo_grupo_preferencia_ofertas',
    'codigo_curso_ofertas',
    'turno_ofertas',
    'participa_p_fies_ofertas'  # A única coluna extra que precisamos para o filtro
]

dfo = pd.read_csv(pathof)

dfo=dfo[colunas_necessarias_ofertas].copy()

print('comecando merge')
# Realiza o merge
df_verificar = df.merge(
    right=dfo,
    right_on=colunas_ofertas,
    left_on=colunas_inscricoes,
    how='left',
    #suffixes=('', '_oferta') # <-- A SOLUÇÃO ESTÁ AQUI
)  
print('fim do merge')


print('comecando filtro')

# Cria o filtro para encontrar inconsistências
filtro_verificar = (df_verificar['possivel_candidato'] == 'P-FIES') & ((df_verificar['participa_p_fies_ofertas'] == 'NAO') | (df_verificar['participa_p_fies_ofertas'].isna()))
print('fim filtro')



print('comecando ajuste')

# APLICA O FILTRO CORRETO (filtro_verificar)
df_verificar.loc[filtro_verificar, 'possivel_candidato'] = 'eliminado'
print('fim ajuste')


df_final = df_verificar[df.columns.to_list()]


display(df_final.shape)#type: ignore
# %%
df_final.to_csv(path_save,index=False)


# %%
