import random
import numpy as np
from scipy import stats


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

