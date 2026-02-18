# %%
import pandas as pd
import numpy as np

# 1. Configurações Visuais
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', 1000)
pd.set_option('display.float_format', '{:.2f}'.format)

# 2. Carregamento dos Dados
caminho_arquivo = '../../../planilhas/limpo/modulo_3/limpar_e_padronizar_colunas/inscritos_limpo.csv'
try:
    df = pd.read_csv(caminho_arquivo)
except FileNotFoundError:
    df = pd.read_csv('inscritos_limpo.csv')

# 3. Filtros (Cenário Real)
df = df[(df['opcao_curso'] == 1) & (df['modalidade_fies'] == 'Modalidade I')]

# 4. Tratamento de Área
df['nome_cine_area_geral'] = df['nome_cine_area_geral'].fillna('Outras Áreas')

# 5. Faixas de Renda (Mantendo a estrutura de 6 faixas)
bins_renda = [0, 600, 1200, 1800, 2400, 3000, 10000]
labels_renda = [
    '1. Renda 0 - 600', 
    '2. Renda 601 - 1200', 
    '3. Renda 1201 - 1800', 
    '4. Renda 1801 - 2400', 
    '5. Renda 2401 - 3000', 
    '6. Renda > 3000'
]
df['Faixa Renda'] = pd.cut(df['renda_per_capita'], bins=bins_renda, labels=labels_renda)

# 6. DEFINIÇÃO DOS 6 NÍVEIS DE NOTA (Escala Expressiva de 150 pontos)
df['gap'] = df['media_enem'] - df['nota_corte_gp']

# Intervalos: 
# < -150 | -150 a -50 | -50 a 0 | 0 a 50 | 50 a 150 | > 150
bins_gap = [-1000, -150, -50, 0, 50, 150, 1000]

labels_gap = [
    '6. Nota Muito Inferior ao Corte (Gap < -150)',
    '5. Nota Inferior ao Corte (Gap -150 a -50)',
    '4. Nota Pouco Inferior ao Corte (Gap -50 a 0)',
    '3. Nota Pouco Superior ao Corte (Gap 0 a +50)',
    '2. Nota Superior ao Corte (Gap +50 a +150)',
    '1. Nota Muito Superior ao Corte (Gap > +150)'
]

df['Nivel_Nota'] = pd.cut(df['gap'], bins=bins_gap, labels=labels_gap)

# 7. Classificação de Status Formal
def classificar_status(status):
    if status == 'CONTRATADA':
        return 'Contratado'
    elif status in ['NÃO CONTRATADO', 'REJEITADA PELA CPSA', 'PARTICIPACAO CANCELADA PELO CANDIDATO', 'INSCRIÇÃO POSTERGADA']:
        return 'Pré-Selecionado (Não Contratou)'
    elif status == 'LISTA DE ESPERA':
        return 'Lista de Espera'
    else:
        return 'Outros'

df['Status_Resumo'] = df['situacao_fies'].apply(classificar_status)

# 8. Agrupamento Final (Área -> Renda -> Nível Nota Expressivo)
analise_6_niveis = df.groupby(
    ['nome_cine_area_geral', 'Faixa Renda', 'Nivel_Nota'], 
    observed=True
).agg(
    # Quantidade
    Total_Inscritos=('id_estudante', 'count'),
    
    # Destino dos Candidatos
    Qtd_Contratados=('Status_Resumo', lambda x: (x == 'Contratado').sum()),
    Qtd_Pre_Selecionados_Nao_Contrataram=('Status_Resumo', lambda x: (x == 'Pré-Selecionado (Não Contratou)').sum()),
    Qtd_Lista_Espera=('Status_Resumo', lambda x: (x == 'Lista de Espera').sum()),
    
    # Indicadores Financeiros
    Media_Perc_Financiamento=('percentual_financiamento', 'mean'),
    Media_Semestres=('qtde_semestre_financiado', 'mean')

).reset_index()

# 9. Limpeza (Remover linhas vazias)
analise_6_niveis = analise_6_niveis[analise_6_niveis['Total_Inscritos'] > 0]

# Renomear colunas para o relatório final
analise_6_niveis.columns = [
    'Área do Conhecimento', 
    'Faixa de Renda', 
    'Nível da Nota (Gap)', 
    'Total Candidatos', 
    'Qtd. Contratados', 
    'Qtd. Barrados Burocracia', 
    'Qtd. Lista Espera', 
    'Média % Financiamento', 
    'Média Semestres'
]

# Exibição
analise_6_niveis
# %%
pathsave= '../../../planilhas/processado/modulo_5/quem_ocupa_vaga/analise_quem_ocupa_vaga.csv'
analise_6_niveis.to_csv(pathsave,index=False)

# %%
