import tkinter as tk
from tkinter import ttk
from tkinter import filedialog

from tkinter import messagebox

from lector import cargar, validar, obtener_aristas
from grafo import construir_grafo
from reporte import generar_reporte_seleccion, convertir_reportes_a_dataframe, tabla_final_reportes
import pandas as pd



class AppOncoRuta(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("OncoRuta")
        self.geometry("800x600")
        self.state("zoomed")
        self.ruta_excel = None        
        self.pacientes = None
        self.matriz = None
        self.grafo = None
        self.tabla_reportes = None
        self.tabla_final = None
        self.cargar_datos_iniciales()
        self.crear_pestanas()
        self.crear_tab_datos()
        self.crear_tab_resultados()
        

    def crear_pestanas(self):
        self.pestanas = ttk.Notebook(self)
        self.pestanas.pack(fill="both", expand=True)

        self.tab_datos = ttk.Frame(self.pestanas)
        self.tab_resultados = ttk.Frame(self.pestanas)
        self.tab_grafo = ttk.Frame(self.pestanas)

        self.pestanas.add(self.tab_datos, text="Datos", )
        self.pestanas.add(self.tab_resultados, text="Resultados")
        self.pestanas.add(self.tab_grafo, text="Grafo")

    def crear_tab_datos(self):
        barra = ttk.Frame(self.tab_datos)
        barra.pack(fill="x", padx=10, pady=10)

        self.boton_cargar = ttk.Button(barra, text="Cargar Excel", command=self.cargar_excel)
        self.boton_cargar.pack(side="left")
        
        self.etiqueta_archivo = ttk.Label(barra, text="Ningún archivo cargado")
        self.etiqueta_archivo.pack(side="left", padx=10)

    def cargar_excel(self):
        ruta = filedialog.askopenfilename(title="Seleccionar archivo Excel", filetypes=[("Excel o CSV", "*.xlsx *.csv")])
        if ruta == "":
            return
        self.ruta_excel = ruta
        self.etiqueta_archivo.config(text=ruta)

    def crear_tab_resultados(self):
        zona_paciente  = ttk.Frame(self.tab_resultados)
        zona_paciente.pack(fill="x", padx=10, pady=10)

        ttk.Label(zona_paciente , text="Paciente").pack(anchor="w")
        self.var_paciente = tk.StringVar(value="Todos")
        self.combo_paciente = ttk.Combobox(zona_paciente , textvariable=self.var_paciente, state="readonly",  values=self.obtener_paciente(), width=10)
        self.combo_paciente.pack(fill="x", pady=5)

        zona_opciones = ttk.Frame(self.tab_resultados)
        zona_opciones.pack(fill="x", padx=10)
        self.var_bfs = tk.BooleanVar(value=True)
        self.var_ucs = tk.BooleanVar(value=True)
        self.var_a_star = tk.BooleanVar(value=True)

        ttk.Checkbutton(zona_opciones, text="BFS", variable=self.var_bfs).pack(side="left", padx=10)
        ttk.Checkbutton(zona_opciones, text="UCS", variable=self.var_ucs).pack(side="left", padx=10)
        ttk.Checkbutton(zona_opciones, text="A*", variable=self.var_a_star).pack(side="left", padx=10)

        self.boton_ejecutar = ttk.Button(zona_opciones, text="Ejecutar", command=self.ejecutar_algoritmos)
        self.boton_ejecutar.pack(side="left", padx=20, ipadx=10)

        self.etiqueta_estado = ttk.Label(self.tab_resultados, text="Ejecuta primero")
        self.etiqueta_estado.pack(anchor="w", padx=10, pady=10)
        self.crear_tabla()

    def ejecutar_algoritmos(self):
        algoritmos = []
        if self.var_bfs.get():
            algoritmos.append("BFS")
        if self.var_ucs.get():
            algoritmos.append("UCS")
        if self.var_a_star.get():
            print("En construcción: A*")

        if not algoritmos:
            self.etiqueta_estado.config(text="Elige al menos un algoritmo")
            return
        paciente = self.var_paciente.get()
        try:
            reportes = generar_reporte_seleccion(self.pacientes, self.grafo, paciente, algoritmos)
        except ValueError as e:
            self.etiqueta_estado.config(text=f"Error: {str(e)}")
            return  
        self.tabla_reportes = convertir_reportes_a_dataframe(reportes)
        self.tabla_final = tabla_final_reportes(self.tabla_reportes)
        self.mostrar_tabla()
        self.etiqueta_estado.config(text=f"listos {len(self.tabla_final)} reportes generados")

    def cargar_datos_iniciales(self):
        try:
            pacientes, matriz = cargar()
            validar(pacientes, matriz)
            self.pacientes = pacientes
            self.matriz = matriz
            self.grafo = construir_grafo(obtener_aristas(matriz))
        except Exception  as e:
            messagebox.showerror("Error al cargar datos", str(e))   

    def obtener_paciente(self):
        if self.pacientes is None:
            return ["Todos"]
        return ["Todos"] + self.pacientes["ID_Paciente"].tolist()

    def crear_tabla(self):
        zona_tabla = ttk.Frame(self.tab_resultados)
        zona_tabla.pack(fill="both", expand=True, padx=10, pady=10)
        self.columnas = [
                "ID_Paciente", "Algoritmo", "Ruta Propuesta", "Costo Económico",
                "Nodos Expandidos", "Costo del Algoritmo", "Efectividad (%)", "Tiempo (ms)",
            ]

        self.vista_tabla = ttk.Treeview(zona_tabla, columns=self.columnas, show="headings")
        for nombre in self.columnas:
            self.vista_tabla.heading(nombre, text=nombre)
            self.vista_tabla.column(nombre, width=100, anchor="center")
        self.vista_tabla.column("Ruta Propuesta", width=200, anchor="w")
        self.vista_tabla.pack(fill="both", expand=True)


    def mostrar_tabla(self):
        for fila in self.vista_tabla.get_children():
            self.vista_tabla.delete(fila)

        for fila in self.tabla_final.itertuples(index=False):
            valores = ["-" if pd.isna(valor) else valor for valor in fila]            
            self.vista_tabla.insert("", "end", values=valores)

if __name__ == "__main__":
    app = AppOncoRuta()
    app.mainloop()

