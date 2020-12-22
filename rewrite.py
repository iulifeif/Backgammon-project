import copy
import random


class Backgammon:
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

    def print_table(self):
        print([indices for indices in range(len(self.table))])
        print(self.table)

    def roll_dices(self):
        self.first_dice = random.randint(1, 6)
        self.second_dice = random.randint(1, 6)

    def end_game(self):
        return self.end_pieces_1 == 10 or self.end_pieces_0 == 10

    def pieces_out(self):
        # daca are piese afara, le bag in casa, daca nu, apelez mutari
        number_pieces = self.out_pieces_0 if self.player == 0 else self.out_pieces_1
        if number_pieces >= 2:
            self.add_in_house(self.first_dice, self.second_dice)

        elif number_pieces == 1:
            dice = int(input("Cu ce zar vrei sa intrii in casa? : "))
            if self.first_dice == dice:
                self.add_in_house(dice, 0)
                if self.can_move():
                    self.choose_to_move()
                else:
                    self.second_dice = 0
            elif self.second_dice == dice:
                self.add_in_house(0, dice)
                if self.can_move():
                    self.choose_to_move()
                else:
                    self.first_dice = 0
            else:
                return None

        else:
            while self.can_move():
                self.choose_to_move()
        self.switch_player()

    def switch_player(self):
        print("Tura ta s-a terminat")
        self.player = (self.player + 1) % 2

    def add_in_house(self, dice1, dice2):
        temporary_state = Backgammon(self.player, self.table, self.first_dice, self.second_dice, self.end_pieces_0, self.end_pieces_1, self.out_pieces_0, self.out_pieces_1)
        if self.player == 0:
            if dice1:
                if temporary_state.table[dice1 - 1] <= 0:
                    temporary_state.table[dice1 - 1] -= 1
                    temporary_state.out_pieces_0 -= 1
                elif temporary_state.table[dice1 - 1] == 1:
                    temporary_state.table[dice1 - 1] = -1
                    temporary_state.out_pieces_0 -= 1
                    temporary_state.out_pieces_1 += 1
                else:
                    temporary_state.first_dice = 0
                    return None
            if dice2:
                if temporary_state.table[dice2 - 1] <= 0:
                    temporary_state.table[dice2 - 1] -= 1
                    temporary_state.out_pieces_0 -= 1
                elif temporary_state.table[dice2 - 1] == 1:
                    temporary_state.table[dice2 - 1] = -1
                    temporary_state.out_pieces_0 -= 1
                    temporary_state.out_pieces_1 += 1
                else:
                    temporary_state.second_dice = 0
                    return None
        elif self.player == 1:
            if dice1:
                if temporary_state.table[24 - dice1] >= 0:
                    temporary_state.table[24 - dice1] += 1
                    temporary_state.out_pieces_1 -= 1
                elif temporary_state.table[24 - dice1] == -1:
                    temporary_state.table[24 - dice1] = 1
                    temporary_state.out_pieces_1 -= 1
                    temporary_state.out_pieces_0 += 1
                else:
                    temporary_state.first_dice = 0
                    return None
            if dice2:
                if temporary_state.table[24 - dice2] >= 0:
                    temporary_state.table[24 - dice2] += 1
                    temporary_state.out_pieces_1 -= 1
                elif temporary_state.table[24 - dice2] == -1:
                    temporary_state.table[24 - dice2] = 1
                    temporary_state.out_pieces_1 -= 1
                    temporary_state.out_pieces_0 += 1
                else:
                    temporary_state.second_dice = 0
                    return None
        return temporary_state

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

    def move(self, start_position, dice):
        temporary_state = Backgammon(self.player, self.table, self.first_dice, self.second_dice, self.end_pieces_0, self.end_pieces_1, self.out_pieces_0, self.out_pieces_1)
        if temporary_state.player == 0:
            temporary_state.table[start_position] += 1
            if start_position - dice == 0:
                temporary_state.end_pieces_0 += 1
            elif temporary_state.table[start_position - dice] <= 0:
                temporary_state.table[start_position - dice] -= 1
            elif temporary_state.table[start_position - dice] == 1:
                temporary_state.table[start_position - dice] = -1
            else:
                return None
        elif temporary_state.player == 1:
            temporary_state.table[start_position] -= 1
            if start_position + dice == 24:
                temporary_state.end_pieces_1 += 1
            elif temporary_state.table[start_position + dice] >= 0:
                temporary_state.table[start_position + dice] += 1
            elif temporary_state.table[start_position + dice] == -1:
                temporary_state.table[start_position + dice] = 1
            else:
                return None
        if temporary_state.first_dice == dice and temporary_state.first_dice:
            temporary_state.first_dice = 0
        elif temporary_state.second_dice == dice and temporary_state.second_dice:
            temporary_state.second_dice = 0
        else:
            return None
        return temporary_state

    def choose_to_move(self):
        if self.first_dice:
            position = int(input("Alege pozitia piesei pentru zarul 1: "))
            self.move(position, self.first_dice)
        if self.second_dice:
            position = int(input("Alege pozitia piesei pentru zarul 2: "))
            self.move(position, self.second_dice)


def play_game():
    game = Backgammon()
    while not game.end_game():
        print("Acum joaca playerul: {}".format(game.player))
        game.roll_dices()
        print("Cu zarurile: {}, {}".format(game.first_dice, game.second_dice))
        game.print_table()
        game.pieces_out()


if __name__ == '__main__':
    play_game()
