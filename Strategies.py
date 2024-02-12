import random
from GameTools import Tools
import statistics


class Strategy:
    def __init__(self, name, init_choice):
        self.name = name
        self._choice = init_choice
        self.opp_history = list()

    @property
    def choice(self):
        raise NotImplementedError("Subclasses must implement the set_choice method")

    @choice.setter
    def choice(self, value):
        """The choice parameter is set by the run_game method within the GameRunner class. This is the previous choice
        set by the opponent."""
        self._choice = value
        raise NotImplementedError("Subclasses must implement the set_choice method")

    def strategy(self, opp_choice):
        raise NotImplementedError("Subclasses must implement the make_choice method")


class TitForTat(Strategy):
    """The strategy of do unto thee what was done unto me. Not really an eye-for-an because it is not vengeance
     that is sought, but more that this strategy is not a push-over.
     A 'NICE' strategy in that we start peacefully until provoked."""

    def __init__(self):
        super().__init__("TitForTat", "Cooperate")

    @property
    def choice(self):
        return self._choice

    @choice.setter
    def choice(self, new_choice):
        self._choice = new_choice

    def strategy(self, opp_choice):
        self.choice = opp_choice


class AlwaysDefect(Strategy):
    """The strategy of the logical. This strategy is not a push-over and never will be. It is also unforgiving.
    The logical strategy concludes that the opponent will also choose to Defect. This is because of the risk
    involved with the selection of the cooperative choice. While not the most optimal, it will guarantee points.
    A 'NOT NICE' strategy in that we start and end with provocation."""

    def __init__(self):
        super().__init__("AlwaysDefect", "Defect")

    @property
    def choice(self):
        return self._choice

    @choice.setter
    def choice(self, new_choice):
        self._choice = new_choice

    def strategy(self, opp_choice):
        self.choice = "Defect"


class AlwaysCooperate(Strategy):
    """The strategy of do only kindness unto all.This strategy is a push-over but has the potential to score the
    highest.
     A 'NICE' strategy in that we start and end peacefully."""

    def __init__(self):
        super().__init__("AlwaysCooperate", "Cooperate")

    @property
    def choice(self):
        return self._choice

    @choice.setter
    def choice(self, new_choice):
        self._choice = new_choice

    def strategy(self, opp_choice):
        self.choice = "Cooperate"


class GenerousTitForTat(Strategy):
    """The strategy of do unto thee what was done unto me but let's not get ourselves tied up in a circular argument
    for all eternity. This strategy is not a push-over.
    A 'NICE' strategy in that we start peacefully until provoked but if we continue in a cycle of punishment, it will
    sacrifice a move for the greater good."""

    def __init__(self):
        super().__init__("GenerousTitForTat", "Cooperate")
        self.historic_choices = list()

    @property
    def choice(self):
        return self._choice

    @choice.setter
    def choice(self, new_choice):
        self.historic_choices.append(new_choice)
        self._choice = new_choice

    def strategy(self, opp_choice):
        if self.historic_choices[-10:].count('Defect') >= 10:
            self.choice = "Cooperate"
        else:
            self.choice = opp_choice


class Friedman(Strategy):
    """The strategy of do nice unto others until betrayed. This strategy is not a push-over.
     A 'NICE' strategy in that we start peacefully until provoked. Once provoked it is unforgiving"""

    def __init__(self):
        super().__init__("Friedman", "Cooperate")

    @property
    def choice(self):
        return self._choice

    @choice.setter
    def choice(self, new_choice):
        self._choice = new_choice

    def strategy(self, opp_choice):
        if 'Defect' in self.opp_history:
            self.choice = "Defect"
        else:
            self.choice = "Cooperate"


class Joss(Strategy):
    """Similar to Tit-For-tat in that it will start out as Cooperative and will mimic the opponent.
    However, as a sneaky little side hustle, Joss will Defect around 10% of the time."""

    def __init__(self):
        super().__init__("Joss", "Cooperate")

    @property
    def choice(self):
        return self._choice

    @choice.setter
    def choice(self, new_choice):
        self._choice = new_choice

    def strategy(self, opp_choice):
        if random.randint(1, 10) == 1:
            self.choice = "Defect"
        else:
            self.choice = opp_choice


