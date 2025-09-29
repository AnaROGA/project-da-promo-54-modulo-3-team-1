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
    df_copia = df.copy()

    if df_copia.duplicated().sum() > 0:
        print(f'El número de filas es de {df_copia.shape[0]}')
        print(f'El número de duplicados es: {df_copia.duplicated().sum()}.')
        print('Borrando duplicados...')
        df_copia.drop_duplicates(inplace = True)
        print(f'Se han eliminado los duplicados.')
        print(f'Comprobando que el número de duplicados sea cero.')
        print(f'Comprobación: {df_copia.duplicated().sum()}')
        print(f'Ahora el número de filas es: {df_copia.shape[0]}')
    else: 
        print('Este dataframe no tiene duplicados.')

    return df_copia
    
# %%

# USO: Devuelve tablas con las diferentes categorias de las columnas que encontramos en el dataframe. Devolverá tantas 
# tablas como columnas haya en el dataframe. 
def categorias(df):
    for col in df.select_dtypes(include='O').columns:
        print(f"Las categorías que tenemos para la columna {col} son:")
        display(df[col].value_counts().reset_index())
        print('_' * 100)


# %%

def imputacion_categorica(df, col_imput, col_ref, dic):
    """
    Imputa valores faltantes en 'col_imput' con ayuda de un diccionario que mapea valores de 'col_ref'.
    
    Parámetros
    ----------
    df : pd.DataFrame
        DataFrame de entrada
    col_imput : str
        Columna objetivo donde se imputan nulos.
    col_ref : str
        Columna de referencia para buscar el valor imputado según 'dic'.
    dic : dict
        Diccionario de mapeo: clave = valor en col_ref, valor = imputación para col_imput

    
    Retorna
    -------
    pd.DataFrame

    """
    df_copia = df.copy()

    # Normalizar columna jobrole
    df_copia[col_ref] = df_copia[col_ref].str.strip().str.lower()
    # Normalizar claves del diccionario también
    dict_clean = {k.lower().strip(): v for k, v in dic.items()}
    # Aplicar el mapping
    df_copia[col_imput] = (
        df_copia[col_ref].map(dict_clean).fillna(df_copia[col_imput]))
    
    porc_nulo = round(df_copia[col_imput].isnull().sum()/df_copia[col_imput].shape[0]*100, 2)

    display(df_copia[[col_ref, col_imput]].head(10))

    if porc_nulo > 0: 
        print(f'No se han imputado todas las filas de la columna {col_imput}.')
        print(f'Comprueba si hay algún error en el diccionario el porcentaje de nulos es del {porc_nulo}%')
    else: 
        print(f'Se han imputado todas las filas de la columna {col_imput}.')

    return df_copia

# %%

# USO: realiza la limpieza de los datos que se encuentran en la columna a limpiar. Se le tiene 
# que pasar los siguientes parametros a la función: 
#   - df -> dataframe
#   - col_limpiar -> columna a limpiar (str)
#   - limp -> lo que se quiere quitar o lipiar de los datos (str)
#   - transf -> por lo que se quiere sustituir (str)  
def limpiar(df, col_limpiar, limp, transf): 
    """
    Limpia los datos de una o varias columnas del DataFrame.
    
    Parámetros
    ----------
    df : pd.DataFrame
        DataFrame de entrada
    col_limpiar : str o list
        Nombre(s) de la(s) columna(s) a limpiar.
    limp : str o list
        Lo que se quiere quitar o limpiar de los datos.
    transf : str o list
        Por lo que se sustituye lo anterior. 
    
    Retorna
    -------
    pd.DataFrame
        DataFrame con los datos de las columnas deseadas limpios.
    """

    df_copia = df.copy()

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
        df_copia[c] = df_copia[c].astype(str)

        if len(limp) != len(transf): 
            print(f'ERROR: "limp" y "transf" deben tener la misma longitud (columna {c})')
            continue

        for l, t in zip(limp, transf): 
            df_copia[c] = df_copia[c].str.replace(l, t, regex = False)
        
        print(f"Limpiezas aplicada en la columna '{c}'.")

    return df_copia

# %%

def columnas_a_eliminar(df, cols): 
    """
    Elimina una o varias columnas de un DataFrame.
    
    Parámetros
    ----------
    df : pd.DataFrame
        DataFrame de entrada
    cols : str o list
        Nombre(s) de la(s) columna(s) a eliminar. 
    
    Retorna
    -------
    pd.DataFrame
        DataFrame sin las columnas eliminadas.
    """
    df_copia = df.copy()

    if isinstance(cols, str):
        cols = [cols]
    # Verificar que las columnas existen en el dataframe
    cols_exis = [c for c in cols if c in df_copia.columns]
    cols_no_encontradas = [c for c in cols if c not in df_copia.columns]

    if cols_no_encontradas: 
        print(f'ADVERTENCIA: estas columnas no existen en el DataFrame: {cols_no_encontradas}')

    df_copia = df_copia.drop(columns = cols_exis)
    
    if cols_exis: 
        print('¡Columnas eliminadas con éxito!')
        print(f'Se eliminaron las siguientes {len(cols_exis)} columnas: {cols_exis}')
        print(f'El DataFrame ahora tiene {df_copia.shape[1]} columnas.')   
    
    
    return df_copia
# %%

def imputacion_conversion_datos_numericos(df, cols, dic_mapeo, redondeo=0):
    """
    Convierte columnas con valores de texto a números usando un diccionario de mapeo.
    Permite redondear y convertir a enteros si se desea.
    
    Parámetros
    ----------
    df : pd.DataFrame  
        DataFrame de entrada
    cols : str o list  
        Columna(s) a procesar
    dic_mapeo : dict  
        Diccionario de mapeo {texto: número}
    redondeo : int, default integer  
        Número de decimales a redondear (0 = enteros)
    
    Retorna
    -------
    pd.DataFrame
        DataFrame con columnas convertidas
    """
    df_copia = df.copy()

    # Normalizar columnas
    if isinstance(cols, str):
        cols = [cols]

    for col in cols:
        # 1. Reemplazar texto por números según diccionario
        df_copia[col] = df_copia[col].replace(dic_mapeo)

        # 2. Convertir a numérico
        df_copia[col] = pd.to_numeric(df_copia[col], errors="coerce")

        # 3. Redondear según necesidad
        if redondeo == 0:
            df_copia[col] = df_copia[col].round(redondeo).astype("Int64")
        else:
            df_copia[col] = df_copia[col].round(redondeo)

        print(f"Columna '{col}' procesada:")
        print(df_copia[col].head(10))
        print(f"Tipo final: {df_copia[col].dtype}\n")

    return df_copia

# %%

def imputacion_conversion_datos_categoricos(df, cols, dic_mapeo):
    """
    completar
    """
    df_copia = df.copy()

    if isinstance(cols, str): 
        cols = [cols]

    for col in cols: 
        df_copia[col] = df_copia[col].replace(dic_mapeo)

        print(f"Columna '{col}' estandarizada.")
        print(f"\nNuevo conteo de '{col}':")
        print(df_copia[col].value_counts())
        print('_' * 100)

    return df_copia