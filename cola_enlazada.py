"""Práctica 1.2: cola de pedidos con nodos."""


class Order:
    """Pedido con cantidad de producto y cliente."""

    def __init__(self, qtty, customer):
        self.qtty = qtty
        self.customer = customer

    def getQtty(self):
        return self.qtty

    def getCustomer(self):
        return self.customer

    def print(self):
        print(f"     Cliente: {self.getCustomer()}")
        print(f"     Cantidad: {self.getQtty()}")
        print("     ------------")


class Node:
    """Contiene un objeto y una referencia al siguiente nodo."""

    def __init__(self, info):
        self.info = info
        self.next = None


class Queue:
    """Cola FIFO: inserta al final y extrae por el principio."""

    def __init__(self):
        self.top = None
        self.tail = None
        self._size = 0

    def size(self):
        return self._size

    def isEmpty(self):
        return self._size == 0

    def front(self):
        """Consulta el primero sin retirarlo; None si está vacía."""
        if self.isEmpty():
            return None
        return self.top.info

    def enqueue(self, info):
        """Enlaza un nuevo nodo al final, sin recorrer la cola."""
        nuevo = Node(info)
        if self.isEmpty():
            self.top = nuevo
        else:
            self.tail.next = nuevo
        self.tail = nuevo
        self._size += 1

    def dequeue(self):
        """Retira y devuelve el primero; None si está vacía."""
        if self.isEmpty():
            return None
        info = self.top.info
        self.top = self.top.next
        self._size -= 1
        # Si salió el último nodo, ya no hay ningún extremo.
        if self.isEmpty():
            self.tail = None
        return info

    def getNth(self, pos):
        """Posiciones desde 1. Una posición inválida devuelve None."""
        if type(pos) is not int or pos < 1 or pos > self._size:
            return None
        actual = self.top
        for _ in range(pos - 1):
            actual = actual.next
        return actual.info

    def printInfo(self):
        """Recorre los nodos sin modificar la cola."""
        print("********* CONTENIDO DE LA COLA *********")
        print(f"   Tamaño: {self.size()}")
        actual = self.top
        posicion = 1
        while actual is not None:
            print(f"   ** Elemento {posicion}")
            if isinstance(actual.info, Order):
                actual.info.print()
            else:
                print(f"     {actual.info}")
            actual = actual.next
            posicion += 1
        print("**************************************")


class TestQueue:
    """Demostración de las operaciones con cuatro pedidos."""

    @staticmethod
    def main():
        cola = Queue()
        print("¿Está vacía al comenzar?", cola.isEmpty())
        print("front() en cola vacía:", cola.front())
        print("dequeue() en cola vacía:", cola.dequeue())
        cola.printInfo()

        # Esta tupla solo contiene los ejemplos; Queue almacena nodos.
        pedidos = (
            Order(20, "Ana"),
            Order(30, "Bruno"),
            Order(40, "Carla"),
            Order(50, "Diego"),
        )
        for pedido in pedidos:
            print(f"\nInsertando pedido de {pedido.getCustomer()}...")
            cola.enqueue(pedido)
            cola.printInfo()

        print("\nPrimer pedido, sin extraerlo:")
        cola.front().print()
        print("Tamaño después de front():", cola.size())
        print("\nTercer pedido, sin extraerlo:")
        cola.getNth(3).print()
        print("Tamaño después de getNth(3):", cola.size())
        print("Posición 0 (inválida):", cola.getNth(0))
        print("Posición 5 (inválida):", cola.getNth(5))

        print("\nProcesando pedidos por orden de llegada:")
        while not cola.isEmpty():
            atendido = cola.dequeue()
            print(f"Atendido: {atendido.getCustomer()}")
            cola.printInfo()

        print("\n¿Está vacía al terminar?", cola.isEmpty())
        print("dequeue() en cola vacía:", cola.dequeue())
        cola.printInfo()
        print("\nLa cola se puede volver a utilizar:")
        cola.enqueue(Order(10, "Elena"))
        cola.printInfo()
        print("Atendido:", cola.dequeue().getCustomer())
        cola.printInfo()


if __name__ == "__main__":
    TestQueue.main()
