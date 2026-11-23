import math
import networkx as nx
import matplotlib.pyplot as plt


def construir_grafo(aristas):
    """Construye un grafo dirigido a partir de la lista de aristas."""
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

def obtener_maximizacion(paciente):
    if paciente["Maximizar_Supervivencia"] == 1:
        return 0.2, 100000
    if paciente["Minimizar_Costo_Financiero"] == 1:
        return 1.5, 80000
    return 1.0, 50000

def peso_severidad(paciente):
    return 1 + (paciente["Severidad_Diagnostico"] -1 )/4

def calcular_Gn(datos, paciente):
    alpha, beta = obtener_maximizacion(paciente)
    efectividad = datos["efectividad"]
    if efectividad <= 0:
        efectividad = float('inf')
    falla = -math.log(efectividad)
    riesgo = peso_severidad(paciente) * producto_multiplicadores(datos, paciente) * falla
    return datos["costo_base"] * alpha + beta * riesgo

def calcular_Hn(datos, paciente):
    """Igual que el costo real, pero con ∏multiplicadores = 1."""
    alpha, beta = obtener_maximizacion(paciente)
    efectividad = datos["efectividad"]
    if efectividad <= 0:
        return float("inf")
    return datos["costo_base"] * alpha + beta * peso_severidad(paciente) * -math.log(efectividad)

def producto_multiplicadores(datos, paciente):
    """Multiplica solo los multiplicadores de los factores de riesgo activos de los pacientes."""
    producto = 1.0
    if paciente["Insuficiencia_Renal"] == 1:
        producto *= datos["mult_renal"]
    if paciente["Cardiopatia"] == 1:
        producto *= datos["mult_cardio"]
    if paciente["Edad_Avanzada_Fragil"] == 1:
        producto *= datos["mult_edad"]
    if paciente["Inmunosupresion"] == 1:
        producto *= datos["mult_inmuno"]
    return producto

def calcular_heuristica(grafo, meta='Alta'):
    """h(n) = costo mínimo de n a la meta usando costo_h (sin multiplicadores)."""
    dist = nx.single_source_dijkstra_path_length(grafo.reverse(copy=True), meta, weight='costo_h')
    return {nodo: dist.get(nodo, float('inf')) for nodo in grafo.nodes}

def asignar_costos(grafo, paciente, meta='Alta'):
    copia = grafo.copy()
    for _, _, datos in copia.edges(data=True):
        datos["costo"] = calcular_Gn(datos, paciente)
        datos["costo_h"] = calcular_Hn(datos, paciente)
    h = calcular_heuristica(copia, meta)
    for nodo in copia.nodes:
        copia.nodes[nodo]["h"] = h[nodo]
    return copia

# Posiciones fijas: el flujo se lee de izquierda a derecha
POSICIONES = {
    "Diagnostico":   (0, 0),
    "Post_Op_Mayor": (1, 1.5),
    "Post_Op_Menor": (1, 0.5),
    "Consolidacion": (2, 1),
    "Alta":          (3, 0),
}

COLORES_ALGORITMO = {"BFS": "#1f77b4", "UCS": "#2ca02c", "A*": "#d62728"}


def obtener_posiciones(grafo):
    """Usa las posiciones fijas; si aparece un nodo desconocido, usa un layout automático."""
    if all(nodo in POSICIONES for nodo in grafo.nodes):
        return POSICIONES
    return nx.spring_layout(grafo, seed=42)


def formatear_h(valor):
    if valor is None or valor == float("inf"):
        return "∞"
    return f"{valor:,.0f}"


