# Preparação dos Dados - FIES Computação (2019-2021)

Este guia detalha como preparar os arquivos brutos do FIES para análise, incluindo download, movimentação, renomeação e limpeza dos arquivos.

---

## 1. Download dos Arquivos

1. Acesse o [Portal de Dados Abertos do MEC](https://dadosabertos.mec.gov.br/fies).  
2. Baixe os arquivos `.csv` correspondentes a **Inscrições** e **Ofertas**, período **2019-2021**.  
3. Salve todos os arquivos na pasta `Downloads` do seu computador.

---

## 2. Criar Ambiente Virtual

Na raiz do projeto, execute:

```bash
python3 -m venv venv
source venv/bin/activate   # Linux/Mac
venv\Scripts\activate      # Windows
´´´

Depois, instale as dependências do projeto:

´´´bash
pip install -r README/requirements.txt
´´´

## 3. Movimentação e Renomeação Inicial dos Arquivos

1. Mova os arquivos `.csv` da pasta `Downloads` para a **raiz do projeto**.  
2. Execute o script de PASSOS_INICIAIS.py de renomeação/movimentação (presente na pasta `README/`).  

Este script realiza:  
- Move os arquivos de **Inscrições** para `csv originais/INSCRICOES`.  
- Move os arquivos de **Ofertas** para `csv originais/OFERTAS`.  
- Coloca arquivos específicos com problemas, como `resultado de inscricoes fies 2020/1`,
 em `csv_originais/DATASETS COM ERROS`.

---

## 4. Limpeza dos Arquivos de Inscrições

Após a movimentação inicial, execute o script `limpar_inscricoes.py` (presente na pasta `README/`).  

Este script faz o seguinte:  
- Lê os arquivos brutos de `csv_originais/INSCRICOES`.  
- Remove linhas 100% duplicadas.  
- Salva os arquivos limpos em `csv_originais/INSCRICOES CORRIGIDAS` no formato:

<ano>_inscricoes_<semestre>.csv'

## 5. Próximos Passos

Após a limpeza, os arquivos em INSCRICOES CORRIGIDAS já estão prontos para serem utilizados,
em análise e visualização na pasta "ANALISES".