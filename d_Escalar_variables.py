
#### CATEGORICAS:  'BalanceTrabajo-Vida', 'Satisfaccion-Trabajo', 'Satisfaccion-Ambiente', 'JobLevel','Education','BusinessTravel', 'Department','EducationField','Gender','JobRole','MaritalStatus', 'Desercion', 'Fecha-Retiro',
###'tipoRetiro', 'RazonRetiro','StockOptionLevel','Participación-Trabajo', 'Nivel-Trabajo'

### NUMÉRICAS: 'Age','DistanceFromHome','EmployeeCount',  
###                'MonthlyIncome','NumCompaniesWorked', 'PercentSalaryHike', 'StandardHours', 'TotalWorkingYears', 
###                    'TrainingTimesLastYear', 'YearsAtCompany', 'YearsSinceLastPromotion', 'YearsWithCurrManager'

###CONSTANTES: 'EmployeeCount',  'StandardHours', 'Over18'

###TARGET: Desercion

import sqlite3 as sql #### para bases de datos sql
import pandas as pd
from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import StandardScaler

conn = sql.connect("db_despidos")

# Se hacen las conexiones 
dt = pd.read_sql("select * from dt", conn)
dt.drop('index', axis = 1, inplace = True)


le = LabelEncoder()

dt['JobLevel'] = le.fit_transform(dt.JobLevel)
dt['Education'] = le.fit_transform(dt.Education)
dt['BusinessTravel'] = le.fit_transform(dt.BusinessTravel)
dt['Department'] = le.fit_transform(dt.Department)
dt['EducationField'] = le.fit_transform(dt.EducationField)
dt['Gender'] = le.fit_transform(dt.Gender)
dt['JobRole'] = le.fit_transform(dt.JobRole)
dt['MaritalStatus'] = le.fit_transform(dt.MaritalStatus)
dt['Desercion'] = le.fit_transform(dt.Desercion)
dt['FechaRetiro'] = le.fit_transform(dt.FechaRetiro)
dt['TipoRetiro'] = le.fit_transform(dt.TipoRetiro)
dt['RazonRetiro'] = le.fit_transform(dt.RazonRetiro)
dt['StockOptionLevel'] = le.fit_transform(dt.StockOptionLevel)
dt['ParticipaciónTrabajo'] = le.fit_transform(dt.ParticipaciónTrabajo)
dt['NivelRendimiento'] = le.fit_transform(dt.NivelRendimiento)
dt['SatisfaccionAmbiente'] = le.fit_transform(dt.SatisfaccionAmbiente)
dt['SatisfaccionTrabajo'] = le.fit_transform(dt.SatisfaccionTrabajo)
dt['BalanceTrabajoVida'] = le.fit_transform(dt.BalanceTrabajoVida)

scaler = StandardScaler()

Lista = ['Age','DistanceFromHome', 'MonthlyIncome','NumCompaniesWorked', 'PercentSalaryHike',  'TotalWorkingYears', 
        'TrainingTimesLastYear', 'YearsAtCompany', 'YearsSinceLastPromotion', 'YearsWithCurrManager']

for i in Lista:
  dt[[i]] = scaler.fit_transform(dt[[i]])

del dt['EmployeeCount']
del dt['StandardHours']
del dt['Over18']
del dt['FechaRetiro']
del dt['TipoRetiro']
del dt['RazonRetiro']

conn = sql.connect("db_despidos") ### crea una base de datos con el nombre dentro de comillas, si existe crea una conexión.

### Llevar tablas a base de datos
dt.to_sql("dt", conn, if_exists="replace")