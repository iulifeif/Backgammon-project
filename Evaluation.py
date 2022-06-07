class Evaluation:

    def __init__(self):
        self.winner = []
        self.game_turns = []

    def add_game_data(self, game_turns, winner):
        self.winner.append(winner)
        self.game_turns.append(game_turns)

    def get_average_turns(self):
        total_turns = 0
        for result in range(len(self.game_turns)):
            total_turns += result
        return total_turns/len(self.game_turns)

    def number_wins(self, player):
        count = 0
        for index in range(len(self.winner)):
            if self.winner[index] == player:
                count += 1
        return count

    def evaluate(self):
        print("Number of times BLACK won:", self.number_wins(1))
        print("Number of times WHITE won:", self.number_wins(0))
        print(self.game_turns)
        print("Average number of turns: ", self.get_average_turns())
