# %%
import pandas as pd

path= '../../../../planilhas/COMP DF_funil 12 etapas.csv'

df=pd.read_csv(path)
df

df.columns.to_list()

colunas=[
'Ano',
 'Semestre',
 'Nome do Curso',
 'UF do Local de Oferta',
 'Vagas ofertadas FIES',
 'Inscritos_Geral',
 'Inscritos_Validados',
 'Inscritos_Eliminados',
 'Candidatos_Unicos_Geral',
 'Candidatos_Unicos_Validados',
 'Candidatos_Unicos_Eliminados',
 'Inscritos_Com_Nota_Suficiente',
 'Concorrendo_Total',
 'Concorrendo_FIES',
 'Concorrendo_P_FIES',
 'Vagas ocupadas'
 ]

COLUNAS_FUNIL_GRAFICAMENTE_SERA=[

'Vagas ofertadas FIES',
'Inscritos_Geral',

'Inscritos_Com_Nota_Suficiente',

'Candidatos_Unicos_Geral',


'Concorrendo_Total',#CANDIDATOS UNICOS COM NOTA SUFICIENTE SERIA ESTE
'Vagas ocupadas'

]



cursosComputacao_QUETEMSALVOAQUI = [

'ANÁLISE E DESENVOLVIMENTO DE SISTEMAS',
'CIÊNCIA DA COMPUTAÇÃO',
'SISTEMAS DE INFORMAÇÃO',
'REDES DE COMPUTADORES',
'ENGENHARIA DA COMPUTAÇÃO',
'ENGENHARIA DE SOFTWARE'

]


# =============================================================================
# CONTINUAÇÃO DO SEU CÓDIGO
# Importações, criação da pasta e preparação para os gráficos de BARRAS
# =============================================================================
import matplotlib.pyplot as plt
import seaborn as sns
import os # Biblioteca para interagir com o sistema operacional (criar pastas)

# --- Criação da pasta para salvar os gráficos ---
output_dir = '../GRAFICOS/FUNIL 6 ETAPAS CURSOS COMP'
os.makedirs(output_dir, exist_ok=True) # Cria a pasta se ela não existir
print(f"Pasta '{output_dir}' pronta para salvar os gráficos.")

# Define um estilo visual
sns.set_style("whitegrid")

# Prepara o DataFrame para plotagem criando uma coluna 'Periodo'
df['Periodo'] = df['Ano'].astype(str) + '/' + df['Semestre'].astype(str)
print("Setup de visualização concluído.")



# =============================================================================
# 1. O FUNIL COMO TABELA (SOMA GERAL) - Mantido para referência
# =============================================================================
print("\n--- Tabela Resumo: Funil Agregado para Todos os Cursos (2019-2021) ---")
funil_total_agregado = df[COLUNAS_FUNIL_GRAFICAMENTE_SERA].sum().reset_index()
funil_total_agregado.columns = ['Etapa do Funil', 'Quantidade Total']
print(funil_total_agregado)



# =============================================================================
# 2. FUNÇÃO ATUALIZADA PARA PLOTAR E SALVAR GRÁFICOS DE BARRAS AGRUPADAS
# =============================================================================
def plotar_e_salvar_funil_barras(dataframe, titulo, nome_base_arquivo):
    """
    Esta função gera e salva um gráfico de BARRAS AGRUPADAS para o funil.
    """
    # Agrupa os dados por Período e soma as colunas do funil
    df_agg = dataframe.groupby('Periodo')[COLUNAS_FUNIL_GRAFICAMENTE_SERA].sum().reset_index()
    
    # Reorganiza o dataframe (usando .melt) para o formato ideal de plotagem
    df_melted = df_agg.melt(id_vars='Periodo', var_name='Etapa_Funil', value_name='Quantidade')
    
    # Garante que a ordem das etapas no eixo X será a que você definiu
    df_melted['Etapa_Funil'] = pd.Categorical(df_melted['Etapa_Funil'], categories=COLUNAS_FUNIL_GRAFICAMENTE_SERA, ordered=True)
    
    # Cria a figura do gráfico com uma altura maior
    plt.figure(figsize=(18, 9)) # Aumentei o tamanho para melhor visualização
    
    # !!! MUDANÇA PRINCIPAL: Usando sns.barplot para criar o gráfico de barras agrupadas !!!
    sns.barplot(
        data=df_melted,
        x='Etapa_Funil',
        y='Quantidade',
        hue='Periodo', # 'hue' cria as barras agrupadas por período
        palette='viridis'
    )
    
    # Configurações do gráfico
    plt.title(titulo, fontsize=18, weight='bold')
    plt.xlabel('Etapas do Funil de Seleção', fontsize=14)
    plt.ylabel('Quantidade', fontsize=14)
    plt.xticks(rotation=45, ha='right') # Rotaciona os nomes das etapas
    # Removida a escala logarítmica para uma visualização linear, como solicitado
    plt.tight_layout()
    
    # --- Lógica para Salvar o Gráfico ---
    # Sanitiza o nome do arquivo para remover caracteres inválidos
    nome_arquivo_seguro = "".join([c if c.isalnum() else "_" for c in nome_base_arquivo]) + ".png"
    caminho_salvar = os.path.join(output_dir, nome_arquivo_seguro)
    
    plt.savefig(caminho_salvar)
    print(f"-> Gráfico salvo em: {caminho_salvar}")
    
    plt.show()

print("\nFunção 'plotar_e_salvar_funil_barras' definida e pronta para uso.")



# =============================================================================
# 3. GERAÇÃO E SALVAMENTO DOS 7 GRÁFICOS
# =============================================================================
print("\n--- Gerando e salvando os 7 gráficos de funil ---")

# --- Gráficos 1 a 6: Um para cada curso ---
for curso in cursosComputacao_QUETEMSALVOAQUI:
    df_curso = df[df['Nome do Curso'] == curso]
    if not df_curso.empty:
        # Chama a função, passando o título e um nome base para o arquivo
        plotar_e_salvar_funil_barras(df_curso, f'Funil do FIES para: {curso}', f'funil_{curso}')
    else:
        print(f"\nAviso: Não foram encontrados dados para o curso '{curso}'.")

# --- Gráfico 7: Funil total para todos os cursos ---
plotar_e_salvar_funil_barras(df, 'Funil Agregado do FIES para a Área de Computação', 'funil_agregado_total_computacao')

print("\nProcesso concluído. Todos os gráficos foram gerados e salvos.")


# %%
