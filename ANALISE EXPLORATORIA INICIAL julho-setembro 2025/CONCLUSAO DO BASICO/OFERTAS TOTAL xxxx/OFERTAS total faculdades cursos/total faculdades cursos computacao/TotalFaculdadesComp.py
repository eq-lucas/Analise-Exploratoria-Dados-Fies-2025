# %%
import pandas as pd

ano=[2019,2020,2021,2022]
sem=[1,2]

lista_DF=[]

for year in ano: 
    for semestre in sem:

        if year == 2022 and semestre == 2:
            break

        caminho_inscricoes= f'../../../../../csv originais/OFERTAS/{year}_ofertas_{semestre}.csv'

        df_bruto= pd.read_csv(caminho_inscricoes,
                              sep=';',
                              encoding='latin-1',
                              decimal=',')

        

        pd.set_option('display.max_columns', None)



        ordem_ofertas2022= [
        'Nome do Curso',
        'Cód. Do Grupo de Preferência',
        'Código do Curso',
        'Turno',

        ]

        ordem_ofertas= [
        'Nome do Curso',
        'Código do Grupo de Preferência',
        'Código do Curso',
        'Turno',

        ]

        vagas=[
        'Vagas autorizadas e-mec',
        'Vagas ofertadas FIES',
        'Vagas além da Oferta',
        'Vagas ocupadas'
        ]


        cursosComputacao=[
            
        'ANÃLISE E DESENVOLVIMENTO DE SISTEMAS',
        'ANÁLISE E DESENVOLVIMENTO DE SISTEMAS',
        'CIÊNCIA DA COMPUTAÇÃO',
        'CIÊNCIAS DA COMPUTAÇÃO',

        'SISTEMAS DE INFORMAÇÃO',
        'SISTEMA DE INFORMAÇÃO',

        'REDES DE COMPUTADORES',


        'ENGENHARIA DE COMPUTAÇÃO',
        'ENGENHARIA DA COMPUTAÇÃO',

        'ENGENHARIA DE SOFTWARE'

        ]

        if year == 2022:
            df_sort= (df_bruto.sort_values(by=ordem_ofertas2022,
        ascending=[True,True,True,True])) 
        else:

            df_sort= (df_bruto.sort_values(by=ordem_ofertas,
        ascending=[True,True,True,True])) 

        if year == 2020 and semestre == 1:
            df_sort=df_sort.drop_duplicates(subset=df_sort.columns.to_list())

        '''
        APENAS DE COMPUTACAO LOGO NAO COMENTAR ESTAS LINHAS
        '''
        cursosComputacao=[
            'ANÃLISE E DESENVOLVIMENTO DE SISTEMAS',
            'ANÁLISE E DESENVOLVIMENTO DE SISTEMAS',
            'CIÊNCIA DA COMPUTAÇÃO',
            'CIÊNCIAS DA COMPUTAÇÃO',
            'SISTEMAS DE INFORMAÇÃO',
            'SISTEMA DE INFORMAÇÃO',
            'REDES DE COMPUTADORES',
            'ENGENHARIA DE COMPUTAÇÃO',
            'ENGENHARIA DA COMPUTAÇÃO',
            'ENGENHARIA DE SOFTWARE'
        ]

        filtro = df_sort['Nome do Curso'].isin(cursosComputacao)
        df_temporario = df_sort[filtro].copy()


        # 2. DEPOIS DE FILTRAR, PADRONIZA OS NOMES NA TABELA RESULTANTE
        mapa_nomes_corretos = {
            'ANÃLISE E DESENVOLVIMENTO DE SISTEMAS': 'ANÁLISE E DESENVOLVIMENTO DE SISTEMAS',
            'CIÊNCIAS DA COMPUTAÇÃO': 'CIÊNCIA DA COMPUTAÇÃO',
            'SISTEMA DE INFORMAÇÃO': 'SISTEMAS DE INFORMAÇÃO',
            'ENGENHARIA DE COMPUTAÇÃO': 'ENGENHARIA DA COMPUTAÇÃO'
        }
        df_temporario['Nome do Curso'] = df_temporario['Nome do Curso'].replace(mapa_nomes_corretos)




        df_agrupar_cursos= (df_temporario.
        groupby(['Nome do Curso'],as_index=False).agg(

            TOTAL_faculdades= ('Nome do Curso','count'),
           # Total_Vagas_Ofertadas=('Vagas ofertadas FIES','sum'),
            #Total_Vagas_Ocuapdas=('Vagas ocupadas','sum'),

        ))

        df_agrupar_cursos['ano']=year

        df_agrupar_cursos['semestre']=semestre


        filtro= (df_agrupar_cursos['Nome do Curso'].isin(cursosComputacao))
        df_temporario= df_agrupar_cursos[filtro]

        lista_DF.append(df_temporario)

df_concat= pd.concat(lista_DF)


desempate=['Nome do Curso','ano','semestre']

ordem=[True,True,True]

df_organizado= (df_concat
.sort_values(by=desempate,ascending=ordem))



df_final = pd.pivot(
    data=df_organizado,
    index=['ano', 'semestre'],
    columns='Nome do Curso',
    values=['TOTAL_faculdades']#, 'Total_Vagas_Ofertadas', 'Total_Vagas_Ocuapdas']
).reset_index().fillna(0)

# --------------------------------------------------------------------
# 2. BLOCO NOVO: ACHATAR AS COLUNAS HIERÁRQUICAS
#    As colunas são tuplas (nível_0, nível_1). Vamos juntá-las com um underscore.
#    Ex: ('TOTAL_faculdades', 'CIÊNCIA DA COMPUTAÇÃO') vira 'TOTAL_faculdades_CIÊNCIA DA COMPUTAÇÃO'

df_final.columns = [f'{level_0}_{level_1}' for level_0, level_1 in df_final.columns]
# --------------------------------------------------------------------


df_final.columns.name=None

indicesCorretos={
    'ano_':'ano',
    "semestre_":"semestre"
}

df_final= df_final.rename(columns=indicesCorretos)

df_final

#def AjusarnomeErrado(x: pd.Series):
#        
#    x['ANÁLISE E DESENVOLVIMENTO DE SISTEMAS']= x['ANÃLISE E DESENVOLVIMENTO DE SISTEMAS']+x['ANÁLISE E DESENVOLVIMENTO DE SISTEMAS']
#    x['ENGENHARIA DA COMPUTAÇÃO']=  x['ENGENHARIA DA COMPUTAÇÃO']+x['ENGENHARIA DE COMPUTAÇÃO']
#    x['SISTEMAS DE INFORMAÇÃO']= x['SISTEMA DE INFORMAÇÃO']+ x['SISTEMAS DE INFORMAÇÃO']
#    x['CIÊNCIA DA COMPUTAÇÃO']= x['CIÊNCIAS DA COMPUTAÇÃO'] + x['CIÊNCIA DA COMPUTAÇÃO']
#    return x
#
#df_limpo= df_final.apply(AjusarnomeErrado,axis=1)
#
#
#colunas_erradas=[
#
#    'SISTEMA DE INFORMAÇÃO',
#    'ENGENHARIA DE COMPUTAÇÃO',
#    'ANÃLISE E DESENVOLVIMENTO DE SISTEMAS',
#    'CIÊNCIAS DA COMPUTAÇÃO',
#]
#
#
#
#df_salvar=df_limpo.drop(columns=colunas_erradas)
#df_salvar
# %%
salvar_caminho= '../../../planilhas basico/totalFaculdadesComp.csv'

df_final.to_csv(salvar_caminho,index=False)
# %%
