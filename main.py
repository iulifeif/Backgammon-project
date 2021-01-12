import copy
import random
from time import sleep
import pygame
import sys

pygame.init()

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BROWN = (150, 75, 0)
BLUE = (106, 159, 181)


class Interface:
    # initialize table with fixed dimensions
    def __init__(self):
        self.squaresize = 50
        self.column_count = 12
        self.row_count = 16
        self.width = self.squaresize * (self.column_count + 1)
        self.height = self.squaresize * self.row_count
        self.size = (self.width, self.height)
        self.radius = int(self.squaresize / 2 - 5)
        self.screen = pygame.display.set_mode(self.size)
        self.up_table = []
        self.down_table = []
        pygame.display.set_caption("Backgammon")

    # split the original table from logic (which is a list) in 2 lists
    # one for up site of table and another one for down side
    def prepro(self, table):
        # from the middle to the end is up side
        self.up_table = table[len(table) // 2:]
        intermediary_down_table = table[:len(table) // 2]
        self.down_table = []
        # from the beginning to the middle is down side, but need to be reversed
        for pos in reversed(range(len(intermediary_down_table))):
            self.down_table.append(intermediary_down_table[pos])

    # draw the pieces according to the board received
    # and the velue of pieces, because player 0 has negative pieces and player 1 positive pieces
    def draw_pieces(self, table, pos):
        for col in range(len(table)):
            line = pos
            while table[col] != 0:
                if table[col] < 0:
                    # if the piece has negative value, piece is BROWN, because player 0 has BROWN pieces
                    pygame.draw.circle(self.screen, BROWN,
                                       (int(col * self.squaresize + self.squaresize / 2),
                                        int(line * self.squaresize + self.squaresize + self.squaresize / 2)),
                                       self.radius)
                    table[col] += 1
                elif table[col] > 0:
                    # if the piece has positive value, piece is WHITE, because player 1 has WHITE pieces
                    pygame.draw.circle(self.screen, WHITE,
                                       (int(col * self.squaresize + self.squaresize / 2),
                                        int(line * self.squaresize + self.squaresize + self.squaresize / 2)),
                                       self.radius)
                    table[col] -= 1
                # the line at which it is drawn moves up or down
                # depending on the part of the board on which it is located
                line = line + 1 if pos == 0 else line - 1

    # draw the pieces that are taken out of the board
    # player 0 at the top, and player 1 at the bottom
    def draw_outer_pieces(self, out_pieces, pos):
        # out_pieces is a number, not a list
        # a number that means how many pieces are removed
        # for player 0, number is negative and for player1 the opposite

        color = BROWN if pos == 0 else WHITE
        line = pos
        while out_pieces != 0:
            # if the position is 0 (which means up side), piece is BROWN
            # because player 0 has the pieces taken out of the board at the top
            # otherwise means down side, piece is WHITE
            # because player 1 has the pieces taken out of the board at the bottom
            pygame.draw.circle(self.screen, color,
                               (int(12 * self.squaresize + self.squaresize / 2),
                                int(line * self.squaresize + self.squaresize + self.squaresize / 2)),
                               self.radius)
            out_pieces -= 1
            # the line at which it is drawn moves up or down
            # depending on the part of the board on which it is located
            line = line + 1 if pos == 0 else line - 1

    # draw on the whole right side of the board, black pieces to erase the old pieces
    def clean_outer_pieces(self):
        # like the board, there are 16 lines
        for line in range(16):
            pygame.draw.circle(self.screen, BLACK,
                               (int(12 * self.squaresize + self.squaresize / 2),
                                int(line * self.squaresize + self.squaresize + self.squaresize / 2)),
                               self.radius)

    def choose_player(self):
        self.screen.fill(BLUE)
        pygame.display.update()
        font_title = pygame.font.SysFont("Roboto", 45)
        text_title = font_title.render("Choose the player type: ", True, WHITE)
        self.screen.blit(text_title, (self.width / 5,
                                      self.height / 3))

        font_title = pygame.font.SysFont("Roboto", 30)
        text_title = font_title.render("Person", True, WHITE)
        self.screen.blit(text_title, (self.width / 2 - self.squaresize + 10,
                                      self.height / 3 + self.squaresize * 2))

        font_title = pygame.font.SysFont("Roboto", 30)
        text_title = font_title.render("Computer", True, WHITE)
        self.screen.blit(text_title, (self.width / 2 - self.squaresize,
                                      self.height / 3 + self.squaresize * 4))
        pygame.display.update()
        player_type = -1
        while player_type == -1:
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    col, line = event.pos
                    print(event.pos)
                    if 275 <= col <= 360 and \
                            355 <= line <= 390:
                        # which means person
                        return 1
                    elif 265 <= col <= 380 and \
                            455 <= line <= 490:
                        # which means computer
                        return 2

    # the board is drawn as a matrix with green elements
    # then add in each square, a black circle
    def draw_board(self, table, table_out_0, table_out_1):
        for index_column in range(self.column_count):
            for index_line in range(self.row_count):
                pygame.draw.rect(self.screen,
                                 GREEN,
                                 (index_column * self.squaresize,
                                  index_line * self.squaresize + self.squaresize,
                                  self.squaresize,
                                  self.squaresize))
                # less on line 7, to delimit the up side from the bottom
                if index_line != 7:
                    pygame.draw.circle(self.screen,
                                       BLACK,
                                       (int(index_column * self.squaresize + self.squaresize / 2),
                                        int(index_line * self.squaresize + self.squaresize + self.squaresize / 2)),
                                       self.radius)
        # model the table to be more easily to take the positions of the pieces
        self.prepro(table)
        # draw pieces for up side and down side
        self.draw_pieces(self.up_table, 0)
        self.draw_pieces(self.down_table, 14)
        # erase the old pieces taken out
        self.clean_outer_pieces()
        # draw the new pieces taken out (update the column)
        self.draw_outer_pieces(table_out_0, 0)
        self.draw_outer_pieces(table_out_1, 14)
        # update the whole screen
        pygame.display.update()


class Backgammon:
    # initializes the state
    def __init__(self, player=0, table=None,
                 dice1=0, dice2=0,
                 end_pieces_0=0, end_pieces_1=0,
                 out_pieces_0=0, out_pieces_1=0):
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

    # printing at the screen the game board (including position indexes)
    def print_table(self):
        print([indices for indices in range(len(self.table))])
        print(self.table)

    # dice initialization
    def roll_dice(self):
        # a dice can have a value 1 and 6
        self.first_dice = random.randint(1, 6)
        self.second_dice = random.randint(1, 6)

    # check if one of the players has finished the game
    # (if he has removed all the pieces from the table)
    def end_game(self):
        return self.end_pieces_1 == 10 or self.end_pieces_0 == 10

    # the player is updated from 0 to 1 and vice versa
    def switch_player(self):
        self.player = (self.player + 1) % 2

    # check if the player has pieces to put in the house
    def need_to_put_in_house(self):
        # check which player has to move and he has outer pieces
        return (self.player == 0 and self.out_pieces_0) or \
               (self.player == 1 and self.out_pieces_1)

    def can_put_in_house(self):
        # if exist a valid dice and can put the piece in the house with that dice, returns True
        # if is nowhere to put the piece in the house, the dice are canceled and moves to the next player
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

    # add in the house to the received position
    def add_in_house(self, position):
        # create a copy for state
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

    # check if player is able to move a piece
    def can_move(self):
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

    # move a piece on the table, from a specific position to another specific position
    def move(self, start_position, end_position):
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
        for position in range(len(self.table)):
            if self.table[position] >= 1 and self.first_dice and \
                    self.table[position + self.first_dice] >= -1:
                return position, position + self.first_dice
            elif self.table[position] >= 1 and self.second_dice and \
                    self.table[position + self.second_dice] >= -1:
                return position, position + self.second_dice
        return None

    def pc_house_position(self):
        if self.first_dice and self.table[self.first_dice - 1] >= -1:
            return self.first_dice - 1
        elif self.second_dice and self.table[self.second_dice - 1] >= -1:
            return self.second_dice - 1
        else:
            return None


# receives the coordinates where it is clicked and
# returns the position in the table from logic part
def click_for_position(interf):
    col = -1
    line = -1
    # wait until receive the first click
    while col == -1:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                # save the position in col and line
                col, line = event.pos
                # divides according to the size of the squares
                line = int(line / interf.squaresize)
                col = int(col / interf.squaresize)
    # if the line is smaller than 7, it means we are talking about the top of the board
    # otherwise the bottom
    if line < 7:
        print("s-a ales pozitia")
        return col + 12
    elif line > 7:
        print("s-a ales pozitia")
        return 11 - col


# print the received message on the screen (at the top of the board)
def message(interf, game, text, number_message):
    # this number is for indent the text
    number = 3 if number_message == 1 else 8
    text_rect = text.get_rect()
    text_rect.center = (interf.squaresize * number, interf.squaresize / 2)
    interf.screen.blit(text, text_rect)
    interf.draw_board(game.table, game.out_pieces_0, game.out_pieces_1)


# the part where it unfolds the logic and the interface of the game
def play_game():
    # create class instances so as to use them
    game = Backgammon()
    interf = Interface()
    player_type = interf.choose_player()
    # initialize a variable to turn off the loop if needed
    game_over = False
    # create the font for the text
    font = pygame.font.Font(None, 28)
    # draw the interface

    interf.draw_board(game.table, game.out_pieces_0, game.out_pieces_1)
    while not game.end_game() and not game_over:
        # add player information on the screen
        color = "BROWN" if game.player == 0 else "WHITE"
        text = font.render("Player: {}".format(color), True, WHITE, BLACK)
        message(interf, game, text, 1)

        # roll the dice
        game.roll_dice()

        # add information about the dice on the screen
        text = font.render("Dice: {}, {}".format(game.first_dice, game.second_dice), True, WHITE, BLACK)
        message(interf, game, text, 2)

        # if game is with computer and computer needs to move, wait 5s to see the table
        if player_type == 2 and game.player == 1:
            sleep(5)

        # if the player has pieces outside the table and can put them in the house
        while game.need_to_put_in_house() and game.can_put_in_house():
            # position_home = int(input("Unde vrei sa intrii cu piesa: "))
            # click where i want to put the piece
            position_home = 0
            # first if: game mode is with 2 players, both of they click for position, or
            # game mode is 2(computer) and human needs to move
            # second if is for game with computer when computer needs to move
            if player_type == 1 or game.player == 0:
                position_home = click_for_position(interf)
            elif player_type == 2 and game.player == 1:
                position_home = game.pc_house_position()

            # if the position he wants to move to is not a valid one, he cannot move to that place
            # click until it receives a valid position
            game_copy = copy.deepcopy(game)
            game = game.add_in_house(position_home)
            while game is None:
                print("Wrong position! Click again!")
                position_home = click_for_position(interf)
                game = game_copy.add_in_house(position_home)

            # redraw the table after the move
            interf.draw_board(game.table, game.out_pieces_0, game.out_pieces_1)
            if player_type == 2 and game.player == 1:
                sleep(5)
        while game.can_move():
            position_start = 0
            position_end = 0

            # first if: game mode is with 2 players, both of they click for position, or
            # game mode is 2(computer) and human needs to move
            # second if is for game with computer when computer needs to move
            if player_type == 1 or game.player == 0:
                # click to select the piece which i want to be moved
                position_start = click_for_position(interf)
                # click to select the position where to move the piece
                position_end = click_for_position(interf)
            elif player_type == 2 and game.player == 1:
                position_start, position_end = game.pc_piece_positions()

            # if the positions are not a valid, player cannot move
            # click until it receives valid positions
            game_copy = copy.deepcopy(game)
            game = game.move(position_start, position_end)
            while game is None:
                print("Wrong position! Click again! ")
                position_start = click_for_position(interf)
                position_end = click_for_position(interf)
                game = game_copy.move(position_start, position_end)

            # redraw the board
            interf.draw_board(game.table, game.out_pieces_0, game.out_pieces_1)
            # if game is with computer and computer needs to move, wait 5s to see the table
            if player_type == 2 and game.player == 1:
                sleep(5)
        # turn is over and switch the player
        game.switch_player()
        # quit from x
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
                sys.exit()
    # check who won
    if game.end_pieces_1 == 10:
        print("Player 1 WON!")
    elif game.end_pieces_0 == 10:
        print("Player 0 WON!")


if __name__ == '__main__':
    play_game()
