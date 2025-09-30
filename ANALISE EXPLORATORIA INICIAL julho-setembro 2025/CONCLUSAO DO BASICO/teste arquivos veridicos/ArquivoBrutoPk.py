# %%

import pandas as pd


path1= '../../../csv originais/INSCRICOES/2019_inscricoes_1.csv'

df1= pd.read_csv(path1,sep=';',encoding='latin-1')

path2= '../../../csv originais/inscricoes CORRIGIDAS/fies_1_inscricao_2019.csv'

df2= pd.read_csv(path2)



years=[2019,2020,2021]
sem=[1,2]

lista_shapes=[]
lista_shapes_pk=[]
lista_shapes_pk_df_limpo=[]

for ano in years:
    for semestre in sem:


        path1= f'../../../csv originais/INSCRICOES/{ano}_inscricoes_{semestre}.csv'

        df1= pd.read_csv(path1,sep=';',encoding='latin-1')


        PK= [
        'ID do estudante',
        'Opções de cursos da inscrição'
        ]


        qtdeLinhas_BRUTO_pk=df1.groupby(PK,as_index=False)['Opções de cursos da inscrição'].count()['ID do estudante'].count()

        pk_suposta_certa= df1.shape[0]-qtdeLinhas_BRUTO_pk # 868 resultou


        filtro= df1.duplicated(subset=df1.columns.to_list())

        DfCOMduplicatas= df1[filtro] 

        duplicatas= DfCOMduplicatas.shape[0] # 868 tambem


        dfSEMduplicatas= df1.drop_duplicates(subset=df1.columns.to_list())


        DF_pk_shape= dfSEMduplicatas.groupby(PK,as_index=False).agg(total=('ID do estudante','count')).shape[0]


        if pk_suposta_certa != duplicatas:
            print(f'{ano}-{semestre}: PK esta errada, com diferenca de: {pk_suposta_certa - duplicatas}')

        else:
            print(f'{ano}-{semestre}: PK TA CERTA, com diferenca de: {pk_suposta_certa - duplicatas}')

        lista_shapes.append(df1.shape[0])

        lista_shapes_pk.append(qtdeLinhas_BRUTO_pk)

        lista_shapes_pk_df_limpo.append(DF_pk_shape)

SerieShapes= pd.Series(lista_shapes)

DfShapes=pd.DataFrame()

DfShapes['Linhas Antes']= SerieShapes

DfShapes['Linhas com PK']= lista_shapes_pk

DfShapes['Linhas df limpo com pk']= lista_shapes_pk_df_limpo


DfShapes    
# %%
DfShapes.to_csv('../planilhas basico/DfShapesInscritos.csv',index=False)
# %%
