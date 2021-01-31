"""
Название (обсуждается):
    The Hue
Некое вступление:
    Некий гном (имя надо еще придумать) находит карту
    По ней находит замок
    В замке нужно найти все камни у всех хранителей (имена их каждый для себя придумает самостоятельно)

Концепция:
    Первый этаж-меню. Если пойдешь к дверям, то выходишь из игры, если к лестнице, то переходишь на первый этаж

    Есть три "хранителя". Каждый занимает этаж и в своих загадках, боях и т.д. прячет камни, необходимые для прохода к сокровищу
    На последнем этаже есть дверь с нашей начальной загадкой (ее нельзя будет активировать пока не соберешь все камни
"""

import pygame
import sys
import os

# переменные
FPS = 50
display_size = 960, 704
tile_width = tile_height = 64
speed = 10

other_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()


def load_image(name, colorkey=None):
    fullname = os.path.join('data/pictures', name)
    # если файл не существует, то выходим
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    return image


tile_images = {
    'floor': load_image('floor.png'),
    'door': load_image('door.png'),
    'wall': load_image('wall.png'),
    'stage': load_image('stage.png'),
    'hero1': load_image('hero1.png'),
    'hero2': load_image('hero2.png'),
}


class Creature(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__()

        self.pos_x = pos_x
        self.pos_y = pos_y


class Level:
    def __init__(self, level_name):
        self.level_name = level_name
        self.spawn_point = self.get_spawn_point()

        self.pos_x = (display_size[0] - tile_width) // 2 - self.spawn_point[0] * tile_width
        self.pos_y = (display_size[1] - tile_height) // 2 - self.spawn_point[1] * tile_height

        self.sprite_group = pygame.sprite.Group()

    def level_render_prepare(self):
        delta_x = self.pos_x
        delta_y = self.pos_y

        self.sprite_group.empty()
        level = self.get_level()

        for i in range(len(level)):
            for j in range(len(level[i])):
                if level[i][j] == '#':
                    self.sprite_group.add(Tile('wall', j * tile_width + delta_x, i * tile_height + delta_y))
                elif level[i][j] == '.':
                    self.sprite_group.add(Tile('floor', j * tile_width + delta_x, i * tile_height + delta_y))
                elif level[i][j] == '0':
                    self.sprite_group.add(Tile('door', j * tile_width + delta_x, i * tile_height + delta_y))
                elif level[i][j] == '=':
                    self.sprite_group.add(Tile('stage', j * tile_width + delta_x, i * tile_height + delta_y))

    def get_level(self):
        with open('data/levels/' + self.level_name + '.txt', 'r', encoding='UTF-8') as f:
            level = f.read().split('\n')[1:]
        return level

    def get_spawn_point(self):
        with open('data/levels/' + self.level_name + '.txt', 'r', encoding='UTF-8') as f:
            spawn = f.read().split('\n')[0]
        return list(map(int, spawn.split(',')))

    def move(self, delta_x, delta_y):
        self.pos_x += delta_x
        self.pos_y += delta_y


class Hero(Creature):
    def __init__(self, pos_x, pos_y):
        super().__init__(pos_x, pos_y)

        self.image = tile_images['hero1']
        self.rect = self.image.get_rect().move((display_size[0] - tile_width) // 2,
                                               (display_size[1] - tile_height) // 2)

    def flip_picture(self):
        pass

    def attack(self):
        pass

    def cell_action(self, level, way):
        if way == 'w':
            cell = (self.pos_x // tile_width, self.pos_y // tile_width)

            if level[cell[0]][cell[1]] == '#':
                return level[cell[0]][cell[1]]


class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__()
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(pos_x, pos_y)


def start_screen():  # функция заставки
    """
        картинка для заставки, название или еще что-нибудь
    """
    pass


def terminate():  # функция выхода
    pygame.quit()
    sys.exit()
