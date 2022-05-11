import pygame
import sys

from utils import load_sprite
from colors import *


class Interface:
    def __init__(self, table=None, dice1=0, dice2=0,
                 end_pieces0=0, end_pieces1=0,
                 out_pieces0=0, out_pieces1=0):
        """ initialize table with fixed dimensions """
        self.table = table
        self.screen = pygame.display.set_mode((800, 800))
        self.background = load_sprite("main_table", False)
        self.up_table = []
        self.down_table = []
        self.first_dice = dice1
        self.seconf_dice = dice2
        self.end_pieces0 = end_pieces0
        self.end_pieces1 = end_pieces1
        self.out_pieces0 = out_pieces0
        self.out_pieces1 = out_pieces1


    def preprocess_table(self):
        """ split the original table from logic (which is a list) in 2 lists
            one for up site of table and another one for down side
            Args:
                table (int, list): the list which contain pieses, the logical table
            Updated variables:
                up_table: the second half of the logical table
                down_table: the first half of logical table and reversed"""
        # from the middle to the end is up side
        self.up_table = self.table[len(self.table) // 2:]
        intermediary_down_table = self.table[:len(self.table) // 2]
        self.down_table = []
        # from the beginning to the middle is down side, but need to be reversed
        for pos in reversed(range(len(intermediary_down_table))):
            self.down_table.append(intermediary_down_table[pos])

    def draw_pieces(self, side_table):
        """ draw the pieces according to the board received
            and the velue of pieces, because player 0 has negative pieces and player 1 positive pieces
            Args:
                :param side_table: values are: "upper" or "lower" accordingly with the side table"""
        table = self.up_table if side_table == "upper" else self.down_table
        # create a new empty column in the middle for the outer pieces
        table.insert(6, 0)

        for index in range(len(table)):
            nr_pieces = abs(table[index])
            draw_pieces = 0
            piece_color = "white_got" if table[index] >= 1 else "black_got"
            while draw_pieces < nr_pieces:
                sprite = load_sprite(piece_color, True)
                if table == self.up_table:
                    blit_position = pygame.Vector2((80 + index * 50, 135 + draw_pieces * 45))
                else:
                    blit_position = pygame.Vector2((80 + index * 50, 730 - draw_pieces * 45))
                self.screen.blit(sprite, blit_position)
                draw_pieces = draw_pieces + 1

    def draw_outer_pieces(self):
        """ draw the pieces that are taken out of the board
            player 0 at the top, and player 1 at the bottom
            Args:
                out_pieces (int): a number that represents how many pieces removed has the player
                pos (int): the position of the line from which to start drawing the parts"""
        number_draw_pieces = 0
        sprite = load_sprite("white_got", True)
        while number_draw_pieces < self.out_pieces0:
            blit_position = pygame.Vector2((380, 300 + number_draw_pieces * 50))
            self.screen.blit(sprite, blit_position)
            number_draw_pieces = number_draw_pieces + 1
        number_draw_pieces = 0
        sprite = load_sprite("black_got", True)
        while number_draw_pieces < self.out_pieces1:
            blit_position = pygame.Vector2((380, 570 - number_draw_pieces * 50))
            self.screen.blit(sprite, blit_position)
            number_draw_pieces = number_draw_pieces + 1

    def draw_board(self):
        """ the board is drawn as a matrix with green elements
            then add in each square, a black circle, this function also calls the necessary functions for
            preprocessing the table, for draw the pieces from table and pieces outer table
            Args:
                table(int, list): the list which contain pieces,the logical table
                table_out_0 (int): the number that represents how many pieces removed has player 0
                table_out_1 (int): the number that represents how many pieces removed has player 1"""
        # set screen size
        self.screen = pygame.display.set_mode((800, 800))
        self.screen.fill(WHITE)
        self.screen.blit(load_sprite("main_table", False), (0, 0))
        # pygame.display.set_caption("Backgammon")
        # set the background
        # self.background = load_sprite("main_table", False)
        self.preprocess_table()
        self.draw_pieces("upper")
        self.draw_pieces("lower")
        self.draw_outer_pieces()
        pygame.display.update()


def choose_game_mode():
    """ draw the screen for choose the type of player want to play with (Person or Computer)"""
    # draw the table
    screen = pygame.display.set_mode((800, 800))
    screen.fill(BLACK)
    font_title = pygame.font.SysFont("Roboto", 45)
    text_title = font_title.render("Choose the mode: ", True, RED)
    screen.blit(text_title, (800 / 5, 800 / 3))
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            #         check if a mouse is clicked
            if event.type == pygame.MOUSEBUTTONDOWN:
                col, line = event.pos
                # coords for Human
                if 330 <= col <= 560 and 355 <= line <= 405:
                    # which means person
                    return 1
                # coords for Computer
                elif 320 <= col <= 580 and 455 <= line <= 505:
                    # which means computer
                    return 2
        col, line = pygame.mouse.get_pos()
        if 330 <= col <= 560 and 355 <= line <= 405:
            pygame.draw.rect(screen, LIGHT, [330, 355, 230, 50], border_radius=40)
        # coords for Computer
        elif 320 <= col <= 580 and 455 <= line <= 505:
            pygame.draw.rect(screen, LIGHT, [320, 455, 260, 50], border_radius=40)
        else:
            pygame.draw.rect(screen, DARK_SHADE, [330, 355, 230, 50], border_radius=40)
            pygame.draw.rect(screen, DARK_SHADE, [320, 455, 260, 50], border_radius=40)
        font_title = pygame.font.SysFont("Roboto", 30)
        text = font_title.render("Human VS Human", True, RED)
        screen.blit(text, (800 / 2 - 50 + 10,
                           800 / 3 + 50 * 2))
        text = font_title.render("Computer VS Human", True, RED)
        screen.blit(text, (800 / 2 - 50,
                           800 / 3 + 50 * 4))

        pygame.display.update()
