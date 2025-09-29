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

# Aceso a BASE DE DATOS existente:

def acceso_bbdd(cnx,nombre_bbdd):  # USE nombre_bbdd
    mycursor = cnx.cursor()   # creamos nuestro cursor (nos abre mysql)
    print(f"Variable 'mycursor' creada.")
    try:
        mycursor.execute(f'USE {nombre_bbdd};')
        print(f"Estamos en la bbdd indicada")
        return mycursor
    except Exception as e:
        print(f"No ha sido posible moverse a la base de datos indicada:\n{e}")


# %%

# Creación de TABLAS

def creacion_tablas(mycursor, *args): # para meter tantas queries como queramos
    try:
        for query in args:
            mycursor.execute(query)
            print('Tabla creada con éxito.')
    except Exception as e:
        print("Error al crear la tabla:", e)

# %%

# INSERCIÓN datos: tablas generales

    # Departamento

def insercion_tabla_departamento(mycursor, cnx, df_trabajo):
    # quitamos los valores duplicados
    df = df_trabajo[['department']].drop_duplicates() # 3 entradas
    # iteramos en el df para sacar los valores que necesitamos
    tabla_departamento=[]
    for row in df[['department']].itertuples():
        tabla_departamento.append((row.department,))
    
    try:
        # Le pedimos a sql que nos ejecute lo que indicamos en el archivo de soporte
        mycursor.executemany(query.query_insercion_departamento, tabla_departamento)
        cnx.commit()
        print(f"Datos insertados correctamente: {mycursor.rowcount} filas.")
    except Exception as e:
        print(f"No se ha podido realizar la inserción:\n{e}")
        
    # Puesto

def insercion_tabla_puesto(mycursor, cnx, df_puesto):
    # quitamos los valores duplicados
    df= df_puesto[['jobrole', 'joblevel']]
    df = df.drop_duplicates().reset_index(drop = True)  # 26 entradas
    # iteramos en el df para sacar los valores que necesitamos
    tabla_puesto =[]
    for row in df[['jobrole', 'joblevel']].itertuples():
        tabla_puesto.append((row.jobrole,row.joblevel,))
    
    try:
        # Le pedimos a sql que nos ejecute lo que indicamos en el archivo de soporte
        mycursor.executemany(query.query_insercion_puesto, tabla_puesto)
        cnx.commit()
        print(f"Datos insertados correctamente: {mycursor.rowcount} filas.")
    except Exception as e:
        print(f"No se ha podido realizar la inserción:\n{e}")

    # Educación

def insercion_tabla_educacion(mycursor, cnx, df_educacion):
    # quitamos los valores duplicados
    df = df_educacion[['education', 'educationfield']]
    df = df.drop_duplicates().reset_index(drop = True)   # 29 entradas
    # iteramos en el df para sacar los valores que necesitamos
    tabla_educacion =[]
    for row in df[['education', 'educationfield']].itertuples():
        tabla_educacion.append((row.education,row.educationfield,))
    
    try:
        # Le pedimos a sql que nos ejecute lo que indicamos en el archivo de soporte
        mycursor.executemany(query.query_insercion_educacion, tabla_educacion)
        cnx.commit()
        print(f"Datos insertados correctamente: {mycursor.rowcount} filas.")
    except Exception as e:
        print(f"No se ha podido realizar la inserción:\n{e}")

# %%

# INSERCIÓN datos: tabla ppal y dependientes

    # Empleados <-- tabla principal, KP y KF

