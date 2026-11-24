"""
Ejercicio 3: Ordenamiento Externo por Mezcla Equilibrada (Mezcla Natural)
Caso de uso: Ordenamiento de una bitácora de lecturas de sensores con tramos
parcialmente ordenados, utilizando cuatro archivos (dos de entrada y dos de
salida que alternan roles) y aprovechando secuencias ordenadas naturales.
"""

from pathlib import Path
import tempfile


def leer_entero(archivo):
    """Lee el siguiente entero del archivo o devuelve None al llegar al final."""
    linea = archivo.readline()
    if not linea:
        return None
    linea = linea.strip()
    return int(linea) if linea else None


def leer_tramos_naturales(ruta: Path):
    """Generador que extrae tramos (runs) ordenados de máxima longitud de un archivo."""
    with ruta.open("r", encoding="utf-8") as f:
        actual = leer_entero(f)
        if actual is None:
            return
        tramo = [actual]
        siguiente = leer_entero(f)
        while siguiente is not None:
            if siguiente >= actual:
                tramo.append(siguiente)
            else:
                yield tramo
                tramo = [siguiente]
            actual = siguiente
            siguiente = leer_entero(f)
        yield tramo


def distribucion_inicial(ruta_origen: Path, ruta_f1: Path, ruta_f2: Path) -> int:
    """
    Detecta tramos ordenados naturales en `ruta_origen` y los distribuye
    alternadamente entre F1 y F2. Devuelve el número de tramos detectados.
    """
    tramos = 0
    escribir_en_f1 = True

    with (
        ruta_f1.open("w", encoding="utf-8") as f1,
        ruta_f2.open("w", encoding="utf-8") as f2,
    ):
        for tramo in leer_tramos_naturales(ruta_origen):
            destino = f1 if escribir_en_f1 else f2
            for valor in tramo:
                destino.write(f"{valor}\n")
            tramos += 1
            escribir_en_f1 = not escribir_en_f1

    return tramos


def fusion_equilibrada_pasada(
    in1: Path, in2: Path, out1: Path, out2: Path
) -> tuple[int, int]:
    """
    Ejecuta una pasada de fusión equilibrada:
    toma un tramo natural de `in1` y uno de `in2`, los intercala en orden
    y escribe el resultado alternadamente en `out1` y `out2`.
    Devuelve (comparaciones, registros_en_out2).
    """
    comparaciones = 0
    registros_out2 = 0
    escribir_en_out1 = True

    gen1 = leer_tramos_naturales(in1)
    gen2 = leer_tramos_naturales(in2)

    t1 = next(gen1, None)
    t2 = next(gen2, None)

    with (
        out1.open("w", encoding="utf-8") as f_out1,
        out2.open("w", encoding="utf-8") as f_out2,
    ):
        while t1 is not None or t2 is not None:
            destino = f_out1 if escribir_en_out1 else f_out2
            es_out2 = not escribir_en_out1

            if t1 is not None and t2 is not None:
                i = j = 0
                while i < len(t1) and j < len(t2):
                    comparaciones += 1
                    if t1[i] <= t2[j]:
                        destino.write(f"{t1[i]}\n")
                        i += 1
                    else:
                        destino.write(f"{t2[j]}\n")
                        j += 1
                    if es_out2:
                        registros_out2 += 1

                while i < len(t1):
                    destino.write(f"{t1[i]}\n")
                    i += 1
                    if es_out2:
                        registros_out2 += 1

                while j < len(t2):
                    destino.write(f"{t2[j]}\n")
                    j += 1
                    if es_out2:
                        registros_out2 += 1

                t1 = next(gen1, None)
                t2 = next(gen2, None)
            elif t1 is not None:
                for valor in t1:
                    destino.write(f"{valor}\n")
                    if es_out2:
                        registros_out2 += 1
                t1 = next(gen1, None)
            else:
                for valor in t2:
                    destino.write(f"{valor}\n")
                    if es_out2:
                        registros_out2 += 1
                t2 = next(gen2, None)

            escribir_en_out1 = not escribir_en_out1

    return comparaciones, registros_out2


