import heapq
from typing import Dict, List, Tuple, Optional


def dijkstra(
    grafo: Dict[str, List[Tuple[str, int]]], origen: str
) -> Tuple[Dict[str, float], Dict[str, Optional[str]]]:
    """
    Calcula las rutas más cortas desde un nodo origen hacia todos los demás
    nodos de un grafo ponderado con pesos no negativos usando el Algoritmo de Dijkstra.
    """
    # Inicializar distancias como infinito y predecesores como None
    distancias: Dict[str, float] = {nodo: float("inf") for nodo in grafo}
    predecesores: Dict[str, Optional[str]] = {nodo: None for nodo in grafo}
    distancias[origen] = 0

    # Cola de prioridad (min-heap) que almacena tuplas (distancia_acumulada, nodo)
    cola_prioridad: List[Tuple[float, str]] = [(0, origen)]
    visitados = set()

    print(f"=== Inicio del Algoritmo de Dijkstra (Origen: {origen}) ===")
    paso = 1

    while cola_prioridad:
        distancia_actual, u = heapq.heappop(cola_prioridad)

        if u in visitados:
            continue
        visitados.add(u)
        print(f"Paso {paso}: Visitando nodo '{u}' (distancia mínima confirmada = {distancia_actual})")
        paso += 1

        # Relajación de aristas adyacentes
        for vecino, peso in grafo[u]:
            if vecino not in visitados:
                nueva_distancia = distancia_actual + peso
                if nueva_distancia < distancias[vecino]:
                    print(
                        f"   -> Relajando arista ({u} -> {vecino}, peso={peso}): "
                        f"distancia mejora de {distancias[vecino]} a {nueva_distancia}"
                    )
                    distancias[vecino] = nueva_distancia
                    predecesores[vecino] = u
                    heapq.heappush(cola_prioridad, (nueva_distancia, vecino))

    return distancias, predecesores


def reconstruir_camino(predecesores: Dict[str, Optional[str]], destino: str) -> List[str]:
    """Reconstruye el camino más corto desde el origen hasta el nodo destino."""
    camino = []
    actual: Optional[str] = destino
    while actual is not None:
        camino.append(actual)
        actual = predecesores[actual]
    return camino[::-1]


if __name__ == "__main__":
    # Grafo ponderado de ejemplo (6 nodos: A, B, C, D, E, F)
    grafo_ejemplo = {
        "A": [("B", 4), ("C", 2)],
        "B": [("A", 4), ("C", 1), ("D", 5)],
        "C": [("A", 2), ("B", 1), ("D", 8), ("E", 10)],
        "D": [("B", 5), ("C", 8), ("E", 2), ("F", 6)],
        "E": [("C", 10), ("D", 2), ("F", 3)],
        "F": [("D", 6), ("E", 3)],
    }

    nodo_origen = "A"
    dist_finales, pred_finales = dijkstra(grafo_ejemplo, nodo_origen)

    print("\n=== Resultados Finales: Caminos Más Cortos desde 'A' ===")
    print(f"{'Destino':<10} | {'Costo Mínimo':<14} | {'Ruta Óptima'}")
    print("-" * 52)
    for nodo in sorted(grafo_ejemplo.keys()):
        ruta = " -> ".join(reconstruir_camino(pred_finales, nodo))
        print(f"{nodo:<10} | {dist_finales[nodo]:<14} | {ruta}")