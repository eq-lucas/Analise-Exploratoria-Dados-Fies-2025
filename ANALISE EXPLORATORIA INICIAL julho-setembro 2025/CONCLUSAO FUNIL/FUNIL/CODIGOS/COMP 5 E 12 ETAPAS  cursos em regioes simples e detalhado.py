# %%
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

def gerar_grafico_funil(df_dados, curso, regiao, etapas_do_funil, pasta_sufixo):
    df_dados['periodo'] = df_dados['Ano'].astype(int).astype(str) + '-' + df_dados['Semestre'].astype(int).astype(str)
    
    df_plot = df_dados.melt(
        id_vars='periodo', 
        value_vars=etapas_do_funil,
        var_name='Etapa do Funil', 
        value_name='Quantidade'
    )
    
    plt.figure(figsize=(20, 11))
    ax = sns.barplot(
        data=df_plot,
        x='Etapa do Funil',
        y='Quantidade',
        hue='periodo',
        palette='plasma'
    )
    
    ax.set_title(f'Funil de Seleção para {curso}\nRegião: {regiao} ({pasta_sufixo})', fontsize=20)
    ax.set_xlabel('Etapa do Processo', fontsize=14)
    ax.set_ylabel('Quantidade (Escala Normal)', fontsize=14)
    ax.get_yaxis().set_major_formatter(plt.FuncFormatter(lambda x, p: format(int(x), ',')))
    plt.xticks(rotation=20, ha='right', fontsize=12)
    plt.legend(title='Período')
    plt.tight_layout()
    
    curso_safe = curso.replace(' ', '_').replace('/', '')
    regiao_safe = regiao.replace(' ', '_').replace('-', '')
    
    pasta_saida = f'../GRAFICOS/FUNIL 5 E 12 ETAPAS CURSOS COMP regiao/{pasta_sufixo}/{curso_safe}'
    os.makedirs(pasta_saida, exist_ok=True)
    
    nome_arquivo = f"funil_{curso_safe}_{regiao_safe}.png"
    caminho_salvar = os.path.join(pasta_saida, nome_arquivo)
    
    plt.savefig(caminho_salvar, dpi=300)    
    plt.close()

# --- SCRIPT PRINCIPAL ---
if __name__ == '__main__':
    PASTA_DADOS = '../../../../planilhas' 
    NOME_ARQUIVO = 'COMP DF_funil 12 etapas.csv'
    caminho_arquivo = os.path.join(PASTA_DADOS, NOME_ARQUIVO)

    try:
        df_geral = pd.read_csv(caminho_arquivo)
    except FileNotFoundError:
        exit()
        
    mapa_regioes = {
        'AC': 'Norte', 'AP': 'Norte', 'AM': 'Norte', 'PA': 'Norte', 'RO': 'Norte', 'RR': 'Norte', 'TO': 'Norte',
        'AL': 'Nordeste', 'BA': 'Nordeste', 'CE': 'Nordeste', 'MA': 'Nordeste', 'PB': 'Nordeste', 'PE': 'Nordeste', 'PI': 'Nordeste', 'RN': 'Nordeste', 'SE': 'Nordeste',
        'DF': 'Centro-Oeste', 'GO': 'Centro-Oeste', 'MT': 'Centro-Oeste', 'MS': 'Centro-Oeste',
        'ES': 'Sudeste', 'MG': 'Sudeste', 'RJ': 'Sudeste', 'SP': 'Sudeste',
        'PR': 'Sul', 'RS': 'Sul', 'SC': 'Sul'
    }
    # USA O NOME EXATO DA COLUNA DO CSV
    df_geral['Regiao'] = df_geral['UF do Local de Oferta'].map(mapa_regioes)
    
    # USA A LISTA EXATA DE COLUNAS DE MÉTRICAS DO SEU CSV
    colunas_metricas = [
        'Vagas ofertadas FIES', 'Inscritos_Geral', 'Inscritos_Validados', 'Inscritos_Eliminados',
        'Candidatos_Unicos_Geral', 'Candidatos_Unicos_Validados', 'Candidatos_Unicos_Eliminados',
        'Concorrendo_Total', 'Concorrendo_FIES', 'Concorrendo_P_FIES', 'Vagas ocupadas'
    ]
    
    colunas_agrupamento = ['Ano', 'Semestre', 'Regiao', 'Nome do Curso']
    df_agregado = df_geral.groupby(colunas_agrupamento, as_index=False)[colunas_metricas].sum()

    lista_cursos = df_agregado['Nome do Curso'].unique()
    lista_regioes = df_agregado['Regiao'].dropna().unique()
    sns.set_theme(style="whitegrid")

    # --- GERAÇÃO DOS GRÁFICOS DO FUNIL SIMPLIFICADO ---
    etapas_simplificadas = [
        'Vagas ofertadas FIES', 
        'Inscritos_Geral', 
        'Candidatos_Unicos_Geral', 
        'Concorrendo_FIES', 
        'Vagas ocupadas'
    ]
    
    for curso in lista_cursos:
        for regiao in lista_regioes:
            df_filtrado = df_agregado[(df_agregado['Nome do Curso'] == curso) & (df_agregado['Regiao'] == regiao)]
            if not df_filtrado.empty:
                gerar_grafico_funil(df_filtrado.copy(), curso, regiao, etapas_simplificadas, 'simplificado')

    # --- GERAÇÃO DOS GRÁFICOS DO FUNIL COMPLETO ---
    etapas_completas = colunas_metricas

    for curso in lista_cursos:
        for regiao in lista_regioes:
            df_filtrado = df_agregado[(df_agregado['Nome do Curso'] == curso) & (df_agregado['Regiao'] == regiao)]
            if not df_filtrado.empty:
                gerar_grafico_funil(df_filtrado.copy(), curso, regiao, etapas_completas, 'completo')

# %%