import tkinter as tk 
from world import World
import heuristic
import animations

# Función para iniciar la búsqueda y mostrar la animación
def start_search(algorithm):
    # Cargar el mundo desde un archivo de texto (puedes implementar esta función en World)
    world = World("prueba1.txt")

    # Seleccionar el algoritmo de búsqueda
    if algorithm == "informada":
        result = heuristic.breadth_first_search(world)
    elif algorithm == "no_informada":
        result = heuristic.uniform_cost_search(world)
    else:
        return

    # Mostrar la animación de la solución
    animations.animate_solution(world, result)

# Crear la interfaz gráfica
root = tk.Tk()
root.title("Bombero Inteligente")

# Botones para seleccionar el algoritmo de búsqueda
algorithm_label = tk.Label(root, text="Selecciona el algoritmo:")
algorithm_label.pack()

algorithms = ['informada', 'no_informada']
for algorithm in algorithms:
    button = tk.Button(root, text=algorithm, command=lambda algo=algorithm: start_search(algo))
    button.pack()

# Iniciar la interfaz gráfica
root.mainloop()