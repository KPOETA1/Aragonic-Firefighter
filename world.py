import numpy as np

# Crear una matriz de 10x10 inicializada con ceros en numpy
matriz = np.zeros((10, 10), dtype=int)

# Leer el archivo prueba1.txt y guardar cada línea en la matriz
with open("Prueba1.txt", "r") as file:
    for fila, linea in enumerate(file):
        valores = linea.split()  # Dividir la línea en valores separados por espacios
        for columna, valor in enumerate(valores):
            matriz[fila, columna] = int(valor)

# Guardar la matriz en la variable world
world = matriz