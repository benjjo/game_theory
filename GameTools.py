import random
import numpy as np
import statistics

C = "Cooperate"
D = "Defect"


class Tools:

    @staticmethod
    def calculate_payoff(player_action, opponent_action):
        """
        Scoring matrix.
        :param player_action:
        :param opponent_action:
        :return int():
        """
        score_matrix = {
            ("Cooperate", "Cooperate"): 3,
            ("Cooperate", "Defect"):    0,
            ("Defect", "Cooperate"):    5,
            ("Defect", "Defect"):       1
        }
        # Retrieve the payoff for the given actions
        return score_matrix.get((player_action, opponent_action))

    @staticmethod
    def get_payoff_type(player_action, opponent_action):
        """
        R (Reward): The payoff received when both players cooperate.
        S (Sucker's Payoff): The payoff received when the player cooperates, but the opponent defects.
        T (Temptation): The payoff received when the player defects, and the opponent cooperates.
        P (Punishment): The payoff received when both players defect.
        :param player_action:
        :param opponent_action:
        :return str():
        """
        payoff_matrix = {
            ("Cooperate", "Cooperate"): 'R',
            ("Cooperate", "Defect"):    'S',
            ("Defect", "Cooperate"):    'T',
            ("Defect", "Defect"):       'P'
        }
        # Retrieve the payoff for the given actions
        return payoff_matrix.get((player_action, opponent_action))

    @staticmethod
    def random_5050_sample(sample_size, cooperation_probability):
        choices = ["Cooperate", "Defect"]
        probabilities = [cooperation_probability, 1 - cooperation_probability]
        random_sample = random.choices(choices, probabilities, k=sample_size)
        return random_sample

    @staticmethod
    def compare_samples(sample1, sample2):
        # Convert "Cooperate" to 1 and "Defect" to 0 for easier calculations
        sample1_numeric = np.array([1 if choice == "Cooperate" else 0 for choice in sample1])
        sample2_numeric = np.array([1 if choice == "Cooperate" else 0 for choice in sample2])

        # Calculate proportions
        proportion1 = np.mean(sample1_numeric)
        proportion2 = np.mean(sample2_numeric)

        # Calculate z-score
        z_score = (proportion1 - proportion2) / np.sqrt((proportion1 * (1 - proportion1) / len(sample1)) +
                                                        (proportion2 * (1 - proportion2) / len(sample2)))

        # Check if the absolute z-score is greater than 3 (indicating a significant difference)
        return abs(z_score) > 3

    @staticmethod
    def history_manager(obj1, obj2, obj1_choice, obj2_choice):
        obj1.history_data(own_choice=obj1_choice, opponent_choice=obj2_choice)
        obj2.history_data(own_choice=obj2_choice, opponent_choice=obj1_choice)

    @staticmethod
    def generate_choice_noise(choice, chance=100):
        # 1% chance the choice will be flipped. This will only be invoked if noise is set to True.
        if random.randint(1, chance) == 1:
            return C if choice == D else D
        return choice

    @staticmethod
    def object_spawner(strategy_classes):
        strategy_objects = list()
        for strategy_class in strategy_classes:
            strategy = strategy_class()
            strategy_objects.append(strategy)
        return strategy_objects


