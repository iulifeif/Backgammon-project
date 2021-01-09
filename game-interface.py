# import pygame module in this program
import pygame
import sys
import numpy as np

pygame.init()

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BROWN = (150, 75, 0)

SQUARESIZE = 100
COLUMN_COUNT = 12
ROW_COUNT = 6
width = SQUARESIZE * (COLUMN_COUNT + 1)
height = SQUARESIZE * ROW_COUNT
size = (width, height)
RADIUS = int(SQUARESIZE / 2 - 5)


def create_board():
    board = np.zeros((ROW_COUNT, COLUMN_COUNT))
    return board


def draw_board(board):
    for index_column in range(COLUMN_COUNT):
        for index_line in range(ROW_COUNT):
            pygame.draw.rect(screen, GREEN,
                             (index_column * SQUARESIZE, index_line * SQUARESIZE + SQUARESIZE, SQUARESIZE, SQUARESIZE))
            pygame.draw.circle(screen, BLACK,
                               (int(index_column * SQUARESIZE + SQUARESIZE / 2),
                                int(index_line * SQUARESIZE + SQUARESIZE + SQUARESIZE / 2)),
                               RADIUS)


if __name__ == '__main__':
    # infinite loop
    game_over = False
    while not game_over:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                print(event.pos)
        screen = pygame.display.set_mode(size)
        board = create_board()
        draw_board(board)
        pygame.display.update()
