# Análise Exploratória de Dados - FIES Computação (2019-2021)

Projeto de Iniciação Científica (IC) realizado na **Universidade Tecnológica Federal do Paraná (UTFPR)**, focado na análise dos microdados públicos do Fundo de Financiamento Estudantil (FIES) para a área de Computação.

---

## Estrutura do Repositório

A organização das pastas garante que o pipeline de dados seja reproduzido de forma clara e ordenada.

```plaintext
raiz do projeto .
├── Analises/               # Subpastas com códigos e gráficos
├── csv originais/          # Arquivos brutos e processados
│   ├── DATASETS COM ERROS/
│   ├── INSCRICOES/
│   ├── INSCRICOES CORRIGIDAS/
│   └── OFERTAS/
├── planilhas/              # Datasets finais analíticos
├── planilhas ETL/          # Datasets originais organizados
├── Outros/                 # Materiais de apoio
│   ├── 1 INFORMACOES/
│   ├── dataset extras/
│   └── FIES FUNCIONAMENTO/ # funcionamento da pessoa ir atras do fies, ate ser efetivada
└── README/                 # Instruções iniciais
```
---

## Como Replicar a Análise

1. **Download dos Dados Brutos**  
   - Acesse o [Portal de Dados Abertos do MEC](https://dadosabertos.mec.gov.br/fies).  
   - Baixe os arquivos `.csv`.
   - Foram considerados os arquivos de **Inscrições** e **Ofertas**, no período de **2019 a 2021**.


2. **Ambiente e Dependência**

Para rodar a análise, recomenda-se criar um ambiente virtual e instalar as dependências listadas em `README/requirements.txt`.
 

3. **Preparação e Limpeza Inicial**  

  -As pastas já estão criadas no repositório (mantidas via .gitkeep).

    (Um guia detalhado será disponibilizado em README/PREPARACAO_DADOS.md).

---


## Objetivo do Projeto

O objetivo principal foi **estruturar um pipeline de dados** para transformar um grande volume de dados brutos e inconsistentes em datasets analíticos e visualizações, permitindo a extração de conclusões estratégicas sobre a dinâmica do programa.

---


## Tecnologias Utilizadas

- **Linguagem:** Python  
- **Bibliotecas:** Pandas, Matplotlib, Seaborn, entre outras 
- **Ambiente:**  VS Code com Jupyter  
