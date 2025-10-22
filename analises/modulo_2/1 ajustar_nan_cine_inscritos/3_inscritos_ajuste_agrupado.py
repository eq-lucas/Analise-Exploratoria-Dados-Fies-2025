# %%
import pandas as pd
import os
import numpy as np # Usado para checar NaNs

mapa_correcao_manual = {
    'DIREITO': ('Negócios, administração e direito', '04'),
    'ENFERMAGEM': ('Saúde e bem-estar', '09'),
    'ADMINISTRAÇÃO': ('Negócios, administração e direito', '04'),
    'NUTRIÇÃO': ('Saúde e bem-estar', '09'),
    'PSICOLOGIA': ('Ciências sociais, comunicação e informação', '03'),
    'FARMÁCIA': ('Saúde e bem-estar', '09'),
    'FISIOTERAPIA': ('Saúde e bem-estar', '09'),
    'EDUCAÇÃO FÍSICA': ('Educação', '01'),
    'PEDAGOGIA': ('Educação', '01'),
    'CIÊNCIAS CONTÁBEIS': ('Negócios, administração e direito', '04'),
    'GESTÃO DE RECURSOS HUMANOS': ('Negócios, administração e direito', '04'),
    'ARQUITETURA E URBANISMO': ('Engenharia, produção e construção', '07'),
    'ENGENHARIA CIVIL': ('Engenharia, produção e construção', '07'),
    'ODONTOLOGIA': ('Saúde e bem-estar', '09'),
    'BIOMEDICINA': ('Saúde e bem-estar', '09'),
    'ENGENHARIA ELÉTRICA': ('Engenharia, produção e construção', '07'),
    'ENGENHARIA DE PRODUÇÃO': ('Engenharia, produção e construção', '07'),
    'SERVIÇO SOCIAL': ('Saúde e bem-estar', '09'),
    'LOGÍSTICA': ('Serviços', '10'),
    'MEDICINA VETERINÁRIA': ('Agricultura, silvicultura, pesca e veterinária', '08'),
    'ENGENHARIA MECÂNICA': ('Engenharia, produção e construção', '07'),
    'ANÁLISE E DESENVOLVIMENTO DE SISTEMAS': ('Computação e Tecnologias da Informação e Comunicação (TIC)', '06'),
    'RADIOLOGIA': ('Saúde e bem-estar', '09'),
    'SISTEMAS DE INFORMAÇÃO': ('Computação e Tecnologias da Informação e Comunicação (TIC)', '06'),
    'CIÊNCIAS BIOLÓGICAS': ('Ciências naturais, matemática e estatística', '05'),
    'MARKETING': ('Negócios, administração e direito', '04'),
    'GESTÃO FINANCEIRA': ('Negócios, administração e direito', '04'),
    'GESTÃO COMERCIAL': ('Negócios, administração e direito', '04'),
    'GASTRONOMIA': ('Serviços', '10'),
    'ESTÉTICA E COSMÉTICA': ('Serviços', '10'),
    'GESTÃO HOSPITALAR': ('Negócios, administração e direito', '04'),
    'REDES DE COMPUTADORES': ('Computação e Tecnologias da Informação e Comunicação (TIC)', '06'),
    'SEGURANÇA NO TRABALHO': ('Engenharia, produção e construção', '07'),
    'ENGENHARIA DE COMPUTAÇÃO': ('Engenharia, produção e construção', '07'),
    'ENGENHARIA AMBIENTAL E SANITÁRIA': ('Engenharia, produção e construção', '07'),
    'GESTÃO DE SEGURANÇA PRIVADA': ('Serviços', '10'),
    'ENGENHARIA DE CONTROLE E AUTOMAÇÃO': ('Engenharia, produção e construção', '07'),
    'HISTÓRIA': ('Educação', '01'),
    'CONSTRUÇÃO DE EDIFÍCIOS': ('Engenharia, produção e construção', '07'),
    'GESTÃO AMBIENTAL': ('Negócios, administração e direito', '04'),
    'JORNALISMO': ('Ciências sociais, comunicação e informação', '03'),
    'DESIGN GRÁFICO': ('Artes e humanidades', '02'),
    'GESTÃO PÚBLICA': ('Negócios, administração e direito', '04'),
    'DESIGN DE INTERIORES': ('Artes e humanidades', '02'),
    'PROCESSOS GERENCIAIS': ('Negócios, administração e direito', '04'),
    'GESTÃO DA TECNOLOGIA DA INFORMAÇÃO': ('Computação e Tecnologias da Informação e Comunicação (TIC)', '06'),
    'LETRAS - LÍNGUA PORTUGUESA': ('Educação', '01'),
    'PUBLICIDADE E PROPAGANDA': ('Ciências sociais, comunicação e informação', '03'),
    'ENGENHARIA QUÍMICA': ('Engenharia, produção e construção', '07'),
    'CIÊNCIA DA COMPUTAÇÃO': ('Computação e Tecnologias da Informação e Comunicação (TIC)', '06'),
    'LETRAS - PORTUGUÊS': ('Educação', '01'),
    'SISTEMAS PARA INTERNET': ('Computação e Tecnologias da Informação e Comunicação (TIC)', '06'),
    'MATEMÁTICA': ('Educação', '01'),
    'TURISMO': ('Serviços', '10'),
    'GEOGRAFIA': ('Educação', '01'),
    'LETRAS - INGLÊS': ('Educação', '01'),
    'COMÉRCIO EXTERIOR': ('Negócios, administração e direito', '04'),
    'COMUNICAÇÃO SOCIAL - PUBLICIDADE E PROPAGANDA': ('Negócios, administração e direito', '04'),
    'ENGENHARIA AGRONÔMICA': ('Agricultura, silvicultura, pesca e veterinária', '08'),
    'LETRAS - PORTUGUÊS E INGLÊS': ('Educação', '01'),
    'RELAÇÕES INTERNACIONAIS': ('Ciências sociais, comunicação e informação', '03'),
    'SECRETARIADO EXECUTIVO': ('Negócios, administração e direito', '04'),
    'COMUNICAÇÃO SOCIAL - JORNALISMO': ('Ciências sociais, comunicação e informação', '03'),
    'SISTEMA DE INFORMAÇÃO': ('Computação e Tecnologias da Informação e Comunicação (TIC)', '06'),
    'GESTÃO DA QUALIDADE': ('Negócios, administração e direito', '04'),
    'ENGENHARIA AMBIENTAL': ('Engenharia, produção e construção', '07'),
    'JOGOS DIGITAIS': ('Computação e Tecnologias da Informação e Comunicação (TIC)', '06'),
    'TERAPIA OCUPACIONAL': ('Saúde e bem-estar', '09'),
    'DEFESA CIBERNÉTICA': ('Computação e Tecnologias da Informação e Comunicação (TIC)', '06'),
    'SEGURANÇA DA INFORMAÇÃO': ('Computação e Tecnologias da Informação e Comunicação (TIC)', '06'),
    'LETRAS - ESPANHOL': ('Educação', '01'),
    'AGRONOMIA': ('Agricultura, silvicultura, pesca e veterinária', '08'),
    'CIÊNCIAS ECONÔMICAS': ('Ciências sociais, comunicação e informação', '03'),
    'PRODUÇÃO MULTIMÍDIA': ('Artes e humanidades', '02'),
    'QUÍMICA': ('Educação', '01'),
    'CIÊNCIAS SOCIAIS': ('Educação', '01'),
    'ENGENHARIA AGRÍCOLA': ('Agricultura, silvicultura, pesca e veterinária', '08'),
    'ENGENHARIA DE ENERGIA': ('Engenharia, produção e construção', '07'),
    'COMUNICAÇÃO SOCIAL': ('Ciências sociais, comunicação e informação', '03'),
    'NEGÓCIOS IMOBILIÁRIOS': ('Negócios, administração e direito', '04'),
    'LETRAS': ('Educação', '01'),
    'FOTOGRAFIA': ('Artes e humanidades', '02'),
    'PRODUÇÃO AUDIOVISUAL': ('Artes e humanidades', '02'),
    'RELAÇÕES PÚBLICAS': ('Ciências sociais, comunicação e informação', '03'),
    'PILOTAGEM PROFISSIONAL DE AERONAVES': ('Serviços', '10'),
    'ENGENHARIA MECATRÔNICA': ('Engenharia, produção e construção', '07'),
    'ENGENHARIA DE TELECOMUNICAÇÕES': ('Engenharia, produção e construção', '07'),
    'GESTÃO DE TURISMO': ('Serviços', '10'),
    'ARTES VISUAIS': ('Educação', '01'),
    'BIOLOGIA': ('Ciências naturais, matemática e estatística', '05'),
    'PETRÓLEO E GÁS': ('Engenharia, produção e construção', '07'),
    'SECRETARIADO': ('Negócios, administração e direito', '04'),
    'ARTES CÊNICAS': ('Artes e humanidades', '02'),
    'FONOAUDIOLOGIA': ('Saúde e bem-estar', '09'),
    'ENGENHARIA DE PETRÓLEO': ('Engenharia, produção e construção', '07'),
    'ENGENHARIA DE ALIMENTOS': ('Engenharia, produção e construção', '07'),
    'PROPAGANDA E MARKETING': ('Negócios, administração e direito', '04'),
    'CONSTRUÇÃO NAVAL': ('Engenharia, produção e construção', '07'),
    'FÍSICA': ('Educação', '01'),
    'HOTELARIA': ('Serviços', '10'),
    'SERVIÇOS PENAIS': ('Serviços', '10'),
    'AUTOMAÇÃO INDUSTRIAL': ('Engenharia, produção e construção', '07'),
    'LETRAS - PORTUGUÊS E ESPANHOL': ('Educação', '01'),
    'ENGENHARIA DA COMPUTAÇÃO': ('Engenharia, produção e construção', '07'),
    'CIÊNCIA POLÍTICA': ('Ciências sociais, comunicação e informação', '03'),
    'EVENTOS': ('Serviços', '10'),
    'TEOLOGIA': ('Artes e humanidades', '02'),
    'CIÊNCIA ECONÔMICA': ('Ciências sociais, comunicação e informação', '03'),
    'GEOPROCESSAMENTO': ('Engenharia, produção e construção', '07'),
    'CIÊNCIAS DA COMPUTAÇÃO': ('Computação e Tecnologias da Informação e Comunicação (TIC)', '06'),
    'GESTÃO PORTUÁRIA': ('Serviços', '10'),
    'FORMAÇÃO PEDAGÓGICA PARA PORTADORES DE ENSINO SUPERIOR': ('Educação', '01'),
    'BANCO DE DADOS': ('Computação e Tecnologias da Informação e Comunicação (TIC)', '06'),
    'DESIGN DE MODA': ('Artes e humanidades', '02'),
    'GESTÃO DE EMPREENDIMENTOS ESPORTIVOS': ('Serviços', '10'),
    'PSICOPEDAGOGIA': ('Educação', '01'),
    'ENGENHARIA': ('Engenharia, produção e construção', '07'),
    'GESTÃO DA PRODUÇÃO INDUSTRIAL': ('Negócios, administração e direito', '04'),
    'DESIGN': ('Artes e humanidades', '02'),
    'FILOSOFIA': ('Educação', '01'),
    'MÚSICA': ('Artes e humanidades', '02'),
    'CINEMA E AUDIOVISUAL': ('Artes e humanidades', '02'),
    'COMUNICAÇÃO INSTITUCIONAL': ('Ciências sociais, comunicação e informação', '03'),
    'DESIGN DE PRODUTO': ('Artes e humanidades', '02'),
    'MARKETING DIGITAL': ('Negócios, administração e direito', '04'),
    'COMUNICAÇÃO SOCIAL - CINEMA E AUDIOVISUAL': ('Artes e humanidades', '02'),
    'ENGENHARIA ELETRÔNICA': ('Engenharia, produção e construção', '07'),
    'ADMINISTRAÇÃO PÚBLICA': ('Negócios, administração e direito', '04'),
    'MANUTENÇÃO INDUSTRIAL': ('Engenharia, produção e construção', '07'),
    'ENGENHARIA DE PETRÓLEO E GÁS': ('Engenharia, produção e construção', '07'),
    'COMUNICAÇÃO SOCIAL COM HABILITAÇÃO EM PUBLICIDADE E PROPAGANDA': ('Ciências sociais, comunicação e informação', '03'),
    'GESTÃO DE SERVIÇOS JURÍDICOS, NOTARIAIS E DE REGISTRO': ('Negócios, administração e direito', '04'),
    'SISTEMAS ELÉTRICOS': ('Engenharia, produção e construção', '07'),
    'VISAGISMO E TERAPIAS CAPILARES': ('Serviços', '10'),
    'GERENCIAMENTO DE REDES DE COMPUTADORES': ('Computação e Tecnologias da Informação e Comunicação (TIC)', '06'),
    'GESTÃO DE RECURSOS HÍDRICOS': ('Engenharia, produção e construção', '07'),
    'COMUNICAÇÃO EMPRESARIAL': ('Ciências sociais, comunicação e informação', '03'),
    'COMUNICAÇÃO SOCIAL - RADIO E TELEVISÃO': ('Ciências sociais, comunicação e informação', '03'),
    'ENERGIAS RENOVÁVEIS': ('Engenharia, produção e construção', '07'),
    'MODA': ('Artes e humanidades', '02'),
    'ENGENHARIA BIOMÉDICA': ('Engenharia, produção e construção', '07'),
    'SEGURANÇA PÚBLICA': ('Serviços', '10'),
    'CIÊNCIA DE DADOS E MACHINE LEARNING': ('Computação e Tecnologias da Informação e Comunicação (TIC)', '06'),
    'GESTÃO DE PRODUÇÃO INDUSTRIAL': ('Negócios, administração e direito', '04'),
    'MULTIMÍDIA': ('Artes e humanidades', '02'),
    'BIOCOMBUSTÍVEIS': ('Engenharia, produção e construção', '07'),
    'ENGENHARIA DE BIOPROCESSOS E BIOTECNOLOGIA': ('Engenharia, produção e construção', '07'),
    'ZOOTECNIA': ('Agricultura, silvicultura, pesca e veterinária', '08'),
    'GESTÃO DESPORTIVA E DE LAZER': ('Serviços', '10'),
    'TRANSPORTE TERRESTRE': ('Serviços', '10'),
    'PROCESSOS QUÍMICOS': ('Engenharia, produção e construção', '07'),
    'SECRETARIADO EXECUTIVO TRILINGUE': ('Negócios, administração e direito', '04'),
    'ELETROTÉCNICA INDUSTRIAL': ('Engenharia, produção e construção', '07'),
    'AGROPECUÁRIA': ('Agricultura, silvicultura, pesca e veterinária', '08'),
    'BIBLIOTECONOMIA': ('Ciências sociais, comunicação e informação', '03'),
    'AGRIMENSURA': ('Engenharia, produção e construção', '07'),
    'ENGENHARIA DE SOFTWARE': ('Computação e Tecnologias da Informação e Comunicação (TIC)', '06'),
    'ESTÉTICA': ('Serviços', '10'),
    'PRODUÇÃO GRÁFICA DIGITAL': ('Artes e humanidades', '02'),
    'TECNÓLOGO EM METALURGIA': ('Engenharia, produção e construção', '07'),
    'GESTÃO DE COOPERATIVAS': ('Negócios, administração e direito', '04'),
    'COMUNICAÇÃO SOCIAL - RELAÇÕES PÚBLICAS': ('Ciências sociais, comunicação e informação', '03'),
    'ENGENHARIA DE MATERIAIS': ('Engenharia, produção e construção', '07'),
    'DANÇA': ('Artes e humanidades', '02'),
    'SEGURANÇA PRIVADA': ('Serviços', '10'),
    'MECATRÔNICA INDUSTRIAL': ('Engenharia, produção e construção', '07'),
    'POLÍTICAS PÚBLICAS': ('Ciências sociais, comunicação e informação', '03'),
    'PAPEL E CELULOSE': ('Engenharia, produção e construção', '07'),
    'SERVIÇOS JURÍDICOS, CARTORÁRIOS E NOTARIAIS': ('Negócios, administração e direito', '04'),
    'ENGENHARIA AEROESPACIAL': ('Engenharia, produção e construção', '07'),
    'AGRONEGÓCIO': ('Agricultura, silvicultura, pesca e veterinária', '08'),
    'PROCESSOS ESCOLARES': ('Educação', '01'),
    'LETRAS - LÍNGUA PORTUGUESA E LITERATURAS DE LÍNGUA PORTUGUESA': ('Educação', '01'),
    'PRODUÇÃO CULTURAL': ('Artes e humanidades', '02'),
    'GESTÃO DE SERVIÇOS JURÍDICOS E NOTARIAIS': ('Negócios, administração e direito', '04'),
    'GESTÃO DE NEGÓCIOS NO VAREJO': ('Negócios, administração e direito', '04'),
    'COMUNICAÇÃO PARA WEB': ('Ciências sociais, comunicação e informação', '03'),
    'COMUNICAÇÃO SOCIAL\xa0 - RADIALISMO': ('Ciências sociais, comunicação e informação', '03'),
    'ACUPUNTURA': ('Saúde e bem-estar', '09'),
    'DESIGN DE ANIMAÇÃO': ('Artes e humanidades', '02'),
    'EDUCAÇÃO ARTÍSTICA': ('Educação', '01'),
    'GESTÃO DE NEGÓCIOS E INOVAÇÃO': ('Negócios, administração e direito', '04'),
    'LOGÃ\x8dSTICA': ('Negócios, administração e direito', '04'),
    'HOTELARIA HOSPITALAR': ('Saúde e bem-estar', '09'),
    'DESENVOLVIMENTO PARA WEB': ('Computação e Tecnologias da Informação e Comunicação (TIC)', '06'),
    'FORMAÇÃO PEDAGÓGICA DE DOCENTES PARA A EDUCAÇÃO BÁSICA E PROFISSIONAL': ('Educação', '01'),
    'GESTÃO EMPREENDEDORA': ('Negócios, administração e direito', '04'),
    'PUBLICIDADE': ('Ciências sociais, comunicação e informação', '03'),
    'QUIROPRAXIA': ('Saúde e bem-estar', '09'),
    'OFTÁLMICA': ('Saúde e bem-estar', '09'),
    'CIÊNCIA DE DADOS': ('Computação e Tecnologias da Informação e Comunicação (TIC)', '06'),
    'TEATRO': ('Artes e humanidades', '02'),
    'ESTATÍSTICA': ('Ciências naturais, matemática e estatística', '05'),
    'RÁDIO, TV E INTERNET': ('Ciências sociais, comunicação e informação', '03'),
    'SECRETARIADO EXECUTIVO TRILÍNGUE': ('Negócios, administração e direito', '04'),
    'COMUNICAÇÃO SOCIAL - RADIALISMO (RÁDIO E TV)': ('Ciências sociais, comunicação e informação', '03'),
    'SISTEMAS BIOMÉDICOS': ('Engenharia, produção e construção', '07'),
    'BIG DATA E INTELIGÊNCIA ANALÍTICA': ('Computação e Tecnologias da Informação e Comunicação (TIC)', '06'),
    'LETRAS - FRANCÊS': ('Educação', '01'),
    'COMUNICAÇÃO EM CRIAÇÃO E DESENVOLVIMENTO DE WEB SITES E DESIGN': ('Ciências sociais, comunicação e informação', '03'),
    'SEGURANÇA NO TRÂNSITO': ('Serviços', '10'),
    'ELETRÔNICA INDUSTRIAL': ('Engenharia, produção e construção', '07'),
    'GESTÃO MERCADOLÓGICA': ('Negócios, administração e direito', '04'),
    'ENGENHARIA FLORESTAL': ('Agricultura, silvicultura, pesca e veterinária', '08'),
    'INTELIGÊNCIA ARTIFICIAL': ('Computação e Tecnologias da Informação e Comunicação (TIC)', '06'),
    'CIÊNCIAS DA ACUPUNTURA': ('Saúde e bem-estar', '09'),
    'ENGENHARIA CARTOGRÁFICA E DE AGRIMENSURA': ('Engenharia, produção e construção', '07'),
    'MUSEOLOGIA': ('Ciências sociais, comunicação e informação', '03'),
    'TURISMO RECEPTIVO': ('Serviços', '10'),
    'COMUNICAÇÃO DIGITAL': ('Ciências sociais, comunicação e informação', '03'),
    'SERVIÇOS JUDICIAIS': ('Negócios, administração e direito', '04'),
    'DESENHO INDUSTRIAL': ('Artes e humanidades', '02'),
    'MÚSICA - MÚSICA POPULAR BRASILEIRA': ('Artes e humanidades', '02'),
    'VITICULTURA E ENOLOGIA': ('Agricultura, silvicultura, pesca e veterinária', '08'),
    'COMPUTAÇÃO EM NUVEM': ('Computação e Tecnologias da Informação e Comunicação (TIC)', '06'),
    'SERVIÇOS JURÍDICOS': ('Negócios, administração e direito', '04'),
    'SERVIÇOS NOTARIAIS E REGISTRAIS': ('Negócios, administração e direito', '04'),
    'GESTÃO DO AGRONEGÓCIO': ('Agricultura, silvicultura, pesca e veterinária', '08'),
    'E-COMMERCE': ('Negócios, administração e direito', '04'),
    'SECRETARIADO EXECUTIVO BILINGUE - PORTUGUÊS/INGLÊS': ('Negócios, administração e direito', '04'),
    'GESTÃO DE TURISMO RECEPTIVO': ('Serviços', '10'),
    'FORMAÇÃO DE DOCENTES PARA A EDUCAÇÃO BÁSICA': ('Educação', '01'),
    'PRODUÇÃO SUCROALCOOLEIRA': ('Engenharia, produção e construção', '07'),
    'AGROINDUSTRIA': ('Agricultura, silvicultura, pesca e veterinária', '08'),
    'COMUNICAÇÃO E ILUSTRAÇÃO DIGITAL': ('Artes e humanidades', '02'),
    'CIÊNCIAS DA RELIGIÃO': ('Artes e humanidades', '02'),
    'PROCESSOS METALÚRGICOS': ('Engenharia, produção e construção', '07'),
    'CONTROLE DE OBRAS': ('Engenharia, produção e construção', '07'),
    'FABRICAÇÃO MECÂNICA': ('Engenharia, produção e construção', '07'),
    'GERONTOLOGIA': ('Saúde e bem-estar', '09'),
    'COSMÉTICOS': ('Engenharia, produção e construção', '07'),
    'PAISAGISMO': ('Agricultura, silvicultura, pesca e veterinária', '08'),
    'ENGENHARIA DE PESCA': ('Agricultura, silvicultura, pesca e veterinária', '08'),
    'SUCROALCOOLEIRA': ('Engenharia, produção e construção', '07'),
    'SISTEMAS DE TELECOMUNICAÇÕES': ('Engenharia, produção e construção', '07'),
    'ENGENHARIA AUTOMOTIVA': ('Engenharia, produção e construção', '07'),
    'DESENVOLVIMENTO E GESTÃO DE STARTUPS': ('Negócios, administração e direito', '04'),
    'GESTÃO DE STARTUP E NOVOS NEGÓCIOS': ('Negócios, administração e direito', '04'),
    'TECNOLOGIA E DESIGN DE NEGÓCIOS': ('Negócios, administração e direito', '04'),
    'INTERDISCIPLINAR EM CIÊNCIA E TECNOLOGIA': ('Ciências naturais, matemática e estatística', '05'),
    # --- NOMES NÃO ENCONTRADOS NO GABARITO ---
    'GESTÃO DE ENERGIAS': ('VERIFICAR MANUALMENTE', 'XX'), 

    # adicionado apos executar modulo3-> verificacao cursos nan, entao refeito todos csv do modulo 2 em diante( poucos refeitos)
    'ENGENHARIA DE ENERGIAS': ('Engenharia, produção e construção', '07'),
}



