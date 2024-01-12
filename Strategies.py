import random

""" 
Strategies to be added:
Tideman & Chieruzzi, Nydegger, Grofman, Shubik, Stein & Rapoport, Davis, Downing, Feld, Tullock, (Name Withheld), 
Random"""


class Strategy:
    def __init__(self, name, init_choice):
        self.name = name
        self.choice = init_choice

    def set_choice(self, choice):
        """The choice parameter is set by the run_game method within the GameRunner class. This is the previous choice
        set by the opponent."""
        self.choice = choice
        raise NotImplementedError("Subclasses must implement the set_choice method")

    def get_choice(self):
        raise NotImplementedError("Subclasses must implement the get_choice method")

    def make_choice(self, opp_choice):
        raise NotImplementedError("Subclasses must implement the make_choice method")

    def update_opponent_choice(self, choice):
        pass


class TitForTat(Strategy):
    """The strategy of do unto thee what was done unto me. Not really an eye-for-an because it is not vengeance
     that is sought, but more that this strategy is not a push-over.
     A 'NICE' strategy in that we start peacefully until provoked."""

    def __init__(self):
        super().__init__("TitForTat", "Cooperate")

    def get_choice(self):
        return self.choice

    def set_choice(self, new_choice):
        self.choice = new_choice

    def make_choice(self, opp_choice):
        self.set_choice(opp_choice)


class AlwaysDefect(Strategy):
    """The strategy of the logical. This strategy is not a push-over and never will be. It is also unforgiving.
    The logical strategy concludes that the opponent will also choose to Defect. This is because of the risk
    involved with the selection of the cooperative choice. While not the most optimal, it will guarantee points.
    A 'NOT NICE' strategy in that we start and end with provocation."""

    def __init__(self):
        super().__init__("AlwaysDefect", "Defect")

    def get_choice(self):
        return "Defect"

    def set_choice(self, choice):
        pass

    def make_choice(self, opp_choice):
        pass


class AlwaysCooperate(Strategy):
    """The strategy of do only kindness unto all.This strategy is a push-over but has the potential to score the
    highest.
     A 'NICE' strategy in that we start and end peacefully."""

    def __init__(self):
        super().__init__("AlwaysCooperate", "Cooperate")

    def get_choice(self):
        return "Cooperate"

    def set_choice(self, choice):
        pass

    def make_choice(self, opp_choice):
        pass


class SoftTitForTat(Strategy):
    """The strategy of do unto thee what was done unto me but let's not get ourselves tied up in a circular argument
    for all eternity. This strategy is not a push-over.
    A 'NICE' strategy in that we start peacefully until provoked but if we continue in a cycle of punishment, it will
    sacrifice a move for the greater good."""

    def __init__(self):
        super().__init__("SoftTitForTat", "Cooperate")
        self.historic_choices = list()

    def get_choice(self):
        return self.choice

    def set_choice(self, new_choice):
        self.update_opp_choice(new_choice)
        self.choice = new_choice

    def update_opp_choice(self, recent_choice):
        self.historic_choices.append(recent_choice)

    def make_choice(self, opp_choice):
        if self.historic_choices[-10:].count('Defect') >= 10:
            self.set_choice("Cooperate")
        elif opp_choice == "Cooperate":
            self.set_choice("Cooperate")
        else:
            self.set_choice("Defect")


class Friedman(Strategy):
    """The strategy of do nice unto others until betrayed. This strategy is not a push-over.
     A 'NICE' strategy in that we start peacefully until provoked. Once provoked it is unforgiving"""

    def __init__(self):
        super().__init__("Friedman", "Cooperate")
        self.historic_opponent_choices = list()

    def get_choice(self):
        return self.choice

    def set_choice(self, new_choice):
        self.choice = new_choice

    def make_choice(self, opp_choice):
        self.historic_opponent_choices.append(opp_choice)
        if 'Defect' in self.historic_opponent_choices:
            self.set_choice("Defect")
        elif opp_choice == "Cooperate":
            self.set_choice("Cooperate")
        else:
            self.set_choice("Defect")


class Joss(Strategy):
    """Similar to Tit-For-tat in that it will start out as Cooperative, but will always mimic the opponent from that
    point onward. However, as a sneaky little side hustle, Joss will Defect around 10% of the time."""

    def __init__(self):
        super().__init__("Joss", "Cooperate")

    def get_choice(self):
        return self.choice

    def set_choice(self, new_choice):
        self.choice = new_choice

    def make_choice(self, opp_choice):
        if random.randint(1, 10) == 1:
            self.set_choice("Defect")
        else:
            self.set_choice(opp_choice)


