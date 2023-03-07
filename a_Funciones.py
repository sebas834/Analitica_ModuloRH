from plotly.subplots import make_subplots
import plotly.graph_objects as go

def eliminar_fecha(df, fecha):
  df[fecha] = df[fecha].str[11:]

# Función para hacer las gráficas
def graf(df_in, df_out, mes):
  fig = make_subplots(rows = 2, cols = 2, subplot_titles=("<b>Horas de entrada<b>", "<b>Horas de salida<b>"))

  fig.add_trace(go.Violin(y = df_in.iloc[:,0].sort_values(), name = 'Primer día'), row = 1, col = 1)
  fig.add_trace(go.Violin(y = df_out.iloc[:,0].sort_values(), name = 'Primer día'), row = 1, col = 2)
  fig.add_trace(go.Violin(y = df_in.iloc[:,-1].sort_values(), name = 'Último día'), row = 2, col = 1)
  fig.add_trace(go.Violin(y = df_out.iloc[:,-1].sort_values(), name = 'Último día'), row = 2, col = 2)

  fig.update_layout(title_text = mes, title_x = 0.5, showlegend = False, height = 650)
  fig.show()