class Graaskamp(Strategy):
    """Similar to Joss in that it will start out as Cooperative and mimic the opponent.
    However, Graaskamp will defect every 50th round."""

    def __init__(self):
        super().__init__("Graaskamp", "Cooperate")
        self.round = int()

    @property
    def choice(self):
        return self._choice

    @choice.setter
    def choice(self, new_choice):
        self._choice = new_choice

    def strategy(self, opp_choice):
        self.round += 1
        if self.round % 50 == 0:
            self.choice = "Defect"
        else:
            self.choice = opp_choice


class TidemanChieruzzi(Strategy):
    """
    Tideman & Chieruzzi strategy
    This strategy begins by playing Tit For Tat and then things get slightly complicated:
    Every run of defections played by the opponent increases the number of defections that this strategy
    retaliates with by 1.
    A ‘fresh start’ is a sequence of two co-operations followed by an assumption that the game has just
    started (everything is forgotten).
    See https://github.com/Axelrod-Python/Axelrod/issues/1105
    """

    def __init__(self):
        super().__init__("TidemanChieruzzi", "Cooperate")
        self.retaliation_counter = 0
        self.retaliations = 0
        self.fresh_start = bool()
        self.fresh_start_counter = 0
        self.my_points = 0
        self.their_points = 0
        self.own_history = list()
        self.games_counter = 0

    @property
    def choice(self):
        return self._choice

    @choice.setter
    def choice(self, new_choice):
        self._choice = new_choice

    def set_fresh_start_condition(self, my_choice, opp_choice):
        """The opponent is given a ‘fresh start’ if:
            - it is 10 points behind this strategy
            - and it has not just started a run of defections
            - and it has been at least 20 rounds since the last ‘fresh start’
            - and there are more than 10 rounds remaining in the tournament
            - and the total number of defections differs from a 50-50 random sample by at least 3.0 standard deviations.
            """
        self.fresh_start_counter += 1
        self.games_counter += 1
        self.my_points += Tools.calculate_payoff(my_choice, opp_choice)
        self.their_points += Tools.calculate_payoff(opp_choice, my_choice)

        return (
                self.my_points - self.their_points >= 10
                and self.own_history[-2:].count("Defect") == 2
                and self.fresh_start_counter > 20
                and self.games_counter < 190
                and Tools.compare_samples(Tools.random_5050_sample(self.games_counter, 0.7), self.own_history))

    def strategy(self, opp_choice):
        self.own_history.append(opp_choice)
        self.set_fresh_start_condition(self.choice, opp_choice)

        if opp_choice == "Defect":
            self.retaliations += 1
            self.retaliation_counter = self.retaliations  # start the retaliations counter again
        else:
            if self.retaliation_counter > 0:
                self.retaliation_counter -= 1

        if self.fresh_start:
            self.retaliation_counter = 0

        self.choice = ("Defect" if self.retaliation_counter else "Cooperate")


class Nydegger(Strategy):
    """
        The Nydegger strategy is based on the following rules:

        The Nydegger strategy cooperates on the first round.
        After the first round, it analyzes the opponent's last five moves.
        If the opponent has defected in three or more of the last five moves, Nydegger will defect.
        Otherwise, it will cooperate."""

    def __init__(self):
        super().__init__("Nydegger", "Cooperate")

    @property
    def choice(self):
        return self._choice

    @choice.setter
    def choice(self, new_choice):
        self._choice = new_choice

    def strategy(self, opp_choice):
        self.opp_history.append(opp_choice)
        self.choice = statistics.mode(self.opp_history[-5:])


class TitForTwoTats(Strategy):
    """
        The TitForTwoTats strategy is based on the following rules:

        The Sample strategy cooperates on the first round.
        After the first round, it analyzes the opponent's last two moves.
        If the opponent has defected both times, Sample will defect.
        Otherwise, it will cooperate."""

    def __init__(self):
        super().__init__("TitForTwoTats", "Cooperate")

    @property
    def choice(self):
        return self._choice

    @choice.setter
    def choice(self, new_choice):
        self._choice = new_choice

    def strategy(self, opp_choice):
        self.opp_history.append(opp_choice)
        if self.opp_history[-2:].count("Defect") == 2:
            self.choice = "Defect"
        else:
            self.choice = "Cooperate"


class Random(Strategy):
    """Straight up random"""

    def __init__(self):
        super().__init__("Random", "Cooperate")

    @property
    def choice(self):
        return self._choice

    @choice.setter
    def choice(self, new_choice):
        self._choice = new_choice

    def strategy(self, opp_choice):
        self.choice = random.choice(["Defect", "Cooperate"])


