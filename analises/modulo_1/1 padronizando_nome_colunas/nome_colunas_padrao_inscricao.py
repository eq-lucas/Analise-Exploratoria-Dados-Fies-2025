# %%
import pandas as pd
import os

path= '../../../planilhas/bruto/sem_duplicata/'

lista_semDuplicatas= os.listdir(path=path)


lista_nome_colunas= [] 


for arquivo in lista_semDuplicatas:
    
    if arquivo.endswith('.csv') and 'inscricao' in arquivo:

        caminho_csv= os.path.join(path,arquivo)

        df_colunas=pd.read_csv(caminho_csv,nrows=1)


        colunas_do_df= df_colunas.columns.str.strip().to_list()

        lista_nome_colunas.append(colunas_do_df)

# display(lista_nome_colunas)


import pandas as pd
import os
import re # Para limpeza de espaços

# --- 1. O MAPA DE PADRONIZAÇÃO PARA "INSCRICAO" ---
# Chave = Nome Antigo / Errado
# Valor = Nome Novo / Padronizado
MAPA_RENOMEAR_INSCRICAO = {
    'Ano do processo seletivo': 'ano_processo_seletivo',
    'Semestre do processo seletivo': 'semestre_processo_seletivo',
    'Cod. do Grupo de preferência': 'codigo_grupo_preferencia',
    'Classificação': 'classificacao',
    'ID do estudante': 'id_estudante',
    'Sexo': 'sexo',
    'Data de Nascimento': 'data_nascimento',
    'UF de residência': 'uf_residencia',
    'Municipio de residência': 'municipio_residencia',
    'Etnia/Cor': 'etnia_cor',
    'Pessoa com deficiência?': 'pessoa_com_deficiencia',
    'Concluiu ensino médio escola pública': 'concluiu_ensino_medio_escola_publica',
    'Ano conclusão ensino médio': 'ano_conclusao_ensino_medio',
    'Concluiu curso superior?': 'concluiu_curso_superior',
    'Beneficiado pelo Creduc ou Fies': 'beneficiado_creduc_ou_fies',
    'Professor rede pública ensino?': 'professor_rede_publica_ensino',
    'Nº de membros Grupo Familiar': 'numero_membros_grupo_familiar',
    'Renda familiar mensal bruta': 'renda_familiar_mensal_bruta',
    'Renda mensal bruta per capita': 'renda_mensal_bruta_per_capita',
    'Região grupo de preferência': 'regiao_grupo_preferencia',
    'UF': 'uf_grupo_preferencia', # Nome ambíguo no original, nomeando como _gp
    'Cod.Microrregião': 'codigo_microrregiao',
    'Microrregião': 'microrregiao',
    'Cod.Mesorregião': 'codigo_mesorregiao',
    'Mesorregião': 'mesorregiao',
    'Conceito de curso do GP': 'conceito_curso_gp',
    'Área do conhecimento': 'area_conhecimento',
    'Subárea do conhecimento': 'subarea_conhecimento',
    'Nota Corte Grupo Preferência': 'nota_corte_grupo_preferencia',
    'Opções de cursos da inscrição': 'opcoes_cursos_inscricao',
    'Nome mantenedora': 'nome_mantenedora',
    'Natureza Jurídica Mantenedora': 'natureza_juridica_mantenedora',
    'CNPJ da mantenedora': 'cnpj_mantenedora',
    'Código e-MEC da Mantenedora': 'codigo_e_mec_mantenedora',
    'Nome da IES': 'nome_ies',
    'Código e-MEC da IES': 'codigo_e_mec_ies',
    'Organização Acadêmica da IES': 'organizacao_academica_ies',
    'Município da IES': 'municipio_ies',
    'UF da IES': 'uf_ies',
    'Nome do Local de oferta': 'nome_local_oferta',
    'Código do Local de Oferta': 'codigo_local_oferta',
    'Munícipio do Local de Oferta': 'municipio_local_oferta', # Corrigindo 'Munícipio'
    'UF do Local de Oferta': 'uf_local_oferta',
    'Código do curso': 'codigo_curso',
    'Nome do curso': 'nome_curso',
    'Turno': 'turno',
    'Grau': 'grau',
    'Conceito': 'conceito_curso', # Nomeado como _curso para diferenciar do _gp
    'Média nota Enem': 'media_nota_enem',
    'Ano do Enem': 'ano_enem',
    'Redação': 'nota_redacao',
    'Matemática e suas Tecnologias': 'nota_matematica',
    'Linguagens, Códigos e suas Tec': 'nota_linguagens',
    'Ciências Natureza e suas Tec': 'nota_ciencias_natureza',
    'Ciências Humanas e suas Tec': 'nota_ciencias_humanas',
    'Situação Inscrição Fies': 'situacao_inscricao_fies',
    'Percentual de financiamento': 'percentual_financiamento',
    'Semestre do financiamento': 'semestre_financiamento',
    'Qtde semestre financiado': 'qtde_semestre_financiado'
}

