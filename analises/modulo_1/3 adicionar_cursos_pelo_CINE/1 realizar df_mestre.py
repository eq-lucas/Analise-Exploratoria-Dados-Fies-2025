# %%
import os
import shutil

# --- CONFIGURAÇÃO ---

# 1. Caminho base (planilhas/externo)
base_path_censos = '../../../planilhas/externo' 
destination_folder = base_path_censos 

# 2. Padrões de NOME/CAMINHO
data_subfolder = 'dados'

# 3. Nomes dos arquivos de ORIGEM (ambos serão processados)
source_filenames_templates = [
    'MICRODADOS_CADASTRO_CURSOS_{year}.CSV',
    'MICRODADOS_CADASTRO_IES_{year}.CSV'
]

# 4. Anos que você quer processar
start_year = 2016
end_year = 2024
years_to_process = range(start_year, end_year + 1)

# --- FIM DA CONFIGURAÇÃO ---

# Garante que a pasta de destino exista
if not os.path.isdir(destination_folder):
    print(f"ERRO: Pasta de destino '{destination_folder}' não encontrada. Crie-a primeiro.")
    exit()

print("\n--- 1. INICIANDO MOVIMENTAÇÃO E RENAME (Usando os.listdir) ---")

folders_to_delete = []
moved_count = 0
error_count = 0

try:
    # Lista todo o conteúdo da pasta 'planilhas/externo'
    all_items_in_base = os.listdir(base_path_censos)
except Exception as e:
    print(f"ERRO: Não foi possível ler o conteúdo de '{base_path_censos}'. Erro: {e}")
    exit()

# Loop pelos anos
for year in years_to_process:
    print(f"\n--- Processando ano: {year} ---")
    
    year_str = str(year)
    
    # 1. Encontra a pasta do ano usando 'in' (contém)
    # Procura por qualquer item que seja um diretório e contenha o ano no nome.
    matching_folders = [
        item for item in all_items_in_base 
        if year_str in item and os.path.isdir(os.path.join(base_path_censos, item))
    ]

    if not matching_folders:
        print(f"  AVISO: Nenhuma pasta encontrada para o ano {year}. Pulando.")
        continue
    
    # Assumimos que a primeira pasta encontrada é a correta para o ano
    current_year_folder_name = matching_folders[0] 
    print(f"  Pasta encontrada: {current_year_folder_name}")

    # Caminho completo da PASTA RAIZ do ano
    root_folder_to_delete = os.path.join(base_path_censos, current_year_folder_name)
    
    # Caminho completo da subpasta 'dados'
    full_data_subfolder_path = os.path.join(root_folder_to_delete, data_subfolder)

    # Adiciona a pasta raiz à lista de exclusão
    if root_folder_to_delete not in folders_to_delete:
        folders_to_delete.append(root_folder_to_delete)

    # Loop pelos dois arquivos
    for source_template in source_filenames_templates:
        
        source_filename = source_template.format(year=year)
        full_source_path = os.path.join(full_data_subfolder_path, source_filename)
        
        # Monta o destino (renomeando para .csv minúsculo)
        destination_filename = source_filename.replace('.CSV', '.csv')
        full_destination_path = os.path.join(destination_folder, destination_filename)

        # Verifica se o arquivo de ORIGEM existe
        if os.path.exists(full_source_path):
            print(f"  Arquivo encontrado: {source_filename}")
            try:
                # Move o arquivo e o renomeia
                shutil.move(full_source_path, full_destination_path)
                print(f"  >>> SUCESSO: Movido para: {full_destination_path}")
                moved_count += 1
                
            except Exception as e:
                print(f"  !!! ERRO: Falha ao mover/renomear {source_filename}. Erro: {e}")
                error_count += 1
        else:
            print(f"  AVISO: Arquivo de origem não encontrado: {source_filename}. Pulando.")


# --- 2. EXCLUSÃO DAS PASTAS ---

print("\n--- 2. INICIANDO EXCLUSÃO DAS PASTAS DE ORIGEM ---")
print("!!! ATENÇÃO: As pastas serão APAGADAS permanentemente. !!!")

deleted_count = 0
for folder_path in folders_to_delete: 
    if os.path.isdir(folder_path):
        print(f"  > Tentando apagar: {folder_path}")
        try:
            shutil.rmtree(folder_path)
            print(f"  >>> SUCESSO: Pasta apagada.")
            deleted_count += 1
        except Exception as e:
            print(f"  !!! ERRO: Não foi possível apagar a pasta {folder_path}. Erro: {e}")
            error_count += 1
        
# --- 3. RESUMO FINAL ---

print("\n--- PROCESSO COMPLETO CONCLUÍDO ---")
print(f"Arquivos movidos e renomeados: {moved_count}")
print(f"Pastas de origem apagadas: {deleted_count}")
print(f"Total de erros encontrados: {error_count}")
# %%
