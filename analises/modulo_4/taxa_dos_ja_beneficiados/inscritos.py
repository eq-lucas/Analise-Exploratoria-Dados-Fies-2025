# %% 
import pandas as pd


path = '../../../planilhas/limpo/modulo_3/limpar_e_padronizar_colunas/inscritos_limpo.csv'

df = pd.read_csv(path,low_memory=False)


coluna= [
'beneficiado_creduc_fies',
]

correcao={
'sim':True,
'não':False,
}

print('---O ANTES: quais os tipo de respostas---')

display(df[coluna].value_counts())#type:ignore
# para descobrir como distinct e qntas linahs tem de cada resposta

print('---O ANTES: o tipo da coluna --')

display(df[coluna].dtypes)#type:ignore




df['beneficiado_creduc_fies']= (df['beneficiado_creduc_fies']
             .str.strip()
             .str.lower()
             .map(correcao)
             .astype('boolean')) # NAO USE 'BOOL' PQ TRANSFORMA NULO EM TRUE

print('---Apos aplicar a correcao ---')

display(df[coluna])#type:ignore


print('---Qntos tipos existem---')

display(df['beneficiado_creduc_fies'].unique())#type:ignore

#df[coluna].unique() assim da erro pq o unique so vai
# para SERIES pq n tem como fazer unique em relacao
# a N colunas... isso seria o groupby q faz melhor...
# alias este unique ta fazendo papel de DISTINCT
# se quiser saber qntos tem de cada use value_counts

print('---Qntos tem no total ---')
df['beneficiado_creduc_fies'].fillna(False).value_counts()
#df['beneficiado_creduc_fies'].value_counts() #sem fillNa resultou em apenas 6 a menos



coluna_com_ano_semestre=[
    'ano',
    'semestre',
    'beneficiado_creduc_fies',
]


df_analise= (df
             .groupby(coluna_com_ano_semestre,as_index=False)
             [['beneficiado_creduc_fies']]
             .size()
             .rename(columns={'size':'qtde'}))

display(df_analise)#type: ignore
# %%
