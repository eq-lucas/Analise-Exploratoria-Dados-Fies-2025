# %%
import pandas as pd

path = "planilhas ETL/GERAL ETL inscritos.csv"

df = pd.read_csv(path,decimal=',')

df.columns.to_list()
# %%

# %%
