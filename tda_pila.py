class NodoPila(object):
    dato = None
    siguiente = None


class Pila(object):
    def __init__(self) -> None:
        self.tope_pila = None

    def reiniciar(self):
        # Elimina todos los elementos de la pila
        self.tope_pila = None

    def insertar(self, dato):
        # Inserta un elemento en la pila
        nodo = NodoPila()
        nodo.dato = dato
        nodo.siguiente = self.tope_pila
        self.tope_pila = nodo

    def quitar(self):
        # Elimina un elemento de la pila
        x = self.tope_pila.dato
        nodo_elimiar = self.tope_pila
        self.tope_pila = self.tope_pila.siguiente
        nodo_elimiar.siguiente = None
        return x

    def vacia(self):
        # Devuelve True si la pila está vacía
        return self.tope_pila is None

    def tope(self):
        # Devuelve el elemento en el tope de la pila
        if self.tope_pila is not None:
            return self.tope_pila.dato
        else:
            return None
