import pygame
import os
from random import choice
pygame.init()
pygame.display.set_caption('Тетрис')
size = width, height = (1280, 960)
screen = pygame.display.set_mode(size)


def load_image(name, color_key=None):
    fullname = os.path.join('data', name)
    image = pygame.image.load(fullname)
    if color_key is not None:
        if color_key == -1:
            color_key = image.get_at((0, 0))
        image.set_colorkey(color_key)
    else:
        image = image.convert_alpha()
    return image


FIGURES = ['Z', 'reverse_Z', 'L', 'reverse_L', 'I', 'cube', 'triple']
CUBE_IMAGE = load_image('cube.png')


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
                    if i >= 0:
                        sprite = pygame.sprite.Sprite()
                        sprite.image = CUBE_IMAGE
                        sprite.rect = sprite.image.get_rect()
                        sprite.rect.x = board.left + j * board.cell_size
                        sprite.rect.y = board.top + i * board.cell_size
                        cubes_sprites.add(sprite)


class Figure:
    def __init__(self, type):
        self.type = type
        self.centre_x = 5
        self.centre_y = 0
        self.pose = 0
        if self.type == 'Z':
            self.poses_elements = (((1, 1), (1, 0), (0, 0), (0, -1)),
                                   ((-1, 1), (0, 1), (0, 0), (1, 0)))
        elif self.type == 'reverse_Z':
            self.poses_elements = (((1, -1), (1, 0), (0, 0), (0, 1)),
                                   ((1, 1), (0, 1), (0, 0), (-1, 0)))
        elif self.type == 'L':
            self.poses_elements = (((1, -1), (0, -1), (0, 0), (0, 1)),
                                   ((-1, -1), (-1, 0), (0, 0), (1, 0)),
                                   ((-1, 1), (0, 1), (0, 0), (0, -1)),
                                   ((1, 1), (1, 0), (0, 0), (-1, 0)))
        elif self.type == 'reverse_L':
            self.poses_elements = (((1, 1), (0, 1), (0, 0), (0, -1)),
                                   ((1, -1), (1, 0), (0, 0), (-1, 0)),
                                   ((-1, -1), (0, -1), (0, 0), (0, 1)),
                                   ((-1, 1), (-1, 0), (0, 0), (1, 0)))
        elif self.type == 'I':
            self.poses_elements = (((0, -2), (0, -1), (0, 0), (0, 1)),
                                   ((-2, 0), (-1, 0), (0, 0), (1, 0)))
        elif self.type == 'cube':
            self.poses_elements = (((1, -1), (0, -1), (0, 0), (1, 0)),)
        elif self.type == 'triple':
            self.poses_elements = (((0, -1), (0, 1), (0, 0), (1, 0)),
                                   ((-1, 0), (1, 0), (0, 0), (0, -1)),
                                   ((0, -1), (0, 1), (0, 0), (-1, 0)),
                                   ((-1, 0), (1, 0), (0, 0), (0, 1)))
        self.get_elements()

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

    def rotate_clockwise(self):
        self.pose += 1
        self.pose %= len(self.poses_elements)
        self.get_elements()
        for i in self.elements:
            if i[0] >= 20 or i[1] >= 10 or i[1] < 0 or (board.board[i[0]][i[1]] and i[0] >= 0):
                self.rotate_counterclockwise()
                break

    def rotate_counterclockwise(self):
        self.pose -= 1
        self.pose %= len(self.poses_elements)
        self.get_elements()
        for i in self.elements:
            if i[0] >= 20 or i[1] >= 10 or i[1] < 0 or (board.board[i[0]][i[1]] and i[0] >= 0):
                self.rotate_clockwise()
                break

    def fall(self):
        for i in self.elements:
            if i[0] + 1 >= 20 or (board.board[i[0] + 1][i[1]] and i[0] + 1 >= 0):
                return False
        for i in self.elements:
            i[0] += 1
        self.centre_y += 1
        return True

    def render(self):
        for i in self.elements:
            if i[0] >= 0:
                sprite = pygame.sprite.Sprite()
                sprite.image = CUBE_IMAGE
                sprite.rect = sprite.image.get_rect()
                sprite.rect.x = board.left + i[1] * board.cell_size
                sprite.rect.y = board.top + i[0] * board.cell_size
                cubes_sprites.add(sprite)

    def get_elements(self):
        self.elements = []
        for i in self.poses_elements[self.pose]:
            self.elements.append([self.centre_y + i[0], self.centre_x + i[1]])


def game_over():
    pass


if __name__ == '__main__':
    board = Board(10, 20)
    board.set_view(480, 100, 35)
    next_figure = Figure(choice(FIGURES))
    figure = Figure(choice(FIGURES))
    cubes_sprites = pygame.sprite.Group()
    figure.render()
    cubes_sprites.draw(screen)
    pygame.display.flip()
    clock = pygame.time.Clock()
    need_count = 120
    count = 0
    running = True
    while running:
        clock.tick(120)
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
                        cubes_sprites = pygame.sprite.Group()
                        figure.render()
                        board.render()
                        cubes_sprites.draw(screen)
                        pygame.display.flip()
                if event.key == pygame.K_RIGHT:
                    if figure.can_go_right():
                        for i in figure.elements:
                            i[1] += 1
                        figure.centre_x += 1
                        screen.fill((0, 0, 0))
                        cubes_sprites = pygame.sprite.Group()
                        figure.render()
                        board.render()
                        cubes_sprites.draw(screen)
                        pygame.display.flip()
                if event.key == pygame.K_a:
                    figure.rotate_counterclockwise()
                if event.key == pygame.K_z:
                    figure.rotate_counterclockwise()
                if event.key == pygame.K_s:
                    figure.rotate_clockwise()
                if event.key == pygame.K_x:
                    figure.rotate_clockwise()
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
        cubes_sprites = pygame.sprite.Group()
        figure.render()
        board.render()
        cubes_sprites.draw(screen)
        pygame.display.flip()
    pygame.quit()
