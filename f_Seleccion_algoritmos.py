import sqlite3 as sql #### para bases de datos sql
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
from sklearn.metrics import confusion_matrix
from sklearn.neighbors import  KNeighborsClassifier
from sklearn.metrics import classification_report
from sklearn.model_selection import RepeatedStratifiedKFold
from sklearn.model_selection import RandomizedSearchCV

conn = sql.connect("vbles_kbest")
conn1 = sql.connect("vbles_RFE")

# Se hacen las conexiones 
df = pd.read_sql("select * from df", conn)
df.drop('index', axis = 1, inplace = True)

df_1 = pd.read_sql("select * from df_1", conn1)
df_1.drop('index', axis = 1, inplace = True)


### Se aplican los algoritmos a las variables elegidas en KBest
arreglo = df.values
X = arreglo[:,:-1]
y = arreglo[:,-1] # variable independiente

# Para evitar errores
y = y.astype('int')

# Se dividen los datos en entrenamiento y prueba
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.2, random_state = 42, stratify = y)

# Se aplica el algoritmo Support Vector Machine (SVC)
svc = SVC(kernel = 'linear').fit(X_train, y_train)

print(f'El Score es: {svc.score(X_test, y_test)} \n')

yhat = svc.predict(X_test)
precision = confusion_matrix(y_test, yhat)
print(f'Matriz de confusión: \n {precision}')

# Se aplica el algoritmo K-Vecinos más Cercanos ()
knn = KNeighborsClassifier(n_neighbors = 2)
knn.fit(X_train, y_train)
print(f'El Score es {knn.score(X_test, y_test)} \n')

yhat = knn.predict(X_test)
precision = confusion_matrix(y_test, yhat)
print(f'Matriz de confusión: \n {precision}')

print(classification_report(y_test,yhat))

### Segunda opción de features elegidos por RFE

arreglo = df_1.values
X1 = arreglo[:,:-1]
y1 = arreglo[:,-1] # variable independiente

# Para evitar errores
y1 = y1.astype('int')

# Se dividen los datos en entrenamiento y prueba
X_train, X_test, y_train, y_test = train_test_split(X1, y1, test_size = 0.2, random_state = 42, stratify = y1)

# Se aplica el algoritmo Support Vector Machine (SVC)
svc1 = SVC(kernel = 'linear').fit(X_train, y_train)

# cv = RepeatedStratifiedKFold(n_splits=10, n_repeats=3, random_state=1)

print(f'El Score es: {svc1.score(X_test, y_test)} \n')

yhat = svc1.predict(X_test)
precision = confusion_matrix(y_test, yhat)
print(f'Matriz de confusión: \n {precision}')

# Se aplica el algoritmo K-Vecinos más Cercanos ()
knn1 = KNeighborsClassifier(n_neighbors = 2)
knn1.fit(X_train, y_train)

cv = RepeatedStratifiedKFold(n_splits=10, n_repeats=3, random_state=1)

print(f'El Score es {knn1.score(X_test, y_test)} \n')

yhat1 = knn1.predict(X_test)
precision = confusion_matrix(y_test, yhat1)
print(f'Matriz de confusión: \n {precision}')

print(classification_report(y_test,yhat1))

############################## Afinamiento de hiperparámetros ##############################
param_grid = [{'n_neighbors': [10, 100], 'leaf_size': [2, 4, 5]},{'weights': ['uniform', 'distance']}]

tun_rf=RandomizedSearchCV(knn,param_grid, cv =10,scoring="recall")
search=tun_rf.fit(X,y)

tun_rf.best_params_
resultados=tun_rf.cv_results_
pd_resultados=pd.DataFrame(resultados)
pd_resultados[["params","mean_test_score"]]
