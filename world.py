# El Bombero Inteligente. Considere el problema del bombero inteligente que consiste en un
# agente que se encarga de apagar dos puntos de fuego en un mundo donde se cuenta con dos cubetas (una
# de 1 litro y la otra de 2) y un solo hidrante. Se puede suponer que cada punto de fuego se apaga con un
# litro de agua. El bombero debe inicialmente encontrar una de las dos cubetas, luego dirigirse al hidrante,
# y finalmente proceder a encontrar los puntos de fuego. En caso de que haya tomado la cubeta de un solo
# litro deberá recargarla nuevamente. El bombero no puede tomar las dos cubetas.
# Tenga en cuenta que si el agente pasa sobre un punto de fuego teniendo agua, éste se apagará
# automáticamente, es decir, no se puede decidir entre utilizar el agua o conservarla. Además, el agente
# no puede pasar por un punto de fuego si no lleva agua. En cada exploración el agente podrá realizar
# desplazamientos simples como moverse arriba, abajo, izquierda, y derecha. El costo de cada movimiento
# realizado por el agente cuando no lleva ningún suministro de agua es de 1. Llevar una cubeta vacía no tiene
# costo adicional. Sin embargo, cuando se lleva agua en una cubeta, el costo de cada movimiento se aumenta
# en 1 por cada litro de agua. Por lo tanto, si el agente lleva la cubeta de 1 litro con agua, el costo de cada
# movimiento será de 2, si lleva la cubeta de 2 litros con un litro de agua el costo de cada movimiento será
# de 2, y si lleva la cubeta de 2 litros con dos litros de agua el costo será de 3. Al llegar a un hidrante las
# cubetas se llenan automáticamente. Sin embargo, la cubeta de dos litros no se vuelve a recargar si se
# pasa nuevamente por el hidrante. La búsqueda termina cuando se apaguen los dos puntos de fuego.
# Considere la siguiente abstracción del mundo del bombero inteligente representado por medio de una
# matriz de 10x10.

# La información del mundo se representa por medio de los siguientes números:
# • 0 si es una casilla libre
# • 1 si es un obstáculo
# • 2 si es un punto de fuego
# • 3 si es la cubeta de un litro
# • 4 si es la cubeta de dos litros
# • 5 si es el punto de inicio
# • 6 si es el hidrante
# Por ejemplo, el mundo mostrado en la figura se representa mediante la matriz:
# 0 0 0 1 1 0 0 0 0 0
# 0 1 0 1 1 0 1 1 1 1
# 0 1 0 2 0 0 0 0 0 1
# 0 1 0 1 1 1 1 1 0 0
# 5 0 0 6 4 0 0 1 0 1
# 0 1 1 1 1 1 0 1 0 1
# 3 0 0 0 2 0 0 1 0 1
# 0 1 0 1 1 1 1 1 0 1
# 0 1 0 0 0 0 0 1 0 1
# 0 1 0 1 1 1 0 0 0 0
# el archivo del mundo se llama prueba1.txt

import tkinter as tk  

class World:
    def __init__(self, filename, heuristic=None):
        self.load_world(filename)

    def load_world(self, filename):
        try:
            with open(filename, "r") as file:
                # Leer el contenido del archivo y crear la matriz del mundo
                self.grid = [list(map(int, line.strip().split())) for line in file.readlines()]
                self.rows = len(self.grid)
                self.cols = len(self.grid[0])
        except FileNotFoundError:
            print(f"El archivo '{filename}' no se encontró.")

    def display(self):
        # Mostrar el mundo gráficamente con la biblioteca Tkinter
        # ventana
        root = tk.Tk()
        root.title("Bombero Araganico")

        # canvas
        canvas = tk.Canvas(root, width=500, height=500)
        canvas.pack()

        # dibujar el mundo
        colors = {
            0: "white",
            1: "gray",
            2: "orange",
            3: "#DC143C",
            4: "red",
            5: "green",
            6: "blue"
        }

        for row in range(self.rows):
            for col in range(self.cols):
                cell_value = self.grid[row][col]
                color = colors.get(cell_value, "white")
                x1 , y1 = col * 50, row * 50
                x2, y2 = x1 + 50, y1 + 50
                canvas.create_rectangle(x1, y1, x2, y2, fill=color)
        
        # iniciar la interfaz gráfica
        root.mainloop()

    def is_goal_state(self):
        # Verificar si se han apagado ambos puntos de fuego
        fire_count = sum([row.count(2) for row in self.grid]) # la suma de todos los 2 en el grid

        return fire_count == 0

    def get_actions(self):
        # Obtener las acciones posibles para el bombero
        actions = []

        # Obtener la posición actual del bombero
        for row in range(self.rows):
            for col in range(self.cols):
                if self.grid[row][col] == 5:
                    current_row, current_col = row, col

        # Posibles movientos del aragancito
        possibles_moves = [(0, 1), (0, -1), (1, 0), (-1, 0)]

        for move in possibles_moves:
            new_row = current_row + move[0]
            new_col = current_col + move[1]

            # Es valida la posición si no se sale del mundo y no hay un obstaculo
            if 0 <= new_row < self.rows and 0 <= new_col < self.cols:
                cell_value = self.grid[new_row][new_col]

                if cell_value == 0 or cell_value == 2:  # Casilla libre o punto de fuego
                    actions.append((new_row, new_col))

        return actions
                
if __name__ == "__main__":
    world = World("prueba1.txt")
    world.display()