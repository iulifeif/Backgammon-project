import copy
import random


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
    def add_in_house(self, dice):
        new_state = Backgammon(self.player, self.table, self.first_dice, self.second_dice, self.end_pieces_0,
                               self.end_pieces_1, self.out_pieces_0, self.out_pieces_1)
        position = dice - 1 if self.player == 0 else 24 - dice
        piece_sign = 1 if self.player == 0 else -1

        if self.player_sign[self.player](new_state.table[position], 0):
            # daca pe pozitia respectiva sunt piese de acelasi fel sau nu e niciuna
            new_state.table[position] -= piece_sign
            if not self.player:
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
        if self.first_dice and self.first_dice == dice:
            self.first_dice = 0
        elif self.second_dice and self.second_dice == dice:
            self.second_dice = 0
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

    def move(self, start_position, dice):
        new_state = Backgammon(self.player, self.table, self.first_dice, self.second_dice,
                                     self.end_pieces_0, self.end_pieces_1, self.out_pieces_0, self.out_pieces_1)
        position = start_position - dice if self.player == 0 else start_position + dice
        piece_sign = 1 if self.player == 0 else -1
        end_position = 0 if self.player == 0 else 24

        new_state.table[start_position] += piece_sign
        if position == end_position:
            if self.player == 0:
                new_state.end_pieces_0 += 1
            else:
                new_state.end_pieces_1 += 1
        elif self.player_sign[self.player](new_state.table[position], 0):
            new_state.table[position] -= piece_sign
        elif new_state.table[position] == piece_sign:
            new_state.table[position] = -1 * piece_sign
            if self.player == 0:
                new_state.out_pieces_1 += 1
            else:
                new_state.out_pieces_0 += 1
        else:
            return None

        if new_state.first_dice == dice and new_state.first_dice:
            new_state.first_dice = 0
        elif new_state.second_dice == dice and new_state.second_dice:
            new_state.second_dice = 0
        else:
            return None

        return new_state


def play_game():
    game = Backgammon()
    while not game.end_game():
        print("Acum joaca playerul: {}".format(game.player))
        game.roll_dices()
        print("Cu zarurile: {}, {}".format(game.first_dice, game.second_dice))
        print("Tabla de start: ")
        game.print_table()
        while game.need_to_put_in_house():
            number_dice = int(input("Cu ce zar vrei sa intrii in casa?: "))
            game = game.add_in_house(number_dice)
            print("Tabla dupa ce a intrat cu piesa in casa: ")
            game.print_table()
        while game.can_move():
            position = int(input("Pozitia de la care vrei sa muti piesa: "))
            number_dice = int(input("Cu ce zar vrei sa muti piesa?: "))
            game = game.move(position, number_dice)
            print("Tabla dupa ce a mutat piesa: ")
            game.print_table()
        game.switch_player()
    if game.end_pieces_1 == 10:
        print("Jucatorul 1 a castigat!")
    elif game.end_pieces_0 == 10:
        print("Jucatorul 0 a castigat!")


if __name__ == '__main__':
    play_game()
