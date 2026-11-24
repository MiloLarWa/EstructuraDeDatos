"""
Ejercicio 2: Ordenamiento Externo por Mezcla Directa (Straight Merge)
Caso de uso: Ordenamiento ascendente de un archivo secuencial de folios
de pedidos desordenados utilizando dos archivos auxiliares (F1 y F2)
con particiones de longitud fija que se duplican en cada pasada (1, 2, 4, ...).
"""

from pathlib import Path
import tempfile


def leer_entero(archivo):
    """Lee la siguiente clave entera del archivo o devuelve None al llegar al final."""
    linea = archivo.readline()
    if not linea:
        return None
    linea = linea.strip()
    return int(linea) if linea else None


def particionar(ruta_f: Path, ruta_f1: Path, ruta_f2: Path, longitud: int) -> int:
    """
    Distribuye los registros de F en bloques alternos de tamaño `longitud`
    entre los archivos auxiliares F1 y F2. Devuelve el total de registros leídos.
    """
    total = 0
    escribir_en_f1 = True

    with (
        ruta_f.open("r", encoding="utf-8") as f,
        ruta_f1.open("w", encoding="utf-8") as f1,
        ruta_f2.open("w", encoding="utf-8") as f2,
    ):
        while True:
            destino = f1 if escribir_en_f1 else f2
            leidos_en_bloque = 0
            while leidos_en_bloque < longitud:
                valor = leer_entero(f)
                if valor is None:
                    return total
                destino.write(f"{valor}\n")
                leidos_en_bloque += 1
                total += 1
            escribir_en_f1 = not escribir_en_f1


def fusionar(ruta_f1: Path, ruta_f2: Path, ruta_f: Path, longitud: int) -> int:
    """
    Intercala pares de bloques ordenados de tamaño `longitud` desde F1 y F2
    y escribe el resultado combinado en F. Devuelve el número de comparaciones.
    """
    comparaciones = 0

    with (
        ruta_f1.open("r", encoding="utf-8") as f1,
        ruta_f2.open("r", encoding="utf-8") as f2,
        ruta_f.open("w", encoding="utf-8") as f,
    ):
        v1 = leer_entero(f1)
        v2 = leer_entero(f2)

        while v1 is not None or v2 is not None:
            k1 = 0
            k2 = 0

            # Intercalar un bloque de F1 con un bloque de F2
            while k1 < longitud and k2 < longitud and v1 is not None and v2 is not None:
                comparaciones += 1
                if v1 <= v2:
                    f.write(f"{v1}\n")
                    v1 = leer_entero(f1)
                    k1 += 1
                else:
                    f.write(f"{v2}\n")
                    v2 = leer_entero(f2)
                    k2 += 1

            # Vaciar el resto del bloque activo en F1
            while k1 < longitud and v1 is not None:
                f.write(f"{v1}\n")
                v1 = leer_entero(f1)
                k1 += 1

            # Vaciar el resto del bloque activo en F2
            while k2 < longitud and v2 is not None:
                f.write(f"{v2}\n")
                v2 = leer_entero(f2)
                k2 += 1

    return comparaciones


def mezcla_directa(ruta_f: Path, mostrar_traza: bool = True) -> dict:
    """Ejecuta el algoritmo completo de Mezcla Directa sobre el archivo `ruta_f`."""
    f1 = ruta_f.parent / "aux_f1.txt"
    f2 = ruta_f.parent / "aux_f2.txt"

    # Contar registros iniciales en F
    with ruta_f.open("r", encoding="utf-8") as f:
        n = sum(1 for linea in f if linea.strip())

    longitud = 1
    pasadas = 0
    total_comparaciones = 0

    while longitud < n:
        pasadas += 1
        particionar(ruta_f, f1, f2, longitud)

        if mostrar_traza:
            c_f1 = [int(x) for x in f1.read_text(encoding="utf-8").split()]
            c_f2 = [int(x) for x in f2.read_text(encoding="utf-8").split()]

        comp = fusionar(f1, f2, ruta_f, longitud)
        total_comparaciones += comp

        if mostrar_traza:
            c_f = [int(x) for x in ruta_f.read_text(encoding="utf-8").split()]
            print(f"\nPasada {pasadas} (longitud de bloque = {longitud}):")
            print(f"  F1: {c_f1}")
            print(f"  F2: {c_f2}")
            print(f"  F : {c_f}  (comparaciones: {comp})")

        longitud *= 2

    return {
        "n": n,
        "pasadas": pasadas,
        "comparaciones": total_comparaciones,
    }


def main():
    folios_desordenados = [48, 12, 75, 30, 5, 64, 19, 88, 41, 27, 93, 14]

    with tempfile.TemporaryDirectory() as tmpdir:
        ruta_f = Path(tmpdir) / "pedidos_pendientes.txt"
        ruta_f.write_text(
            "\n".join(str(x) for x in folios_desordenados) + "\n",
            encoding="utf-8",
        )

        print("=== EJERCICIO 2: MEZCLA DIRECTA ===")
        print(f"Archivo inicial F: {folios_desordenados}")

        metricas = mezcla_directa(ruta_f, mostrar_traza=True)
        resultado = [int(x) for x in ruta_f.read_text(encoding="utf-8").split()]

        print("\nResultado final ordenado:")
        print(f"  {resultado}")
        print("\nMétricas de ejecución:")
        print(f"  Registros (n): {metricas['n']}")
        print(f"  Pasadas:       {metricas['pasadas']}")
        print(f"  Comparaciones: {metricas['comparaciones']}")


if __name__ == "__main__":
    main()