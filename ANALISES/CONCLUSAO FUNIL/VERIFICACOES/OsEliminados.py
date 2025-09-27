# %%

import pandas as pd

path ='planilhas ETL/GERAL ETL inscritos.csv'

df = pd.read_csv(path)


filtro= df['possivel_candidato'] == 'Eliminado'


cursosComputacao = [

    'ANÁLISE E DESENVOLVIMENTO DE SISTEMAS',
    'CIÊNCIA DA COMPUTAÇÃO',
    'SISTEMAS DE INFORMAÇÃO',
    'REDES DE COMPUTADORES',
    'ENGENHARIA DA COMPUTAÇÃO',
    'ENGENHARIA DE SOFTWARE'
]

filtro_computacao = df['Nome do curso'].isin(cursosComputacao)

df = df[filtro_computacao].copy()

df.groupby(['Ano','Semestre','possivel_candidato'],as_index=False).count()

# comp =3

# tudo = 221
# %%
