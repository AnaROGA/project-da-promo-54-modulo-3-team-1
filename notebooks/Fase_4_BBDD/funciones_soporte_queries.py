################## Creamos el schema / BBDD
query_creacion_bbdd = 'CREATE SCHEMA IF NOT EXISTS `Optimizacion_Talento` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci;'

##################  Nos posicionamos en la BBDD creada
query_moverse_bbdd = 'USE `Optimizacion_Talento` ;'

##################  Creación de tablas

    # Tabla A: Departamento
query_creacion_tabla_departamento = '''
CREATE TABLE IF NOT EXISTS Departamento (
  DepartamentoID INT AUTO_INCREMENT PRIMARY KEY,
  NombreDepartamento VARCHAR(100) NOT NULL UNIQUE 
  );'''
#  3   department --> object 
print("Tabla 'Departamento' creada.")

    # Tabla B: Puesto
query_creacion_tabla_puesto = '''
CREATE TABLE IF NOT EXISTS Puesto (
  PuestoID INT AUTO_INCREMENT PRIMARY KEY,
  NombrePuesto VARCHAR(100) NOT NULL,
  NivelPuesto INT
  );'''
# 12  jobrole --> object 
# 11  joblevel --> int64 
print("Tabla 'Puesto' creada.")

    # Tabla C: Educacion_Nivel_Campo
query_creacion_tabla_educacion = '''
CREATE TABLE IF NOT EXISTS Educacion_Nivel_Campo (
  EducacionID INT AUTO_INCREMENT PRIMARY KEY,
  Nivel INT NOT NULL, 
  Campo VARCHAR(100) 
  );'''
#  5   education --> int64 
#  6   educationfield --> object
print("Tabla 'Educacion_Nivel_Campo' creada.")

# --- DEFINICIÓN DE TABLA CENTRAL (Con FKs) ---

# Tabla PPAL: Empleados (Tabla Central)
query_creacion_tabla_empleados = '''
CREATE TABLE IF NOT EXISTS Empleados (
    EmployeeNumber INT PRIMARY KEY,
    Edad INT NOT NULL,
    EnEmpresa VARCHAR(3),
    Genero VARCHAR(10),
    EstadoCivil VARCHAR(20), 
    AnoNacimiento YEAR, 

    -- Claves Foráneas
    DepartamentoFK INT,
    PuestoFK INT,
    EducacionFK INT,
  
      
    -- Definición de Relaciones de Claves Foráneas
    FOREIGN KEY (DepartamentoFK) REFERENCES Departamento(DepartamentoID) ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (PuestoFK) REFERENCES Puesto(PuestoID) ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (EducacionFK) REFERENCES Educacion_Nivel_Campo(EducacionID) ON DELETE CASCADE ON UPDATE CASCADE
    );'''
# 7   employeenumber -->  int64 (ya únicos en el df)
# 0   age --> int64 
# 1   attrition --> object   
# 9   gender --> object 
# 14  maritalstatus --> object 
# 25  datebirth --> int64  
print("Tabla 'Empleados' creada con todas las FKs.")

    # Tabla E: Nivel_Satisfaccion
query_creacion_tabla_nivel_satisfaccion = '''
CREATE TABLE IF NOT EXISTS Nivel_Satisfaccion (
  NSAmbienteLaboral  INT, 
  NSLaboral INT, 
  NSRelInterpersonales INT,

  -- Claves Foráneas
  EmployeeNumberFK INT,

  -- Definición de Relaciones de Claves Foráneas
  FOREIGN KEY (EmployeeNumberFK) REFERENCES Empleados (EmployeeNumber) ON DELETE CASCADE ON UPDATE CASCADE
  );'''
#  8   environmentsatisfaction --> int64 
#  13  jobsatisfaction --> int64 
#  18  relationshipsatisfaction --> int64
print("Tabla 'Nivel_Satisfaccion' creada.")

    # Tabla F: Condiciones_Laborales
