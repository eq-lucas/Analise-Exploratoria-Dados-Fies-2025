# %%
import os
import pandas as pd

pd.set_option('display.max_columns', None)


arquivos_csv = []

for f in os.listdir("."):
    if f.endswith(".csv"):
        arquivos_csv.append(f)

print(arquivos_csv,'\n\n')

arquivos_csv.sort()

for arq in arquivos_csv:
    print(arq)



# %%

for arquivo in arquivos_csv:
    caminho = os.path.join(".", arquivo)
    df = pd.read_csv(caminho)
    
    print("\nO caminho eh: ",caminho)
    display(df)

    print("\n\n\n")

# %%
