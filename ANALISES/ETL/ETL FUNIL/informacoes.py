# %%
import pandas as pd

path= '../../../planilhas/COMP DF_funil 11 etapas.csv'

df=pd.read_csv(path)
df
# %%
df.columns.to_list()

colunas=[
'Ano',
 'Semestre',
 'Nome do Curso',
 'UF do Local de Oferta',
 'Vagas ofertadas FIES',
 'Inscritos_Geral',
 'Inscritos_Validados',
 'Inscritos_Eliminados',
 'Candidatos_Unicos_Geral',
 'Candidatos_Unicos_Validados',
 'Candidatos_Unicos_Eliminados',
 'Inscritos_Com_Nota_Suficiente',
 'Concorrendo_Total',
 'Concorrendo_FIES',
 'Concorrendo_P_FIES',
 'Vagas ocupadas'
 ]

COLUNAS_FUNIL_GRAFICAMENTE_SERA=[

'Vagas ofertadas FIES',
'Inscritos_Geral',

'Candidatos_Unicos_Geral',

'Inscritos_Com_Nota_Suficiente',
'Concorrendo_Total',#CANDIDATOS UNICOS COM NOTA SUFICIENTE SERIA ESTE
'Vagas ocupadas'

]

# %%

cursosComputacao_QUETEMSALVOAQUI = [

'ANÁLISE E DESENVOLVIMENTO DE SISTEMAS',
'CIÊNCIA DA COMPUTAÇÃO',
'SISTEMAS DE INFORMAÇÃO',
'REDES DE COMPUTADORES',
'ENGENHARIA DA COMPUTAÇÃO',
'ENGENHARIA DE SOFTWARE'

]

# %%