def insercion_tabla_empleados(mycursor, cnx, df):
    # Obtener IDs FOREIGN KEYS de las otras tablas YA CREADAS 
    mycursor.execute(query.query_id_tabla_departamento)
    departamentoID = {nombre: id for id, nombre in mycursor.fetchall()} # <-- diccionario
    
    mycursor.execute(query.query_id_tabla_puesto)
    puestoID = {(nombre, nivel): id for id, nombre, nivel in mycursor.fetchall()} # <-- diccionario
    
    mycursor.execute(query.query_id_tabla_educacion)
    educacionID = {(nivel, campo): id for id, nivel, campo in mycursor.fetchall()} # <-- diccionario

    # iteramos en el df para sacar los valores que necesitamos
    tabla_empleados =[]
    for row in df[['employeenumber', 'age', 'attrition', 'gender', 'maritalstatus', 'datebirth',
                   'department', 'jobrole', 'joblevel', 'education', 'educationfield'
                   ]].itertuples():
        try:
            # Buscamos el ID correspondiente a cada fila del DataFrame, para añadirlo a la tabla_empleados
            departamento_id= departamentoID[row.department]
            puesto_id= puestoID[(row.jobrole, row.joblevel)]
            educacion_id = educacionID[(row.education, row.educationfield)]

            tabla_empleados.append((
                row.employeenumber,
                row.age,
                row.attrition,
                row.gender,
                row.maritalstatus,
                row.datebirth,
                departamento_id,
                puesto_id,
                educacion_id,
                ))
            
        except KeyError as e:
            print(f"Error de clave foránea no encontrada: {e}\nFila problemática: {row}")

    try:
        # Le pedimos a sql que nos ejecute lo que indicamos en el archivo de soporte
        mycursor.executemany(query.query_insercion_empleados, tabla_empleados)
        cnx.commit()
        print(f"Datos insertados correctamente: {mycursor.rowcount} filas.")
    except Exception as e:
        print(f"No se ha podido realizar la inserción:\n{e}")


    # Nivel_Satisfaccion <-- KF

def insercion_tabla_nivel_satisfaccion(mycursor, cnx, df):
    # iteramos en el df para sacar los valores que necesitamos
    tabla_nivel_satisfaccion =[]
    for row in df[['environmentsatisfaction', 'jobsatisfaction', 'relationshipsatisfaction', 'employeenumber']].itertuples():
        tabla_nivel_satisfaccion.append((
            row.environmentsatisfaction,
            row.jobsatisfaction,
            row.relationshipsatisfaction,
            row.employeenumber,   # clave foránea (está tb en el df)
            ))
    
    try:
        # Le pedimos a sql que nos ejecute lo que indicamos en el archivo de soporte
        mycursor.executemany(query.query_insercion_nivel_satisfaccion, tabla_nivel_satisfaccion)
        cnx.commit()
        print(f"Datos insertados correctamente: {mycursor.rowcount} filas.")
    except Exception as e:
        print(f"No se ha podido realizar la inserción:\n{e}")


    # Condiciones_Laborales

def insercion_tabla_condiciones_laborales(mycursor, cnx, df):
    # iteramos en el df para sacar los valores que necesitamos
    tabla_laborales =[]
    for row in df[['businesstravel', 'distancefromhome', 'jobinvolvement', 'numcompaniesworked', 'overtime', 'performancerating', 'stockoptionlevel', 'trainingtimeslastyear', 'worklifebalance', 'yearsatcompany', 'yearssincelastpromotion', 'yearswithcurrmanager', 'salary', 'remotework', 'employeenumber']].itertuples():
        tabla_laborales.append((
            row.businesstravel,
            row.distancefromhome,
            row.jobinvolvement,
            row.numcompaniesworked,
            row.overtime,
            row.performancerating,
            row.stockoptionlevel,
            row.trainingtimeslastyear,
            row.worklifebalance,
            row.yearsatcompany,
            row.yearssincelastpromotion,
            row.yearswithcurrmanager,
            row.salary,
            row.remotework,
            row.employeenumber,   # clave foránea (está tb en el df)
            ))
    
    try:
        # Le pedimos a sql que nos ejecute lo que indicamos en el archivo de soporte
        mycursor.executemany(query.query_insercion_condiciones_laborales, tabla_laborales)
        cnx.commit()
        print(f"Datos insertados correctamente: {mycursor.rowcount} filas.")
    except Exception as e:
        print(f"No se ha podido realizar la inserción:\n{e}")


        
# %%

# Cerramos la conexión
def cerrar_conexion(cnx):
    cnx.close()
    print("Conexión cerrada.")

# %%