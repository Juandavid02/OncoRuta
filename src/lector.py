import pandas as pd

df = pd.read_excel("data/datos_clinicos.xlsx", sheet_name=None)
pacientes = df["Pacientes"]
matriz_Tratamientos = df["Matriz_Tratamientos"]
pacientes.head()