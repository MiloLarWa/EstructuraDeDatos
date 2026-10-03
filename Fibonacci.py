from functools import lru_cache
from itertools import islice
from math import sqrt


def fibonacci_iterativo(n: int) -> list[int]:
    """Devuelve una lista con los primeros n términos de la serie."""
    if n <= 0:
        return []
    serie = [0]
    a, b = 0, 1
    for _ in range(n - 1):
        a, b = b, a + b
        serie.append(a)
    return serie


@lru_cache(maxsize=None)
def fibonacci_recursivo(n: int) -> int:
    """Devuelve el n-ésimo término F(n) usando recursión con memoización."""
    if n < 0:
        raise ValueError("n debe ser un entero no negativo")
    if n < 2:
        return n
    return fibonacci_recursivo(n - 1) + fibonacci_recursivo(n - 2)


def fibonacci_generador():
    """Generador infinito de números de Fibonacci."""
    a, b = 0, 1
    while True:
        yield a
        a, b = b, a + b


def fibonacci_binet(n: int) -> int:
    """F(n) mediante la fórmula de Binet (aproximada para n grande)."""
    phi = (1 + sqrt(5)) / 2
    return round(phi**n / sqrt(5))


def razon_aurea(n: int) -> float:
    """Cociente F(n+1)/F(n), que converge a la razón áurea (≈1.6180339887)."""
    return fibonacci_recursivo(n + 1) / fibonacci_recursivo(n)


def pedir_entero(mensaje: str) -> int:
    """Solicita un entero positivo al usuario."""
    while True:
        try:
            valor = int(input(mensaje))
            if valor > 0:
                return valor
            print("Por favor ingresa un número mayor que 0.")
        except ValueError:
            print("Entrada no válida. Ingresa un número entero.")


def main() -> None:
    n = pedir_entero("¿Cuántos términos de la serie de Fibonacci quieres? ")

    print(f"\n1) Iterativo:   {fibonacci_iterativo(n)}")
    print(f"2) Generador:   {list(islice(fibonacci_generador(), n))}")
    print(f"3) Recursivo:   {[fibonacci_recursivo(i) for i in range(n)]}")

    if n <= 70:  # Binet pierde precisión por los decimales flotantes
        print(f"4) Binet:       {[fibonacci_binet(i) for i in range(n)]}")

    if n >= 2:
        print(f"\nF({n - 1}) = {fibonacci_recursivo(n - 1)}")
        print(f"Razón F({n})/F({n - 1}) ≈ {razon_aurea(n - 1):.10f}")


if __name__ == "__main__":
    main()