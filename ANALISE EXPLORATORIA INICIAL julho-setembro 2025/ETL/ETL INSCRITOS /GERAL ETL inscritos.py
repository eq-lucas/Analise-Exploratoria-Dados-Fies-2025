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


# 1. Garante que a coluna de renda é numérica (necessário para a comparação)
df4['Renda mensal bruta per capita'] = pd.to_numeric(
    df4['Renda mensal bruta per capita'].astype(str).str.replace(',', '.'), 
    errors='coerce'
)

# 2. Define as condições baseadas no Ano e na Renda
condicoes = [
    (df4['Ano'] == 2019) & (df4['Renda mensal bruta per capita'] <= 2994.00),
    (df4['Ano'] == 2019) & (df4['Renda mensal bruta per capita'] > 2994.00) & (df4['Renda mensal bruta per capita'] <= 4990.00),
    (df4['Ano'] == 2020) & (df4['Renda mensal bruta per capita'] <= 3135.00),
    (df4['Ano'] == 2020) & (df4['Renda mensal bruta per capita'] > 3135.00) & (df4['Renda mensal bruta per capita'] <= 5225.00),
    (df4['Ano'] == 2021) & (df4['Renda mensal bruta per capita'] <= 3300.00)
]

# 3. Define as respostas para cada condição
respostas = ['FIES', 'P-FIES', 'FIES', 'P-FIES', 'FIES']

# a posicao repostas[0] corerpsonde a primeria linah de condicao ali o primeiro parenteses... entendeu?

# 4. Cria a nova coluna usando np.select, com o default ajustado para 'Eliminado'
df4['possivel_candidato'] = np.select(condicoes, respostas, default='eliminado')


df4

# %%
df4.to_csv('../../../planilhas ETL/GERAL ETL inscritos.csv',index=False)

# %%