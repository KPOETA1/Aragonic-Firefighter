import pygame as pyg, sys
from pygame.locals import *


class Button:
    def __init__(self, x, y, juego, texto):
        self.screen = juego.screen
        self.screen_rect = self.screen.get_rect()
        self.width, self.height = 200, 50
        self.color = '#D7621A'
        self.textoColor = (255, 255, 255)
        self.font = pyg.font.SysFont('Pixels', 50)
        self.rect = pyg.Rect(x, y, self.width, self.height)
        self.prepara_texto(texto)

    def prepara_texto(self, texto):
        self.texto_image = self.font.render(texto, True, self.textoColor, None)
        self.texto_image_rect = self.texto_image.get_rect()

    def dibuja_boton(self):
        self.screen.fill(self.color, self.rect)
        self.screen.blit(self.texto_image, ((self.rect.x + self.width)/2 + 50, self.rect.y))


class World:
    def __init__(self, filename, heuristic=None):
        pyg.init()

        # ventana
        self.screen = pyg.display.set_mode((500, 500))
        pyg.display.set_caption('Bombero Araganico')
        self.icon = pyg.image.load('Sprites/bomberoicon.png')
        self.color = '#2F2C2B'
        pyg.display.set_icon(self.icon)
        self.load_world(filename)
        self.play_boton = Button((250 - 100), (250 - 25), self, "Play")
        self.gameOn = False

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

        # iniciar la interfaz gráfica
        while True:
            for event in pyg.event.get():
                if event.type == QUIT:
                    pyg.quit()
                    sys.exit()
                elif event.type == pyg.MOUSEBUTTONDOWN:
                    mousePos = pyg.mouse.get_pos()
                    self.checaBoton(mousePos)

            if self.gameOn:
                self.cargaMundo()
            if not self.gameOn:
                self.screen.fill(self.color)
                self.play_boton.dibuja_boton()
            pyg.display.update()

    def is_goal_state(self):
        # Verificar si se han apagado ambos puntos de fuego
        fire_count = sum([row.count(2) for row in self.grid])  # la suma de todos los 2 en el grid

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

    def cargaMundo(self):
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
                x1, y1 = col * 50, row * 50
                x2, y2 = x1 + 50, y1 + 50
                pyg.draw.rect(self.screen, color, (x1, y1, x2, y2))
                pyg.draw.line(self.screen, (0, 0, 0), (x1, y1), (x2, y1), 1)
                pyg.draw.line(self.screen, (0, 0, 0), (x1, y1), (x1, y2), 1)
                if color == 'green':
                    bombero = pyg.image.load('Sprites/bomberoicon.png')
                    self.screen.blit(bombero, (x1, y1))

    def checaBoton(self, mousePos):
        self.botonP = self.play_boton.rect.collidepoint(mousePos)
        if self.botonP and not self.gameOn:
            self.gameOn = True


if __name__ == "__main__":
    world = World("prueba1.txt")
    world.display()
