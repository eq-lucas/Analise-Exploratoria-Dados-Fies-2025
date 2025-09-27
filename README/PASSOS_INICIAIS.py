# %%
import os
import shutil

# --- Lógica de Caminhos Robusta ---
# Pega o diretório onde o script atual (organizar_arquivos.py) está localizado.
# Ex: /caminho/completo/para/seu/projeto/README
script_dir = os.path.dirname(os.path.abspath(__file__))
# Define a pasta raiz do projeto, que está um nível acima da pasta README.
# Ex: /caminho/completo/para/seu/projeto
project_root = os.path.dirname(script_dir)

print(f"Raiz do projeto identificada em: {project_root}")
print("Iniciando a organização dos arquivos CSV baixados...")

# Mapeia o nome do arquivo baixado para o novo nome e a pasta de destino (relativa à raiz).
mapa_arquivos = {
    # --- Ano 2019 ---
    'relatorio_dados_abertos_oferta_12019_18102021.csv': ('2019_ofertas_1.csv', 'csv originais/OFERTAS'),
    'relatorio_dados_abertos_oferta_22019_18102021.csv': ('2019_ofertas_2.csv', 'csv originais/OFERTAS'),
    'relatorio_inscricao_dados_abertos_fies_12019.csv': ('2019_inscricoes_1.csv', 'csv originais/INSCRICOES'),
    'relatorio_inscricao_dados_abertos_fies_22019.csv': ('2019_inscricoes_2.csv', 'csv originais/INSCRICOES'),
    
    # --- Ano 2020 ---
    'relatorio_dados_abertos_oferta_12020_18102021.csv': ('2020_ofertas_1.csv', 'csv originais/OFERTAS'),
    'relatorio_dados_abertos_oferta_22020_18102021.csv': ('2020_ofertas_2.csv', 'csv originais/OFERTAS'),
    'relatorio_inscricao_dados_abertos_fies_12020.csv': ('2020_inscricoes_1.csv', 'csv originais/INSCRICOES'),
    'relatorio_inscricao_dados_abertos_fies_22020.csv': ('2020_inscricoes_2.csv', 'csv originais/INSCRICOES'),
    
    # --- Ano 2021 ---
    'relatorio_dados_abertos_oferta_12021_18102021.csv': ('2021_ofertas_1.csv', 'csv originais/OFERTAS'),
    'relatorio_dados_abertos_oferta_22021_18102021.csv': ('2021_ofertas_2.csv', 'csv originais/OFERTAS'),
    'relatorio_inscricao_dados_abertos_fies_12021.csv': ('2021_inscricoes_1.csv', 'csv originais/INSCRICOES'),
    'relatorio_inscricao_dados_abertos_fies_22021.csv': ('2021_inscricoes_2.csv', 'csv originais/INSCRICOES'),
    
    # --- Ano 2022 ---
    'relatorio_dados_abertos_oferta_12022_15072022.csv': ('2022_ofertas_1.csv', 'csv originais/OFERTAS'),

    # --- Arquivo Especial (Resultado/Erro) ---
    'relatorio_resultado_fies_12021.csv': ('resultado_fies_2020_1.csv', 'csv originais/DATASETS COM ERROS')
}

# Garante que as pastas de destino existam na raiz do projeto
os.makedirs(os.path.join(project_root, 'csv originais/OFERTAS'), exist_ok=True)
os.makedirs(os.path.join(project_root, 'csv originais/INSCRICOES'), exist_ok=True)
os.makedirs(os.path.join(project_root, 'csv originais/DATASETS COM ERROS'), exist_ok=True)

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
