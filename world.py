import pygame as pyg, sys, numpy as np
from pygame.locals import *


import BusquedaNoInformada.Amplitud
from BusquedaNoInformada.Amplitud import *

import BusquedaNoInformada.CostoUniforme
from BusquedaNoInformada.CostoUniforme import *

import BusquedaNoInformada.Profundidad
from BusquedaNoInformada.Profundidad import *


class Button:
    def __init__(self, x, y, juego, texto):
        self.screen = juego.screen
        self.screen_rect = self.screen.get_rect()
        self.width, self.height = 210, 50
        self.color = '#D7621A'
        self.textoColor = (255, 255, 255)
        self.font = pyg.font.Font("./Fonts/Pixels.ttf", 50)
        self.rect = pyg.Rect(x, y, self.width, self.height)
        self.prepara_texto(texto)

    def prepara_texto(self, texto):
        self.texto_image = self.font.render(texto, True, self.textoColor, None)
        self.texto_image_rect = self.texto_image.get_rect()

    def set_coord(self, set_x, set_y):
        self.rect.x = set_x
        self.rect.y = set_y

    def dibuja_boton(self):
        self.screen.fill(self.color, self.rect)
        self.screen.blit(self.texto_image, ((self.width - self.texto_image_rect.width) / 2 + self.rect.x, self.rect.y))


