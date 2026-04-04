"""
 --------------------------------------------------------------------------------------------------------
 main.py
 --------------------------------------------------------------------------------------------------------
 UNIVERSIDAD DEL VALLE DE GUATEMALA
 Análisis y Diseño de Algoritmos

 Descripción: Script principal del Proyecto II - Word Break Problem.

              Ejecuta demostraciones de ambos algoritmos (Divide and Conquer y Programación
              Dinámica), muestra ejemplos ilustrativos del problema, y lanza el análisis
              empírico completo con generación de gráficas comparativas. Este archivo sirve
              como punto de entrada único para reproducir todos los resultados del proyecto.

 Autores:     André Pivaral, Hansel López
 Fecha:       6 de Abril de 2026
 --------------------------------------------------------------------------------------------------------
"""

from word_break_dac import solve_dac
from word_break_dp import solve_dp
from benchmark import run_benchmark, export_csv, generate_plots
import random


# --------------------------------------------------------------------------------------------------------
# Demostración del problema con casos ilustrativos.
# Muestra el funcionamiento de ambos algoritmos sobre entradas conocidas para
# validar la correctitud antes de proceder al análisis empírico completo.
# --------------------------------------------------------------------------------------------------------
def run_demo():
    """Ejecuta ejemplos demostrativos del Word Break Problem."""

    print()
    print("=" * 120)
    print()
    print("    ██     ██  ██████  ██████  ██████      ██████  ██████  ███████  █████  ██   ██")
    print("    ██     ██ ██    ██ ██   ██ ██   ██     ██   ██ ██   ██ ██      ██   ██ ██  ██ ")
    print("    ██  █  ██ ██    ██ ██████  ██   ██     ██████  ██████  █████   ███████ █████  ")
    print("    ██ ███ ██ ██    ██ ██   ██ ██   ██     ██   ██ ██   ██ ██      ██   ██ ██  ██ ")
    print("     ███ ███   ██████  ██   ██ ██████      ██████  ██   ██ ███████ ██   ██ ██   ██")
    print()
    print("                         PROYECTO II - ANÁLISIS Y DISEÑO DE ALGORITMOS")
    print("                              André Pivaral  |  Hansel López")
    print()
    print("=" * 120)

    test_cases = [
    {
        "desc": "Caso 1: leetcode",
        "string": "leetcode",
        "dict": ["leet", "code"]
    },
    {
        "desc": "Caso 2: applepenapple",
        "string": "applepenapple",
        "dict": ["apple", "pen"]
    },
    {
        "desc": "Caso 3: catsandog (NO segmentable)",
        "string": "catsandog",
        "dict": ["cats", "dog", "sand", "and", "cat"]
    },
    {
        "desc": "Caso 4: cars",
        "string": "cars",
        "dict": ["car", "ca", "rs"]
    },
    {
        "desc": "Caso 5: aaaaaaa",
        "string": "aaaaaaa",
        "dict": ["aaaa", "aaa"]
    },
]

    print()
    print("-" * 120)
    print("  DEMOSTRACIÓN DE AMBOS ALGORITMOS")
    print("-" * 120)

    for i, tc in enumerate(test_cases, 1):
        print()
        print(f"  Caso {i}: {tc['desc']}")
        print(f"  Cadena     : \"{tc['string']}\"")
        print(f"  Diccionario: {tc['dict']}")
        print()

        # DaC
        dac_res, dac_t, dac_ops = solve_dac(tc["string"], tc["dict"])
        print(f"    [DaC] Resultado: {'Segmentable' if dac_res else 'No segmentable':<20}  "
              f"Tiempo: {dac_t:.6f} s   Operaciones: {dac_ops}")

        # DP
        dp_res, dp_t, dp_ops = solve_dp(tc["string"], tc["dict"])
        print(f"    [DP ] Resultado: {'Segmentable' if dp_res else 'No segmentable':<20}  "
              f"Tiempo: {dp_t:.6f} s   Operaciones: {dp_ops}")

        # Verificar consistencia
        if dac_res == dp_res:
            print(f"    [OK ] Ambos algoritmos coinciden.")
        else:
            print(f"    [!!] DISCREPANCIA entre algoritmos.")

        print(f"    {'─' * 80}")

    print()


# ============================================================
# EJECUCIÓN PRINCIPAL
# ============================================================
if __name__ == "__main__":

    # Fase 1: Demostración
    run_demo()

    # Fase 2: Análisis empírico
    print()
    print("=" * 120)
    print("  INICIANDO ANÁLISIS EMPÍRICO COMPLETO")
    print("=" * 120)

    random.seed(42)
    results = run_benchmark()
    export_csv(results)
    generate_plots(results)

    # Resumen final
    print()
    print("=" * 120)
    print("  RESUMEN DEL PROYECTO")
    print("=" * 120)
    print()
    print("  Problema         : Word Break Problem")
    print("  Algoritmo DaC    : Divide and Conquer puro (sin memoización)")
    print("                     Complejidad teórica: O(2^n) en el peor caso")
    print("  Algoritmo DP     : Programación Dinámica bottom-up con tabla booleana")
    print("                     Complejidad teórica: O(n^2 * m)")
    print()
    print("  Archivos generados:")
    print("    - resultados_benchmark.csv   : tabla de resultados numéricos")
    print("    - graficas_benchmark.png     : gráficas comparativas")
    print()
    print("  Conclusión: La Programación Dinámica elimina la redundancia de")
    print("  subproblemas superpuestos, logrando un rendimiento drásticamente")
    print("  superior al enfoque DaC puro, especialmente en entradas grandes.")
    print()
    print("=" * 120)
    print()
