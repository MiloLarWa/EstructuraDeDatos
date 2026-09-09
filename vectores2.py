import random
import statistics

# Generar una lista de 50 números enteros al azar entre 1 y 100
datos = [random.randint(1, 999) for _ in range(50)]

# Ordenar la lista para facilitar la visualización (opcional)
datos.sort()

# Calcular las medidas estadísticas
media = statistics.mean(datos)
mediana = statistics.median(datos)

# Manejo de la moda por si hay múltiples modas o ninguna única
try:
    moda = statistics.mode(datos)
except statistics.StatisticsError:
    # Si hay múltiples modas, obtenemos todas las que se repiten el máximo número de veces
    from collections import Counter
    conteo = Counter(datos)
    max_frecuencia = max(conteo.values())
    moda = [k for k, v in conteo.items() if v == max_frecuencia]

rango = max(datos) - min(datos)
varianza = statistics.variance(datos)
desviacion_estandar = statistics.stdev(datos)

# Mostrar resultados
print(f"Lista de datos generada ({len(datos)} elementos):")
print(datos)
print("\n--- Estadísticas ---")
print(f"Media (Promedio): {media:.2f}")
print(f"Mediana: {mediana}")
print(f"Moda: {moda}")
print(f"Rango: {rango} (Mínimo: {min(datos)}, Máximo: {max(datos)})")
print(f"Varianza muestral: {varianza:.2f}")
print(f"Desviación estándar: {desviacion_estandar:.2f}")
