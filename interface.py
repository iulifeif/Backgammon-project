import random

import pygame
import sys

from numpy.ma import copy

from backgammon import Backgammon
from utils import load_sprite
from colors import *


class Interface:
    def __init__(self, player=0, table=None, dice1=0, dice2=0,
                 end_pieces_0=0, end_pieces_1=0,
                 out_pieces_0=0, out_pieces_1=0, game_mode=2):
        """ initialize table with fixed dimensions """
        self.player = player
        self.table = table
        self.screen = 0
        self.up_table = []
        self.down_table = []
        self.first_dice = dice1
        self.second_dice = dice2
        self.end_pieces_0 = end_pieces_0
        self.end_pieces_1 = end_pieces_1
        self.out_pieces_0 = out_pieces_0
        self.out_pieces_1 = out_pieces_1
        self.game_mode = game_mode
        self.clicked_piece = -1
        self.clicked_side = -1
        self.third_dice = 0
        self.fourth_dice = 0
        self.first_dice_used = 0
        self.second_dice_used = 0
        self.third_dice_used = 0
        self.fourth_dice_used = 0

    def update_clicked_piece(self, piece_start, up_or_down):
        self.clicked_piece = piece_start
        self.clicked_side = up_or_down

    def update_player(self, player):
        self.player = player

    def update_table(self, table):
        print(table)
        self.table = table

    def update_dice(self, dice1, dice2, dice3, dice4):
        if dice1 == 0:
            self.first_dice_used = 1
        else:
            self.first_dice = dice1
            self.first_dice_used = 0
        if dice2 == 0:
            self.second_dice_used = 1
        else:
            self.second_dice = dice2
            self.second_dice_used = 0
        if dice3 == 0:
            self.third_dice_used = 1
        else:
            self.third_dice = dice3
            self.third_dice_used = 0
        if dice4 == 0:
            self.fourth_dice_used = 1
        else:
            self.fourth_dice = dice4
            self.fourth_dice_used = 0

    def update_end_pieces(self, end_pieces_0, end_pieces_1):
        self.end_pieces_0 = end_pieces_0
        self.end_pieces_1 = end_pieces_1

    def update_out_pieces(self, out_pieces_0, out_pieces_1):
        self.out_pieces_0 = out_pieces_0
        self.out_pieces_1 = out_pieces_1
        print("PIESELE OUT ", self.out_pieces_0, self.out_pieces_1)

    def update_game_mode(self, game_mode):
        self.game_mode = game_mode

    def draw_table(self):
        self.screen = pygame.display.set_mode((800, 800))
        self.screen.fill(WHITE)
        if self.game_mode == 1:
            self.screen.blit(load_sprite("two_players_back", False), (0, 0))
        else:
            self.screen.blit(load_sprite("main_back", False), (0, 0))

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

    def draw_end_pieces(self):
        """ draw the pieces that are taken out of the board
            player 0 at the top, and player 1 at the bottom
            Args:
                out_pieces (int): a number that represents how many pieces removed has the player
                pos (int): the position of the line from which to start drawing the parts"""
        piece_index = 0
        while piece_index < self.end_pieces_0:
            sprite = load_sprite("white_beard_off", True)
            blit_position = pygame.Vector2((750, 366 + piece_index * 11))
            self.screen.blit(sprite, blit_position)
            piece_index += 1
        piece_index = 0
        while piece_index < self.end_pieces_1:
            sprite = load_sprite("black_beard_off", True)
            blit_position = pygame.Vector2((750, 755 + piece_index * 11))
            self.screen.blit(sprite, blit_position)
            piece_index += 1

    def draw_out_pieces(self):
        piece_index = 0
        while piece_index < self.out_pieces_0:
            sprite = load_sprite("white_got", True)
            blit_position = pygame.Vector2((380, 300 + piece_index * 50))
            self.screen.blit(sprite, blit_position)
            piece_index += 1
        piece_index = 0
        while piece_index < self.out_pieces_1:
            sprite = load_sprite("black_got", True)
            blit_position = pygame.Vector2((380, 570 - piece_index * 50))
            self.screen.blit(sprite, blit_position)
            piece_index += 1

    def draw_turn_ligh(self):
        sprite = load_sprite("turn_light", True)
        if self.player == 0:
            blit_position = pygame.Vector2((287, 1))
        else:
            blit_position = pygame.Vector2((430, 1))
        self.screen.blit(sprite, blit_position)

    def draw_dice_roll(self):
        blit_position = pygame.Vector2((743, 382))
        if self.first_dice_used == self.second_dice_used == self.third_dice_used == self.fourth_dice_used:
            if self.player == 0:
                sprite = load_sprite("active_dice_button", True)
                self.screen.blit(sprite, blit_position)
            else:
                sprite = load_sprite("active_player2_dice", True)
                self.screen.blit(sprite, blit_position)

    def draw_dice(self):
        color = "white_dice_" if self.player == 0 else "black_dice_"
        sprite = load_sprite(color + str(self.first_dice), True)
        blit_position = pygame.Vector2((450, 390))
        self.screen.blit(sprite, blit_position)
        sprite = load_sprite(color + str(self.second_dice), True)
        blit_position = pygame.Vector2((500, 390))
        self.screen.blit(sprite, blit_position)

        if self.first_dice == self.second_dice:
            blit_position = pygame.Vector2((450, 450))
            self.screen.blit(sprite, blit_position)
            blit_position = pygame.Vector2((500, 450))
            self.screen.blit(sprite, blit_position)

    def draw_piece_highlite(self):
        piece_color = "white_highlight" if self.player == 0 else "black_highlight"
        sprite = load_sprite(piece_color, True)
        number_pieces = self.table[self.clicked_piece] - 1
        if number_pieces == -1:
            print("Ai dat click pe langa!")
            return None
        if self.clicked_side == "down":
            column_position = 11 - self.clicked_piece
            if column_position > 6:
                column_position += 1
            blit_position = pygame.Vector2((80 + column_position * 50,
                                            730 - number_pieces * 45))
        elif self.clicked_side == "up":
            column_position = self.clicked_piece - 12
            if column_position > 6:
                column_position += 1
            blit_position = pygame.Vector2((80 + column_position * 50,
                                            135 + number_pieces * 45))
        else:
            return None
        self.screen.blit(sprite, blit_position)

    def draw_where_player_can_move(self):
        game = Backgammon(self.game_mode, self.player, self.table,
                          self.first_dice, self.second_dice,
                          self.end_pieces_0, self.end_pieces_1,
                          self.out_pieces_0, self.out_pieces_1)
        dice_value = [self.first_dice, self.second_dice, self.third_dice, self.fourth_dice]
        dice_used = [self.first_dice_used, self.second_dice_used, self.third_dice_used, self.fourth_dice_used]
        for index_dice in range(len(dice_value)):
            move_with_one_dice = self.clicked_piece - dice_value[index_dice] if self.player == 0 \
                else self.clicked_piece + dice_value[index_dice]
            if dice_used[index_dice] == 0 and game.move_can_be_made(self.clicked_piece, move_with_one_dice):
                if move_with_one_dice > 11:
                    if move_with_one_dice > 17:
                        move_with_one_dice += 1
                    move_with_one_dice -= 12
                    sprite = load_sprite("destination_light", True)
                    blit_position = pygame.Vector2((73 + move_with_one_dice * 50, 115))
                else:
                    move_with_one_dice = 11 - move_with_one_dice
                    print("pozitia de DESENAT ", move_with_one_dice)
                    if move_with_one_dice > 6:
                        move_with_one_dice += 1
                    sprite = load_sprite("destination_light_bottom", True)
                    blit_position = pygame.Vector2((73 + move_with_one_dice * 50, 500))
                self.screen.blit(sprite, blit_position)

    def draw(self):
        """ the board is drawn as a matrix with green elements
            then add in each square, a black circle, this function also calls the necessary functions for
            preprocessing the table, for draw the pieces from table and pieces outer table
            Args:
                table(int, list): the list which contain pieces,the logical table
                table_out_0 (int): the number that represents how many pieces removed has player 0
                table_out_1 (int): the number that represents how many pieces removed has player 1"""
        # set screen size
        self.draw_table()
        self.preprocess_table()
        self.draw_turn_ligh()
        self.draw_dice_roll()
        if self.first_dice != 0 and (self.first_dice_used == 0 or self.second_dice_used == 0 or
                                     self.third_dice_used == 0 or self.fourth_dice_used == 0):
            self.draw_dice()
        self.draw_pieces("upper")
        self.draw_pieces("lower")
        if self.clicked_piece != -1:
            self.draw_piece_highlite()
            self.draw_where_player_can_move()
        self.draw_out_pieces()
        self.draw_end_pieces()
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
