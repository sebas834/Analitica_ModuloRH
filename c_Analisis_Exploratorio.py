#Importar paquetes de datos
import pandas as pd
import numpy as np
import a_Funciones as funciones
import sqlite3 as sql #### para bases de datos sql
import plotly.express as px
from matplotlib.pyplot import figure
import seaborn as sns
import matplotlib.pyplot as plt
import sys

conn = sql.connect("db_despidos")
conn_in = sql.connect("in_time")
conn_out = sql.connect("out_time")
cur = conn.cursor() ### para ejecutar querys sql en base de datos create y drop table

# Se hacen las conexiones 
dt = pd.read_sql("select * from dt", conn)
dt.drop('index', axis = 1, inplace = True)

in_time = pd.read_sql("select * from in_time", conn_in)
in_time.drop('index', axis = 1, inplace = True)

out_time  = pd.read_sql("select * from out_time", conn_out)
out_time.drop('index', axis = 1, inplace = True)

###Analisis de correlaciones
corr = dt.copy(deep = True)
del corr['EmployeeID']
# del corr['EmployeeCount']
# del corr['StandardHours']

#HEAT MAP
figure(figsize= (22,15),dpi=80);
sns.heatmap(corr.corr(),annot = True);
plt.title("Mapa de calor correalaciones variables", fontsize =20);


###Pairplot
sns.pairplot(corr[['Age','PercentSalaryHike','TotalWorkingYears','YearsAtCompany','SatisfaccionAmbiente','NivelRendimiento','Education']], height=2, aspect=1.3, plot_kws={"s": 3});

Ausentismos = dt.groupby(['Department'])[['Cantidad de faltas']].sum().reset_index()
plot1 = px.bar(Ausentismos, x = 'Department', y = ['Cantidad de faltas'], title = '<b> Cantidad de ausentismos año 2015 por departamento <b>', color_discrete_sequence = px.colors.qualitative.G10)

###Histograma y Boxplot

figure(figsize=(20, 5), dpi=80);

##GRAFICAR HISTOGRAMAS
# graficar Age
plt.subplot(1, 5, 1) 
plt.tight_layout()
plt.title('Age')
plt.hist(corr['Age'],color= 'skyblue')

# graficar Temperatura
plt.subplot(1, 5, 2) 
plt.tight_layout()
plt.title('PercentSalaryHike')
plt.hist(corr['PercentSalaryHike'],color= 'skyblue')

# graficar Velocidad del aire
plt.subplot(1, 5, 3) 
plt.tight_layout()
plt.title('TotalWorkingYears')
plt.hist(corr['TotalWorkingYears'],color= 'skyblue')

# graficar Humedad 
plt.subplot(1, 5, 4) 
plt.tight_layout()
plt.title('SatisfaccionAmbiente')
plt.hist(corr['SatisfaccionAmbiente'],color= 'skyblue')

# graficar Precipitacion
plt.subplot(1, 5, 5) 
plt.tight_layout()
plt.title('Education')
plt.hist(corr['Education'],color= 'skyblue',);

###Graficas Genero

print('La menor edad es de',dt['Age'].min())
print('La mayor edad es de',dt['Age'].max())

print('El menor ingreso es de',dt['MonthlyIncome'].min())
print('El mayor ingreso es de',dt['MonthlyIncome'].max())

rangos = dt.copy(deep = True)
rangos['age_range'] = pd.cut(x=rangos['Age'], bins=[15, 20,25,30,35,40,45,50,55,60])
rangos['MonthlyIncome'] = rangos['MonthlyIncome']/1000
rangos['MonthlyIncome_range'] = pd.cut(x=rangos['MonthlyIncome'], bins=[10, 30,50,70,90,110,130,150,170,200])

g1 = dt.groupby(['BusinessTravel','Gender'])[['EmployeeCount']].count().reset_index()
fig = px.bar(g1, x="Gender", y="EmployeeCount", color="BusinessTravel", title="Genero y la frecuencia de viajes laborales", barmode = 'group')
fig.show()

g1 = rangos.groupby(['MonthlyIncome_range','Gender'])[['EmployeeCount']].count().reset_index()
fig = px.bar(g1, x="Gender", y="EmployeeCount", color="MonthlyIncome_range", title="Genero y los rangos de ingresos", barmode = 'group')
fig.show()
# rango de ingresos mensuales

g1 = rangos.groupby(['age_range','Gender'])[['EmployeeCount']].count().reset_index()
fig = px.bar(g1, x="Gender", y="EmployeeCount", color="age_range", title="Genero y los rangos de edad", barmode = 'group')
fig.show()

g1 = dt.groupby(['Desercion','Gender'])[['EmployeeCount']].count().reset_index()
fig = px.bar(g1, x="Gender", y="EmployeeCount", color="Desercion", title="Genero y la salida de la empresa", barmode = 'group')
fig.show()

# crear gráfica
fig = px.pie(dt, values = 'MonthlyIncome', names ='Gender',
             title= '<b> Ingresos totales por genero<b>',hole = .3,
             color_discrete_sequence=px.colors.qualitative.G10)
fig.show()

# poner detalles a la gráfica
fig.update_layout(
    template = 'simple_white',
    title_x = 0.5,)
fig.show()

g1 = dt.groupby(['Department','Gender'])[['EmployeeCount']].count().reset_index()
fig = px.bar(g1, x="Gender", y="EmployeeCount", color="Department", title="Genero y el departamento", barmode = 'group')
fig.show()

g1 = dt.groupby(['EducationField','Gender'])[['EmployeeCount']].count().reset_index()
fig = px.bar(g1, x="Gender", y="EmployeeCount", color="EducationField", title="Genero y campo de educación", barmode = 'group')
fig.show()

