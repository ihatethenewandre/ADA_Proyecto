# Word Break Problem — Proyecto II

**Universidad del Valle de Guatemala**
Análisis y Diseño de Algoritmos — Sección 10

| | |
|---|---|
| **Autores** | André Pivaral, Hansel López |
| **Catedrático** | Gabriel Brolo |
| **Fecha** | Abril 2026 |

---

## Descripción del Problema

El **Word Break Problem** consiste en determinar si una cadena de texto `s` puede segmentarse en una secuencia de una o más palabras válidas pertenecientes a un diccionario `D`.

### Ejemplo

```
Entrada:
  s = "catsanddog"
  D = ["cat", "cats", "and", "sand", "dog"]

Salida: True
  → "cats" + "and" + "dog"
```

```
Entrada:
  s = "catsandog"
  D = ["cats", "dog", "sand", "and", "cat"]

Salida: False
  → No existe segmentación válida
```

El problema es relevante en procesamiento de lenguaje natural, segmentación de texto sin espacios y autocompletado, entre otras aplicaciones.

---

## Algoritmos Implementados

### Divide and Conquer

El algoritmo prueba cada posición de corte posible en la cadena. Para cada prefijo que pertenezca al diccionario, resuelve recursivamente el sufijo restante.

| Fase | Descripción |
|------|-------------|
| **Divide** | Separar la cadena en prefijo `s[0..i]` y sufijo `s[i+1..n]` |
| **Conquer** | Verificar si el prefijo está en el diccionario; resolver recursivamente el sufijo |
| **Combine** | Si prefijo válido **Y** sufijo segmentable → cadena segmentable |

**Complejidad:** `O(2^n)` en el peor caso (exponencial).

### Programación Dinámica (Bottom-Up)

Construye una tabla `dp[i]` que indica si el substring `s[0..i-1]` es segmentable. Se llena iterativamente de izquierda a derecha, eliminando la redundancia de subproblemas superpuestos.

| Elemento | Descripción |
|----------|-------------|
| **Tabla** | `dp[i] = True` si `s[0..i-1]` puede segmentarse |
| **Caso base** | `dp[0] = True` (cadena vacía) |
| **Transición** | `dp[i] = True` si existe `j < i` tal que `dp[j] = True` y `s[j..i] ∈ D` |

**Complejidad:** `O(n² · m)` donde `m` es la longitud máxima de palabra (polinomial).

---

## Análisis Teórico

### DaC — Relación de Recurrencia

```
T(n) = T(n-1) + T(n-2) + ... + T(1) + T(0) + Θ(n)
T(0) = Θ(1)
```

Resolviendo por **árbol de recursión** y verificando por **sustitución**: `T(n) = O(2^n)`.

### DP — Conteo de Operaciones

Ciclo externo `n` iteraciones × ciclo interno hasta `m` iteraciones × búsqueda en hash `O(m)`:

```
T(n) = O(n · m²)  ≈  O(n²) cuando m es constante
```

---

## Análisis Empírico

Se evaluaron **35 entradas de prueba** organizadas en tres grupos:

| Grupo | Cantidad | Propósito |
|-------|----------|-----------|
| Peor caso DaC | 12 | Cadenas `"aaa...ab"` que fuerzan exploración exponencial |
| Segmentables | 11 | Cadenas construidas concatenando palabras del diccionario |
| No segmentables | 12 | Cadenas sin segmentación válida posible |

### Resultados Destacados (Peor Caso DaC)

| n | DaC Operaciones | DaC Tiempo | DP Operaciones | DP Tiempo |
|---|-----------------|------------|----------------|-----------|
| 10 | 2,046 | 0.0002 s | 29 | 0.00001 s |
| 16 | 131,070 | 0.02 s | 47 | 0.00001 s |
| 20 | 2,097,150 | 0.25 s | 59 | 0.00003 s |
| 24 | 33,554,430 | 4.0 s | 71 | 0.00004 s |
| 26 | TIMEOUT | — | 77 | 0.00004 s |

Las operaciones del DaC se duplican exactamente con cada incremento de 2 en `n`, confirmando `O(2^n)`.

---

## Estructura del Repositorio

```
.
├── README.md                           # Este archivo
├── word_break_dac.py                   # Algoritmo Divide and Conquer
├── word_break_dp.py                    # Algoritmo Programación Dinámica
├── benchmark.py                        # Análisis empírico y gráficas
├── main.py                             # Script principal (demostración + benchmark)
├── PARTE_1_problema_y_algoritmos.py    # Parte 1 del video: problema y algoritmos
├── PARTE_2_analisis_teorico_y_empirico.py  # Parte 2 del video: análisis
├── resultados_benchmark.csv            # Resultados numéricos exportados
└── graficas_benchmark.png              # Gráficas comparativas generadas
```

---

## Ejecución

### Requisitos

```bash
pip install matplotlib numpy
```

### Ejecutar todo el proyecto

```bash
python main.py
```

### Ejecutar solo la demostración (Parte 1)

```bash
python PARTE_1_problema_y_algoritmos.py
```

### Ejecutar solo el análisis empírico (Parte 2)

```bash
python PARTE_2_analisis_teorico_y_empirico.py
```

### Ejecutar algoritmos individualmente

```bash
python word_break_dac.py
python word_break_dp.py
```

---

## Conclusión

La Programación Dinámica resuelve el Word Break Problem de forma drásticamente más eficiente que el enfoque Divide and Conquer puro. Mientras DaC se vuelve impracticable para cadenas de más de 25 caracteres en el peor caso, DP procesa cadenas de cientos de caracteres en microsegundos. La diferencia radica en que DP almacena los resultados de subproblemas superpuestos en una tabla, evitando el recálculo exponencial que caracteriza al DaC sin memoización.

---

## Fuentes

- Cormen, T., Leiserson, C., Rivest, R., & Stein, C. (2009). *Introduction to Algorithms* (3rd ed.). MIT Press. Capítulos 4 y 15.
- LeetCode Problem 139: Word Break. https://leetcode.com/problems/word-break/
