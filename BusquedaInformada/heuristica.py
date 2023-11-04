COSTO_MOVIMIENTO = 1
COSTO_MOVIMIENTO_CUBO = 1
COSTO_MOVIMIENTO_1L = 2
COSTO_MOVIMIENTO_2L = 3

# Diccionario de acciones con sus respectivos desplazamientos
acciones = {
    "arriba": (-1, 0),
    "abajo": (1, 0),
    "izquierda": (0, -1),
    "derecha": (0, 1)
}

def get_fuego_positions(nodo):
    '''
    Retorna la posición de los fuegos en el mundo.
    Args:
        nodo (Nodo): Nodo del mundo.
    Returns:
        list: Posición de los fuegos.
    '''
    fuego_positions = []
    for i in range(10):
        for j in range(10):
            if nodo.world[i][j] == 2:
                fuego_positions.append((i, j))
    return fuego_positions

def get_cubo_ol_positions(nodo):
    '''
    Retorna la posición del cubo de 1 litro en el mundo.
    Args:
        nodo (Nodo): Nodo del mundo.
    Returns:
        list: Posición de los cubos de 1 litro.
    '''
    for i in range(10):
        for j in range(10):
            if nodo.world[i][j] == 3:
                return (i, j)

def get_cubo_tl_positions(nodo):
    '''
    Retorna la posición del cubo de 2 litros en el mundo.
    Args:
        nodo (Nodo): Nodo del mundo.
    Returns:
        list: Posición de los cubos de 2 litros.
    '''
    for i in range(10):
        for j in range(10):
            if nodo.world[i][j] == 4:
                return (i, j)

def get_hidrante_position(nodo):
    '''
    Retorna la posición del hidrante en el mundo.
    Args:
        nodo (Nodo): Nodo del mundo.
    Returns:
        tuple: Posición del hidrante.
    '''
    for i in range(10):
        for j in range(10):
            if nodo.world[i][j] == 6:
                return (i, j)
            
def distancia_manhattan(pos1, pos2):
    '''
    Retorna la distancia de Manhattan entre dos posiciones.
    Args:
        pos1 (tuple): Posición 1.
        pos2 (tuple): Posición 2.
    Returns:
        int: Distancia de Manhattan.
    '''
    return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])
            

