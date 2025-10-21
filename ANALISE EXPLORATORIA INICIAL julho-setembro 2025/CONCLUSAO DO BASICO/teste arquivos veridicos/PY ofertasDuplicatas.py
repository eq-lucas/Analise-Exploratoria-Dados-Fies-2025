# %%
import pandas as pd

pd.set_option('display.max_columns', None)

year = [2019, 2020, 2021, 2022]
semestre = [1, 2]

ano_lista = []
semestre_lista = []
default = []
duplicata_lista= []
pk_lista=[]
tem_duplicata=[]
pk_eh_correta=[]

PK_2022 = [
    'Código e-MEC da Mantenedora',
    'Código do Local de Oferta',
    'Cód. Do Grupo de Preferência',
    'Código do Curso',
    'Turno',
]

PK = [
    'Código e-MEC da Mantenedora',
    'Código do Local de Oferta',
    'Código do Grupo de Preferência',
    'Código do Curso',
    'Turno',
        ]

for i in year:
    for j in semestre:
        if i == 2022 and j == 2:
            break

        caminho= '../../../csv originais/OFERTAS/{ano}_ofertas_{semestre}.csv'

        caminho = caminho.format(ano=i, semestre=j)

        df = pd.read_csv(caminho, sep=';', encoding='latin-1')

        ano_lista.append(i)
        semestre_lista.append(j)
        

        # ---- ofertas Bruto
        default.append(df.shape[0])


        # ---- sem duplicatas
        df_Semduplicatas = df.drop_duplicates(subset=df.columns.tolist())
        duplicata_lista.append(df_Semduplicatas.shape[0])
        duptem= not(df.shape[0]-df_Semduplicatas.shape[0] == 0)
        tem_duplicata.append(duptem)

        # ---- com PK
        if i == 2022:
            df_unicoPk = df.drop_duplicates(subset=PK_2022)
        else:
            df_unicoPk = df.drop_duplicates(subset=PK)

        pk_lista.append(df_unicoPk.shape[0])
        pkcorreta= (df_unicoPk.shape[0]- df_Semduplicatas.shape[0]) == 0
        pk_eh_correta.append(pkcorreta)

ofertas_dict_analise = {
    'ano': ano_lista,
    'semestre': semestre_lista,
    'default': default,
    'duplicata': duplicata_lista,
    'pk': pk_lista,
    'Dataset tem linhas duplicadas':tem_duplicata,
    'PK esta correta':pk_eh_correta
}

salvar = '../planilhas basico/ofertasDuplicatas.csv'

ofertas = pd.DataFrame(ofertas_dict_analise)

ofertas

# %%
ofertas.to_csv(salvar,index=False)

# %%