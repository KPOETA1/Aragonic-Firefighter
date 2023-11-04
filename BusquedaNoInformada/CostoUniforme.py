#from world import world
import copy, time

# Diccionario de acciones con sus respectivos desplazamientos
acciones = {
    "arriba": (-1, 0),
    "abajo": (1, 0),
    "izquierda": (0, -1),
    "derecha": (0, 1)
}


def get_position(nodo, x):
    '''
    Retorna la posición de un elemento en el mundo.
    Args:
        nodo (Nodo): Nodo que contiene el mundo.
        x (int): Elemento a buscar.
    Returns:
        tuple: Posición del elemento.
    '''
    for i in range(10):
        for j in range(10):
            if nodo[i][j] == x:
                return (i, j)


def apply_action_node(nodo, action):
    """
    Aplica una acción a un nodo y retorna el nodo resultante.
    Args:
        action (str): Acción a aplicar.
        nodo (Nodo): Nodo al que se le aplicará la acción.
    Returns:
        Nodo: Nodo resultante de aplicar la acción.
    """
    # Obtener el mundo del nodo
    world = nodo.world
    # Crear una copia del mundo para no modificar el original
    new_world = copy.deepcopy(world)
    # Obtener la acción a aplicar
    accion = acciones[action]
    # Obtener la posicion del bombero
    posicion = nodo.position
    # Obtener la posición a la que se moverá el bombero
    posicion = (posicion[0] + accion[0], posicion[1] + accion[1])

    # Verifica si la posición a la que se moverá el bombero es un fuego
    if new_world[posicion[0], posicion[1]] == 2 and nodo.agua > 0:
        new_world[posicion[0], posicion[1]] = 0
        return Nodo(new_world, nodo, action, nodo.cubo, nodo.agua - 1, posicion, fire=nodo.fire - 1, # COSTO : COSTO_MOVIMIENTO_1LT O COSTO_MOVIMIENTO_2LT
                    costo=nodo.costo + 1 + nodo.agua)
    # Verifica si la posición a la que se moverá el bombero es un cubo de 1 litro
    elif new_world[posicion[0], posicion[1]] == 3 and nodo.cubo == 0:
        new_world[posicion[0], posicion[1]] = 0
        return Nodo(new_world, nodo, action, nodo.cubo + 1, nodo.agua, posicion, fire=nodo.fire, costo=nodo.costo + 1) # COSTO_MOVIMIENTO
    # Verifica si la posición a la que se moverá el bombero es un cubo de 2 litros
    elif new_world[posicion[0], posicion[1]] == 4 and nodo.cubo == 0:
        new_world[posicion[0], posicion[1]] = 0
        return Nodo(new_world, nodo, action, nodo.cubo + 2, nodo.agua, posicion, fire=nodo.fire, costo=nodo.costo + 1) # COSTO_MOVIMIENTO
    # Verifica si la posición a la que se moverá el bombero es el hidrante
    elif new_world[posicion[0], posicion[1]] == 6 and nodo.agua == 0:
        return Nodo(new_world, nodo, action, nodo.cubo, nodo.agua + nodo.cubo, posicion, fire=nodo.fire, # COSTO_MOVIMIENTO_CUBO
                    costo=nodo.costo + 1)
    # En caso de que no sea ninguno de los anteriores, solo se mueve
    else:
        return Nodo(new_world, nodo, action, nodo.cubo, nodo.agua, posicion, fire=nodo.fire, # COSTO_MOVIMIENTO O COSTO_MOVIMIENTO_CUBO
                    costo=nodo.costo + 1 + nodo.agua)


def can_go_back(nodo):
    """
    Verifica si el bombero puede regresar a la posición anterior.
    Args:
        nodo (Nodo): Nodo actual.
    Returns:
        bool: True si puede regresar, False en caso contrario.
    """

    if nodo.padre.cubo != nodo.cubo:  # Si se recogió un cubo
        return True
    elif nodo.padre.agua != nodo.agua:  # Si se recogió agua
        return True
    elif nodo.padre.fire != nodo.fire:  # Si se apagó un fuego
        return True
    else:
        return False


