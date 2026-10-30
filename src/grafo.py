import networkx as nx
import matplotlib.pyplot as plt

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


def dibujar_grafo(grafo):
    # Posiciones fijas: el flujo se lee de izquierda a derecha
    pos = {
        "Diagnostico":   (0, 0),
        "Post_Op_Mayor": (1, 1.5),
        "Post_Op_Menor": (1, 0.5),
        "Consolidacion": (2, 1),
        "Alta":          (3, 0),
    }
    tam_nodo = 2800

    fig, ax = plt.subplots(figsize=(11, 6))
    nx.draw_networkx_nodes(grafo, pos, node_color="lightblue",
                           node_size=tam_nodo, ax=ax)
    nx.draw_networkx_labels(grafo, pos, font_size=8, ax=ax)

    # Agrupar las aristas por par (origen, destino) para detectar las paralelas
    pares = {}
    for u, v, k, datos in grafo.edges(keys=True, data=True):
        pares.setdefault((u, v), []).append(datos)

    for (u, v), lista in pares.items():
        n = len(lista)
        for i, datos in enumerate(lista):
            # Una sola arista: recta. Varias: curvas simétricas (-0.25 y 0.25)
            rad = 0.0 if n == 1 else -0.25 + 0.5 * i / (n - 1)

            nx.draw_networkx_edges(
                grafo, pos, edgelist=[(u, v)],
                connectionstyle=f"arc3,rad={rad}",
                arrows=True, arrowsize=18, node_size=tam_nodo, ax=ax,
            )

            # Etiqueta en el punto medio de la curva
            x1, y1 = pos[u]
            x2, y2 = pos[v]
            dx, dy = x2 - x1, y2 - y1
            xm = (x1 + x2) / 2 + 0.5 * rad * dy
            ym = (y1 + y2) / 2 - 0.5 * rad * dx
            ax.text(xm, ym, datos["tratamiento"], fontsize=8,
                    ha="center", va="center",
                    bbox=dict(facecolor="white", edgecolor="none", alpha=0.85))

    ax.set_title("Grafo de Tratamientos")
    ax.axis("off")
    plt.tight_layout()
    plt.show()