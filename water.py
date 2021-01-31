import pygame
import sys
import os
from random import randrange


def terminate():
    pygame.quit()
    sys.exit()


def start_screen():
    # Рисование начального экрана
    screen.fill((255, 255, 255))
    intro_text = ["Plumber", "",
                  "Правила миниигры:",
                  "Чтобы пройти дальше, собери",
                  "систему из труб."]
    font = pygame.font.Font(None, 24)
    text_coord1 = 50
    for line1 in intro_text:
        string_rendered1 = font.render(line1, True, pygame.Color('black'))
        intro_rect = string_rendered1.get_rect()
        text_coord1 += 10
        intro_rect.top = text_coord1
        intro_rect.x = 10
        text_coord1 += intro_rect.height
        screen.blit(string_rendered1, intro_rect)

    while True:
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                terminate()
            elif ev.type == pygame.KEYDOWN or \
                    ev.type == pygame.MOUSEBUTTONDOWN:
                return
        pygame.display.flip()
        clock.tick(5)


def end_screen():
    # Рисование конечного экрана
    screen.fill((255, 255, 255))
    outro_text = ["Миниигра пройдена!",
                  "Нажми на какую-нибудь клавишу",
                  "или кнопку, чтобы выйти"]
    font = pygame.font.Font(None, 22)
    text_coord2 = 50
    for line2 in outro_text:
        string_rendered2 = font.render(line2, True, pygame.Color('black'))
        outro_rect = string_rendered2.get_rect()
        text_coord2 += 10
        outro_rect.top = text_coord2
        outro_rect.x = 10
        text_coord2 += outro_rect.height
        screen.blit(string_rendered2, outro_rect)

    while True:
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                terminate()
            elif ev.type == pygame.KEYDOWN or \
                    ev.type == pygame.MOUSEBUTTONDOWN:
                return
        pygame.display.flip()
        clock.tick(5)


def load_image(name):
    # Загрузка изображения
    fullname = os.path.join('data', 'plumber', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname).convert()
    image.set_colorkey((255, 255, 255))
    return image


pygame.init()
pygame.display.set_caption('Plumber')
size = 300, 400
screen = pygame.display.set_mode(size)


class WaterPipes(pygame.sprite.Sprite):
    # Класс для спрайтов всех труб
    water_pipes = []
    pipes = []
    for i in range(1, 13):
        water_pipes.append(pygame.transform.scale(load_image('water_pipe' + str(i) + '.png'), (50, 50)))
        pipes.append(pygame.transform.scale(load_image('pipe' + str(i) + '.png'), (50, 50)))

    def __init__(self, num, x, y):
        super().__init__(all_sprites)
        self.image = pygame.transform.scale(load_image('pipe' + str(num) + '.png'), (50, 50))
        self.cell_size = 50
        self.top = 150
        self.num = num
        self.rect = pygame.Rect((x * self.cell_size, y * self.cell_size + self.top),
                                (self.image.get_width(), self.image.get_height()))


class MovingPipes(WaterPipes):
    # Класс для спрайтов тех труб, которые можно поворачивать
    def __init__(self, x, i, j):
        if x < 5:
            num1 = 1
        elif x < 7:
            num1 = 6
        elif x < 9:
            num1 = 7
        else:
            num1 = 12
        self.num = num1
        board[j][i - 1] = self.num
        super().__init__(num1, i, j)
        self.add(moving_pipes)

    def update(self, pos):
        # Изменение изображения спрайта при нажатии на повёрнутое на 90 градусов
        if self.rect.x < pos[0] < (self.rect.x + self.rect.width) and \
                self.rect.y < pos[1] < (self.rect.y + self.rect.height):
            if self.num < 5:
                self.num = 1 + self.num % 4
            elif self.num < 7:
                self.num = 5 + self.num % 2
            elif self.num < 9:
                self.num = 7 + self.num % 2
            else:
                self.num = 9 + self.num % 4
            self.image = WaterPipes.pipes[self.num - 1]
            board[self.rect.y // 50 - 3][(self.rect.x // 50) - 1] = self.num

            # Если система из труб собрана, заменить изображения на трубы с водой и закончить игру
            if board == map1:
                all_sprites.draw(screen)
                for sp in all_sprites.sprites():
                    sp.image = WaterPipes.water_pipes[sp.num - 1]
                    screen.fill((255, 255, 255))
                    all_sprites.draw(screen)
                    pygame.display.flip()
                    pygame.time.delay(100)
                pygame.time.delay(1000)
                end_screen()
                print('win')
                terminate()



screen.fill((255, 255, 255))
clock = pygame.time.Clock()
running = True
game_over = True

while running:
    if game_over:
        start_screen()
        # Объявление необходимых классов
        all_sprites = pygame.sprite.Group()
        moving_pipes = pygame.sprite.Group()
        file = 'data/plumber/plumber' + str(randrange(1, 3)) + '.txt'
        # Считывание уровня из файла
        if os.path.exists(file):
            with open(file) as f:
                lines_file = f.read().split('\n')
            a = [[int(j) for j in i.split(' ')] for i in lines_file[0].split(', ')]
            a1 = a[1:]
            a = a[0]
            board = [[0 for j in range(a[1])] for i in range(a[0])]
            for i in range(len(a1)):
                if a1[i][0] == 0:
                    WaterPipes(5, a1[i][0], a1[i][1])
            map1 = [[int(j) for j in i.split(' ') if j != ''] for i in lines_file[1:] if i != '']
            for i in range(a[0]):
                for j in range(a[1]):
                    if map1[j][i] != 0:
                        MovingPipes(map1[j][i], i + 1, j)
            for i in range(len(a1)):
                if a1[i][0] != 0:
                    WaterPipes(5, a1[i][0], a1[i][1])
        game_over = False
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            terminate()
        if event.type == pygame.MOUSEBUTTONDOWN:
            moving_pipes.update(event.pos)
    screen.fill((255, 255, 255))
    all_sprites.draw(screen)
    # Пояснение правил
    help_text = ["Поворачивай кусочки труб",
                 "нажатием левой кнопки мыши"]
    font1 = pygame.font.Font(None, 21)
    text_coord = 0
    for line in help_text:
        string_rendered = font1.render(line, True, pygame.Color('black'))
        help_rect = string_rendered.get_rect()
        text_coord += 10
        help_rect.top = text_coord
        help_rect.x = 10
        text_coord += help_rect.height
        screen.blit(string_rendered, help_rect)
    pygame.display.flip()
    clock.tick(8)
