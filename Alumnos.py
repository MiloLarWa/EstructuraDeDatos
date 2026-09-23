import csv
import random
import time

def generar_forma_1(num_alumnos, num_materias):
    """
    Forma 1: Filas = Alumnos, Columnas = Materias.
    Estructura: matriz[alumno][materia]
    """
    return [[random.randint(1, 10) for _ in range(num_materias)] for _ in range(num_alumnos)]

def generar_forma_2(num_alumnos, num_materias):
    """
    Forma 2: Filas = Materias, Columnas = Alumnos.
    Estructura: matriz[materia][alumno]
    """
    return [[random.randint(1, 10) for _ in range(num_alumnos)] for _ in range(num_materias)]

def exportar_a_csv(matriz, num_alumnos, lista_materias, nombre_archivo="calificaciones.csv"):
    with open(nombre_archivo, mode="w", newline="", encoding="utf-8") as archivo:
        escritor = csv.writer(archivo)
        # Encabezado con nombres reales de las materias
        encabezado = ["Alumno"] + lista_materias
        escritor.writerow(encabezado)
        for a in range(num_alumnos):
            fila = [f"Alumno {a + 1}"] + matriz[a]
            escritor.writerow(fila)
    print(f"[Archivo Generado] Se guardó la tabla completa en '{nombre_archivo}'.")

def pedir_entero(mensaje, minimo, maximo):
    """Solicita un valor entero asegurando que se encuentre dentro del rango válido."""
    while True:
        try:
            valor = int(input(mensaje))
            if minimo <= valor <= maximo:
                return valor
            print(f"Error: Ingrese un valor entre {minimo} y {maximo}.")
        except ValueError:
            print("Error: Por favor, ingrese un número entero válido.")

def main():
    num_alumnos = 500
    
    # 1. Lista de materias definidas correctamente dentro de main()
    materias = [
        "Cálculo",
        "Álgebra Lineal",
        "Programación",
        "Estructuras de Datos",
        "Química",
        "Física"
    ]
    num_materias = len(materias)
    
    print("==================================================")
    print(f"SISTEMA DE GESTIÓN: {num_alumnos} ALUMNOS Y {num_materias} MATERIAS")
    print("==================================================")
    
    # Creación y medición de tiempos
    inicio = time.perf_counter()
    matriz_forma1 = generar_forma_1(num_alumnos, num_materias)
    tiempo_creacion_1 = time.perf_counter() - inicio
    
    inicio = time.perf_counter()
    matriz_forma2 = generar_forma_2(num_alumnos, num_materias)
    tiempo_creacion_2 = time.perf_counter() - inicio
    
    print(f"[Creación] Forma 1 (Alumno x Materia): {tiempo_creacion_1:.6f} s")
    print(f"[Creación] Forma 2 (Materia x Alumno): {tiempo_creacion_2:.6f} s")
    
    # Exportación a CSV con los nombres de las materias
    exportar_a_csv(matriz_forma1, num_alumnos, materias)
    
    # Mostrar el catálogo de materias disponibles
    print("\n--- CATÁLOGO DE MATERIAS ---")
    for i, nombre in enumerate(materias, start=1):
        print(f"{i}. {nombre}")
    
    # Búsqueda interactiva
    print("\n--- BÚSQUEDA PERSONALIZADA ---")
    id_alumno = pedir_entero(f"Ingrese el número de alumno a buscar (1 a {num_alumnos}): ", 1, num_alumnos)
    id_materia = pedir_entero(f"Ingrese el número de materia a buscar (1 a {num_materias}): ", 1, num_materias)
    
    # Conversión a índices base 0
    idx_alumno = id_alumno - 1
    idx_materia = id_materia - 1
    nombre_materia_elegida = materias[idx_materia]
    
    # Búsqueda en Forma 1: matriz[alumno][materia]
    inicio = time.perf_counter()
    calif_1 = matriz_forma1[idx_alumno][idx_materia]
    tiempo_busqueda_1 = time.perf_counter() - inicio
    
    # Búsqueda en Forma 2: matriz[materia][alumno]
    inicio = time.perf_counter()
    calif_2 = matriz_forma2[idx_materia][idx_alumno]
    tiempo_busqueda_2 = time.perf_counter() - inicio
    
    print("\n--- RESULTADO DE LA BÚSQUEDA ---")
    print(f"Materia consultada: {nombre_materia_elegida} (Opción {id_materia})")
    print(f"Forma 1 [Fila: Alum {id_alumno}][Col: {nombre_materia_elegida}]: Calificación = {calif_1} | Tiempo: {tiempo_busqueda_1:.9f} s")
    print(f"Forma 2 [Fila: {nombre_materia_elegida}][Col: Alum {id_alumno}]: Calificación = {calif_2} | Tiempo: {tiempo_busqueda_2:.9f} s")

if __name__ == "__main__":
    main()