class GameRunner:
    """Runs two strategies against each other for a set number of games. Presents the scores at the end in text.
    Returns the two strategy names and their respective scores.
    Points are awarded as follows:
        A score of 3-3 is awarded to Cooperate - Cooperate outcome.
        A score of 5-0 is awarded to a Defect - Cooperate outcome in favour of the Defective party.
        A score of 1-1 is awarded to a Defect - Defect outcome.
    :returns: str (name of strategy 1), int (strategy 1 score), str (name of strategy 2), int (strategy 2 score)
    """
    def __init__(self, num_games, noise):
        self.num_games = num_games
        self.noise = noise

    def run_game(self, player1, player2):
        player1_score = 0
        player2_score = 0

        for _ in range(self.num_games):
            # Strategies are instantiated with a choice already made.
            p1_choice = player1.choice
            p2_choice = player2.choice

            if self.noise:
                # If noise is set to True, this will introduce a 1% chance of the choice being flipped.
                p1_choice = GameRunner.generate_choice_noise(p1_choice)
                p2_choice = GameRunner.generate_choice_noise(p2_choice)

            # Update the rolling score using the scoring matrix.
            player1_score += Tools.calculate_payoff(p1_choice, p2_choice)
            player2_score += Tools.calculate_payoff(p2_choice, p1_choice)

            # Update the historical data after the choices have been scored
            player1.history_data(opponent_choice=p2_choice, own_choice=p1_choice)
            player2.history_data(opponent_choice=p1_choice, own_choice=p2_choice)

            # Run the strategies to set the next decision
            player1.strategy()
            player2.strategy()

        print(f"{player1.name:>20} vs {player2.name:<20} {player1_score:>20} : {player2_score} ")
        return player1, player1_score, player2, player2_score

    @staticmethod
    def generate_choice_noise(choice):
        # 1% chance the choice will be flipped. This will only be invoked if noise is set to True.
        if random.randint(1, 100) == 1:
            return C if choice == D else D
        return choice


class Tournament:
    """Utilising the GameRunner class, runs a tournament of X amount of games, where the strategies are played
    against each other in a round-robin type of tournament. Scores are then printed to the screen.
    Noise can be introduced by setting the noise parameter to True."""
    def __init__(self, strategy_classes, num_games_per_match=200, noise=False):
        self.strategy_classes = strategy_classes
        self.num_games_per_match = num_games_per_match
        self.scores = {strategy_class.__name__: 0 for strategy_class in self.strategy_classes}
        self.noise = noise

    def run_tournament(self):
        """
        A fresh object is instantiated for each round. All strategies against all strategies.
        i.e. [p1, p2] will play games in the following fashion:
            p1 vs p1
            p1 vs p2
            p2 vs p1
            p2 vs p2
            This means that a strategy playing itself will play itself 4 times.
        :return: dict
        """
        for i, strategy1 in enumerate(self.strategy_classes):
            for j, strategy2 in enumerate(self.strategy_classes):
                # if i != j:  # Avoid playing a strategy against itself
                player1 = strategy1()
                player2 = strategy2()
                # Change the noise assignment to True to introduce noise
                game_runner = GameRunner(self.num_games_per_match, self.noise)
                player1, player1_score, player2, player2_score = game_runner.run_game(player1, player2)

                # Halve the score for a strategy playing itself otherwise it will update the same score key twice.
                if player1.name == player2.name:
                    score = statistics.mean([player1_score, player1_score])
                    self.scores[player1.name] += score
                else:
                    # Update the scores for differing opponents
                    self.scores[player1.name] += player1_score
                    self.scores[player2.name] += player2_score

        return self.scores

    def round_robin(self):
        """
        A Round-Robin tournament between each of the strategies. Each strategy will play itself and another strategy
        once. i.e. [p1, p2] will play games in the following fashion:
            p1 vs p1
            p1 vs p2
            p2 vs p2
        :return: dict
        """
        strategy_objs = Tools.object_spawner(self.strategy_classes)

        for player1 in strategy_objs:
            for player2 in strategy_objs:
                # Change the noise assignment to True to introduce noise
                game_runner = GameRunner(self.num_games_per_match, self.noise)
                player1, player1_score, player2, player2_score = game_runner.run_game(player1, player2)

                # Halve the score for a strategy playing itself otherwise it will update the same score key twice.
                if player1.name == player2.name:
                    score = statistics.mean([player1_score, player1_score])
                    self.scores[player1.name] += score
                else:
                    # Update the scores for differing opponents
                    self.scores[player1.name] += player1_score
                    self.scores[player2.name] += player2_score
            strategy_objs = strategy_objs[1:]

        return self.scores
