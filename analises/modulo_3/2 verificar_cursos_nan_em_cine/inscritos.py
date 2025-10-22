# %%
import pandas as pd
import numpy as np

pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)

# --- 1. CAMINHO E LEITURA ---
path_inscritos_limpo = '../../../planilhas/limpo/modulo_3/limpar_e_padronizar_colunas/inscritos_limpo.csv' 

print(f"Lendo dataset: {path_inscritos_limpo}")
try:
    df = pd.read_csv(path_inscritos_limpo, low_memory=False)
    print(f"DataFrame carregado. Shape: {df.shape}\n")
except FileNotFoundError:
    print(f"!!! ERRO: Arquivo não encontrado em: {path_inscritos_limpo}")
    raise SystemExit("Arquivo de entrada não encontrado.")

# --- 2. DEFINIÇÃO DAS COLUNAS CHAVE ---
# Usar os nomes padronizados e curtos
COL_NOME_CURSO_INSCRITO = 'nome_curso'       # Nome do curso que o aluno se inscreveu (o que queremos ver)
COL_NOME_CURSO_CINE = 'nome_cine_area_geral'      # Nome do curso CINE (filtro)
COL_CODIGO_CINE = 'codigo_curso_cine'        # Código CINE (filtro)

# Garantir que as colunas existem
for col in [COL_NOME_CURSO_INSCRITO, COL_NOME_CURSO_CINE, COL_CODIGO_CINE]:
    if col not in df.columns:
        print(f"!!! ERRO: Coluna essencial '{col}' não encontrada no DataFrame.")
        print(f"Colunas disponíveis: {df.columns.to_list()}")
        raise SystemExit("Colunas CINE ausentes após renomeação.")


# --- PEDIDO 1: Quais nomes de curso têm CÓDIGO CINE (codigo_curso_cine) == NaN ---
print("\n=======================================================")
print("  PEDIDO 1: LISTA DE NOMES DE CURSO COM CÓDIGO CINE AUSENTE")
print("=======================================================")

# Filtro 1: Código CINE está faltando (NaN)
filtro_cod_cine_nan = df[COL_CODIGO_CINE].isna()

# Pega os nomes dos cursos originais e remove duplicatas para listar os títulos
cursos_sem_cod_cine = df[filtro_cod_cine_nan][COL_NOME_CURSO_INSCRITO].dropna().unique()

print(f"Total de registros com {COL_CODIGO_CINE} NaN: {filtro_cod_cine_nan.sum()}")
print(f"Total de Nomes de Curso ÚNICOS sem {COL_CODIGO_CINE}: {len(cursos_sem_cod_cine)}\n")
print(">>> LISTA DE NOMES DE CURSO (ORIGINAIS) <<<")
for nome in cursos_sem_cod_cine:
    print(f"- {nome}")
print("\n" + "=" * 50)


# --- PEDIDO 2: CÓDIGO CINE (NaN) E NOME CURSO CINE (NaN) ---
print("\n=================================================================================")
print("  PEDIDO 2: REGISTROS ONDE CÓDIGO CINE E NOME CURSO CINE ESTÃO AUSENTES (Totalmente Desconhecidos)")
print("=================================================================================")

# Filtro 2: Código CINE está faltando E o Nome do Curso CINE está faltando
filtro_duplo_cine_nan = df[COL_CODIGO_CINE].isna() & df[COL_NOME_CURSO_CINE].isna()

# Contagem e amostra para visualização
total_duplo_cine_nan = filtro_duplo_cine_nan.sum()
amostra_duplo_cine_nan = df[filtro_duplo_cine_nan]

print(f"Total de registros com {COL_CODIGO_CINE} E {COL_NOME_CURSO_CINE} NaN: {total_duplo_cine_nan}")

if total_duplo_cine_nan > 0:
    print("\nAmostra (head) dos registros. Nome do Curso Original (nome_curso) com Classificação CINE Ausente:")
    
    # Exibir a coluna NOME_CURSO_INSCRITO (o título original) e as colunas CINE (para provar que são NaN)
    display(amostra_duplo_cine_nan['nome_curso'])# type: ignore
else:
    print("\nNenhum registro encontrado onde AMBAS as informações CINE estão NaN simultaneamente.")
    
print("=" * 50)

# %%