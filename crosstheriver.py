import pygame
import sys
from random import randrange, choice


def terminate(n=None):
    if n is None:
        pygame.quit()
        sys.exit()
    else:
        pygame.quit()
        sys.exit(n)


class Board(pygame.sprite.Sprite):
    # Класс для спрайтов брёвен, плывущих по реке
    def __init__(self, y, x=0):
        super().__init__(all_sprites)
        self.add(boards)
        self.length = randrange(40, 70)
        self.width = 15
        self.y = y
        self.added = False
        # Справа или слева бревно поплывёт
        if x != 0:
            if x < 0:
                self.n = -self.length
            else:
                self.n = 300
        else:
            self.n = choice([-self.length, 300])
        self.image = pygame.Surface((self.length, self.width),
                                    pygame.SRCALPHA, 32)
        pygame.draw.rect(self.image, (73, 19, 13),
                         (0, 0, self.length, self.width), 0)
        self.rect = pygame.Rect((self.n, self.y), (self.length, self.width))
        # Выбор скорости, с которой спрайт 'плывёт'
        if self.n < 0:
            self.vx = randrange(2, 5)
        else:
            self.vx = -1 * randrange(2, 5)

    def update(self):
        self.rect.x += self.vx
        if ((self.n > 0 and self.rect.x < 160) or
                (self.n < 0 and self.rect.x > 140)) and (not self.added):
            Board(self.y, self.n)
            self.added = True
        # Проверка, не выплыл ли спрайт за границы экрана
        if not self.rect.colliderect(screen_rect):
            # Если да, то с в том же направлении поплывёт новый спрайт
            if not self.added:
                Board(self.y, self.n)
            self.kill()


class Land(pygame.sprite.Sprite):
    # Класс для спрайтов земли сверху и снизу
    def __init__(self, x):
        super().__init__(all_sprites)
        self.add(land)
        self.image = pygame.Surface((300, 35), pygame.SRCALPHA, 32)
        pygame.draw.rect(self.image, (43, 110, 58),
                         (0, 0, 300, 35), 0)
        if x == 0:
            self.rect = pygame.Rect(0, 0, 300, 35)
        else:
            self.rect = pygame.Rect(0, 365, 300, 35)


class Gamer(pygame.sprite.Sprite):
    # Класс для спрайта игрока
    def __init__(self):
        super().__init__(all_sprites)
        self.add(gamer)
        self.image = pygame.Surface((14, 14), pygame.SRCALPHA, 32)
        pygame.draw.circle(self.image, (255, 0, 0),
                           (7, 7), 7, 0)
        self.rect = pygame.Rect((150 - 7, 400 - 29), (14, 14))

    def update(self, *kp):
        global game_over
        if len(kp) > 0:
            # Передвижение игрока
            if kp[0] == pygame.K_LEFT:
                self.rect.x += -20
            if kp[0] == pygame.K_UP:
                self.rect.y += -30
            if kp[0] == pygame.K_RIGHT:
                self.rect.x += 20
            if kp[0] == pygame.K_DOWN:
                self.rect.y += 30
        m = pygame.sprite.spritecollideany(self, land)
        n = pygame.sprite.spritecollideany(self, boards)
        if m is None and n is None:
            game_over = True
            print('game over')
        elif m == land.sprites()[0]:
            # Окончание игры, если игрок дошёл до конца
            print('win')
            end_screen()
            terminate(1)
        elif n:
            # Если игрок стоит на бревне, то его скорость равна скорости бревна
            self.rect.x += n.vx


def start_screen():
    # Рисуется начальный экран
    screen.fill((255, 255, 255))
    intro_text = ["Cross the river", "",
                  "Правила миниигры:",
                  "Тебе необходимо добраться до",
                  "другой стороны реки по брёвнам,",
                  "для этого используй стрелки.",
                  "Нажми на какую-нибудь клавишу",
                  "или кнопку, чтобы начать игру"]
    font = pygame.font.Font(None, 22)
    text_coord = 50
    for line in intro_text:
        string_rendered = font.render(line, True, pygame.Color('black'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)

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
    # Рисуется конечный экран
    screen.fill((255, 255, 255))
    intro_text = ["Ты успешно прошёл миниигру!",
                  "Нажми на какую-нибудь клавишу",
                  "или кнопку, чтобы выйти"]
    font = pygame.font.Font(None, 22)
    text_coord = 50
    for line in intro_text:
        string_rendered = font.render(line, True, pygame.Color('black'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)

    while True:
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                terminate()
            elif ev.type == pygame.KEYDOWN or \
                    ev.type == pygame.MOUSEBUTTONDOWN:
                return
        pygame.display.flip()
        clock.tick(5)


pygame.init()
pygame.display.set_caption('Cross the river')
size = 300, 400
screen = pygame.display.set_mode(size)
screen.fill((255, 255, 255))
clock = pygame.time.Clock()
running = True
game_over = True
screen_rect = (0, 0, 300, 400)

while running:
    if game_over:
        # Объявляются группы спрайтов и др для начала игры
        start_screen()
        all_sprites = pygame.sprite.Group()
        land = pygame.sprite.Group()
        boards = pygame.sprite.Group()
        gamer = pygame.sprite.Group()
        Land(0)
        Land(1)
        for i in range(2, 13):
            Board(400 - i * 30)
        Gamer()
        game_over = False
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            terminate()
        if event.type == pygame.KEYDOWN:
            gamer.update(event.key)
    screen.fill((40, 35, 245))

    boards.update()
    gamer.update()
    all_sprites.draw(screen)
    gamer.draw(screen)
    pygame.display.flip()
    clock.tick(8)
