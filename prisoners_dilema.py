from Strategies import *
C = "Cooperate"
D = "Defect"


class Tournament:
    """Runs a tournament of X amount of games, where the strategies are played against each other in a round-robin
    type of tournament. Scores are then printed to the screen.
    Noise can be introduced by setting the noise parameter to True."""
    def __init__(self, strategy_classes, num_games_per_match=200, noise=False):
        self.strategy_classes = strategy_classes
        self.num_games_per_match = num_games_per_match
        self.scores = {strategy_class.__name__: 0 for strategy_class in strategy_classes}
        self.noise = noise

    def run_tournament(self):
        """
        A fresh object is instantiated for each round.
        :return: dict
        """
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
        self.historical_data = list()
        self.player_choice = str()
        self.opponent_choice = str()

    def run_game(self):
        player1_score = 0
        player2_score = 0

        for i in range(self.num_games):
            player1_choice = self.player1.choice
            player2_choice = self.player2.choice

            if self.noise:
                # If noise is set to True, this will introduce a 1% chance of the choice being flipped.
                player1_choice = GameRunner.generate_choice_noise(player1_choice)
                player2_choice = GameRunner.generate_choice_noise(player2_choice)

            # Update the rolling score using the scoring matrix.
            player1_score += Tools.calculate_payoff(player1_choice, player2_choice)
            player2_score += Tools.calculate_payoff(player2_choice, player1_choice)

            # Update the historical data after the choices have been made
            self.player1.history_data(opp_choice=player2_choice, own_choice=player1_choice)
            self.player2.history_data(opp_choice=player1_choice, own_choice=player2_choice)

            # Run the strategies to set the next decision
            self.player1.strategy(player2_choice)
            self.player2.strategy(player1_choice)

        print(f"{self.player1.name:>20} vs {self.player2.name:<20} {player1_score:>20} : {player2_score} ")
        return self.player1, player1_score, self.player2, player2_score

    def historic_manager(self, player, opponent):
        self.player_choice = player
        self.opponent_choice = opponent

    @staticmethod
    def generate_choice_noise(choice):
        # 1% chance the choice will be flipped. This will only be invoked if noise is set to True.
        if random.randint(1, 100) == 1:
            if choice == D:
                return C
            else:
                return D
        return choice


# Example usage:

# No random elements # Add more strategies as needed
strategies = [TitForTat, AlwaysDefect, GenerousTitForTat, ModalTFT, AlwaysCooperate, Friedman, Graaskamp,
              Nydegger, DefectOnce, TitForTwoTats, WinStayLooseShift, Benjo, Shubik, Downing]


# Introduced random elements
# strategies = [TitForTat, AlwaysDefect, GenerousTitForTat, Joss, TidemanChieruzzi, Random,
#              AlwaysCooperate, Friedman, Graaskamp, Nydegger, DefectOnce, Downing,
#              TitForTwoTats, WinStayLooseShift, Benjo, Shubik, ModalTFT]  # Add more strategies as needed

# strategies = [TitForTat, AlwaysDefect, GenerousTitForTat, Joss, Random,
#              AlwaysCooperate, DefectOnce, TitForTwoTats, ModalTFT]  # Add more strategies as needed
# games = random.randint(200, 1000)
games = 2000

# Testing games
# strategies = [Random, ModalTFT]

tournament = Tournament(strategies, num_games_per_match=games, noise=True)  # Mess with the parameters if you want.
overall_scores = tournament.run_tournament()

sorted_scores = sorted(overall_scores.items(), key=lambda x: x[1], reverse=True)
print("")
print('*'*44)
print(" Overall Scores, sorted by highest ranking:")
print('*'*44)
print(f"Number of games: {games}\n")
for strategy, score in sorted_scores:
    print(f"{strategy:>20}: {score}")
print('*'*44)

