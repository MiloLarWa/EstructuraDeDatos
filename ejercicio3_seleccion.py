def select(arr: list[int], i: int) -> int:
    """
    Encuentra y retorna el índice del elemento más pequeño en el subarreglo
    no ordenado que comienza en el índice `i`.
    """
    min_idx = i
    for j in range(i + 1, len(arr)):
        if arr[j] < arr[min_idx]:
            min_idx = j
    return min_idx


def selection_sort(arr: list[int]) -> list[int]:
    """
    Ordena una lista de enteros de menor a mayor utilizando el algoritmo
    de ordenamiento por selección.
    """
    resultado = arr.copy()
    n = len(resultado)

    for i in range(n - 1):
        min_idx = select(resultado, i)
        if min_idx != i:
            resultado[i], resultado[min_idx] = resultado[min_idx], resultado[i]

    return resultado


if __name__ == "__main__":
    ejemplo_1 = [4, 1, 3, 9, 7]
    print("Entrada:", ejemplo_1)
    print("Salida ordenada:", selection_sort(ejemplo_1))

    ejemplo_2 = [64, 25, 12, 22, 11]
    print("\nEntrada:", ejemplo_2)
    print("Salida ordenada:", selection_sort(ejemplo_2))