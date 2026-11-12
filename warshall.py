from typing import List


def warshall(matriz_adyacencia: List[List[int]], etiquetas: List[str]) -> List[List[int]]:
    """
    Calcula la clausura transitiva (matriz de alcanzabilidad) de un grafo dirigido
    utilizando el Algoritmo de Warshall mediante operaciones booleanas.
    """
    n = len(matriz_adyacencia)
    clausura = [fila[:] for fila in matriz_adyacencia]

    print("=== Ejecución del Algoritmo de Warshall (Clausura Transitiva) ===")
    for k in range(n):
        nuevas_conexiones = []
        for i in range(n):
            for j in range(n):
                if not clausura[i][j] and (clausura[i][k] and clausura[k][j]):
                    clausura[i][j] = 1
                    nuevas_conexiones.append(f"{etiquetas[i]}->{etiquetas[j]}")
        if nuevas_conexiones:
            print(
                f"Paso k={k} (Pivote '{etiquetas[k]}'): Nuevos caminos descubiertos: "
                f"{', '.join(nuevas_conexiones)}"
            )
        else:
            print(f"Paso k={k} (Pivote '{etiquetas[k]}'): Sin nuevas conexiones transitivas.")

    return clausura


def imprimir_matriz_booleana(matriz: List[List[int]], etiquetas: List[str], titulo: str) -> None:
    print(f"\n{titulo}")
    encabezado = "      " + " ".join(f"{et:>4}" for et in etiquetas)
    print(encabezado)
    print("    " + "-" * (len(etiquetas) * 5 + 2))
    for i, fila in enumerate(matriz):
        valores = " ".join(f"{val:>4}" for val in fila)
        print(f"{etiquetas[i]:>3} | {valores}")


if __name__ == "__main__":
    vertices = ["A", "B", "C", "D"]
    # Matriz booleana de adyacencia inicial (1 = existe arista directa, 0 = no existe)
    adyacencia_inicial = [
        [0, 1, 0, 0],
        [0, 0, 0, 1],
        [0, 0, 0, 0],
        [1, 0, 1, 0],
    ]

    imprimir_matriz_booleana(adyacencia_inicial, vertices, "Matriz de Adyacencia Inicial W(0):")
    matriz_alcanzabilidad = warshall(adyacencia_inicial, vertices)
    imprimir_matriz_booleana(
        matriz_alcanzabilidad, vertices, "Matriz de Clausura Transitiva Final W(4):"
    )