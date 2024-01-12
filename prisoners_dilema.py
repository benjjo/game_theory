import random
from Strategies import *


class Tournament:
    """Runs a tournament of X amount of games, where the strategies are played against each other in a round-robin
    type of tournament. Scores are then printed to the screen.
    Noise can be introduced by setting the noise parameter to True."""
    def __init__(self, strategy_classes, num_games_per_match=200, noise=True):
        self.strategy_classes = strategy_classes
        self.num_games_per_match = num_games_per_match
        self.scores = {strategy_class.__name__: 0 for strategy_class in strategy_classes}
        self.noise = noise

    def run_tournament(self):
        noise = self.noise
        for i, strategy1 in enumerate(self.strategy_classes):
            for j, strategy2 in enumerate(self.strategy_classes):
                # if i != j:  # Avoid playing a strategy against itself
                player1 = strategy1()
                player2 = strategy2()
                # Change the noise assignment to True to introduce noise
                game_runner = GameRunner(player1, player2, self.num_games_per_match, noise)
                player1, player1_score, player2, player2_score = game_runner.run_game()

                self.scores[player1.name] += player1_score
                self.scores[player2.name] += player2_score
        return self.scores


class GameRunner:
    """Runs two strategies against each other for a set number of games. Presents the scores at the end in text.
    Returns the two strategy names and their respective scores.
    Points are awarded as follows:
        A score of 3-3 is awarded to Cooperate - Cooperate outcome.
        A score of 5-0 is awarded to a Defect - Cooperate outcome in favour of the Defective party.
        A score of 1-1 is awarded to a Defect - Defect outcome.
    :returns: str (name of strategy 1), int (strategy 1 score), str (name of strategy 2), int (strategy 2 score)
    """
    def __init__(self, player1, player2, num_games, noise):
        self.player1 = player1
        self.player2 = player2
        self.num_games = num_games
        self.noise = noise

    def run_game(self):
        player1_score = 0
        player2_score = 0

        for _ in range(self.num_games):
            choice1 = self.player1.get_choice()
            choice2 = self.player2.get_choice()

            if self.noise:
                # If noise is set to True, this will introduce a 1% chance of the choice being flipped.
                choice1 = self.generate_choice_noise(choice1)
                choice2 = self.generate_choice_noise(choice2)

            if choice1 == "Cooperate" and choice2 == "Cooperate":
                player1_score += 3
                player2_score += 3
            elif choice1 == "Defect" and choice2 == "Cooperate":
                player1_score += 5
            elif choice1 == "Cooperate" and choice2 == "Defect":
                player2_score += 5
            elif choice1 == "Defect" and choice2 == "Defect":
                player1_score += 1
                player2_score += 1

            # Update the strategies with the opponent's previous choice
            self.player1.make_choice(choice2)
            self.player2.make_choice(choice1)
            # print(f"{self.player1.name:<20} :: {choice1:<20} {self.player2.name:<20} :: {choice2:<10}")

        print(f"{self.player1.name} vs {self.player2.name} :: {player1_score} : {player2_score} ")

        return self.player1, player1_score, self.player2, player2_score

    def generate_choice_noise(self, choice):
        # 1% chance the choice will be flipped. This will only be invoked if noise is set to True.
        if random.randint(1, 100) == 1:
            if choice == "Defect":
                return "Cooperate"
            else:
                return "Defect"
        return choice


# Example usage:
strategies = [TitForTat, AlwaysDefect, GenerousTitForTat,
              AlwaysCooperate, Friedman, Joss, Graaskamp, Nydegger,
              TitForTwoTats, Random]  # Add more strategies as needed
games = random.randint(200, 1000)
tournament = Tournament(strategies, num_games_per_match=games, noise=True)  # Mess with the parameters if you want.
overall_scores = tournament.run_tournament()

sorted_scores = sorted(overall_scores.items(), key=lambda x: x[1], reverse=True)
print("")
print('*'*44)
print(" Overall Scores, sorted by highest ranking:")
print('*'*44)
print(f"Number of games: {games}\n")
for strategy, score in sorted_scores:
    print(f"{strategy}: {score}")
print('*'*44)

