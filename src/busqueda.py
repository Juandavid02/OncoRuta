from collections import deque

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