def expand_node(nodo):
    """
    Expande un nodo y retorna sus hijos.
    Args:
        nodo (Nodo): Nodo a expandir.
    Returns:
        list: Lista de nodos hijos.
    """
    # Crear una lista de nodos hijos
    hijos = []
    acciones_posibles = []
    # Verificar si se puede ir arriba
    if nodo.position[0] - 1 >= 0:
        if nodo.world[nodo.position[0] - 1, nodo.position[1]] != 1:
            if nodo.world[nodo.position[0] - 1, nodo.position[1]] != 2 or nodo.agua > 0:
                if nodo.accion != "abajo" or can_go_back(nodo):
                    acciones_posibles.append("arriba")
    # Verificar si se puede ir abajo
    if nodo.position[0] + 1 < 10:
        if nodo.world[nodo.position[0] + 1, nodo.position[1]] != 1:
            if nodo.world[nodo.position[0] + 1, nodo.position[1]] != 2 or nodo.agua > 0:
                if nodo.accion != "arriba" or can_go_back(nodo):
                    acciones_posibles.append("abajo")
    # Verificar si se puede ir a la izquierda
    if nodo.position[1] - 1 >= 0:
        if nodo.world[nodo.position[0], nodo.position[1] - 1] != 1:
            if nodo.world[nodo.position[0], nodo.position[1] - 1] != 2 or nodo.agua > 0:
                if nodo.accion != "derecha" or can_go_back(nodo):
                    acciones_posibles.append("izquierda")
    # Verificar si se puede ir a la derecha
    if nodo.position[1] + 1 < 10:
        if nodo.world[nodo.position[0], nodo.position[1] + 1] != 1:
            if nodo.world[nodo.position[0], nodo.position[1] + 1] != 2 or nodo.agua > 0:
                if nodo.accion != "izquierda" or can_go_back(nodo):
                    acciones_posibles.append("derecha")

    # Iterar sobre las acciones
    for accion in acciones_posibles:
        # Aplicar la acción al nodo
        hijo = apply_action_node(nodo, accion)
        # Agregar el nodo hijo a la lista de hijos
        hijos.append(hijo)
    # Retornar la lista de hijos
    return hijos


# Crear la clase nodo para el algoritmo de busqueda por Amplitud
class Nodo:
    """
    Constructor de la clase Nodo.

    Args:
        world (numpy.ndarray): Matriz de 10x10 que representa el mundo.
        padre (Nodo): Nodo padre del nodo actual.
        accion (str): Acción que se tomó para llegar al nodo actual.
    """

    def __init__(self, world, padre=None, accion=None, cubo=0, agua=0, position=None, fire=2, costo=0):
        self.world = world
        self.padre = padre
        self.accion = accion
        self.cubo = cubo
        self.agua = agua
        self.position = position
        self.fire = fire
        self.costo = costo


def solve_costo_uniforme(world):
    # Inicializa un temporizador
    timer_start = time.time()
    # Crear el nodo inicial
    nodoInicial = Nodo(world, cubo=0, agua=0, position=get_position(world, 5), fire=2)
    # Crear una lista de nodos por expandir (cola)
    nodos_por_expandir = [nodoInicial]
    # Contador de nodos expandidos
    contador = 0
    # Variable para determinaar si el problema fue resuelto
    solved = False
    while not solved:
        # Verificar el primer nodo de la lista de nodos por expandir
        nodo = nodos_por_expandir[0]
        # Verificar si el nodo es una meta
        if nodo.fire == 0:
            solved = True
        else:
            # Expandir el nodo
            hijos = expand_node(nodo)
            # Agregar los hijos a la lista de nodos por expandir
            nodos_por_expandir = nodos_por_expandir[1:] + hijos
            # Ordenar la lista de nodos por expandir de forma ascendente por el costo
            nodos_por_expandir.sort(key=lambda x: x.costo)
            # Incremento del contador
            contador += 1

    costo = nodo.costo

    acciones = []
    path = []  # camino recorrido
    maps = []  # los mapas de cada nodo

    while nodo.padre is not None:
        path.append(nodo.position)
        maps.append(nodo.world)
        acciones.append(nodo.accion)
        nodo = nodo.padre

    path.append(nodo.position)
    path.reverse()  # Se invierte el camino para que quede en el orden correcto

    maps.append(nodo.world)
    maps.reverse()  # Se invierte el camino para que quede en el orden correcto

    acciones.append(nodo.accion)
    acciones.reverse()  # Se invierte el camino para que quede en el orden correcto

    timer_finish = time.time()
    tiempo = round(timer_finish - timer_start, 5)
    # Retornar el nodo meta
    return nodo, path, maps, acciones, contador, tiempo, costo

# if __name__ == "__main__":
#     nodo, path, maps, acciones = solve_amplitud(world)
#     print(nodo.position)
#     print(nodo.fire)
#     print(path)
#     print(maps[-1])
#     print(acciones)