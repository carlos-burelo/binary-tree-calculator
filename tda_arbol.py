from tda_pila import Pila


class NodoArbol(object):
    dato = None
    izq = None
    der = None


class ArbolExpresiones(object):
    def __init__(self):
        # Inicializa el árbol
        self.raiz = None

    def vacio(self):
        # Devuelve True si el árbol está vacío
        return self.raiz is None

    def reiniciar(self):
        # Elimina todos los elementos del árbol
        self.raiz = None

    def imprimir(self, tipo):
        # Imprime el árbol en el recorrido indicado por tipo
        cadena = ""
        if tipo == 0:
            cadena = self.prefijo(self.raiz)
        elif tipo == 1:
            cadena = self.postfijo(self.raiz)
        elif tipo == 2:
            cadena = self.entrefijo(self.raiz)
        return cadena

    def prefijo(self, nodo):
        # Devuelve una cadena con el recorrido en preorden del árbol
        cadena = ""
        if nodo is not None:
            cadena += str(nodo.dato)
            cadena += self.prefijo(nodo.izq)
            cadena += self.prefijo(nodo.der)
        return cadena

    def postfijo(self, nodo):
        # Devuelve una cadena con el recorrido en postorden del árbol
        cadena = ""
        if nodo is not None:
            cadena += self.postfijo(nodo.izq)
            cadena += self.postfijo(nodo.der)
            cadena += str(nodo.dato)
        return cadena

    def entrefijo(self, nodo):
        # Devuelve una cadena con el recorrido en entreorden del árbol
        cadena = ""
        if nodo is not None:
            cadena += self.entrefijo(nodo.izq)
            cadena += str(nodo.dato)
            cadena += self.entrefijo(nodo.der)
        return cadena

    def crear_sub_arbol(self, operando2, operando1, operador):
        # Crea un subárbol con el operador y sus operandos
        operador.izq = operando1
        operador.der = operando2
        return operador

    def prioridad(self, caracter):
        # Devuelve la prioridad de un operador con base a su jerarquía
        if caracter in ['^']:
            prioridad = 3
        elif caracter in ["*", '/']:
            prioridad = 2
        elif caracter in ['+', '-']:
            prioridad = 1
        else:
            prioridad = 0
        return prioridad

    def es_operador(self, caracter):
        # Devuelve True si el caracter es un operador
        return caracter in ['(', ')', '^', '*', '/', '+', '-']

    def validar_parentesis(self, cadena):
        # Valida que los paréntesis estén balanceados (abierto y cerrado)
        pila = Pila()
        for caracter in cadena:
            # Si el caracter es un paréntesis abierto, lo inserta en la pila
            if caracter == '(':
                pila.insertar(caracter)
            elif caracter == ')':
                # Si la pila está vacía, no hay paréntesis abierto para cerrar
                if pila.vacia() or pila.quitar() != '(':
                    # arroja un error de paréntesis desbalanceados
                    raise ValueError("Error: Paréntesis desbalanceados")

        # Si la pila no está vacía, hay paréntesis abierto sin cerrar
        if not pila.vacia():
            # arroja un error de paréntesis desbalanceados
            raise ValueError("Error: Paréntesis desbalanceados")

    def crear_arbol(self, cadena):
        # cada que se quiera crear un arbol primero se debe validar los parentesis
        self.validar_parentesis(cadena)

        # Se crea una pila para los operandos y otra para los operadores
        pila_operandos = Pila()
        pila_operadores = Pila()

        # Se crea una variable para almacenar los números que se van leyendo
        # para permitir números con más de un dígito y decimales
        numero = ""

        # Se recorre la cadena caracter por caracter
        for caracter in cadena:
            # Si el caracter es un dígito o un punto, se concatena a la variable numero
            if caracter.isdigit() or caracter == '.':
                numero += caracter
            else:
                # Si la variable numero tiene algún valor, se inserta en la pila de operandos
                if numero:
                    # Se crea un nodo para el número y se inserta en la pila de operandos
                    token = NodoArbol()
                    token.dato = float(numero)
                    pila_operandos.insertar(token)
                    # Se reinicia la variable numero para leer el siguiente número
                    numero = ""
                # Si el caracter es un operador, se crea un nodo para el operador
                if self.es_operador(caracter):
                    token = NodoArbol()
                    token.dato = caracter
                    # si el caracter es un operador de apertura, se inserta en la pila de operadores
                    if caracter == '(':
                        pila_operadores.insertar(token)
                    # si el caracter es un operador de cierre, se sacan los operadores de la pila
                    elif caracter == ')':
                        tope = pila_operadores.tope()
                        # mientras la pila no este vacia y el tope no sea un operador de apertura (otra expresion anidada)
                        while not pila_operadores.vacia() and tope.dato != '(':
                            # se sacan los operandos de la pila de operandos
                            operando2 = pila_operandos.quitar()
                            operando1 = pila_operandos.quitar()
                            operador = pila_operadores.quitar()
                            # se crea un nuevo operador con los operandos y se inserta en la pila de operandos
                            nuevo_operador = self.crear_sub_arbol(
                                operando2, operando1, operador)
                            pila_operandos.insertar(nuevo_operador)
                            # se actualiza el tope de la pila de operadores
                            tope = pila_operadores.tope()
                        # si la pila de operadores esta vacia, no hay paréntesis abierto para cerrar
                        if pila_operadores.vacia():
                            # arroja un error de parentecis desbalanceados
                            raise ValueError(
                                "Error: Paréntesis desbalanceados")
                        pila_operadores.quitar()  # Quitar el paréntesis izquierdo
                    else:
                        # si el caracter es un operador de cierre, se sacan los operadores de la pila
                        tope = pila_operadores.tope()
                        # mientras la pila de operadores no este vacia y la prioridad del caracter sea menor o igual a la del tope
                        while not pila_operadores.vacia() and self.prioridad(caracter) <= self.prioridad(tope.dato):
                            operando2 = pila_operandos.quitar()
                            operando1 = pila_operandos.quitar()
                            operador = pila_operadores.quitar()
                            # se crea un nuevo operando con base a los valores anteriores
                            nuevo_operando = self.crear_sub_arbol(
                                operando2, operando1, operador)
                            # se inserta el nuevo operando en la pila de operandos
                            pila_operandos.insertar(nuevo_operando)
                            # se actualiza el tope de la pila de operadores
                            tope = pila_operadores.tope()
                        pila_operadores.insertar(token)

        # si la variable numero tiene algún valor, se inserta en la pila de operandos
        if numero:
            token = NodoArbol()
            token.dato = float(numero)
            pila_operandos.insertar(token)
        # mientras la pila de operadores no este vacia
        while not pila_operadores.vacia():
            operando2 = pila_operandos.quitar()
            operando1 = pila_operandos.quitar()
            operador = pila_operadores.quitar()
            # se crea un nuevo operando con base a los valores anteriores
            nuevo_operando = self.crear_sub_arbol(
                operando2, operando1, operador)
            pila_operandos.insertar(nuevo_operando)
        # se asigna el nodo raiz del arbol a la raiz del arbol
        self.raiz = pila_operandos.quitar()

    def evalua(self):
        # se evalua la expresion con base a la raiz del arbol
        return self.evaluar_expresion(self.raiz)

    def evaluar_expresion(self, sub_arbol):
        # se crea una variable para almacenar el resultado de la evaluacion
        acum = 0.0
        # si el sub arbol no es un operador, se retorna el valor del nodo
        if not self.es_operador(sub_arbol.dato):
            return float(sub_arbol.dato)
        else:
            # si el valor del sub_arbol es el simbolo de exponente se retorna el resultado de la evaluacion de los sub arboles izquierdo y derecho
            if sub_arbol.dato == '^':
                acum += self.evaluar_expresion(
                    sub_arbol.izq) ** self.evaluar_expresion(sub_arbol.der)
            # si el valor del sub_arbol es el simbolo de multiplicacion se retorna el resultado de la evaluacion de los sub arboles izquierdo y derecho
            elif sub_arbol.dato == '*':
                acum += self.evaluar_expresion(sub_arbol.izq) * \
                    self.evaluar_expresion(sub_arbol.der)
            # si el valor del sub_arbol es el simbolo de division se retorna el resultado de la evaluacion de los sub arboles izquierdo y derecho
            elif sub_arbol.dato == '/':
                # se evalua el denominador
                denominador = self.evaluar_expresion(sub_arbol.der)
                if denominador == 0:  # si el denominador es cero, se arroja un error de division entre cero
                    raise ZeroDivisionError("Error: División entre cero")
                # se retorna el resultado de la division de los sub arboles izquierdo y derecho
                acum += self.evaluar_expresion(sub_arbol.izq) / denominador
            # si el valor del sub_arbol es el simbolo de suma se retorna el resultado de la evaluacion de los sub arboles izquierdo y derecho
            elif sub_arbol.dato == '+':
                acum += self.evaluar_expresion(sub_arbol.izq) + \
                    self.evaluar_expresion(sub_arbol.der)
            # si el valor del sub_arbol es el simbolo de resta se retorna el resultado de la evaluacion de los sub arboles izquierdo y derecho
            elif sub_arbol.dato == '-':
                acum += self.evaluar_expresion(sub_arbol.izq) - \
                    self.evaluar_expresion(sub_arbol.der)
        # retorna el valor acumulado de todas las expresiones
        return acum
