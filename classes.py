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
display_size = 960, 640
tile_width = tile_height = 64

other_group = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()
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
}

hero = load_image('floor.png')


class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__()
        self.image = hero
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)


class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__()
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)


def level_render(level):
    tiles_group.empty()
    with open('data/levels/' + level + '.txt', 'r', encoding='UTF-8') as f:
        level = f.read().split('\n')

        for i in range(len(level)):
            for j in range(len(level[i])):
                if level[i][j] == '#':
                    tiles_group.add(Tile('wall', j, i))
                elif level[i][j] == '.':
                    tiles_group.add(Tile('floor', j, i))
                elif level[i][j] == '0':
                    tiles_group.add(Tile('door', j, i))
                elif level[i][j] == '=':
                    tiles_group.add(Tile('stage', j, i))


def start_screen():  # функция заставки
    """
        картинка для заставки, название или еще что-нибудь
    """
    pass


def terminate():  # функция выхода
    pygame.quit()
    sys.exit()
