from lector import cargar, validar, obtener_paciente, obtener_aristas
from grafo import construir_grafo, dibujar_grafo, asignar_costos
from busqueda import bfs, ucs
from reporte import generar_reporte_completo

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
        print(f"{id_paciente:<6}{r['algoritmo']:<10}{ruta:<55}{r['costo_total']:<40}{r['nodos_expandidos']}")
    #dibujar_grafo(grafo)
    dibujar_grafo(grafo)

    # 5. Probar UCS
    print(f"\n{'ID':<6}{'Algoritmo':<10}{'Ruta':<55}{'Costo':<20}{'Costo Financiero':<20}{'Nodos exp.'}")
    print("-" * 120)
    for id_paciente in pacientes["ID_Paciente"]:
        paciente = obtener_paciente(pacientes, id_paciente)
        grafo_ucs = asignar_costos(grafo, paciente)
        r = ucs(grafo_ucs)
        ruta = " > ".join(r["ruta_propuesta"])
        print (f"{id_paciente:<6}{r['algoritmo']:<10}{ruta:<55}{r['costo_total']:<20}{r['costo_financiero']:<20}{r['nodos_expandidos']}")
    #dibujar_grafo(grafo)

    # 6. Generar reporte completo
    filas = generar_reporte_completo(pacientes, ["BFS", "UCS"], grafo)
    print(len(filas))     # debe dar 24
    print(filas[0])       # P001 con BFS
    print(filas[1])       # P001 con UCS

    un_paciente = pacientes[pacientes["ID_Paciente"] == "P004"]
    print(len(generar_reporte_completo(un_paciente, ["BFS", "UCS"], grafo)))   # debe dar 2

if __name__ == "__main__":
    main()