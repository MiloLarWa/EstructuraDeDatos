def ordenamiento_insercion_longitud(lista: list[str]) -> list[str]:
    """
    Ordena una lista de cadenas de texto de menor a mayor longitud
    utilizando el algoritmo de ordenamiento por inserción.
    """
    arr = lista.copy()

    for i in range(1, len(arr)):
        actual = arr[i]
        j = i - 1

        # Desplazar hacia la derecha las palabras más largas que `actual`
        while j >= 0 and len(arr[j]) > len(actual):
            arr[j + 1] = arr[j]
            j -= 1

        arr[j + 1] = actual

    return arr


if __name__ == "__main__":
    frutas = ["manzana", "uva", "melocotón", "sandía", "melón"]
    print("Lista original:", frutas)
    frutas_ordenadas = ordenamiento_insercion_longitud(frutas)
    print("Ordenada por longitud:", frutas_ordenadas)

    # Caso adicional con lenguajes de programación
    lenguajes = ["Python", "C", "JavaScript", "Go", "Java", "Rust"]
    print("\nLista original:", lenguajes)
    print("Ordenada por longitud:", ordenamiento_insercion_longitud(lenguajes))