"""
 --------------------------------------------------------------------------------------------------------
 benchmark.py
 --------------------------------------------------------------------------------------------------------
 UNIVERSIDAD DEL VALLE DE GUATEMALA
 Análisis y Diseño de Algoritmos

 Descripción: Análisis empírico comparativo del Word Break Problem (DaC vs DP).

              Este script genera 35 entradas de prueba de tamaño creciente, ejecuta ambos
              algoritmos sobre cada entrada, registra tiempos de ejecución y conteo de
              operaciones, y produce gráficas comparativas. Las entradas incluyen casos
              segmentables y no segmentables para evaluar el comportamiento en peor caso.
              Se generan cuatro gráficas: comparación de tiempos, comparación de operaciones,
              curvas teóricas vs empíricas para DaC, y curvas teóricas vs empíricas para DP.

 Autores:     André Pivaral, Hansel López
 Fecha:       6 de Abril de 2026
 --------------------------------------------------------------------------------------------------------
"""

import time
import random
import string
import matplotlib.pyplot as plt
import matplotlib
import numpy as np
import csv
from word_break_dac import solve_dac
from word_break_dp import solve_dp

matplotlib.use("Agg")


# --------------------------------------------------------------------------------------------------------
# Generador de entradas de prueba.
# Produce cadenas y diccionarios de tamaño controlado para evaluar el rendimiento
# de ambos algoritmos bajo condiciones uniformes. Se crean tanto casos segmentables
# (concatenando palabras del diccionario) como no segmentables (cadenas aleatorias).
# --------------------------------------------------------------------------------------------------------
def generate_test_inputs():
    """
    Genera 35 entradas de prueba con tamaños crecientes.
    Incluye tres categorías:
      - Peor caso DaC: cadenas tipo "aaa...ab" con dict=["a","aa","aaa",...] que fuerzan
        exploración exponencial ya que cada prefijo es válido pero la cadena completa no.
      - Caso segmentable: cadenas construidas concatenando palabras del diccionario.
      - Caso general: mezcla de cadenas con diccionarios variados.

    Retorna:
        Lista de tuplas (nombre, cadena, diccionario, tamaño)
    """
    test_inputs = []

    # ---- Grupo 1: Peor caso para DaC (fuerza exploración exponencial) ----
    # Cadena = "aaa...ab", diccionario = {"a", "aa", "aaa", ...}
    # El DaC explora todas las combinaciones de prefijos "a" antes de fallar con "b"
    worst_sizes = [4, 6, 8, 10, 12, 14, 16, 18, 20, 22, 24, 26]
    for idx, n in enumerate(worst_sizes):
        s = "a" * (n - 1) + "b"
        word_dict = ["a" * k for k in range(1, n)]  # "a", "aa", "aaa", ...
        label = f"E{idx+1:02d}_PEOR_n{n}"
        test_inputs.append((label, s, word_dict, n))

    # ---- Grupo 2: Casos segmentables ----
    seg_cases = [
        (5,  "abcab",         ["a", "b", "c", "ab", "abc"]),
        (8,  "catsandd",      ["cat", "cats", "and", "sand", "d", "an"]),
        (10, "catsanddog",    ["cat", "cats", "and", "sand", "dog"]),
        (13, "applepenapple", ["apple", "pen"]),
        (15, "ilikecatsandog",["i", "like", "cat", "cats", "and", "dog", "an", "sand", "o"]),
        (17, "pineapplepenappl", ["pine", "apple", "pen", "pineapple", "appl", "p", "l"]),
        (20, "aaaaaaaaaaaaaaaaaaaa" + "a", ["a", "aa", "aaa", "aaaa", "aaaaa"]),
        (24, "algorithmdynamicproblem" + "s", ["algorithm", "dynamic", "problem", "s"]),
        (28, "dividesortmergeconquerbuild", ["divide", "sort", "merge", "conquer", "build", "b"]),
        (32, "abcabcabcabcabcabcabcabcabcabcab", ["abc", "ab", "a", "b", "c"]),
        (36, "aaa" * 12, ["a", "aa", "aaa"]),
    ]
    for idx2, (n, s, d) in enumerate(seg_cases):
        s = s[:n] if len(s) > n else s
        n = len(s)
        label = f"E{len(test_inputs)+1:02d}_SEG_n{n}"
        test_inputs.append((label, s, d, n))

    # ---- Grupo 3: Casos no segmentables variados ----
    noseg_cases = [
        (6,  "xyzwqj",              ["cat", "dog", "bat"]),
        (10, "abcdefghij",           ["abc", "def", "ghi"]),
        (15, "zzzzzzzzzzzzzzz",      ["a", "ab", "abc"]),
        (20, "qwertyuiopasdfghjklz", ["hello", "world", "foo", "bar"]),
        (25, "abcdeabcdeabcdeabcdeabcde", ["abcdef", "ghij", "klmno"]),
        (30, "xyzxyzxyzxyzxyzxyzxyzxyzxyzxyz", ["xy", "yz", "xyz", "xyzx"]),
        (35, "ababababababababababababababababababa", ["aba", "bab", "abab", "baba"]),
        (40, "abcdefghijabcdefghijabcdefghijabcdefghij", ["abcde", "fghij", "abcdef"]),
        (45, "hellohellohellohellohellohellohellohellohello", ["hell", "ello", "hel", "lo"]),
        (50, "aabbaabbaabbaabbaabbaabbaabbaabbaabbaabbaabbaabbaabb", ["aab", "bba", "aabb", "bbaa"]),
        (55, "x" * 55,              ["xx", "xxx", "xxxxx", "xxxxxxx"]),
        (60, "y" * 60,              ["yy", "yyy", "yyyyy", "yyyyyyy"]),
    ]
    for idx3, (n, s, d) in enumerate(noseg_cases):
        s = s[:n] if len(s) > n else s
        n = len(s)
        label = f"E{len(test_inputs)+1:02d}_NO_n{n}"
        test_inputs.append((label, s, d, n))

    return test_inputs