def dibujar_grafo(grafo, ax=None, ruta_estados=None, ruta_tratamientos=None,
                  color_ruta="#d62728", mostrar_h=False,
                  titulo="Grafo de Tratamientos", tam_nodo=2800, tam_fuente=8):
    """
    Dibuja el grafo con posiciones fijas y etiquetas de tratamientos en las aristas.
    - ax: eje de matplotlib donde dibujar (si es None se abre una ventana propia).
    - ruta_estados / ruta_tratamientos: ruta elegida por un algoritmo, que se resalta.
    - mostrar_h: escribe h(n) debajo del nombre de cada nodo (requiere asignar_costos).
    """
    ventana_propia = ax is None
    if ventana_propia:
        _, ax = plt.subplots(figsize=(11, 6))

    pos = obtener_posiciones(grafo)
    hay_ruta = bool(ruta_estados)
    nodos_ruta = set(ruta_estados or [])
    # Cada paso de la ruta se identifica por (origen, destino, tratamiento),
    # porque en un MultiDiGraph puede haber varias aristas entre las mismas fases.
    aristas_ruta = set()
    if hay_ruta and ruta_tratamientos:
        aristas_ruta = set(zip(ruta_estados[:-1], ruta_estados[1:], ruta_tratamientos))

    colores_nodos = []
    for nodo in grafo.nodes:
        if not hay_ruta:
            colores_nodos.append("lightblue")
        elif nodo in nodos_ruta:
            colores_nodos.append(color_ruta)
        else:
            colores_nodos.append("#e0e0e0")
    nx.draw_networkx_nodes(grafo, pos, node_color=colores_nodos,
                           edgecolors="#555555", node_size=tam_nodo, ax=ax)

    # Nombre de la fase encima del nodo y h(n) debajo, para que no se salgan del círculo
    radio = (tam_nodo ** 0.5) / 2 + 2  # radio del nodo en puntos
    for nodo, datos in grafo.nodes(data=True):
        x, y = pos[nodo]
        ax.annotate(nodo, (x, y), xytext=(0, radio if mostrar_h else 0), textcoords="offset points",
                    ha="center", va="bottom" if mostrar_h else "center",
                    fontsize=tam_fuente, fontweight="bold")
        if mostrar_h and "h" in datos:
            ax.annotate(f"h={formatear_h(datos['h'])}", (x, y), xytext=(0, -radio),
                        textcoords="offset points", ha="center", va="top",
                        fontsize=tam_fuente, color="#333333",
                        bbox=dict(boxstyle="round,pad=0.2", facecolor="#fff8dc",
                                  edgecolor="#c8a800", alpha=0.95))

    # Agrupar las aristas por par (origen, destino) para detectar las paralelas
    pares = {}
    for u, v, k, datos in grafo.edges(keys=True, data=True):
        pares.setdefault((u, v), []).append(datos)

    for (u, v), lista in pares.items():
        n = len(lista)
        for i, datos in enumerate(lista):
            # Una sola arista: recta. Varias: curvas simétricas (-0.25 y 0.25)
            rad = 0.0 if n == 1 else -0.25 + 0.5 * i / (n - 1)
            resaltada = (u, v, datos["tratamiento"]) in aristas_ruta
            if resaltada:
                color, ancho = color_ruta, 3.0
            elif hay_ruta:
                color, ancho = "#b0b0b0", 1.0
            else:
                color, ancho = "black", 1.2

            nx.draw_networkx_edges(
                grafo, pos, edgelist=[(u, v)],
                connectionstyle=f"arc3,rad={rad}",
                arrows=True, arrowsize=18, node_size=tam_nodo,
                edge_color=color, width=ancho, ax=ax,
            )

            # Etiqueta en el punto medio de la curva
            x1, y1 = pos[u]
            x2, y2 = pos[v]
            dx, dy = x2 - x1, y2 - y1
            xm = (x1 + x2) / 2 + 0.5 * rad * dy
            ym = (y1 + y2) / 2 - 0.5 * rad * dx
            ax.text(xm, ym, datos["tratamiento"], fontsize=tam_fuente,
                    ha="center", va="center",
                    color=color_ruta if resaltada else "black",
                    fontweight="bold" if resaltada else "normal",
                    bbox=dict(facecolor="white", edgecolor="none", alpha=0.85))

    ax.set_title(titulo, fontsize=tam_fuente + 2)
    ax.axis("off")
    ax.margins(0.12)
    if ventana_propia:
        plt.tight_layout()
        plt.show()
    return ax
