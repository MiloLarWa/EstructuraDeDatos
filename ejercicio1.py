"""Ejercicio 1. Ejecutar con Python 3.9 o posterior, sin dependencias."""
from dataclasses import dataclass
from typing import Optional
import unicodedata


def limpiar(nombre):
    nombre = " ".join(nombre.split())
    if not nombre:
        raise ValueError("El nombre no puede estar vacío.")
    return unicodedata.normalize("NFC", nombre)


def clave(nombre):
    # Ignora mayúsculas y acentos, pero conserva la ñ.
    partes = []
    for letra in limpiar(nombre).casefold():
        if letra == "ñ":
            partes.append(letra)
        else:
            partes.extend(c for c in unicodedata.normalize("NFD", letra)
                          if not unicodedata.combining(c))
    return "".join(partes)


def orden(nombre):
    # Cada letra se representa con una pareja para situar ñ después de n.
    return tuple(("n", 1) if c == "ñ" else (c, 0) for c in clave(nombre))


@dataclass
class Nodo:
    nombre: str
    siguiente: Optional["Nodo"] = None


class ListaIngredientes:
    def __init__(self, nombres=()):
        self.cabeza = None
        ultimo = None
        # Una carga directa conserva repeticiones para el ejercicio 2.
        # Las operaciones normales de alta e inserción sí las rechazan.
        for nombre in nombres:
            nuevo = Nodo(limpiar(nombre))
            if ultimo is None:
                self.cabeza = nuevo
            else:
                ultimo.siguiente = nuevo
            ultimo = nuevo

    def __iter__(self):
        actual = self.cabeza
        while actual is not None:
            yield actual.nombre
            actual = actual.siguiente

    def agregar(self, nombre):
        nombre = limpiar(nombre)
        actual, anterior = self.cabeza, None
        while actual is not None:
            if clave(actual.nombre) == clave(nombre):
                raise ValueError(f"El ingrediente '{nombre}' ya existe.")
            anterior, actual = actual, actual.siguiente
        nuevo = Nodo(nombre)
        if anterior is None:
            self.cabeza = nuevo
        else:
            anterior.siguiente = nuevo

    def eliminar(self, nombre):
        buscado = clave(nombre)
        actual, anterior = self.cabeza, None
        while actual is not None and clave(actual.nombre) != buscado:
            anterior, actual = actual, actual.siguiente
        if actual is None:
            raise ValueError(f"El ingrediente '{nombre}' no existe en este postre.")
        if anterior is None:
            self.cabeza = actual.siguiente
        else:
            anterior.siguiente = actual.siguiente
        actual.siguiente = None

    def vaciar(self):
        while self.cabeza is not None:
            eliminado = self.cabeza
            self.cabeza = eliminado.siguiente
            eliminado.siguiente = None


@dataclass
class Postre:
    nombre: str
    ingredientes: ListaIngredientes


def posicion(postres, nombre):
    """Búsqueda binaria: devuelve la posición y si se encontró el postre."""
    buscado = orden(nombre)
    izquierda, derecha = 0, len(postres)
    while izquierda < derecha:
        medio = (izquierda + derecha) // 2
        if orden(postres[medio].nombre) < buscado:
            izquierda = medio + 1
        else:
            derecha = medio
    encontrado = (izquierda < len(postres)
                  and clave(postres[izquierda].nombre) == clave(nombre))
    return izquierda, encontrado


def obtener_postre(postres, nombre):
    indice, encontrado = posicion(postres, nombre)
    if not encontrado:
        raise ValueError(f"El postre '{nombre}' no existe.")
    return postres[indice]


def imprimir_ingredientes(postres, nombre):
    """Inciso a."""
    postre = obtener_postre(postres, nombre)
    print(f"Ingredientes de {postre.nombre}:")
    if postre.ingredientes.cabeza is None:
        print("  (sin ingredientes)")
    for ingrediente in postre.ingredientes:
        print(f"  - {ingrediente}")


def insertar_ingredientes(postres, nombre, ingredientes):
    """Inciso b: valida todo antes de modificar la lista."""
    postre = obtener_postre(postres, nombre)
    nuevos = [limpiar(i) for i in ingredientes]
    if not nuevos:
        raise ValueError("Debe indicar al menos un ingrediente.")
    vistos = {clave(i) for i in postre.ingredientes}
    for ingrediente in nuevos:
        if clave(ingrediente) in vistos:
            raise ValueError(f"Ingrediente repetido: '{ingrediente}'. No se insertó ninguno.")
        vistos.add(clave(ingrediente))
    for ingrediente in nuevos:
        postre.ingredientes.agregar(ingrediente)


def eliminar_ingrediente(postres, nombre, ingrediente):
    """Inciso c: sirve para el primero, uno intermedio, el último o el único."""
    obtener_postre(postres, nombre).ingredientes.eliminar(ingrediente)


def dar_alta(postres, nombre, ingredientes):
    """Inciso d: inserta el postre en su posición alfabética."""
    nombre = limpiar(nombre)
    indice, encontrado = posicion(postres, nombre)
    if encontrado:
        raise ValueError(f"El postre '{nombre}' ya está registrado.")
    nombres = [limpiar(i) for i in ingredientes]
    if len({clave(i) for i in nombres}) != len(nombres):
        raise ValueError("Hay ingredientes repetidos. No se dio de alta el postre.")
    postres.insert(indice, Postre(nombre, ListaIngredientes(nombres)))


def dar_baja(postres, nombre):
    """Inciso e: desenlaza todos los ingredientes y elimina el postre."""
    indice, encontrado = posicion(postres, nombre)
    if not encontrado:
        raise ValueError(f"El postre '{nombre}' no existe.")
    postres[indice].ingredientes.vaciar()
    del postres[indice]


def mostrar_postres(postres):
    if not postres:
        print("No hay postres registrados.")
    for postre in postres:
        ingredientes = ", ".join(postre.ingredientes) or "(sin ingredientes)"
        print(f"- {postre.nombre}: {ingredientes}")


def leer_ingredientes():
    texto = input("Ingredientes separados por comas (vacío = ninguno): ").strip()
    return texto.split(",") if texto else []


def main():
    POSTRES = []
    while True:
        print("\n1. Consultar ingredientes\n2. Insertar ingredientes"
              "\n3. Eliminar un ingrediente\n4. Dar de alta un postre"
              "\n5. Dar de baja un postre\n6. Mostrar todos los postres\n0. Salir")
        opcion = input("Opción: ").strip()
        try:
            if opcion == "0":
                break
            elif opcion == "1":
                imprimir_ingredientes(POSTRES, input("Postre: "))
            elif opcion == "2":
                nombre = input("Postre: ")
                insertar_ingredientes(POSTRES, nombre, leer_ingredientes())
                print("Ingredientes insertados.")
            elif opcion == "3":
                nombre = input("Postre: ")
                eliminar_ingrediente(POSTRES, nombre, input("Ingrediente: "))
                print("Ingrediente eliminado.")
            elif opcion == "4":
                nombre = input("Postre: ")
                dar_alta(POSTRES, nombre, leer_ingredientes())
                print("Postre registrado.")
            elif opcion == "5":
                dar_baja(POSTRES, input("Postre: "))
                print("Postre y todos sus ingredientes eliminados.")
            elif opcion == "6":
                mostrar_postres(POSTRES)
            else:
                print("Error: opción inválida.")
        except ValueError as error:
            print(f"Error: {error}")


if __name__ == "__main__":
    try:
        main()
    except (EOFError, KeyboardInterrupt):
        print("\nPrograma terminado.")
