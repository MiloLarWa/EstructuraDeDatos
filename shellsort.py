"""
shellsort.py
------------
Programa interactivo que ordena una lista de números con el algoritmo
ShellSort (Donald Shell, 1959).

Materia : Estructura de Datos
Práctica: Algoritmos de ordenamiento avanzados
"""

import math

NOMBRE_METODO = "ShellSort"


# ======================================================================
# 1. ALGORITMO DE ORDENAMIENTO
# ======================================================================
def shell_sort(lista, mostrar_pasos=False):
    """
    Ordena una lista de números de menor a mayor usando ShellSort.

    Idea: es una mejora del ordenamiento por inserción. En lugar de comparar
    solo elementos vecinos, compara elementos separados por una distancia
    llamada "gap" (salto). El gap se reduce a la mitad en cada pasada hasta
    llegar a 1; en esa última pasada se hace una inserción normal, pero la
    lista ya está "casi ordenada", así que se necesitan muy pocos movimientos.

    Parámetros:
        lista (list): números a ordenar (NO se modifica).
        mostrar_pasos (bool): si es True, imprime la lista después de cada gap.

    Retorna:
        list: una nueva lista con los números ordenados.
    """
    datos = list(lista)          # Copia para conservar la lista original
    n = len(datos)
    gap = n // 2                 # Secuencia original de Shell: n/2, n/4, ..., 1

    while gap > 0:
        # Inserción "con saltos": se ordena por inserción cada sublista
        # formada por elementos separados 'gap' posiciones.
        for i in range(gap, n):
            temporal = datos[i]
            j = i
            # Recorrer hacia la izquierda (de gap en gap) desplazando
            # los elementos que sean mayores que 'temporal'.
            while j >= gap and datos[j - gap] > temporal:
                datos[j] = datos[j - gap]
                j -= gap
            datos[j] = temporal  # Insertar en su lugar correcto

        if mostrar_pasos:
            print(f"   gap = {gap:<4} -> {formatear_lista(datos)}")

        gap //= 2                # Reducir el salto a la mitad

    return datos


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
        # Primero se intenta como entero; si no, como decimal.
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
    ordenada = shell_sort(numeros, mostrar_pasos)
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
