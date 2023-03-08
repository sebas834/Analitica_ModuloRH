#Importar paquetes de datos
import pandas as pd
import numpy as np
import a_Funciones as funciones
import sqlite3 as sql #### para bases de datos sql
import sys

# sys.path
# sys.path.append('c:\\Users\\SEBASTIAN\\OneDrive - Universidad de Antioquia\\1. UdeA 2023-1\\Analítica\\Unidad_RH\\Entregas\\Entrega 1\\Github')

# Cargar datos
employee_survey = pd.read_csv('https://raw.githubusercontent.com/sebas834/Analtica-Modulo_RH/main/Datos/employee_survey_data.csv')
general_data = pd.read_csv('https://raw.githubusercontent.com/sebas834/Analtica-Modulo_RH/main/Datos/general_data.csv', sep=';')
manager_survey_data = pd.read_csv('https://raw.githubusercontent.com/sebas834/Analtica-Modulo_RH/main/Datos/manager_survey_data.csv')
retirement_info = pd.read_csv('https://raw.githubusercontent.com/sebas834/Analtica-Modulo_RH/main/Datos/retirement_info.csv', sep=';')
in_time = pd.read_csv('https://raw.githubusercontent.com/sebas834/Analtica-Modulo_RH/main/Datos/in_time.csv')
out_time = pd.read_csv('https://raw.githubusercontent.com/sebas834/Analtica-Modulo_RH/main/Datos/out_time.csv')

###################################### ANÁLISIS TABLA: employee_survey###########################

#Renombrar Columnas
employee_survey = employee_survey.rename(columns ={'EnvironmentSatisfaction':'SatisfaccionAmbiente','JobSatisfaction':'SatisfaccionTrabajo','WorkLifeBalance':'BalanceTrabajoVida'}) 

# Análisis del dataframe
print("El tamaño del DF es",employee_survey.shape)
print("El nombre de las columnas del DF es",employee_survey.columns)
print("El tipo de variable de cada columna es\n", employee_survey.dtypes)

#Análisis de nulos
#No hay numero significante de datos faltantes en la base de datos Insumo 1
print(employee_survey.isnull().sum())                   # Número de nulos por variable
print("---------")
print(employee_survey.isnull().sum() / employee_survey.shape[0])# % de nulos por variable

#Analisis de las categorias de las variables
# No se evidencian problemas de digitación de las catgorias de las variables
lista = [ 'SatisfaccionAmbiente', 'BalanceTrabajoVida', 'SatisfaccionTrabajo'] #Se crea una lista para poder aplicar funciones
for i in lista:  print(employee_survey[i].value_counts())  #Contar los valores de cada categoria

###################################### ANÁLISIS TABLA: general_data###########################

general_data = general_data.rename(columns ={'':'','':''}) # Renombrar una columnas
general_data.info()

####Analisis de nulos

#No hay numero significante de datos faltantes en la base de datos
print(general_data.isnull().sum())                   # Número de nulos por variable
print("---------")
print(general_data.isnull().sum() / general_data.shape[0])# % de nulos por variable

####Analisis de categorias de las variables

# # No se evidencian problemas de digitación de las catgorias de las variables
lista = [ 'BusinessTravel', 'Department',  'Education',
       'EducationField', 'EmployeeCount', 'Gender', 'JobLevel',
       'JobRole', 'MaritalStatus', 'MonthlyIncome',
       'Over18', 'PercentSalaryHike', 'StandardHours', 'StockOptionLevel'] #Se crea una lista para poder aplicar funciones
for i in lista:
  print(general_data[i].value_counts())  #Contar los valores de cada categoria
  print('--------------------------------')


###################################### ANÁLISIS TABLA: manager_survey_data###########################

# Renombrar columnas
manager_survey_data = manager_survey_data.rename(columns ={'JobInvolvement':'ParticipaciónTrabajo','PerformanceRating':'NivelRendimiento'}) 

####Tamaño y forma

#Forma del DF
print("El tamaño del DF es",manager_survey_data.shape )
print("El nombre de las columnas del DF es",manager_survey_data.columns )
print("El tipo de variable de cada columna es", manager_survey_data.dtypes )

### Analisis de nuloS

#No hay numero significante de datos faltantes en la base de datos
print(manager_survey_data.isnull().sum())                   # Número de nulos por variable
print("---------")
print(manager_survey_data.isnull().sum() / manager_survey_data.shape[0])# % de nulos por variable