# --- 1. Configuração ---
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)

# Caminho para o arquivo AGRUPADO (que você criou)
path_agrupado_base = '../../../planilhas/limpo/modulo_1/agrupado/'
arquivo_agrupado = 'inscritos_agrupado.csv'
caminho_leitura = os.path.join(path_agrupado_base, arquivo_agrupado)

# Colunas que vamos checar e corrigir
coluna_chave = 'nome_curso_inscricao'
coluna_valor_nome = 'NO_CINE_AREA_GERAL'
coluna_valor_cod = 'CO_CINE_AREA_GERAL'


# --- 3. Função de Correção (Apply) ---

def corrigir_linha(row, mapa, chave, val_nome, val_cod):
    """
    Função para ser usada com .apply()
    Verifica se a linha precisa de correção e, se sim, aplica.
    """
    # Condição 1: O valor do nome da área é NaN?
    if pd.isna(row[val_nome]):
        
        nome_curso_atual = row[chave]
        
        # Condição 2: O nome do curso existe no nosso mapa?
        if nome_curso_atual in mapa:
            
            # Pega os valores corrigidos do mapa
            correcao = mapa[nome_curso_atual] # Ex: ('Saúde e bem-estar', '09')
            
            # Não corrige os que marcamos para verificação manual
            if correcao[0] != 'VERIFICAR MANUALMENTE':
                row[val_nome] = correcao[0] # Preenche o NOME da área
                row[val_cod] = correcao[1]  # Preenche o CÓDIGO da área
                
    # Retorna a linha (modificada ou original)
    return row

