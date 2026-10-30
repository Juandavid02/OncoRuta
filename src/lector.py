import pandas as pd

def cargar():
    df = pd.read_excel("data/datos_clinicos.xlsx", sheet_name=None)
    pacientes = df["Pacientes"]
    matriz_Tratamientos = df["Matriz_Tratamientos"]
    return pacientes, matriz_Tratamientos

def validar(pacientes, matriz_Tratamientos):
    validar_pacientes(pacientes)
    validar_matriz_Tratamientos(matriz_Tratamientos)

def validar_pacientes(pacientes):
    if pacientes.empty:
        raise ValueError("La hoja 'Pacientes' está vacía.")
    columnas_esperadas = ["ID_Paciente", "Nombre_Anonimizado",
                        "Severidad_Diagnostico", "Insuficiencia_Renal", 
                        "Cardiopatia", "Edad_Avanzada_Fragil", "Inmunosupresion", 
                        "Minimizar_Costo_Financiero", "Maximizar_Supervivencia"]
    if pacientes.isnull().any().any():
        raise ValueError("La hoja 'Pacientes' contiene valores nulos.")
    faltantes = set(columnas_esperadas) - set(pacientes.columns)
    if faltantes:
        raise ValueError(f"Columnas faltantes en la hoja 'Pacientes': {faltantes}")
    columnas_binarias = ["Insuficiencia_Renal", "Cardiopatia",
                        "Edad_Avanzada_Fragil", "Inmunosupresion",
                        "Minimizar_Costo_Financiero", "Maximizar_Supervivencia"]
    if pacientes[columnas_binarias].isin([0, 1]).all().all() == False: #IA genariva para poder recorrer todas las columnas binarias y verificar que solo contengan valores 0 o 1
        raise ValueError("Las columnas binarias deben contener solo valores 0 o 1.")
    if (pacientes["Severidad_Diagnostico"] < 1).any() or (pacientes["Severidad_Diagnostico"] > 5).any():
        raise ValueError("La columna 'Severidad_Diagnostico' debe contener valores entre 1 y 5.")
    suma_preferencias = pacientes["Minimizar_Costo_Financiero"] + pacientes["Maximizar_Supervivencia"]
    if (suma_preferencias != 1).any():
        raise ValueError("Cada paciente debe tener exactamente una preferencia activa.")

def validar_matriz_Tratamientos(matriz_Tratamientos):
    if matriz_Tratamientos.empty:
        raise ValueError("La hoja 'Matriz_Tratamientos' está vacía.")
    if matriz_Tratamientos.isnull().any().any():
        raise ValueError("La hoja 'Matriz_Tratamientos' contiene valores nulos.")
    columnas_esperadas = ["Tratamiento", "Fase_Origen",
                        "Fase_Destino", "Costo_Financiero_Base",
                        "Tasa_Efectividad_Base", "Multiplicador_Riesgo_Renal", 
                        "Multiplicador_Riesgo_Cardio", "Multiplicador_Riesgo_Edad",
                        "Multiplicador_Inmuno"]
    faltantes = set(columnas_esperadas) - set(matriz_Tratamientos.columns)
    if faltantes:
        raise ValueError(f"Columnas faltantes en la hoja 'Matriz_Tratamientos': {faltantes}")
    if (matriz_Tratamientos["Costo_Financiero_Base"] < 0).any():
        raise ValueError("La columna 'Costo_Financiero_Base' debe contener valores no negativos.") 
    if (matriz_Tratamientos["Tasa_Efectividad_Base"] < 0).any() or (matriz_Tratamientos["Tasa_Efectividad_Base"] > 1).any():
        raise ValueError("La columna 'Tasa_Efectividad_Base' debe contener valores entre 0 y 1.")
    if (matriz_Tratamientos["Multiplicador_Riesgo_Renal"] < 0).any() or (matriz_Tratamientos["Multiplicador_Riesgo_Cardio"] < 0).any() or (matriz_Tratamientos["Multiplicador_Riesgo_Edad"] < 0).any() or (matriz_Tratamientos["Multiplicador_Inmuno"] < 0).any():
        raise ValueError("Las columnas de multiplicadores de riesgo deben contener valores no negativos.")
    if "Diagnostico" not in matriz_Tratamientos["Fase_Origen"].values:
        raise ValueError("Ninguna arista parte de 'Diagnostico'.")
    if "Alta" not in matriz_Tratamientos["Fase_Destino"].values:
        raise ValueError("Ninguna arista llega a 'Alta'.")

def obtener_paciente(pacientes, id_paciente):
    paciente = pacientes[pacientes["ID_Paciente"] == id_paciente]
    if paciente.empty:
        raise ValueError(f"No se encontró el paciente con ID {id_paciente}.")
    return paciente.to_dict(orient="records")[0]

def obtener_aristas(matriz_Tratamientos):
    return matriz_Tratamientos.to_dict(orient="records")

if __name__ == "__main__":
    pacientes, matriz = cargar()
    validar(pacientes, matriz)
    print("Validación exitosa:", len(pacientes), "pacientes y", len(matriz), "aristas.")