def mezcla_equilibrada(ruta_origen: Path, mostrar_traza: bool = True) -> dict:
    """
    Ordena `ruta_origen` mediante Mezcla Equilibrada (Mezcla Natural)
    usando 4 archivos (F1, F2, F3, F4) que alternan roles de entrada y salida.
    """
    base = ruta_origen.parent
    f1 = base / "eq_f1.txt"
    f2 = base / "eq_f2.txt"
    f3 = base / "eq_f3.txt"
    f4 = base / "eq_f4.txt"

    tramos_iniciales = distribucion_inicial(ruta_origen, f1, f2)
    if mostrar_traza:
        c1 = [int(x) for x in f1.read_text(encoding="utf-8").split()]
        c2 = [int(x) for x in f2.read_text(encoding="utf-8").split()]
        print(f"\nDistribución inicial ({tramos_iniciales} tramos naturales):")
        print(f"  F1: {c1}")
        print(f"  F2: {c2}")

    # Si F2 ya quedó vacío, el archivo original ya estaba ordenado
    if not f2.read_text(encoding="utf-8").strip():
        return {
            "tramos_iniciales": tramos_iniciales,
            "pasadas": 0,
            "comparaciones": 0,
        }

    entrada = (f1, f2)
    salida = (f3, f4)
    pasadas = 0
    total_comparaciones = 0

    while True:
        pasadas += 1
        comp, reg_out2 = fusion_equilibrada_pasada(
            entrada[0], entrada[1], salida[0], salida[1]
        )
        total_comparaciones += comp

        if mostrar_traza:
            c_out1 = [int(x) for x in salida[0].read_text(encoding="utf-8").split()]
            c_out2 = [int(x) for x in salida[1].read_text(encoding="utf-8").split()]
            print(
                f"\nPasada {pasadas} ({entrada[0].name}, {entrada[1].name} -> "
                f"{salida[0].name}, {salida[1].name}):"
            )
            print(f"  {salida[0].name}: {c_out1}")
            print(f"  {salida[1].name}: {c_out2}  (comparaciones: {comp})")

        # Condición de paro: el segundo archivo de salida quedó vacío
        if reg_out2 == 0:
            ruta_origen.write_text(
                salida[0].read_text(encoding="utf-8"), encoding="utf-8"
            )
            break

        # Intercambiar roles de entrada y salida
        entrada, salida = salida, entrada

    return {
        "tramos_iniciales": tramos_iniciales,
        "pasadas": pasadas,
        "comparaciones": total_comparaciones,
    }


def main():
    # Bitácora de timestamps con secuencias naturales preexistentes:
    # [104, 118, 135], [101, 122, 149, 160], [108, 129], [112, 140, 155]
    lecturas_sensores = [104, 118, 135, 101, 122, 149, 160, 108, 129, 112, 140, 155]

    with tempfile.TemporaryDirectory() as tmpdir:
        ruta_f = Path(tmpdir) / "bitacora_sensores.txt"
        ruta_f.write_text(
            "\n".join(str(x) for x in lecturas_sensores) + "\n",
            encoding="utf-8",
        )

        print("=== EJERCICIO 3: MEZCLA EQUILIBRADA (NATURAL) ===")
        print(f"Archivo inicial: {lecturas_sensores}")

        metricas = mezcla_equilibrada(ruta_f, mostrar_traza=True)
        resultado = [int(x) for x in ruta_f.read_text(encoding="utf-8").split()]

        print("\nResultado final ordenado:")
        print(f"  {resultado}")
        print("\nMétricas de ejecución:")
        print(f"  Tramos naturales iniciales: {metricas['tramos_iniciales']}")
        print(f"  Pasadas de fusión:          {metricas['pasadas']}")
        print(f"  Comparaciones:              {metricas['comparaciones']}")


if __name__ == "__main__":
    main()