# --------------------------------------------------------------------------------------------------------
# Ejecución del benchmark completo sobre ambos algoritmos.
# Establece un timeout para DaC en cadenas grandes para evitar tiempos excesivos.
# --------------------------------------------------------------------------------------------------------
def run_benchmark():
    """Ejecuta ambos algoritmos sobre todas las entradas y recopila resultados."""

    print()
    print("=" * 120)
    print("                          BENCHMARK COMPARATIVO - WORD BREAK PROBLEM")
    print("                               Divide and Conquer vs Programación Dinámica")
    print("=" * 120)

    test_inputs = generate_test_inputs()

    results = []
    DAC_TIMEOUT = 8.0  # Timeout en segundos para DaC
    dac_skip = False   # Si un caso peor ya dio timeout, saltar DaC en casos similares o mayores

    print()
    print(f"  {'#':<4} {'Entrada':<20} {'n':<5} {'DaC Tiempo (s)':<18} {'DaC Ops':<14} {'DP Tiempo (s)':<18} {'DP Ops':<14} {'Resultado':<12}")
    print("-" * 120)

    for idx, (label, s, word_dict, n) in enumerate(test_inputs):

        # Ejecutar DP (siempre rápido)
        dp_result, dp_time, dp_ops = solve_dp(s, word_dict)

        # Ejecutar DaC (con protección de timeout)
        dac_result = None
        dac_time = None
        dac_ops = None

        # Saltar DaC si un caso peor anterior ya dio timeout y esta entrada es grande
        skip_this = dac_skip and n > 24

        if not skip_this:
            try:
                dac_result, dac_time, dac_ops = solve_dac(s, word_dict)

                if dac_time > DAC_TIMEOUT:
                    dac_skip = True
                    dac_time = None
                    dac_ops = None
                    dac_result = None
            except RecursionError:
                dac_result = None
                dac_time = None
                dac_ops = None

        # Formatear salida
        dac_t_str = f"{dac_time:.6f}" if dac_time is not None else "TIMEOUT"
        dac_o_str = f"{dac_ops}" if dac_ops is not None else "---"
        res_str = "Segmentable" if dp_result else "No segmentable"

        print(f"  {idx+1:<4} {label:<20} {n:<5} {dac_t_str:<18} {dac_o_str:<14} {dp_time:.6f}{'':<12} {dp_ops:<14} {res_str:<12}")

        results.append({
            "label": label,
            "n": n,
            "string": s,
            "dac_time": dac_time,
            "dac_ops": dac_ops,
            "dp_time": dp_time,
            "dp_ops": dp_ops,
            "dp_result": dp_result,
            "dac_result": dac_result,
        })

    print("-" * 120)
    print(f"  Total de entradas evaluadas: {len(results)}")
    print("=" * 120)

    return results


