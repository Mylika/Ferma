import pygame
import os
import sys

pygame.init()
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
size = width, height = screen.get_size()
screen.fill('#C0F400')


def load_image(name, colorkey=-9):
    fullname = os.path.join('picture', name)
    # если файл не существует, то выходим
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    image1 = pygame.transform.scale(image, (100, 100))
    return image1


all_sprites = pygame.sprite.Group()
sprite_p = pygame.sprite.Sprite()
sprite_p.image = load_image("plant1.jpg")
sprite_p.rect = sprite_p.image.get_rect()
sprite_s = pygame.sprite.Sprite()
sprite_s.image = load_image("trava.png")
sprite_s.rect = sprite_s.image.get_rect()
all_sprites.add(sprite_s)
all_sprites.add(sprite_p)


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
        x, y = self.left, self.top
        for i in range(self.height):
            for j in range(self.width):
                pygame.draw.rect(screen, '#573B08', (x, y, self.cell_size, self.cell_size), 1)
                if self.board[i][j] == 1:
                    pygame.draw.rect(screen, '#644F28', (x + 1, y + 1, self.cell_size - 2, self.cell_size - 2))
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
        sprite_s.rect.x = mouse_pos[0]
        sprite_s.rect.y = mouse_pos[1]

    def on_click(self, cell):
        self.board[cell[1]][cell[0]] = 1


class Bottom:
    def __init__(self, w, h):
        self.w = w
        self.h = h

    def draw(self):
        color = pygame.Color('#FFAA00')
        pygame.draw.rect(screen, color,
                         (int(self.w * 0.1), int(self.h * 0.85), int(self.w * 0.3),
                          int(self.h * 0.15)))  # панель выбора растения
        pygame.draw.rect(screen, color,
                         (int(self.w * 0.45), int(self.h * 0.85), int(self.w * 0.1),
                          int(self.h * 0.15)))  # мотыга, грабля
        pygame.draw.rect(screen, color,
                         (int(self.w * 0.79), int(self.h * 0.85), int(self.w * 0.2), int(self.h * 0.15)))  # меню
        pygame.draw.rect(screen, color, (self.w * 0.6, 0, self.w * 0.3, self.h * 0.12))


board = Board(8, 6, width, height)
Bottom(width, height).draw()

pygame.display.flip()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            board.get_click(event.pos)
            all_sprites.draw(screen)

    board.render()
    pygame.display.flip()

pygame.quit()
