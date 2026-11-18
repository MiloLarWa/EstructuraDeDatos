"""
radix.py
--------
Programa interactivo que ordena una lista de números ENTEROS con el
algoritmo Radix Sort LSD (dígito menos significativo primero), en base 10.

RESTRICCIÓN: Radix Sort trabaja dígito por dígito, por lo que solo acepta
números enteros. Los números negativos SÍ se manejan: se separan, se
ordenan por su valor absoluto y al final se unen en el orden correcto.

Materia : Estructura de Datos
Práctica: Algoritmos de ordenamiento avanzados
"""

import math

NOMBRE_METODO = "Radix Sort (LSD, base 10)"
BASE = 10


# ======================================================================
# 1. ALGORITMO DE ORDENAMIENTO
# ======================================================================
def radix_sort(lista, mostrar_pasos=False):
    """
    Ordena una lista de enteros (positivos, cero o negativos) de menor a
    mayor usando Radix Sort.

    Manejo de negativos:
      1. Se separan los negativos y se guardan como valor absoluto.
      2. Se ordenan ambos grupos con Radix Sort (solo no negativos).
      3. Los negativos se invierten y se les devuelve el signo
         (ej. absolutos [2, 5, 9] -> [-9, -5, -2]) y se colocan antes
         de los no negativos.

    Parámetros:
        lista (list[int]): enteros a ordenar (NO se modifica).
        mostrar_pasos (bool): si es True, imprime cada pasada por dígito.

    Retorna:
        list[int]: una nueva lista con los números ordenados.
    """
    negativos_abs = [-x for x in lista if x < 0]
    no_negativos = [x for x in lista if x >= 0]

    negativos_ordenados = radix_sort_no_negativos(
        negativos_abs, mostrar_pasos, "negativos (en valor absoluto)")
    no_negativos_ordenados = radix_sort_no_negativos(
        no_negativos, mostrar_pasos, "no negativos")

    # El negativo con MAYOR valor absoluto es el MENOR, por eso se invierte.
    return [-x for x in reversed(negativos_ordenados)] + no_negativos_ordenados


def radix_sort_no_negativos(lista, mostrar_pasos=False, etiqueta=""):
    """
    Radix Sort LSD para enteros >= 0.

    Se ordena primero por las unidades, luego por las decenas, luego por
    las centenas... hasta el dígito más significativo del número mayor.
    Cada pasada usa Counting Sort, que es ESTABLE (respeta el orden previo
    de los elementos con el mismo dígito); por eso el resultado final
    queda completamente ordenado.
    """
    datos = list(lista)
    if not datos:
        return datos

    if mostrar_pasos:
        print(f"\n   Grupo {etiqueta}: {formatear_lista(datos)}")

    maximo = max(datos)
    exp = 1                      # 1 = unidades, 10 = decenas, 100 = centenas...
    while maximo // exp > 0:
        datos = counting_sort_por_digito(datos, exp)
        if mostrar_pasos:
            print(f"     por {nombre_posicion(exp):<14} -> {formatear_lista(datos)}")
        exp *= BASE

    return datos


def counting_sort_por_digito(datos, exp):
    """
    Ordena 'datos' de forma estable según el dígito que está en la
    posición 'exp' (1, 10, 100, ...). Dígito = (numero // exp) % 10.
    """
    conteo = [0] * BASE
    salida = [0] * len(datos)

    # 1) Contar cuántos números tienen cada dígito (0-9)
    for numero in datos:
        conteo[(numero // exp) % BASE] += 1

    # 2) Acumular: conteo[d] = posición final (+1) del último número con dígito d
    for d in range(1, BASE):
        conteo[d] += conteo[d - 1]

    # 3) Colocar cada número en su lugar, recorriendo de derecha a izquierda
    #    para mantener la estabilidad.
    for numero in reversed(datos):
        digito = (numero // exp) % BASE
        conteo[digito] -= 1
        salida[conteo[digito]] = numero

    return salida


def nombre_posicion(exp):
    """Devuelve un nombre legible para la posición del dígito."""
    nombres = {1: "unidades", 10: "decenas", 100: "centenas",
               1000: "millares", 10000: "dec. de millar"}
    return nombres.get(exp, f"posición 10^{len(str(exp)) - 1}")


# ======================================================================
# 2. UTILIDADES DE FORMATO
# ======================================================================
def formatear_lista(lista):
    """Convierte una lista de números en texto legible: [3, -1, 7]."""
    return "[" + ", ".join(str(v) for v in lista) + "]"


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


def leer_entero(mensaje):
    """
    Pide un número ENTERO (puede ser negativo). Si el usuario escribe un
    decimal, se explica la restricción de Radix Sort y se vuelve a pedir.
    Un valor como 7.0 se acepta y se convierte a 7.
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
        if math.isfinite(valor) and valor.is_integer():
            return int(valor)
        print("   [!] Radix Sort solo ordena números ENTEROS "
              f"('{texto}' tiene parte decimal o no es finito).")


def capturar_datos():
    """Pide la cantidad de números y luego cada número, uno por uno."""
    cantidad = leer_entero_positivo("\n¿Cuántos números deseas ordenar? ")
    numeros = []
    for i in range(1, cantidad + 1):
        numeros.append(leer_entero(f"   Número entero {i} de {cantidad}: "))
    print(f"\n   Lista capturada: {formatear_lista(numeros)}")
    return numeros


# ======================================================================
# 4. MENÚ Y FLUJO PRINCIPAL
# ======================================================================
def mostrar_menu():
    """Imprime las opciones disponibles y la restricción del método."""
    print("\n" + "=" * 55)
    print(f"MÉTODO DE ORDENAMIENTO: {NOMBRE_METODO}".center(55))
    print("=" * 55)
    print("  Nota: solo se aceptan números ENTEROS.")
    print("        Los negativos se manejan automáticamente.")
    print("-" * 55)
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
    ordenada = radix_sort(numeros, mostrar_pasos)
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
