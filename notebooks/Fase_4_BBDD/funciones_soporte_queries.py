# Creamos el schema / BBDD
query_creacion_bbdd = 'CREATE SCHEMA IF NOT EXISTS `Optimizacion_Talento` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci;'

# Nos posicionamos en la BBDD creada
query_moverse_bbdd = 'USE `Optimizacion_Talento` ;'

# Creación de tablas

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
  NombrePuesto VARCHAR(100) NOT NULL UNIQUE
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
  Campo VARCHAR(100) NOT NULL, 
  UNIQUE KEY UQ_Nivel_Campo (Nivel, Campo)
  );'''
#  5   education --> int64 
#  6   educationfield --> object
print("Tabla 'Educacion_Nivel_Campo' creada.")

    # Tabla D: Nivel_Satisfaccion
query_creacion_tabla_nivel_satisfaccion = '''
CREATE TABLE IF NOT EXISTS Nivel_Satisfaccion (
  NSatisfaccionID INT AUTO_INCREMENT PRIMARY KEY,
  NSAmbienteLaboral  INT, 
  NSLaboral INT, 
  NSRelInterpersonales INT
  );'''
#  8   environmentsatisfaction --> int64 
#  13  jobsatisfaction --> int64 
#  18  relationshipsatisfaction --> int64
print("Tabla 'Nivel_Satisfaccion' creada.")

    # Tabla E: Condiciones_Laborales
query_creacion_tabla_condiciones_laborales = '''
CREATE TABLE IF NOT EXISTS Condiciones_Laborales (
  CLaborales ID INT AUTO_INCREMENT PRIMARY KEY,
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
  Teletrabajo VARCHAR(3)
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

# --- 3. DEFINICIÓN DE TABLA CENTRAL (Con FKs) ---

# Tabla F: Empleados (Tabla Central)
query_creacion_tabla_empleados = '''
CREATE TABLE IF NOT EXISTS Empleados (
    EmployeeNumber_CSV INT PRIMARY KEY,
    Edad INT NOT NULL,
    EnEmpresa VARCHAR(3),
    Genero VARCHAR(10),
    EstadoCivil VARCHAR(20), 
    AñoNacimiento YEAR, 

    -- Claves Foráneas
    DepartamentoFK INT NOT NULL,
    PuestoFK INT NOT NULL,
    EducacionFK INT NOT NULL,
    NSatisfaccionFK INT NOT NULL,
    CLaboralesFK ID,
      
    -- Definición de Relaciones de Claves Foráneas
    FOREIGN KEY (DepartamentoFK) REFERENCES Departamento (DepartamentoID) ON DELETE RESTRICT ON UPDATE CASCADE,
    FOREIGN KEY (PuestoFK) REFERENCES Puesto(PuestoID) ON DELETE RESTRICT ON UPDATE CASCADE,
    FOREIGN KEY (EducacionFK) REFERENCES Educacion_Nivel_Campo(EducacionID) ON DELETE RESTRICT ON UPDATE CASCADE,
    FOREIGN KEY (NSatisfaccionFK) REFERENCES Nivel_Satisfaccion(NSatisfaccionID) ON DELETE RESTRICT ON UPDATE CASCADE,
    FOREIGN KEY (CLaboralesFK) REFERENCES Condiciones_Laborales(CLaboralesID) ON DELETE RESTRICT ON UPDATE CASCADE
    );'''
# 7   employeenumber -->  int64 (ya únicos en el df)
# 0   age --> int64 
# 1   attrition --> object   
# 9   gender --> object 
# 14  maritalstatus --> object 
# 25  datebirth --> int64  
print("Tabla 'Empleados' creada con todas las FKs.")
