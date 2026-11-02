# OncoRuta

**Sistema de Soporte a Decisiones Clínicas mediante Algoritmos de Búsqueda (SSDC)**

Pipeline de Inteligencia Artificial que transforma datos clínicos y financieros de un archivo Excel en un grafo de estados dinámico, y compara estrategias de búsqueda para proponer la ruta de tratamiento oncológico que mejor balancea costo económico, efectividad médica y riesgo para el paciente.

| | |
|---|---|
| **Materia** | IABS: Búsqueda y Optimización de Soluciones |
| **Integrantes** | Juan David Rojas Heredia |
| | Andres Steeven Oyuela Mendez |

---

## Tabla de contenido

1. [Contexto](#1-contexto)
2. [Arquitectura del pipeline](#2-arquitectura-del-pipeline)
3. [Estructura del proyecto](#3-estructura-del-proyecto)
4. [Requisitos e instalación](#4-requisitos-e-instalación)
5. [Cómo ejecutar](#5-cómo-ejecutar)
6. [Formato del archivo Excel](#6-formato-del-archivo-excel)
7. [Función de costo unificada](#7-función-de-costo-unificada)
8. [Algoritmos de búsqueda](#8-algoritmos-de-búsqueda)
9. [Reporte comparativo y exportación](#9-reporte-comparativo-y-exportación)
10. [La aplicación (interfaz gráfica)](#10-la-aplicación-interfaz-gráfica)
11. [Estado del proyecto](#11-estado-del-proyecto)
12. [Limitaciones conocidas](#12-limitaciones-conocidas)

---

## 1. Contexto

En oncología, una decisión de tratamiento no depende solo de la efectividad teórica de una terapia, sino del perfil biológico del paciente y de sus comorbilidades. Un tratamiento muy efectivo puede ser peligroso si el paciente tiene insuficiencia renal, cardiopatía, edad avanzada y fragilidad, o inmunosupresión.

OncoRuta modela el flujo de tratamiento como un grafo de fases clínicas:

```
Diagnostico ──► Post_Op_Mayor ──┐
     │                          ├──► Consolidacion ──► Alta
     ├───────► Post_Op_Menor ───┘
     │
     └──────────────────────────────────────────────► Alta
                                  (Cuidado_Paliativo)
```

Cada arista es un tratamiento con un costo financiero, una tasa de efectividad y cuatro multiplicadores de riesgo (renal, cardiovascular, edad e inmunosupresión). El costo real de cada arista se calcula de forma distinta para cada paciente.

---

## 2. Arquitectura del pipeline

```
[ Excel: hojas Pacientes y Matriz_Tratamientos ]
                      │
                      ▼
        [ CAPA 1: Inferencia de grafo ]
   (cruza el perfil del paciente con la matriz
     de tratamientos y genera pesos dinámicos)
                      │
                      ▼
       [ CAPA 2: Pipeline de evaluación ]
        ┌─────────────┼─────────────────┐
        ▼             ▼                 ▼
     NIVEL 1       NIVEL 2           NIVEL 3
       BFS           UCS               A*
   (peso = 1)   (costo unificado)   (pendiente)
        └─────────────┼─────────────────┘
                      ▼
      [ CAPA 3: Métricas y comparativa ]
  (costo, efectividad, nodos expandidos, tiempo)
```

1. **Capa 1 – Inferencia de grafo:** lee el Excel con `pandas`, extrae el perfil de un paciente y genera un grafo ponderado personalizado.
2. **Capa 2 – Evaluación:** ejecuta los algoritmos de búsqueda sobre el grafo del paciente.
3. **Capa 3 – Métricas:** consolida costo económico, efectividad estimada, tiempo de cómputo y nodos expandidos.

---

## 3. Estructura del proyecto

```
oncoruta/
├── data/
│   └── datos_clinicos.xlsx     # Pool de pacientes y matriz de tratamientos
├── src/
│   ├── lector.py               # Lectura y validación del Excel
│   ├── grafo.py                # Construcción del grafo y cálculo de costos
│   ├── busqueda.py             # BFS y UCS (A* pendiente)
│   ├── reporte.py              # Reportes, tabla comparativa y exportación
│   ├── main.py                 # Ejecución por consola (pruebas del pipeline)
│   └── app.py                  # Interfaz gráfica (Tkinter)
├── pyproject.toml
├── .python-version
└── README.md
```

| Módulo | Responsabilidad |
|---|---|
| `lector.py` | `cargar(ruta)` lee las dos hojas; `validar` revisa columnas, nulos, valores binarios, rangos y que exista una única preferencia activa por paciente; `obtener_paciente` y `obtener_aristas` entregan los datos al resto del sistema. |
| `grafo.py` | `construir_grafo` crea un `MultiDiGraph` de NetworkX; `asignar_costos` calcula el costo de cada arista según el paciente; `dibujar_grafo` dibuja el grafo con matplotlib. |
| `busqueda.py` | Implementación propia de BFS (con `collections.deque`) y UCS (con `heapq`). No se usan algoritmos de grafos de NetworkX: la librería solo se usa para construir el grafo y leer los vecinos. |
| `reporte.py` | Ejecuta los algoritmos, mide el tiempo, arma la tabla con pandas y la exporta. |
| `app.py` | Ventana principal con pestañas, selección de paciente y algoritmos, tabla de resultados y exportación. |

---

## 4. Requisitos e instalación

**Requisitos**

- Python 3.11 o superior
- Dependencias (definidas en `pyproject.toml`): `pandas`, `networkx`, `matplotlib`, `openpyxl`
- Tkinter (viene incluido con Python en Windows y macOS; en Linux puede requerir instalar `python3-tk`)

**Instalación con `uv`**

```bash
uv sync
```

**Instalación con `pip`**

```bash
python -m venv .venv

# Windows
.venv\Scripts\activate
# Linux / macOS
source .venv/bin/activate

pip install pandas networkx matplotlib openpyxl
```

---

## 5. Cómo ejecutar

> Ejecuta siempre los comandos **desde la carpeta raíz del proyecto** (la que contiene `src/` y `data/`), porque el archivo por defecto se busca en `data/datos_clinicos.xlsx`.

**Aplicación con interfaz gráfica**

```bash
python src/app.py
```

**Pruebas por consola**

```bash
python src/main.py
```

Con `uv`, antepón `uv run` a cualquiera de los dos comandos.

---

## 6. Formato del archivo Excel

El archivo debe tener dos hojas con estos nombres exactos.

### Hoja `Pacientes`

| Columna | Descripción |
|---|---|
| `ID_Paciente` | Identificador único (P001 a P012 en el archivo de ejemplo) |
| `Nombre_Anonimizado` | Código de control médico |
| `Severidad_Diagnostico` | Entero de 1 (etapa temprana) a 5 (etapa crítica / metástasis) |
| `Insuficiencia_Renal` | 0 o 1 |
| `Cardiopatia` | 0 o 1 |
| `Edad_Avanzada_Fragil` | 0 o 1 |
| `Inmunosupresion` | 0 o 1 |
| `Minimizar_Costo_Financiero` | 0 o 1 (preferencia del paciente) |
| `Maximizar_Supervivencia` | 0 o 1 (preferencia del paciente) |

Cada paciente debe tener **exactamente una** preferencia activa.

### Hoja `Matriz_Tratamientos`

| Tratamiento | Fase_Origen | Fase_Destino | Costo base ($) | Efectividad base | Mult. renal | Mult. cardio | Mult. edad | Mult. inmuno |
|---|---|---|---|---|---|---|---|---|
| Cirugia_Abierta | Diagnostico | Post_Op_Mayor | 8500 | 0.85 | 1.0 | 2.5 | 3.0 | 1.5 |
| Cirugia_Laparos | Diagnostico | Post_Op_Menor | 12000 | 0.80 | 1.0 | 1.2 | 1.3 | 1.1 |
| Quimio_Estandar | Post_Op_Mayor | Consolidacion | 3000 | 0.75 | 4.0 | 1.5 | 1.5 | 2.0 |
| Quimio_Estandar | Post_Op_Menor | Consolidacion | 3000 | 0.75 | 4.0 | 1.5 | 1.5 | 2.0 |
| Inmunoterapia | Post_Op_Mayor | Consolidacion | 25000 | 0.90 | 1.1 | 1.0 | 1.1 | 1.0 |
| Inmunoterapia | Post_Op_Menor | Consolidacion | 25000 | 0.90 | 1.1 | 1.0 | 1.1 | 1.0 |
| Radioterapia | Consolidacion | Alta | 5000 | 0.60 | 1.0 | 1.0 | 1.2 | 1.1 |
| Cuidado_Paliativo | Diagnostico | Alta | 1500 | 0.20 | 1.0 | 1.0 | 1.0 | 1.0 |

La efectividad se guarda como valor entre 0 y 1. Los nombres exactos de las columnas están definidos en `lector.py`.

### Validaciones

`validar` rechaza el archivo con un mensaje claro si: hay columnas faltantes, valores nulos, columnas binarias con valores distintos de 0 o 1, severidad fuera de 1 a 5, efectividad fuera de 0 a 1, costos o multiplicadores negativos, o si ninguna arista parte de `Diagnostico` o llega a `Alta`. Si falta alguna de las dos hojas, la app lo informa indicando las hojas que sí encontró.

---

## 7. Función de costo unificada

No se pueden sumar directamente dólares con tasas de riesgo, así que cada arista recibe un costo unificado que depende del paciente:

```
C_arista = (Costo_Financiero_Base × α) + (β × ∏ Multiplicadores_Activos)
```

Los **multiplicadores activos** son solo los de los factores de riesgo que el paciente tiene (renal, cardiovascular, edad, inmunosupresión). Si no tiene ninguno, el producto vale 1.

Los pesos α y β se eligen según la preferencia del paciente:

| Preferencia | α | β | Efecto |
|---|---|---|---|
| `Minimizar_Costo_Financiero = 1` | 1.5 | 100 | Favorece las rutas económicas, salvo que el riesgo sea muy alto |
| `Maximizar_Supervivencia = 1` | 0.2 | 5000 | Penaliza fuertemente los tratamientos riesgosos |

---

## 8. Algoritmos de búsqueda

Todos parten de `Diagnostico` y buscan `Alta`. Los algoritmos están implementados de forma nativa en `busqueda.py`.

### Nivel 1: BFS (ruta de flujo clínico estándar)

Búsqueda en anchura con cola `deque`. Ignora costos y riesgos: cada arista pesa 1. Representa un protocolo institucional rígido que minimiza el número de etapas. Su propósito es mostrar el peligro de aplicar protocolos ciegos al perfil del paciente.

### Nivel 2: UCS (ruta de costo mínimo personalizado)

Búsqueda de costo uniforme con cola de prioridad mínima (`heapq`) sobre la función de costo unificada. La meta se evalúa **al extraer** el nodo de la cola, no al generarlo. Incluye un contador de desempate para ordenar elementos con igual costo.

### Nivel 3: A* (pendiente)

> **Estado: aún no implementado.**

La búsqueda A* (`f(n) = g(n) + h(n)`) usará una heurística admisible y consistente basada en la columna `Severidad_Diagnostico`. Está contemplada en el diseño del pipeline y en la interfaz (la casilla A* aparece deshabilitada), y se agregará en una entrega posterior.

### Resultado de cada búsqueda

Cada algoritmo devuelve la secuencia de estados, los tratamientos de la ruta, el costo acumulado, el costo financiero (suma de costos base), la tasa de efectividad de la ruta (producto de las efectividades de cada tratamiento) y el número de nodos expandidos. Si no existe camino entre `Diagnostico` y `Alta`, devuelve `None`, y el reporte lo marca como "Sin ruta".

---

## 9. Reporte comparativo y exportación

Por cada paciente y algoritmo se genera una fila con estas columnas:

| Columna | Descripción |
|---|---|
| `ID_Paciente` | Identificador del paciente |
| `Algoritmo` | BFS o UCS |
| `Ruta Propuesta` | Tratamientos en orden, separados por flechas |
| `Costo Económico` | Suma de los costos financieros base de la ruta ($) |
| `Nodos Expandidos` | Tamaño del espacio de búsqueda explorado |
| `Costo del Algoritmo` | Lo que cada algoritmo minimizó: **número de pasos** en BFS, **costo unificado** en UCS |
| `Efectividad (%)` | Producto de las efectividades de la ruta, en porcentaje |
| `Tiempo (ms)` | Tiempo de cómputo |

> `Costo Económico` es siempre dinero y por eso es comparable entre algoritmos. `Costo del Algoritmo` tiene unidades distintas según el algoritmo y no debe compararse entre BFS y UCS.

Con los 12 pacientes y dos algoritmos el reporte tiene 24 filas. Se puede exportar a **Excel (`.xlsx`)** o **CSV (`.csv`, con codificación UTF-8 con BOM para que Excel muestre bien las tildes)**.

---

## 10. La aplicación (interfaz gráfica)

Construida con Tkinter, como una clase `AppOncoRuta`. Tiene tres pestañas:

### Pestaña Datos

- Botón **Cargar Excel**: abre el selector de archivos, lee y valida el archivo elegido. Solo reemplaza los datos si la carga fue correcta; si falla, muestra el motivo en una ventana y conserva los datos anteriores.
- Al cargar un archivo válido se actualiza la lista de pacientes y se limpia la tabla de resultados.

### Pestaña Resultados

- Lista desplegable de pacientes (los del Excel cargado, más la opción **Todos**).
- Casillas **BFS**, **UCS** y **A\*** (esta última deshabilitada hasta que se implemente).
- Botón **Ejecutar**: calcula los reportes y los muestra en una tabla con barra de desplazamiento.
- Botón **Exportar tabla**: guarda la tabla en Excel o CSV.
- Una línea de estado informa el resultado de cada acción.

### Pestaña Grafo

Reservada para dibujar el grafo de tratamientos con la ruta elegida resaltada. **Está en desarrollo.** Mientras tanto, `src/main.py` dibuja el grafo en una ventana de matplotlib.

---

## 11. Estado del proyecto

| Componente | Estado |
|---|---|
| Lectura y validación del Excel | Hecho |
| Construcción del grafo y costos personalizados | Hecho |
| BFS (Nivel 1) | Hecho |
| UCS (Nivel 2) | Hecho |
| **A\* (Nivel 3)** | **Pendiente** |
| Reporte comparativo (tabla con pandas) | Hecho |
| Exportación a Excel y CSV | Hecho |
| Interfaz: pestañas Datos y Resultados | Hecho |
| Carga de un Excel propio desde la interfaz | Hecho |
| Interfaz: pestaña Grafo (ruta resaltada) | Pendiente |
| Análisis crítico y ético (reporte PDF) | Pendiente |

---

## 12. Limitaciones conocidas

- **UCS y BFS coinciden con la fórmula literal.** Con los datos de ejemplo, la ruta de menor costo unificado es siempre `Cuidado_Paliativo` para los 12 pacientes: es la más barata en dinero, no recibe penalización de riesgo y tiene una sola arista. La fórmula del enunciado no considera la efectividad, así que no distingue un tratamiento paliativo (20 % de efectividad) de uno curativo. Una extensión posible es agregar a la función de costo un término que penalice la baja efectividad, escalado por la severidad del paciente. Este hallazgo se discute en el análisis crítico.
- **Las fases son fijas.** El sistema busca desde `Diagnostico` hasta `Alta`, y el dibujo del grafo usa posiciones escritas a mano para las cinco fases de la matriz de ejemplo. Un Excel con otras fases se puede cargar, pero el dibujo no se adapta.
- **No se valida la conectividad.** El validador comprueba que exista una arista que parta de `Diagnostico` y otra que llegue a `Alta`, pero no que haya un camino entre ambas. En ese caso el reporte muestra "Sin ruta".
- **La ruta del Excel por defecto es relativa** a la carpeta desde la que se ejecuta el programa.

---

*Proyecto académico de la materia IABS: Búsqueda y Optimización de Soluciones. Esta herramienta es un ejercicio de clase y no está diseñada ni validada para su uso clínico real.*
