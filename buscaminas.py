#añadi game over, pantalla de victoria y banderas con click derecho

import tkinter as tk
import random

# Dimensiones del tablero
filas = 10
columnas = 10
num_minas = 15

# Ventana principal
ventana = tk.Tk()
ventana.geometry("300x420")
ventana.resizable(False, False)
ventana.title("Buscaminas")
ventana.iconbitmap("buscaminas.ico")

# marco del contador y botón de reinicio
marco_superior = tk.Frame(ventana)
marco_superior.pack(fill=tk.X, pady=5)

# Contador de celdas reveladas
contador_var = tk.IntVar()
contador_var.set(0)
contador_label = tk.Label(marco_superior, textvariable=contador_var, font=("Arial", 12))
contador_label.pack(side="left", padx=20)

# Mensaje de Game Over (inicialmente vacío)
game_over_label = tk.Label(marco_superior, text="", font=("Arial", 12), fg="red")
game_over_label.pack(side="left", expand=True)

# Botón de reinicio
boton_reinicio = tk.Button(marco_superior, text="🔄", font=("Arial", 14), command=lambda: reiniciar_juego())
boton_reinicio.pack(side="right", padx=20)

# cuadrícula inferior 

marco_juego = tk.Frame(ventana)
marco_juego.pack(side="bottom", pady=10)

# Inicialización de variables
botones = []
tablero = []

# Generar tablero con minas aleatorias
def generar_tablero():
    global tablero
    tablero = [[0 for _ in range(columnas)] for _ in range(filas)]
    minas_pos = random.sample(range(filas * columnas), num_minas)

    for pos in minas_pos:
        fila = pos // columnas
        columna = pos % columnas
        tablero[fila][columna] = -1  # Mina

    calcular_adyacencia()

# Calcular números de adyacencia
def calcular_adyacencia():
    for fila in range(filas):
        for columna in range(columnas):
            if tablero[fila][columna] == -1:
                continue
            contador = sum(1 for i in range(-1, 2) for j in range(-1, 2) 
                           if 0 <= fila + i < filas and 0 <= columna + j < columnas 
                           and tablero[fila + i][columna + j] == -1)
            tablero[fila][columna] = contador

# Función revelar celda al hacer clic derecho
def revelar_celda(fila, columna):
    if botones[fila][columna]["text"] == "🚩":
        return  # No permitir revelar una celda con bandera

    valor = tablero[fila][columna]
    if valor == -1:
        for f in range(filas):
            for c in range(columnas):
                if tablero[f][c] == -1:
                    botones[f][c].config(text="💣", fg="red")
                botones[f][c].config(state="disabled")  # Desactivar todos los botones
        game_over_label.config(text="GAME OVER", fg="red")  # Mensaje de derrota
    else:
        botones[fila][columna].config(text=str(valor), fg="black")
        contador_var.set(contador_var.get() + 1)
        botones[fila][columna].config(state="disabled")  # Desactivar el botón presionado
        verificar_victoria()  # Comprobar si el jugador ha ganado

# Verificar Victoria
def verificar_victoria():
    # Calcular cuántas celdas sin minas han sido reveladas
    celdas_descubiertas = sum(1 for fila in range(filas) for columna in range(columnas) 
                              if botones[fila][columna]["state"] == "disabled" and tablero[fila][columna] != -1)
    total_celdas_seguras = filas * columnas - num_minas  # Total de celdas sin minas

    if celdas_descubiertas == total_celdas_seguras:
        game_over_label.config(text="¡Ganaste! 🎉", fg="green")  # Mensaje de victoria
        for fila in range(filas):
            for columna in range(columnas):
                botones[fila][columna].config(state="disabled")  # Bloquear botones
                
# Función para reiniciar el juego
def reiniciar_juego():
    contador_var.set(0)  # Reiniciar el contador
    game_over_label.config(text="")  # Limpiar el mensaje de Game Over
    generar_tablero()  # Generar nuevo tablero
    for fila in range(filas):
        for columna in range(columnas):
            botones[fila][columna].config(text="", fg="black", state="normal")  # Limpiar botones

# Crear los botones en la cuadrícula

for fila in range(filas):
    fila_botones = []
    for columna in range(columnas):
        boton = tk.Button(marco_juego, width=2, height=1, text="", font=("Arial", 12),
                          command=lambda f=fila, c=columna: revelar_celda(f, c))
        boton.bind("<Button-3>", lambda event, f=fila, c=columna: alternar_bandera(event, f, c))  # Clic derecho
        boton.grid(row=fila, column=columna)
        fila_botones.append(boton)
    botones.append(fila_botones)
    
# Crear funcion de banderas con click derecho
def alternar_bandera(event, fila, columna):
    boton = botones[fila][columna]
    if boton["text"] == "🚩":
        boton.config(text="")  # Quitar bandera
    elif boton["state"] == "normal":  # Solo marcar si la celda no ha sido revelada
        boton.config(text="🚩", fg="blue")  # Colocar bandera

# Inicializar el juego
generar_tablero()

ventana.mainloop()
