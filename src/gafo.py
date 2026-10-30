import networkx as nx
from lector import obtener_aristas, cargar, validar

def calcular_costo(grafo, paciente):
    return 0

def construir_grafo(aristas):
    G = nx.MultiDiGraph()
    for arista in aristas:
        origen = arista["Fase_Origen"]
        destino = arista["Fase_Destino"]
        G.add_edge(origen, destino,
                peso = 1,
                tratamiento=arista["Tratamiento"],
                efectividad=arista["Tasa_Efectividad_Base"],
                costo_base=arista["Costo_Financiero_Base"],
                mult_renal=arista["Multiplicador_Riesgo_Renal"],
                mult_cardio=arista["Multiplicador_Riesgo_Cardio"],
                mult_edad=arista["Multiplicador_Riesgo_Edad"],
                mult_inmuno=arista["Multiplicador_Inmuno"])
    return G


if __name__ == "__main__":
    pacientes, matriz = cargar()
    validar(pacientes, matriz)
    aristas = obtener_aristas(matriz)
    grafo = construir_grafo(aristas)
    print(grafo.number_of_nodes(), "nodos en el grafo.")
    print(grafo.number_of_edges(), "aristas en el grafo.")
