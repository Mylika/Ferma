import pygame
import random
import os
import sys

file = open("Save.txt", encoding="utf-8")
file_data = file.read().rstrip('\n').split('\n')
file.close()
data = []

for i in file_data:
    if i == '':
        data.append([])
    else:
        data.append(i.split(', '))

pygame.init()

all_sprites = pygame.sprite.Group()
bk = pygame.sprite.Group()

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
        self.board = [['0'] * width for _ in range(height)]

        self.left = int(w * 0.05)
        self.top = int(h * 0.1)
        self.cell_size = int(h * 0.09)

    def set_view(self, save):
        if len(save) > 1:
            self.board = save

    def render(self):
        all_sprites.empty()
        self.save()
        x, y = self.left, self.top
        for i in range(self.height):
            for j in range(self.width):
                pygame.draw.rect(screen, '#573B08', (x, y, self.cell_size, self.cell_size), 1)
                if int(self.board[i][j]) >= 1:
                    Plant(x, y, int(self.board[i][j]), all_sprites)
                elif int(self.board[i][j]) <= -1:
                    Weed(x, y, int(self.board[i][j]), all_sprites)
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
        if self.board[cell[1]][cell[0]] == '0':
            self.board[cell[1]][cell[0]] = '1'
        elif int(self.board[cell[1]][cell[0]]) <= -1:
            self.board[cell[1]][cell[0]] = '0'

    def sorniak(self):
        i, j = random.randrange(self.height), random.randrange(self.width)

        while self.board[i][j] != '0':
            i, j = random.randrange(self.height), random.randrange(self.width)

        self.board[i][j] = '-1'

    def update(self):
        for i in range(self.height):
            for j in range(self.width):
                if self.board[i][j] == '1' or self.board[i][j] == '2':
                    self.board[i][j] = str(int(self.board[i][j]) + 1)
                elif self.board[i][j] == '-1' or self.board[i][j] == '-2':
                    self.board[i][j] = str(int(self.board[i][j]) - 1)
        self.sorniak()
        self.sorniak()

    def save(self):
        save_data = open("Save.txt", 'w')
        for elem in self.board:
            save_data.write(', '.join(elem) + '\n')
        save_data.close()


class Weed(pygame.sprite.Sprite):
    image_1 = pygame.transform.scale(load_image("weed_1.png"), (int(height*0.09), int(height*0.09)))
    image_2 = pygame.transform.scale(load_image("weed_2.png"), (int(height*0.09), int(height*0.09)))
    image_3 = pygame.transform.scale(load_image("weed_3.png"), (int(height*0.09), int(height*0.09)))

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
    image_1 = pygame.transform.scale(load_image("plant_1.png"), (int(height*0.09), int(height*0.09)))
    image_2 = pygame.transform.scale(load_image("plant_2.png"), (int(height*0.09), int(height*0.09)))
    image_3 = pygame.transform.scale(load_image("plant_3.png"), (int(height*0.09), int(height*0.09)))

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


board = Board(12, 8, width, height)

board.render()
board.set_view(data)
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