class World:
    def __init__(self, filename):
        pyg.init()
        pyg.mixer.init()

        #Bombero
        self.bombero_position = (0, 0) # Posición inicial del bombero

        # ventana
        self.screen = pyg.display.set_mode((500, 500))
        pyg.display.set_caption('Bombero Araganico')
        self.icon = pyg.image.load('Sprites/bomberoicon.png')
        self.color = '#2F2C2B'
        pyg.display.set_icon(self.icon)
        pyg.mixer.music.load('Music/Jeremy Blake - PowerUp!.wav')
        pyg.mixer.music.play(-1)
        pyg.mixer.music.set_volume(0.5)
        self.button_sound = pyg.mixer.Sound('Music/button_clic.wav')
        self.bombero = pyg.image.load('./Sprites/bomberoicon.png')
        self.filename = filename
        self.matrix = filename
        self.matrix_generator()
        self.load_world(filename)
        self.carga_mundo_boton = Button((250 - 105), 155, self, "Cargar Mundo")
        self.informada_boton = Button((250 - 105), 225, self, "Informada")
        self.avara_boton = Button(145, 170, self, "Avara")
        self.A_star_boton = Button(145, 230, self, "A*")
        self.no_informada_boton = Button(145, 295, self, "No Informada")
        self.amplitud_boton = Button(145, 165, self, "Amplitud")
        self.costo_uniforme_boton = Button(145, 225, self, "Costo Uniforme")
        self.profundidad_boton = Button(145, 285, self, "Profundidad")
        self.menu_boton = Button(0, 0, self, "Menu")
        self.game_on = 'Menu'

    def load_world(self, filename):
        try:
            with open(filename, "r") as file:
                # Leer el contenido del archivo y crear la matriz del mundo
                self.grid = [list(map(int, line.strip().split())) for line in file.readlines()]
                self.rows = len(self.grid)
                self.cols = len(self.grid[0])
        except FileNotFoundError:
            print(f"El archivo '{filename}' no se encontró.")

    #   actualizacion posicion del bombero
    def move_bomber(self, path, fire_count):
        self.load_world(self.filename)
        balde = False
        for next_position in path:
            self.bombero_position = next_position

            self.screen.fill(self.color)
            cell_value = self.grid[next_position[0]][next_position[1]]
            if cell_value == 2 or cell_value == 3 and not balde or cell_value == 4 and not balde:
                if cell_value == 2:
                    fire_count -= 1
                if cell_value == 4 or cell_value == 3:
                    balde = True

                self.grid[next_position[0]][next_position[1]] = 0
            if fire_count == 0:
                self.game_on = 'Menu'
                break

            self.carga_mundo()
            pyg.display.update()

            pyg.time.delay(250)
            # print("posicion bombero", self.bombero_position)

    def display(self):

        # iniciar la interfaz gráfica
        while True:
            for event in pyg.event.get():
                if event.type == QUIT:
                    pyg.quit()
                    sys.exit()
                elif event.type == pyg.MOUSEBUTTONDOWN:
                    mouse_pos = pyg.mouse.get_pos()
                    self.checa_boton(mouse_pos)

            if self.game_on == 'Carga mundo':
                self.screen.fill(self.color)
                self.carga_mundo()
            if self.game_on == 'Menu':
                self.screen.fill(self.color)
                self.carga_mundo_boton.dibuja_boton()
                self.informada_boton.dibuja_boton()
                self.no_informada_boton.dibuja_boton()
            if self.game_on == 'No Informada':
                self.screen.fill(self.color)
                self.amplitud_boton.dibuja_boton()
                self.costo_uniforme_boton.dibuja_boton()
                self.profundidad_boton.dibuja_boton()
                self.menu_boton.set_coord(145, 345)
                self.menu_boton.dibuja_boton()
            if self.game_on == 'Informada':
                self.screen.fill(self.color)
                self.avara_boton.dibuja_boton()
                self.A_star_boton.dibuja_boton()
                self.menu_boton.set_coord(145, 290)
                self.menu_boton.dibuja_boton()
            if self.game_on == 'Amplitud':
                nodo, path, maps, acciones = BusquedaNoInformada.Amplitud.solve_amplitud(self.matrix)
                self.move_bomber(path, nodo.fire)
            if self.game_on == 'Costo Uniforme':
                nodo, path, maps, acciones = BusquedaNoInformada.CostoUniforme.solve_costo_uniforme(self.matrix)
                self.move_bomber(path, nodo.fire)
            if self.game_on == 'Profundidad':
                nodo, path, maps, acciones = BusquedaNoInformada.Profundidad.solve_profundidad(self.matrix)
                self.move_bomber(path, nodo.fire)



            pyg.display.update()

    def carga_mundo(self):
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
                # dibujar el bombero en movimiento
                if (row, col) == self.bombero_position:
                    self.bombero = pyg.transform.scale(self.bombero, (50, 50))
                    self.screen.blit(self.bombero, (x1, y1))

    def matrix_generator(self):
        matriz = np.zeros((10, 10), dtype=int)

        with open(self.filename) as file:
            for fila, linea in enumerate(file):
                valores = linea.split()
                for columna, valor in enumerate(valores):
                    matriz[fila, columna] = int(valor)
        self.matrix = matriz

    def checa_boton(self, mouse_pos):
        self.boton_c = self.carga_mundo_boton.rect.collidepoint(mouse_pos)
        self.boton_inf = self.informada_boton.rect.collidepoint(mouse_pos)
        self.boton_ninf = self.no_informada_boton.rect.collidepoint(mouse_pos)
        self.boton_m = self.menu_boton.rect.collidepoint(mouse_pos)
        self.boton_amp = self.amplitud_boton.rect.collidepoint(mouse_pos)
        self.boton_cuni = self.costo_uniforme_boton.rect.collidepoint(mouse_pos)
        self.boton_prof = self.profundidad_boton.rect.collidepoint(mouse_pos)
        if self.boton_c and self.game_on == 'Menu':
            self.game_on = 'Carga mundo'
            self.button_sound.play()
        elif self.boton_inf and self.game_on == 'Menu':
            self.game_on = 'Informada'
            self.button_sound.play()
        elif self.boton_ninf and self.game_on == 'Menu':
            self.game_on = 'No Informada'
            self.button_sound.play()
        elif self.boton_m and (self.game_on == 'Informada' or self.game_on == 'No Informada'):
            self.game_on = 'Menu'
            self.button_sound.play()
        elif self.boton_amp and self.game_on == 'No Informada': # Mover al bombero
            self.game_on = 'Amplitud'
            self.button_sound.play()
        elif self.boton_cuni and self.game_on == 'No Informada':
            self.game_on = 'Costo Uniforme'
            self.button_sound.play()
        elif self.boton_prof and self.game_on == 'No Informada':
            self.game_on = 'Profundidad'
            self.button_sound.play()

