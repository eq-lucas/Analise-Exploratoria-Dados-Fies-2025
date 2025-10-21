# README - MÓDULO 1: Preparação e Limpeza de Dados

Este módulo contém os scripts para a primeira etapa do projeto de Iniciação Científica: a preparação, limpeza e consolidação dos dados brutos do FIES (2019-2021).

O objetivo é transformar os 12 arquivos CSV "brutos" (6 de ofertas, 6 de inscrição) da pasta `bruto/sem_duplicata/` em 2 arquivos CSV "mestres" limpos e normalizados, que serão salvos em `limpo/modulo_1/`.

## Dependências de Arquivos Externos (Estratégia Mestre Corrigida)

Para enriquecer nossos dados do FIES com a classificação **CINE (Grande Área do Conhecimento)**, a estratégia de merge precisa ser robusta para evitar NaNs. Faremos isso construindo um **Dataset Mestre de Cursos** que combina todos os anos disponíveis + um ajuste manual.

Siga estas instruções **exatamente** para obter os arquivos necessários:

### 1. Acesse o Portal do INEP e Baixe os Dados

* Vá para a página oficial de [Microdados do Censo da Educação Superior](https://www.gov.br/inep/pt-br/acesso-a-informacao/dados-abertos/microdados/censo-da-educacao-superior).
* Procure pela seção e baixe os arquivos principais (`.zip`) dos Censos de **2016 até 2024**.

### 2. Prepare e Mova os Arquivos de Cadastro

1.  Descompacte **todos** os arquivos `.zip` baixados.
2.  Mova as pastas anuais descompactadas (ex: `Microdados do Censo da...{ano}`) para a pasta **`planilhas/externo/`** do seu projeto.
3.  Execute o script Python de movimentação e limpeza que esta localizado na pasta 3 do modulo_1 onde faz a adoção da coluna. Este script irá:
    * Procurar as pastas anuais dentro de `planilhas/externo/`.
    * Mover os arquivos **`MICRODADOS_CADASTRO_CURSOS_{year}.CSV`** e **`MICRODADOS_CADASTRO_IES_{year}.CSV`** para a raiz de `planilhas/externo/`.
    * Renomear a extensão para **`.csv`**.
    * **EXCLUIR** as pastas anuais de origem (limpando a pasta `planilhas/externo`).

### Propósito dos Arquivos Externos

* **`MICRODADOS_CADASTRO_CURSOS_{year}.csv` (Obrigatório):**
    * **ESTRATÉGIA:** Todos estes arquivos serão concatenados (juntos) para criar um **Dataset Mestre de Cursos** único.
    * **CHAVES:** Este Dataset Mestre será usado para fazer o `pd.merge` usando a coluna `CO_CURSO` (código do curso) com os datasets do FIES (`codigo_curso_inscricao` ou `codigo_curso_ofertas`).
    * **COLUNAS DESEJADAS:** Serão extraídas: `CO_CURSO`, `NO_CURSO`, `CO_CINE_AREA_GERAL`, e `NO_CINE_AREA_GERAL`. O uso de uma base mestre garante que o máximo possível de NaNs seja corrigido.

* **`MICRODADOS_CADASTRO_IES_{year}.csv` (Opcional):**
    * Contém informações cadastrais sobre as Instituições (Faculdades, Universidades). Pode ser usado futuramente para enriquecer os dados.
