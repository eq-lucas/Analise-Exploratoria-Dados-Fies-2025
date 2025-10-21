# Análise Exploratória de Dados - FIES Computação (2019-2021)

Projeto de Iniciação Científica (IC) realizado na **Universidade Tecnológica Federal do Paraná (UTFPR)**, focado na análise dos microdados públicos do Fundo de Financiamento Estudantil (FIES) para a área de Computação.

---

## Objetivo do Projeto

O objetivo principal foi **estruturar um pipeline de dados** para transformar um grande volume de dados brutos e inconsistentes em datasets analíticos e visualizações, permitindo a extração de conclusões estratégicas sobre a dinâmica do programa.

---

## Tecnologias Utilizadas

- **Linguagem:** Python  
- **Bibliotecas:** Pandas, Matplotlib, Seaborn, entre outras 
- **Ambiente:**  VS Code com Jupyter  

---

## Estrutura do Repositório

A organização das pastas garante que o pipeline de dados seja reproduzido de forma clara e ordenada.

```plaintext
├── analises/                 # Subpastas com códigos e gráficos
│
├── planilhas/                # Estrutura do fluxo ETL
│   │
│   ├── bruto/                # Dados originais recebidos
│   │   ├── com_erro/         # Arquivos com inconsistências
│   │   ├── sem_duplicata/    # Arquivos após remoção de duplicatas
│   │   └── fonte/            # Arquivos "FIES" da fonte
│   │
│   ├── externo/              # datasets externos utilizados
│   │
│   ├── limpo/                # Dados normalizados (colunas, tipos, nomes)
│   └── processado/           # Dados prontos para análise (ETL aplicado)
│
└── pipeline_inicial.py/      # Instruções iniciais
```
---

## Como Replicar a Análise

1. **Ambiente e Dependência**

Para rodar a análise, recomenda-se criar um ambiente virtual e instalar as dependências listadas em `requirements.txt`:

Na raiz do projeto, execute:

```bash

python3 -m venv venv

source venv/bin/activate   # Linux/Mac

venv\Scripts\activate      # Windows
```

Depois, instale as dependências do projeto:

```bash
pip install -r requirements.txt
```

---

2. **Download dos Dados Brutos**  

   - Acesse o [Portal de Dados Abertos do MEC](https://dadosabertos.mec.gov.br/fies).  
   - Baixe os arquivos `.csv`.
   - Foram considerados os arquivos de **Inscrições** e **Ofertas**, no período de **2019 a 2021**.

---

3. **Preparação e Limpeza Inicial**  


1. Mova os arquivos `.csv` baixados para a **raiz do projeto**.  
2. Execute o script de pipeline_inicial.py de renomeação/movimentação/correção


Este script realiza:  

- Move os arquivos de **Inscrições** e **Ofertas** para `planilhas/bruto/fonte`.  
- Coloca arquivos específicos com problemas, como `resultado de inscricoes fies 2020/1`,
 em `planilhas/bruto/com_erro/`.

- Lê os arquivos brutos de `planilhas/bruto/fonte/`.  
- Remove linhas duplicadas.  
- Salva os arquivos limpos em `planilhas/bruto/fonte/sem_duplicata` no formato:

- '<ano>_inscricoes_<semestre>_sem_duplicata.csv'
- '<ano>_ofertas_<semestre>_sem_duplicata.csv'

---

4. **Próximos Passos**

Após a limpeza, os arquivos já estão prontos para serem utilizados.


