import argparse
import logging

import pygame
from keras import Model

from GameStructure.PlayGame import play_game
from utils.Evaluation import Evaluation

pygame.init()


def parse_args():
    parser = argparse.ArgumentParser(description="TD-Gammon model.")
    parser.add_argument(
        "--test", action='store_true', help="test model"
    )
    parser.add_argument(
        "--train", action='store_true', help="train model"
    )
    parser.add_argument(
        "--debug", action='store_true', help="debug logging"
    )
    parser.add_argument(
        "--restore", help="path to the model to restore from"
    )
    return parser.parse_args()


def main(args):
    logging.basicConfig(level=logging.DEBUG if args.debug else logging.INFO)

    m = Model(args.restore)
    if args.test:
        m.test()
    elif args.train:
        m.train()
    else:
        ev = Evaluation()
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    break
            number_of_turns, player = play_game()
            ev.add_game_data(number_of_turns, player)
            ev.evaluate()


if __name__ == "__main__":
    main(parse_args())
    # m = Model()
    # m.train()
