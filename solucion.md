# Solución: estructura POSTRES

El primer programa tiene un menú interactivo y empieza con el arreglo vacío. El segundo ejecuta una demostración con duplicados e importa las estructuras del primero. Sus funciones también se pueden importar desde otros programas.

## Ejercicio 1

`POSTRES` es una lista de Python usada como arreglo dinámico y mantenida en orden alfabético. Cada objeto `Postre` contiene su nombre y una `ListaIngredientes`. Cada `Nodo` contiene un ingrediente y la referencia `siguiente`. `None` representa el `NIL` del dibujo.

Los ingredientes conservan el orden de inserción: el enunciado exige ordenar los postres, no sus ingredientes.

| Inciso | Función | Solución |
| --- | --- | --- |
| a | `imprimir_ingredientes` | Busca el postre y recorre sus nodos hasta `None`. |
| b | `insertar_ingredientes` | Valida todos los nuevos ingredientes y los agrega al final de la lista. |
| c | `eliminar_ingrediente` | Localiza el nodo y modifica la cabeza o el enlace del nodo anterior. |
| d | `dar_alta` | Localiza la posición alfabética mediante búsqueda binaria e inserta el postre con sus ingredientes. |
| e | `dar_baja` | Desenlaza todos los ingredientes y elimina la entrada del arreglo. |

### Casos contemplados

- Arreglo vacío, postre inexistente y lista de ingredientes vacía.
- Alta y baja al principio, en medio o al final del arreglo; baja del único postre.
- Eliminación del primer ingrediente, uno intermedio, el último o el único.
- Nombres vacíos, opciones inválidas e ingredientes inexistentes.
- Postres e ingredientes repetidos: se muestra el error y se rechaza la operación.
- Inserción de varios ingredientes: se valida todo antes de modificar la lista, evitando cambios parciales cuando uno es inválido o repetido.
- Un ingrediente puede pertenecer a diferentes postres; eso es válido.
- Se permite un postre sin ingredientes porque el dibujo incluye una referencia directa a `NIL`.

Se ignoran mayúsculas, acentos y espacios sobrantes al comparar: `FLAN` y `Flan` son el mismo postre; `azucar` y `Azúcar` son el mismo ingrediente. La `ñ` se distingue de la `n`. Se conserva la escritura del primer nombre registrado. Para ordenar se consideran las vocales acentuadas como vocales y se coloca la `ñ` después de la `n`.

El arreglo es dinámico, por lo que no se establece una capacidad fija. La búsqueda realiza O(log P) comparaciones; insertar o eliminar del arreglo puede desplazar O(P) elementos, donde P es el número de postres. Recorrer una lista de I ingredientes cuesta O(I), sin contar la longitud de los textos.

## Ejercicio 2

El enunciado no precisa si «elementos repetidos» significa postres o ingredientes repetidos. El subprograma `eliminar_repetidos` resuelve ambos casos mediante este criterio: **fusionar los postres del mismo nombre y conservar todos sus ingredientes distintos**.

1. Recorre el arreglo y agrupa los postres por su nombre normalizado.
2. Crea una lista enlazada nueva para cada postre distinto.
3. Copia una sola vez cada ingrediente de ese postre.
4. Reemplaza el contenido de `POSTRES` por los postres únicos ordenados.
5. Devuelve los conteos de postres e ingredientes repetidos eliminados.

El diccionario y los conjuntos son estructuras auxiliares. El resultado sigue siendo un arreglo de postres con listas enlazadas.

Las altas normales del ejercicio 1 previenen duplicados; el ejercicio 2 permite depurar datos importados o previamente cargados. Por eso su demostración crea explícitamente registros repetidos. Para usarlo sobre cualquier arreglo creado con estas clases:

```python
from ejercicio2 import eliminar_repetidos
resumen = eliminar_repetidos(POSTRES)
print(resumen)
```

### Resultado de la demostración

```text
ANTES:
- Flan: Leche, Huevo, Leche
- FLAN: Azúcar, Huevo
- Gelatina: (sin ingredientes)
- Gelatina: Agua, Grenetina, Agua
- Pastel: Harina, Leche, Harina

DESPUÉS:
- Flan: Leche, Huevo, Azúcar
- Gelatina: Agua, Grenetina
- Pastel: Harina, Leche

Postres repetidos eliminados: 2
Ingredientes repetidos eliminados: 4
```

`Leche` permanece en Flan y en Pastel: los ingredientes se depuran dentro de cada receta, no entre recetas distintas.

### ¿Qué sucedió con las listas?

Las listas de los registros que representan el mismo postre se fusionaron en una nueva lista sin repeticiones. El azúcar que estaba solamente en el segundo registro de Flan se conservó. Un postre vacío también se conserva; si otro registro del mismo postre tiene ingredientes, se incorporan.

Las listas anteriores dejan de pertenecer a `POSTRES`. Si ningún otro objeto las referencia, Python puede recuperar automáticamente su memoria. Si otra parte del programa conserva una referencia a una lista anterior, esa lista sigue existiendo sin modificaciones. El subprograma crea nodos nuevos y no deja referencias colgantes.

### ¿Mandó mensaje de error?

No: la demostración termina sin errores. Un arreglo vacío o sin duplicados también es válido. En el ejercicio 1, las entradas inválidas se reportan mediante mensajes controlados con `ValueError`, sin detener el menú.

### Conclusiones

Eliminar únicamente el registro de un postre repetido podría perder los ingredientes exclusivos de su lista. Antes de eliminarlo se debe definir cómo tratar sus ingredientes; aquí se conserva la unión de las listas. Construir listas nuevas evita cambiar enlaces mientras se recorren los originales.

Una segunda ejecución sobre el resultado elimina cero duplicados. Con P registros, I apariciones de ingredientes y U postres únicos, el tiempo esperado es O(P + I + U log U), sin contar la longitud de los textos. La memoria auxiliar es proporcional a los postres e ingredientes únicos.
