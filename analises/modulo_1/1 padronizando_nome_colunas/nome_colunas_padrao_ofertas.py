# %%
import pandas as pd
import os

path= '../../../planilhas/bruto/sem_duplicata/'

lista_semDuplicatas= os.listdir(path=path)


lista_nome_colunas= [] 


for arquivo in lista_semDuplicatas:
    
    if arquivo.endswith('.csv') and 'ofertas' in arquivo:

        caminho_csv= os.path.join(path,arquivo)

        df_colunas=pd.read_csv(caminho_csv,nrows=1)


        colunas_do_df= df_colunas.columns.str.strip().to_list()

        lista_nome_colunas.append(colunas_do_df)

# display(lista_nome_colunas)



import pandas as pd
import os
import re # Importa a biblioteca de Regular Expressions

# --- 1. O MAPA DE PADRONIZAÇÃO (Atualizado) ---
# As chaves agora estão "limpas" (sem espaços extras no meio)
MAPA_RENOMEAR_OFERTAS = {
    'Ano': 'ano',
    'Semestre': 'semestre',
    'Nome Mantenedora': 'nome_mantenedora',
    'Código e-MEC da Mantenedora': 'codigo_e_mec_mantenedora',
    'CNPJ da mantenedora': 'cnpj_mantenedora',
    'Nome da IES': 'nome_ies',
    'Código e-MEC da IES': 'codigo_e_mec_ies',
    'Organização Acadêmica da IES': 'organizacao_academica_ies',
    'UF da IES': 'uf_ies',
    'Município da IES': 'municipio_ies',
    'Nome do Local de oferta': 'nome_local_oferta',
    'Código do Local de Oferta': 'codigo_local_oferta',
    'Município do Local de Oferta': 'municipio_local_oferta',
    'UF do Local de Oferta': 'uf_local_oferta',
    'Nome da Microrregião': 'nome_microrregiao',
    'Código da Microrregião': 'codigo_microrregiao',
    'Código da Mesorregião': 'codigo_mesorregiao',
    'Nome da Mesorregião': 'nome_mesorregiao',
    'Área do conhecimento': 'area_conhecimento',
    'Subárea do conhecimento': 'subarea_conhecimento',
    'Código do Grupo de Preferência': 'codigo_grupo_preferencia',
    'Nota de Corte Grupo Preferência': 'nota_corte_grupo_preferencia', # Chave limpa
    'Código do Curso': 'codigo_curso',
    'Nome do Curso': 'nome_curso',
    'Turno': 'turno',
    'Grau': 'grau',
    'Conceito': 'conceito',
    'Vagas autorizadas e-mec': 'vagas_autorizadas_e_mec',
    'Vagas ofertadas FIES': 'vagas_ofertadas_fies',
    'Vagas além da Oferta': 'vagas_alem_da_oferta',
    'Vagas ocupadas': 'vagas_ocupadas',
    'Participa do P-FIES': 'participa_p_fies',
    'Vagas Ofertadas P-FIES': 'vagas_ofertadas_p_fies',
    
    # Chaves limpas (só 1 espaço)
    'BANCO NORDESTE BRASIL (004)': 'banco_nordeste_brasil_004', 
    'ITAU UNIBANCO (PRAVALER)(341)': 'itau_unibanco_pravaler_341',
    'BV FINANCEIRA (PRAVALER)(455)': 'bv_financeira_pravaler_455',
    'BANCO ANDBANK (PRAVALER)(65)': 'banco_andbank_pravaler_65',
    'BANCO DA AMAZONIA S.A. (003)': 'banco_amazonia_sa_003', 
    
    'Valor bruto do curso': 'valor_bruto_curso', # Chave limpa
    'Índice de correção - IPCA': 'indice_correcao_ipca', # Chave limpa

    # As duas variações apontam para o mesmo nome limpo
    'Valor do curso para FIES': 'valor_curso_fies', 
    'Valor do curso para o FIES': 'valor_curso_fies', 
    
    **{f'{i} Semestre Bruto': f'semestre_{i}_bruto' for i in range(1, 13)}, # Chaves limpas
    **{f'{i} Semestre FIES': f'semestre_{i}_fies' for i in range(1, 13)}, # Chaves limpas
}

