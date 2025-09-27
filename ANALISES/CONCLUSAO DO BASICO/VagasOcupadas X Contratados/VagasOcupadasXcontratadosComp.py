# %%
import pandas as pd

path = '../planilhas basico/COMP CONTRATADOS.csv'

path2 = '../planilhas basico/Total_Vagas_OcupadasComp.csv'

dfi= pd.read_csv(path)

dfo= pd.read_csv(path2)



# %%
# da errado!
#df=pd.DataFrame(columns=dfi.columns.tolist(),index=dfi.index.tolist())

#def subtracao(x:pd.Series):
    #for string,i in range(enumerate(x.index.to_list())):
        #x.iloc[i]= dfo.iloc[i,string]-dfi.iloc[j,string]
   # return x

#df_limpo= df.apply(subtracao,axis=1)



# %%


dfo= dfo.set_index(['ano','semestre'])
dfi= dfi.set_index(['ano','semestre'])

# %%


df= dfo- dfi

df= df.reset_index()
df
# %%
df.to_csv('../planilhas basico/VagasOcupadasXcontratadosComp.csv',index=False)
# %%