class Grofman(Strategy):
    """The Grofman strategy is a probabilistic strategy designed for the iterated prisoner's dilemma (IPD) game.
    It was introduced by Bernard Grofman in the early 1980s. The Grofman strategy is based on probabilistic
    decision-making, aiming to strike a balance between cooperation and defection

    Probabilistic Decision-Making:
    The core of the Grofman strategy involves probabilistic decision-making. Instead of strictly choosing to cooperate
    or defect, the strategy assigns probabilities to each action.

    Randomized Choices:
    In each round of the game, the Grofman strategy randomly chooses between cooperation and defection based on the
    assigned probabilities.

    Adaptive Probabilities:
    The strategy adapts its probabilities based on the outcomes of previous rounds. If cooperation leads to favorable
    outcomes, the probability of cooperating in the next round may increase. Conversely, if defection results in better
    outcomes, the probability of defecting may increase.

    Learning from Opponent's Behavior:
    The Grofman strategy may adjust its probabilities based on the opponent's behavior. For example, if the opponent
    tends to defect frequently, the Grofman strategy may increase the probability of defection in response.

    Exploration and Exploitation:
    The strategy aims to balance exploration and exploitation. It explores different actions by assigning non-zero
    probabilities to both cooperation and defection. Over time, it exploits the actions that lead to higher payoffs.

    Stochastic Behavior:
    The Grofman strategy's stochastic (randomized) behavior adds an element of unpredictability, making it challenging
    for opponents to exploit a deterministic pattern.

    Probabilistic Tit For Tat (PTFT) Variation:
    There is a variation of the Grofman strategy known as Probabilistic Tit For Tat (PTFT). PTFT starts by cooperating
    and then probabilistically imitates the opponent's previous move in each subsequent round.

    Performance in Tournaments:
    The Grofman strategy is designed to perform well in IPD tournaments by adapting to the opponent's strategy and
    maintaining a level of unpredictability through its probabilistic decision-making.
    """

    def __init__(self):
        super().__init__("Grofman", "Cooperate")

    @property
    def choice(self):
        return self._choice

    @choice.setter
    def choice(self, new_choice):
        self._choice = new_choice

    def strategy(self, opp_choice):
        pass


class Shubik(Strategy):
    """
    This is Shubik's strategy, which ranked fifth in Axelrod's first tournament. It plays as TFT, with the following
    modification. SHU defects once following an opponent's first defection, then co-operates. If the opponent defects
    on a second occasion when SHU co-operates, SHU then defects twice before resuming cooperation. After each occasion
    on which the opponent defects when SHU co-operates, SHU increments its retaliatory defections by one. SHU thus
    becomes progressively less forgiving, in direct arithmetic relation to the number of occasions on which SHU s
    co-operation meets with an opponent's defection.

    """

    def __init__(self):
        super().__init__("Shubik", "Cooperate")
        self.retaliation_counter = 0
        self.retaliations = 0

    @property
    def choice(self):
        return self._choice

    @choice.setter
    def choice(self, new_choice):
        self._choice = new_choice

    def strategy(self, opp_choice):
        if opp_choice == "Defect":
            self.retaliations += 1
            self.retaliation_counter = self.retaliations  # start the retaliations counter again
        else:
            if self.retaliation_counter > 0:
                self.retaliation_counter -= 1

        self.choice = ("Defect" if self.retaliation_counter else "Cooperate")


class SteinRapoport(Strategy):
    """

    """

    def __init__(self):
        super().__init__("SteinRapoport", "Cooperate")

    @property
    def choice(self):
        return self._choice

    @choice.setter
    def choice(self, new_choice):
        self._choice = new_choice

    def strategy(self, opp_choice):
        pass


class WinStayLooseShift(Strategy):
    """
    In the context of the Win-Stay, Lose-Shift (WSLS) strategy in the Iterated Prisoner's Dilemma (IPD), what is
    considered a "high payoff" is typically defined relative to the payoffs received in the previous round.

    The WSLS strategy operates based on the following principles:

    Win-Stay: If the strategy received a high payoff in the previous round (for example, mutual cooperation), it
    continues to cooperate.

    Lose-Shift: If the strategy received a low payoff in the previous round (for example, mutual defection), it shifts
    its behavior and defects in the next round.
    """

    def __init__(self):
        super().__init__("WinStayLooseShift", "Cooperate")

    @property
    def choice(self):
        return self._choice

    @choice.setter
    def choice(self, new_choice):
        self._choice = new_choice

    def strategy(self, opp_choice):
        payoff = Tools.get_payoff_type(self.choice, opp_choice)
        self.choice = ('Cooperate' if payoff in ['R', 'T', 'P'] else 'Defect')


