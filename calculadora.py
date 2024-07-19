from tkinter import INSERT, Tk, Entry, Button, END, Frame, messagebox
from tda_arbol import ArbolExpresiones


class Calculadora:
    # se crea una matriz de los botones de la calculadora
    botones = [
        ["C", "(", ")", "/"],
        ["7", "8", "9", "*"],
        ["4", "5", "6", "-"],
        ["1", "2", "3", "+"],
        ["^", "0", ".", "="],
    ]

    def __init__(self) -> None:
        self.ventana = Tk()
        self.ventana.title("Calculadora")
        # la self.ventana se divide en 2 frames
        # frame_entrada y frame_botones
        self.frame_entrada = Frame(self.ventana)
        self.frame_botones = Frame(self.ventana)
        # frame_entrada sera de color gris y un tamaño de 300x100
        self.frame_entrada.config(bg="gray", width=400, height=100)
        # frame_botones sera de color blanco y un tamaño de 400x500 (grid: 4x5)
        self.frame_botones.config(bg="white", width=400, height=500)
        # se agregan los frames a la self.ventana
        self.frame_entrada.pack()
        self.frame_botones.pack()
        # se crea la entrada de texto
        self.entrada = Entry(self.frame_entrada, font=("Arial", 20))
        self.entrada.grid(row=0, column=0, columnspan=5, padx=5, pady=5)

        self.iniciar()

    def click(self, valor):
        # se obtiene el valor de la entrada actual
        previa = self.entrada.get()
        # se obtiene la posicion del cursor
        posicion = self.entrada.index(INSERT)
        # se inserta el valor en la posicion del cursor
        self.entrada.insert(posicion, valor)

    def borrar(self):
        # se borra todo lo que hay en la entrada
        self.entrada.delete(0, END)

    def calcular(self):
        # se obtiene el valor de la entrada
        expresion = self.entrada.get()
        # se hace una sentencia try/catch para evaluar la expresion
        # ya que contamos con los escenarios donde puede fallar
        # ya sea por Dividir entre 0 y por no ser una expresion valida
        try:
            # creamos una instancia de la clase ArbolExpresiones
            arbol = ArbolExpresiones()
            # se crea el arbol con la expresion
            arbol.crear_arbol(expresion)
            # se borra la entrada
            self.entrada.delete(0, END)
            # se agrega el resultado de la evaluacion de la expresion
            self.entrada.insert(0, str(arbol.evalua()))

        # se crean los mensajes de error para cada escenario
        except ValueError as e:
            # si la expresion no es valida se arroja un error (problmas con los parentesis)
            messagebox.showerror("Error", e)
        except ZeroDivisionError as e:
            # si se intenta dividir entre cero se arroja un error
            messagebox.showerror("Error", e)
        except Exception as e:
            # si la expresion no es valida se arroja un error (problemas con los operadores)
            messagebox.showerror("Error", e)

    def crear_botones(self):
        # Recorre las filas y columnas de la matriz de botones
        for fila in range(5):
            for columna in range(4):
                # botones redondos color verde estilo flat
                # crea un boton con el texto de la matriz de botones y estilos basicos
                boton = Button(
                    self.frame_botones,
                    text=self.botones[fila][columna],
                    width=10,
                    height=4,
                    font=("Arial", 10, "bold"),
                    bg="white",
                    relief="flat",
                )
                # se agrega el boton a la ventana en la fila y columna correspondiente
                boton.grid(row=fila, column=columna, padx=0, pady=0)
                # se agregan los comandos a los botones

                # si el boton es el "=" se le agrega el comando de calcular
                if boton["text"] == "=":
                    boton.configure(command=self.calcular)
                # si el boton es el "C" se le agrega el comando de borrar
                elif boton["text"] == "C":
                    boton.configure(command=self.borrar)
                # cualquier otro boton se le agrega el comando de click con el texto del boton
                else:
                    boton.configure(
                        command=lambda x=boton["text"]: self.click(x))

    def iniciar(self):
        # se crean los botones
        self.crear_botones()
        # se inicia la ventana principal
        self.ventana.mainloop()


calculadora = Calculadora()
