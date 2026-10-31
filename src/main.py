from lector import cargar, validar, obtener_paciente, obtener_aristas
from grafo import construir_grafo, dibujar_grafo
from busqueda import bfs

def main():
    # 1. Cargar y validar
    pacientes, matriz = cargar()
    validar(pacientes, matriz)
    print(f"Datos OK: {len(pacientes)} pacientes, {len(matriz)} aristas\n")

    # 2. Construir el grafo
    aristas = obtener_aristas(matriz)
    grafo = construir_grafo(aristas)
    print(f"Grafo: {grafo.number_of_nodes()} nodos, {grafo.number_of_edges()} aristas")
    for origen, destino, datos in grafo.out_edges(data=True):
        print(f"  {origen} -> {destino} ({datos['tratamiento']})")
    print()

    # 3. Probar BFS
    print(f"{'ID':<6}{'Algoritmo':<10}{'Ruta':<28}{'Costo':<8}{'Nodos exp.'}")
    print("-" * 62)
    for id_paciente in pacientes["ID_Paciente"]:
        r = bfs(grafo)
        ruta = " > ".join(r["ruta_propuesta"])
        print(f"{id_paciente:<6}{r['algoritmo']:<10}{ruta:<28}{r['costo_total']:<8}{r['nodos_expandidos']}")
    dibujar_grafo(grafo)

if __name__ == "__main__":
    main()