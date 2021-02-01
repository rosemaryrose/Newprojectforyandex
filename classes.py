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
import time
import random

# переменные
FPS = 60  # ного fps грузит комп
display_size = 960, 704
tile_width = tile_height = 64
speed = 8  # обязательно степень двойки 2 4 8 и тд

other_group = pygame.sprite.Group()

hp = 100
cryst_collected = 36
game_list = ['water.py', 'nonogram.py', 'crosstheriver.py']
played_game = []


def load_image(name, colorkey=None):
    fullname = os.path.join('data/pictures', name)
    # если файл не существует, то выходим
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    return image


tile_images = {
    'floor1': load_image('floor1.png'),  # символ: .
    'floor2': load_image('floor3.png'),  # символ: ,
    'door': load_image('door.png'),  # символ: 0
    'wall': load_image('wall.png'),  # символ: -
    'ceiling': load_image('ceiling.png'),  # символ: #
    'stage': load_image('stage.png'),  # символ:  =
    'book': load_image('book.png'),  # символ: x
    'gold_door': load_image('gold_door.png'),  # символ: *
    'table': load_image('table.png'),  # символ: %
    'table_big': load_image('table_big.png'),
    'donut': load_image('donut.png'),  # символ: !
    'hero1': load_image('hero1.png'),
    'hero2': load_image('hero2.png'),
    'hero3': load_image('hero3.png'),
    'hero4': load_image('hero4.png'),
    'end_screen': load_image('end_screen.png')
}


