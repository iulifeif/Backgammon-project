import copy
import random


class Backgammon:
    # table is formed by down side of game table reversed plus up side
    #     player0: human who wants to play with positive pieces
    #       player0 move <--<--
    #     player1: human or computer with negative pieces
    #         player1 move -->-->

    def __init__(self, dice1=0, dice2=0, table=None, player=0, home_player0=0, home_player1=0):
        self.dice_first = dice1
        self.dice_second = dice2
        if table is None:
            self.table = [2, 0, 0, 0, 0, -5, 0, -3, 0, 0, 0, 5, -5, 0, 0, 0, 3, 0, 5, 0, 0, 0, 0, -2]
        else:
            self.table = copy.deepcopy(table)
        self.player = player
        self.home_player0 = home_player0
        self.home_player1 = home_player1

    def roll_the_dice(self):
        self.dice_first = random.randint(1, 6)
        self.dice_second = random.randint(1, 6)

    def view_table(self):
        print([indices for indices in range(len(self.table))])
        print(self.table)

    def move(self, dice, position_piece):
        temporary_state = Backgammon(self.dice_first, self.dice_second, self.table, self.player, self.home_player1,
                                     self.home_player2)

        # if is human
        if self.player == 0 and self.table[position_piece] < 0:
            end_position = position_piece - dice
            if self.table[end_position] <= 0:
                # remove the piece from the starting place
                temporary_state.table[position_piece] += 1
                # add the piece
                temporary_state.table[end_position] -= 1
            elif self.table[end_position] == 1:
                # remove the piece from the starting place
                temporary_state.table[position_piece] += 1
                # add the piece
                temporary_state.table[end_position] = -1
            else:
                return None

        # if is computer
        elif self.player == 1 and self.table[position_piece] > 0:
            end_position = position_piece + dice
            if self.table[end_position] >= 0:
                # remove the piece from the starting place
                temporary_state.table[position_piece] -= 1
                # add the piece
                temporary_state.table[end_position] += 1
            elif self.table[end_position] == -1:
                # remove the piece from the starting place
                temporary_state.table[position_piece] -= 1
                # add the piece
                temporary_state.table[end_position] = 1
            else:
                return None
        else:
            return None

        if temporary_state.dice_first == dice:
            temporary_state.dice_first = 0
        elif temporary_state.dice_second == dice:
            temporary_state.dice_second = 0
        else:
            return None
        return temporary_state

    def pieces_out(self):
        pieces = 0
        for index in range(len(self.table)):
            if (self.player == 0 and self.table[index] < 0) or \
                    (self.player == 1 and self.table[index] > 0):
                pieces += self.table[index]
        if self.player == 0:
            pieces += self.home_player0
        else:
            pieces += self.home_player1
        return abs(pieces)

    def add_in_house(self, dice):
        temporary_state = Backgammon(self.dice_first, self.dice_second, self.table, self.player, self.home_player1,
                                     self.home_player2)
        if self.player == 0:
            # if the box in occupied by player1
            if temporary_state.table[dice - 1] <= 0:
                temporary_state.table[dice - 1] -= 1
            # if the box is occupied by a single piece of the player2
            elif temporary_state.table[dice - 1] == 1:
                temporary_state.table[dice - 1] = -1
            else:
                return None
        elif self.player == 1:
            position_in_home = len(temporary_state.table) - dice + 1
            if temporary_state.table[position_in_home] >= 0:
                temporary_state.table[position_in_home] += 1
            elif temporary_state.table[position_in_home] == -1:
                temporary_state.table[position_in_home] = 1
            else:
                return None
        if temporary_state.dice_first == dice:
            temporary_state.dice_first = 0
        elif temporary_state.dice_second == dice:
            temporary_state.dice_second = 0
        else:
            return None
        return temporary_state

    def player_can_move(self):
        if not self.dice_first and not self.dice_second:
            return 0
        for position in range(len(self.table)):
            if self.player == 0 and self.table[position] < 0 and \
                    (self.table[position - self.dice_first] < 0 or self.table[position - self.dice_first] == 1):
                return 1
            if self.player == 0 and self.table[position] < 0 and \
                    (self.table[position - self.dice_second] < 0 or self.table[position - self.dice_second] == 1):
                return 1
            if self.player == 1 and self.table[position] > 0 and \
                    (self.table[position + self.dice_first] > 0 or self.table[position + self.dice_first] == -1):
                return 1
            if self.player == 1 and self.table[position] > 0 and \
                    (self.table[position + self.dice_second] > 0 or self.table[position + self.dice_second] == -1):
                return 1
        return 0

    def player_can_add_in_house(self):
        if self.player == 0 and self.dice_first and self.table[self.dice_first - 1] <= 1:
            return 1
        if self.player == 0 and self.dice_second and self.table[self.dice_second - 1] <= 1:
            return 1
        if self.player == 1 and self.dice_first and self.table[self.dice_first - 1] >= -1:
            return 1
        if self.player == 1 and self.dice_second and self.table[self.dice_second - 1] >= -1:
            return 1
        return 0

    def end_game(self):
        return self.home_player0 == 10 or self.home_player1 == 10

    def all_pieces_in_house(self):
        pass


def play_game():
    game = Backgammon()
    game.view_table()
    # cat timp jocul nu s-a terminat
    while not game.end_game():
        # afiseaza ce player joaca
        print("Player {}: ".format(game.player))
        # da cu zarul
        game.roll_the_dice()
        # se afiseaza zarurile
        print("Zarurile tale sunt: {}, {}".format(game.dice_first, game.dice_second))
        # cazul cand are piese afara
        if game.pieces_out() != 10 and game.player_can_add_in_house():
            game.add_in_house(game.dice_first)
        if game.pieces_out() != 10 and game.player_can_add_in_house():
            game.add_in_house(game.dice_second)
        if game.player_can_move():
            # move for first dice
            while game.dice_first:
                start = int(input("Pozitia de la care vrei sa faci mutarea pt zarul1: "))
                temporary_game = game.move(game.dice_first, start)
                if temporary_game is not None:
                    game = temporary_game
                else:
                    print("Ai introdus o pozitie gresita!")
            game.view_table()

            # move for second dice
            while game.dice_second:
                start = int(input("Pozitia de la care vrei sa faci mutarea pt zarul2: "))
                temporary_game = game.move(game.dice_second, start)
                if temporary_game is not None:
                    game = temporary_game
                else:
                    print("Ai introdus o pozitie gresita!")
            game.view_table()
        else:
            print("Nu ai mutari valide!")
        print("S-a terminat tura")
        game.player = (game.player + 1) % 2


if __name__ == '__main__':
    play_game()
