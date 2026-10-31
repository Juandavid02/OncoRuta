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
    frontera = deque([(inicio, [inicio], [], 0.0, 0.0, 1.0)])
    explorados = set()
    explorados.add(inicio)
    nodos_expandidos = 0

    while frontera:
        nodo_actual, camino_estados, camino_acciones, costo_acum, costo_financiero, tasa_efectividad = frontera.popleft()
        if nodo_actual == meta:
            return {
                'algoritmo': 'BFS',
                'camino_estados': camino_estados,
                'ruta_propuesta': camino_acciones,
                'costo_total': costo_acum,
                'nodos_expandidos': nodos_expandidos,
                'costo_financiero': costo_financiero,
                'tasa_efectividad': tasa_efectividad
            }
        nodos_expandidos += 1
        neighbors = list(grafo.out_edges(nodo_actual, data=True))
        for neighbor in neighbors:
            vecino = neighbor[1]
            if vecino not in explorados:
                explorados.add(vecino)
                arista_data = neighbor[2]
                nuevo_costo = costo_acum + arista_data['peso']
                nuevo_costo_financiero = costo_financiero + arista_data['costo_base']
                nueva_tasa_efectividad = tasa_efectividad * arista_data['efectividad']
                frontera.append((vecino, camino_estados + [vecino], camino_acciones + [arista_data['tratamiento']], nuevo_costo, nuevo_costo_financiero, nueva_tasa_efectividad))
    return None

# ---------------------------------------------------------------
# Búsqueda en costo uniforme (UCS)
# ---------------------------------------------------------------

def ucs(grafo, inicio='Diagnostico', meta='Alta'):
    """
    Nivel 2: UCS.
    Considera costos y riesgos del paciente (peso = costo calculado por UCS).
    Retorna: ruta_estados, ruta_tratamientos, costo_acumulado, nodos_expandidos.
    """
    desempate = 0
    frontera = []
    heapq.heappush(frontera, (0.0, desempate, inicio, [inicio], [], 0.0, 1.0))
    costos_minimos = {inicio: 0.0}
    nodos_expandidos = 0

    while frontera:
        costo_acum, _, nodo_actual, camino_estados, camino_acciones, costo_financiero, tasa_efectividad = heapq.heappop(frontera)
        if nodo_actual == meta:
            return {
                'algoritmo': 'UCS',
                'camino_estados': camino_estados,
                'ruta_propuesta': camino_acciones,
                'costo_total': costo_acum,
                'nodos_expandidos': nodos_expandidos,
                'costo_financiero': costo_financiero,
                'tasa_efectividad': tasa_efectividad
            }
        if costo_acum > costos_minimos[nodo_actual]:
            continue
        nodos_expandidos += 1
        neighbors = list(grafo.out_edges(nodo_actual, data=True))
        for neighbor in neighbors:
            vecino = neighbor[1]
            arista_data = neighbor[2]
            costo_total = costo_acum + arista_data['costo']
            if vecino not in costos_minimos or costo_total < costos_minimos[vecino]:
                costos_minimos[vecino] = costo_total
                desempate += 1
                heapq.heappush(frontera, (costo_total, desempate, vecino, camino_estados + [vecino], camino_acciones + [arista_data['tratamiento']], costo_financiero + arista_data['costo_base'], tasa_efectividad * arista_data['efectividad']))
    return None
