# OncoRuta

**Sistema de Soporte a Decisiones Clínicas mediante Algoritmos de Búsqueda (SSDC)**

<p>
  <img alt="Python" src="https://img.shields.io/badge/Python-3.11%2B-3776AB?logo=python&logoColor=white">
  <img alt="pandas" src="https://img.shields.io/badge/pandas-3.1-150458?logo=pandas&logoColor=white">
  <img alt="NetworkX" src="https://img.shields.io/badge/NetworkX-3.6-2C6E9B">
  <img alt="Matplotlib" src="https://img.shields.io/badge/Matplotlib-3.11-11557C">
  <img alt="OpenPyXL" src="https://img.shields.io/badge/OpenPyXL-3.1-217346">
  <img alt="Estado" src="https://img.shields.io/badge/estado-completo-success">
  <img alt="Uso" src="https://img.shields.io/badge/uso-académico-lightgrey">
</p>

OncoRuta transforma datos clínicos y financieros de un libro de Excel en un grafo de estados
ponderado y compara tres estrategias de búsqueda —BFS, UCS y A\*— para proponer la ruta de
tratamiento oncológico que mejor equilibra **costo económico**, **efectividad médica** y **riesgo
clínico** del paciente.

> Proyecto académico de la materia *IABS — Búsqueda y Optimización de Soluciones*. No está validado
> para uso clínico real.

---

## Tabla de contenido

