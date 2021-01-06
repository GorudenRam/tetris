import pygame
from random import choice


FIGURES = ['Z', 'reverse_Z', 'L', 'reverse_L', 'I', 'cube', 'triple']


class Board:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.board = [[False] * width for _ in range(height)]
        self.left = 10
        self.top = 10
        self.cell_size = 30

    def set_view(self, left, top, cell_size):
        self.left = left
        self.top = top
        self.cell_size = cell_size

    def get_cell(self, mouse_pos):
        x, y = mouse_pos
        if x < self.left or y < self.top\
                or x > self.left + self.cell_size * self.width - 1\
                or y > self.top + self.cell_size * self.height - 1:
            return None
        else:
            return (x - self.left) // self.cell_size, (y - self.top) // self.cell_size

    def render(self):
        for i in range(self.height):
            for j in range(self.width):
                if board.board[i][j]:
                    pygame.draw.rect(screen, self.board[i][j], (self.left + j * self.cell_size,
                                                                self.top + i * self.cell_size,
                                                                self.cell_size, self.cell_size), 0)
                    pygame.draw.rect(screen, 'white', (self.left + j * self.cell_size,
                                                       self.top + i * self.cell_size,
                                                       self.cell_size, self.cell_size), 1)


class Figure:
    def __init__(self, type):
        self.type = type
        self.centre_x = 5
        self.centre_y = 0
        if self.type == 'Z':
            self.elements = [[self.centre_y + 1, self.centre_x - 1],
                             [self.centre_y + 1, self.centre_x],
                             [self.centre_y, self.centre_x],
                             [self.centre_y, self.centre_x + 1]]
        elif self.type == 'reverse_Z':
            self.elements = [[self.centre_y + 1, self.centre_x + 1],
                             [self.centre_y + 1, self.centre_x],
                             [self.centre_y, self.centre_x],
                             [self.centre_y, self.centre_x - 1]]
        elif self.type == 'L':
            self.elements = [[self.centre_y + 1, self.centre_x - 1],
                             [self.centre_y, self.centre_x - 1],
                             [self.centre_y, self.centre_x],
                             [self.centre_y, self.centre_x + 1]]
        elif self.type == 'reverse_L':
            self.elements = [[self.centre_y + 1, self.centre_x + 1],
                             [self.centre_y, self.centre_x + 1],
                             [self.centre_y, self.centre_x],
                             [self.centre_y, self.centre_x - 1]]
        elif self.type == 'I':
            self.elements = [[self.centre_y, self.centre_x - 2],
                             [self.centre_y, self.centre_x - 1],
                             [self.centre_y, self.centre_x],
                             [self.centre_y, self.centre_x + 1]]
        elif self.type == 'cube':
            self.elements = [[self.centre_y + 1, self.centre_x - 1],
                             [self.centre_y, self.centre_x - 1],
                             [self.centre_y, self.centre_x],
                             [self.centre_y + 1, self.centre_x]]
        elif self.type == 'triple':
            self.elements = [[self.centre_y, self.centre_x - 1],
                             [self.centre_y, self.centre_x + 1],
                             [self.centre_y, self.centre_x],
                             [self.centre_y + 1, self.centre_x]]

    def can_go_right(self):
        for i in self.elements:
            if i[1] + 1 >= 10 or board.board[i[0]][i[1] + 1]:
                return False
        return True

    def can_go_left(self):
        for i in self.elements:
            if i[1] - 1 < 0 or board.board[i[0]][i[1] - 1]:
                return False
        return True

    def can_rotate_clockwise(self):
        pass

    def can_rotate_counterclockwise(self):
        pass

    def rotate_clockwise(self):
        pass

    def rotate_counterclockwise(self):
        pass

    def fall(self):
        for i in self.elements:
            if i[0] + 1 >= 20 or board.board[i[0] + 1][i[1]]:
                return False
        for i in self.elements:
            i[0] += 1
        self.centre_y += 1
        return True

    def draw(self):
        for i in self.elements:
            pygame.draw.rect(screen, 'blue', (board.left + i[1] * board.cell_size,
                                              board.top + i[0] * board.cell_size,
                                              board.cell_size, board.cell_size), 0)
            pygame.draw.rect(screen, 'white', (board.left + i[1] * board.cell_size,
                                               board.top + i[0] * board.cell_size,
                                               board.cell_size, board.cell_size), 1)


def game_over():
    pass


if __name__ == '__main__':
    pygame.init()
    pygame.display.set_caption('Тетрис')
    size = width, height = (1280, 960)
    screen = pygame.display.set_mode(size)
    board = Board(10, 20)
    board.set_view(480, 100, 35)
    next_figure = Figure(choice(FIGURES))
    figure = Figure(choice(FIGURES))
    figure.draw()
    pygame.display.flip()
    clock = pygame.time.Clock()
    need_count = 60
    count = 0
    running = True
    while running:
        clock.tick(60)
        count += 1
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    if figure.can_go_left():
                        for i in figure.elements:
                            i[1] -= 1
                            figure.centre_x -= 1
                        screen.fill((0, 0, 0))
                        figure.draw()
                        board.render()
                        pygame.display.flip()
                if event.key == pygame.K_RIGHT:
                    if figure.can_go_right():
                        for i in figure.elements:
                            i[1] += 1
                        figure.centre_x += 1
                        screen.fill((0, 0, 0))
                        figure.draw()
                        board.render()
                        pygame.display.flip()
                if event.key == pygame.K_UP:
                    pass
                if event.key == pygame.K_DOWN:
                    figure.fall()
        if count == need_count:
            count = 0
            if not figure.fall():
                if board.board[0][5]:
                    game_over()
                else:
                    for i in figure.elements:
                        board.board[i[0]][i[1]] = 'red'
                    figure = next_figure
                    next_figure = Figure(choice(FIGURES))
                    for i in range(board.height):
                        is_full = True
                        for j in range(board.width):
                            if not board.board[i][j]:
                                is_full = False
                        if is_full:
                            for k in range(i, 0, -1):
                                for j in range(board.width):
                                    board.board[k][j] = board.board[k - 1][j]
                            board.board[0] = [False] * board.width
        screen.fill((0, 0, 0))
        figure.draw()
        board.render()
        pygame.display.flip()
    pygame.quit()