query_creacion_tabla_condiciones_laborales = '''
CREATE TABLE IF NOT EXISTS Condiciones_Laborales (
  ViajesTrabajo VARCHAR(50), 
  DistanciaVivienda INT, 
  NivelImplicacion INT,
  NumEmpresasAnteriores INT,
  HorasExtra VARCHAR(10),
  Rendimiento INT,
  OpcionesAcciones INT,
  HorasFormacionAñoPasado INT,
  NivelConciliacion INT,
  AñosEmpresa INT,
  AñosDesdePromocion INT,
  AñosMismoManager INT,
  Salario DECIMAL(10, 2),
  Teletrabajo VARCHAR(3),

  -- Claves Foráneas
  EmployeeNumberFK INT,

  -- Definición de Relaciones de Claves Foráneas
  FOREIGN KEY (EmployeeNumberFK) REFERENCES Empleados (EmployeeNumber) ON DELETE CASCADE ON UPDATE CASCADE

  );'''
# 2   businesstravel --> object 
# 4   distancefromhome -->  int64   
# 10  jobinvolvement --> int64
# 15  numcompaniesworked --> int64  
# 16  overtime --> object
# 17  performancerating  --> int64  
# 19  stockoptionlevel--> int64
# 20  trainingtimeslastyear --> int64
# 21  worklifebalance --> int64  
# 22  yearsatcompany -->   int64 
# 23  yearssincelastpromotion -->   int64
# 24  yearswithcurrmanager  --> int64
# 26  salary --> float64 
# 27  remotework -->  object
print("Tabla 'Condiciones_Laborales' creada.")

##################  Inserción de Datos

    # Departamento
query_insercion_departamento = '''
INSERT IGNORE INTO departamento (NombreDepartamento)
VALUES (%s);
'''
print("Datos insertados en tabla 'Departamento'.")

    # Puesto
query_insercion_puesto = '''
INSERT IGNORE INTO puesto (NombrePuesto, NivelPuesto)
VALUES (%s,%s);
'''
print("Datos insertados en tabla 'Puesto'.")

    # Educación
query_insercion_educacion = '''
INSERT IGNORE INTO educacion_nivel_campo (Nivel, Campo)
VALUES (%s,%s);
'''
print("Datos insertados en tabla 'Educación'.")

#####  Tabla ppal y dependientes

# Obtención de datos ya existentes en las tablas creadas:
    # DepartamentoFK
query_id_tabla_departamento = '''
SELECT DepartamentoID, NombreDepartamento 
FROM Departamento;
'''
    # PuestoFK
query_id_tabla_puesto = '''
SELECT PuestoID, NombrePuesto, NivelPuesto 
FROM Puesto;
'''
    # EducacionFK
query_id_tabla_educacion = '''
SELECT EducacionID, Nivel, Campo
FROM Educacion_Nivel_Campo;
'''

    # Empleados
query_insercion_empleados = '''
INSERT IGNORE INTO empleados (EmployeeNumber, Edad, EnEmpresa, Genero, EstadoCivil, AnoNacimiento, DepartamentoFK, PuestoFK, EducacionFK)
VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s);
   '''
# 7   employeenumber -->  int64 (ya únicos en el df)
# 0   age --> int64 
# 1   attrition --> object   
# 9   gender --> object 
# 14  maritalstatus --> object 
# 25  datebirth --> int64  
print("Tabla 'Empleados' creada con todas las FKs.")

    # Nivel_Satisfaccion
query_insercion_nivel_satisfaccion  = '''
INSERT IGNORE INTO nivel_satisfaccion  (NSAmbienteLaboral, NSLaboral, NSRelInterpersonales, EmployeeNumberFK)
VALUES (%s,%s,%s,%s);
'''
print("Datos insertados en tabla 'Nivel_Satisfaccion'.")

    # Condiciones_Laborales
query_insercion_condiciones_laborales = '''
INSERT IGNORE INTO condiciones_laborales (ViajesTrabajo, DistanciaVivienda, NivelImplicacion, NumEmpresasAnteriores, HorasExtra, Rendimiento, OpcionesAcciones, HorasFormacionAñoPasado, NivelConciliacion, AñosEmpresa, AñosDesdePromocion, AñosMismoManager, Salario, Teletrabajo, EmployeeNumberFK )
VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);
'''
print("Datos insertados en tabla 'Condiciones_Laborales'.")