class Creature(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__()

        self.pos_x = pos_x
        self.pos_y = pos_y


class Level:
    def __init__(self, level_name, spawn_point=None):
        self.level_name = level_name

        if spawn_point is None:
            self.spawn_point = self.get_spawn_point()
        else:
            self.spawn_point = spawn_point
        self.doors = {}

        with open('data/levels/' + self.level_name + '.txt', 'r', encoding='UTF-8') as f:
            level = f.read().split('\n')

            for i in range(self.get_door_number()):
                self.doors[str(self.get_door_cell(i))] = [self.get_door_spawn(i), self.get_next_level(i)]

        self.pos_x = (display_size[0] - tile_width) // 2 - self.spawn_point[0] * tile_width
        self.pos_y = (display_size[1] - tile_height) // 2 - self.spawn_point[1] * tile_height

        self.sprite_group = pygame.sprite.Group()

    def level_render_prepare(self):
        delta_x = self.pos_x
        delta_y = self.pos_y

        self.sprite_group.empty()
        level = self.get_level_map()

        for i in range(len(level)):
            for j in range(len(level[i])):
                if level[i][j] == '-':
                    self.sprite_group.add(Tile('wall', j * tile_width + delta_x, i * tile_height + delta_y))
                elif level[i][j] == '.':
                    self.sprite_group.add(Tile('floor1', j * tile_width + delta_x, i * tile_height + delta_y))
                elif level[i][j] == '0':
                    self.sprite_group.add(Tile('door', j * tile_width + delta_x, i * tile_height + delta_y))
                elif level[i][j] == '=':
                    self.sprite_group.add(Tile('stage', j * tile_width + delta_x, i * tile_height + delta_y))
                elif level[i][j] == '#':
                    self.sprite_group.add(Tile('ceiling', j * tile_width + delta_x, i * tile_height + delta_y))
                elif level[i][j] == 'x':
                    self.sprite_group.add(Tile('book', j * tile_width + delta_x, i * tile_height + delta_y))
                elif level[i][j] == '*':
                    self.sprite_group.add(Tile('gold_door', j * tile_width + delta_x, i * tile_height + delta_y))
                elif level[i][j] == '%':
                    self.sprite_group.add(Tile('table', j * tile_width + delta_x, i * tile_height + delta_y))
                elif level[i][j] == '!':
                    self.sprite_group.add(Tile('donut', j * tile_width + delta_x, i * tile_height + delta_y))

    def get_level_map(self):
        with open('data/levels/' + self.level_name + '.txt', 'r', encoding='UTF-8') as f:
            level = f.read().split('\n')[self.get_door_number() * 3 + 2:]
        return level

    def get_spawn_point(self):
        with open('data/levels/' + self.level_name + '.txt', 'r', encoding='UTF-8') as f:
            spawn = f.read().split('\n')[0]
        return list(map(int, spawn.split(',')))

    def get_next_level(self, n):
        with open('data/levels/' + self.level_name + '.txt', 'r', encoding='UTF-8') as f:
            next_level = f.read().split('\n')[4 + 3 * n]
        return next_level

    def get_door_spawn(self, n):
        with open('data/levels/' + self.level_name + '.txt', 'r', encoding='UTF-8') as f:
            door_spawn = f.read().split('\n')[3 + 3 * n]
        return list(map(int, door_spawn.split(',')))

    def get_door_cell(self, n):
        with open('data/levels/' + self.level_name + '.txt', 'r', encoding='UTF-8') as f:
            door_spawn = f.read().split('\n')[2 + 3 * n]
        return list(map(int, door_spawn.split(',')))

    def get_door_number(self):
        with open('data/levels/' + self.level_name + '.txt', 'r', encoding='UTF-8') as f:
            number = f.read().split('\n')[1]
        return int(number)

    def move(self, delta_x, delta_y):
        self.pos_x += delta_x
        self.pos_y += delta_y


class Hero(Creature):
    def __init__(self, pos_x, pos_y):
        super().__init__(pos_x, pos_y)
        self.width = 48
        self.height = 32
        self.sprite_group = pygame.sprite.Group()

        self.image = tile_images['hero1']
        self.rect = self.image.get_rect().move((display_size[0] - tile_width) // 2,
                                               (display_size[1] - tile_height) // 2)

        self.sprite_group.add(self)

    def flip_picture(self, picture_name):
        self.sprite_group.empty()

        self.image = tile_images[picture_name]
        self.rect = self.image.get_rect().move((display_size[0] - tile_width) // 2,
                                               (display_size[1] - tile_height) // 2)

        self.sprite_group.add(self)

    def attack(self):
        pass

    def can_go_way(self, level, way):
        cell = [self.pos_x + (tile_width - self.width) // 2, self.pos_y + tile_height - self.height]
        cell1 = [self.pos_x + tile_width - (tile_width - self.width) // 2, self.pos_y + tile_height - self.height]
        cell2 = [self.pos_x + tile_width - (tile_width - self.width) // 2, self.pos_y + tile_height - 1]
        cell3 = [self.pos_x + (tile_width - self.width) // 2, self.pos_y + tile_height - 1]

        if way == 'w':
            cell[1] -= speed
        elif way == 's':
            cell[1] += speed
        elif way == 'a':
            cell[0] -= speed
        elif way == 'd':
            cell[0] += speed

        if way == 'w':
            cell1[1] -= speed
        elif way == 's':
            cell1[1] += speed
        elif way == 'a':
            cell1[0] -= speed
        elif way == 'd':
            cell1[0] += speed

        if way == 'w':
            cell2[1] -= speed
        elif way == 's':
            cell2[1] += speed
        elif way == 'a':
            cell2[0] -= speed
        elif way == 'd':
            cell2[0] += speed

        if way == 'w':
            cell3[1] -= speed
        elif way == 's':
            cell3[1] += speed
        elif way == 'a':
            cell3[0] -= speed
        elif way == 'd':
            cell3[0] += speed

        cell = get_cell(cell)
        cell1 = get_cell(cell1)
        cell2 = get_cell(cell2)
        cell3 = get_cell(cell3)
        if level[cell[1]][cell[0]] == '#':
            return False
        if level[cell1[1]][cell1[0]] == '#':
            return False
        if level[cell2[1]][cell2[0]] == '#':
            return False
        if level[cell3[1]][cell3[0]] == '#':
            return False
        if level[cell[1]][cell[0]] == '-':
            return False
        if level[cell1[1]][cell1[0]] == '-':
            return False
        if level[cell2[1]][cell2[0]] == '-':
            return False
        if level[cell3[1]][cell3[0]] == '-':
            return False
        return True

    def in_cell(self, level):
        cell = get_cell((self.pos_x + (tile_width - self.width) // 2 + self.width // 2,
                         self.pos_y + tile_height - self.height // 2))
        return level[cell[1]][cell[0]]


class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__()
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(pos_x, pos_y)


def get_cell(m_pos):
    w = m_pos[0]
    h = m_pos[1]

    return [w // tile_width, h // tile_height]


def start_screen(screen, clock):  # функция заставки
        for i in range(255):
            screen.fill((i, i, i))
            pygame.display.flip()
            clock.tick(FPS)

        sprite = pygame.sprite.Sprite()
        sprite.image = load_image('start_screen.png')
        sprite.rect = sprite.image.get_rect()
        other_group.add(sprite)
        other_group.draw(screen)

        pygame.display.flip()

        for i in range(500):
            pygame.display.flip()
            clock.tick(FPS)


def end_screen(screen, clock):
    for i in range(255):
        screen.fill((i, i, i))
        pygame.display.flip()
        clock.tick(FPS)

    sprite = pygame.sprite.Sprite()
    sprite.image = load_image('end_screen.png')
    sprite.rect = sprite.image.get_rect()
    other_group.add(sprite)
    other_group.draw(screen)

    pygame.display.flip()

    for i in range(500):
        pygame.display.flip()
        clock.tick(FPS)

    terminate()


def terminate():  # функция выхода
    pygame.quit()
    sys.exit()
