import copy
import logging
from time import time

import numpy as np
import tf

from Board import Board
from GameStructure.Backgammon import Backgammon
from utils.Imports import *


class Model:
    """
    Model wraps the neural net and provides methods for training and
    action selection by the agent.
    """
    _LAMBDA = 0.7
    _ALPHA = 0.1

    def __init__(self, restore_path=None):
        """Construct a model with random weights.

        Arguments:
        restore_path -- path to stored checkpoint to restore if given
            (default None)
        """
        inputs = tf.keras.Input(shape=(198,))
        x = tf.keras.layers.Dense(40, activation="sigmoid")(inputs)
        outputs = tf.keras.layers.Dense(1, activation="sigmoid")(x)
        self._model = tf.keras.Model(inputs=inputs, outputs=outputs)

        # Lazily initialize trace once the shape of the gradients is known.
        self._trace = []
        self.game_state = Backgammon(3)
        self._state = tf.Variable(self.game_state.encode_state(0))
        self._value = tf.Variable(self._model(self._state[np.newaxis]))

        if restore_path is not None:
            self.load(restore_path)

    def train(self, n_episodes=5000, n_validation=500, n_checkpoint=500, n_tests=1000):
        """Trains the model.


        Arguments:
        n_episodes -- number of episodes to train (default 5000)
        n_validation -- number of episodes between testing the model
            (default 500)
        n_checkpoint -- number of episodes between saving the model
            (default 500)
        n_tests -- number of episodes to test (default 1000)
        """
        logging.info("training model [n_episodes = %d]", n_episodes)
        for episode in range(1, n_episodes + 1):
            logging.info("running episode [episode = %d]", episode)
            if episode % n_validation == 0:
                self.test(n_tests)
            if episode > 1 and episode % n_checkpoint == 0:
                self.save()
            number_of_turns, who_won = self.fast_game()
            self._reset_trace()

        self.save()

    def test(self, n_episodes=100):
        """Tests the model against a random agent.

        Arguments:
        n_episodes -- number of episodes to test (default 100)
        """
        logging.info("testing model [n_episodes = %d]", n_episodes)
        wins = 0
        for episode in range(1, n_episodes + 1):
            number_of_moves, player = self.fast_game()

            if player:
                wins += 1

            logging.info("game complete [model wins %d] [episodes %d]", player, episode)

        logging.info("test complete [model win ratio %f]", wins / n_episodes)

    def action(self, board, roll, player):
        """Predicts the optimal move given the current state.

        This calculates each afterstate for all possible moves given the
        current state and selects the action that leads to the state with
        the greatest afterstate value.

        Arguments:
        board -- board containing the game state
        roll -- list of dice rolls left in the players turn
        player -- number of the player
        """
        start = time()

        max_move = None
        max_prob = -np.inf
        permitted = board.permitted_moves(roll, player)
        print("[PERMITED] ", permitted)
        for move in permitted:
            afterstate = copy.deepcopy(board)
            if not afterstate.move(*move, player):
                logging.error("model requested an invalid move")
                continue

            state = afterstate.encode_state(player)[np.newaxis]
            prob = tf.reduce_sum(self._model(state))
            # The network gives the probability of player 0 winning so must
            # change if player 1.
            prob = 1 - prob if player == 1 else prob

            if prob > max_prob:
                max_prob = prob
                max_move = move

        if self._state is None:
            self._state = tf.Variable(board.encode_state(player))
        if self._value is None:
            self._value = tf.Variable(self._model(self._state[np.newaxis]))

        duration = time() - start
        logging.debug("playing move [player = %d] [move = %s] [winning prob = %f] [duration = %ds]",
                      self.game_state.player, str(max_move), max_prob, duration)
        return max_move

    def update(self, board, player):
        """Updates the model given the current state and reward.

        This is expected to be called after the player has made their move.

        The aim is to move the predicted values towards the actual reward
        using TD-lambda.

        Arguments:
        board -- board containing the game state
        roll -- list of dice rolls left in the players turn
        """
        start = time()

        x_next = board.encode_state(player)
        with tf.GradientTape() as tape:
            value_next = self._model(x_next[np.newaxis])

        trainable_vars = self._model.trainable_variables
        grads = tape.gradient(value_next, trainable_vars)

        # Lazily initialize when gradient shape known.
        if len(self._trace) == 0:
            for grad in grads:
                self._trace.append(tf.Variable(
                    tf.zeros(grad.get_shape()), trainable=False
                ))

        if player == 0 and board.won(player):
            reward = 1
        else:
            reward = 0

        td_error = tf.reduce_sum(reward + value_next - self._value)
        for i in range(len(grads)):
            self._trace[i].assign((self._LAMBDA * self._trace[i]) + grads[i])

            grad_trace = self._ALPHA * td_error * self._trace[i]
            self._model.trainable_variables[i].assign_add(grad_trace)

        self._state = tf.Variable(x_next)
        self._value = tf.Variable(value_next)

        duration = time() - start
        logging.debug("updating model [player = %d] [duration = %ds]", player, duration)

    def load(self, path):
        logging.info("loading checkpoint [path = %s]", path)

        ckpt = tf.train.Checkpoint(model=self._model, state=self._state, value=self._value)
        ckpt.restore(path)

    def save(self):
        if not os.path.exists('checkpoint'):
            os.mkdir('checkpoint')

        # directory = 'checkpoint/model-' + str(datetime.datetime.now().strftime("%Y-%m-%d-%H.%M.%S"))
        directory = 'checkpoint/model-0'
        if not os.path.exists(directory):
            os.mkdir(directory)

        ckpt = tf.train.Checkpoint(model=self._model, state=self._state, value=self._value)
        path = ckpt.save(directory)

        logging.info("saving checkpoint [path = %s]", path)

        return path

    def _reset_trace(self):
        for i in range(len(self._trace)):
            self._trace[i].assign(tf.zeros(self._trace[i].get_shape()))

    def fast_game(self):
        game_mode = 3
        game = Backgammon(game_mode)
        turns = 0
        while True:
            game.roll_dice()
            print("[1]while")
            # if the player has pieces outside the table and can put them in the house
            while game.need_to_put_in_house() and game.can_put_in_house():
                print("[2]house")
                if not game.player:
                    position_home = game.choose_house_position_pc_player_0()
                    game_copy = game.add_in_house(position_home)
                else:
                    board = Board(game.table,
                                  game.out_pieces_1, game.out_pieces_0,
                                  game.end_pieces_1, game.out_pieces_0)
                    rolls = [game.first_dice, game.second_dice, game.third_dice, game.fourth_dice]
                    _bar, position_home = self.action(board, rolls, game.player)
                    self.update(board, game.player)
                    game_copy = game.add_in_house(position_home-1)
                # update map
                if game_copy is not None:
                    game = game_copy
                elif game_copy is None and game.player == 1:
                    print("table: ", game.table)
                    print("ROBOTUL nu are mutari valide")
                    break
                else:
                    print("table: ", game.table)
                    print("Calculatorul a dat o mutare gresita")
                    break
            while game.can_move():
                print("[3]move")
                if game.player:
                    board = Board(game.table,
                                  game.out_pieces_1, game.out_pieces_0,
                                  game.end_pieces_1, game.out_pieces_0)
                    print("[table]: {}".format(game.table))
                    rolls = [game.first_dice, game.second_dice, game.third_dice, game.fourth_dice]
                    position_start, dice_used = self.action(board, rolls, game.player)
                    self.update(board, game.player)
                    print("zaruri [robot]: ", game.first_dice, game.second_dice, game.third_dice, game.fourth_dice)
                    print("[POSITIONS]: ", position_start, position_start+dice_used)
                    new_state = game.move(position_start, position_start + dice_used)
                else:
                    position_start, position_end = game.return_positions_for_movement(0)
                    new_state = game.move(position_start, position_end)
                if new_state is not None:
                    game = new_state
                else:
                    print("[NONE] new state")
                    print("[table]: {}".format(game.table))
                    print("[start_end] {} {} ;  table[start]: {}, table[end]: {}".format(position_start, position_end, game.table[position_start], game.table[position_start+dice_used]))
                    break
            print("[4]done move")
            # turn is over and switch the player
            game.switch_player()
            turns += 1
            if game.end_pieces_0 == 15 or game.end_pieces_1 == 15:
                break
        # check who won, if someone won
        someone_won = game.won()
        return turns, someone_won
