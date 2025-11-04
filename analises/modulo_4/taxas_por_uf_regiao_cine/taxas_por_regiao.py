# %%

import pandas as pd

path = '../../../planilhas/processado/modulo_3/funil_e_candidatos_unicos/funil_por_regiao.csv'

path_salvar= '../../../planilhas/processado/modulo_4/taxas_por_uf_regiao_cine/taxas_por_regiao.csv'

df=pd.read_csv(path)

df['taxa_inscricao'] = df['Inscritos_Geral'] / df['vagas_fies']
# ou seja qto tem de inscritos por vaga

df['taxa_aprovacao_por_inscritos'] = df['inscritos_com_nota_suficiente'] / df['Inscritos_Geral']
df['taxa_aprovacao_por_candidato'] = df['candidatos_unicos_com_nota_suficiente'] / df['Candidatos_Unicos_Geral']

df['taxa_ocupacao'] = df['vagas_ocupadas'] / df['vagas_fies']



df['taxa_conversao_inscritos']=df['vagas_ocupadas'] / df['Inscritos_Geral']
df['taxa_conversao_candidatos']=df['vagas_ocupadas'] / df['Candidatos_Unicos_Geral']

#df['taxa_conversao_inscritos_com_nota']=df['vagas_ocupadas'] / df['inscritos_com_nota_suficiente']
# NAO PODE USAR ESTE, pois nao eh necessariametne quem tem nota que esta ocupando a vaga
# porem posso usar esta metrica para calcular se tal area geral do cine ( curso ) eh buscado por alunos mais capacitados
df['taxa_inscritos_capacitados']=df['vagas_ocupadas'] / df['inscritos_com_nota_suficiente']
df['taxa_candidatos_capacitados']=df['vagas_ocupadas'] / df['candidatos_unicos_com_nota_suficiente']





# nao esquecer de fazer x100 para visualizar em porcentagem
colunas=[
'ano',
'semestre',
'nome_cine_area_geral',
'regiao',
'taxa_inscricao',
'taxa_aprovacao_por_inscritos',
'taxa_aprovacao_por_candidato',
'taxa_ocupacao',
'taxa_conversao_inscritos',
'taxa_conversao_candidatos',
'taxa_inscritos_capacitados',
'taxa_candidatos_capacitados',
]


display(df[colunas])#type:ignore

df[colunas].to_csv(path_salvar,index=False)
# %%