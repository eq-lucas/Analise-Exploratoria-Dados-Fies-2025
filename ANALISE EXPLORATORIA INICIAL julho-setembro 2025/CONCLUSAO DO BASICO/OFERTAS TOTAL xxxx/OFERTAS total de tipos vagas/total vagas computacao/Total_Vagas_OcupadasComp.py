# %%
import pandas as pd
import os

pd.set_option('display.max_columns', None)

# --- 1. CONFIGURAÇÃO (FORA DO LOOP) ---
anos = [2019, 2020, 2021]
semestres = [1, 2]

# Mapa para corrigir TODOS os nomes de cursos para um padrão único
mapa_nomes_corretos = {
    'ANÃLISE E DESENVOLVIMENTO DE SISTEMAS': 'ANÁLISE E DESENVOLVIMENTO DE SISTEMAS',
    'CIÊNCIAS DA COMPUTAÇÃO': 'CIÊNCIA DA COMPUTAÇÃO',
    'SISTEMA DE INFORMAÇÃO': 'SISTEMAS DE INFORMAÇÃO',
    'ENGENHARIA DE COMPUTAÇÃO': 'ENGENHARIA DA COMPUTAÇÃO'
}

# Lista de cursos de computação já com os nomes padronizados
cursosComputacao = [
    'ANÁLISE E DESENVOLVIMENTO DE SISTEMAS',
    'CIÊNCIA DA COMPUTAÇÃO',
    'SISTEMAS DE INFORMAÇÃO',
    'REDES DE COMPUTADORres',
    'ENGENHARIA DA COMPUTAÇÃO',
    'ENGENHARIA DE SOFTWARE'
]

lista_DF = []

# --- 2. LOOP DE PROCESSAMENTO ---
for year in anos:
    for semestre in semestres:
        caminho_ofertas = f'../../../../../csv originais/OFERTAS/{year}_ofertas_{semestre}.csv'
        
        try:
            df_bruto = pd.read_csv(caminho_ofertas, sep=';', encoding='latin-1', decimal=',')
        except FileNotFoundError:
            print(f"AVISO: Arquivo não encontrado em '{caminho_ofertas}'. Pulando.")
            continue

        # **CORREÇÃO PRINCIPAL: Padronizar os nomes AQUI, no início**
        df_bruto['Nome do Curso'] = df_bruto['Nome do Curso'].replace(mapa_nomes_corretos)
        
        # Filtra apenas para os cursos de computação
        filtro_comp = df_bruto['Nome do Curso'].isin(cursosComputacao)
        df_comp = df_bruto[filtro_comp]

        # Agrupa para somar as vagas ocupadas
        df_agrupado = df_comp.groupby('Nome do Curso', as_index=False)['Vagas ocupadas'].sum()
        
        # Adiciona as colunas de tempo para a pivotagem
        df_agrupado['ano'] = year
        df_agrupado['semestre'] = semestre
        
        lista_DF.append(df_agrupado)

# --- 3. CONSOLIDAÇÃO E PIVOTAGEM ---
df_concat = pd.concat(lista_DF, ignore_index=True)

df_pivotado = pd.pivot_table(
    data=df_concat,
    index=['ano', 'semestre'],
    columns='Nome do Curso',
    values='Vagas ocupadas',
    fill_value=0 # fill_value é mais direto que .fillna(0)
).reset_index()

df_pivotado.columns.name = None # Limpa o nome do índice das colunas

# --- 4. CÁLCULO DO TOTAL POR PERÍODO (CORRIGIDO) ---
# Seleciona apenas as colunas dos cursos para a soma
colunas_cursos = [col for col in df_pivotado.columns if col not in ['ano', 'semestre']]

# Usa axis=1 para somar ao longo das linhas (soma de todos os cursos por período)
df_pivotado['Total_Comp'] = df_pivotado[colunas_cursos].sum(axis=1)


# --- 5. EXIBIÇÃO E SALVAMENTO ---

salvar_caminho = '../../../planilhas basico/Total_Vagas_OcupadasComp_CORRIGIDO.csv'
df_pivotado.to_csv(salvar_caminho, index=False)
print(f"\nArquivo corrigido salvo em: {salvar_caminho}")
df_pivotado

# %%

# %%
