import pygame as pyg, sys, numpy as np, animations as a
from pygame.locals import *

# INFORMADA
import BusquedaNoInformada.Amplitud
from BusquedaNoInformada.Amplitud import *

import BusquedaNoInformada.CostoUniforme
from BusquedaNoInformada.CostoUniforme import *

import BusquedaNoInformada.Profundidad
from BusquedaNoInformada.Profundidad import *

# NO INFORMADA
import BusquedaInformada.A_estrella
from BusquedaInformada.A_estrella import *

import BusquedaInformada.Avara
from BusquedaInformada.Avara import *


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
        self.clock = pyg.time.Clock()

        # ventana
        self.screen = pyg.display.set_mode((500, 500))
        pyg.display.set_caption('Bombero Araganico')
        self.icon = pyg.image.load('Sprites/bomberoicon.png')
        self.fire_image = pyg.image.load('Sprites/fire.png')
        self.hidrante = pyg.image.load('Sprites/hidrante.png')
        self.balde = pyg.image.load('Sprites/balde.png')
        self.color = '#2F2C2B'
        pyg.display.set_icon(self.icon)
        pyg.mixer.music.load('Music/Jeremy Blake - PowerUp!.wav')
        pyg.mixer.music.play(-1)
        pyg.mixer.music.set_volume(0.5)
        self.button_sound = pyg.mixer.Sound('Music/button_clic.wav')
        self.moving_sprites = pyg.sprite.Group()
        self.bombero = a.Bombero(self.bombero_position)
        self.moving_sprites.add(self.bombero)
        self.filename = filename
        self.costo = False
        self.record_state = None
        self.matrix = filename
        self.matrix_generator()
        self.load_world(filename)
        self.informada_boton = Button((250 - 105), 170, self, "Informada")
        self.avara_boton = Button(145, 170, self, "Avara")
        self.A_star_boton = Button(145, 230, self, "A*")
        self.no_informada_boton = Button(145, 230, self, "No Informada")
        self.amplitud_boton = Button(145, 165, self, "Amplitud")
        self.costo_uniforme_boton = Button(145, 225, self, "Costo Uniforme")
        self.profundidad_boton = Button(145, 285, self, "Profundidad")
        self.menu_boton = Button(0, 0, self, "Menu")
        self.game_on = 'Inicio'

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
    def move_bomber(self, path, fire_count, acciones):
        self.load_world(self.filename)
        balde = False
        i = 0
        accion = 'derecha'
        for next_position in path:
            self.bombero_position = next_position
            self.moving_sprites = pyg.sprite.Group()
            self.screen.fill(self.color)
            cell_value = self.grid[next_position[0]][next_position[1]]
            if cell_value == 2 or (cell_value == 3 and not balde) or (cell_value == 4 and not balde):
                if cell_value == 2:
                    fire_count -= 1
                if cell_value == 4 or cell_value == 3:
                    balde = True

                self.grid[next_position[0]][next_position[1]] = 0
            event = pyg.event.get(QUIT)
            if not event:
                None
            elif event[0].type == QUIT:
                pyg.quit()
                sys.exit()
            if balde and (acciones[i] == 'arriba' or acciones[i] == 'abajo'):
                if self.bombero.image == self.bombero.animation_right[self.bombero.counter]:
                    accion = 'derecha balde'
            elif acciones[i] == 'izquierda':
                if balde:
                    accion = 'izquierda balde'
                else:
                    accion = 'izquierda'
            elif acciones[i] == 'derecha':
                if balde:
                    accion = 'derecha balde'
                else:
                    accion = 'derecha'

            if fire_count == 0:
                self.grid[next_position[0]][next_position[1]] = 0
                self.carga_mundo(accion)
                pyg.display.update()
                pyg.time.wait(1000)
                self.game_on = 'Registro'
                self.crear_texto('Presiona r para ver el registro', (250, 250), self.screen)

                break
            pyg.event.pump()
            self.carga_mundo(accion)
            i += 1

    def crear_texto(self, text, position, screen):

        font = pyg.font.Font('Fonts/Pixels.ttf', 50)
        mensaje = font.render(text, True, '#DF621C', None)

        mensaje_rect = mensaje.get_rect()
        mensaje_rect.center = [position[0], position[1]]
        screen.blit(mensaje, mensaje_rect)

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
                    if self.game_on == 'Menu':
                        self.screen.fill(self.color)
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
                        nodo, path, maps, acciones, contador, tiempo = BusquedaNoInformada.Amplitud.solve_amplitud(self.matrix)
                        self.move_bomber(path, nodo.fire, acciones)
                        self.record_state = 'Amp'
                    if self.game_on == 'Costo Uniforme':
                        nodo, path, maps, acciones, contador, tiempo, costo = BusquedaNoInformada.CostoUniforme.solve_costo_uniforme(self.matrix)
                        self.move_bomber(path, nodo.fire, acciones)
                        self.record_state = 'Cu'
                    if self.game_on == 'Profundidad':
                        nodo, path, maps, acciones, contador, tiempo = BusquedaNoInformada.Profundidad.solve_profundidad(self.matrix)
                        self.move_bomber(path, nodo.fire, acciones)
                        self.record_state = 'Prof'
                    if self.game_on == 'A*':
                        nodo, path, maps, acciones, contador, tiempo = BusquedaInformada.A_estrella.solve_a_estrella(self.matrix)
                        self.move_bomber(path, nodo.fire, acciones)
                        self.record_state = 'A*'
                    if self.game_on == 'Avara':
                        nodo, path, maps, acciones, contador, tiempo = BusquedaInformada.Avara.solve_avara(self.matrix)
                        self.move_bomber(path, nodo.fire, acciones)
                        self.record_state = 'Ava'
                if event.type == pyg.KEYDOWN:
                    if event.key == pyg.K_r and self.game_on == 'Registro':
                        self.screen.fill(self.color)
                        self.menu_boton.set_coord(145, 290)
                        self.menu_boton.dibuja_boton()
                        nodos = 0
                        profundidad = 0
                        tiempo = 0
                        costo = 0
                        if self.record_state == 'Amp':
                            nodo, path, maps, acciones, contador, tiempo = BusquedaNoInformada.Amplitud.solve_amplitud(self.matrix)
                            profundidad = len(path)
                            nodos = contador

                        if self.record_state == 'Cu':
                            nodo, path, maps, acciones, contador, tiempo, costo = BusquedaNoInformada.CostoUniforme.solve_costo_uniforme(self.matrix)
                            profundidad = len(path)
                            nodos = contador
                            self.crear_texto('Costo de solucion: {}'.format(costo), (250, 200), self.screen)

                        if self.record_state == 'Prof':
                            nodo, path, maps, acciones, contador, tiempo = BusquedaNoInformada.Profundidad.solve_profundidad(self.matrix)
                            profundidad = len(path)
                            nodos = contador

                        if self.record_state == 'A*':
                            nodo, path, maps, acciones, contador, tiempo = BusquedaInformada.A_estrella.solve_a_estrella(self.matrix)
                            profundidad = len(path)
                            nodos = contador
                            self.crear_texto('Costo de solucion: {}'.format(costo), (250, 200), self.screen)

                        if self.record_state == 'Ava':
                            nodo, path, maps, acciones, contador, tiempo = BusquedaInformada.Avara.solve_avara(self.matrix)
                            profundidad = len(path)
                            nodos = contador

                        self.crear_texto('Nodos expandidos: {}'.format(nodos), (250, 50), self.screen)
                        self.crear_texto('Profundidad del arbol: {}'.format(profundidad), (250, 100), self.screen)
                        self.crear_texto('Tiempo de computo: {}'.format(tiempo), (250, 150), self.screen)

            if self.game_on == 'Inicio':
                self.screen.fill(self.color)
                self.informada_boton.dibuja_boton()
                self.no_informada_boton.dibuja_boton()

            self.clock.tick(60)
            pyg.display.update()

    def carga_mundo(self, accion):
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
        x_pos = 0
        y_pos = 0
        rect_color = 'white'
        grid_row = 0
        grid_col = 0
        for row in range(self.rows):
            for col in range(self.cols):
                cell_value = self.grid[row][col]
                color = colors.get(cell_value, "white")
                x1, y1 = col * 50, row * 50
                x2, y2 = x1 + 50, y1 + 50
                if cell_value == 2:
                    pyg.draw.rect(self.screen, 'white', (x1, y1, x2, y2))
                    self.screen.blit(self.fire_image, (x1, y1))
                    pyg.draw.line(self.screen, (0, 0, 0), (x1, y1), (x2, y1), 1)
                    pyg.draw.line(self.screen, (0, 0, 0), (x1, y1), (x1, y2), 1)
                elif cell_value == 6:
                    pyg.draw.rect(self.screen, 'white', (x1, y1, x2, y2))
                    self.screen.blit(self.hidrante, (x1, y1))
                    pyg.draw.line(self.screen, (0, 0, 0), (x1, y1), (x2, y1), 1)
                    pyg.draw.line(self.screen, (0, 0, 0), (x1, y1), (x1, y2), 1)
                elif cell_value == 3 or cell_value == 4:
                    pyg.draw.rect(self.screen, 'white', (x1, y1, x2, y2))
                    self.screen.blit(self.balde, (x1, y1))
                    pyg.draw.line(self.screen, (0, 0, 0), (x1, y1), (x2, y1), 1)
                    pyg.draw.line(self.screen, (0, 0, 0), (x1, y1), (x1, y2), 1)
                else:
                    pyg.draw.rect(self.screen, color, (x1, y1, x2, y2))
                    pyg.draw.line(self.screen, (0, 0, 0), (x1, y1), (x2, y1), 1)
                    pyg.draw.line(self.screen, (0, 0, 0), (x1, y1), (x1, y2), 1)
                # dibujar el bombero en movimiento
                if (row, col) == self.bombero_position:
                    self.bombero = a.Bombero((x1, y1))
                    self.moving_sprites.add(self.bombero)
                    rect_color = color
                    x_pos = x1
                    y_pos = y1
                    grid_row = row
                    grid_col = col
        pyg.display.update()
        for sprite in range(0, 3):
            update_rect = pyg.draw.rect(self.screen, rect_color, (x_pos + 1, y_pos + 1, 48, 48))
            if self.grid[grid_row][grid_col] == 2:
                pyg.draw.rect(self.screen, 'white', (x_pos + 1, y_pos + 1, 48, 48))
                self.screen.blit(self.fire_image, (x_pos, y_pos))
            if self.grid[grid_row][grid_col] == 3 or self.grid[grid_row][grid_col] == 4:
                pyg.draw.rect(self.screen, 'white', (x_pos + 1, y_pos + 1, 48, 48))
                self.screen.blit(self.balde, (x_pos, y_pos))
            if self.grid[grid_row][grid_col] == 6:
                pyg.draw.rect(self.screen, 'white', (x_pos + 1, y_pos + 1, 48, 48))
                self.screen.blit(self.hidrante, (x_pos, y_pos))
            self.moving_sprites.update(accion)
            self.moving_sprites.draw(self.screen)
            pyg.display.update(update_rect)
            pyg.time.wait(80)

    def matrix_generator(self):
        matriz = np.zeros((10, 10), dtype=int)

        with open(self.filename) as file:
            for fila, linea in enumerate(file):
                valores = linea.split()
                for columna, valor in enumerate(valores):
                    matriz[fila, columna] = int(valor)
        self.matrix = matriz

    def checa_boton(self, mouse_pos):
        self.boton_inf = self.informada_boton.rect.collidepoint(mouse_pos)
        self.boton_ninf = self.no_informada_boton.rect.collidepoint(mouse_pos)
        self.boton_m = self.menu_boton.rect.collidepoint(mouse_pos)
        self.boton_amp = self.amplitud_boton.rect.collidepoint(mouse_pos)
        self.boton_cuni = self.costo_uniforme_boton.rect.collidepoint(mouse_pos)
        self.boton_prof = self.profundidad_boton.rect.collidepoint(mouse_pos)
        self.boton_star = self.A_star_boton.rect.collidepoint(mouse_pos)
        self.boton_avara = self.avara_boton.rect.collidepoint(mouse_pos)
        if self.boton_inf and (self.game_on == 'Menu' or self.game_on == 'Inicio'):
            self.game_on = 'Informada'
            self.button_sound.play()
        elif self.boton_ninf and (self.game_on == 'Menu' or self.game_on == 'Inicio'):
            self.game_on = 'No Informada'
            self.button_sound.play()
        elif self.boton_m and (self.game_on == 'Informada' or self.game_on == 'No Informada' or
                               self.game_on == 'Registro'):
            self.game_on = 'Menu'
            self.button_sound.play()
        elif self.boton_amp and self.game_on == 'No Informada':
            self.game_on = 'Amplitud'
            self.button_sound.play()
        elif self.boton_cuni and self.game_on == 'No Informada':
            self.game_on = 'Costo Uniforme'
            self.button_sound.play()
        elif self.boton_prof and self.game_on == 'No Informada':
            self.game_on = 'Profundidad'
            self.button_sound.play()
        elif self.boton_star and self.game_on == 'Informada':
            self.game_on = 'A*'
            self.button_sound.play()
        elif self.boton_avara and self.game_on == 'Informada':
            self.game_on = 'Avara'
            self.button_sound.play()


