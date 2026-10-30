from collections import deque
import networkx as nx


def bfs(grafo, inicio='Diagnostico', meta='Alta'):
    """
    Nivel 1: BFS.
    Ignora costos y riesgos del paciente (peso = 1 por arista).
    Retorna: ruta_estados, ruta_tratamientos, costo_acumulado, nodos_expandidos.
    """
    frontera = deque([(inicio, [inicio], [], 0.0)])
    explorados = set()
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

        if nodo_actual in explorados:
            continue

        explorados.add(nodo_actual)
        nodos_expandidos += 1

        for vecino in grafo.neighbors(nodo_actual):
            if vecino in explorados:
                continue

            atributos = grafo[nodo_actual][vecino]
            accion = atributos.get('accion', f"{nodo_actual}->{vecino}")

            costo_arista = 1

            frontera.append((
                vecino,
                camino_estados + [vecino],
                camino_acciones + [accion],
                costo_acum + costo_arista,
            ))

    return None