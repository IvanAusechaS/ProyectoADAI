import time
import matplotlib.pyplot as plt

from lector_txt import leer_archivo_txt
from lector_txt2 import leer_archivo_txt_estrategia_2
from estrategia1 import generar_salida_txt
from estrategia2 import generar_salida_txt_estrategia2



def medir_tiempo(funcion):
    inicio = time.perf_counter()
    funcion()
    fin = time.perf_counter()
    return fin - inicio


def contar_encuestados(ruta_txt):
    with open(ruta_txt, 'r', encoding='utf-8') as f:
        return sum(1 for line in f if line.strip() and "," in line and not line.startswith("Pregunta"))


def comparar_estrategias():
    archivos = [
        "pruebasMonitor/Test1.txt",
        "pruebasMonitor/Test2.txt",
        "pruebasMonitor/Test3.txt"
    ]

    tamanos = []
    tiempos_estrategia_1 = []
    tiempos_estrategia_2 = []

    for archivo in archivos:
        print(f"📂 Procesando: {archivo}")
        tamanos.append(contar_encuestados(archivo))

        encuesta1 = leer_archivo_txt(archivo)
        generar_salida_txt(encuesta1, archivo.replace(".txt", "_salida_e1.txt"))

        encuesta2 = leer_archivo_txt_estrategia_2(archivo)
        generar_salida_txt_estrategia2(encuesta2, archivo.replace(".txt", "_salida_e2.txt"))

        t1 = medir_tiempo(lambda: leer_archivo_txt(archivo))
        t2 = medir_tiempo(lambda: leer_archivo_txt_estrategia_2(archivo))

        tiempos_estrategia_1.append(t1)
        tiempos_estrategia_2.append(t2)

        print(f"    🟦 Estrategia 1: {t1:.4f} s")
        print(f"    🟥 Estrategia 2: {t2:.4f} s")

    # Gráfica
    plt.figure(figsize=(10, 6))
    plt.plot(tamanos, tiempos_estrategia_1, marker='o', label='Estrategia 1 (listas)')
    plt.plot(tamanos, tiempos_estrategia_2, marker='s', label='Estrategia 2 (heap + ABB)')
    plt.xlabel("Cantidad de encuestados")
    plt.ylabel("Tiempo de ejecución (segundos)")
    plt.title("Comparación de rendimiento entre estrategias")
    plt.legend()
    plt.grid(True)
    plt.savefig("comparacion_estrategias.png")
    plt.show()



if __name__ == "__main__":
    comparar_estrategias()
