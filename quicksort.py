"""
quicksort.py
------------
Programa interactivo que ordena una lista de números con el algoritmo
QuickSort (C. A. R. Hoare, 1960), usando pivote "mediana de tres".

Materia : Estructura de Datos
Práctica: Algoritmos de ordenamiento avanzados
"""

import math

NOMBRE_METODO = "QuickSort"


# ======================================================================
# 1. ALGORITMO DE ORDENAMIENTO
# ======================================================================
def quick_sort(lista, mostrar_pasos=False):
    """
    Ordena una lista de números de menor a mayor usando QuickSort.

    Idea ("divide y vencerás"):
      1. Se elige un elemento llamado PIVOTE.
      2. Se PARTICIONA la lista: los menores o iguales al pivote quedan a su
         izquierda y los mayores a su derecha. El pivote queda en su
         posición definitiva.
      3. Se repite el proceso con la parte izquierda y la parte derecha.

    Parámetros:
        lista (list): números a ordenar (NO se modifica).
        mostrar_pasos (bool): si es True, imprime cada partición.

    Retorna:
        list: una nueva lista con los números ordenados.
    """
    datos = list(lista)          # Copia para conservar la lista original
    _quick_sort_recursivo(datos, 0, len(datos) - 1, mostrar_pasos)
    return datos


def _quick_sort_recursivo(datos, bajo, alto, mostrar_pasos):
    """
    Ordena datos[bajo..alto] en el mismo arreglo (in-place).

    Optimización: se hace la llamada recursiva sobre la parte MÁS PEQUEÑA y
    la parte grande se procesa con el ciclo 'while'. Así la profundidad de
    la recursión nunca pasa de O(log n) y se evita desbordar la pila.
    """
    while bajo < alto:
        indice_pivote = particionar(datos, bajo, alto)

        if mostrar_pasos:
            pivote = formatear_numero(datos[indice_pivote])
            print(f"   pivote {pivote:>6} queda en la posición "
                  f"{indice_pivote:<3} -> {formatear_lista(datos)}")

        if indice_pivote - bajo < alto - indice_pivote:
            _quick_sort_recursivo(datos, bajo, indice_pivote - 1, mostrar_pasos)
            bajo = indice_pivote + 1
        else:
            _quick_sort_recursivo(datos, indice_pivote + 1, alto, mostrar_pasos)
            alto = indice_pivote - 1


def elegir_pivote_mediana_de_tres(datos, bajo, alto):
    """
    Elige como pivote la mediana entre el primer, el central y el último
    elemento, y lo coloca al final del subarreglo. Esto evita el peor caso
    O(n^2) cuando la lista ya viene ordenada o invertida.
    """
    medio = (bajo + alto) // 2
    if datos[medio] < datos[bajo]:
        datos[medio], datos[bajo] = datos[bajo], datos[medio]
    if datos[alto] < datos[bajo]:
        datos[alto], datos[bajo] = datos[bajo], datos[alto]
    if datos[alto] < datos[medio]:
        datos[alto], datos[medio] = datos[medio], datos[alto]
    # Ahora datos[bajo] <= datos[medio] <= datos[alto]; la mediana es 'medio'.
    datos[medio], datos[alto] = datos[alto], datos[medio]
    return datos[alto]


def particionar(datos, bajo, alto):
    """
    Partición de Lomuto. Deja los elementos <= pivote a la izquierda y los
    mayores a la derecha. Devuelve la posición final del pivote.
    """
    pivote = elegir_pivote_mediana_de_tres(datos, bajo, alto)
    i = bajo - 1                 # Frontera de la zona "menores o iguales"
    for j in range(bajo, alto):
        if datos[j] <= pivote:
            i += 1
            datos[i], datos[j] = datos[j], datos[i]
    # Colocar el pivote justo después de la zona de menores
    datos[i + 1], datos[alto] = datos[alto], datos[i + 1]
    return i + 1


# ======================================================================
# 2. UTILIDADES DE FORMATO
# ======================================================================
def formatear_numero(valor):
    """Muestra 5.0 como '5' y deja 5.25 como '5.25'."""
    if isinstance(valor, float) and valor.is_integer():
        return str(int(valor))
    return str(valor)