# --------------------------------------------------------------------------------------------------------
# Exportación de resultados a CSV para documentación y análisis externo.
# --------------------------------------------------------------------------------------------------------
def export_csv(results, filename="resultados_benchmark.csv"):
    """Exporta los resultados del benchmark a un archivo CSV."""

    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["Entrada", "n", "Cadena", "DaC Tiempo (s)", "DaC Operaciones",
                         "DP Tiempo (s)", "DP Operaciones", "Resultado"])
        for r in results:
            writer.writerow([
                r["label"], r["n"], r["string"],
                r["dac_time"] if r["dac_time"] is not None else "TIMEOUT",
                r["dac_ops"] if r["dac_ops"] is not None else "N/A",
                r["dp_time"], r["dp_ops"],
                "Segmentable" if r["dp_result"] else "No segmentable"
            ])

    print(f"\n  Resultados exportados a: {filename}")


# --------------------------------------------------------------------------------------------------------
# Generación de gráficas comparativas.
# Se producen cuatro gráficas:
#   1. Comparación de tiempos de ejecución (DaC vs DP)
#   2. Comparación de operaciones (DaC vs DP)
#   3. Tiempo empírico vs curva teórica O(2^n) para DaC
#   4. Tiempo empírico vs curva teórica O(n^2) para DP
# --------------------------------------------------------------------------------------------------------
def generate_plots(results):
    """Genera las gráficas de análisis empírico."""

    # Separar datos válidos
    ns = [r["n"] for r in results]
    dp_times = [r["dp_time"] for r in results]
    dp_ops = [r["dp_ops"] for r in results]

    dac_valid = [(r["n"], r["dac_time"], r["dac_ops"]) for r in results if r["dac_time"] is not None]
    dac_ns = [d[0] for d in dac_valid]
    dac_times = [d[1] for d in dac_valid]
    dac_ops_list = [d[2] for d in dac_valid]

    fig, axes = plt.subplots(2, 2, figsize=(16, 12))
    fig.suptitle("ANÁLISIS EMPÍRICO - WORD BREAK PROBLEM\nDivide and Conquer vs Programación Dinámica",
                 fontsize=14, fontweight="bold", y=0.98)

    # ----------------------------------------
    # GRÁFICA 1: Comparación de tiempos
    # ----------------------------------------
    ax1 = axes[0][0]
    ax1.plot(ns, dp_times, "o-", color="#2196F3", label="Programación Dinámica", markersize=4, linewidth=1.5)
    if dac_ns:
        ax1.plot(dac_ns, dac_times, "s-", color="#F44336", label="Divide and Conquer", markersize=4, linewidth=1.5)
    ax1.set_xlabel("Tamaño de entrada (n)", fontsize=10)
    ax1.set_ylabel("Tiempo de ejecución (s)", fontsize=10)
    ax1.set_title("Comparación de Tiempos de Ejecución", fontsize=11, fontweight="bold")
    ax1.legend(fontsize=9)
    ax1.grid(True, alpha=0.3)
    ax1.set_yscale("log")

    # ----------------------------------------
    # GRÁFICA 2: Comparación de operaciones
    # ----------------------------------------
    ax2 = axes[0][1]
    ax2.plot(ns, dp_ops, "o-", color="#2196F3", label="Programación Dinámica", markersize=4, linewidth=1.5)
    if dac_ns:
        ax2.plot(dac_ns, dac_ops_list, "s-", color="#F44336", label="Divide and Conquer", markersize=4, linewidth=1.5)
    ax2.set_xlabel("Tamaño de entrada (n)", fontsize=10)
    ax2.set_ylabel("Número de operaciones", fontsize=10)
    ax2.set_title("Comparación de Operaciones Realizadas", fontsize=11, fontweight="bold")
    ax2.legend(fontsize=9)
    ax2.grid(True, alpha=0.3)
    ax2.set_yscale("log")

    # ----------------------------------------
    # GRÁFICA 3: DaC empírico vs teórico O(2^n)
    # ----------------------------------------
    ax3 = axes[1][0]
    if dac_ns:
        ax3.plot(dac_ns, dac_times, "s-", color="#F44336", label="DaC Empírico", markersize=5, linewidth=1.5)

        # Curva teórica O(2^n) escalada
        n_arr = np.array(dac_ns, dtype=float)
        theoretical = 2.0 ** n_arr
        if dac_times[-1] > 0 and theoretical[-1] > 0:
            scale = dac_times[-1] / theoretical[-1]
        else:
            scale = 1e-10
        ax3.plot(dac_ns, theoretical * scale, "--", color="#FF9800", label="Teórico O(2ⁿ) escalado", linewidth=2)

    ax3.set_xlabel("Tamaño de entrada (n)", fontsize=10)
    ax3.set_ylabel("Tiempo de ejecución (s)", fontsize=10)
    ax3.set_title("DaC: Empírico vs Teórico O(2ⁿ)", fontsize=11, fontweight="bold")
    ax3.legend(fontsize=9)
    ax3.grid(True, alpha=0.3)
    ax3.set_yscale("log")

    # ----------------------------------------
    # GRÁFICA 4: DP empírico vs teórico O(n^2)
    # ----------------------------------------
    ax4 = axes[1][1]
    ax4.plot(ns, dp_times, "o-", color="#2196F3", label="DP Empírico", markersize=5, linewidth=1.5)

    # Curva teórica O(n^2) escalada
    n_arr = np.array(ns, dtype=float)
    theoretical_dp = n_arr ** 2
    if dp_times[-1] > 0 and theoretical_dp[-1] > 0:
        scale_dp = dp_times[-1] / theoretical_dp[-1]
    else:
        scale_dp = 1e-10
    ax4.plot(ns, theoretical_dp * scale_dp, "--", color="#4CAF50", label="Teórico O(n²) escalado", linewidth=2)

    ax4.set_xlabel("Tamaño de entrada (n)", fontsize=10)
    ax4.set_ylabel("Tiempo de ejecución (s)", fontsize=10)
    ax4.set_title("DP: Empírico vs Teórico O(n²)", fontsize=11, fontweight="bold")
    ax4.legend(fontsize=9)
    ax4.grid(True, alpha=0.3)

    plt.tight_layout(rect=[0, 0, 1, 0.95])
    plt.savefig("graficas_benchmark.png", dpi=200, bbox_inches="tight")
    print("\n  Gráficas guardadas en: graficas_benchmark.png")
    plt.close()


# ============================================================
# EJECUCIÓN PRINCIPAL
# ============================================================
if __name__ == "__main__":
    random.seed(42)

    results = run_benchmark()
    export_csv(results)
    generate_plots(results)

    print()
    print("=" * 72)
    print("  BENCHMARK FINALIZADO")
    print("=" * 72)
    print()
