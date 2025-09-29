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

# USO: realiza la imputación de datos faltantes con ayuda de un diccionario creado previamente. Se le tiene 
# que pasar los siguientes parametros a la función: 
#   - df -> dataframe
#   - col_imput -> columna a imputar (str)
#   - col_ref -> columna de referencia para la columna a imputar (str)
#   - dic -> diccionario creado previamente  

def imputacion_categorica(df, col_imput, col_ref, dic): 
    # Normalizar columna jobrole
    df[col_ref] = df[col_ref].str.strip().str.lower()
    # Normalizar claves del diccionario también
    dict_clean = {k.lower().strip(): v for k, v in dic.items()}
    # Aplicar el mapping
    df[col_imput] = (
        df[col_ref].map(dict_clean).fillna(df[col_imput]))
    
    porc_nulo = round(df[col_imput].isnull().sum()/df[col_imput].shape[0]*100, 2)

    display(df[[col_ref, col_imput]].head(10))

    if porc_nulo > 0: 
        print(f'No se han imputado todas las filas de la columna {col_imput}.')
        print(f'Comprueba si hay algún error en el diccionario el porcentaje de nulos es del {porc_nulo}%')
    else: 
        print(f'Se han imputado todas las filas de la columna {col_imput}.')


# %%

# USO: realiza la limpieza de los datos que se encuentran en la columna a limpiar. Se le tiene 
# que pasar los siguientes parametros a la función: 
#   - df -> dataframe
#   - col_limpiar -> columna a limpiar (str)
#   - limp -> lo que se quiere quitar o lipiar de los datos (str)
#   - transf -> por lo que se quiere sustituir (str)  
def limpiar(df, col_limpiar, limp, transf): 
    if type(limp) == str: 
        limp = [limp]
    if type(transf) == str: 
        transf = [transf]
    
    if type(col_limpiar) == list: 
        cols = col_limpiar
    elif type(col_limpiar) == str: 
        cols = [col_limpiar]
    else:
        print('ERROR: Tipo no válido en col_limpiar.')
    
    for c in cols: 
        df[c] = df[c].astype(str)

        if len(limp) != len(transf): 
            print(f'ERROR: "limp" y "transf" deben tener la misma longitud (columna {c})')
            continue

        for l, t in zip(limp, transf): 
            df[c] = df[c].str.replace(l, t, regex = False)
        
        print(f'Limpiezas aplicada en la columna {c}')

    display(df.head(10))

# %%

# USO: Eliminar una o varias columnas de un DataFrame
def columnas_a_eliminar(df, cols): 
    if isinstance(cols, str):
        cols = [cols]
    # Verificar que las columnas existen en el dataframe
    cols_exis = [c for c in cols if c in df.columns]
    cols_no_encontradas = [c for c in cols if c not in df.columns]

    if cols_no_encontradas: 
        print(f'ADVERTENCIA: estas columnas no existen en el DataFrame: {cols_no_encontradas}')

    if cols_exis: 
        print('¡Columnas eliminadas con éxito!')
        print(f'Las columnas eliminadas son: {cols_exis}')   
    
    df = df.drop(columns = cols_exis)
    return df