#%%

# importamos librerias para manejo datos
import pandas as pd
from IPython.display import display

#%%

def visualizacion_datos(df): 
    print('VISUALIZACIÓN RÁPIDA DE LOS DATOS:')
    print('--' * 17)
    display(df.head(3))
    display(df.tail(3))
    display(df.sample(3))
    print('--' * 120)
    print(f'El número de filas es de {df.shape[0]} y el número de columnas es de {df.shape[1]}.')
    print('Las diferentes columnas que tenemos son:')
    num = 0
    for i in df.columns: 
        num +=1
        print(f'    {num}. {i}')
    print('--' * 120)
    print('INFORMACIÓN DEL CONJUNTO DE DATOS:')
    print('--' * 17)
    df.info()

#%%

def variables_nulas(df): 
    nulos = (df.isnull().sum()/df.shape[0]*100).reset_index()
    #nulos.sort_values(ascending=False)
    nulos.rename(columns={'index': 'columna', 0:'%_nulos'}, inplace=True)
    mascara = nulos['%_nulos'] > 0

    if nulos['%_nulos'].sum() == 0: 
        print('Ninguna columna tiene valores nulos. Puedes continuar con tu estudio.')
    else: 
        col_nulos = nulos.loc[nulos['%_nulos']!=0, 'columna'].to_list() 
        display(round(nulos[mascara].sort_values(by='%_nulos', ascending=False), 4))
        print('Las siguientes columnas tienen valores nulos:')
        for i in col_nulos:
            print(f'      - {i}')
        return col_nulos
    
#%%   

def duplicados_ver(df, list_sort_by):
    duplicados = df.duplicated()
    print("Número de filas duplicadas:", duplicados.sum())
    mascara = df.duplicated(keep=False)
    display(df[mascara].sort_values(by = list_sort_by))

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

# USO: Devuelve tablas con las diferentes categorias de las columnas que encontramos en el dataframe. Devolverá tantas 
# tablas como columnas haya en el dataframe. 
def categorias(df): 
    for col in df.select_dtypes(include='O').columns:
        print(f"Las categorías que tenemos para la columna {col} son:")
        display(df[col].value_counts().reset_index())
        print('_' * 100)

# %%