| | | |
|---|---|---|
| [1. Características](#1-características) | [6. Modelo de costo](#6-modelo-de-costo) | [11. Estado del proyecto](#11-estado-del-proyecto) |
| [2. Cómo funciona](#2-cómo-funciona) | [7. Algoritmos de búsqueda](#7-algoritmos-de-búsqueda) | [12. Limitaciones](#12-limitaciones) |
| [3. Arquitectura](#3-arquitectura) | [8. Reporte y exportación](#8-reporte-y-exportación) | [13. Problemas comunes](#13-problemas-comunes) |
| [4. Instalación](#4-instalación) | [9. Resultados de referencia](#9-resultados-de-referencia) | [14. Licencia y uso](#14-licencia-y-uso) |
| [5. Uso](#5-uso) | [10. Interfaz gráfica](#10-interfaz-gráfica) | |

---

## 1. Características

- **Grafo personalizado por paciente.** Los pesos de cada arista se recalculan según la severidad,
  las comorbilidades y la preferencia del paciente; el grafo base es el mismo para todos.
- **Tres estrategias comparables sobre el mismo modelo.** BFS (protocolo ciego), UCS (costo mínimo)
  y A\* (búsqueda informada) con una heurística admisible y consistente.
- **Función de costo unificada.** Convierte dólares, efectividad y riesgo en una sola escala, con
  justificación matemática documentada.
- **Validación estricta de la entrada.** Estructura, tipos, rangos, integridad referencial y reglas
  de negocio antes de ejecutar cualquier búsqueda.
- **Trazabilidad completa.** Cada ejecución reporta ruta, costo económico, efectividad, nodos
  expandidos y tiempo, y se exporta a Excel o CSV.
- **Interfaz de escritorio.** Tkinter, con pestañas de datos, resultados y visualización del grafo.

---

## 2. Cómo funciona

El itinerario terapéutico se modela como un grafo dirigido acíclico: cada nodo es una fase clínica y
cada arista un tratamiento.

```
                        ┌──► Post_Op_Mayor ──┐
Diagnostico ────────────┤                    ├──► Consolidacion ──► Alta
                        └──► Post_Op_Menor ──┘

Diagnostico ─────────────────────────────────────────────────────► Alta
                          (Cuidado_Paliativo)
```

El pipeline se ejecuta en cascada y de una sola pasada:

```
Excel  ──►  [Capa 1]  ──►  [Capa 2]  ──►  [Capa 3]  ──►  [Capa 4]
            lectura        grafo          BFS           consolidación
            validación     personalizado  UCS           comparación
                           + h(n)         A*            exportación
```

---

## 3. Arquitectura

Cuatro capas con responsabilidades disjuntas. Cada capa recibe un artefacto de la anterior, lo
transforma y entrega un artefacto distinto a la siguiente, de modo que una estrategia de búsqueda o
un formato de reporte puede sustituirse sin modificar las demás.

| Capa | Responsabilidad | Módulo | Entrada | Salida |
|---|---|---|---|---|
| **1. Ingesta y validación** | Leer el archivo y verificar estructura y reglas de negocio. | `lector.py` | Excel (`.xlsx`, `.xls`) o CSV | Perfiles validados y matriz de tratamientos |
| **2. Representación del grafo** | Construir el grafo ponderado del paciente y calcular `h(n)`. | `grafo.py` | Perfiles validados y matriz | `MultiDiGraph` con pesos y heurística |
| **3. Evaluación de búsquedas** | Ejecutar las tres estrategias sobre el grafo. | `busqueda.py` | Grafo individual | Ruta, costo, efectividad, nodos, tiempo |
| **4. Métricas y presentación** | Consolidar, comparar y exportar. | `reporte.py` · `app.py` | Resultados de la capa 3 | Tabla comparativa y reporte |

### Estructura del repositorio

```
OncoRuta/
├── src/
│   ├── lector.py      Lectura, validación y acceso a los datos
│   ├── grafo.py       Grafo, costos g(n) y heurística h(n)
│   ├── busqueda.py    BFS, UCS y A* implementados de forma nativa
│   ├── reporte.py     Métricas, tabla comparativa y exportación
│   ├── app.py         Interfaz gráfica (Tkinter)
│   └── main.py        Punto de entrada
├── data/
│   ├── datos_clinicos.xlsx   Fuente por defecto (12 pacientes y matriz)
│   └── Prueba.xlsx           Archivo auxiliar de pruebas
├── reportes/                 Reportes exportados
├── pyproject.toml
├── uv.lock
└── README.md
```

| Módulo | Responsabilidad principal |
|---|---|
| `lector.py` | `cargar()` lee las hojas; `validar()` aplica las reglas; `obtener_paciente()` y `obtener_aristas()` alimentan al resto del sistema. |
| `grafo.py` | `construir_grafo()` crea el `MultiDiGraph` base; `asignar_costos()` calcula `g(n)` y `h(n)`; `dibujar_grafo()` dibuja y resalta rutas. |
| `busqueda.py` | BFS con `deque`, UCS y A\* con `heapq`. NetworkX se usa solo para construir el grafo y calcular la heurística, no para buscar. |
| `reporte.py` | Orquesta las ejecuciones, mide tiempos, construye el `DataFrame` final y lo exporta. |
| `app.py` | Interfaz con pestañas *Datos*, *Resultados* y *Grafo*. |

---

## 4. Instalación

**Requisitos**

- Python 3.11 o superior
- `pandas`, `networkx`, `matplotlib`, `openpyxl`
- Tkinter (incluido en Windows y macOS; en Linux puede requerir `python3-tk`)

**Con `uv`** (recomendado)

```bash
uv sync
```

**Con `pip`**

```bash
python -m venv .venv

# Windows
.venv\Scripts\activate
# Linux / macOS
source .venv/bin/activate

pip install pandas networkx matplotlib openpyxl
```

---

## 5. Uso

> Ejecuta siempre los comandos **desde la raíz del proyecto**, porque el archivo por defecto se busca
> en `data/datos_clinicos.xlsx`.

```bash
python src/app.py       # aplicación de escritorio
uv run python src/app.py  # equivalente con uv
```

La aplicación carga el archivo por defecto al iniciar. Para evaluar otro conjunto de pacientes, usa
*Datos → Cargar Excel*; para generar el informe completo de los 12 pacientes, elige **Todos** en el
selector y pulsa *Ejecutar*.

> No existe un modo por lotes en consola: el informe se produce desde la interfaz.

---

## 6. Modelo de costo

No es posible sumar dólares con tasas de riesgo, así que cada arista recibe un costo unificado y
adimensional que depende del paciente:

```
C_arista = (Costo_base × α) + β × w_sev × (∏ multiplicadores activos) × (−ln e)
```

donde `e` es la efectividad del tratamiento y

```
w_sev = 1 + (Severidad − 1) / 4        →  rango [1, 2]
```

| Término | Función |
|---|---|
| `∏ multiplicadores activos` | Solo los factores que el paciente presenta. Sin factores vale `1`, de modo que el término de riesgo nunca se anula. |
| `−ln e` | Convierte un objetivo multiplicativo (maximizar `∏e`, la probabilidad de éxito de la ruta) en uno aditivo, que es lo que UCS y A\* pueden optimizar. |
| `w_sev` | Hace que el mismo riesgo pese más en pacientes en etapa avanzada. |

### Parámetros α y β

| Preferencia | α | β | Comportamiento |
|---|---|---|---|
| `Maximizar_Supervivencia = 1` | 0.2 | 100 000 | Penaliza con fuerza el riesgo; un multiplicador alto vuelve la arista prohibitiva. |
| `Minimizar_Costo_Financiero = 1` | 1.5 | 80 000 | Favorece rutas económicas, salvo que el riesgo sea extremo. |
| Sin preferencia (rechazado por el validador) | 1.0 | 50 000 | Valor por defecto; no se alcanza con datos válidos. |

### Por qué no se usa la fórmula literal del enunciado

Con `C = Costo·α + β·∏multiplicadores`, toda ruta curativa cuesta al menos `3β + 16 500α` y la
paliación `β + 1 500α`. Como los multiplicadores son `≥ 1`, la desigualdad se cumple para todo
`α, β ≥ 0`: la fórmula premia el menor número de pasos y reproduce exactamente la paradoja que BFS
debía evidenciar. Además ignora la efectividad, así que no distingue una paliación (20 %) de una
ruta curativa (38–46 %).

---

## 7. Algoritmos de búsqueda

Los tres parten de `Diagnostico`, buscan `Alta` y están implementados de forma nativa en
`busqueda.py`.

| Nivel | Algoritmo | Criterio | Función de evaluación |
|---|---|---|---|
| 1 | **BFS** | Minimiza el número de etapas; ignora costo y riesgo. | Cola `deque`, peso unitario |
| 2 | **UCS** | Minimiza el costo unificado personalizado. | `heapq` ordenado por `g(n)` |
| 3 | **A\*** | Minimiza el costo con guía heurística. | `heapq` ordenado por `g(n) + h(n)` |

### Diseño de `h(n)`

Costo mínimo desde `n` hasta `Alta` en un problema **relajado**: el mismo grafo y la misma función de
costo, pero suponiendo que el paciente no tiene comorbilidades (`∏multiplicadores = 1`). La severidad
se conserva a través de `w_sev`, de modo que `h` crece con la severidad del diagnóstico. Se calcula
con un Dijkstra sobre el grafo invertido usando los pesos relajados.

- **Admisibilidad.** Todos los multiplicadores son `≥ 1`, luego cada arista relajada cuesta menos o
  igual que la real y `h(n) ≤ h*(n)`.
- **Consistencia.** `h` es una distancia exacta en el grafo relajado, por lo que cumple la
  desigualdad triangular.

### Salida de cada búsqueda

Secuencia de estados, secuencia de tratamientos, costo acumulado `g`, costo financiero base sumado,
efectividad de la ruta (producto) y nodos expandidos. Si no existe camino, retorna `None` y el
reporte lo marca como `Sin ruta`.

---

## 8. Reporte y exportación

| Columna | Descripción |
|---|---|
| `ID_Paciente` | Identificador del paciente |
| `Algoritmo` | `BFS`, `UCS` o `A*` |
| `Ruta Propuesta` | Tratamientos en orden, separados por flechas |
| `Costo Económico` | Suma de los costos base de la ruta, en USD |
| `Nodos Expandidos` | Tamaño del espacio de búsqueda explorado |
| `Costo del Algoritmo` | Lo que cada algoritmo minimizó: pasos en BFS, costo unificado en UCS y A\* |
| `Efectividad (%)` | Producto de las efectividades de la ruta |
| `Tiempo (ms)` | Tiempo de cómputo |

Exportación a `.xlsx` y `.csv` (UTF-8 con BOM para conservar las tildes en Excel).

> `Costo Económico` está siempre en dólares y es comparable entre algoritmos. `Costo del Algoritmo`
> tiene unidades distintas según la estrategia y **no debe compararse entre BFS y UCS**.

### Formato de entrada

El libro debe traer dos hojas con nombres exactos: `Pacientes` y `Matriz_Tratamientos`. Si solo
incluye `Pacientes`, la aplicación completa la matriz con la del archivo por defecto.

**Hoja `Pacientes`:** `ID_Paciente`, `Nombre_Anonimizado`, `Severidad_Diagnostico` (1–5),
`Insuficiencia_Renal`, `Cardiopatia`, `Edad_Avanzada_Fragil`, `Inmunosupresion`,
`Minimizar_Costo_Financiero`, `Maximizar_Supervivencia`.

Las columnas de factores y preferencias son binarias y cada paciente debe tener **exactamente una**
preferencia activa. El `Nombre_Anonimizado` sigue la convención *letra griega según el orden del
listado + edad* (`Eta-35` = séptimo paciente, 35 años).

**Hoja `Matriz_Tratamientos`:**

| Tratamiento | Origen | Destino | Costo (USD) | Efect. | Renal | Cardio | Edad | Inmuno |
|---|---|---|---|---|---|---|---|---|
| Cirugia_Abierta | Diagnostico | Post_Op_Mayor | 8 500 | 0.85 | 1.0 | 2.5 | 3.0 | 1.5 |
| Cirugia_Laparos | Diagnostico | Post_Op_Menor | 12 000 | 0.80 | 1.0 | 1.2 | 1.3 | 1.1 |
| Quimio_Estandar | Post_Op_Mayor | Consolidacion | 3 000 | 0.75 | 4.0 | 1.5 | 1.5 | 2.0 |
| Quimio_Estandar | Post_Op_Menor | Consolidacion | 3 000 | 0.75 | 4.0 | 1.5 | 1.5 | 2.0 |
| Inmunoterapia | Post_Op_Mayor | Consolidacion | 25 000 | 0.90 | 1.1 | 1.0 | 1.1 | 1.0 |
| Inmunoterapia | Post_Op_Menor | Consolidacion | 25 000 | 0.90 | 1.1 | 1.0 | 1.1 | 1.0 |
| Radioterapia | Consolidacion | Alta | 5 000 | 0.60 | 1.0 | 1.0 | 1.2 | 1.1 |
| Cuidado_Paliativo | Diagnostico | Alta | 1 500 | 0.20 | 1.0 | 1.0 | 1.0 | 1.0 |

### Reglas de validación

`lector.validar()` rechaza el archivo si faltan columnas, hay valores nulos, una columna binaria
toma valores distintos de `0` y `1`, la severidad sale de `[1, 5]`, la efectividad sale de `[0, 1]`,
hay costos o multiplicadores negativos, un paciente no tiene exactamente una preferencia activa, o
ninguna arista parte de `Diagnostico` / llega a `Alta`.

La validación no comprueba conectividad: un grafo sin camino se detecta durante la búsqueda y se
reporta como `Sin ruta`.

---

## 9. Resultados de referencia

Salida esperada con `data/datos_clinicos.xlsx`. BFS propone `Cuidado_Paliativo` en los 12 casos; UCS
y A\* coinciden en ruta y costo en todos.

| ID | Perfil | Ruta UCS = A\* | Costo (USD) | Efect. | Nodos BFS / UCS / A\* |
|---|---|---|---|---|---|
| P001 | S2 · sin factores · supervivencia | CA → IT → RT | 38 500 | 45.9 % | 3 / 4 / 3 |
| P002 | S4 · cardiopatía · supervivencia | CL → IT → RT | 42 000 | 43.2 % | 3 / 4 / 3 |
| P003 | S5 · renal + fragilidad · supervivencia | CL → IT → RT | 42 000 | 43.2 % | 3 / 4 / 3 |
| P004 | S5 · los cuatro factores · supervivencia | CL → IT → RT | 42 000 | 43.2 % | 3 / 3 / 3 |
| P005 | S3 · inmunosupresión · costo | CA → IT → RT | 38 500 | 45.9 % | 3 / 4 / 4 |
| P006 | S4 · renal · supervivencia | CA → IT → RT | 38 500 | 45.9 % | 3 / 4 / 3 |
| P007 | S1 · sin factores · costo | CA → QE → RT | 16 500 | 38.2 % | 3 / 4 / 3 |
| P008 | S4 · cardio + fragilidad · supervivencia | CL → IT → RT | 42 000 | 43.2 % | 3 / 3 / 3 |
| P009 | S3 · renal + inmunosupresión · costo | CA → IT → RT | 38 500 | 45.9 % | 3 / 4 / 4 |
| P010 | S2 · cardiopatía · supervivencia | CL → IT → RT | 42 000 | 43.2 % | 3 / 4 / 3 |
| P011 | S1 · sin factores · costo | CA → QE → RT | 16 500 | 38.2 % | 3 / 4 / 3 |
| P012 | S5 · los cuatro factores · supervivencia | CL → IT → RT | 42 000 | 43.2 % | 3 / 3 / 3 |
| **Total** | | | | | **36 / 45 / 38** |

**CA** Cirugía abierta · **CL** Cirugía laparoscópica · **QE** Quimioterapia estándar ·
**IT** Inmunoterapia · **RT** Radioterapia · **S** severidad.

A\* reduce los nodos expandidos un 16 % frente a UCS sin perder optimalidad, pero es más lento en
tiempo absoluto porque recalcula `h(n)` en cada llamada. En un grafo de 5 nodos el costo de construir
la heurística supera el ahorro de podar un nodo: la ventaja de A\* es asintótica y se manifestaría en
grafos con más fases o mayor ramificación.

---

## 10. Interfaz gráfica

Aplicación de escritorio en Tkinter (`AppOncoRuta`).

| Pestaña | Contenido |
|---|---|
| **Datos** | Carga y validación de `.xlsx`, `.xls` y `.csv`; lista de pacientes; conserva los datos anteriores si la carga falla. |
| **Resultados** | Selector de paciente (incluye *Todos*), casillas BFS / UCS / A\*, tabla desplazable y exportación a Excel. |
| **Grafo** | Grafo general o, por paciente, tres paneles con la ruta de cada algoritmo resaltada y `h(n)` en cada nodo. |

---

## 11. Estado del proyecto

| Componente | Estado |
|---|---|
| Lectura y validación del archivo | ✅ Completo |
| Construcción del grafo y costos personalizados | ✅ Completo |
| BFS (Nivel 1) | ✅ Completo |
| UCS (Nivel 2) | ✅ Completo |
| A\* y heurística (Nivel 3) | ✅ Completo |
| Reporte comparativo y exportación | ✅ Completo |
| Interfaz: Datos y Resultados | ✅ Completo |
| Interfaz: Grafo con rutas resaltadas | ✅ Completo |
| Análisis crítico y ético | ✅ Completo |

---

## 12. Limitaciones

- **Dependencia de β.** Cambiar los pesos altera la recomendación de forma radical: con β bajo el
  sistema colapsa a `Cuidado_Paliativo` incluso en pacientes con intención curativa. Es una decisión
  de política clínica, no un detalle técnico.
- **La heurística se recalcula en cada llamada.** `asignar_costos()` ya deja `h(n)` en cada nodo, pero
  `a_estrella()` vuelve a ejecutar el Dijkstra. Reutilizar el valor precalculado eliminaría el
  sobrecosto.
- **Efectividad `0`.** `calcular_Gn()` sustituye `e = 0` por `inf`, lo que produce `−ln(inf) = −inf`
  y un costo de `−∞` en lugar de `+∞`. No ocurre con los datos actuales.
- **`a_estrella()` requiere un grafo ya costeado.** Sobre el grafo base falla porque las aristas no
  tienen el atributo `costo_h`.
- **Posiciones fijas en el dibujo.** Un archivo con fases distintas se procesa, pero el dibujo usa un
  layout automático.
- **Sin validación de conectividad** al cargar: se detecta en la búsqueda.
- **Ruta del archivo por defecto relativa** a la carpeta desde la que se ejecuta el programa.

---

## 13. Problemas comunes

| Síntoma | Causa y solución |
|---|---|
| `ModuleNotFoundError: No module named 'tkinter'` | Falta Tkinter. En Linux: `sudo apt install python3-tk`. |
| `FileNotFoundError: data/datos_clinicos.xlsx` | Se ejecutó desde otra carpeta. Ejecuta desde la raíz del proyecto. |
| `PermissionError` al exportar | El archivo de destino está abierto en Excel. Ciérralo e intenta de nuevo. |
| La ventana del grafo no aparece | Bloque de backend de Matplotlib; en entornos sin pantalla usa un backend no interactivo (`Agg`). |
| `KeyError: 'costo_h'` al llamar A\* directamente | La búsqueda necesita un grafo ya costeado: llama antes a `asignar_costos()`. |

---

## 14. Licencia y uso

Proyecto académico desarrollado para la asignatura *IABS — Búsqueda y Optimización de Soluciones*.
Los multiplicadores de riesgo y los pesos α y β son valores de diseño no validados clínicamente.

El sistema **no sustituye** el juicio del personal médico: propone rutas para que un profesional las
evalúe, contraste y decida.

---

<div align="center">

**Juan David Rojas Heredia** · **Andres Steeven Oyuela Mendez**

</div>
