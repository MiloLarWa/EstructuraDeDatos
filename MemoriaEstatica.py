import tkinter as tk
from tkinter import simpledialog

root = tk.Tk()
root.withdraw()

calificaciones = [0] * 5

for i in range(5):
    valor = simpledialog.askinteger("Entrada", "Ingrese la calificación:")
    
    if valor is not None:
        calificaciones[i] = valor
    else:
        calificaciones[i] = 0