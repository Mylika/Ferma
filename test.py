import pygame
import random
import os
import sys
from subprocess import call

# Получение данных о расположении растений
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

screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
size = width, height = screen.get_size()
# size = width, height = 1024, 860
# screen = pygame.display.set_mode(size)
screen.fill('#C0F400')


def load_image(name, colorkey=-9):
    fullname = os.path.join('data', name)
    # если файл не существует, то выходим
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    # if colorkey is not None:
    # if colorkey is not None:
    #    image = image.convert()
    #    if colorkey == -1:
    #        colorkey = image.get_at((0, 0))
    #    image.set_colorkey(colorkey)
    # else:
    # else:
    image = image.convert_alpha()
    image1 = pygame.transform.scale(image, (100, 100))
    return image1


class Board:
    def __init__(self, left, top, save):
        self.width = 12
        self.height = 8
        # Если еть данные загружаем их на поле, иначе заполняем поле пустыми клетками
        if len(save) > 1:
            self.board = save
        else:
            self.board = [['0'] * width for _ in range(height)]

        self.left = int(left * 0.07)
        self.top = int(top * 0.2)
        self.cell_size = int(top * 0.09)

    def render(self):
        all_sprites.empty()  # очищаем группу спайтов во избежание наложений
        x, y = self.left, self.top
        for i in range(self.height):
            for j in range(self.width):
                # Отрсовываем сетку грядок
                pygame.draw.rect(screen, '#573B08', (x, y, self.cell_size, self.cell_size), 1)
                # Отрисовываем грядки
                pygame.draw.rect(screen, '#865F1A', (x + 1, y + 1, self.cell_size - 2, self.cell_size - 2))
                # Если на грядке есть растение или сорняк, то отрисоваваем его спрайт
                if int(self.board[i][j]) >= 1:
                    Plant(x, y, int(self.board[i][j]), all_sprites)
                elif int(self.board[i][j]) <= -1:
                    Weed(x, y, int(self.board[i][j]), all_sprites)
                x += self.cell_size
            x = self.left
            y += self.cell_size

    def get_cell(self, mouse_pos):
        # Сложная система опредиления выбрана ли грядка
        if self.left <= mouse_pos[0] <= self.left + self.cell_size * self.width and \
                self.top <= mouse_pos[1] <= self.top + self.cell_size * self.height:
            x, y = - 1, -1

            # Не менее сложная сиситема получения координат шрядки
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
        # Проверка выбрана ли грядка
        if cell:
            self.on_click(cell)

    def on_click(self, cell):
        # Пытаемся понять что от нас хотет пользоваель
        # Если грядка пустая, то садим растение
        if self.board[cell[1]][cell[0]] == '0':
            self.board[cell[1]][cell[0]] = '1'
        # Если выбран сорняк, удаляем сорняк
        elif int(self.board[cell[1]][cell[0]]) <= -1:
            self.board[cell[1]][cell[0]] = '0'
        self.save()  # Сохраняем изменения

    def sorniak(self):
        # Выбираем клетку для расположения сорняка
        i, j = random.randrange(self.height), random.randrange(self.width)

        # Проверяем не занята ли грядка
        while self.board[i][j] != '0':
            i, j = random.randrange(self.height), random.randrange(self.width)

        self.board[i][j] = '-1'

    def update(self):
        # Повышаем уровень растений и сорняков на один
        for i in range(self.height):
            for j in range(self.width):
                if self.board[i][j] == '1' or self.board[i][j] == '2':
                    self.board[i][j] = str(int(self.board[i][j]) + 1)
                elif self.board[i][j] == '-1' or self.board[i][j] == '-2':
                    self.board[i][j] = str(int(self.board[i][j]) - 1)
        # Выращиваем ещё два сорняка
        # Возожно это можно было сделать проще, но мне влом переписывать код
        self.sorniak()
        self.sorniak()
        self.save()  # сохраняем изменения

    def save(self):
        # Кое-как записываем данные поля в txt
        save_data = open("Save.txt", 'w')
        for elem in self.board:
            save_data.write(', '.join(elem) + '\n')
        save_data.close()