# --- 4. Ler, Aplicar e Salvar ---

print(f"Lendo o arquivo agrupado principal: {caminho_leitura}")
try:
    df_principal = pd.read_csv(caminho_leitura, low_memory=False)
    
    # Verifica a contagem de NaNs ANTES
    nans_antes = df_principal[coluna_valor_nome].isnull().sum()
    print(f"\nTotal de NaNs ANTES da correção: {nans_antes}")

    if nans_antes > 0:
        print("Iniciando correção (usando .apply())... Isso pode levar alguns minutos...")
        
        # Aplicando a função linha a linha (axis=1)
        df_corrigido = df_principal.apply(
            corrigir_linha,
            args=(mapa_correcao_manual, coluna_chave, coluna_valor_nome, coluna_valor_cod),
            axis=1
        )
        
        # Verifica a contagem de NaNs DEPOIS
        nans_depois = df_corrigido[coluna_valor_nome].isnull().sum()
        print(f"\nTotal de NaNs DEPOIS da correção: {nans_depois}")
        print(f"Total de NaNs Corrigidos: {nans_antes - nans_depois}")

        # Salva o arquivo final e corrigido
        nome_salvar = 'inscritos_agrupado_limpo_CORRIGIDO.csv'
        path_save= '../../../planilhas/limpo/modulo_2/ajustar_nan_cine_inscritos/'

        caminho_salvar = os.path.join(path_save, nome_salvar)
        
        print(f"\nSalvando arquivo corrigido em: {caminho_salvar}")
        df_corrigido.to_csv(caminho_salvar, index=False, encoding='utf-8-sig')
        
        print("\n--- Processo de correção concluído! ---")
        
        if nans_depois > 0:
            print(f"\nAinda restaram {nans_depois} NaNs.")
            print("Isso pode ser o curso 'GESTÃO DE ENERGIAS' ou outros erros de digitação")
            print("que não foram encontrados no 'dataset_auxiliar'.")

    else:
        print("Nenhum NaN encontrado. Nenhum processo de correção foi necessário.")

except FileNotFoundError:
    print(f"ERRO: Arquivo não encontrado: {caminho_leitura}")
    print("Por favor, rode o script de concatenação ('inscritos_agrupado.csv') primeiro.")
except KeyError:
    print(f"ERRO: Não foi possível encontrar as colunas necessárias no arquivo.")
    print(f"Verifique se o '{arquivo_agrupado}' contém '{coluna_chave}', '{coluna_valor_nome}' e '{coluna_valor_cod}'.")
except Exception as e:
    print(f"ERRO inesperado: {e}")

# %%