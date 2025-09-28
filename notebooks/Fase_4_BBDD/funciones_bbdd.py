#%%

# importamos las bibliotecas y conectores necesarios

import mysql.connector
from mysql.connector import errorcode

import pandas as pd

# Importamos nuestra librería de soporte
import funciones_soporte_queries as query

# %%

# conectamos Phyton a mySQL con manejo de errores

def conexion_servidor(password):  # 'AlumnaAdalab'
    try:
        # Intenta hacer la conexión con SQL
        cnx = mysql.connector.connect(
            user='root',
            password= password,
            host='127.0.0.1'
        )
        print("¡Conexión exitosa a MySQL!\n Variable 'cnx' creada.") # si es exitosa lo informa
        return cnx  #la conexión queda abierta

    # definimos los posibles errores y su manejo
    except mysql.connector.Error as err:
        # Si es un error de acceso denegado (ej. contraseña o usuario incorrecto)
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Algo está mal con tu nombre de usuario o contraseña.") # informa el error encontrado
        # Si la base de datos no existe
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("La base de datos no existe.") # informa el error encontrado
        # Para cualquier otro tipo de error
        else:
            print(err) # informa del error
            print("Código de Error:", err.errno) # informa el código del error
            print("SQLSTATE", err.sqlstate) # informa el estado de conexión
            print("Mensaje", err.msg)


# %%    

# Creación BASE DE DATOS:

def creacion_bbdd(cnx,query_creacion_bbdd, query_movernos_bbdd):
    mycursor = cnx.cursor()   # creamos nuestro cursor (nos abre mysql)
    
    try:
        mycursor.execute(query_creacion_bbdd)
        print(f"BBDD creada correctamente.")
        mycursor.execute(query_movernos_bbdd) # Nos movemos a esa bbdd
        print(f"Variable 'mycursor' creada.")
        return mycursor
    except:
        print(f"No ha sido posible crear la base de datos.")

# %%    

def acceso_bbdd(cnx,sql_bbdd):  # USE nombre_bbdd
    mycursor = cnx.cursor()   # creamos nuestro cursor (nos abre mysql)
    print(f"Variable 'mycursor' creada.")
    try:
        mycursor.execute(sql_bbdd)
        print(f"Estamos en la bbdd indicada")
        return mycursor
    except:
        print(f"No ha sido posible moverse a la base de datos indicada.")


# %%

def creacion_tablas(mycursor, *args): # para meter tantas queries como queramos
    num_tablas = 0
    try:
        for query in args:
            mycursor.execute(query)
            num_tablas += 1
            print(f"{num_tablas} tabla/s creada/s con exito.")
    except:
        print("No se ha/n podido crear la/s tabla/s.")

# %%

def insercion_tabla_artistas(mycursor, cnx, df):
    tabla_artistas=[]
    for row in df.itertuples():
        tabla_artistas.append((row.nombre_artista, row.oyentes, row.reproducciones))
    
    try:
        mycursor.executemany(query.query_insercion_tabla_artistas, tabla_artistas)
        cnx.commit()
        print(f"Datos insertados correctamente {mycursor.rowcount} total")
    except:
        print(f"No se ha podido realizar la insercion")
        
    return tabla_artistas
# %%

# Cerramos la conexión

def cerrar_conexion(cnx):
    cnx.close()
    print("Conexión cerrada.")

# %%