class Graaskamp(Strategy):
    """Similar to Joss in that it will start out as Cooperative, but will always mimic the opponent from that
    point onward. However, Graaskamp will defect every 50th round."""

    def __init__(self):
        super().__init__("Graaskamp", "Cooperate")
        self.round = int()

    def get_choice(self):
        return self.choice

    def set_choice(self, new_choice):
        self.choice = new_choice

    def make_choice(self, opp_choice):
        self.round += 1
        if self.round % 50 == 0:
            self.set_choice("Defect")
        else:
            self.set_choice(opp_choice)


class TidemanChieruzzi(Strategy):
    """
    This strategy begins by playing Tit For Tat and then things get slightly complicated:
    Every run of defections played by the opponent increases the number of defections that this strategy
    retaliates with by 1. The opponent is given a ‘fresh start’ if:
    - it is 10 points behind this strategy
    - and it has not just started a run of defections
    - and it has been at least 20 rounds since the last ‘fresh start’
    - and there are more than 10 rounds remaining in the tournament
    - and the total number of defections differs from a 50-50 random sample by at least 3.0 standard deviations.
    A ‘fresh start’ is a sequence of two cooperations followed by an assumption that the game has just
    started (everything is forgotten).
    See https://github.com/Axelrod-Python/Axelrod/issues/1105

    WIP - 2024-Jan-13
    """

    def __init__(self):
        super().__init__("TidemanChieruzzi", "Cooperate")
        self.history = []
        self.defection_runs = 0
        self.opponent_defection_runs = 0
        self.last_fresh_start_round = 0
        self.cooperation_count = 0
        self.total_rounds = 0

    def get_choice(self):
        return self.choice

    def set_choice(self, new_choice):
        self.choice = new_choice

    def make_choice(self, opp_choice, opponent_score=None, own_score=None):
        if not self.history:
            # Start with Tit For Tat
            return "Cooperate"

        if self.should_start_fresh(opponent_score):
            self.start_fresh()
            return "Cooperate"

        # Retaliate with increasing defections based on opponent's recent defections
        retaliation_count = min(self.defection_runs, 5)
        return "Defect" if self.opponent_defection_runs >= retaliation_count else "Cooperate"

    def update_opponent_choice(self, choice):
        super().update_opponent_choice(choice)
        self.history.append(choice)

    def should_start_fresh(self, opponent_score):
        return (
            opponent_score is not None
            and opponent_score + 10 <= self.get_own_score()
            and self.opponent_defection_runs > 0
            and self.total_rounds - self.last_fresh_start_round >= 20
            and self.total_rounds <= 190  # Assuming there are more than 10 rounds remaining
            and self.defection_difference_significant()
        )

    def start_fresh(self):
        # Start a fresh sequence
        self.history.extend(["Cooperate", "Cooperate"])
        self.opponent_defection_runs = 0
        self.defection_runs = 0
        self.last_fresh_start_round = self.total_rounds
        self.cooperation_count = 0

    def defection_difference_significant(self):
        # Check if the total defections differ from a 50-50 random sample by at least 3.0 standard deviations
        total_defections = self.history.count("Defect")
        expected_defections = len(self.history) / 2  # Assuming 50-50 random sample
        deviation = abs(total_defections - expected_defections) / (len(self.history) / 2)
        return deviation >= 3.0

    def get_own_score(self):
        # Calculate the current own score based on the history
        # return sum([3 if self.get_choice() == "Cooperate" else 5 for self.get_choice() in self.history])
        pass


class Nydegger(Strategy):
    """
        The Nydegger strategy is based on the following rules:

        The Nydegger strategy cooperates on the first round.
        After the first round, it analyzes the opponent's last five moves.
        If the opponent has defected in three or more of the last five moves, Nydegger will defect.
        Otherwise, it will cooperate."""

    def __init__(self):
        super().__init__("Nydegger", "Cooperate")
        self.history = list()

    def get_choice(self):
        return self.choice

    def set_choice(self, new_choice):
        self.choice = new_choice

    def make_choice(self, opp_choice):
        self.history.append(opp_choice)
        if self.history[-5:].count("Defect") >= 3:
            self.set_choice("Defect")
        else:
            self.set_choice("Cooperate")


