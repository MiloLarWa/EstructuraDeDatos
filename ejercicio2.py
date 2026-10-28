"""Ejercicio 2. Guardar junto a ejercicio1.py y ejecutar este archivo."""
from ejercicio1 import ListaIngredientes, Nodo, Postre, clave, mostrar_postres, orden


def eliminar_repetidos(postres):
    """Une los postres repetidos y conserva sus ingredientes sin repeticiones.

    Modifica el mismo arreglo y devuelve los conteos de duplicados eliminados.
    Las listas nuevas evitan alterar los enlaces que se están recorriendo.
    """
    unicos = {}
    postres_eliminados = 0
    ingredientes_eliminados = 0
    for postre in postres:
        identificador = clave(postre.nombre)
        if identificador not in unicos:
            nuevo = Postre(postre.nombre, ListaIngredientes())
            # Cada registro contiene: postre nuevo, ingredientes vistos, último nodo.
            unicos[identificador] = [nuevo, set(), None]
        else:
            postres_eliminados += 1
        registro = unicos[identificador]
        destino, vistos, ultimo = registro
        for ingrediente in postre.ingredientes:
            identificador_ingrediente = clave(ingrediente)
            if identificador_ingrediente in vistos:
                ingredientes_eliminados += 1
                continue
            vistos.add(identificador_ingrediente)
            nodo = Nodo(ingrediente)
            if ultimo is None:
                destino.ingredientes.cabeza = nodo
            else:
                ultimo.siguiente = nodo
            ultimo = nodo
        registro[2] = ultimo
    # La asignación por rebanada conserva el objeto arreglo original.
    postres[:] = sorted((registro[0] for registro in unicos.values()),
                        key=lambda postre: orden(postre.nombre))
    return {"postres_eliminados": postres_eliminados,
            "ingredientes_eliminados": ingredientes_eliminados}


def main():
    # Simula datos importados con duplicados; las altas normales los previenen.
    POSTRES = [
        Postre("Flan", ListaIngredientes(["Leche", "Huevo", "Leche"])),
        Postre("FLAN", ListaIngredientes(["Azúcar", "Huevo"])),
        Postre("Gelatina", ListaIngredientes()),
        Postre("Gelatina", ListaIngredientes(["Agua", "Grenetina", "Agua"])),
        Postre("Pastel", ListaIngredientes(["Harina", "Leche", "Harina"])),
    ]
    print("ANTES:")
    mostrar_postres(POSTRES)
    resumen = eliminar_repetidos(POSTRES)
    print("\nDESPUÉS:")
    mostrar_postres(POSTRES)
    print(f"\nPostres repetidos eliminados: {resumen['postres_eliminados']}")
    print(f"Ingredientes repetidos eliminados: {resumen['ingredientes_eliminados']}")
    print("\nLas listas se fusionaron sin perder ingredientes distintos.")
    print("No se produjo un error. Python gestiona los objetos sin referencias.")


if __name__ == "__main__":
    main()
