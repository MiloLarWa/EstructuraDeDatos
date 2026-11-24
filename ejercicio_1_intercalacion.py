"""
Ejercicio 1: Ordenamiento Externo por Intercalación Simple
Caso de uso: Fusión de dos archivos secuenciales ordenados de inventario
(Sucursal Norte y Sucursal Sur) en un único archivo maestro ordenado por código.
"""

from pathlib import Path
import tempfile


def leer_registro(archivo):
    """Lee una línea del archivo y la convierte en tupla (clave, linea_limpia)."""
    linea = archivo.readline()
    if not linea:
        return None
    linea = linea.strip()
    if not linea:
        return None
    clave = int(linea.split(",")[0])
    return clave, linea


def intercalacion_simple(ruta_f1: Path, ruta_f2: Path, ruta_salida: Path) -> dict:
    """
    Combina dos archivos secuenciales previamente ordenados (F1 y F2)
    en un archivo de salida ordenado (F3) leyendo un registro a la vez.
    """
    comparaciones = 0
    lecturas = 0
    escrituras = 0

    with (
        ruta_f1.open("r", encoding="utf-8") as f1,
        ruta_f2.open("r", encoding="utf-8") as f2,
        ruta_salida.open("w", encoding="utf-8") as f3,
    ):
        reg1 = leer_registro(f1)
        if reg1 is not None:
            lecturas += 1

        reg2 = leer_registro(f2)
        if reg2 is not None:
            lecturas += 1

        # Intercalación mientras ambos archivos tengan registros disponibles
        while reg1 is not None and reg2 is not None:
            comparaciones += 1
            if reg1[0] <= reg2[0]:
                f3.write(reg1[1] + "\n")
                escrituras += 1
                reg1 = leer_registro(f1)
                if reg1 is not None:
                    lecturas += 1
            else:
                f3.write(reg2[1] + "\n")
                escrituras += 1
                reg2 = leer_registro(f2)
                if reg2 is not None:
                    lecturas += 1

        # Copiar registros restantes de F1 (si existen)
        while reg1 is not None:
            f3.write(reg1[1] + "\n")
            escrituras += 1
            reg1 = leer_registro(f1)
            if reg1 is not None:
                lecturas += 1

        # Copiar registros restantes de F2 (si existen)
        while reg2 is not None:
            f3.write(reg2[1] + "\n")
            escrituras += 1
            reg2 = leer_registro(f2)
            if reg2 is not None:
                lecturas += 1

    return {
        "comparaciones": comparaciones,
        "lecturas": lecturas,
        "escrituras": escrituras,
    }


def main():
    # Dos archivos de entrada previamente ordenados por código de producto
    datos_norte = [
        "102,Teclado Mecánico,15",
        "115,Mouse Óptico,42",
        "128,Monitor 24 pulgadas,9",
        "140,Cable HDMI 2m,60",
        "165,Hub USB-C,18",
    ]
    datos_sur = [
        "105,Audífonos Diadema,25",
        "115,Mouse Óptico (Lote B),10",
        "120,Webcam HD,14",
        "150,SSD 1TB NVMe,22",
        "172,Base Enfriadora,11",
        "185,Memoria USB 64GB,50",
    ]

    with tempfile.TemporaryDirectory() as tmpdir:
        base = Path(tmpdir)
        f1 = base / "sucursal_norte.txt"
        f2 = base / "sucursal_sur.txt"
        f3 = base / "inventario_maestro.txt"

        f1.write_text("\n".join(datos_norte) + "\n", encoding="utf-8")
        f2.write_text("\n".join(datos_sur) + "\n", encoding="utf-8")

        metricas = intercalacion_simple(f1, f2, f3)
        resultado = f3.read_text(encoding="utf-8").strip().splitlines()

        print("=== EJERCICIO 1: INTERCALACIÓN SIMPLE ===")
        print(f"Registros en F1 (Norte): {len(datos_norte)}")
        print(f"Registros en F2 (Sur):   {len(datos_sur)}")
        print("\nArchivo maestro ordenado (F3):")
        for linea in resultado:
            print(f"  {linea}")

        print("\nMétricas de ejecución:")
        print(f"  Comparaciones: {metricas['comparaciones']}")
        print(f"  Lecturas:      {metricas['lecturas']}")
        print(f"  Escrituras:    {metricas['escrituras']}")


if __name__ == "__main__":
    main()