####Analisis de categorias de las variables

# No se evidencian problemas de digitación de las catgorias de las variables
lista = ['ParticipaciónTrabajo', 'NivelRendimiento'] #Se crea una lista para poder aplicar funciones
for i in lista:
  print(manager_survey_data[i].value_counts())  #Contar los valores de cada categoria
  print('--------------------------------')

###################################### ANÁLISIS TABLA: retirement_info###########################

# Renombrar columnas
retirement_info = retirement_info.rename(columns ={'Attrition':'Desercion','retirementDate':'FechaRetiro','retirementType':'TipoRetiro','resignationReason':'RazonRetiro'}) 

####Tamaño y Forma

#Forma del DF
print("El tamaño del DF es",retirement_info.shape )
print("El nombre de las columnas del DF es",retirement_info.columns )
print("El tipo de variable de cada columna es", retirement_info.dtypes )

###Analisis de nulos

#No hay numero significante de datos faltantes en la base de datos Insumo 1
print(retirement_info.isnull().sum())                   # Número de nulos por variable
print("---------")
print(retirement_info.isnull().sum() / retirement_info.shape[0])# % de nulos por variable

retirement_info['RazonRetiro'] = retirement_info['RazonRetiro'].fillna('No Aplica')

####Analisis de la categoria de cada variable

# No se evidencian problemas de digitación de las catgorias de las variables
lista = [ 'Desercion', 'TipoRetiro','RazonRetiro'] #Se crea una lista para poder aplicar funciones
for i in lista:
  print(retirement_info[i].value_counts())  #Contar los valores de cada categoria
  print('--------------------------------')

###################################### ANÁLISIS TABLA: in_time y out_time###########################
# Dimensiones
print(in_time.shape)
print(out_time.shape)

# Se cambia el nombre de la columna de identificadores
in_time.rename(columns = {'Unnamed: 0': 'EmployeeID'}, inplace = True)
out_time.rename(columns = {'Unnamed: 0': 'EmployeeID'}, inplace = True)

# % de nulos por variable
print(in_time.isnull().sum() / in_time.shape[0]*100)

print(out_time.isnull().sum() / out_time.shape[0]*100)

# Se eliminana las columnas que son completamente nulas.
in_time.dropna(axis = 1, how = 'all', inplace = True)
out_time.dropna(axis = 1, how = 'all', inplace = True)

# Se cuentan la cantidad de faltas que cada empleado tuvo en el año
in_time.insert(1, "Cantidad de faltas", in_time.isnull().sum(axis = 1))
out_time.insert(1, "Cantidad de faltas", out_time.isnull().sum(axis = 1))

# Nuevas dimensiones
print(in_time.shape)
print(out_time.shape)

# Se eliminan las fechas y se dejan las horas en cada dataframe
for i in in_time.columns[2:]:
  funciones.eliminar_fecha(in_time, i)
  funciones.eliminar_fecha(out_time, i)

dt3 = in_time.iloc[:, 0:2]

#Union de bases
dt1 = employee_survey.merge(general_data, on='EmployeeID', how='left')
dt2 = dt1.merge(manager_survey_data, on='EmployeeID', how='left')
dt4 = dt2.merge(retirement_info, on='EmployeeID', how='left')
dt = dt4.merge(dt3, on='EmployeeID', how='left')
dt['Desercion'] = dt['Desercion'].fillna('No')
dt.head()
dt.isnull().sum()
#### crear base de datos para manejo de datos ####

conn = sql.connect("db_despidos") ### crea una base de datos con el nombre dentro de comillas, si existe crea una conexión.

### Llevar tablas a base de datos
dt.to_sql("dt", conn, if_exists="replace")

# # Reemplazar los valores nulos de manera que el valor nulo se llene con el valor siguiente no nulo
# Se debe correr para realizar los gráficos que analiza las horas de entrada y salida
in_time.fillna(method = 'bfill', inplace = True)
out_time.fillna(method = 'bfill', inplace = True)

# En caso de existir un nulo en la última fila el nulo se reemplazará por el valor anterior no nulo
in_time.fillna(method = 'ffill', inplace = True)
out_time.fillna(method = 'ffill', inplace = True)

# Se crear bases de datos con las horas de entrada y salida para graficar en el análisis exploratorio
conn = sql.connect("in_time")
in_time.to_sql("in_time", conn, if_exists="replace")

conn = sql.connect("out_time")
out_time.to_sql("out_time", conn, if_exists="replace")
