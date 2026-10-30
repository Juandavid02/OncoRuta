from costos import calcular_peso_arista

def construir_grafo(pacientes, matriz_Tratamientos):
    """
    Construye un grafo dirigido ponderado a partir de los datos de pacientes y la matriz de tratamientos.
    
    Pacientes: Diccionario o Serie de Pandas con los datos de 1 pacientes.
    matriz_Tratamientos: Diccionario o Serie de Pandas con los datos de 1 fila de Matriz_matriz_Tratamientoss.
    
    Retorna un diccionario que representa el grafo, donde las llaves son los nodos y los valores son listas de tuplas (nodo_destino, peso_arista).
    """
    estados = ['Diagnostico', 'Post_Op_Mayor', 'Post_Op_Menor', 'Consolidacion', 'Alta']
    grafo = {estado: [] for estado in estados}

    for _, fila in matriz_Tratamientos.iterrows():
        origen = fila['Estado_Origen']
        destino = fila['Estado_Destino']
        accion = fila['Tratamiento']
        efectividad = fila['Tasa_Efectividad_Base']

        costo_unificado = calcular_peso_arista(pacientes, fila)

        arista = {
            'destino': destino,
            'accion': accion,
            'efectividad': efectividad,
            'costo_unificado': costo_unificado
        }

        grafo[origen].append(arista)

    return grafo