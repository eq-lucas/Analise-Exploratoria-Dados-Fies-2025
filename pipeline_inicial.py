# %%
import os
import shutil
import pandas as pd # apenas para nao executar errado este comando

# --- Lógica de Caminhos Robusta ---
# Pega o diretório onde o script atual (pipeline_inicial.py) está localizado.
script_dir = os.path.dirname(os.path.abspath(__file__))

# CORREÇÃO: Assume que a pasta do script É a raiz do projeto (pasta x).
project_root = script_dir 
# project_root = os.path.dirname(script_dir) # <- Linha antiga removida

print(f"Raiz do projeto identificada em: {project_root}")
print("Iniciando a organização dos arquivos CSV baixados...")

# Mapeia o nome do arquivo baixado para o novo nome e a pasta de destino (relativa à raiz).
mapa_arquivos = {
    # --- Ano 2019 ---
    'relatorio_dados_abertos_oferta_12019_18102021.csv': ('2019_ofertas_1.csv', 'planilhas/bruto/fonte'),
    'relatorio_dados_abertos_oferta_22019_18102021.csv': ('2019_ofertas_2.csv', 'planilhas/bruto/fonte'),
    'relatorio_inscricao_dados_abertos_fies_12019.csv': ('2019_inscricoes_1.csv', 'planilhas/bruto/fonte'),
    'relatorio_inscricao_dados_abertos_fies_22019.csv': ('2019_inscricoes_2.csv', 'planilhas/bruto/fonte'),
    
    # --- Ano 2020 ---
    'relatorio_dados_abertos_oferta_12020_18102021.csv': ('2020_ofertas_1.csv', 'planilhas/bruto/fonte'),
    'relatorio_dados_abertos_oferta_22020_18102021.csv': ('2020_ofertas_2.csv', 'planilhas/bruto/fonte'),
    'relatorio_inscricao_dados_abertos_fies_12020.csv': ('2020_inscricoes_1.csv', 'planilhas/bruto/fonte'),
    'relatorio_inscricao_dados_abertos_fies_22020.csv': ('2020_inscricoes_2.csv', 'planilhas/bruto/fonte'),
    
    # --- Ano 2021 ---
    'relatorio_dados_abertos_oferta_12021_18102021.csv': ('2021_ofertas_1.csv', 'planilhas/bruto/fonte'),
    'relatorio_dados_abertos_oferta_22021_18102021.csv': ('2021_ofertas_2.csv', 'planilhas/bruto/fonte'),
    'relatorio_inscricao_dados_abertos_fies_12021.csv': ('2021_inscricoes_1.csv', 'planilhas/bruto/fonte'),
    'relatorio_inscricao_dados_abertos_fies_22021.csv': ('2021_inscricoes_2.csv', 'planilhas/bruto/fonte'),
    
    # --- Ano 2022 ---
    'relatorio_dados_abertos_oferta_12022_15072022.csv': ('2022_ofertas_1.csv', 'planilhas/bruto/fonte'),

    # --- Arquivo Especial (Resultado/Erro) ---
    'relatorio_resultado_fies_12021.csv': ('resultado_fies_2020_1.csv', 'planilhas/bruto/com_erro')
}

# Garante que as pastas de destino existam na raiz do projeto
os.makedirs(os.path.join(project_root, 'planilhas/bruto/fonte'), exist_ok=True)
os.makedirs(os.path.join(project_root, 'planilhas/bruto/fonte'), exist_ok=True)
os.makedirs(os.path.join(project_root, 'planilhas/bruto/com_erro'), exist_ok=True)

# Itera sobre o mapa para renomear e mover os arquivos
arquivos_movidos = 0
for nome_original, (novo_nome, pasta_relativa) in mapa_arquivos.items():
    # Constrói o caminho completo a partir da raiz do projeto
    caminho_original = os.path.join(project_root, nome_original)
    caminho_destino = os.path.join(project_root, pasta_relativa, novo_nome)
    
    if os.path.exists(caminho_original):
        try:
            shutil.move(caminho_original, caminho_destino)
            print(f"SUCESSO: '{nome_original}' -> '{caminho_destino}'")
            arquivos_movidos += 1
        except Exception as e:
            print(f"ERRO ao mover '{nome_original}': {e}")
    else:
        print(f"AVISO: Arquivo '{nome_original}' não encontrado na raiz do projeto. Pulando.")

print(f"\nOrganização concluída. {arquivos_movidos} de {len(mapa_arquivos)} arquivos foram movidos.")

# %%
import pandas as pd

# --- 1. CONFIGURAÇÃO ---
anos = [2019, 2020, 2021]
semestres = [1, 2]

pasta_entrada = 'planilhas/bruto/fonte'
pasta_saida = 'planilhas/bruto/sem_duplicata'

os.makedirs(pasta_saida, exist_ok=True)

# --- 2. LOOP DE LIMPEZA ---
for ano in anos:
    for semestre in semestres:
        # Monta o caminho do arquivo bruto
        nome_arquivo_bruto = f'{ano}_inscricoes_{semestre}.csv'
        caminho_bruto = os.path.join(pasta_entrada, nome_arquivo_bruto)

        # Monta o caminho do arquivo limpo que será salvo
        nome_arquivo_limpo = f'fies_{semestre}_inscricao_{ano}_sem_duplicata.csv'
        caminho_limpo = os.path.join(pasta_saida, nome_arquivo_limpo)

        # Lê o arquivo bruto
        df_bruto = pd.read_csv(caminho_bruto, sep=';', encoding='latin-1',decimal=',', low_memory=False)

        # Remove linhas 100% duplicadas
        df_sem_duplicatas = df_bruto.drop_duplicates(subset=df_bruto.columns.to_list())

        # Salva o DataFrame limpo no novo arquivo
        df_sem_duplicatas.to_csv(caminho_limpo, index=False)

for ano in anos:
    for semestre in semestres:
        # Monta o caminho do arquivo bruto
        nome_arquivo_bruto = f'{ano}_ofertas_{semestre}.csv'
        caminho_bruto = os.path.join(pasta_entrada, nome_arquivo_bruto)

        # Monta o caminho do arquivo limpo que será salvo
        nome_arquivo_limpo = f'fies_{semestre}_ofertas_{ano}_sem_duplicata.csv'
        caminho_limpo = os.path.join(pasta_saida, nome_arquivo_limpo)

        # Lê o arquivo bruto
        df_bruto = pd.read_csv(caminho_bruto, sep=';', encoding='latin-1',decimal=',', low_memory=False)

        # Remove linhas 100% duplicadas
        df_sem_duplicatas = df_bruto.drop_duplicates(subset=df_bruto.columns.to_list())


        # Salva o DataFrame limpo no novo arquivo
        df_sem_duplicatas.to_csv(caminho_limpo, index=False)
