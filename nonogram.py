import pygame
import sys
import os
from random import randrange


def terminate():
    pygame.quit()
    sys.exit()


def start_screen():
    screen.fill((255, 255, 255))
    intro_text = ["Nonogram", "",
                  "Правила миниигры:",
                  "Чтобы пройти дальше, собери",
                  "японскую головоломку.",
                  "Сверху поля ты увидишь, сколько ",
                  "закрашенных клеток должно быть",
                  "в каждом столбце или линии"]
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
    screen.fill((255, 255, 255))
    outro_text = ["Миниигра пройдена!",
                  "Нажми на какую-нибудь клавишу",
                  "или кнопку, чтобы выйти"]
    font = pygame.font.Font(None, 22)
    text_coord = 50
    for line in outro_text:
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


class Nonogram:
    def __init__(self, level):
        self.cs = 20
        self.top = 100
        self.left = 0
        self.lives = 10
        self.k = 0
        file = 'data/nonogram' + level + '.txt'
        if os.path.exists(file):
            with open(file) as f:
                lines_file = f.read().split('\n')
        self.filled_board = [[int(j) for j in list(i)] for i in lines_file]
        self.board = [[0 for i in range(10)] for j in range(10)]
        self.vertical = []
        self.horizontal = []
        self.filled_cells = 0

        for line in range(10):
            k = 0
            full_line = []
            for s in lines_file[line]:
                if s == '1':
                    k += 1
                    self.filled_cells += 1
                elif k != 0 and s == '0':
                    full_line.append(str(k))
                    k = 0
            if k != 0:
                full_line.append(str(k))
            self.vertical.append('  '.join(full_line))

        for column in range(10):
            k = 0
            full_column = []
            for s in range(10):
                if lines_file[s][column] == '1':
                    k += 1
                elif k != 0 and lines_file[s][column] == '0':
                    full_column.append(str(k))
                    k = 0
            if k != 0:
                full_column.append(str(k))
            self.horizontal.append(full_column)

    def render(self):
        help_text = ["Закрашивай нужную клетку с помощью",
                     "левой кнопки мыши и отмечай пустые ",
                     "клетки крестами правой кнопкой.",
                     "Помни, что ошибаться можно лишь 10 раз!"]
        font = pygame.font.Font(None, 19)
        text_coord = 0
        for line in help_text:
            string_rendered = font.render(line, True, pygame.Color('black'))
            intro_rect = string_rendered.get_rect()
            text_coord += 10
            intro_rect.top = text_coord
            intro_rect.x = 10
            text_coord += intro_rect.height
            screen.blit(string_rendered, intro_rect)
        pygame.draw.rect(screen, (0, 0, 0),
                         ((self.left + 5 * self.cs - 1, self.top + 5 * self.cs - 1), (202, 202)), 1)
        for i in range(15):
            for j in range(15):
                if i >= 5 and j >= 5:
                    pygame.draw.rect(screen, (0, 0, 0),
                                     ((self.left + i * self.cs, self.top + j * self.cs), (self.cs, self.cs)), 1)
                    if self.board[i - 5][j - 5] == 1:
                        pygame.draw.rect(screen, (21, 18, 126),
                                         ((self.left + i * self.cs + 1, self.top + j * self.cs + 1),
                                         (self.cs - 2, self.cs - 2)), 0)
                    elif self.board[i - 5][j - 5] == 2:
                        x1 = self.left + i * self.cs
                        y1 = self.top + j * self.cs
                        pygame.draw.line(screen, (110, 110, 110), (x1 + 3, y1 + 3),
                                         (x1 + self.cs - 3, y1 + self.cs - 3), 1)
                        pygame.draw.line(screen, (110, 110, 110), (x1 + 3, y1 + self.cs - 3),
                                         (x1 + self.cs - 3, y1 + 3), 1)
                    elif self.board[i - 5][j - 5] == 3:
                        x1 = self.left + i * self.cs
                        y1 = self.top + j * self.cs
                        pygame.draw.line(screen, (213, 16, 56), (x1 + 3, y1 + 3),
                                         (x1 + self.cs - 3, y1 + self.cs - 3), 1)
                        pygame.draw.line(screen, (213, 16, 56), (x1 + 3, y1 + self.cs - 3),
                                         (x1 + self.cs - 3, y1 + 3), 1)
                if i < 5 and j >= 5:
                    string_rendered = font.render(self.vertical[j - 5], True, (0, 0, 0))
                    intro_rect = string_rendered.get_rect()
                    text_coord = self.top + 20 * j
                    intro_rect.top = text_coord + 3
                    intro_rect.x = 25
                    screen.blit(string_rendered, intro_rect)
                    pygame.draw.line(screen, (90, 90, 90), (self.left + 20, self.top + j * self.cs),
                                     (self.left + 5 * self.cs, self.top + j * self.cs), 1)
                if i >= 5 and j < 5:
                    if len(self.horizontal[i - 5]) > j:
                        string_rendered = font.render(self.horizontal[i - 5][j], True, (0, 0, 0))
                        intro_rect = string_rendered.get_rect()
                        intro_rect.top = 10 + self.top + 18 * j
                        intro_rect.x = 20 * i + 5
                        screen.blit(string_rendered, intro_rect)
                    pygame.draw.line(screen, (90, 90, 90), (self.left + i * self.cs, self.top + 5),
                                     (self.left + i * self.cs, self.top + 5 * self.cs), 1)

    def get_click(self, mouse_pos, button):
        cell = self.get_cell(mouse_pos)
        if cell is not None:
            self.on_click(cell, button)

    def get_cell(self, mouse_pos):
        x = mouse_pos[0] - self.left
        y = mouse_pos[1] - self.top
        if (x < self.cs * 5) or (y < self.cs * 5) or (x > self.cs * 15) or (y > self.cs * 15):
            return None
        else:
            return (x // self.cs) - 5, (y // self.cs) - 5

    def on_click(self, cell, button):
        global game_over
        if self.board[cell[0]][cell[1]] == 0:
            if self.filled_board[cell[1]][cell[0]] == 0 and button == 1:
                self.board[cell[0]][cell[1]] = 3
                self.lives += -1
                if self.lives == 0:
                    print('game_over')
                    game_over = True
            if button == 3:
                self.board[cell[0]][cell[1]] = 2
            if self.filled_board[cell[1]][cell[0]] == 1 and button == 1:
                self.board[cell[0]][cell[1]] = 1
                self.k += 1
        elif self.board[cell[0]][cell[1]] == 2:
            if button == 3:
                self.board[cell[0]][cell[1]] = 0
            if button == 1 and self.filled_board[cell[1]][cell[0]] == 1:
                self.board[cell[0]][cell[1]] = 1
                self.k += 1
            if button == 1 and self.filled_board[cell[1]][cell[0]] == 0:
                self.board[cell[0]][cell[1]] = 3
        if self.k == self.filled_cells:
            print('win')
            pygame.time.delay(2000)
            end_screen()
            terminate()


pygame.init()
pygame.display.set_caption('Nonogram')
size = 300, 400
screen = pygame.display.set_mode(size)
screen.fill((255, 255, 255))
clock = pygame.time.Clock()
running = True
game_over = True

while running:
    if game_over:
        start_screen()
        game_over = False
        board = Nonogram(str(randrange(1, 6)))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            terminate()
        if event.type == pygame.MOUSEBUTTONDOWN:
            board.get_click(event.pos, event.button)
    screen.fill((255, 255, 255))
    board.render()
    pygame.display.flip()
    clock.tick(8)
