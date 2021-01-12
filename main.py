import copy
import math
import random
import pygame
import sys
import numpy as np

pygame.init()

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BROWN = (150, 75, 0)


class Interface:
    def __init__(self, table):
        self.squaresize = 50
        self.column_count = 12
        self.row_count = 16
        self.width = self.squaresize * (self.column_count + 1)
        self.height = self.squaresize * self.row_count
        self.size = (self.width, self.height)
        self.radius = int(self.squaresize / 2 - 5)
        self.screen = pygame.display.set_mode(self.size)
        self.draw_board(table)
        pygame.display.update()

    def prepro(self, table):
        self.up_table = table[len(table) // 2:]
        intermediar_down_table = table[:len(table) // 2]
        self.down_table = []
        for pos in reversed(range(len(intermediar_down_table))):
            self.down_table.append(intermediar_down_table[pos])

    def draw_pieces(self, table, pos):
        for col in range(len(table)):
            line = pos
            while table[col] != 0:
                if table[col] < 0:
                    pygame.draw.circle(self.screen, BROWN,
                                       (int(col * self.squaresize + self.squaresize / 2),
                                        int(line * self.squaresize + self.squaresize + self.squaresize / 2)),
                                       self.radius)
                    table[col] += 1
                elif table[col] > 0:
                    pygame.draw.circle(self.screen, WHITE,
                                       (int(col * self.squaresize + self.squaresize / 2),
                                        int(line * self.squaresize + self.squaresize + self.squaresize / 2)),
                                       self.radius)
                    table[col] -= 1

                line = line + 1 if pos == 0 else line - 1

    def draw_board(self, table):
        for index_column in range(self.column_count):
            for index_line in range(self.row_count):
                pygame.draw.rect(self.screen,
                                 GREEN,
                                 (index_column * self.squaresize,
                                  index_line * self.squaresize + self.squaresize,
                                  self.squaresize,
                                  self.squaresize))
                if index_line != 7:
                    pygame.draw.circle(self.screen,
                                       BLACK,
                                       (int(index_column * self.squaresize + self.squaresize / 2),
                                        int(index_line * self.squaresize + self.squaresize + self.squaresize / 2)),
                                       self.radius)
        self.prepro(table)
        self.draw_pieces(self.up_table, 0)
        self.draw_pieces(self.down_table, 14)
        pygame.display.update()


class Backgammon:
    # initializarea starii
    def __init__(self, player=0, table=None, dice1=0, dice2=0, end_pieces_0=0, end_pieces_1=0, out_pieces_0=0, out_pieces_1=0):
        self.player = player
        if table is None:
            self.table = [2, 0, 0, 0, 0, -5, 0, -3, 0, 0, 0, 5, -5, 0, 0, 0, 3, 0, 5, 0, 0, 0, 0, -2]
        else:
            self.table = copy.deepcopy(table)
        self.first_dice = dice1
        self.second_dice = dice2
        self.end_pieces_0 = end_pieces_0
        self.end_pieces_1 = end_pieces_1
        self.out_pieces_0 = out_pieces_0
        self.out_pieces_1 = out_pieces_1
        self.player_sign = {0: lambda a, b: a <= b,
                            1: lambda a, b: a >= b}

    # printarea tablei de joc (cu tot cu indicii pozitiilor)
    def print_table(self):
        print([indices for indices in range(len(self.table))])
        print(self.table)

    # initializarea zarurilor
    def roll_dices(self):
        self.first_dice = random.randint(1, 6)
        self.second_dice = random.randint(1, 6)

    # verifica daca unul dintre jucatori a terminat jocul (daca a scos toate piesele)
    def end_game(self):
        return self.end_pieces_1 == 10 or self.end_pieces_0 == 10

    def switch_player(self):
        print("Tura ta s-a terminat")
        self.player = (self.player + 1) % 2

    def need_to_put_in_house(self):
        return self.player == 0 and self.out_pieces_0 and \
               (self.table[self.first_dice - 1] <= 1 or self.table[self.second_dice - 1] <= 1) or \
               self.player == 1 and self.out_pieces_1 and \
               (self.table[24 - self.first_dice] >= 1 or self.table[24 - self.second_dice] >= 1)

    # adauga cu zarul "dice" in casa playerului care este la mutare
    def add_in_house(self, position):
        new_state = Backgammon(self.player, self.table, self.first_dice, self.second_dice, self.end_pieces_0,
                               self.end_pieces_1, self.out_pieces_0, self.out_pieces_1)
        # position = dice - 1 if self.player == 0 else 24 - dice
        piece_sign = 1 if new_state.player == 0 else -1

        if new_state.player_sign[new_state.player](new_state.table[position], 0):
            # daca pe pozitia respectiva sunt piese de acelasi fel sau nu e niciuna
            new_state.table[position] -= piece_sign
            if not new_state.player:
                new_state.out_pieces_0 -= 1
            else:
                new_state.out_pieces_1 -= 1
        elif new_state.table[position] == piece_sign:
            # daca este o singura piesa de cealalta culoare
            new_state.table[position] = -1 * piece_sign
            new_state.out_pieces_0 -= piece_sign
            new_state.out_pieces_1 += piece_sign
        else:
            return None

        dice = 24 - position if new_state.player == 0 else position + 1
        print("zarul este: {}".format(dice))

        if new_state.first_dice and new_state.first_dice == dice:
            new_state.first_dice = 0
        elif new_state.second_dice and new_state.second_dice == dice:
            new_state.second_dice = 0
        return new_state

    def can_move(self):
        if not self.first_dice and not self.second_dice:
            return 0
        for position in range(len(self.table)):
            if self.player == 0 and self.table[position] < 0 and \
                    (self.table[position - self.first_dice] <= 1 or self.table[position - self.second_dice] <= 1):
                return 1
            elif self.player == 1 and self.table[position] > 1 and \
                    (self.table[position + self.first_dice] >= -1 or self.table[position + self.second_dice] >= -1):
                return 1
        return 0

    def move(self, start_position, end_position):
        new_state = Backgammon(self.player, self.table, self.first_dice, self.second_dice,
                                     self.end_pieces_0, self.end_pieces_1, self.out_pieces_0, self.out_pieces_1)
        piece_sign = 1 if self.player == 0 else -1
        out_position = 0 if self.player == 0 else 24

        new_state.table[start_position] += piece_sign
        if end_position == out_position:
            if new_state.player == 0:
                new_state.end_pieces_0 += 1
            else:
                new_state.end_pieces_1 += 1
        elif new_state.player_sign[new_state.player](new_state.table[end_position], 0):
            new_state.table[end_position] -= piece_sign
        elif new_state.table[end_position] == piece_sign:
            new_state.table[end_position] = -1 * piece_sign
            if new_state.player == 0:
                new_state.out_pieces_1 += 1
            else:
                new_state.out_pieces_0 += 1
        else:
            return None
        dice = abs(end_position - start_position)
        if new_state.first_dice == dice and new_state.first_dice:
            new_state.first_dice = 0
        elif new_state.second_dice == dice and new_state.second_dice:
            new_state.second_dice = 0
        else:
            return None

        return new_state


def click_for_position():
    col = -1
    while col == -1:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                col, line = event.pos
                line = int(line / 50)
                col = int(col / 50)
                if line < 7:
                    line = 0
                elif line > 7:
                    line = 1
    if not line:
        return col + 12
    else:
        return 11 - col


def message(interf, table, text, number_message):
    number = 3 if number_message == 1 else 7
    textRect = text.get_rect()
    textRect.center = (interf.squaresize * number, interf.squaresize / 2)
    interf.screen.blit(text, textRect)
    interf.draw_board(table)


def play_game():
    game = Backgammon()
    game_over = False
    interf = Interface(game.table)
    font = pygame.font.Font(None, 28)
    while not game.end_game() and not game_over:
        interf.draw_board(game.table)

        # adaug informatii despre jucator si zaruri
        text = font.render("Acum joaca playerul: {}".format(game.player), True, WHITE)
        message(interf, game.table, text, 1)

        # print("Acum joaca playerul: {}".format(game.player))
        game.roll_dices()

        text = font.render("Cu zarurile: {}, {}".format(game.first_dice, game.second_dice), True, WHITE)
        message(interf, game.table, text, 2)

        # print("Cu zarurile: {}, {}".format(game.first_dice, game.second_dice))
        print("Tabla de start: ")
        game.print_table()
        while game.need_to_put_in_house():

            # position_home = int(input("Unde vrei sa intrii cu piesa: "))
            position_home = click_for_position()

            game = game.add_in_house(position_home)

            print("Tabla dupa ce a intrat cu piesa in casa: ")
            game.print_table()
            interf.draw_board(game.table)
        while game.can_move():
            # position_start = int(input("Pozitia de la care vrei sa muti piesa: "))

            position_start = click_for_position()

            # print("positia start este", position_start)

            position_end = click_for_position()

            # position_end = int(input("Pozitia unde muti?: "))
            # print("positia end este", position_end)

            game = game.move(position_start, position_end)
            print("Tabla dupa ce a mutat piesa: ")
            game.print_table()
            interf.draw_board(game.table)
        game.switch_player()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
                sys.exit()
    if game.end_pieces_1 == 10:
        print("Jucatorul 1 a castigat!")
    elif game.end_pieces_0 == 10:
        print("Jucatorul 0 a castigat!")


if __name__ == '__main__':
    play_game()
