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
display_size = 315, 545
tile_width = tile_height = 50

all_sprites = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    # если файл не существует, то выходим
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    return image


tile_images = {
    'wall': load_image('box.png'),
    'empty': load_image('grass.png')
}
player_image = load_image('mario.png')


class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(tiles_group, all_sprites)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)


def start_screen():  # функция заставки
    """
        картинка для заставки, название или еще что-нибудь
    """
    pass


def terminate():  # функция выхода
    pygame.quit()
    sys.exit()
