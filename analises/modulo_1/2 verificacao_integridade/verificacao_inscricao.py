# %%
import pandas as pd
import os

path='../../../planilhas/limpo/modulo_1/inscricao/'



pasta_arquivos= os.listdir(path=path)

for arquivo in pasta_arquivos:


    if arquivo.endswith('.csv') and 'inscricao' in arquivo:
        caminho= os.path.join(path,arquivo)

        PK= [
            'id_estudante_inscricao',
            'opcoes_cursos_inscricao_inscricao'
            ]

        df_limpo= pd.read_csv(caminho)

        qtde_linhas_antes= df_limpo.shape[0]

        df_agrupando_por_pk= df_limpo.groupby(by=PK,as_index=False).count()

        qtde_linhas_depois= df_agrupando_por_pk.shape[0]
        
        print(f'{arquivo} antes : {qtde_linhas_antes}')
        print(f'{arquivo} depois: {qtde_linhas_depois}')

        if qtde_linhas_antes != qtde_linhas_depois:

            print('\nERRO PROVAVEL DUPLICAÇÃO DE LINHA: ')
            
            filtro= df_limpo.duplicated(subset=df_limpo.columns.to_list(),keep='first')

            linhas_duplicadas= df_limpo[filtro].shape[0]

            print(f'Total de linhas duplicadas: {linhas_duplicadas}\n')

            if linhas_duplicadas == 0:

                print('ERRO PROVAVEL LINHA VAZIA:')

                df_sem_linha_vazia= df_limpo.dropna(subset=df_limpo.columns.to_list(),how='all')

                qtde_linhas_antes= df_sem_linha_vazia.shape[0]

                df_agrupando_por_pk= df_limpo.groupby(by=PK,as_index=False).count()

                qtde_linhas_depois= df_agrupando_por_pk.shape[0]

                print(f'\n{arquivo} antes : {qtde_linhas_antes}')
                print(f'{arquivo} depois: {qtde_linhas_depois}\n')

                if qtde_linhas_antes == qtde_linhas_depois:

                    caminho_saida= os.path.join(path,arquivo)

                    df_sem_linha_vazia.to_csv(caminho_saida,index=False,encoding='utf-8')

# %%
