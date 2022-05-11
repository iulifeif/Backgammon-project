import copy
import random


class Backgammon:
    def __init__(self, player=0, table=None,
                 dice1=0, dice2=0,
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
            self.table = [2, 0, 0, 0, 0, -5, 0, -3, 0, 0, 0, 5, -5, 0, 0, 0, 3, 0, 5, 0, 0, 0, 0, -2]
        else:
            self.table = copy.deepcopy(table)
        self.first_dice = dice1
        self.second_dice = dice2
        self.end_pieces_0 = end_pieces_0
        self.end_pieces_1 = end_pieces_1
        self.out_pieces_0 = out_pieces_0
        self.out_pieces_1 = out_pieces_1
        self.game_mode = 1
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
        first_dice = 0
        second_dice = 0
        if self.first_dice:
            first_dice = 24 - self.first_dice if self.player == 0 else self.first_dice - 1
        if self.second_dice:
            second_dice = 24 - self.second_dice if self.player == 0 else self.second_dice - 1
        sign_pieces = 1 if self.player == 0 else -1

        if (self.first_dice and self.table[first_dice] <= sign_pieces) or \
                (self.second_dice and self.table[second_dice] <= sign_pieces):
            return True
        else:
            self.first_dice = 0
            self.second_dice = 0
            return False

    def add_in_house(self, position):
        """ add the piece in house to the received position
        Args:
            position(int): represent the position on the logical table where to add the piece
        Return:
            new_state(obj): the new state who contain all variables for game
            None: in case of error"""
        # create a copy for actual state
        new_state = Backgammon(self.player, self.table, self.first_dice, self.second_dice, self.end_pieces_0,
                               self.end_pieces_1, self.out_pieces_0, self.out_pieces_1)
        # check the player to save the sign on the piece (positive or negative)
        piece_sign = 1 if new_state.player == 0 else -1

        # if at the position are pieces of the same kind or None
        if new_state.player_sign[new_state.player](new_state.table[position], 0):
            # add another piece
            new_state.table[position] -= piece_sign
            # from the variable that saves outer pieces, decreases a piece that has just been added
            # here it is checked according to the player
            if not new_state.player:
                new_state.out_pieces_0 -= 1
            else:
                new_state.out_pieces_1 -= 1
        # if it is a single piece of the other color
        elif new_state.table[position] == piece_sign:
            # on position put a piece with value specific for player that is moving
            new_state.table[position] = -1 * piece_sign
            # subtract a piece from the player that is moving, and add a piece to the other player
            new_state.out_pieces_0 -= piece_sign
            new_state.out_pieces_1 += piece_sign
        else:
            return None

        # calculate the dice used to cancel it
        dice = 24 - position if new_state.player == 0 else position + 1

        # cancel the dice who was used
        if new_state.first_dice and new_state.first_dice == dice:
            new_state.first_dice = 0
        elif new_state.second_dice and new_state.second_dice == dice:
            new_state.second_dice = 0
        else:
            return None

        # return the new state, after all these modifications
        return new_state

    def can_move(self):
        """ check if player is able to move any piece who belong to him"""
        # if the player still has valid dice to move with
        if not self.first_dice and not self.second_dice:
            return 0
        # or if the player has pieces who can be moved with his dice
        # which means that a piece can be moved to another free position
        for position in range(len(self.table)):
            if self.player == 0 and self.table[position] < 0 and \
                    (self.table[position - self.first_dice] <= 1 or self.table[position - self.second_dice] <= 1):
                return True
            elif self.player == 1 and self.table[position] > 1 and \
                    (self.table[position + self.first_dice] >= -1 or self.table[position + self.second_dice] >= -1):
                return True
        return False

    def move(self, start_position, end_position):
        """ move a piece on the table, from a specific position to another specific position
            Args:
                start_position (int): the position from which want to move the piece on the logic table
                end_position(int): the position to which want to move the piece on the logic board
            Return:
                new_state(obj): the new state who contain all variables for game
                None: in case of error"""
        # create a copy for state
        new_state = Backgammon(self.player, self.table, self.first_dice, self.second_dice,
                               self.end_pieces_0, self.end_pieces_1, self.out_pieces_0, self.out_pieces_1)
        # set the sign for player
        piece_sign = 1 if self.player == 0 else -1
        # set the outer boundary depending on the player
        out_position = 0 if self.player == 0 else 24

        # remove the piece from the start position
        new_state.table[start_position] += piece_sign
        # if the position is off the table
        if end_position == out_position:
            # save the piece as being taken out of the game definitive
            # here the player is also checked, to see where the piece should be saved
            if new_state.player == 0:
                new_state.end_pieces_0 += 1
            else:
                new_state.end_pieces_1 += 1
        # if at the position are pieces of the same kind or None
        elif new_state.player_sign[new_state.player](new_state.table[end_position], 0):
            #  add another piece
            new_state.table[end_position] -= piece_sign
        # if it is a single piece of the other color
        elif new_state.table[end_position] == piece_sign:
            # on position put a piece with value specific for player that is moving
            new_state.table[end_position] = -1 * piece_sign
            # subtract a piece from the player that is moving, and add a piece to the other player
            if new_state.player == 0:
                new_state.out_pieces_1 += 1
            else:
                new_state.out_pieces_0 += 1
        else:
            return None

        # calculate the dice used
        dice = abs(end_position - start_position)

        # cancel the dice who was used
        if new_state.first_dice == dice and new_state.first_dice:
            new_state.first_dice = 0
        elif new_state.second_dice == dice and new_state.second_dice:
            new_state.second_dice = 0
        else:
            return None

        # return the new state, after all these modifications
        return new_state

    # return position start and end for a piece who must be moved
    def pc_piece_positions(self):
        """ Search for a piece who can be moved with at least one dice, if the dice is valid
            Return:
                the position from which you want to move the piece and
                the position to which you want to move the piece"""
        for position in range(len(self.table)):
            if self.table[position] >= 1 and self.first_dice and \
                    self.table[position + self.first_dice] >= -1:
                return position, position + self.first_dice
            elif self.table[position] >= 1 and self.second_dice and \
                    self.table[position + self.second_dice] >= -1:
                return position, position + self.second_dice
        return None

    def pc_house_position(self):
        """check if with the given dice, can enter in the house with at least one of the dice
            Return:
                position in the house, where it can enter with at least one of the given dice
                None: in case of error"""
        if self.first_dice and self.table[self.first_dice - 1] >= -1:
            return self.first_dice - 1
        elif self.second_dice and self.table[self.second_dice - 1] >= -1:
            return self.second_dice - 1
        else:
            return None