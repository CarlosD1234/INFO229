import pygame
import tkinter as tk
from tkinter import messagebox
import random

class BuscaminasGUI:
	#Patron Game Loop
	#ProcessInput: revelar_Minas(Self), cavar(self, fila, columna)
	#Update: minas_vecinas(self, fila, columna), celdas_vecinas(self, fila, columna)
	#Render: inicializar_interfaz(self)
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
        pygame.init()
        self.sonido_mina = pygame.mixer.Sound("boom.wav")
        self.sonido_mina.set_volume(0.1)
	
	#Inicializa la interfaz del juego creando los botones
    def inicializar_interfaz(self):
        for fila in range(self.alto):
            for columna in range(self.ancho):
                btn = tk.Button(self.master, text=' ', width=2, height=1,
                                command=lambda r=fila, c=columna: self.cavar(r, c))
                btn.grid(row=fila, column=columna)
                self.buttons[fila][columna] = btn

    #Coloca las minas en el tablero de forma aleatoria
    def colocar_minas(self):
        minas_colocadas = 0
        while minas_colocadas < self.minas:
            fila = random.randint(0, self.alto - 1)
            columna = random.randint(0, self.ancho - 1)
            if self.tablero[fila][columna] != 'X':
                self.tablero[fila][columna] = 'X'
                minas_colocadas += 1

    #Revela las celdas al hacer click, tambien termina el juego si se pisa una mina (derrota) o si solo quedan minas en el tablero (victoria)
    def cavar(self, fila, columna):
        if (fila, columna) in self.celdas_descubiertas:
            return
        self.celdas_descubiertas.add((fila, columna))
        if self.tablero[fila][columna] == 'X':
            self.sonido_mina.play()  # Reproduce el sonido
            self.revelar_minas()
            messagebox.showinfo("Game Over", "Has pisado una mina. ¡Juego terminado!")
            self.master.destroy()
        else:
            minas_alrededor = self.minas_vecinas(fila, columna)
            if minas_alrededor > 0:
                self.buttons[fila][columna].config(text=str(minas_alrededor), bg='gray')
            else:
                self.buttons[fila][columna].config(text=' ', bg='gray')
                for r, c in self.celdas_vecinas(fila, columna):
                    self.cavar(r, c)
                if len(self.celdas_descubiertas) + self.minas == self.alto * self.ancho:
                    messagebox.showinfo("¡Felicidades!", "¡Has ganado el juego!")
                    self.master.destroy()

    
    # Calcula la cantidad de minas vecinas a una celda específica
    def minas_vecinas(self, fila, columna):
        return sum(1 for r, c in self.celdas_vecinas(fila, columna) if self.tablero[r][c] == 'X')

    # Obtiene las celdas vecinas de una celda específica
    def celdas_vecinas(self, fila, columna):
        vecinos = []
        for r in range(max(0, fila - 1), min(self.alto, fila + 2)):
            for c in range(max(0, columna - 1), min(self.ancho, columna + 2)):
                if (r, c) != (fila, columna):
                    vecinos.append((r, c))
        return vecinos
    
    #Revela todas las minas al perder el juego
    def revelar_minas(self):
        for r in range(self.alto):
            for c in range(self.ancho):
                if self.tablero[r][c] == 'X':
                    self.buttons[r][c].config(text='X', bg='red')
