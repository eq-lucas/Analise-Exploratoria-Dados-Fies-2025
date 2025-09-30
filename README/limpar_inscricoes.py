# %%
import pandas as pd
import os

# --- 1. CONFIGURAÇÃO ---
anos = [2019, 2020, 2021]
semestres = [1, 2]

pasta_entrada = '../csv originais/INSCRICOES'
pasta_saida = '../csv originais/inscricoes CORRIGIDAS'

os.makedirs(pasta_saida, exist_ok=True)

# --- 2. LOOP DE LIMPEZA ---
for ano in anos:
    for semestre in semestres:
        # Monta o caminho do arquivo bruto
        nome_arquivo_bruto = f'{ano}_inscricoes_{semestre}.csv'
        caminho_bruto = os.path.join(pasta_entrada, nome_arquivo_bruto)

        # Monta o caminho do arquivo limpo que será salvo
        nome_arquivo_limpo = f'fies_{semestre}_inscricao_{ano}.csv'
        caminho_limpo = os.path.join(pasta_saida, nome_arquivo_limpo)

        # Lê o arquivo bruto
        df_bruto = pd.read_csv(caminho_bruto, sep=';', encoding='latin-1',decimal=',', low_memory=False)

        # Remove linhas 100% duplicadas
        df_sem_duplicatas = df_bruto.drop_duplicates(subset=df_bruto.columns.to_list())

        # Salva o DataFrame limpo no novo arquivo
        df_sem_duplicatas.to_csv(caminho_limpo, index=False)
# %%