# --- 2. SCRIPT CORRIGIDO ---

path_bruto = '../../../planilhas/bruto/sem_duplicata/'
path_limpo = '../../../planilhas/limpo/modulo_1/ofertas'
os.makedirs(path_limpo, exist_ok=True) 

lista_semDuplicatas = os.listdir(path_bruto)

print(f"Iniciando processo... Lendo de: {path_bruto}")
print(f"Salvando arquivos limpos em: {path_limpo}\n")

arquivos_processados = 0

for arquivo in lista_semDuplicatas:
    if arquivo.endswith('.csv') and 'ofertas' in arquivo:
        caminho_csv = os.path.join(path_bruto, arquivo)
        
        try:
            # 1. Carrega o arquivo
            df_temp = pd.read_csv(caminho_csv, low_memory=False) 
            
            # --- 2. LIMPEZA DOS NOMES DAS COLUNAS (A NOVA ETAPA) ---
            novas_colunas = []
            for col in df_temp.columns:
                col_limpa = str(col).strip() # 2a. Tira espaços do início e fim
                col_limpa = re.sub(r'\s+', ' ', col_limpa) # 2b. Substitui espaços múltiplos por um único espaço
                novas_colunas.append(col_limpa)
            
            df_temp.columns = novas_colunas # Define as colunas limpas
            
            # --- 3. REMOÇÃO DO LIXO (UNNAMED) ---
            # Filtra para manter apenas colunas que NÃO contenham 'unnamed' (ignorando maiúsculas)
            colunas_para_manter = [
                col for col in df_temp.columns 
                if 'unnamed' not in col.lower()
            ]
            df_temp = df_temp[colunas_para_manter] # Filtra o DF
            
            # --- 4. APLICA O MAPA DE RENOMEAÇÃO ---
            # Agora o mapa vai encontrar as chaves limpas
            df_temp.rename(columns=MAPA_RENOMEAR_OFERTAS, inplace=True)
            
            # --- 5. ADICIONA O SUFIXO '_ofertas' ---
            # .columns não é uma lista, é um Index. Temos que reatribuir.
            df_temp.columns = [f"{col}_ofertas" for col in df_temp.columns]
            
            # --- 6. GERA O NOVO NOME E SALVA COMO .CSV ---
            nome_base_limpo = arquivo.replace('_sem_duplicata.csv', '') 
            nome_arquivo_saida = f"{nome_base_limpo}_limpo.csv"
            caminho_saida = os.path.join(path_limpo, nome_arquivo_saida)
            
            df_temp.to_csv(caminho_saida, index=False, encoding='utf-8-sig')
            
            print(f"OK: '{arquivo}' -> salvo como '{nome_arquivo_saida}'")
            arquivos_processados += 1

        except pd.errors.EmptyDataError:
            print(f"AVISO: O arquivo '{arquivo}' está vazio e foi ignorado.")
        except Exception as e:
            print(f"ERRO: Ao processar '{arquivo}': {e}")


print(f"\n--- Processo concluído! ---")
print(f"Total de {arquivos_processados} arquivos de 'ofertas' foram limpos e salvos em {path_limpo}")
# %%

import pandas as pd
import os

path= '../../../planilhas/limpo/modulo_1/ofertas'

lista_semDuplicatas= os.listdir(path=path)


lista_nome_colunas= []


for arquivo in lista_semDuplicatas:
    
    if arquivo.endswith('.csv') and 'ofertas' in arquivo:

        caminho_csv= os.path.join(path,arquivo)

        df_colunas=pd.read_csv(caminho_csv,nrows=1)


        colunas_do_df= df_colunas.columns.str.strip().to_list()

        lista_nome_colunas.append(colunas_do_df)

display(lista_nome_colunas)

# %%
