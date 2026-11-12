from typing import List, Optional, Tuple

INF = float("inf")


def floyd(
    matriz_pesos: List[List[float]], etiquetas: List[str]
) -> Tuple[List[List[float]], List[List[Optional[int]]]]:
    """
    Calcula las distancias más cortas entre todos los pares de vértices
    utilizando el Algoritmo de Floyd (Programación Dinámica).
    """
    n = len(matriz_pesos)
    # Copia profunda de la matriz de distancias iniciales
    dist = [fila[:] for fila in matriz_pesos]
    # Matriz de siguiente nodo para reconstruir caminos óptimos
    siguiente: List[List[Optional[int]]] = [[None] * n for _ in range(n)]

    for i in range(n):
        for j in range(n):
            if i != j and dist[i][j] != INF:
                siguiente[i][j] = j

    print("=== Ejecución del Algoritmo de Floyd (Todos los Pares) ===")
    for k in range(n):
        cambios = 0
        for i in range(n):
            for j in range(n):
                if dist[i][k] != INF and dist[k][j] != INF:
                    nueva_dist = dist[i][k] + dist[k][j]
                    if nueva_dist < dist[i][j]:
                        print(
                            f"Iteración k={k} (Intermedio '{etiquetas[k]}'): "
                            f"Ruta {etiquetas[i]} -> {etiquetas[j]} mejora de "
                            f"{dist[i][j]} a {nueva_dist} pasando por {etiquetas[k]}"
                        )
                        dist[i][j] = nueva_dist
                        siguiente[i][j] = siguiente[i][k]
                        cambios += 1
        if cambios == 0:
            print(f"Iteración k={k} (Intermedio '{etiquetas[k]}'): Sin mejoras en la matriz.")

    return dist, siguiente


def imprimir_matriz(matriz: List[List[float]], etiquetas: List[str], titulo: str) -> None:
    print(f"\n{titulo}")
    encabezado = "      " + " ".join(f"{et:>6}" for et in etiquetas)
    print(encabezado)
    print("    " + "-" * (len(etiquetas) * 7 + 2))
    for i, fila in enumerate(matriz):
        valores = " ".join(f"{'INF':>6}" if v == INF else f"{int(v):>6}" for v in fila)
        print(f"{etiquetas[i]:>3} | {valores}")


if __name__ == "__main__":
    nodos = ["1", "2", "3", "4"]
    # Matriz de adyacencia ponderada (0 en la diagonal, INF donde no hay arista directa)
    grafo_matriz = [
        [0, 3, INF, 7],
        [8, 0, 2, INF],
        [5, INF, 0, 1],
        [2, INF, INF, 0],
    ]

    imprimir_matriz(grafo_matriz, nodos, "Matriz de Distancias Inicial D(0):")
    distancias_minimas, matriz_rutas = floyd(grafo_matriz, nodos)
    imprimir_matriz(distancias_minimas, nodos, "Matriz Final de Distancias Mínimas D(4):")