def heuristic(nodo, accion):
    '''
    Retorna la heurística de un nodo.
    Args:
        nodo (Nodo): Nodo del mundo.
        accion (str): Acción a aplicar.
    Returns:
        int: Valor de la heurística en el nodo.
    '''
    if accion is not None:
        bombero_position = (nodo.position[0] + acciones[accion][0], nodo.position[1] + acciones[accion][1])
    else: 
        bombero_position = nodo.position
    
    fuego_positions = get_fuego_positions(nodo)
    cubo_ol_positions = get_cubo_ol_positions(nodo)
    cubo_tl_positions = get_cubo_tl_positions(nodo)
    hidrante_position = get_hidrante_position(nodo)
    heuristica1 = 0
    heuristica2 = 0

    # Calcular la distancia entre el bombero y el cubo de 1 litro
    if nodo.cubo == 0:
        # Caso 1: El bombero no tiene cubo y se escoge el de 1 litro
        heuristica1 += distancia_manhattan(bombero_position, cubo_ol_positions) * COSTO_MOVIMIENTO
        heuristica1 += distancia_manhattan(cubo_ol_positions, hidrante_position) * COSTO_MOVIMIENTO_CUBO
        if distancia_manhattan(hidrante_position, fuego_positions[0]) < distancia_manhattan(hidrante_position, fuego_positions[1]):
            heuristica1 += (distancia_manhattan(hidrante_position, fuego_positions[0])) * COSTO_MOVIMIENTO_2L #<--- Aquí se debe cambiar el costo de movimiento entre fuego e hidrante (ES EL COSTO DE LA DISTANCIA ENTRE EL HIDRANTE Y EL FUUEGO MAS CERCANO DE IDA Y VUELTA)
            heuristica1 += (distancia_manhattan(hidrante_position, fuego_positions[1])) * COSTO_MOVIMIENTO_1L
        else:
            heuristica1 += (distancia_manhattan(hidrante_position, fuego_positions[1])) * COSTO_MOVIMIENTO_2L #<--- Aquí se debe cambiar el costo de movimiento entre fuego e hidrante (ES EL COSTO DE LA DISTANCIA ENTRE EL HIDRANTE Y EL FUUEGO MAS CERCANO DE IDA Y VUELTA)
            heuristica1 += (distancia_manhattan(hidrante_position, fuego_positions[0])) * COSTO_MOVIMIENTO_1L
        
        #Caso 2: El bombero no tiene cubo y se escoge el de 2 litros
        heuristica2 += distancia_manhattan(bombero_position, cubo_tl_positions)
        heuristica2 += distancia_manhattan(cubo_tl_positions, hidrante_position)
        if distancia_manhattan(hidrante_position, fuego_positions[0]) < distancia_manhattan(hidrante_position, fuego_positions[1]):
            heuristica2 += (distancia_manhattan(hidrante_position, fuego_positions[0])) * COSTO_MOVIMIENTO_2L
            heuristica2 += (distancia_manhattan(fuego_positions[0], fuego_positions[1])) * COSTO_MOVIMIENTO_1L
        else:
            heuristica2 += (distancia_manhattan(hidrante_position, fuego_positions[1])) * COSTO_MOVIMIENTO_2L
            heuristica2 += (distancia_manhattan(fuego_positions[1], fuego_positions[0])) * COSTO_MOVIMIENTO_1L
        return min(heuristica1, heuristica2)
    elif nodo.cubo == 1:
        # Sin agua y con 2 fuegos :(
        if nodo.agua == 0 and nodo.fire == 2:
            heuristica1 += distancia_manhattan(bombero_position, hidrante_position)
            if distancia_manhattan(hidrante_position, fuego_positions[0]) < distancia_manhattan(hidrante_position, fuego_positions[1]):
                heuristica1 += (distancia_manhattan(hidrante_position, fuego_positions[0])) * COSTO_MOVIMIENTO_2L #<--- Aquí se debe cambiar el costo de movimiento entre fuego e hidrante (ES EL COSTO DE LA DISTANCIA ENTRE EL HIDRANTE Y EL FUUEGO MAS CERCANO DE IDA Y VUELTA)
                heuristica1 += (distancia_manhattan(hidrante_position, fuego_positions[1])) * COSTO_MOVIMIENTO_1L
            else:
                heuristica1 += (distancia_manhattan(hidrante_position, fuego_positions[1])) * COSTO_MOVIMIENTO_2L #<--- Aquí se debe cambiar el costo de movimiento entre fuego e hidrante (ES EL COSTO DE LA DISTANCIA ENTRE EL HIDRANTE Y EL FUUEGO MAS CERCANO DE IDA Y VUELTA)
                heuristica1 += (distancia_manhattan(hidrante_position, fuego_positions[0])) * COSTO_MOVIMIENTO_1L
        # Con agua y con 2 fuegos :)
        elif nodo.agua > 0 and nodo.fire == 2:
            if distancia_manhattan(bombero_position, fuego_positions[0]) < distancia_manhattan(bombero_position, fuego_positions[1]):
                heuristica1 += (distancia_manhattan(bombero_position, fuego_positions[0])) * COSTO_MOVIMIENTO_1L
                heuristica1 += (distancia_manhattan(fuego_positions[0], hidrante_position)) * COSTO_MOVIMIENTO_CUBO
                heuristica1 += (distancia_manhattan(hidrante_position, fuego_positions[1])) * COSTO_MOVIMIENTO_1L
            else:
                heuristica1 += (distancia_manhattan(bombero_position, fuego_positions[1])) * COSTO_MOVIMIENTO_1L
                heuristica1 += (distancia_manhattan(fuego_positions[1], hidrante_position)) * COSTO_MOVIMIENTO_CUBO
                heuristica1 += (distancia_manhattan(hidrante_position, fuego_positions[0])) * COSTO_MOVIMIENTO_1L
        # Sin agua y con 1 fuego :(
        elif nodo.agua == 0 and nodo.fire == 1:
            heuristica1 += distancia_manhattan(bombero_position, hidrante_position) * COSTO_MOVIMIENTO_CUBO
            heuristica1 += distancia_manhattan(hidrante_position, fuego_positions[0]) * COSTO_MOVIMIENTO_1L
        # Con agua y con 1 fuego :)
        elif nodo.agua > 0 and nodo.fire == 1:
            heuristica1 += distancia_manhattan(bombero_position, fuego_positions[0]) * COSTO_MOVIMIENTO_1L
        return heuristica1
    elif nodo.cubo == 2:
        # Sin agua y con 2 fuegos :(
        if nodo.agua == 0 and nodo.fire == 2:
            heuristica2 += distancia_manhattan(bombero_position, hidrante_position) * COSTO_MOVIMIENTO_CUBO
            if distancia_manhattan(hidrante_position, fuego_positions[0]) < distancia_manhattan(hidrante_position, fuego_positions[1]):
                heuristica2 += (distancia_manhattan(hidrante_position, fuego_positions[0])) * COSTO_MOVIMIENTO_2L
                heuristica2 += (distancia_manhattan(fuego_positions[0], fuego_positions[1])) * COSTO_MOVIMIENTO_1L
            else:
                heuristica2 += (distancia_manhattan(hidrante_position, fuego_positions[1])) * COSTO_MOVIMIENTO_2L
                heuristica2 += (distancia_manhattan(fuego_positions[0], fuego_positions[0])) * COSTO_MOVIMIENTO_1L
        # Con agua y con 2 fuegos :)
        elif nodo.agua == 2 and nodo.fire == 2:
            if distancia_manhattan(bombero_position, fuego_positions[0]) < distancia_manhattan(bombero_position, fuego_positions[1]):
                heuristica2 += (distancia_manhattan(bombero_position, fuego_positions[0])) * COSTO_MOVIMIENTO_2L
                heuristica2 += (distancia_manhattan(fuego_positions[0], fuego_positions[1])) * COSTO_MOVIMIENTO_1L
            else:
                heuristica2 += (distancia_manhattan(bombero_position, fuego_positions[1])) * COSTO_MOVIMIENTO_2L
                heuristica2 += (distancia_manhattan(fuego_positions[1], fuego_positions[0])) * COSTO_MOVIMIENTO_1L
        # Con fuego y sin agua :(
        else:
            heuristica2 += (distancia_manhattan(bombero_position, fuego_positions[0])) * COSTO_MOVIMIENTO_1L
        return heuristica2