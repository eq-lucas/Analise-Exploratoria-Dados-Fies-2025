# %%
import pandas as pd
import os
import numpy as np # Usado para checar NaNs

# --- 1. Configuração ---
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)

# Caminho onde estão os arquivos INDIVIDUAIS de OFERTAS com CINE (com NaNs)
path_leitura_base = '../../../planilhas/limpo/modulo_1/ofertas_coluna_CINE/' # <-- Lendo os individuais de OFERTAS

# Colunas que vamos checar e corrigir (VERIFIQUE OS NOMES!)
coluna_chave = 'nome_curso_ofertas'      # <-- Ajustado para OFERTAS
coluna_valor_nome = 'NO_CINE_AREA_GERAL'
coluna_valor_cod = 'CO_CINE_AREA_GERAL'

# --- 2. O MAPA DE CORREÇÃO MANUAL PARA OFERTAS (Versão 3 - Corrigida) ---
mapa_correcao_manual_ofertas = {
    'ADMINISTRAÇÃO': ('Negócios, administração e direito', '04'),
    'EDUCAÇÃO FÍSICA': ('Educação', '01'), # Corrigido!
    'CIÊNCIAS CONTÁBEIS': ('Negócios, administração e direito', '04'),
    'ENGENHARIA DE PRODUÇÃO': ('Engenharia, produção e construção', '07'),
    'PEDAGOGIA': ('Educação', '01'),
    'LOGÍSTICA': ('Negócios, administração e direito', '04'),
    'GESTÃO DE RECURSOS HUMANOS': ('Negócios, administração e direito', '04'),
    'ENGENHARIA CIVIL': ('Engenharia, produção e construção', '07'),
    'DIREITO': ('Negócios, administração e direito', '04'),
    'SERVIÇO SOCIAL': ('Saúde e bem-estar', '09'),
    'NUTRIÇÃO': ('Saúde e bem-estar', '09'),
    'FARMÁCIA': ('Saúde e bem-estar', '09'),
    'BIOMEDICINA': ('Saúde e bem-estar', '09'),
    'ARQUITETURA E URBANISMO': ('Engenharia, produção e construção', '07'),
    'MARKETING': ('Negócios, administração e direito', '04'),
    'FISIOTERAPIA': ('Saúde e bem-estar', '09'),
    'CIÊNCIAS BIOLÓGICAS': ('Ciências naturais, matemática e estatística', '05'),
    'ENGENHARIA ELÉTRICA': ('Engenharia, produção e construção', '07'),
    'ENFERMAGEM': ('Saúde e bem-estar', '09'),
    'REDES DE COMPUTADORES': ('Computação e Tecnologias da Informação e Comunicação (TIC)', '06'),
    'ANÁLISE E DESENVOLVIMENTO DE SISTEMAS': ('Computação e Tecnologias da Informação e Comunicação (TIC)', '06'),
    'GESTÃO FINANCEIRA': ('Negócios, administração e direito', '04'),
    'GESTÃO COMERCIAL': ('Negócios, administração e direito', '04'),
    'SEGURANÇA NO TRABALHO': ('Engenharia, produção e construção', '07'),
    'SISTEMAS DE INFORMAÇÃO': ('Computação e Tecnologias da Informação e Comunicação (TIC)', '06'),
    'PSICOLOGIA': ('Ciências sociais, comunicação e informação', '03'),
    'ESTÉTICA E COSMÉTICA': ('Serviços', '10'),
    'GESTÃO HOSPITALAR': ('Negócios, administração e direito', '04'),
    'ENGENHARIA MECÂNICA': ('Engenharia, produção e construção', '07'),
    'PROCESSOS GERENCIAIS': ('Negócios, administração e direito', '04'),
    'LETRAS - PORTUGUÊS E INGLÊS': ('Educação', '01'),
    'DESIGN DE INTERIORES': ('Artes e humanidades', '02'),
    'TURISMO': ('Serviços', '10'),
    'COMÉRCIO EXTERIOR': ('Negócios, administração e direito', '04'),
    'GASTRONOMIA': ('Serviços', '10'),
    'ENGENHARIA DE COMPUTAÇÃO': ('Engenharia, produção e construção', '07'),
    'LETRAS - LÍNGUA PORTUGUESA': ('Educação', '01'),
    'JORNALISMO': ('Ciências sociais, comunicação e informação', '03'),
    'GESTÃO PÚBLICA': ('Negócios, administração e direito', '04'),
    'ENGENHARIA AMBIENTAL E SANITÁRIA': ('Engenharia, produção e construção', '07'),
    'HISTÓRIA': ('Educação', '01'),
    'GESTÃO DA TECNOLOGIA DA INFORMAÇÃO': ('Computação e Tecnologias da Informação e Comunicação (TIC)', '06'),
    'DESIGN GRÁFICO': ('Artes e humanidades', '02'),
    'ODONTOLOGIA': ('Saúde e bem-estar', '09'),
    'ENGENHARIA DE CONTROLE E AUTOMAÇÃO': ('Engenharia, produção e construção', '07'),
    'GESTÃO AMBIENTAL': ('Engenharia, produção e construção', '07'), # Ofertas Aux tem Engenharia
    'CIÊNCIA DA COMPUTAÇÃO': ('Computação e Tecnologias da Informação e Comunicação (TIC)', '06'),
    'PUBLICIDADE E PROPAGANDA': ('Ciências sociais, comunicação e informação', '03'),
    'GESTÃO DE SEGURANÇA PRIVADA': ('Serviços', '10'),
    'SISTEMAS PARA INTERNET': ('Computação e Tecnologias da Informação e Comunicação (TIC)', '06'),
    'ENGENHARIA QUÍMICA': ('Engenharia, produção e construção', '07'),
    'CONSTRUÇÃO DE EDIFÍCIOS': ('Engenharia, produção e construção', '07'),
    'RADIOLOGIA': ('Saúde e bem-estar', '09'),
    'GESTÃO DA QUALIDADE': ('Negócios, administração e direito', '04'),
    'GEOGRAFIA': ('Educação', '01'),
    'SECRETARIADO EXECUTIVO': ('Negócios, administração e direito', '04'),
    'MATEMÁTICA': ('Educação', '01'),
    'MEDICINA VETERINÁRIA': ('Agricultura, silvicultura, pesca e veterinária', '08'),
    'ENGENHARIA AGRONÔMICA': ('Agricultura, silvicultura, pesca e veterinária', '08'),
    'RELAÇÕES INTERNACIONAIS': ('Ciências sociais, comunicação e informação', '03'),
    'JOGOS DIGITAIS': ('Computação e Tecnologias da Informação e Comunicação (TIC)', '06'),
    'DESIGN DE MODA': ('Artes e humanidades', '02'),
    'COMUNICAÇÃO SOCIAL - PUBLICIDADE E PROPAGANDA': ('Ciências sociais, comunicação e informação', '03'),
    'ENGENHARIA AMBIENTAL': ('Engenharia, produção e construção', '07'),
    'ENGENHARIA DE ALIMENTOS': ('Engenharia, produção e construção', '07'),
    'CIÊNCIAS ECONÔMICAS': ('Ciências sociais, comunicação e informação', '03'),
    'PRODUÇÃO AUDIOVISUAL': ('Artes e humanidades', '02'),
    'LETRAS - PORTUGUÊS': ('Educação', '01'),
    'SEGURANÇA DA INFORMAÇÃO': ('Computação e Tecnologias da Informação e Comunicação (TIC)', '06'),
    'DEFESA CIBERNÉTICA': ('Computação e Tecnologias da Informação e Comunicação (TIC)', '06'),
    'QUÍMICA': ('Educação', '01'), # Auxiliar Ofertas só tem Educação
    'SISTEMA DE INFORMAÇÃO': ('Computação e Tecnologias da Informação e Comunicação (TIC)', '06'),
    'ENGENHARIA MECATRÔNICA': ('Engenharia, produção e construção', '07'),
    'TERAPIA OCUPACIONAL': ('Saúde e bem-estar', '09'),
    'COMUNICAÇÃO SOCIAL - JORNALISMO': ('Ciências sociais, comunicação e informação', '03'),
    'AGRONOMIA': ('Agricultura, silvicultura, pesca e veterinária', '08'),
    'NEGÓCIOS IMOBILIÁRIOS': ('Negócios, administração e direito', '04'),
    'ENGENHARIA DE ENERGIA': ('Engenharia, produção e construção', '07'),
    'ENGENHARIA AGRÍCOLA': ('Agricultura, silvicultura, pesca e veterinária', '08'),
    'FOTOGRAFIA': ('Artes e humanidades', '02'),
    'SECRETARIADO': ('Negócios, administração e direito', '04'),
    'ARTES VISUAIS': ('Artes e humanidades', '02'),
    'ENGENHARIA DE TELECOMUNICAÇÕES': ('Engenharia, produção e construção', '07'),
    'LETRAS - ESPANHOL': ('Educação', '01'),
    'PRODUÇÃO MULTIMÍDIA': ('Artes e humanidades', '02'),
    'CIÊNCIAS SOCIAIS': ('Ciências sociais, comunicação e informação', '03'), # Auxiliar Ofertas tem Ciencias Sociais
    'LETRAS - INGLÊS': ('Educação', '01'),
    'RELAÇÕES PÚBLICAS': ('Ciências sociais, comunicação e informação', '03'),
    'FONOAUDIOLOGIA': ('Saúde e bem-estar', '09'),
    'COMUNICAÇÃO SOCIAL': ('Ciências sociais, comunicação e informação', '03'),
    'GESTÃO DE TURISMO': ('Serviços', '10'),
    'PETRÓLEO E GÁS': ('Engenharia, produção e construção', '07'),
    'EVENTOS': ('Serviços', '10'),
    'AUTOMAÇÃO INDUSTRIAL': ('Engenharia, produção e construção', '07'),
    'LETRAS': ('Educação', '01'),
    'ENGENHARIA DE PETRÓLEO': ('Engenharia, produção e construção', '07'),
    'HOTELARIA': ('Serviços', '10'),
    'ENGENHARIA DA COMPUTAÇÃO': ('Engenharia, produção e construção', '07'),
    'FÍSICA': ('Educação', '01'), # Auxiliar Ofertas só tem Educação
    'TEOLOGIA': ('Artes e humanidades', '02'),
    'PSICOPEDAGOGIA': ('Educação', '01'),
    'GESTÃO DA PRODUÇÃO INDUSTRIAL': ('Negócios, administração e direito', '04'),
    'CIÊNCIA POLÍTICA': ('Ciências sociais, comunicação e informação', '03'),
    'SERVIÇOS PENAIS': ('Serviços', '10'),
    'GESTÃO PORTUÁRIA': ('Serviços', '10'),
    'BANCO DE DADOS': ('Computação e Tecnologias da Informação e Comunicação (TIC)', '06'),
    'LETRAS - PORTUGUÊS E ESPANHOL': ('Educação', '01'),
    'DESIGN': ('Artes e humanidades', '02'),
    'DESIGN DE PRODUTO': ('Artes e humanidades', '02'),
    'GEOPROCESSAMENTO': ('Engenharia, produção e construção', '07'),
    'ADMINISTRAÇÃO PÚBLICA': ('Negócios, administração e direito', '04'),
    'FORMAÇÃO PEDAGÓGICA PARA PORTADORES DE ENSINO SUPERIOR': ('Educação', '01'),
    'MÚSICA': ('Artes e humanidades', '02'),
    'FILOSOFIA': ('Artes e humanidades', '02'),
    'MANUTENÇÃO INDUSTRIAL': ('Engenharia, produção e construção', '07'),
    'GESTÃO DE EMPREENDIMENTOS ESPORTIVOS': ('Serviços', '10'),
    'ENGENHARIA ELETRÔNICA': ('Engenharia, produção e construção', '07'),
    'MODA': ('Artes e humanidades', '02'),
    'ENGENHARIA DE PETRÓLEO E GÁS': ('Engenharia, produção e construção', '07'),
    'SECRETARIADO EXECUTIVO TRILINGUE': ('Negócios, administração e direito', '04'),
    'GESTÃO DE SERVIÇOS JURÍDICOS, NOTARIAIS E DE REGISTRO': ('Negócios, administração e direito', '04'),
    'CIÊNCIA ECONÔMICA': ('Ciências sociais, comunicação e informação', '03'),
    'SISTEMAS ELÉTRICOS': ('Engenharia, produção e construção', '07'),
    'COMUNICAÇÃO SOCIAL - RADIO E TELEVISÃO': ('Ciências sociais, comunicação e informação', '03'),
    'ENGENHARIA BIOMÉDICA': ('Engenharia, produção e construção', '07'),
    'MARKETING DIGITAL': ('Negócios, administração e direito', '04'),
    'COMUNICAÇÃO INSTITUCIONAL': ('Ciências sociais, comunicação e informação', '03'),
    'COMUNICAÇÃO EMPRESARIAL': ('Ciências sociais, comunicação e informação', '03'),
    'CIÊNCIA DE DADOS E MACHINE LEARNING': ('Computação e Tecnologias da Informação e Comunicação (TIC)', '06'),
    'SEGURANÇA PÚBLICA': ('Serviços', '10'),
    'GESTÃO DE PRODUÇÃO INDUSTRIAL': ('Negócios, administração e direito', '04'),
    'ENERGIAS RENOVÁVEIS': ('Engenharia, produção e construção', '07'),
    'ENGENHARIA DE BIOPROCESSOS E BIOTECNologia': ('Engenharia, produção e construção', '07'),
    'ZOOTECNIA': ('Agricultura, silvicultura, pesca e veterinária', '08'),
    'BIOCOMBUSTÍVEIS': ('Engenharia, produção e construção', '07'),
    'PROCESSOS QUÍMICOS': ('Engenharia, produção e construção', '07'),
    'GESTÃO DE RECURSOS HÍDRICOS': ('Engenharia, produção e construção', '07'),
    'TRANSPORTE TERRESTRE': ('Serviços', '10'),
    'GESTÃO DESPORTIVA E DE LAZER': ('Serviços', '10'),
    'ELETROTÉCNICA INDUSTRIAL': ('Engenharia, produção e construção', '07'),
    'ESTÉTICA': ('Serviços', '10'),
    'GERENCIAMENTO DE REDES DE COMPUTADORES': ('Computação e Tecnologias da Informação e Comunicação (TIC)', '06'),
    'AGRIMENSURA': ('Engenharia, produção e construção', '07'),
    'ENGENHARIA DE SOFTWARE': ('Computação e Tecnologias da Informação e Comunicação (TIC)', '06'),
    'GESTÃO DE COOPERATIVAS': ('Negócios, administração e direito', '04'),
    'ENGENHARIA DE MATERIAIS': ('Engenharia, produção e construção', '07'),
    'MECATRÔNICA INDUSTRIAL': ('Engenharia, produção e construção', '07'),
    'AGROPECUÁRIA': ('Agricultura, silvicultura, pesca e veterinária', '08'),
    'PRODUÇÃO GRÁFICA DIGITAL': ('Artes e humanidades', '02'),
    'BIBLIOTECONOMia': ('Ciências sociais, comunicação e informação', '03'), # Mantendo como no auxiliar
    'DANÇA': ('Artes e humanidades', '02'),
    'SEGURANÇA PRIVADA': ('Serviços', '10'),
    'TECNÓLOGO EM METALURGIA': ('Engenharia, produção e construção', '07'),
    'POLÍTICAS PÚBLICAS': ('Ciências sociais, comunicação e informação', '03'),
    'SERVIÇOS JURÍDICOS, CARTORÁRIOS E NOTARIAIS': ('Negócios, administração e direito', '04'),
    'PROPAGANDA E MARKETING': ('Negócios, administração e direito', '04'),
    'AGRONEGÓCIO': ('Agricultura, silvicultura, pesca e veterinária', '08'),
    'CONSTRUÇÃO NAVAL': ('Engenharia, produção e construção', '07'),
    'LETRAS - LÍNGUA PORTUGUESA E LITERATURAS DE LÍNGUA PORTUGUESA': ('Educação', '01'),
    'GESTÃO DE SERVIÇOS JURÍDICOS E NOTARIAIS': ('Negócios, administração e direito', '04'),
    'PAPEL E CELULOSE': ('Engenharia, produção e construção', '07'),
    'COMUNICAÇÃO PARA WEB': ('Ciências sociais, comunicação e informação', '03'),
    'PROCESSOS ESCOLARES': ('Educação', '01'),
    'EDUCAÇÃO ARTÍSTICA': ('Educação', '01'),
    'PRODUÇÃO CULTURAL': ('Artes e humanidades', '02'),
    'ACUPUNTURA': ('Saúde e bem-estar', '09'),
    'COMUNICAÇÃO SOCIAL\xa0 - RADIALISMO': ('Ciências sociais, comunicação e informação', '03'),
    'DESIGN DE ANIMAÇÃO': ('Artes e humanidades', '02'),
    'ARTES CÊNICAS': ('Artes e humanidades', '02'),
    'PILOTAGEM PROFISSIONAL DE AERONAVES': ('Serviços', '10'),
    'LOGÃ\x8dSTICA': ('Negócios, administração e direito', '04'), # Corrigindo encoding
    'ENGENHARIA DE BIOPROCESSOS E BIOTECNOLOGIA': ('Engenharia, produção e construção', '07'),
    'SECRETARIADO EXECUTIVO TRILÍNGUE': ('Negócios, administração e direito', '04'),
    'DESENVOLVIMENTO PARA WEB': ('Computação e Tecnologias da Informação e Comunicação (TIC)', '06'),
    'VISAGISMO E TERAPIAS CAPILARES': ('Serviços', '10'),
    'PRODUÇÃO PUBLICITÁRIA': ('Ciências sociais, comunicação e informação', '03'),
    'FORMAÇÃO PEDAGÓGICA DE DOCENTES PARA A EDUCAÇÃO BÁSICA E PROFISSIONAL': ('Educação', '01'),
    'GESTÃO DE NEGÓCIOS E INOVAÇÃO': ('Negócios, administração e direito', '04'),
    'GESTÃO DE NEGÓCIOS NO VAREJO': ('Negócios, administração e direito', '04'),
    'COMUNICAÇÃO SOCIAL - RELAÇÕES PÚBLICAS': ('Ciências sociais, comunicação e informação', '03'),
    'GESTÃO EMPREENDEDORA': ('Negócios, administração e direito', '04'),
    'CINEMA E AUDIOVISUAL': ('Artes e humanidades', '02'),
    'ENGENHARIA AUTOMOTIVA': ('Engenharia, produção e construção', '07'),
    'INTELIGÊNCIA ARTIFICIAL': ('Computação e Tecnologias da Informação e Comunicação (TIC)', '06'),
    'CIÊNCIAS DA ACUPUNTURA': ('Saúde e bem-estar', '09'),
    'OFTÁLMICA': ('Saúde e bem-estar', '09'),
    'ESTATÍSTICA': ('Ciências naturais, matemática e estatística', '05'),
    'RÁDIO, TV E INTERNET': ('Ciências sociais, comunicação e informação', '03'),
    'COMUNICAÇÃO EM CRIAÇÃO E DESENVOLVIMENTO DE WEB SITES E DESIGN': ('Ciências sociais, comunicação e informação', '03'),
    'TEATRO': ('Artes e humanidades', '02'),
    'GESTÃO MERCADOLÓGICA': ('Negócios, administração e direito', '04'),
    'ELETRÔNICA INDUSTRIAL': ('Engenharia, produção e construção', '07'),
    'BIG DATA E INTELIGÊNCIA ANALÍTICA': ('Computação e Tecnologias da Informação e Comunicação (TIC)', '06'),
    'ENGENHARIA FLORESTAL': ('Agricultura, silvicultura, pesca e veterinária', '08'),
    'COMUNICAÇÃO SOCIAL - RADIALISMO (RÁDIO E TV)': ('Ciências sociais, comunicação e informação', '03'),
    'LETRAS - FRANCÊS': ('Educação', '01'),
    'SERVIÇOS JUDICIAIS': ('Negócios, administração e direito', '04'),
    'TURISMO RECEPTIVO': ('Serviços', '10'),
    'MEDIAÇÃO': ('Ciências sociais, comunicação e informação', '03'),
    'GESTÃO DE RESÍDUOS SÓLIDOS': ('Engenharia, produção e construção', '07'),
    'FABRICAÇÃO MECÂNICA': ('Engenharia, produção e construção', '07'),
    'ENGENHARIA AEROESPACIAL': ('Engenharia, produção e construção', '07'),
    'DESENHO INDUSTRIAL': ('Artes e humanidades', '02'),
    'COMUNICAÇÃO DIGITAL': ('Ciências sociais, comunicação e informação', '03'),
    'QUIROPRAXIA': ('Saúde e bem-estar', '09'),
    'PODOLOGIA': ('Saúde e bem-estar', '09'),
    'MUSEOLOGIA': ('Ciências sociais, comunicação e informação', '03'),
    'VITICULTURA E ENOLOGIA': ('Agricultura, silvicultura, pesca e veterinária', '08'),
    'EDUCAÇÃO ESPECIAL': ('Educação', '01'),
    'ESTÉTICA E COSMETOLOGIA': ('Serviços', '10'),
    'ENGENHARIA CARTOGRÁFICA E DE AGRIMENSURA': ('Engenharia, produção e construção', '07'),
    'SERVIÇOS JURÍDICOS': ('Negócios, administração e direito', '04'),
    'SECRETARIADO EXECUTIVO BILINGUE - PORTUGUÊS/INGLÊS': ('Negócios, administração e direito', '04'),
    'E-COMMERCE': ('Negócios, administração e direito', '04'),
    'SERVIÇOS NOTARIAIS E REGISTRAIS': ('Negócios, administração e direito', '04'),
    'GESTÃO DE TURISMO RECEPTIVO': ('Serviços', '10'),
    'PROCESSOS METALÚRGICOS': ('Engenharia, produção e construção', '07'),
    'AGROINDUSTRIA': ('Agricultura, silvicultura, pesca e veterinária', '08'),
    'FORMAÇÃO DE DOCENTES PARA A EDUCAÇÃO BÁSICA': ('Educação', '01'),
    'MÚSICA - MÚSICA POPULAR BRASILEIRA': ('Artes e humanidades', '02'),
    'COMPUTAÇÃO EM NUVEM': ('Computação e Tecnologias da Informação e Comunicação (TIC)', '06'),
    'PRODUÇÃO SUCROALCOOLEIRA': ('Engenharia, produção e construção', '07'),
    'CIÊNCIAS DA RELIGIÃO': ('Artes e humanidades', '02'),
    'COMUNICAÇÃO E ILUSTRAÇÃO DIGITAL': ('Artes e humanidades', '02'),
    'SISTEMAS BIOMÉDICOS': ('Engenharia, produção e construção', '07'),
    'SEGURANÇA NO TRÂNSITO': ('Serviços', '10'),
    'PAISAGISMO': ('Agricultura, silvicultura, pesca e veterinária', '08'),
    'GESTÃO DO AGRONEGÓCIO': ('Agricultura, silvicultura, pesca e veterinária', '08'),
    'CIÊNCIA DE DADOS': ('Computação e Tecnologias da Informação e Comunicação (TIC)', '06'),
    'HOTELARIA HOSPITALAR': ('Saúde e bem-estar', '09'),
    'PUBLICIDADE': ('Ciências sociais, comunicação e informação', '03'),
    'CONTROLE DE OBRAS': ('Engenharia, produção e construção', '07'),
    'ENGENHARIA DE PESCA': ('Agricultura, silvicultura, pesca e veterinária', '08'),
    'GESTÃO DE STARTUP E NOVOS NEGÓCIOS': ('Negócios, administração e direito', '04'),
    'GERONTOLOGIA': ('Saúde e bem-estar', '09'),
    'COSMÉTICOS': ('Engenharia, produção e construção', '07'),
    'ENGENHARIA DE SISTEMAS': ('Engenharia, produção e construção', '07'),
    'GESTÃO INTEGRADA DE AGRONEGÓCIOS': ('Agricultura, silvicultura, pesca e veterinária', '08'),
    'LETRAS - LIBRAS': ('Educação', '01'),
    'SUCROALCOOLEIRA': ('Engenharia, produção e construção', '07'),
    'SISTEMAS DE TELECOMUNICAÇÕES': ('Engenharia, produção e construção', '07'),
    '"RÁDIO, TV E INTERNET"': ('Ciências sociais, comunicação e informação', '03'),
    'BIBLIOTECONOMIA': ('Ciências sociais, comunicação e informação', '03'), # Assumindo que "BIBLIOTECONOMia" era typo
    # --- NOMES AINDA NÃO ENCONTRADOS OU AMBÍGUOS ---
    'GESTÃO DE HOTELARIA': ('VERIFICAR MANUALMENTE', 'XX'), # Não encontrado no auxiliar
    'GESTÃO FINANCEIRA PÚBLICA': ('VERIFICAR MANUALMENTE', 'XX'), # Não encontrado no auxiliar
    'ENGENHARIA DE SEGURANÇA NO TRABALHO': ('VERIFICAR MANUALMENTE', 'XX'), # Não encontrado no auxiliar
    'COMUNICAÇÃO SOCIAL - CINEMA E VÍDEO': ('VERIFICAR MANUALMENTE', 'XX'), # Não encontrado no auxiliar
    'PRODUÇÃO DE GRAFOS': ('VERIFICAR MANUALMENTE', 'XX'), # Não encontrado no auxiliar





    # adicionado apos executar modulo3-> verificacao cursos nan, entao refeito todos csv do modulo 2 em diante( poucos refeitos)

    # --- NOVOS CURSOS (Da sua lista de 59 NaNs) ---
    'CIÊNCIAS DA COMPUTAÇÃO': ('Computação e Tecnologias da Informação e Comunicação (TIC)', '06'),
    'ENGENHARIA': ('Engenharia, produção e construção', '07'), # Geralmente o campo ENGENHARIA sem detalhe cai em 07
    'BIOLOGIA': ('Ciências naturais, matemática e estatística', '05'), # Assumindo Bacharelado/Licenciatura
    'LETRAS PORTUGUÊS E INGLÊS': ('Educação', '01'),
    'ENGENHARIA DE ENERGIAS': ('Engenharia, produção e construção', '07'),
    'PRODUÇÃO DE GRÃOS': ('Agricultura, silvicultura, pesca e veterinária', '08'),
    'INTERDISCIPLINAR EM CIÊNCIA E TECNOLOGIA': ('Ciências naturais, matemática e estatística', '05'), # Cursos Interdisciplinares caem em 05 ou 02, escolhemos 05.
    'TECNOLOGIA E DESIGN DE NEGÓCIOS': ('Negócios, administração e direito', '04'),
    'CIÊNCIA DA INFORMAÇÃO': ('Computação e Tecnologias da Informação e Comunicação (TIC)', '06'),
    'NORMAL SUPERIOR': ('Educação', '01'),
    'COMUNICAÇÃO SOCIAL - CINEMA E AUDIOVISUAL': ('Artes e humanidades', '02'),
    'COMUNICAÇÃO SOCIAL COM HABILITAÇÃO EM PUBLICID...': ('Ciências sociais, comunicação e informação', '03'), # Publicidade
    'MULTIMÍDIA': ('Artes e humanidades', '02'),
    'LETRAS - LINGUAGEM AUDIOVISUAL': ('Artes e humanidades', '02'),
    'ESTILISMO': ('Artes e humanidades', '02'), # Design de Moda/Artes
    'GESTÃO DE INVESTIMENTOS': ('Negócios, administração e direito', '04'),
    'DESENVOLVIMENTO E GESTÃO DE STARTUPS': ('Negócios, administração e direito', '04'),
    'EMPREENDEDORISMO': ('Negócios, administração e direito', '04'),
    'COACHING': ('Serviços', '10'), # Serviços/Negócios
    'PRODUÇÃO CERVEJEIRA': ('Engenharia, produção e construção', '07'), # Processos Industriais/Eng. Química
    # --- CURSOS QUE JÁ EXISTIAM NO SEU MAPA, MAS COM OUTROS NOMES/VÍRGULAS/SPACING ---
    'CIÊNCIA DA COMPUTAÇÃO': ('Computação e Tecnologias da Informação e Comunicação (TIC)', '06'), # Mesmo que CIÊNCIAS DA COMPUTAÇÃO
    # --- NOMES AMBÍGUOS OU INCOMPLETOS JÁ LISTADOS ---
    # (Mantendo apenas o que não estava no seu mapa anterior, que não enviei)
    
    # --- CURSOS COMUNS (Mantendo os que você já tinha no original como base) ---
    'ADMINISTRAÇÃO': ('Negócios, administração e direito', '04'),
    'EDUCAÇÃO FÍSICA': ('Saúde e bem-estar', '09'),
    'CIÊNCIAS CONTÁBEIS': ('Negócios, administração e direito', '04'),
    'PEDAGOGIA': ('Educação', '01'),
    'ENGENHARIA CIVIL': ('Engenharia, produção e construção', '07'),
    'DIREITO': ('Negócios, administração e direito', '04'),
    'FARMÁCIA': ('Saúde e bem-estar', '09'),
    'PSICOLOGIA': ('Ciências sociais, comunicação e informação', '03'),
    'JORNALISMO': ('Ciências sociais, comunicação e informação', '03'),
    'ODONTOLOGIA': ('Saúde e bem-estar', '09'),
    'TERAPIA OCUPACIONAL': ('Saúde e bem-estar', '09'),
    'AGRONOMIA': ('Agricultura, silvicultura, pesca e veterinária', '08'),
    # (Adicione aqui o restante dos seus mapeamentos já feitos para garantir que eles não sumam)
    
    # --- NOMES QUE PRECISAM DE LIMPEZA EXTRA (Se vierem sujos) ---
    'LOGÍSTICA': ('Negócios, administração e direito', '04'), # Exemplo de curso que precisa ser adicionado
    'SERVIÇO SOCIAL': ('Saúde e bem-estar', '09'), # Exemplo de curso que precisa ser adicionado
    
    # --- OUTROS CURSOS QUE VOCÊ JÁ TINHA MAIS OTIMIZADOS ---
    # Copie e cole o restante dos seus 100+ mapeamentos já prontos aqui!
}

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

