def count_swaps(a: list[int]) -> tuple[list[int], int]:
    """
    Ordena una lista de enteros usando el método de la burbuja y retorna
    la lista ordenada junto con el total de intercambios realizados.
    """
    arr = a.copy()
    n = len(arr)
    total_swaps = 0

    for i in range(n):
        swapped = False
        for j in range(0, n - i - 1):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                total_swaps += 1
                swapped = True
        # Si no hubo intercambios en esta pasada, la lista ya está ordenada
        if not swapped:
            break

    print(f"Array is sorted in {total_swaps} swaps.")
    if arr:
        print(f"First Element: {arr[0]}")
        print(f"Last Element: {arr[-1]}")

    return arr, total_swaps


if __name__ == "__main__":
    print("--- Caso de prueba 1: [6, 4, 1] ---")
    ordenado_1, swaps_1 = count_swaps([6, 4, 1])
    print("Lista ordenada:", ordenado_1)

    print("\n--- Caso de prueba 2: [1, 2, 3] (ya ordenada) ---")
    ordenado_2, swaps_2 = count_swaps([1, 2, 3])
    print("Lista ordenada:", ordenado_2)

    print("\n--- Caso de prueba 3: [3, 2, 1] (orden inverso) ---")
    ordenado_3, swaps_3 = count_swaps([3, 2, 1])
    print("Lista ordenada:", ordenado_3)