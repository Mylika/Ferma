import pygame


class Board:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.board = [[0] * width for _ in range(height)]

        self.left = 170
        self.top = 130
        self.cell_size = 100

    def set_view(self, left, top, cell_size):
        self.left = left
        self.top = top
        self.cell_size = cell_size

    def render(self):
        x, y = self.left, self.top
        for i in range(self.height):
            for j in range(self.width):
                pygame.draw.rect(screen, '#573B08', (x, y, self.cell_size, self.cell_size), 1)
                if self.board[i][j] ==1:
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

    def on_click(self, cell):
        self.board[cell[1]][cell[0]] = 1


def draw():
    color = pygame.Color('#FFAA00')
    pygame.draw.rect(screen, color, (50, 750, 350, 110))
    pygame.draw.rect(screen, color, (450, 750, 150, 110))
    pygame.draw.rect(screen, color, (900, 750, 200, 110))
    pygame.draw.rect(screen, color, (700, 0, 350, 110))


pygame.init()
size = width, height = 1150, 860
screen = pygame.display.set_mode(size)
screen.fill('#C0F400')

board = Board(8, 6)

draw()
pygame.display.flip()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            board.get_click(event.pos)

    board.render()
    pygame.display.flip()

pygame.quit()