import copy
from time import sleep
import pygame
import sys

from game import Backgammon
from interface import Interface, choose_game_mode
from colors import *


pygame.init()


def click_for_position(interf):
    """this function waits to receive a click to take the coordinates and turn them into position on the logic table
        Args:
            interf(obj): object for interface to call class variables
        Return:
            the position in the table from logic part corresponding to the coordinates where was clicked"""
    col = -1
    line = -1
    # wait until receive the first click
    while col == -1:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                # save the position in col and line
                col, line = event.pos
                # if press Quit
                if 600 <= col <= 630 and 10 <= line <= 40:
                    pygame.quit()
                    sys.exit()
                # divides according to the size of the squares
                line = int(line / interf.squaresize)
                col = int(col / interf.squaresize)
            # quit from x
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
    pygame.draw.circle(interf.screen,
                       SELECTED,
                       (int(col * interf.squaresize + interf.squaresize / 2),
                        int((line - 1) * interf.squaresize + interf.squaresize + interf.squaresize / 2)),
                       interf.radius)
    pygame.display.update()
    # if the line is smaller than 7, it means we are talking about the top of the board
    # otherwise the bottom
    if line <= 7:
        return col + 12
    elif line > 7:
        return 11 - col


def play_game():
    """ the part where it unfolds the logic and the interface of the game
        This is the primary function where the game is played,
        pieces are added to the house, moves are made, and at the end it is displayed who won,
        and all these are displayed in the interface"""
    # create class instances so as to use them
    game = Backgammon()
    interf = Interface(game.table,
                       game.first_dice, game.second_dice,
                       game.end_pieces_0, game.end_pieces_1,
                       game.out_pieces_0, game.out_pieces_1)
    player_type = choose_game_mode()
    # initialize a variable to turn off the loop if needed
    # create the font for the text
    font = pygame.font.Font(None, 28)
    # draw the interface

    interf.draw_board()
    while not game.end_game():
        # roll the dice
        game.roll_dice()

        # if game is with computer and computer needs to move, wait 5s to see the table
        if player_type == 2 and game.player == 1:
            sleep(5)

        # if the player has pieces outside the table and can put them in the house
        while game.need_to_put_in_house() and game.can_put_in_house():
            # position_home = int(input("Unde vrei sa intrii cu piesa: "))
            # click where i want to put the piece
            position_home = 0
            # first if: game mode is with 2 players, both of them click for position, or
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
                interf.draw_board(game_copy.table, game_copy.out_pieces_0, game_copy.out_pieces_1)
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
                interf.draw_board(game_copy.out_pieces_0, game_copy.out_pieces_1)
                position_start = click_for_position(interf)
                position_end = click_for_position(interf)
                game = game_copy.move(position_start, position_end)

            # redraw the board
            interf.draw_board(game.out_pieces_0, game.out_pieces_1)
            # if game is with computer and computer needs to move, wait 5s to see the table
            if player_type == 2 and game.player == 1:
                sleep(5)
        # turn is over and switch the player
        game.switch_player()

    # check who won
    if game.end_pieces_1 == 10:
        # print at the console
        print("Player 1 WON!")
        # print at the screen
        font_title = pygame.font.SysFont("Roboto", 60)
        text_title = font_title.render("Player 1 WON!", True, BLACK)
        interf.screen.blit(text_title, (interf.squaresize * 4, interf.squaresize * 8))
        sleep(5)
    elif game.end_pieces_0 == 10:
        print("Player 0 WON!")
        font_title = pygame.font.SysFont("Roboto", 60)
        text_title = font_title.render("Player 0 WON!", True, BLACK)
        interf.screen.blit(text_title, (interf.squaresize * 4, interf.squaresize * 8))
        sleep(5)


if __name__ == '__main__':
    """ just play the game"""
    play_game()
