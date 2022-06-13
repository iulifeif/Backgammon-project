# import pygame module in this program
import random

import pygame
import sys
import numpy as np

from utils.utils import load_sprite

pygame.init()

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BROWN = (150, 75, 0)

SQUARESIZE = 50
COLUMN_COUNT = 12
ROW_COUNT = 16
width = 800
height = 800
size = (width, height)
RADIUS = int(SQUARESIZE / 2 - 5)


def create_board():
    board = np.zeros((ROW_COUNT, COLUMN_COUNT))
    return board


def prepro(table):
    up_table = table[len(table) // 2:]
    intermediar_down_table = table[:len(table) // 2]
    down_table = []
    for pos in reversed(range(len(intermediar_down_table))):
        down_table.append(intermediar_down_table[pos])
    return up_table, down_table


# def draw_pieces(table, pos):
#     for col in range(len(table)):
#         line = pos
#         while table[col] != 0:
#             if table[col] < 0:
#                 pygame.draw.circle(screen, BROWN,
#                                    (int(col * SQUARESIZE + SQUARESIZE / 2),
#                                     int(line * SQUARESIZE + SQUARESIZE + SQUARESIZE / 2)),
#                                    RADIUS)
#                 table[col] += 1
#             elif table[col] > 0:
#                 pygame.draw.circle(screen, WHITE,
#                                    (int(col * SQUARESIZE + SQUARESIZE / 2),
#                                     int(line * SQUARESIZE + SQUARESIZE + SQUARESIZE / 2)),
#                                    RADIUS)
#                 table[col] -= 1
#
#             line = line + 1 if pos == 0 else line - 1


def draw_board(board, table):
    screen.blit(load_sprite("main_back", False), (0, 0))
    # for index_column in range(COLUMN_COUNT):
    #     for index_line in range(ROW_COUNT):
    #         pygame.draw.rect(screen, GREEN,
    #                          (index_column * SQUARESIZE, index_line * SQUARESIZE + SQUARESIZE, SQUARESIZE, SQUARESIZE))
    #         if index_line != 7:
    #             pygame.draw.circle(screen, BLACK,
    #                                (int(index_column * SQUARESIZE + SQUARESIZE / 2),
    #                                 int(index_line * SQUARESIZE + SQUARESIZE + SQUARESIZE / 2)),
    #                                RADIUS)
    # up_table, down_table = prepro(table)
    # draw_pieces(up_table, 0)
    # draw_pieces(down_table, 14)


def end_game(player_who_won):
    screen = pygame.display.set_mode((800, 800))
    screen.fill(BLACK)
    sprite = load_sprite("banner", True)
    blit_position = pygame.Vector2((200, 200))
    screen.blit(sprite, blit_position)
    # return the position if someone click
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            # check if a mouse is clicked
            if event.type == pygame.MOUSEBUTTONDOWN:
                col, line = event.pos
                if 300 <= col <= 390 and 590 <= line <= 630:
                    print("4")
                    return 4
                elif 400 <= col <= 500 and 590 <= line <= 630:
                    print("5")
        col, line = pygame.mouse.get_pos()
        # draw the shades
        # for human vs human
        if 310 <= col <= 460 and 540 <= line <= 580:
            pygame.draw.rect(screen, RED, [310, 540, 150, 40], border_radius=30)
        # coords for human vs computer
        elif 360 <= col <= 425 and 590 <= line <= 630:
            pygame.draw.rect(screen, RED, [360, 590, 65, 40], border_radius=30)
        else:
            #  erase the shades
            pygame.draw.rect(screen, BLACK, [310, 540, 150, 40], border_radius=30)
            pygame.draw.rect(screen, BLACK, [360, 590, 65, 40], border_radius=30)
        font_announce = pygame.font.SysFont("Roboto", 40)
        font_title = pygame.font.SysFont("Roboto", 30)
        if player_who_won == 0:
            text = font_announce.render("Player WHITE won!! Congrats!!", True, WHITE)
        else:
            text = font_announce.render("Player BLACK won!! Congrats!!", True, WHITE)
        screen.blit(text, (180, 400))
        text = font_title.render("Back to Menu", True, WHITE)
        screen.blit(text, (320, 550))
        text = font_title.render("Exit", True, WHITE)
        screen.blit(text, (372, 600))

        pygame.display.update()


if __name__ == '__main__':

    selected_piece = 0
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                print(event.pos)
        end_game(1)
    # font = pygame.font.Font(None, 28)
    #
    # # infinite loop
    # table = [2, 0, 0, 0, 0, -5, 0, -3, 0, 0, 0, 5, -5, 0, 0, 0, 3, 0, 5, 0, 0, 0, 0, -2]
    # screen = pygame.display.set_mode(size)
    # game_over = False
    # board = create_board()
    # draw_board(board, table)
    # # partea de sus
    # sprite = load_sprite("black_got", True)
    # blit_position = pygame.Vector2((680, 135))
    # screen.blit(sprite, blit_position)
    # blit_position = pygame.Vector2((630, 135))
    # screen.blit(sprite, blit_position)
    # blit_position = pygame.Vector2((680, 180))
    # screen.blit(sprite, blit_position)
    # blit_position = pygame.Vector2((680 - 12 * 50, 135))
    # screen.blit(sprite, blit_position)
    # # partea de jos
    # sprite = load_sprite("white_got", True)
    # blit_position = pygame.Vector2((680, 730))
    # screen.blit(sprite, blit_position)
    # blit_position = pygame.Vector2((680, 685))
    # screen.blit(sprite, blit_position)
    # blit_position = pygame.Vector2((630, 730))
    # screen.blit(sprite, blit_position)
    # blit_position = pygame.Vector2((680 - 12 * 50, 730))
    # screen.blit(sprite, blit_position)
    # # piesele de pe mijloc
    # blit_position = pygame.Vector2((380, 300))
    # screen.blit(sprite, blit_position)
    # blit_position = pygame.Vector2((380, 350))
    # screen.blit(sprite, blit_position)
    # blit_position = pygame.Vector2((380, 570))
    # screen.blit(sprite, blit_position)
    # blit_position = pygame.Vector2((380, 520))
    # screen.blit(sprite, blit_position)
    # # player turn
    # sprite = load_sprite("turn_light", True)
    # blit_position = pygame.Vector2((287, 1))
    # screen.blit(sprite, blit_position)
    # blit_position = pygame.Vector2((430, 1))
    # screen.blit(sprite, blit_position)
    # # unde muta playerul sus
    # sprite = load_sprite("destination_light", True)
    # blit_position = pygame.Vector2((72, 115))
    # screen.blit(sprite, blit_position)
    # blit_position = pygame.Vector2((222, 115))
    # screen.blit(sprite, blit_position)
    # blit_position = pygame.Vector2((272, 115))
    # screen.blit(sprite, blit_position)
    # # unde muta playerul jos
    # sprite = load_sprite("destination_light_bottom", True)
    # blit_position = pygame.Vector2((222, 500))
    # screen.blit(sprite, blit_position)
    # blit_position = pygame.Vector2((272, 500))
    # screen.blit(sprite, blit_position)
    # # dice roll
    # sprite = load_sprite("dice_button", True)
    # blit_position = pygame.Vector2((743, 382))
    # screen.blit(sprite, blit_position)
    # # dice
    # dice1 = str(random.randint(1, 6))
    # dice2 = str(random.randint(1, 6))
    # sprite = load_sprite("white_dice_" + dice1, True)
    # blit_position = pygame.Vector2((450, 390))
    # screen.blit(sprite, blit_position)
    # sprite = load_sprite("white_dice_" + dice1, True)
    # blit_position = pygame.Vector2((500, 390))
    # screen.blit(sprite, blit_position)
    # sprite = load_sprite("white_dice_" + dice1, True)
    # blit_position = pygame.Vector2((450, 450))
    # screen.blit(sprite, blit_position)
    # sprite = load_sprite("white_dice_" + dice1, True)
    # blit_position = pygame.Vector2((500, 450))
    # screen.blit(sprite, blit_position)
    # # piesele scoase afara
    # # negre
    # sprite = load_sprite("black_beard_off", True)
    # blit_position = pygame.Vector2((750, 344))
    # screen.blit(sprite, blit_position)
    # sprite = load_sprite("black_beard_off", True)
    # blit_position = pygame.Vector2((750, 355))
    # screen.blit(sprite, blit_position)
    # sprite = load_sprite("black_beard_off", True)
    # blit_position = pygame.Vector2((750, 366))
    # screen.blit(sprite, blit_position)
    # # albe
    # sprite = load_sprite("white_beard_off", True)
    # blit_position = pygame.Vector2((750, 733))
    # screen.blit(sprite, blit_position)
    # sprite = load_sprite("white_beard_off", True)
    # blit_position = pygame.Vector2((750, 744))
    # screen.blit(sprite, blit_position)
    # sprite = load_sprite("white_beard_off", True)
    # blit_position = pygame.Vector2((750, 755))
    # screen.blit(sprite, blit_position)
    #
    # # draw end game
    # end_game()
    #
    # selected_piece = 0
    # while not game_over:
    #     for event in pygame.event.get():
    #         if event.type == pygame.QUIT:
    #             game_over = True
    #             sys.exit()
    #         if event.type == pygame.MOUSEBUTTONDOWN:
    #             print(event.pos)
    #         pygame.display.update()