# --- 4. Ler Individuais, Concatenar, Aplicar e Salvar ---

print(f"Lendo arquivos individuais de OFERTAS de: {path_leitura_base}")
lista_dfs = []
try:
    lista_nomes_arquivos = os.listdir(path_leitura_base)
except FileNotFoundError:
    print(f"ERRO: Diretório não encontrado: {path_leitura_base}")
    lista_nomes_arquivos = []

df_ofertas_agrupado_final = None # Inicializa como None

if not lista_nomes_arquivos:
    print("Nenhum arquivo encontrado no diretório.")
else:
    for arquivo in lista_nomes_arquivos:
        if arquivo.endswith('.csv') and 'ofertas' in arquivo:
            caminho_completo = os.path.join(path_leitura_base, arquivo)
            print(f"Lendo {arquivo}...")
            try:
                df_temp = pd.read_csv(caminho_completo, low_memory=False)
                
                # Checagem mínima de colunas
                colunas_necessarias = [coluna_chave, coluna_valor_nome, coluna_valor_cod]
                if not all(col in df_temp.columns for col in colunas_necessarias):
                    print(f"  Aviso: Colunas essenciais não encontradas em {arquivo}. Pulando.")
                    continue
                    
                lista_dfs.append(df_temp)
            except Exception as e:
                print(f"Erro ao ler {arquivo}: {e}")

