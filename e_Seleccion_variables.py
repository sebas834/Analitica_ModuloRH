import sqlite3 as sql #### para bases de datos sql
import pandas as pd
from numpy import set_printoptions
from sklearn.feature_selection import SelectKBest # KBest: Seleccione características de acuerdo con las k puntuaciones más altas.
from sklearn.feature_selection import f_classif # cuál de las variables es más importante para la variable de salidad con f_classif
from sklearn.feature_selection import RFE
from sklearn.linear_model import LogisticRegression

conn = sql.connect("db_despidos")

# Se hacen las conexiones 
dt = pd.read_sql("select * from dt", conn)
dt.drop('index', axis = 1, inplace = True)

# Se reordenan las columnas para que la variable respuesta quede de último
columnas = list(dt.columns)
columnas[-2], columnas[-1] = columnas[-1], columnas[-2]

dt = dt[columnas]

dt_copy = dt.copy()

# Se llenan con ceros los nulos ya que se interpreta que el empleado no ha trabajado en otra compañía
dt_copy.fillna('0', inplace = True)

arreglo = dt_copy.values
X = arreglo[:,1:-1]
y = arreglo[:,-1] # variable independiente

# Solucionar error
y = y.astype('int')

# Se aplica KBest
# crear modelo de selección. Entrenamiento. k=8: seleccione los 8 mejores
est_prueba = SelectKBest(score_func = f_classif, k = 8)
est_ajustado = est_prueba.fit(X,y)

# muestro el desempeño de los features basado en el valor f
set_printoptions(precision = 3) # que los arrays de numpy muestran 3 decimales

features = est_ajustado.transform(X) # 
# Se convierte en dataframe los 8 features que más influencia tienen 
pd.DataFrame(features)

# Features escogidos por KBest
df = dt_copy.loc[:,['SatisfaccionAmbiente','SatisfaccionTrabajo','BalanceTrabajoVida','Age', 'MaritalStatus', 'TotalWorkingYears','YearsAtCompany', 'YearsWithCurrManager','Desercion']]


### Recursive Feature Elimination (RFE)

# Extracción de Features
# Primero se crea el estimador, modelo
modelo = LogisticRegression(solver = 'liblinear')

# Modelo selección
est_rfe = RFE(modelo, n_features_to_select = 8)

# Ajusto el modelo
est_ajustado = est_rfe.fit(X, y)
features = est_ajustado.transform(X) 

# Se muestran en un dataframe los mejores features 
pd.DataFrame(features)

# Features elegidos por RFE:
df_1 = dt_copy.loc[:,['SatisfaccionAmbiente','SatisfaccionTrabajo','BalanceTrabajoVida', 'Age','MaritalStatus', 'TotalWorkingYears', 'YearsSinceLastPromotion', 'YearsWithCurrManager','Desercion']]

conn = sql.connect("vbles_kbest") ### crea una base de datos con el nombre dentro de comillas, si existe crea una conexión.
df.to_sql("df", conn, if_exists = "replace")### Llevar tablas a base de datos

conn = sql.connect("vbles_RFE") ### crea una base de datos con el nombre dentro de comillas, si existe crea una conexión.
df_1.to_sql("df_1", conn, if_exists = "replace") ### Llevar tablas a base de datos