class Benjo(Strategy):
    """
    Tit-For-Two-Tat with a WSLS resolution in the case of a 'Cooperate'.
    It's interesting to see that this resolves to a Tit-For-Tat strategy. Or at least I think it does.
    I'm leaving it here to explore.
    """

    def __init__(self):
        super().__init__("Benjo", "Cooperate")

    @property
    def choice(self):
        return self._choice

    @choice.setter
    def choice(self, new_choice):
        self._choice = new_choice

    def strategy(self, opp_choice):
        self.opp_history.append(opp_choice)
        if self.opp_history[-2:].count("Defect") == 2:
            self.choice = "Defect"
        else:
            payoff = Tools.get_payoff_type(self.choice, opp_choice)
            self.choice = ('Cooperate' if payoff in ['R', 'T', 'P'] else 'Defect')


class ModalTFT(Strategy):
    """
    Benjo's Tit For Tat.
    Returns Cooperation with Cooperation. In the case of an opponent Defect, ModalTFT will return with the mode
    of opponent's history.
    """

    def __init__(self):
        super().__init__("ModalTFT", "Cooperate")

    @property
    def choice(self):
        return self._choice

    @choice.setter
    def choice(self, new_choice):
        self._choice = new_choice

    def strategy(self, opp_choice):
        self.opp_history.append(opp_choice)
        if self.opp_history[-1] == "Cooperate":
            self.choice = "Cooperate"
        else:
            self.choice = statistics.mode(self.opp_history)


class ModalDefector(Strategy):
    """
    Benjo's Defector.
    Will defect on a cooperative response and return the mode on a Defect response.
    """

    def __init__(self):
        super().__init__("ModalDefector", "Defect")

    @property
    def choice(self):
        return self._choice

    @choice.setter
    def choice(self, new_choice):
        self._choice = new_choice

    def strategy(self, opp_choice):
        self.opp_history.append(opp_choice)
        if self.opp_history[-1] == "Cooperate":
            self.choice = "Defect"
        else:
            self.choice = statistics.mode(self.opp_history)


class Downing(Strategy):
    """
    DOWNING is based on an “outcome maximization” principle originally developed as a possible interpretation of
    what human subjects do in the Prisoner's Dilemma lab experiments (Downing 1975).
    DOWNING's strategy: – It will try to understand its opponent and then make the choice to maximize its score
    in the long run.
    """

    def __init__(self):
        super().__init__("Downing", "Cooperate")
        self.cooperate_threshold = 0.7  # Adjust as needed

    @property
    def choice(self):
        return self._choice

    @choice.setter
    def choice(self, new_choice):
        self._choice = new_choice

    def strategy(self, opp_choice):
        recent_opponent_moves = self.opp_history[-10:]  # Adjust window size as needed
        try:
            cooperate_ratio = sum(1 for move in recent_opponent_moves if move == "Cooperate") / \
                              len(recent_opponent_moves)
            if cooperate_ratio >= self.cooperate_threshold:
                self.choice = "Cooperate"
            else:
                self.choice = "Defect"
        except ZeroDivisionError:
            self.choice = "Cooperate"


class Feld(Strategy):
    """

    """

    def __init__(self):
        super().__init__("Feld", "Cooperate")

    @property
    def choice(self):
        return self._choice

    @choice.setter
    def choice(self, new_choice):
        self._choice = new_choice

    def strategy(self, opp_choice):
        pass


class Tullock(Strategy):
    """

    """

    def __init__(self):
        super().__init__("Tullock", "Cooperate")

    @property
    def choice(self):
        return self._choice

    @choice.setter
    def choice(self, new_choice):
        self._choice = new_choice

    def strategy(self, opp_choice):
        pass


class NameWithheld(Strategy):
    """

    """

    def __init__(self):
        super().__init__("NameWithheld", "Cooperate")

    @property
    def choice(self):
        return self._choice

    @choice.setter
    def choice(self, new_choice):
        self._choice = new_choice

    def strategy(self, opp_choice):
        pass


class DefectOnce(Strategy):
    """Testing purposes only. Defects once then concedes."""

    def __init__(self):
        super().__init__("DefectOnce", "Defect")

    @property
    def choice(self):
        return self._choice

    @choice.setter
    def choice(self, new_choice):
        self._choice = new_choice

    def strategy(self, opp_choice):
        self.choice = "Cooperate"

