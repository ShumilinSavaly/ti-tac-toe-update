import pygame as pg

BLACK = (0,) * 3
GRAY = (100,) * 3
WHITE = (255,) * 3
RED = (255, 0, 0)

CROSS = '#db049e'
CIRCLE = '#04cddb'

pg.init()
W, H = 600, 600
screen = pg.display.set_mode((W, H))


def draw_circle(sc, x, y, size):
    x = (x + 0.5) * size
    y = (y + 0.5) * size
    pg.draw.circle(sc, CIRCLE, (x, y), (size - 3) // 2, 3)


def draw_cross(sc, x, y, size):
    x = x * size + 3
    y = y * size + 3
    pg.draw.line(sc, CROSS, (x, y), (x + size - 3, y + size - 3), 3)
    pg.draw.line(sc, CROSS, (x + size - 3, y - 3), (x, y + size - 3), 3)


def is_end(board):
    def check_line(x, i):
        if x[i][0] == x[i][1] == x[i][2] != 0:
            return True

    def check_col(x, i):
        if x[0][i] == x[i][1] == x[2][i] != 0:
            return True

    def check_main_diag(x):
        if x[0][0] == x[1][1] == x[2][2] != 0:
            return True

    def check_secondary_diag(x):
        if x[0][2] == x[1][1] == x[2][0] != 0:
            return True

    for i in range(3):
        if check_line(board, i):
            return 'line', i

        if check_col(board, i) == True:
            return 'col', i

    if check_main_diag(board) == True:
        return 'diag', 1

    if check_secondary_diag(board) == True:
        return 'diag', 2


class Board:
    def __init__(self, W, H, size):
        self.W, self.H = W, H
        self.size = size
        self.board = [
            [0, 0, 0],
            [0, 0, 0],
            [0, 0, 0]
        ]
        self.move = 1

    def click(self, mouse_pos):
        x = mouse_pos[0] // self.size
        y = mouse_pos[1] // self.size
        self.board[y][x] = self.move
        self.move = -self.move

    def render(self, screen):
        pg.draw.line(screen, WHITE, (0, 200), (self.W, 200))
        pg.draw.line(screen, WHITE, (0, 400), (self.W, 400))
        pg.draw.line(screen, WHITE, (200, 0), (200, self.H))
        pg.draw.line(screen, WHITE, (400, 0), (400, self.H))
        for y in range(3):
            for x in range(3):
                if self.board[y][x] == 1:
                    draw_cross(screen, x, y, self.size)
                elif self.board[y][x] == -1:
                    draw_circle(screen, x, y, self.size)

    def check_end(self):
        global x0, y0, x1, y1
        is_end_info = is_end(self.board)
        if is_end_info is not None:
            type_end = is_end_info[0]
            number = is_end_info[1]
            if type_end == 'line':
                x0 = 0
                y0 = (number + 0.5) * self.size
                x1 = self.W
                y1 = (number + 0.5) * self.size

            if type_end == 'col':
                x0 = (number + 0.5) * self.size
                y0 = 0
                x1 = (number + 0.5) * self.size
                y1 = self.H

            if type_end == 'diag':
                if number == 1:
                    x0, y0 = 0, 0
                    x1 = self.W, self.H
                if number == 2:
                    x0, y0 = self.W, 0
                    x1, y1 = 0, self.H

            pg.draw.line(screen, RED, (x0, y0), (x1, y1), 10)
            pg.display.update()
            pg.time.delay(3000)
            return True
        else:

            return False


board = Board(W, H, 200)
while True:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            exit()
        if event.type == pg.MOUSEBUTTONDOWN:
            board.click(event.pos)

    screen.fill(BLACK)
    board.render(screen)
    pg.display.update()

    keys = pg.key.get_pressed()
    if keys[pg.K_ESCAPE] or board.check_end():
        pg.quit()
        exit()
