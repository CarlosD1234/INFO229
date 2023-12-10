from buscaminas import BuscaminasGUI
import tkinter as tk

#Configura las dimensiones del tablero y la cantidad de minas mediante la entrada del usuario
def config():
    alto = int(input("Ingrese la altura del tablero: "))
    ancho= int(input("Ingrese el ancho del tablero: "))
    minas = int(input("Ingrese la cantidad de minas: "))

    while minas >= (alto * ancho):
        print("ERROR: la cantidad de minas no puede ser mayor o igual a la contidad de celdas\n")
        minas = int(input("Ingrese la cantidad de minas: "))
    
    return alto, ancho, minas

def main():

    # Establece las dimensiones del juego
    alto, ancho, minas = config()

    root = tk.Tk()
    root.title("Buscaminas")

    BuscaminasGUI(root, alto, ancho, minas)
    root.mainloop()

if __name__ == "__main__":
    main()