# --- 2. SCRIPT PARA CARREGAR, PADRONIZAR E SALVAR INDIVIDUALMENTE ---

# Caminho de entrada
path_bruto = '../../../planilhas/bruto/sem_duplicata/'

# --- Caminho de Saída ---
path_limpo = '../../../planilhas/limpo/modulo_1/inscricao'

# Cria o diretório de saída 'limpo/inscricao/' se ele não existir
os.makedirs(path_limpo, exist_ok=True) 

lista_semDuplicatas = os.listdir(path_bruto)

print(f"Iniciando processo... Lendo de: {path_bruto}")
print(f"Salvando arquivos limpos em: {path_limpo}\n")

arquivos_processados = 0

for arquivo in lista_semDuplicatas:
    # Filtra apenas os arquivos de INSCRICAO
    if arquivo.endswith('.csv') and 'inscricao' in arquivo:
        
        caminho_csv = os.path.join(path_bruto, arquivo)
        
        try:
            # 1. Carrega o arquivo
            df_temp = pd.read_csv(caminho_csv, low_memory=False) 
            
            # --- 2. LIMPEZA DOS NOMES DAS COLUNAS ---
            novas_colunas = []
            for col in df_temp.columns:
                col_limpa = str(col).strip() # Tira espaços do início e fim
                col_limpa = re.sub(r'\s+', ' ', col_limpa) # Substitui espaços múltiplos por um
                novas_colunas.append(col_limpa)
            
            df_temp.columns = novas_colunas # Define as colunas limpas
            
            # --- 3. REMOÇÃO DO LIXO (UNNAMED) ---
            # (Mantendo esta etapa por segurança, embora pareça não haver lixo)
            colunas_para_manter = [
                col for col in df_temp.columns 
                if 'unnamed' not in col.lower()
            ]
            df_temp = df_temp[colunas_para_manter] # Filtra o DF
            
            # --- 4. APLICA O MAPA DE RENOMEAÇÃO ---
            df_temp.rename(columns=MAPA_RENOMEAR_INSCRICAO, inplace=True)
            
            # --- 5. ADICIONA O SUFIXO '_inscricao' ---
            df_temp.columns = [f"{col}_inscricao" for col in df_temp.columns]
            
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
print(f"Total de {arquivos_processados} arquivos de 'inscricao' foram limpos e salvos em {path_limpo}")
# %%

import pandas as pd
import os

path= '../../../planilhas/limpo/modulo_1/inscricao'

lista_semDuplicatas= os.listdir(path=path)


lista_nome_colunas= []


for arquivo in lista_semDuplicatas:
    
    if arquivo.endswith('.csv') and 'inscricao' in arquivo:

        caminho_csv= os.path.join(path,arquivo)

        df_colunas=pd.read_csv(caminho_csv,nrows=1)


        colunas_do_df= df_colunas.columns.str.strip().to_list()

        lista_nome_colunas.append(colunas_do_df)

display(lista_nome_colunas)

# %%
