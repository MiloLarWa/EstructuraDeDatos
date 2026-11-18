"""
heapsort.py
-----------
Programa interactivo que ordena una lista de números con el algoritmo
HeapSort (J. W. J. Williams, 1964), usando un montículo máximo (max-heap).

Materia : Estructura de Datos
Práctica: Algoritmos de ordenamiento avanzados
"""

import math

NOMBRE_METODO = "HeapSort"


# ======================================================================
# 1. ALGORITMO DE ORDENAMIENTO
# ======================================================================
def heap_sort(lista, mostrar_pasos=False):
    """
    Ordena una lista de números de menor a mayor usando HeapSort.

    Idea:
      1. Se convierte la lista en un MONTÍCULO MÁXIMO: un árbol binario
         completo (guardado en el mismo arreglo) donde cada padre es mayor
         o igual que sus hijos. Así, el mayor queda en la posición 0.
         Para el nodo i: hijo izquierdo = 2i + 1, hijo derecho = 2i + 2.
      2. Se intercambia la raíz (el mayor) con el último elemento del
         montículo; ese elemento ya queda en su lugar definitivo.
      3. Se reduce el tamaño del montículo en 1 y se "hunde" la nueva raíz
         para recuperar la propiedad de montículo.
      4. Se repiten los pasos 2 y 3 hasta que el montículo tenga 1 elemento.

    Parámetros:
        lista (list): números a ordenar (NO se modifica).
        mostrar_pasos (bool): si es True, imprime cada extracción.

    Retorna:
        list: una nueva lista con los números ordenados.
    """
    datos = list(lista)          # Copia para conservar la lista original
    n = len(datos)

    # Paso 1: construir el montículo máximo. Se empieza en el último nodo
    # que tiene hijos (n//2 - 1) y se va hacia la raíz.
    for i in range(n // 2 - 1, -1, -1):
        hundir(datos, n, i)

    if mostrar_pasos:
        print(f"   Montículo máximo construido: {formatear_lista(datos)}")

    # Pasos 2-4: extraer el máximo repetidamente.
    for fin in range(n - 1, 0, -1):
        datos[0], datos[fin] = datos[fin], datos[0]   # Mayor -> al final
        hundir(datos, fin, 0)                         # Reparar el montículo
        if mostrar_pasos:
            print(f"   Extrae {formatear_numero(datos[fin]):>6} -> "
                  f"montículo {formatear_lista(datos[:fin])} | "
                  f"ordenado {formatear_lista(datos[fin:])}")

    return datos


def hundir(datos, tamano, raiz):
    """
    "Hunde" (sift-down) el elemento en la posición 'raiz' hasta que sea
    mayor o igual que sus hijos. Solo considera las primeras 'tamano'
    posiciones del arreglo (el resto ya está ordenado).
    """
    while True:
        mayor = raiz
        izquierdo = 2 * raiz + 1
        derecho = 2 * raiz + 2

        if izquierdo < tamano and datos[izquierdo] > datos[mayor]:
            mayor = izquierdo
        if derecho < tamano and datos[derecho] > datos[mayor]:
            mayor = derecho

        if mayor == raiz:        # El padre ya es mayor que sus hijos
            return

        datos[raiz], datos[mayor] = datos[mayor], datos[raiz]
        raiz = mayor             # Continuar bajando por esa rama


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
    ordenada = heap_sort(numeros, mostrar_pasos)
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
