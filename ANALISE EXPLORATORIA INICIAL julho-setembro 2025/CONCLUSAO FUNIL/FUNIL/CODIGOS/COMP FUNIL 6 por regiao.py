# %%
import pandas as pd

path= '../../../../planilhas/COMP DF_funil 12 etapas.csv'

df=pd.read_csv(path)
df

mapa_regioes = {
    'AC': 'Norte', 'AP': 'Norte', 'AM': 'Norte', 'PA': 'Norte', 'RO': 'Norte', 'RR': 'Norte', 'TO': 'Norte',
    'AL': 'Nordeste', 'BA': 'Nordeste', 'CE': 'Nordeste', 'MA': 'Nordeste', 'PB': 'Nordeste', 'PE': 'Nordeste', 'PI': 'Nordeste', 'RN': 'Nordeste', 'SE': 'Nordeste',
    'DF': 'Centro-Oeste', 'GO': 'Centro-Oeste', 'MT': 'Centro-Oeste', 'MS': 'Centro-Oeste',
    'ES': 'Sudeste', 'MG': 'Sudeste', 'RJ': 'Sudeste', 'SP': 'Sudeste',
    'PR': 'Sul', 'RS': 'Sul', 'SC': 'Sul'
}
# USA O NOME EXATO DA COLUNA DO CSV
df['Regiao'] = df['UF do Local de Oferta'].map(mapa_regioes)


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


# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
# SEU CÓDIGO DE SETUP (JÁ ESTÁ PERFEITO)
# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

path = '../../../../planilhas/COMP DF_funil 12 etapas.csv'


df = pd.read_csv(path)

mapa_regioes = {
    'AC': 'Norte', 'AP': 'Norte', 'AM': 'Norte', 'PA': 'Norte', 'RO': 'Norte', 'RR': 'Norte', 'TO': 'Norte',
    'AL': 'Nordeste', 'BA': 'Nordeste', 'CE': 'Nordeste', 'MA': 'Nordeste', 'PB': 'Nordeste', 'PE': 'Nordeste', 'PI': 'Nordeste', 'RN': 'Nordeste', 'SE': 'Nordeste',
    'DF': 'Centro-Oeste', 'GO': 'Centro-Oeste', 'MT': 'Centro-Oeste', 'MS': 'Centro-Oeste',
    'ES': 'Sudeste', 'MG': 'Sudeste', 'RJ': 'Sudeste', 'SP': 'Sudeste',
    'PR': 'Sul', 'RS': 'Sul', 'SC': 'Sul'
}
df['Regiao'] = df['UF do Local de Oferta'].map(mapa_regioes)

COLUNAS_FUNIL_GRAFICAMENTE_SERA = [
    'Vagas ofertadas FIES',
    'Inscritos_Geral',
    'Inscritos_Com_Nota_Suficiente',
    'Candidatos_Unicos_Geral',
    'Concorrendo_Total', # CANDIDATOS UNICOS COM NOTA SUFICIENTE
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

print("Setup inicial concluído. DataFrame carregado e coluna 'Regiao' criada.")



# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
# PREPARAÇÃO PARA A GERAÇÃO DOS GRÁFICOS REGIONAIS
# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=

# --- Criação da pasta para salvar os novos gráficos ---
output_dir_regional = '../GRAFICOS/FUNIL 6 ETAPAS CURSOS REGIAO COMP'
os.makedirs(output_dir_regional, exist_ok=True)
print(f"Pasta '{output_dir_regional}' pronta para salvar os gráficos.")

# Define um estilo visual e cria a coluna 'Periodo'
sns.set_style("whitegrid")
df['Periodo'] = df['Ano'].astype(str) + '/' + df['Semestre'].astype(str)

# Pega a lista de regiões diretamente do dataframe para ser mais robusto
# e remove qualquer valor nulo que possa ter surgido
regioes = [r for r in df['Regiao'].unique() if pd.notna(r)]
print(f"Análise será feita para as regiões: {regioes}")

# Define a lista de "assuntos" a analisar: os 6 cursos + um item para o total
assuntos_analise = cursosComputacao_QUETEMSALVOAQUI + ['Todos os Cursos de Computação']



# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
# FUNÇÃO DE PLOTAGEM (A MESMA DE ANTES, POIS É REUTILIZÁVEL)
# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
def plotar_e_salvar_funil_barras(dataframe, titulo, nome_base_arquivo):
    df_agg = dataframe.groupby('Periodo')[COLUNAS_FUNIL_GRAFICAMENTE_SERA].sum().reset_index()
    df_melted = df_agg.melt(id_vars='Periodo', var_name='Etapa_Funil', value_name='Quantidade')
    df_melted['Etapa_Funil'] = pd.Categorical(df_melted['Etapa_Funil'], categories=COLUNAS_FUNIL_GRAFICAMENTE_SERA, ordered=True)
    
    plt.figure(figsize=(18, 9))
    sns.barplot(
        data=df_melted,
        x='Etapa_Funil',
        y='Quantidade',
        hue='Periodo',
        palette='viridis'
    )
    
    plt.title(titulo, fontsize=18, weight='bold')
    plt.xlabel('Etapas do Funil de Seleção', fontsize=14)
    plt.ylabel('Quantidade', fontsize=14)
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    
    nome_arquivo_seguro = "".join([c if c.isalnum() else "_" for c in nome_base_arquivo]) + ".png"
    caminho_salvar = os.path.join(output_dir_regional, nome_arquivo_seguro)
    
    plt.savefig(caminho_salvar)
    print(f"-> Gráfico salvo em: {caminho_salvar}")
    plt.close() # Fecha a figura para não consumir memória e não exibir no notebook

print("\nFunção de plotagem pronta.")



# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
# LÓGICA PRINCIPAL: LOOPS ANINHADOS PARA GERAR TODOS OS GRÁFICOS
# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
print("\n--- INICIANDO GERAÇÃO MASSIVA DE GRÁFICOS REGIONAIS ---")

# Loop externo: percorre cada "assunto" (6 cursos + 1 total)
for assunto in assuntos_analise:
    print(f"\n==================== Processando Assunto: {assunto} ====================")
    
    # Prepara o dataframe base para o assunto
    if assunto == 'Todos os Cursos de Computação':
        df_assunto = df # Para o total, usamos o dataframe completo
    else:
        df_assunto = df[df['Nome do Curso'] == assunto] # Filtra para um curso específico
    
    # Loop interno: percorre cada região para o assunto atual
    for regiao in regioes:
        # Filtra o dataframe do assunto para a região atual
        df_filtrado = df_assunto[df_assunto['Regiao'] == regiao]
        
        # Só gera o gráfico se houver dados após a filtragem
        if not df_filtrado.empty:
            # Cria um título e nome de arquivo dinâmicos
            titulo_grafico = f'Funil FIES para: {assunto}\n(Região {regiao})'
            nome_arquivo = f'funil_{assunto}_{regiao}'
            
            # Chama a função para gerar e salvar o gráfico
            plotar_e_salvar_funil_barras(df_filtrado, titulo_grafico, nome_arquivo)
        else:
            print(f"-> Aviso: Não há dados para '{assunto}' na região '{regiao}'. Gráfico não gerado.")

print("\n\n--- PROCESSO CONCLUÍDO! ---")
print(f"Todos os gráficos foram salvos na pasta '{output_dir_regional}'.")


# %%