if not lista_dfs:
    print("Nenhum dataframe de OFERTAS foi lido. Correção encerrada.")
else:
    # Junta todos os arquivos de ofertas em um só
    df_ofertas_agrupado_final = pd.concat(lista_dfs, ignore_index=True)
    print("Todos os arquivos de OFERTAS foram concatenados.")

    # Verifica a contagem de NaNs ANTES
    nans_antes = df_ofertas_agrupado_final[coluna_valor_nome].isnull().sum()
    print(f"\nTotal de NaNs ANTES da correção: {nans_antes}")

    if nans_antes > 0:
        print("Iniciando correção (usando .apply())... Isso pode levar alguns minutos...")
        
        # Aplicando a função linha a linha (axis=1)
        df_corrigido = df_ofertas_agrupado_final.apply(
            corrigir_linha,
            args=(mapa_correcao_manual_ofertas, coluna_chave, coluna_valor_nome, coluna_valor_cod),
            axis=1
        )
        
        # Verifica a contagem de NaNs DEPOIS
        nans_depois = df_corrigido[coluna_valor_nome].isnull().sum()
        print(f"\nTotal de NaNs DEPOIS da correção: {nans_depois}")
        print(f"Total de NaNs Corrigidos: {nans_antes - nans_depois}")

        # Ordena o DataFrame corrigido por ano/semestre (se as colunas existirem)
        try:
            # VERIFIQUE os nomes das colunas de ano/semestre para OFERTAS
            ordem = ['ano_processo_seletivo_ofertas', 'semestre_processo_seletivo_ofertas'] 
            df_corrigido.sort_values(by=ordem, inplace=True)
            print("\nDataFrame corrigido ordenado por ano/semestre.")
        except KeyError:
            print("\nColunas de ordenação (ano/semestre) não encontradas, salvando sem ordenar.")
        except Exception as e:
             print(f"\nErro ao ordenar: {e}")

        # Salva o arquivo final e corrigido
        nome_salvar = 'ofertas_agrupado_limpo_CORRIGIDO.csv' # <-- Nome ajustado
        # Salvar na pasta correta do módulo 2 para ofertas
        path_save_base = '../../../planilhas/limpo/modulo_2/ajustar_nan_cine_ofertas/' 
        os.makedirs(path_save_base, exist_ok=True)
        caminho_salvar = os.path.join(path_save_base, nome_salvar)
        
        print(f"\nSalvando arquivo corrigido em: {caminho_salvar}")
        df_corrigido.to_csv(caminho_salvar, index=False, encoding='utf-8-sig')
        
        print("\n--- Processo de correção para OFERTAS concluído! ---")
        
        if nans_depois > 0:
            print(f"\nAinda restaram {nans_depois} NaNs.")
            print("Verifique os nomes marcados como 'VERIFICAR MANUALMENTE' no dicionário")
            print("e outros erros de digitação/nomes não encontrados no auxiliar.")

    else:
        print("Nenhum NaN encontrado. Nenhum processo de correção foi necessário.")

# %%