class Weed(pygame.sprite.Sprite):
    # Сразу загружаем три картинки, потому что иначе не  работае
    # Ну или я не знаю как это делать проще
    image_1 = pygame.transform.scale(load_image("weed_1.png"), (int(height * 0.09), int(height * 0.09)))
    image_2 = pygame.transform.scale(load_image("weed_2.png"), (int(height * 0.09), int(height * 0.09)))
    image_3 = pygame.transform.scale(load_image("weed_3.png"), (int(height * 0.09), int(height * 0.09)))

    def __init__(self, w, h, level, *group):
        super().__init__(*group)
        # сморим какий уровень выбран и загружаем нужную картинку
        if level == -1:
            self.image = Weed.image_1
        elif level == -2:
            self.image = Weed.image_2
        else:
            self.image = Weed.image_3
        self.rect = self.image.get_rect()

        # Сразу располагаем сорняк на нужное место
        self.rect.x = w
        self.rect.y = h


class Plant(pygame.sprite.Sprite):
    # Тож самое, что и в классе Weed
    # Скорее всего их можно было объединить но я тупой
    image_1 = pygame.transform.scale(load_image("plant_1.png"), (int(height * 0.09), int(height * 0.09)))
    image_2 = pygame.transform.scale(load_image("plant_2.png"), (int(height * 0.09), int(height * 0.09)))
    image_3 = pygame.transform.scale(load_image("plant_3.png"), (int(height * 0.09), int(height * 0.09)))

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


# Тут мы инициализируем какие-то кнопки
# Спасибо за говорящие названия
# Переименуй, пожалуйста
im = pygame.transform.scale(load_image("кнопка.png"), (int(width * 0.13), int(height * 0.087)))
but = pygame.sprite.Sprite(bk)
but.image = im
but.rect = but.image.get_rect()
but.rect.x = int(width * 0.7)
but.rect.y = int(height * 0.03)

im = pygame.transform.scale(load_image("кнопка2.png"), (int(width * 0.13), int(height * 0.087)))
buts = pygame.sprite.Sprite(bk)
buts.image = im
buts.rect = buts.image.get_rect()
buts.rect.x = int(width * 0.85)
buts.rect.y = int(height * 0.03)

# Создаём поле
board = Board(width, height, data)

# отображаем поле
board.render()
pygame.display.flip()
act = 0  # Видишь я переименовала p
# Теперь это act  гораздо понятнее зачем он

running = True
while running:
    for event in pygame.event.get():
        # если выход,то входим
        # я не знаю зачем это, если у нас полноэкранный режим, но пусть будет
        # Надеюсь нам не снизят за это балл
        if event.type == pygame.QUIT:
            running = False
        # Если нажата любая кнопка, то выходим
        # Надо не забыть убрать
        if event.type == pygame.KEYDOWN:
            running = False
        # Выходим если гажота какая-то кнопка
        # Серьёно назови кнопку адекватно
        if event.type == pygame.MOUSEBUTTONDOWN and buts.rect.collidepoint(event.pos):
            running = False
        # А если мы нажмём на эту кнопку, то попадём в меню
        if event.type == pygame.MOUSEBUTTONDOWN and but.rect.collidepoint(event.pos):
            call(["python", "menu.py"])
            # Не забываем выходить во избежание ошибок
            # Добавь строчку quit() в muny.py после вызова call
            # Я надеюсь ты поняла
            running = False
        # Если пользователь тыкнул на мышь, то смотрим что он хотел сделать
        # Ну и на всякий рендарим, а то мало ли, вдруг не случайно нажал
        if event.type == pygame.MOUSEBUTTONDOWN:
            board.get_click(event.pos)
            board.render()
            act += 1  # Добавляем действие
            # Интересное наблюдение, если поьзавательтыкнул случайно, то дейсвие тоже будет защитано
            # Надо пофксить
    # Если кол-во действий досигло трёх, то запускаем новый день
    # И апгрейдим растения, сорняки и сажаем новые сорняки
    if act == 3:
        board.update()
        board.render()
        act = 0

    pygame.display.flip()
    all_sprites.draw(screen)
    bk.draw(screen)

pygame.quit()

# На этом всё
# Спасибо за прочтение данного кода
# Сори за грамматику
