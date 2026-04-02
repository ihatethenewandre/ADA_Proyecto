"""
 --------------------------------------------------------------------------------------------------------
 word_break_dac.py
 --------------------------------------------------------------------------------------------------------
 UNIVERSIDAD DEL VALLE DE GUATEMALA
 Análisis y Diseño de Algoritmos

 Descripción: Solución al Word Break Problem mediante el paradigma Divide and Conquer.

              El Word Break Problem consiste en determinar si una cadena de texto puede
              segmentarse en una secuencia de palabras válidas pertenecientes a un diccionario.
              Esta implementación divide la cadena en dos partes en cada posición posible,
              verificando recursivamente si ambas partes pueden descomponerse en palabras
              válidas. La fase Divide separa la cadena en prefijo y sufijo, la fase Conquer
              resuelve recursivamente cada parte, y la fase Combine verifica si ambas partes
              son segmentables simultáneamente.

 Autores:     André Pivaral, Hansel López
 Fecha:       6 de Abril de 2026
 --------------------------------------------------------------------------------------------------------
"""

import time


# --------------------------------------------------------------------------------------------------------
# Función auxiliar para restablecer el contador de operaciones entre ejecuciones.
# Se utiliza una lista mutable como contador global para permitir modificaciones
# dentro de funciones sin necesidad de declarar variables globales explícitas.
# --------------------------------------------------------------------------------------------------------
operation_count = [0]


def reset_counter():
    """Restablece el contador de operaciones a cero."""
    operation_count[0] = 0


# --------------------------------------------------------------------------------------------------------
# Implementación principal del algoritmo Divide and Conquer para Word Break.
# Divide la cadena en todas las posiciones posibles, verifica si el prefijo
# pertenece al diccionario, y resuelve recursivamente el sufijo restante.
# Complejidad temporal: O(2^n) en el peor caso sin memoización.
# --------------------------------------------------------------------------------------------------------
def word_break_dac(s, word_dict):
    """
    Determina si la cadena 's' puede segmentarse en palabras del diccionario 'word_dict'
    utilizando Divide and Conquer puro (sin memoización).

    Parámetros:
        s         : cadena de texto a segmentar
        word_dict : conjunto de palabras válidas (diccionario)

    Retorna:
        True si la cadena puede segmentarse completamente, False en caso contrario.
    """
    operation_count[0] += 1

    # Caso base: cadena vacía es segmentable por definición
    if len(s) == 0:
        return True

    # Fase Divide: probar cada punto de corte posible
    for i in range(1, len(s) + 1):
        operation_count[0] += 1

        prefix = s[:i]
        suffix = s[i:]

        # Fase Conquer: verificar si el prefijo está en el diccionario
        if prefix in word_dict:
            operation_count[0] += 1

            # Fase Combine: si el prefijo es válido y el sufijo es segmentable, la cadena completa lo es
            if word_break_dac(suffix, word_dict):
                return True

    return False


# --------------------------------------------------------------------------------------------------------
# Función envolvente que mide el tiempo de ejecución y las operaciones realizadas.
# Proporciona una interfaz limpia para el análisis empírico del algoritmo.
# --------------------------------------------------------------------------------------------------------
def solve_dac(s, word_dict):
    """
    Ejecuta el algoritmo DaC midiendo tiempo y operaciones.

    Retorna:
        resultado   : booleano indicando si la cadena es segmentable
        tiempo      : tiempo de ejecución en segundos
        operaciones : número total de operaciones realizadas
    """
    reset_counter()

    start = time.perf_counter()
    result = word_break_dac(s, set(word_dict))
    end = time.perf_counter()

    return result, end - start, operation_count[0]


# ============================================================
# EJECUCIÓN INDEPENDIENTE
# ============================================================
if __name__ == "__main__":
    print()
    print("=" * 72)
    print("       WORD BREAK PROBLEM - DIVIDE AND CONQUER")
    print("=" * 72)

    # Ejemplo de prueba
    test_string = "catsanddog"
    dictionary = ["cat", "cats", "and", "sand", "dog"]

    print()
    print(f"  Cadena de entrada : \"{test_string}\"")
    print(f"  Diccionario       : {dictionary}")
    print("-" * 72)

    result, elapsed, ops = solve_dac(test_string, dictionary)

    print(f"  Resultado         : {'Segmentable' if result else 'No segmentable'}")
    print(f"  Tiempo            : {elapsed:.6f} s")
    print(f"  Operaciones       : {ops}")
    print("=" * 72)
    print()
