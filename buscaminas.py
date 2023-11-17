import tkinter as tk
from tkinter import messagebox
import random

class BuscaminasGUI:
    def __init__(self, master, alto, ancho, minas):
        self.alto = alto
        self.ancho = ancho
        self.minas = minas
        self.master = master
        self.buttons = [[None for _ in range(ancho)] for _ in range(alto)]
        self.inicializar_interfaz()
        self.tablero = [[' ' for _ in range(ancho)] for _ in range(alto)]
        self.colocar_minas()
        self.celdas_descubiertas = set()

    def inicializar_interfaz(self):
        for fila in range(self.alto):
            for columna in range(self.ancho):
                btn = tk.Button(self.master, text=' ', width=2, height=1,
                                command=lambda r=fila, c=columna: self.cavar(r, c))
                btn.grid(row=fila, column=columna)
                self.buttons[fila][columna] = btn

    def colocar_minas(self):
        minas_colocadas = 0
        while minas_colocadas < self.minas:
            fila = random.randint(0, self.alto - 1)
            columna = random.randint(0, self.ancho - 1)
            if self.tablero[fila][columna] != 'X':
                self.tablero[fila][columna] = 'X'
                minas_colocadas += 1

    def cavar(self, fila, columna):
        if (fila, columna) in self.celdas_descubiertas:
            return
        self.celdas_descubiertas.add((fila, columna))
        if self.tablero[fila][columna] == 'X':
            self.revelar_minas()
            messagebox.showinfo("Game Over", "Has pisado una mina. ¡Juego terminado!")
            self.master.destroy()
        else:
            minas_alrededor = self.minas_vecinas(fila, columna)
            self.buttons[fila][columna].config(text=str(minas_alrededor))
            if minas_alrededor == 0:
                for r, c in self.celdas_vecinas(fila, columna):
                    self.cavar(r, c)

    def minas_vecinas(self, fila, columna):
        return sum(1 for r, c in self.celdas_vecinas(fila, columna) if self.tablero[r][c] == 'X')

    def celdas_vecinas(self, fila, columna):
        vecinos = []
        for r in range(max(0, fila - 1), min(self.alto, fila + 2)):
            for c in range(max(0, columna - 1), min(self.ancho, columna + 2)):
                if (r, c) != (fila, columna):
                    vecinos.append((r, c))
        return vecinos

    def revelar_minas(self):
        for r in range(self.alto):
            for c in range(self.ancho):
                if self.tablero[r][c] == 'X':
                    self.buttons[r][c].config(text='X', bg='red')

def main():
    root = tk.Tk()
    root.title("Buscaminas")

    # Establece las dimensiones del juego
    alto = 10
    ancho = 10
    minas = 10

    BuscaminasGUI(root, alto, ancho, minas)
    root.mainloop()

if __name__ == "__main__":
    main()
