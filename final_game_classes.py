import pygame
import random
from copy import deepcopy
import os
import sys


def terminate(n=None):
    if n is None:
        pygame.quit()
        sys.exit()
    else:
        pygame.quit()
        sys.exit(n)


class ILoveHueGame:
    def __init__(self, corner_colors, numbers_of_cells):
        self.width = numbers_of_cells[0]
        self.height = numbers_of_cells[1]
        self.board = self.make_board(corner_colors, numbers_of_cells)
        self.random_board = self.random_color_mix(corner_colors)
        self.top = 30
        self.cell_sizex = 315 // self.width
        self.cell_sizey = (539 - self.top) // self.height

        # список "недвижимых" точек
        self.static_cells = [(0, 0), (0, self.height - 1), (self.width - 1, self.height - 1), (self.width - 1, 0)]

    def get_cell(self, mouse_pos):
        # получение координат клетки, в которой сейчас мышка
        w = mouse_pos[0]
        h = mouse_pos[1] - self.top

        if w < 0 or h < 0 or w > self.cell_sizex * self.width or h > self.cell_sizey * self.height:
            return None
        else:
            return (w // self.cell_sizex, h // self.cell_sizey)

    def render(self, screen):
        # рисуем цветные клетки
        for i in range(self.width):
            for j in range(self.height):
                pygame.draw.rect(screen, self.random_board[i][j],
                                 ((i * self.cell_sizex, self.top + j * self.cell_sizey),
                                  (self.cell_sizex, self.cell_sizey)))
        # рисуем "недвижимые" точки
        for i in self.static_cells:
            pygame.draw.circle(screen, (0, 0, 0), (
                self.cell_sizex // 2 + i[0] * self.cell_sizex,
                self.top + self.cell_sizey // 2 + i[1] * self.cell_sizey), 3)

    # создание поля
    def make_board(self, corner_colors, numbers_of_cells):
        line1 = self.make_line(corner_colors[0], corner_colors[1], numbers_of_cells[0])
        line2 = self.make_line(corner_colors[2], corner_colors[3], numbers_of_cells[0])
        board = []

        for i in range(self.width):
            board.append(self.make_line(line1[i], line2[i], numbers_of_cells[1]))
        return board

    # генерация цветового поля
    def make_line(self, start_color, end_color, cells_width):
        line = [[0, 0, 0] for _ in range(cells_width)]
        for i in range(3):
            color0 = start_color[i]
            color1, color2 = start_color[i], end_color[i]
            k = (color2 - color1) / (cells_width - 1)
            for j in range(1, cells_width):
                color1 += k
                line[j][i] = int(color1)
            line[0][i] = color0
            line[cells_width - 1][i] = color2
        return line

    # перемешивание
    def random_color_mix(self, corner_colors):
        random_mix = deepcopy(self.board)
        cells = list()
        for column in self.board:
            for cell in column:
                if tuple(cell) not in corner_colors:
                    cells.append(cell)

        for i in range(self.width):
            for j in range(self.height):
                if tuple(random_mix[i][j]) not in corner_colors:
                    random_mix[i][j] = cells.pop(random.randrange(0, len(cells)))
        return random_mix

    def render_start(self, screen):
        # начальное поле и плавное удаление клеток
        for i in range(self.width):
            for j in range(self.height):
                pygame.draw.rect(screen, self.board[i][j], ((i * self.cell_sizex, self.top + j * self.cell_sizey),
                                                            (self.cell_sizex, self.cell_sizey)))
        for i in self.static_cells:
            pygame.draw.circle(screen, (0, 0, 0), (
                self.cell_sizex // 2 + i[0] * self.cell_sizex,
                self.top + self.cell_sizey // 2 + i[1] * self.cell_sizey), 3)

        pygame.display.flip()
        pygame.time.delay(1000)
        k = 2
        for i in range(self.width + self.height - 2):
            for j in range(k):
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        exit()

                # замена цветных клеток на чёрные волной
                pygame.draw.rect(screen, (0, 0, 0), (((k - j - 1) * self.cell_sizex, self.top + j * self.cell_sizey),
                                                     (self.cell_sizex, self.cell_sizey)))

            # рисуем крайние клетки и точки
            pygame.draw.rect(screen, self.board[self.width - 1][self.height - 1],
                             (((self.width - 1) * self.cell_sizex, self.top + (self.height - 1) * self.cell_sizey),
                              (self.cell_sizex, self.cell_sizey)))
            pygame.draw.rect(screen, self.board[0][self.height - 1],
                             ((0, self.top + (self.height - 1) * self.cell_sizey),
                              (self.cell_sizex, self.cell_sizey)))
            pygame.draw.rect(screen, self.board[self.width - 1][0], (((self.width - 1) * self.cell_sizex, self.top),
                                                                     (self.cell_sizex, self.cell_sizey)))
            pygame.draw.rect(screen, self.board[0][0], ((0, self.top), (self.cell_sizex, self.cell_sizey)))

            for i in self.static_cells:
                pygame.draw.circle(screen, (0, 0, 0), (
                    self.cell_sizex // 2 + i[0] * self.cell_sizex,
                    self.top + self.cell_sizey // 2 + i[1] * self.cell_sizey), 3)

            clock = pygame.time.Clock()
            clock.tick(9)
            pygame.display.flip()
            k += 1


class Button:
    def __init__(self, screen, bg_image_name, position, size):
        pass

    def load_image(self, name, colorkey=None):
        fullname = os.path.join('../../Desktop/Новая папка/ilovehue00/Data', name)

        image = pygame.image.load(fullname)

        if colorkey is not None:
            image = image.convert()
            if colorkey == -1:
                colorkey = image.get_at((0, 0))
            image.set_colorkey(colorkey)
        else:
            image = image.convert_alpha()

        return image


class ILoveHueMenu:
    def __init__(self):
        pass
