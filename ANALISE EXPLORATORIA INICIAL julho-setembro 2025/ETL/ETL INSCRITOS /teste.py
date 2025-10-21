# %%

import pandas as pd
import os

pd.set_option('display.max_columns', None)


ano = [2019, 2020, 2021]
sem = [1, 2]

lista_DF = []


for year in ano: 
    for semestre in sem:


        caminho_inscricoes = f'../../../csv originais/inscricoes CORRIGIDAS/fies_{semestre}_inscricao_{year}.csv'

        df_bruto = pd.read_csv(caminho_inscricoes)



        mapa_nomes_corretos = {

            'ANÃLISE E DESENVOLVIMENTO DE SISTEMAS': 'ANÁLISE E DESENVOLVIMENTO DE SISTEMAS',
            'CIÊNCIAS DA COMPUTAÇÃO': 'CIÊNCIA DA COMPUTAÇÃO',
            'SISTEMA DE INFORMAÇÃO': 'SISTEMAS DE INFORMAÇÃO',
            'ENGENHARIA DE COMPUTAÇÃO': 'ENGENHARIA DA COMPUTAÇÃO'
        }

        df_bruto['Nome do curso'] = df_bruto['Nome do curso'].replace(mapa_nomes_corretos)

        df_temporario = df_bruto


        lista_DF.append(df_temporario)


df_concat = pd.concat(lista_DF, ignore_index=True)


df_organizado= df_concat


# Define a ordem de classificação, com UF em primeiro, como solicitado
desempate = [

'Ano do processo seletivo',
'Semestre do processo seletivo',
'UF do Local de Oferta',
'Cod. do Grupo de preferência',
'Código do curso',
'Turno'
]

df_organizado = df_organizado.sort_values(by=desempate, ascending=True)


df3=df_organizado.rename(columns= 
               {'Ano do processo seletivo':'Ano',
                'Semestre do processo seletivo':'Semestre'})

df3

import numpy as np

df4=df3

colunas_rendas=[
'Renda familiar mensal bruta',
'Renda mensal bruta per capita'
]

df_rendas= df4[colunas_rendas]

df_rendas[colunas_rendas].dtypes

# %%
df_rendas[colunas_rendas]
# %%
dfzao=df4
# 1. Garante que a coluna de renda é numérica (necessário para a comparação)
dfzao['Renda mensal bruta per capita'] = pd.to_numeric(
    dfzao['Renda mensal bruta per capita'].astype(str).str.replace(',', '.'), 
    errors='coerce'
)
dfzao['Renda familiar mensal bruta'] = pd.to_numeric(
    dfzao['Renda familiar mensal bruta'].astype(str).str.replace(',', '.'), 
    errors='coerce'
)

dfzao[colunas_rendas].dtypes
# %%
dfzao[colunas_rendas]
# %%
pd.set_option('display.float_format', '{:,.2f}'.format)  # mostra sempre com 2 casas decimais

dfzao[colunas_rendas].describe()

# %%
for col in colunas_rendas:
    print(f"\n--- {col} ---")
    print("Mínimo :", dfzao[col].min())
    print("Máximo :", dfzao[col].max())
    print("Média  :", dfzao[col].mean())
    print("Mediana:", dfzao[col].median())
    print("Desvio Padrão:", dfzao[col].std())
# %%
# Contar quantos têm renda per capita maior que 6000
conta_percapita = (dfzao['Renda mensal bruta per capita'] > 5325.00).sum()

# Contar quantos têm renda familiar maior que 6000
conta_familiar = (dfzao['Renda familiar mensal bruta'] > 5325.00).sum()

print("Renda per capita > 2.994:", conta_percapita)
print("Renda familiar > 2.994:", conta_familiar)

# %%
