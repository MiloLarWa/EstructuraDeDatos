"""Árbol binario de búsqueda de enteros con un menú de consola."""

from __future__ import annotations

from collections import deque
from collections.abc import Iterator
from dataclasses import dataclass


@dataclass
class Nodo:
    """Guarda un valor y las referencias a sus dos hijos."""

    valor: int
    izquierdo: Nodo | None = None
    derecho: Nodo | None = None


class Arbol:
    """Mantiene los valores menores a la izquierda y los mayores a la derecha."""

    def __init__(self) -> None:
        self.raiz: Nodo | None = None

    def _localizar(self, valor: int) -> tuple[Nodo | None, Nodo | None]:
        """Devuelve el nodo y su padre, o el padre donde se insertaría."""
        padre = None
        actual = self.raiz
        while actual is not None and actual.valor != valor:
            padre = actual
            if valor < actual.valor:
                actual = actual.izquierdo
            else:
                actual = actual.derecho
        return actual, padre

    def insertar(self, valor: int) -> bool:
        """Inserta el valor y devuelve False si ya existe."""
        actual, padre = self._localizar(valor)
        if actual is not None:
            return False

        nuevo = Nodo(valor)
        if padre is None:
            self.raiz = nuevo
        elif valor < padre.valor:
            padre.izquierdo = nuevo
        else:
            padre.derecho = nuevo
        return True

    def buscar(self, valor: int) -> Nodo | None:
        """Devuelve el nodo que contiene el valor, o None si no existe."""
        nodo, _ = self._localizar(valor)
        return nodo

    def eliminar(self, valor: int) -> bool:
        """Elimina el valor y devuelve False si no existe."""
        nodo, padre = self._localizar(valor)
        if nodo is None:
            return False

        # Con dos hijos, se copia el menor valor del subárbol derecho.
        # Ese sucesor no tiene hijo izquierdo y puede retirarse directamente.
        if nodo.izquierdo is not None and nodo.derecho is not None:
            padre_sucesor = nodo
            sucesor = nodo.derecho
            while sucesor.izquierdo is not None:
                padre_sucesor = sucesor
                sucesor = sucesor.izquierdo
            nodo.valor = sucesor.valor
            nodo, padre = sucesor, padre_sucesor

        hijo = nodo.izquierdo if nodo.izquierdo is not None else nodo.derecho
        if padre is None:
            self.raiz = hijo
        elif padre.izquierdo is nodo:
            padre.izquierdo = hijo
        else:
            padre.derecho = hijo
        return True

    def inorden(self) -> list[int]:
        """Devuelve los valores en orden ascendente."""
        valores = []
        pila = []
        actual = self.raiz
        while pila or actual is not None:
            while actual is not None:
                pila.append(actual)
                actual = actual.izquierdo
            actual = pila.pop()
            valores.append(actual.valor)
            actual = actual.derecho
        return valores

    def preorden(self) -> list[int]:
        """Visita la raíz, el subárbol izquierdo y el derecho, en ese orden."""
        valores = []
        pila = [self.raiz] if self.raiz is not None else []
        while pila:
            nodo = pila.pop()
            valores.append(nodo.valor)
            if nodo.derecho is not None:
                pila.append(nodo.derecho)
            if nodo.izquierdo is not None:
                pila.append(nodo.izquierdo)
        return valores

    def postorden(self) -> list[int]:
        """Visita el subárbol izquierdo, el derecho y la raíz, en ese orden."""
        valores = []
        pila = [self.raiz] if self.raiz is not None else []
        # Se recorre en orden raíz, derecha, izquierda y se invierte el resultado.
        while pila:
            nodo = pila.pop()
            valores.append(nodo.valor)
            if nodo.izquierdo is not None:
                pila.append(nodo.izquierdo)
            if nodo.derecho is not None:
                pila.append(nodo.derecho)
        valores.reverse()
        return valores

    def _recorrer_niveles(self) -> Iterator[tuple[Nodo, int]]:
        cola = deque([(self.raiz, 1)]) if self.raiz is not None else deque()
        while cola:
            nodo, nivel = cola.popleft()
            yield nodo, nivel
            if nodo.izquierdo is not None:
                cola.append((nodo.izquierdo, nivel + 1))
            if nodo.derecho is not None:
                cola.append((nodo.derecho, nivel + 1))

    def por_niveles(self) -> list[int]:
        """Visita los nodos de arriba abajo y de izquierda a derecha."""
        return [nodo.valor for nodo, _ in self._recorrer_niveles()]

    def altura(self) -> int:
        """Cuenta los niveles del árbol. El árbol vacío tiene altura 0."""
        return max((nivel for _, nivel in self._recorrer_niveles()), default=0)

    def minimo(self) -> int | None:
        """Devuelve el menor valor, o None si el árbol está vacío."""
        nodo = self.raiz
        if nodo is None:
            return None
        while nodo.izquierdo is not None:
            nodo = nodo.izquierdo
        return nodo.valor

    def maximo(self) -> int | None:
        """Devuelve el mayor valor, o None si el árbol está vacío."""
        nodo = self.raiz
        if nodo is None:
            return None
        while nodo.derecho is not None:
            nodo = nodo.derecho
        return nodo.valor


def main() -> None:
    arbol = Arbol()
    menu = """
Árbol binario de búsqueda
1. Insertar un valor
2. Buscar un valor
3. Eliminar un valor
4. Mostrar recorridos
5. Mostrar altura, mínimo y máximo
0. Salir
"""
    while True:
        print(menu)
        opcion = input("Elige una opción: ").strip()
        if opcion == "0":
            return

        if opcion in {"1", "2", "3"}:
            try:
                valor = int(input("Escribe un número entero: "))
            except ValueError:
                print("Entrada inválida. Escribe un número entero.")
                continue

            if opcion == "1":
                insertado = arbol.insertar(valor)
                print("Valor insertado." if insertado else "El valor ya existe.")
            elif opcion == "2":
                encontrado = arbol.buscar(valor) is not None
                print("Valor encontrado." if encontrado else "Valor no encontrado.")
            else:
                eliminado = arbol.eliminar(valor)
                print("Valor eliminado." if eliminado else "Valor no encontrado.")
        elif opcion == "4":
            print("Inorden:", arbol.inorden())
            print("Preorden:", arbol.preorden())
            print("Postorden:", arbol.postorden())
            print("Por niveles:", arbol.por_niveles())
        elif opcion == "5":
            print("Altura:", arbol.altura())
            if arbol.raiz is None:
                print("El árbol está vacío.")
            else:
                print("Mínimo:", arbol.minimo())
                print("Máximo:", arbol.maximo())
        else:
            print("Opción inválida. Elige un número del menú.")


if __name__ == "__main__":
    try:
        main()
    except (EOFError, KeyboardInterrupt):
        print()
