import copy
import random
import sys

import numpy
import numpy as np
import pygame


class Backgammon:
    _NUM_POINTS = 24
    _STATE_SIZE = 198
    _NUM_CHECKERS = 15

    def __init__(self, game_mode, player=0, table=None,
                 dice1=0, dice2=0, dice3=0, dice4=0,
                 end_pieces_0=0, end_pieces_1=0,
                 out_pieces_0=0, out_pieces_1=0):
        """initializes the state
            Args:
                player (int): 0 for player 0 and 1 for player 1
                table (int, list): the list which contain pieces,the logical table
                end_pieces_0 (int): the number that means how many pieces has player 0 outer table
                end_pieces_1 (int): the number that means how many pieces has player 1 outer table
                out_pieces_0 (int): the number that means how many pieces has player 0 outer table, definitive
                out_pieces_1 (int): the number that means how many pieces has player 1 outer table, definitive"""
        self.player = player
        if table is None:
            # table from the logic part
            self.table = [-2, 0, 0, 0, 0, 5, 0, 3, 0, 0, 0, -5, 5, 0, 0, 0, -3, 0, -5, 0, 0, 0, 0, 2]
        else:
            self.table = copy.deepcopy(table)
        self.first_dice = dice1
        self.second_dice = dice2
        self.third_dice = dice3
        self.fourth_dice = dice4
        self.end_pieces_0 = end_pieces_0
        self.end_pieces_1 = end_pieces_1
        self.out_pieces_0 = out_pieces_0
        self.out_pieces_1 = out_pieces_1
        self.game_mode = game_mode
        # the lambda function to verify 2 position, 0 is for player 0 and 1 for player 1
        self.player_sign = {0: lambda a, b: a <= b,
                            1: lambda a, b: a >= b}

    def print_table(self):
        """ printing at the screen the game board (including position indexes)"""
        print([indices for indices in range(len(self.table))])
        print(self.table)

    def roll_dice(self):
        """ dice initialization
            a dice can have a value between 1 and 6"""
        self.first_dice = random.randint(1, 6)
        self.second_dice = random.randint(1, 6)
        if self.first_dice == self.second_dice:
            self.third_dice = self.first_dice
            self.fourth_dice = self.first_dice

    def end_game(self):
        """ check if one of the players has finished the game
            (if he has removed all the pieces from the table)
            Return:
                True: if one of the players has all 10 pieces outer table, for good
                False:if one of the players not have all 10 pieces outer table"""
        return self.end_pieces_1 == 10 or self.end_pieces_0 == 10

    def switch_player(self):
        """ the player is updated from 0 to 1 and vice versa"""
        self.player = (self.player + 1) % 2

    def need_to_put_in_house(self):
        """ check if the player has pieces to put in the house
        Return:
            True: if the player has pieces to put in the house
            False : if the player not have pieces to put in the house"""
        # check which player has to move and he has outer pieces
        return (self.player == 0 and self.out_pieces_0) or \
               (self.player == 1 and self.out_pieces_1)

    def can_put_in_house(self):
        """ check if the player has valid dice and if he has an empty square to enter with his dice
            if is nowhere to put the piece in the house, the dice are canceled and moves to the next player
            Return:
                True: if exist a valid dice and can put the piece in the house with that dice
                False: if not exist a valid dice and can put the piece in the house with that dice"""
        first_dice = second_dice = third_dice = fourth_dice = 0
        if self.first_dice:
            first_dice = 24 - self.first_dice if self.player == 0 else self.first_dice - 1
        if self.second_dice:
            second_dice = 24 - self.second_dice if self.player == 0 else self.second_dice - 1
        if self.third_dice:
            second_dice = 24 - self.third_dice if self.player == 0 else self.third_dice - 1
        if self.fourth_dice:
            second_dice = 24 - self.fourth_dice if self.player == 0 else self.fourth_dice - 1

        if self.player == 0:
            if (self.first_dice and self.table[first_dice] >= -1) or \
                    (self.second_dice and self.table[second_dice] >= -1) or \
                    (self.third_dice and self.table[third_dice] >= -1) or \
                    (self.fourth_dice and self.table[fourth_dice] >= -1):
                return True
            else:
                self.first_dice = 0
                self.second_dice = 0
                self.third_dice = 0
                self.fourth_dice = 0
                return False
        else:
            if (self.first_dice and self.table[first_dice] <= 1) or \
                    (self.second_dice and self.table[second_dice] <= 1) or \
                    (self.third_dice and self.table[third_dice] <= 1) or \
                    (self.fourth_dice and self.table[fourth_dice] <= 1):
                return True
            else:
                self.first_dice = 0
                self.second_dice = 0
                self.third_dice = 0
                self.fourth_dice = 0
                return False

    def add_in_house(self, position):
        """ add the piece in house to the received position
        Args:
            position(int): represent the position on the logical table where to add the piece
        Return:
            new_state(obj): the new state who contain all variables for game
            None: in case of error"""
        # create a copy for actual state
        print("1")
        if (self.game_mode == 1 or self.player == 0) and self.game_mode != 3:
            position, line = refine_position_to_move(position)
        print("positia la care intra in casa: ", position)
        new_state = Backgammon(self.game_mode, self.player, self.table,
                               self.first_dice, self.second_dice, self.third_dice, self.fourth_dice,
                               self.end_pieces_0, self.end_pieces_1,
                               self.out_pieces_0, self.out_pieces_1)
        # check the player to save the sign on the piece (positive or negative)
        if new_state.player == 0:
            print("2")
            new_state.out_pieces_0 -= 1
            dice = 24 - position
            # if at the position are pieces of the same kind or None
            if new_state.table[position] >= 0:
                new_state.table[position] += 1
                print("3")
            # if it is a single piece of the other color
            elif new_state.table[position] == -1:
                print("4")
                new_state.table[position] = 1
                new_state.out_pieces_1 += 1
            else:
                print("5")
                return None
        else:
            print("6")
            new_state.out_pieces_1 -= 1
            dice = position + 1
            if self.game_mode == 1:
                position += 1
            # if at the position are pieces of the same kind or None
            if new_state.table[position] <= 0:
                print("7")
                new_state.table[position] += -1
            # if it is a single piece of the other color
            elif new_state.table[position] == 1:
                print("8")
                new_state.table[position] = -1
                new_state.out_pieces_0 += 1
            else:
                print("9")
                return None
        # cancel the dice who was used
        if new_state.first_dice and new_state.first_dice == dice:
            print("10")
            new_state.first_dice = 0
        elif new_state.second_dice and new_state.second_dice == dice:
            print("11")
            new_state.second_dice = 0
        elif new_state.third_dice and new_state.third_dice == dice:
            print("12")
            new_state.second_dice = 0
        elif new_state.fourth_dice and new_state.fourth_dice == dice:
            print("13")
            new_state.second_dice = 0
        else:
            print("14")
            return None
        # return the new state, after all the modifications
        return new_state

    def can_move(self):
        """ check if player is able to move any piece who belong to him"""
        # if the player hasn't valid dice to move with
        if not self.first_dice and not self.second_dice and not self.third_dice and not self.fourth_dice:
            return False
        # or if the player has pieces who can be moved with his dice
        # which means that a piece can be moved to another free position
        for position in range(len(self.table)):
            if self.player == 0 and self.table[position] > 0 and \
                    (position - self.first_dice < 0 or self.table[position - self.first_dice] >= -1 or
                     position - self.second_dice < 0 or self.table[position - self.second_dice] >= -1 or
                     position - self.third_dice < 0 or self.table[position - self.third_dice] >= -1 or
                     position - self.fourth_dice or self.table[position - self.fourth_dice] >= -1):
                return True
            elif self.player == 1 and self.table[position] < 0 and \
                    (position + self.first_dice > 23 or self.table[position + self.first_dice] <= 1 or
                     position + self.second_dice > 23 or self.table[position + self.second_dice] <= 1 or
                     position + self.third_dice > 23 or self.table[position + self.third_dice] <= 1 or
                     position + self.fourth_dice > 23 or self.table[position + self.fourth_dice] <= 1):
                return True
        return False

    def can_move_certain_piece(self, pos):
        if self.player == 0 and self.table[pos] > 0:
            return True
        if self.player == 1 and self.table[pos] < 0:
            return True
        return False

    def can_move_to_certain_place(self, pos):
        if self.player == 0 and (self.table[pos] >= -1 or pos < 0):
            return True
        if self.player == 1 and (self.table[pos] <= 1 or pos > 23):
            return True
        return False

    def move_can_be_made(self, start_pos, end_pos):
        if self.player == 0:
            if start_pos < end_pos:
                return False
            if start_pos < 6 and end_pos < 0:
                return True
            if self.table[end_pos] >= -1 and (start_pos - self.first_dice == end_pos or
                                              start_pos - self.second_dice == end_pos or
                                              start_pos - self.third_dice == end_pos or
                                              start_pos - self.fourth_dice == end_pos):
                return True
            return False
        if self.player == 1:
            if start_pos > end_pos:
                return False
            if start_pos > 17 and end_pos > 23:
                return True
            if self.table[end_pos] <= 1 and (start_pos + self.first_dice == end_pos or
                                             start_pos + self.second_dice == end_pos or
                                             start_pos + self.third_dice == end_pos or
                                             start_pos + self.fourth_dice == end_pos):
                return True
            return False

    def return_positions_for_movement(self, interf):
        position_start = position_end = -1
        while position_start == -1:
            if (self.game_mode == 2 and self.player == 1) or self.game_mode == 3:
                if self.player == 0:
                    position_start, position_end = self.pc_piece_positions_for0()
                else:
                    position_start, position_end = self.pc_piece_positions_for1()
            else:
                # click to select the piece which i want to be moved
                position_start = click_for_position()
                position_start, up_or_down = refine_position_to_move(position_start)
                interf.update_clicked_piece(position_start, up_or_down)
                interf.draw()
                # click to select the position where to move the piece
                position_end = click_for_position()
                position_end, up_or_down = refine_position_to_move(position_end)
                interf.update_clicked_piece(-1, "up")
                interf.draw()
                # verifications
                if position_start - position_end > 6 and position_end > 0:
                    print("Difference is too big! Click again!")
                    position_start = position_end = 0
                elif not self.can_move_certain_piece(position_start):
                    print("You can not move that piece! Click again! ", position_start)
                    position_start = position_end = 0
                elif not self.can_move_to_certain_place(position_end):
                    print("You can not move to that place! Click again! ", position_end)
                    position_start = position_end = 0
                elif not self.move_can_be_made(position_start, position_end):
                    print("This move can not be made! Click again! ", position_start, " ", position_end)
                    position_start = position_end = 0

        return position_start, position_end

    def move(self, start_position, end_position):
        """ move a piece on the table, from a specific position to another specific position
            Args:
                start_position (int): the position from which want to move the piece on the logic table
                end_position(int): the position to which want to move the piece on the logic board
            Return:
                new_state(obj): the new state who contain all variables for game
                None: in case of error"""
        # create a copy for state
        new_state = Backgammon(self.game_mode, self.player, self.table,
                               self.first_dice, self.second_dice, self.third_dice, self.fourth_dice,
                               self.end_pieces_0, self.end_pieces_1, self.out_pieces_0, self.out_pieces_1)
        # set the sign for player
        piece_sign = 1 if self.player == 0 else -1

        # remove the piece from the start position
        new_state.table[start_position] -= piece_sign
        # if the position is off the table
        if end_position > 23 or end_position < 0:
            # save the piece as being taken out of the game definitively
            # here the player is also checked, to see where the piece should be saved
            if new_state.player == 0:
                new_state.end_pieces_0 += 1
            else:
                new_state.end_pieces_1 += 1
        elif (new_state.player == 0 and new_state.table[end_position] >= 0) or \
                (new_state.player == 1 and new_state.table[end_position] <= 0):
            #  add another piece
            new_state.table[end_position] += piece_sign
        # if it is a single piece of the other color
        elif new_state.table[end_position] == -1 * piece_sign:
            # on position put a piece with value specific for player that is moving
            new_state.table[end_position] = piece_sign
            # subtract a piece from the player that is moving, and add a piece to the other player
            if new_state.player == 0:
                new_state.out_pieces_1 += 1
            else:
                new_state.out_pieces_0 += 1
        else:
            return None

        # calculate the dice used
        if end_position > 23 or end_position < 0:
            dices = [self.first_dice, self.second_dice, self.third_dice, self.fourth_dice]
            dices.sort()
            if self.player == 1:
                for dice in dices:
                    if 24 - start_position == dice:
                        break
                for dice in dices:
                    if 24 - start_position < dice:
                        break
            else:
                for dice in dices:
                    if start_position + 1 == dice:
                        break
                for dice in dices:
                    if start_position + 1 < dice:
                        break

        else:
            dice = abs(end_position - start_position)

        # cancel the dice who was used
        if new_state.first_dice == dice and new_state.first_dice:
            print("s-a consumat zarul1 ", new_state.first_dice)
            new_state.first_dice = 0
        elif new_state.second_dice == dice and new_state.second_dice:
            print("s-a consumat zarul2 ", new_state.second_dice)
            new_state.second_dice = 0
        elif new_state.third_dice == dice and new_state.third_dice:
            print("s-a consumat zarul3 ", new_state.third_dice)
            new_state.third_dice = 0
        elif new_state.fourth_dice == dice and new_state.fourth_dice:
            print("s-a consumat zarul4 ", new_state.fourth_dice)
            new_state.fourth_dice = 0
        else:
            return None

        # return the new state, after all these modifications
        return new_state

    def calculate_points(self):
        points_white = 0
        points_black = 0
        # add points for pieces placed in the middle of the table (out pieces)
        pieces_in_the_middle = 0
        while pieces_in_the_middle < self.out_pieces_0:
            points_white += 25
            pieces_in_the_middle += 1
        pieces_in_the_middle = 0
        while pieces_in_the_middle < self.out_pieces_1:
            points_black += 25
            pieces_in_the_middle += 1
        for index_table in range(len(self.table)):
            if self.table[index_table] > 0:
                points_white += self.table[index_table] * (index_table + 1)
            if self.table[index_table] < 0:
                points_black += abs(self.table[index_table]) * (index_table + 1)
        return points_white, points_black

    def pc_piece_positions(self):
        """ Search for a piece who can be moved with at least one dice, if the dice is valid
            Return:
                the position from which you want to move the piece and
                the position to which you want to move the piece"""
        list_of_possible_moves = []
        for position in range(len(self.table)):
            if self.table[position] <= -1 and self.first_dice and \
                    self.table[position + self.first_dice] <= 1:
                list_of_possible_moves.append((position, position + self.first_dice))
                # return position, position + self.first_dice
            elif self.table[position] <= -1 and self.second_dice and \
                    self.table[position + self.second_dice] <= 1:
                list_of_possible_moves.append((position, position + self.second_dice))
                # return position, position + self.second_dice
            elif self.table[position] <= -1 and self.third_dice and \
                    self.table[position + self.third_dice] <= 1:
                list_of_possible_moves.append((position, position + self.third_dice))
                # return position, position + self.third_dice
            elif self.table[position] <= -1 and self.fourth_dice and \
                    self.table[position + self.fourth_dice] <= 1:
                list_of_possible_moves.append((position, position + self.fourth_dice))
                # return position, position + self.fourth_dice
        return list_of_possible_moves

    def won(self):
        if self.end_pieces_1 == 10:
            print("Player 1 WON!")
            return 1
        elif self.end_pieces_0 == 10:
            print("Player 0 WON!")
            return 0
        return None

    def pc_piece_positions_for0(self):
        """ Search for a piece who can be moved with at least one dice, if the dice is valid
            Return:
                the position from which you want to move the piece and
                the position to which you want to move the piece"""
        flag = 0
        for index in reversed(range(6, 24)):
            if self.table[index] > 0:
                flag += 1
        if not flag:
            if self.first_dice and self.table[self.first_dice - 1] >= 1:
                return self.first_dice - 1, -1
            elif self.second_dice and self.table[self.second_dice - 1] >= 1:
                return self.second_dice - 1, -1
            elif self.third_dice and self.table[self.third_dice - 1] >= 1:
                return self.third_dice - 1, -1
            elif self.fourth_dice and self.table[self.fourth_dice - 1] >= 1:
                return self.fourth_dice - 1, -1
            else:
                for index in reversed(range(6)):
                    if self.table[index] >= 1:
                        return index, -1
        for position in reversed(range(len(self.table))):
            if self.table[position] >= 1 and self.first_dice and \
                    (self.table[position - self.first_dice] >= -1 or position - self.first_dice < 0):
                return position, position - self.first_dice
            elif self.table[position] >= 1 and self.second_dice and \
                    (self.table[position - self.second_dice] >= -1 or position - self.second_dice < 0):
                return position, position - self.second_dice
            elif self.table[position] >= 1 and self.third_dice and \
                    (self.table[position - self.third_dice] >= -1 or position - self.third_dice < 0):
                return position, position - self.third_dice
            elif self.table[position] >= 1 and self.fourth_dice and \
                    (self.table[position - self.fourth_dice] >= -1 or position - self.fourth_dice < 0):
                return position, position - self.fourth_dice

    def pc_piece_positions_for1(self):
        """ Search for a piece who can be moved with at least one dice, if the dice is valid
            Return:
                the position from which you want to move the piece and
                the position to which you want to move the piece"""
        flag = 0
        for index in range(18):
            if self.table[index] < 0:
                flag += 1
        if not flag:
            if self.first_dice and self.table[24 - self.first_dice] <= -1:
                return 24 - self.first_dice, -1
            elif self.second_dice and self.table[24 - self.second_dice] <= -1:
                return 24 - self.second_dice, -1
            elif self.third_dice and self.table[24 - self.third_dice] <= -1:
                return 24 - self.third_dice, -1
            elif self.fourth_dice and self.table[24 - self.fourth_dice] <= -1:
                return 24 - self.fourth_dice, -1
            else:
                for index in range(18, 24):
                    if self.table[index] <= -1:
                        return index, -1

        for position in range(len(self.table)):
            if self.table[position] <= -1 and self.first_dice and \
                    (self.table[position + self.first_dice] <= 1 or position + self.first_dice > 23):
                return position, position + self.first_dice
            elif self.table[position] <= -1 and self.second_dice and \
                    (self.table[position + self.second_dice] <= 1 or position + self.second_dice > 23):
                return position, position + self.second_dice
            elif self.table[position] <= -1 and self.third_dice and \
                    (self.table[position + self.third_dice] <= 1 or position + self.third_dice > 23):
                return position, position + self.third_dice
            elif self.table[position] <= -1 and self.fourth_dice and \
                    (self.table[position + self.fourth_dice] <= 1 or position + self.fourth_dice > 23):
                return position, position + self.fourth_dice

    # def pc_house_position(self):
    #     """check if with the given dice, can enter in the house with at least one of the dice
    #         Return:
    #             position in the house, where it can enter with at least one of the given dice
    #             None: in case of error"""
    #     list_positions_in_house = []
    #     if self.first_dice and self.table[self.first_dice - 1] <= 1:
    #         # return self.first_dice - 1
    #         list_positions_in_house.append(self.first_dice - 1)
    #     elif self.second_dice and self.table[self.second_dice - 1] <= 1:
    #         # return self.second_dice - 1
    #         list_positions_in_house.append(self.second_dice - 1)
    #     elif self.third_dice and self.table[self.third_dice - 1] <= 1:
    #         # return self.third_dice - 1
    #         list_positions_in_house.append(self.third_dice - 1)
    #     elif self.fourth_dice and self.table[self.fourth_dice - 1] <= 1:
    #         # return self.fourth_dice - 1
    #         list_positions_in_house.append(self.fourth_dice - 1)
    #     return list_positions_in_house
    def pc_house_position_for0(self):
        """check if with the given dice, can enter in the house with at least one of the dice
            Return:
                position in the house, where it can enter with at least one of the given dice
                None: in case of error"""
        if self.first_dice and self.table[24 - self.first_dice] >= -1:
            return 24 - self.first_dice
        elif self.second_dice and self.table[24 - self.second_dice] >= -1:
            return 24 - self.second_dice
        elif self.third_dice and self.table[24 - self.third_dice] >= -1:
            return 24 - self.third_dice
        elif self.fourth_dice and self.table[24 - self.fourth_dice] >= -1:
            return 24 - self.fourth_dice
        else:
            return None

    def pc_house_position_for1(self):
        """check if with the given dice, can enter in the house with at least one of the dice
            Return:
                position in the house, where it can enter with at least one of the given dice
                None: in case of error"""
        print("zarurile pentru bagat is casa sunt: ", self.first_dice, self.second_dice,
              self.third_dice, self.fourth_dice)
        if self.first_dice and self.table[self.first_dice - 1] <= 1:
            return self.first_dice - 1
        elif self.second_dice and self.table[self.second_dice - 1] <= 1:
            return self.second_dice - 1
        elif self.third_dice and self.table[self.third_dice - 1] <= 1:
            return self.third_dice - 1
        elif self.fourth_dice and self.table[self.fourth_dice - 1] <= 1:
            return self.fourth_dice - 1
        else:
            return None

    def encode_state(self, turn):
        _o_points, _x_points = self.calculate_points()
        state = np.zeros(self._STATE_SIZE)

        for point in range(self._NUM_POINTS):
            index = point * 4
            if self.table[point] <= -1:
                state[index:index + 4] = encode_point(abs(self.table[point]))

        for point in range(self._NUM_POINTS):
            index = (point + 24) * 4
            if self.table[point] >= 1:
                state[index:index + 4] = encode_point(self.table[point])

        state[192] = self.out_pieces_1 / 2
        state[193] = self.out_pieces_0 / 2
        state[194] = self.end_pieces_1 / self._NUM_CHECKERS
        state[195] = self.end_pieces_0 / self._NUM_CHECKERS
        state[196] = 1 - turn
        state[197] = turn

        return state


def encode_point(n_checkers):
    arr = np.zeros(4)
    if n_checkers == 1:  # Blot
        arr[0] = 1
    if n_checkers >= 2:  # Made point
        arr[1] = 1
    if n_checkers == 3:
        arr[2] = 1
    if n_checkers > 3:
        arr[3] = (n_checkers - 3) / 2
    return arr


def refine_position_to_move(position):
    col, line = position
    line = "up" if line < 400 else "down"
    col = int((col - 80) / 45)
    if col >= 7:
        col = col - 2
    if line == "down":
        pos = 11 - col
    else:
        pos = 12 + col
    print("pozitia prelucrata: ", pos, line)
    return pos, line


def click_for_position():
    """this function waits to receive a click to take the coordinates and turn them into position on the logic table
        Args:
            interf(obj): object for interface to call class variables
        Return:
            the position in the table from logic part corresponding to the coordinates where was clicked"""
    # wait until receive the first click
    mouse = -1
    while mouse == -1:
        event = pygame.event.wait()
        if event.type == pygame.MOUSEBUTTONDOWN:
            # save the position in col and line
            mouse = event.pos
        # quit from x
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    print("clicked psoition: ", mouse)
    return mouse
