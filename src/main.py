from lector import cargar, validar, obtener_paciente, obtener_aristas
from grafo import construir_grafo, dibujar_grafo
from busqueda import bfs
from busqueda import ucs

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

    # 3. Dibujar el grafo
    dibujar_grafo(grafo)

    # 4. Probar BFS
    print(f"{'ID':<6}{'Algoritmo':<10}{'Ruta':<55}{'Costo':<40}{'Nodos exp.'}")
    print("-" * 120)
    for id_paciente in pacientes["ID_Paciente"]:
        r = bfs(grafo)
        ruta = " > ".join(r["ruta_propuesta"])
        print(f"{id_paciente:<6}{r['algoritmo']:<10}{ruta:<55}{r['costo_total']:<40}{r['nodos_expandidos']}")
    #dibujar_grafo(grafo)

    # 5. Probar UCS
    print(f"\n{'ID':<6}{'Algoritmo':<10}{'Ruta':<55}{'Costo':<20}{'Costo Financiero':<20}{'Nodos exp.'}")
    print("-" * 120)
    for id_paciente in pacientes["ID_Paciente"]:
        paciente = obtener_paciente(pacientes, id_paciente)
        r = ucs(grafo, paciente)
        ruta = " > ".join(r["ruta_propuesta"])
        print(f"{id_paciente:<6}{r['algoritmo']:<10}{ruta:<55}{r['costo_total']:<20}{r['costo_financiero']:<20}{r['nodos_expandidos']}")
    #dibujar_grafo(grafo)

if __name__ == "__main__":
    main()