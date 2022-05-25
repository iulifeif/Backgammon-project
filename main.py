import copy
from time import sleep
import pygame
import sys

from backgammon import Backgammon, click_for_position
from interface import Interface, choose_game_mode
from colors import *

pygame.init()


def play_game():
    """ the part where it unfolds the logic and the interface of the game
        This is the primary function where the game is played,
        pieces are added to the house, moves are made, and at the end it is displayed who won,
        and all these are displayed in the interface"""
    # create class instances so as to use them

    game_mode = choose_game_mode()
    game = Backgammon(game_mode)
    interf = Interface(game.player, game.table,
                       game.first_dice, game.second_dice,
                       game.end_pieces_0, game.end_pieces_1,
                       game.out_pieces_0, game.out_pieces_1, game_mode)

    interf.draw()
    while True:
        # roll the dice
        if game_mode == 2 and game.player == 1:
            game.roll_dice()
            sleep(2)
        elif game_mode == 1 or game.player == 0:
            col, line = click_for_position()
            if 740 <= col and line <= 520:
                game.roll_dice()

        interf.update_dice(game.first_dice, game.second_dice, game.third_dice, game.fourth_dice)
        interf.draw()
        # if the player has pieces outside the table and can put them in the house
        while game.need_to_put_in_house() and game.can_put_in_house():
            print("poate baga si PC ul in casa")
            position_home = 0
            if game.game_mode == 1 or game.player == 0:
                position_out = click_for_position()
                position_home = click_for_position()
            elif game.game_mode == 2 and game.player == 1:
                position_home = game.pc_house_position()

            game_copy = game.add_in_house(position_home)
            # update map
            if game_copy is not None:
                game = game_copy
                interf.update_table(game.table)
                interf.update_dice(game.first_dice, game.second_dice, game.third_dice, game.fourth_dice)
                interf.update_end_pieces(game.end_pieces_0, game.end_pieces_1)
                interf.update_out_pieces(game.out_pieces_0, game.out_pieces_1)
                interf.draw()
            else:
                print("NU POT BAGA IN CASA IS NONE")
            if game.game_mode == 2 and game.player == 1:
                sleep(3)
        while game.can_move() and (game.first_dice != 0 or game.second_dice != 0 or
                                   game.third_dice != 0 or game.fourth_dice != 0):
            position_start, position_end = game.return_positions_for_movement(interf)
            if game.game_mode == 2 and game.player == 1:
                sleep(3)
            game_copy = game.move(position_start, position_end)
            if game_copy is not None:
                # update map
                game = game_copy
                interf.update_table(game.table)
                interf.update_dice(game.first_dice, game.second_dice, game.third_dice, game.fourth_dice)
                interf.update_end_pieces(game.end_pieces_0, game.end_pieces_1)
                interf.update_out_pieces(game.out_pieces_0, game.out_pieces_1)
                # redraw the board
                interf.draw()
            else:
                print("GAME IS NONE")
        # turn is over and switch the player
        game.switch_player()
        interf.update_player(game.player)
        interf.update_dice(game.first_dice, game.second_dice, game.third_dice, game.fourth_dice)
        interf.draw()
        if game.end_pieces_0 == 10 or game.end_pieces_1 == 10:
            break
    # check who won
    if game.end_pieces_1 == 10:
        # print at the console
        print("Player 1 WON!")
        # print at the screen
        font_title = pygame.font.SysFont("Roboto", 60)
        text_title = font_title.render("Player 1 WON!", True, BLACK)
        interf.screen.blit(text_title, (50 * 4, 50 * 8))
        sleep(5)
    elif game.end_pieces_0 == 10:
        print("Player 0 WON!")
        font_title = pygame.font.SysFont("Roboto", 60)
        text_title = font_title.render("Player 0 WON!", True, BLACK)
        interf.screen.blit(text_title, (50 * 4, 50 * 8))
        sleep(5)


if __name__ == '__main__':
    """ just play the game"""
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                break
        play_game()
