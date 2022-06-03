# Copyright 2021 Andrew Dunstall

import logging
import random
import time


# class GameTraining:
#     def __init__(self, game):
#         self.game = game
#
#     def won(self, player):
#         return self.game.won()
#
#     def play(self):
#         start = time.time()
#
#         turn = random.randint(0, 1)
#         logging.debug(f"game started [player = {turn}]")
#         steps = 0
#         while not self._board.won(turn):
#             turn = 1 - turn
#
#             self._agents[turn].turn(self._board)
#             self._agents[turn].update(self._board)
#             steps += 1
#
#         duration = time.time() - start
#         logging.info(f"game complete [duration = {duration}s], [winner = {turn}] [steps = {steps}]")
