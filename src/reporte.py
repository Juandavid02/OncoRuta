from busqueda import bfs, ucs

from lector import obtener_paciente
from grafo import asignar_costos
import time
import pandas as pd

ALGORITMOS = {
    "BFS": bfs,
    "UCS": ucs,
}

def generar_reporte_seleccion(pacientes, grafo, id_paciente, algoritmos):
    """
    Genera los reportes según lo que eligió el usuario en la app.
    id_paciente puede ser un ID (por ejemplo "P003") o "Todos".
    """
    if not algoritmos:
        raise ValueError("Debes elegir al menos un algoritmo.")
    if id_paciente == "Todos":
        return generar_reporte_completo(pacientes, algoritmos, grafo)
    paciente = obtener_paciente(pacientes, id_paciente)
    grafo_paciente = asignar_costos(grafo, paciente)
    return generar_reporte_paciente_varios_algoritmos(id_paciente, algoritmos, grafo_paciente)

def generar_reporte_paciente(id_paciente, algoritmo, grafo_paciente):
    """
    Genera un reporte
    """
    algoritmo = algoritmo.upper().strip()
    if algoritmo not in ALGORITMOS:
        raise ValueError(f"Algoritmo '{algoritmo}' no reconocido. Algoritmos disponibles: {', '.join(ALGORITMOS.keys())}")
    inicio = time.perf_counter()
    resultado = ALGORITMOS[algoritmo](grafo_paciente)
    fin = time.perf_counter()
    tiempo_ejecucion = (fin - inicio) * 1000
    if resultado is None:
        return {
            'id_paciente': id_paciente,
            'algoritmo': algoritmo,
            'camino_estados': [],
            'ruta_propuesta': [],
            'costo_total': None,
            'nodos_expandidos': None,
            'costo_financiero': None,
            'tasa_efectividad': None,
            'tiempo_ejecucion': tiempo_ejecucion,
            'hay_ruta': False
        }
    return {
        'id_paciente': id_paciente,
        'algoritmo': resultado['algoritmo'],
        'camino_estados': resultado['camino_estados'],
        'ruta_propuesta': resultado['ruta_propuesta'],
        'costo_total': resultado['costo_total'],
        'nodos_expandidos': resultado['nodos_expandidos'],
        'costo_financiero': resultado['costo_financiero'],
        'tasa_efectividad': resultado['tasa_efectividad'],
        'tiempo_ejecucion': tiempo_ejecucion,
        'hay_ruta': True
    }

def generar_reporte_paciente_varios_algoritmos(id_paciente, algoritmos, grafo_paciente):
    """
    Genera un reporte para un paciente con varios algoritmos.
    """
    reportes = []
    for algoritmo in algoritmos:
        reporte = generar_reporte_paciente(id_paciente, algoritmo, grafo_paciente)
        reportes.append(reporte)
    return reportes

def generar_reporte_completo(pacientes, algoritmos, grafo):
    """
    Genera un reporte completo para todos los pacientes y algoritmos especificados.
    """
    reportes = []
    for id_paciente in pacientes["ID_Paciente"]:
        paciente = obtener_paciente(pacientes, id_paciente)
        grafo_paciente = asignar_costos(grafo, paciente)
        reportes_paciente = generar_reporte_paciente_varios_algoritmos(id_paciente, algoritmos, grafo_paciente)
        reportes.extend(reportes_paciente)
    return reportes

def ruta_a_texto(fila):
    """
    Convierte la ruta de un reporte a un texto legible.
    """
    if fila['hay_ruta']:
        return " → ".join(fila['ruta_propuesta'])
    else:
        return "Sin ruta"
    

def convertir_reportes_a_dataframe(reportes):
    """
    Convierte una lista de reportes en un DataFrame de pandas.
    """
    if reportes is None or len(reportes) == 0:
        return pd.DataFrame()
    tabla=pd.DataFrame(reportes)
    tabla['costo_total'] = tabla['costo_total'].astype(float)
    tabla['costo_financiero'] = tabla['costo_financiero'].astype(float)
    tabla['nodos_expandidos'] = tabla['nodos_expandidos'].astype('Int64')
    tabla['tasa_efectividad'] = (tabla['tasa_efectividad'].astype(float)*100).round(1)
    tabla['ruta_propuesta'] = tabla.apply(ruta_a_texto, axis=1)
    return tabla

def tabla_final_reportes(tabla_reportes):
    if tabla_reportes is None or tabla_reportes.empty:
        return pd.DataFrame()
    columnas = [
        'id_paciente', 'algoritmo', 'ruta_propuesta',
        'costo_financiero', 'nodos_expandidos',
        'costo_total', 'tasa_efectividad', 'tiempo_ejecucion',
    ]
    tabla_final = tabla_reportes[columnas]
    tabla_final = tabla_final.rename(columns={
        'id_paciente': 'ID_Paciente',
        'algoritmo': 'Algoritmo',
        'ruta_propuesta': 'Ruta Propuesta',
        'costo_financiero': 'Costo Económico',
        'nodos_expandidos': 'Nodos Expandidos',
        'costo_total': 'Costo del Algoritmo',
        'tasa_efectividad': 'Efectividad (%)',
        'tiempo_ejecucion': 'Tiempo (ms)',
    })
    return tabla_final

def exportar_reportes(tabla_reportes, ruta):
    """
    Exporta los reportes a un archivo CSV.
    """
    if tabla_reportes is None or tabla_reportes.empty:
        raise ValueError("No hay reportes para exportar.")
    if ruta.lower().endswith('.csv'):
        tabla_reportes.to_csv(ruta, index=False)
    elif ruta.lower().endswith('.xlsx'):
        tabla_reportes.to_excel(ruta, index=False, encoding='utf-8-sig')
    else:
        raise ValueError("Formato de archivo no soportado.")
