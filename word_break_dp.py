"""
 --------------------------------------------------------------------------------------------------------
 word_break_dp.py
 --------------------------------------------------------------------------------------------------------
 UNIVERSIDAD DEL VALLE DE GUATEMALA
 Análisis y Diseño de Algoritmos

 Descripción: Solución al Word Break Problem mediante Programación Dinámica (bottom-up).

              Se construye una tabla booleana dp[] de tamaño n+1 donde dp[i] indica si el
              substring s[0..i-1] puede segmentarse en palabras del diccionario. La tabla
              se llena iterativamente: para cada posición i, se revisan todos los puntos
              de corte j anteriores tales que dp[j] sea True y s[j..i] pertenezca al
              diccionario. Esto elimina la redundancia de subproblemas superpuestos que
              presenta la solución DaC pura, reduciendo la complejidad a O(n^2 * m)
              donde m es la longitud máxima de palabra en el diccionario.

 Autores:     André Pivaral, Hansel López
 Fecha:       6 de Abril de 2026
 --------------------------------------------------------------------------------------------------------
"""

import time


# --------------------------------------------------------------------------------------------------------
# Contador mutable de operaciones para el análisis empírico.
# --------------------------------------------------------------------------------------------------------
operation_count = [0]


def reset_counter():
    """Restablece el contador de operaciones a cero."""
    operation_count[0] = 0


# --------------------------------------------------------------------------------------------------------
# Implementación bottom-up del algoritmo de Programación Dinámica para Word Break.
# Construye la tabla dp[] de izquierda a derecha, almacenando resultados parciales
# para evitar recalcular subproblemas. Optimización adicional: se limita la búsqueda
# hacia atrás al tamaño máximo de palabra en el diccionario.
# Complejidad temporal: O(n^2 * m) donde n = |s| y m = longitud máxima de palabra.
# --------------------------------------------------------------------------------------------------------
def word_break_dp(s, word_dict):
    """
    Determina si la cadena 's' puede segmentarse en palabras del diccionario 'word_dict'
    utilizando Programación Dinámica bottom-up.

    Parámetros:
        s         : cadena de texto a segmentar
        word_dict : conjunto de palabras válidas (diccionario)

    Retorna:
        True si la cadena puede segmentarse completamente, False en caso contrario.
    """
    n = len(s)
    word_set = set(word_dict)
    max_word_len = max(len(w) for w in word_set) if word_set else 0

    operation_count[0] += 1

    # dp[i] = True si s[0..i-1] es segmentable
    dp = [False] * (n + 1)
    dp[0] = True  # Caso base: cadena vacía

    for i in range(1, n + 1):
        operation_count[0] += 1

        # Solo revisar hacia atrás hasta la longitud máxima de palabra
        for j in range(max(0, i - max_word_len), i):
            operation_count[0] += 1

            # Si dp[j] es True y el substring s[j..i] está en el diccionario
            if dp[j] and s[j:i] in word_set:
                dp[i] = True
                break  # No es necesario seguir buscando para esta posición

    return dp[n]


# --------------------------------------------------------------------------------------------------------
# Función envolvente que mide el tiempo de ejecución y las operaciones realizadas.
# --------------------------------------------------------------------------------------------------------
def solve_dp(s, word_dict):
    """
    Ejecuta el algoritmo DP midiendo tiempo y operaciones.

    Retorna:
        resultado   : booleano indicando si la cadena es segmentable
        tiempo      : tiempo de ejecución en segundos
        operaciones : número total de operaciones realizadas
    """
    reset_counter()

    start = time.perf_counter()
    result = word_break_dp(s, word_dict)
    end = time.perf_counter()

    return result, end - start, operation_count[0]


# ============================================================
# EJECUCIÓN INDEPENDIENTE
# ============================================================
if __name__ == "__main__":
    print()
    print("=" * 72)
    print("     WORD BREAK PROBLEM - PROGRAMACIÓN DINÁMICA (BOTTOM-UP)")
    print("=" * 72)

    # Ejemplo de prueba
    test_string = "catsanddog"
    dictionary = ["cat", "cats", "and", "sand", "dog"]

    print()
    print(f"  Cadena de entrada : \"{test_string}\"")
    print(f"  Diccionario       : {dictionary}")
    print("-" * 72)

    result, elapsed, ops = solve_dp(test_string, dictionary)

    print(f"  Resultado         : {'Segmentable' if result else 'No segmentable'}")
    print(f"  Tiempo            : {elapsed:.6f} s")
    print(f"  Operaciones       : {ops}")
    print("=" * 72)
    print()
