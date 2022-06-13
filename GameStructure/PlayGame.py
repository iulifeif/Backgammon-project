import sys
from time import sleep

import pygame

from GameStructure.Backgammon import Backgammon, click_for_position
from GameStructure.Interface import choose_game_mode, Interface, display_winner, choose_game_difficulty
from Train.Board import Board
from Train.RN import Model


def play_game(player_info=None):
    """ the part where it unfolds the logic and the interface of the game
        This is the primary function where the game is played,
        pieces are added to the house, moves are made, and at the end it is displayed who won,
        and all these are displayed in the interface"""

    # create class instances so as to use them
    game_difficulty = 0
    number_of_turns = 0
    game_mode = choose_game_mode(player_info)
    game = Backgammon(game_mode)
    interf = Interface(game.player, game.table,
                       game.first_dice, game.second_dice,
                       game.end_pieces_0, game.end_pieces_1,
                       game.out_pieces_0, game.out_pieces_1, game_mode)
    while game_mode == 4:
        interf.display_rules()
        game_mode = choose_game_mode(player_info)
    if game_mode == 2:
        game_difficulty = choose_game_difficulty()
    interf.draw()
    while True:
        # roll the dice
        if (game_mode == 2 and game.player == 1) or game_mode == 3:
            sleep(1)
            game.roll_dice()
            sleep(1)
        elif game_mode == 1 or game.player == 0:
            col, line = click_for_position()
            if col < 740 or line >= 520:
                print("You can't roll the dice from that place")
            if 740 <= col and line <= 520:
                game.roll_dice()

        interf.update_dice(game.first_dice, game.second_dice, game.third_dice, game.fourth_dice)
        interf.draw()
        # if the player has pieces outside the table and can put them in the house
        while game.need_to_put_in_house() and game.can_put_in_house():
            position_home = -1
            if (game.game_mode == 1 or game.player == 0) and game.game_mode != 3:
                position_out = click_for_position()
                position_home = click_for_position()
            elif (game.game_mode == 2 and game.player == 1) or game.game_mode == 3:
                if game_difficulty == 1:
                    if game.player == 0:
                        position_home = game.choose_house_position_pc_player_0()
                    else:
                        position_home = game.choose_house_position_pc_player_1()
                else:
                    m = Model()
                    board = Board(game.table, game.out_pieces_1, game.out_pieces_0,
                                  game.end_pieces_1, game.out_pieces_0)
                    rolls = [game.first_dice, game.second_dice, game.third_dice, game.fourth_dice]
                    _bar, position_home = m.action(board, rolls, game.player)
                    m.update(board, game.player)
            game_copy = game.add_in_house(position_home)
            if game_copy is not None:
                game = game_copy
                interf.update_table(game.table)
                interf.update_dice(game.first_dice, game.second_dice, game.third_dice, game.fourth_dice)
                interf.update_end_pieces(game.end_pieces_0, game.end_pieces_1)
                interf.update_out_pieces(game.out_pieces_0, game.out_pieces_1)
                interf.draw()
            else:
                print("NU POT BAGA IN CASA IS NONE")
            if (game.game_mode == 2 and game.player == 1) or game.game_mode == 3:
                sleep(1.5)
        while game.can_move():
            position_start, position_end = game.return_positions_for_movement(interf, game_difficulty)
            if (game.game_mode == 2 and game.player == 1) or game.game_mode == 3:
                sleep(1)
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
        number_of_turns += 1
        interf.update_player(game.player)
        interf.update_dice(game.first_dice, game.second_dice, game.third_dice, game.fourth_dice)
        interf.draw()
        if game.end_pieces_0 == 15 or game.end_pieces_1 == 15:
            break
    # check who won, if someone won
    someone_won = game.won()
    if someone_won:
        player_response = display_winner(someone_won)
        if player_response == 4:
            choose_game_mode()
            return 0
        else:
            pygame.quit()
            sys.exit()
    else:
        print("Nobody won!")
