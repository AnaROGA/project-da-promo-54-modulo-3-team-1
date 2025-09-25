#%%

# importamos librerias para manejo datos
import pandas as pd
from IPython.display import display


#%%

def variables_nulas(df): 
    nulos = (df.isnull().sum()/df.shape[0]*100).reset_index()
    nulos.rename(columns={'index': 'columna', 0:'%_nulos'}, inplace=True)
    mascara = nulos['%_nulos'] > 0

    if nulos['%_nulos'].sum() == 0: 
        print('Ninguna columna tiene valores nulos. Puedes continuar con tu estudio.')
    else: 
        col_nulos = nulos.loc[nulos['%_nulos']!=0, 'columna'].to_list() 
        display(nulos[mascara].sort_values(ascending=False))
        for i in col_nulos:
            print(f'La siguiente columna tiene valores nulos: {i}')
        return col_nulos
    
#%%   

def duplicados_ver(df, list_sort_by):
    duplicados = df.duplicated()
    print("Número de filas duplicadas:", duplicados.sum())
    mascara = df.duplicated(keep=False)
    display(df[mascara].sort_values(by = list_sort_by))

#%% 
dicc = {
    'a':[1,2,3],
    'b':[1,2,3] }
df_dicc= pd.DataFrame(dicc)

duplicados_ver(df_dicc, ['b'])

#%% 

def func_duplicados(df): 
    if df.duplicated().sum() > 0:
        print(f'El número de filas es de {df.shape[0]}')
        print(f'El número de duplicados es: {df.duplicated().sum()}.')
        print('Borrando duplicados...')
        df.drop_duplicates(inplace = True)
        print(f'Se han eliminado los duplicados.')
        print(f'Comprobando que el número de duplicados sea cero.')
        print(f'Comprobación: {df.duplicated().sum()}')
        print(f'Ahora el número de filas es: {df.shape[0]}')
    else: 
        print('Este dataframe no tiene duplicados.')
    
# %%
