from typing import Dict, List, Tuple


class UnionFind:
    """Estructura de Conjuntos Disjuntos (Union-Find) con compresión de caminos y unión por rango."""

    def __init__(self, elementos: List[str]) -> None:
        self.padre: Dict[str, str] = {el: el for el in elementos}
        self.rango: Dict[str, int] = {el: 0 for el in elementos}

    def encontrar(self, u: str) -> str:
        if self.padre[u] != u:
            self.padre[u] = self.encontrar(self.padre[u])
        return self.padre[u]

    def unir(self, u: str, v: str) -> bool:
        raiz_u = self.encontrar(u)
        raiz_v = self.encontrar(v)
        if raiz_u == raiz_v:
            return False  # Formaría un ciclo
        if self.rango[raiz_u] < self.rango[raiz_v]:
            self.padre[raiz_u] = raiz_v
        elif self.rango[raiz_u] > self.rango[raiz_v]:
            self.padre[raiz_v] = raiz_u
        else:
            self.padre[raiz_v] = raiz_u
            self.rango[raiz_u] += 1
        return True


def kruskal(
    nodos: List[str], aristas: List[Tuple[str, str, int]]
) -> Tuple[List[Tuple[str, str, int]], int]:
    """
    Construye el Árbol de Expansión Mínima (MST) de un grafo conexo no dirigido
    mediante el Algoritmo Voraz de Kruskal.
    """
    # 1. Ordenar todas las aristas de menor a mayor peso
    aristas_ordenadas = sorted(aristas, key=lambda item: item[2])
    uf = UnionFind(nodos)
    mst: List[Tuple[str, str, int]] = []
    costo_total = 0

    print("=== Ejecución del Algoritmo de Kruskal (Árbol de Expansión Mínima) ===")
    print(f"{'Arista':<10} | {'Peso':<6} | {'Decisión'}")
    print("-" * 55)

    for u, v, peso in aristas_ordenadas:
        if uf.unir(u, v):
            mst.append((u, v, peso))
            costo_total += peso
            print(f"({u} - {v})    | {peso:<6} | ACEPTADA (se agrega al MST)")
        else:
            print(f"({u} - {v})    | {peso:<6} | RECHAZADA (formaría un ciclo)")

    return mst, costo_total


if __name__ == "__main__":
    vertices_red = ["A", "B", "C", "D", "E", "F"]
    aristas_red = [
        ("A", "B", 4),
        ("A", "C", 4),
        ("B", "C", 2),
        ("B", "D", 5),
        ("C", "D", 5),
        ("C", "E", 11),
        ("D", "E", 2),
        ("D", "F", 6),
        ("E", "F", 3),
    ]

    arbol_minimo, peso_mst = kruskal(vertices_red, aristas_red)

    print("\n=== Resumen del Árbol de Expansión Mínima (MST) ===")
    print(f"Aristas seleccionadas ({len(arbol_minimo)}): " + ", ".join(f"{u}-{v}({w})" for u, v, w in arbol_minimo))
    print(f"Costo Total del MST: {peso_mst}")