"""###Graficas retiros"""

g1 = rangos.groupby(['MonthlyIncome_range','Desercion'])[['EmployeeCount']].count().reset_index()
fig = px.bar(g1, x="Desercion", y="EmployeeCount", color="MonthlyIncome_range", title="Retiro y rangos de ingresos", barmode = 'group')
fig.show()

g1 = rangos.groupby(['age_range','Desercion'])[['EmployeeCount']].count().reset_index()
fig = px.bar(g1, x="Desercion", y="EmployeeCount", color="age_range", title="Retiro y rangos de edades", barmode = 'group')
fig.show()

g1 = dt.groupby(['BalanceTrabajoVida','Desercion'])[['EmployeeCount']].count().reset_index()
fig = px.bar(g1, x="Desercion", y="EmployeeCount", color="BalanceTrabajoVida", title="Retiro y balance trabajo-vida privada", barmode = 'group')
fig.show()

g1 = dt.groupby(['BusinessTravel','Desercion'])[['EmployeeCount']].count().reset_index()
fig = px.bar(g1, x="Desercion", y="EmployeeCount", color="BusinessTravel", title="Retiro y Frecuencia de viajes laborales", barmode = 'group')
fig.show()

g1 = dt.groupby(['SatisfaccionAmbiente','Desercion'])[['EmployeeCount']].count().reset_index()
fig = px.bar(g1, x="Desercion", y="EmployeeCount", color="SatisfaccionAmbiente", title="Retiro y Satisfaccion con el medio de trabajo", barmode = 'group')
fig.show()

g1 = dt.groupby(['MaritalStatus','Desercion'])[['EmployeeCount']].count().reset_index()
fig = px.bar(g1, x="Desercion", y="EmployeeCount", color="MaritalStatus", title="Retiro y estado civil", barmode = 'group')
fig.show()

g1 = dt.groupby(['SatisfaccionTrabajo','Desercion'])[['EmployeeCount']].count().reset_index()
fig = px.bar(g1, x="Desercion", y="EmployeeCount", color="SatisfaccionTrabajo", title="Retiro y Satisfaccion con el  trabajo", barmode = 'group')
fig.show()

## Gráfico de las horas

# Se definen las horas de entrada y salidad en el mes de enero
enero_in = in_time.iloc[:,2:21]
enero_out = out_time.iloc[:,2:21]

# Se usa la función para hacer la gráfica
funciones.graf(enero_in, enero_out, '<b>Enero<b>')

# Se definen las horas de entrada y salidad en el mes de febrero
febrero_in = in_time.iloc[:,21:41]
febrero_out = out_time.iloc[:,21:41]

# Se usa la función para hacer la gráfica
funciones.graf(febrero_in, febrero_out, '<b>Febrero<b>')

# Se definen las horas de entrada y salidad en el mes de marzo
marzo_in = in_time.iloc[:,41:62]
marzo_out = out_time.iloc[:,41:62]

# Se usa la función para hacer la gráfica
funciones.graf(marzo_in, marzo_out, '<b>Marzo<b>')

# Se definen las horas de entrada y salidad en el mes de abril
abril_in = in_time.iloc[:,62:84]
abril_out = out_time.iloc[:,62:84]

# Se usa la función para hacer la gráfica
funciones.graf(abril_in, abril_out, '<b>Abril<b>')

# Se definen las horas de entrada y salidad en el mes de mayo
mayo_in = in_time.iloc[:,84:104]
mayo_out = out_time.iloc[:,84:104]

# Se usa la función para hacer la gráfica
funciones.graf(mayo_in, mayo_out, '<b>Mayo<b>')

# Se definen las horas de entrada y salidad en el mes de junio
junio_in = in_time.iloc[:,104:126]
junio_out = out_time.iloc[:,104:126]

# Se usa la función para hacer la gráfica
funciones.graf(junio_in, junio_out, '<b>Junio<b>')

# Se definen las horas de entrada y salidad en el mes de julio
julio_in = in_time.iloc[:,126:148]
julio_out = out_time.iloc[:,126:148]

# Se usa la función para hacer la gráfica
funciones.graf(julio_in, julio_out, '<b>Julio<b>')

# Se definen las horas de entrada y salidad en el mes de agosto
agosto_in = in_time.iloc[:,148:169]
agosto_out = out_time.iloc[:,148:169]

# Se usa la función para hacer la gráfica
funciones.graf(agosto_in, agosto_in, '<b>Agosto<b>')

# Se definen las horas de entrada y salidad en el mes de septiembre
septiembre_in = in_time.iloc[:,169:190]
septiembre_out = out_time.iloc[:,169:190]

# Se usa la función para hacer la gráfica
funciones.graf(septiembre_in, septiembre_out, '<b>Septiembre<b>')

# Se definen las horas de entrada y salidad en el mes de octubre
octubre_in = in_time.iloc[:,190:211]
octubre_out = out_time.iloc[:,190:211]

# Se usa la función para hacer la gráfica
funciones.graf(octubre_in, octubre_out, '<b>Octubre<b>')

# Se definen las horas de entrada y salidad en el mes de noviembre
noviembre_in = in_time.iloc[:,211:229]
noviembre_out = out_time.iloc[:,211:229]

# Se usa la función para hacer la gráfica
funciones.graf(noviembre_in, noviembre_out, '<b>Noviembre<b>')

# Se definen las horas de entrada y salidad en el mes de diciembre
diciembre_in = in_time.iloc[:,229:-1]
diciembre_out = out_time.iloc[:,229:-1]

# Se usa la función para hacer la gráfica
funciones.graf(diciembre_in, diciembre_out, '<b>Diciembre<b>')