from grafo import calcular_costo_ucs
from grafo import calcular_costo_aestrella
from collections import deque
import heapq

# ---------------------------------------------------------------
# Búsqueda en anchura (BFS)
# ---------------------------------------------------------------

def bfs(grafo, inicio='Diagnostico', meta='Alta'):
    """
    Nivel 1: BFS.
    Ignora costos y riesgos del paciente (peso = 1 por arista).
    Retorna: ruta_estados, ruta_tratamientos, costo_acumulado, nodos_expandidos.
    """
    frontera = deque([(inicio, [inicio], [], 0.0)])
    explorados = set()
    explorados.add(inicio)
    nodos_expandidos = 0

    while frontera:
        nodo_actual, camino_estados, camino_acciones, costo_acum = frontera.popleft()
        if nodo_actual == meta:
            return {
                'algoritmo': 'BFS',
                'camino_estados': camino_estados,
                'ruta_propuesta': camino_acciones,
                'costo_total': costo_acum,
                'nodos_expandidos': nodos_expandidos,
            }
        nodos_expandidos += 1
        neighbors = grafo.out_edges(nodo_actual, data=True)
        for neighbor in neighbors:
            vecino = neighbor[1]
            if vecino not in explorados:
                explorados.add(vecino)
                arista_data = neighbor[2]
                nuevo_costo = costo_acum + arista_data['peso']
                frontera.append((vecino, camino_estados + [vecino], camino_acciones + [arista_data['tratamiento']], nuevo_costo))
    return None

# ---------------------------------------------------------------
# Búsqueda en costo uniforme (UCS)
# ---------------------------------------------------------------

def ucs(grafo, paciente, inicio='Diagnostico', meta='Alta'):
    """
    Nivel 2: UCS (Búsqueda de Costo Uniforme).
    Usa la función de costo unificada C_arista personalizada al paciente.
    Cola de prioridad mínima (heapq); la meta se evalúa al extraer el nodo.
    Retorna: ruta_estados, ruta_tratamientos, costo_acumulado, nodos_expandidos.
    """
    contador = 0
    frontera = [(0.0, contador, inicio, [inicio], [], 0.0)]
    costos_minimos = {inicio: 0.0}
    nodos_expandidos = 0

    while frontera:
        costo_acum, orden, nodo_actual, camino_estados, camino_acciones, costo_fin = heapq.heappop(frontera)

        if costo_acum > costos_minimos.get(nodo_actual, float("inf")):
            continue

        if nodo_actual == meta:
            return {
                'algoritmo': 'UCS',
                'camino_estados': camino_estados,
                'ruta_propuesta': camino_acciones,
                'costo_total': costo_acum,
                'costo_financiero': costo_fin,
                'nodos_expandidos': nodos_expandidos,
            }
        nodos_expandidos += 1
        for origen, vecino, datos in grafo.out_edges(nodo_actual, data=True):
            nuevo_costo = costo_acum + calcular_costo_ucs(datos, paciente)
            if vecino not in costos_minimos or nuevo_costo < costos_minimos[vecino]:
                costos_minimos[vecino] = nuevo_costo
                contador += 1
                heapq.heappush(frontera, (
                    nuevo_costo, contador, vecino,
                    camino_estados + [vecino],
                    camino_acciones + [datos['tratamiento']],
                    costo_fin + datos['costo_base'],
                ))
    return None
