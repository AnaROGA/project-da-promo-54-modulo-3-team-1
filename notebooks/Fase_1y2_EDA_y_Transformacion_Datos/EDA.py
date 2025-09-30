#%%

# importamos librerias para manejo datos
import pandas as pd
from IPython.display import display
from typing import Any

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

def limpiar(df: pd.DataFrame, col_limpiar: str | list[str], limp: str | list[str], transf: str | list[str]) -> pd.DataFrame: 
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
        En el caso de que sea una variable numérica, después habrá que hacer EDA.columnas_a_numerico()
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

def columnas_a_eliminar(df: pd.DataFrame, cols: str | list[str]) -> pd.DataFrame: 
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

def imputacion_conversion_datos_numericos(df: pd.DataFrame, cols: str | list[str], dic_mapeo: dict, 
                                          redondeo: int = 0, tipo: bool = True) -> pd.DataFrame:
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
        Número de decimales a redondear (0 = enteros). 
        Solo tiene sentido si tipo = True (por defecto)
    tipo : bool, default True
        Si True, la conversión es de texto a números. 
        Si False, la conversión es de números a texto. 
    
    Retorna
    -------
    pd.DataFrame
        DataFrame con columnas convertidas
    """
    df_copia = df.copy()

    # Normalizar columnas
    if isinstance(cols, str):
        cols = [cols]

    if tipo: 

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
            print('_' * 100)
    else: 
        for col in cols: 
            df_copia[col] = (
                df_copia[col]
                .astype(float) # Necesario si hay NaN y queremos convertir a int
                .round() 
                .astype('object') # Convertir a Object/String para poder hacer el reemplazo por texto
                .replace(dic_mapeo)
            )

            print(f"Columna '{col}' procesada:\n")
            # El conteo con dropna=False te mostrará también si quedan valores NaN
            print(df_copia[col].value_counts(dropna=False))
            print('_' * 100)

    return df_copia

# %%

def imputacion_conversion_datos_categoricos(df: pd.DataFrame, cols: str | list[str], dic_mapeo: dict) -> pd.DataFrame:
    """
    Convierte columnas con textos erroneos a textos correctos usando un diccionario de mapeo.
    
    Parámetros
    ----------
    df : pd.DataFrame  
        DataFrame de entrada
    cols : str o list  
        Columna(s) a procesar
    dic_mapeo : dict  
        Diccionario de mapeo {texto_error: texto_corregido}

    Retorna
    -------
    pd.DataFrame
        DataFrame con columnas corregidas
    """
    df_copia = df.copy()

    if isinstance(cols, str): 
        cols = [cols]

    for col in cols: 
        df_copia[col] = df_copia[col].replace(dic_mapeo)

        print(f"Columna '{col}' estandarizada.")
        print(f"\nNuevo conteo de '{col}':")
        print(df_copia[col].value_counts(dropna=False))
        print('_' * 100)

    return df_copia

# %%

def columnas_a_numerico(df: pd.DataFrame, cols: str | list[str], cast_enteros: bool = True) -> pd.DataFrame:
    """
    Convierte columnas del DataFrame a tipo numérico usando pd.to_numeric(errors='coerce').

    Parámetros
    ----------
    df : pd.DataFrame
        DataFrame de entrada.
    cols : str o list[str]
        Columna(s) a convertir.
    cast_enteros : bool, default True
        Si True, si una columna resulta sin decimales (solo enteros o NaN),
        se castea a 'Int64' (enteros que admiten NaN). Si no, queda en float64.

    Retorna
    -------
    pd.DataFrame
        DataFrame con la(s) columna(s) indicada(s) convertida(s) a numérica(s).
    """
    df_copia = df.copy()

    if isinstance(cols, str):
        cols = [cols]

    for c in cols:
        serie_num = pd.to_numeric(df_copia[c], errors="coerce")

        if cast_enteros and serie_num.dropna().apply(lambda x: float(x).is_integer()).all():
            df_copia[c] = serie_num.astype("Int64")
        else:
            df_copia[c] = serie_num.astype("float64")
        
        print(f"'{c}' convertida a numérica")
        print(df_copia[c].value_counts(dropna=False))
        print(df_copia[c].dtype)
        print('_' * 100)

    return df_copia

# %%

def normalizacion_datos(df: pd.DataFrame, cols: str | list[str], capitalizar: bool = False ) -> pd.DataFrame: 
    """
    Normaliza texto en una o varias columnas: pasa a minúsculas, elimina espacios extra 
    (incluidos múltiples espacios internos) y, opcionalmente, capitaliza  cada palabra.

    Parámetros
    ----------
    df:
        pd.DataFrame
        DataFrame de entrada.

    cols:
        str o list[str]
        Columna(s) a normalizar.
    
    capitalizar:
        bool, default False
        Si False, no capitaliza cada una de las palabras del texto en los datos del DataFrame.
        Si True, capitaliza cada una de las palabras del texto en los datos del DataFrame.

    Retorna
    -------
    pd.DataFrame
        DataFrame con la(s) columna(s) indicada(s) normalizada(s).
    """
    df_copia = df.copy()
    
    if isinstance(cols, str):
        cols = [cols]

    for c in cols: 
        #Convertir a minúsculas y eliminar espacios extra
        df_copia[c] = df_copia[c].str.lower().str.strip()

        #Reemplazo de caracteres especiales y estandarización
        # Reemplazar múltiples espacios internos con un solo espacio (por si acaso)
        df_copia[c] = df_copia[c].str.replace(r'\s+', ' ', regex=True)

        print(f"Columna '{c}' normalizada a minúsculas y sin espacios extra.")

        if capitalizar:
            df_copia[c] = df_copia[c].astype('string').str.title()
            print(f"Columna '{c}' capitalizadas.")

        # Muestra los nuevos valores únicos para verificar la limpieza
        print("\nConteo de valores únicos después de la normalización:")
        print(df_copia[c].value_counts())
        print('_' * 100)

    return df_copia

# %%

def imputar_na(df: pd.DataFrame, cols: str | list[str], imputar_por: Any) -> pd.DataFrame: 
    """
    Imputa valores nulos en una o varias columnas de un DataFrame. Reemplaza los valores NaN
    en las columnas indicadas por un valor fijo especificado.

    Parámetros
    ----------
    df : pd.DataFrame
        DataFrame de entrada.
    cols : str o list[str]
        Nombre de la columna o lista de columnas en las que se quiere imputar.
    imputar_por : any
        Valor con el que se reemplazarán los NaN (puede ser str, int, float, etc.).

    Retorna
    -------
    pd.DataFrame
        DataFrame con los valores nulos imputados en las columnas seleccionadas.

    """
    df_copia = df.copy()

    if isinstance(cols, str):
        cols = [cols]

    for col in cols: 
        if col not in df_copia.columns:
            print(f'Columnas no encontradas en el DataFrame: {col}')
            continue

        df_copia[col] = df_copia[col].fillna(imputar_por)
        print(f"Nulos en variable '{col}' imputado con '{imputar_por}'")
        print(df_copia[col].value_counts(dropna=False))
        print("_" * 100)

    return df_copia
# %%
