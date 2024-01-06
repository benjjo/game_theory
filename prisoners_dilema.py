import random
from Strategies import *


class Tournament:
    def __init__(self, strategy_classes, num_games_per_match=10):
        self.strategy_classes = strategy_classes
        self.num_games_per_match = num_games_per_match
        self.scores = {strategy_class.__name__: 0 for strategy_class in strategy_classes}

    def run_tournament(self):
        for i, strategy1 in enumerate(self.strategy_classes):
            for j, strategy2 in enumerate(self.strategy_classes):
                # if i != j:  # Avoid playing a strategy against itself
                player1 = strategy1()
                player2 = strategy2()
                game_runner = GameRunner(player1, player2, self.num_games_per_match)
                player1, player1_score, player2, player2_score = game_runner.run_game()

                self.scores[player1.name] += player1_score
                self.scores[player2.name] += player2_score

        return self.scores


class GameRunner:
    """Runs two strategies against each other for a set number of games. Presents the scores at the end in text.
    Returns the two strategy names and their respective scores.
    :returns: str (name of strategy 1), int (strategy 1 score), str (name of strategy 2), int (strategy 2 score)
    """
    def __init__(self, player1, player2, num_games):
        self.player1 = player1
        self.player2 = player2
        self.num_games = num_games

    def run_game(self):
        player1_score = 0
        player2_score = 0

        for _ in range(self.num_games):
            # The 1% chance that noise is introduced
            if random.randint(1, 50) != 1:
                choice1 = self.player1.get_choice()
                choice2 = self.player2.get_choice()
            else:
                choice1 = self.generate_choice_noise()
                choice2 = self.generate_choice_noise()

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
            print(f"{self.player1.name} = {choice1}\t\t\t\t {self.player2.name} = {choice2}")

        print(f"{self.player1.name}'s score: {player1_score}")
        print(f"{self.player2.name}'s score: {player2_score}")

        return self.player1, player1_score, self.player2, player2_score

    def generate_choice_noise(self):
        # The choice is random with 90% in favor of Cooperation.
        choices = ['Cooperate', 'Defect']
        probabilities = [0.9, 0.1]

        # Generate a random choice based on the specified probabilities
        random_choice = random.choices(choices, probabilities)[0]

        return random_choice


# Example usage:
strategies = [TitForTat, AlwaysDefect, SoftTitForTat, AlwaysCooperate, Friedman]  # Add more strategies as needed
tournament = Tournament(strategies, num_games_per_match=200)
overall_scores = tournament.run_tournament()

sorted_scores = sorted(overall_scores.items(), key=lambda x: x[1], reverse=True)

print("Overall Scores:")
for strategy, score in sorted_scores:
    print(f"{strategy}: {score}")

