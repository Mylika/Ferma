import pygame
import random
import os
import sys


pygame.init()

all_sprites = pygame.sprite.Group()

#screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
#size = width, height = screen.get_size()
size = width, height = 1024, 860
screen = pygame.display.set_mode(size)
screen.fill('#C0F400')


def load_image(name, colorkey=-9):
    fullname = os.path.join('data', name)
    # если файл не существует, то выходим
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    #if colorkey is not None:
    #    image = image.convert()
    #    if colorkey == -1:
    #        colorkey = image.get_at((0, 0))
    #    image.set_colorkey(colorkey)
    #else:
    image = image.convert_alpha()
    image1 = pygame.transform.scale(image, (100, 100))
    return image1


class Board:
    def __init__(self, width, height, w, h):
        self.width = width
        self.height = height
        self.board = [[0] * width for _ in range(height)]

        self.left = int(w * 0.15)
        self.top = int(h * 0.15)
        self.cell_size = int(h * 0.11)

    def set_view(self, left, top, cell_size):
        self.left = left
        self.top = top
        self.cell_size = cell_size

    def render(self):
        all_sprites.empty()
        x, y = self.left, self.top
        for i in range(self.height):
            for j in range(self.width):
                pygame.draw.rect(screen, '#573B08', (x, y, self.cell_size, self.cell_size), 1)
                if self.board[i][j] >= 1:
                    Plant(x, y, self.board[i][j], all_sprites)
                elif self.board[i][j] <= -1:
                    Weed(x, y, self.board[i][j], all_sprites)
                else:
                    pygame.draw.rect(screen, '#865F1A', (x + 1, y + 1, self.cell_size - 2, self.cell_size - 2))
                x += self.cell_size
            x = self.left
            y += self.cell_size

    def get_cell(self, mouse_pos):
        if self.left <= mouse_pos[0] <= self.left + self.cell_size * self.width and \
                self.top <= mouse_pos[1] <= self.top + self.cell_size * self.height:
            x, y = - 1, -1

            for i in range(self.left, self.left + self.cell_size * self.width, self.cell_size):
                if i < mouse_pos[0]:
                    x += 1
            for i in range(self.top, self.top + self.cell_size * self.height, self.cell_size):
                if i < mouse_pos[1]:
                    y += 1
            return x, y
        else:
            return None

    def get_click(self, mouse_pos):
        cell = self.get_cell(mouse_pos)
        if cell:
            self.on_click(cell)

    def on_click(self, cell):
        if self.board[cell[1]][cell[0]] == 0:
            self.board[cell[1]][cell[0]] = 1
            self.sorniak()
        elif self.board[cell[1]][cell[0]] == -1:
            self.board[cell[1]][cell[0]] = 0

    def sorniak(self):
        i, j = random.randrange(self.height), random.randrange(self.width)

        while self.board[i][j] == 1 or self.board[i][j] == -1:
            i, j = random.randrange(self.height), random.randrange(self.width)

        self.board[i][j] = -1

    def update(self):
        for i in range(self.height):
            for j in range(self.width):
                if self.board[i][j] == 1 or self.board[i][j] == 2:
                    self.board[i][j] += 1
                elif self.board[i][j] == -1 or self.board[i][j] == -2:
                    self.board[i][j] -= 1


class Bottom:
    def __init__(self, w, h):
        self.w = w
        self.h = h

    def draw(self):
        color = pygame.Color('#FFAA00')
        #pygame.draw.rect(screen, color,
        #                 (int(self.w * 0.1), int(self.h * 0.85), int(self.w * 0.1), int(self.h * 0.15)))  # панель выбора растения
        #pygame.draw.rect(screen, color,
        #                 (int(self.w * 0.25), int(self.h * 0.85), int(self.w * 0.1), int(self.h * 0.15)))  # мотыга, грабля
        pygame.draw.rect(screen, color,
                         (int(self.w * 0.79), int(self.h * 0.85), int(self.w * 0.2), int(self.h * 0.15)))  # меню
        pygame.draw.rect(screen, color, (self.w * 0.6, 0, self.w * 0.3, self.h * 0.12))


class Weed(pygame.sprite.Sprite):
    image_1 = pygame.transform.scale(load_image("weed_1.png"), (int(height*0.11), int(height*0.11)))
    image_2 = pygame.transform.scale(load_image("weed_2.png"), (int(height*0.11), int(height*0.11)))
    image_3 = pygame.transform.scale(load_image("weed_3.png"), (int(height*0.11), int(height*0.11)))

    def __init__(self, w, h, level, *group):
        super().__init__(*group)
        if level == -1:
            self.image = Weed.image_1
        elif level == -2:
            self.image = Weed.image_2
        else:
            self.image = Weed.image_3
        self.rect = self.image.get_rect()

        self.rect.x = w
        self.rect.y = h


class Plant(pygame.sprite.Sprite):
    image_1 = pygame.transform.scale(load_image("plant_1.png"), (int(height*0.11), int(height*0.11)))
    image_2 = pygame.transform.scale(load_image("plant_2.png"), (int(height*0.11), int(height*0.11)))
    image_3 = pygame.transform.scale(load_image("plant_3.png"), (int(height*0.11), int(height*0.11)))

    def __init__(self, w, h, level, *group):
        super().__init__(*group)
        if level == 1:
            self.image = Plant.image_1
        elif level == 2:
            self.image = Plant.image_2
        else:
            self.image = Plant.image_3
        self.rect = self.image.get_rect()

        self.rect.x = w
        self.rect.y = h


board = Board(8, 6, width, height)
Bottom(width, height).draw()

board.render()
pygame.display.flip()
p = 0

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            board.get_click(event.pos)
            board.render()
            p += 1
    if p == 3:
        board.update()
        p = 0

    pygame.display.flip()
    all_sprites.draw(screen)

pygame.quit()