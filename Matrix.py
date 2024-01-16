class PayoffMatrix:
    """
    R (Reward): The payoff received when both players cooperate.
    S (Sucker's Payoff): The payoff received when the player cooperates, but the opponent defects.
    T (Temptation): The payoff received when the player defects, and the opponent cooperates.
    P (Punishment): The payoff received when both players defect.

                | Cooperate | Defect
    ------------|-----------|--------
    Cooperate   |    R, R   |  S, T
    ------------|-----------|--------
    Defect      |    T, S   |  P, P

    """
    @staticmethod
    def calculate_payoff(player_action, opponent_action):
        # Define the payoff matrix
        payoff_matrix = {
            ("Cooperate", "Cooperate"): 'R',
            ("Cooperate", "Defect"): 'S',
            ("Defect", "Cooperate"): 'T',
            ("Defect", "Defect"): 'P'
        }

        # Retrieve the payoff for the given actions
        return payoff_matrix.get((player_action, opponent_action))