def formatear_lista(lista):
    """Convierte una lista de números en texto legible: [3, 1.5, 7]."""
    return "[" + ", ".join(formatear_numero(v) for v in lista) + "]"


# ======================================================================
# 3. CAPTURA Y VALIDACIÓN DE DATOS
# ======================================================================
def leer_entero_positivo(mensaje):
    """Pide un entero mayor que cero hasta que el usuario lo escriba bien."""
    while True:
        texto = input(mensaje).strip()
        try:
            valor = int(texto)
        except ValueError:
            print("   [!] Error: escribe un número ENTERO (por ejemplo: 5).")
            continue
        if valor <= 0:
            print("   [!] Error: la cantidad debe ser mayor que cero.")
            continue
        return valor


def leer_numero(mensaje):
    """
    Pide un número (entero o decimal) y lo devuelve como int o float.
    Acepta coma o punto como separador decimal (3,5 o 3.5).
    """
    while True:
        texto = input(mensaje).strip().replace(",", ".")
        try:
            return int(texto)
        except ValueError:
            pass
        try:
            valor = float(texto)
        except ValueError:
            print(f"   [!] Error: '{texto}' no es un número válido.")
            continue
        if math.isnan(valor) or math.isinf(valor):
            print("   [!] Error: no se permiten valores 'nan' ni 'inf'.")
            continue
        return valor


def capturar_datos():
    """Pide la cantidad de números y luego cada número, uno por uno."""
    cantidad = leer_entero_positivo("\n¿Cuántos números deseas ordenar? ")
    numeros = []
    for i in range(1, cantidad + 1):
        numeros.append(leer_numero(f"   Número {i} de {cantidad}: "))
    print(f"\n   Lista capturada: {formatear_lista(numeros)}")
    return numeros


# ======================================================================
# 4. MENÚ Y FLUJO PRINCIPAL
# ======================================================================
def mostrar_menu():
    """Imprime las opciones disponibles."""
    print("\n" + "=" * 55)
    print(f"MÉTODO DE ORDENAMIENTO: {NOMBRE_METODO}".center(55))
    print("=" * 55)
    print("  1. Ingresar cantidad y números")
    print("  2. Ordenar y mostrar resultado")
    print("  3. Ordenar mostrando el paso a paso")
    print("  4. Salir")
    print("-" * 55)


def ordenar_y_mostrar(numeros, mostrar_pasos=False):
    """Ordena la lista capturada e imprime la lista original y la ordenada."""
    if not numeros:
        print("\n   [!] Primero debes capturar los números (opción 1).")
        return
    print(f"\n   Lista original : {formatear_lista(numeros)}")
    if mostrar_pasos:
        print("\n   Paso a paso:")
    ordenada = quick_sort(numeros, mostrar_pasos)
    print(f"\n   Lista ordenada : {formatear_lista(ordenada)}")


def confirmar_salida():
    """Pregunta al usuario si realmente quiere salir."""
    while True:
        respuesta = input("¿Seguro que deseas salir? (s/n): ").strip().lower()
        if respuesta in ("s", "si", "sí"):
            return True
        if respuesta in ("n", "no"):
            return False
        print("   [!] Responde 's' o 'n'.")


def main():
    """Ciclo principal: se repite hasta que el usuario elige salir."""
    numeros = []
    while True:
        mostrar_menu()
        opcion = input("Elige una opción (1-4): ").strip()

        if opcion == "1":
            numeros = capturar_datos()
        elif opcion == "2":
            ordenar_y_mostrar(numeros, mostrar_pasos=False)
        elif opcion == "3":
            ordenar_y_mostrar(numeros, mostrar_pasos=True)
        elif opcion == "4":
            if confirmar_salida():
                print("\n¡Gracias por usar el programa! Hasta luego.")
                break
        else:
            print("   [!] Opción no válida. Escribe un número del 1 al 4.")


if __name__ == "__main__":
    try:
        main()
    except (KeyboardInterrupt, EOFError):
        print("\n\nPrograma interrumpido por el usuario. ¡Hasta luego!")
