from GameTools import *
import statistics
C = "Cooperate"
D = "Defect"


class Strategy:
    def __init__(self, name, init_choice):
        self.name = name
        self._choice = init_choice
        self.history = {'own': [], 'opp': []}

    @property
    def choice(self):
        raise NotImplementedError("Subclasses must implement the set_choice method")

    @choice.setter
    def choice(self, value):
        """The choice parameter is set by the run_game method within the GameRunner class. This is the previous choice
        set by the opponent."""
        self._choice = value
        raise NotImplementedError("Subclasses must implement the set_choice method")

    def history_data(self, opponent_choice, own_choice):
        self.history['own'].append(own_choice)
        self.history['opp'].append(opponent_choice)
        raise NotImplementedError("Subclasses must implement the set_choice method")

    def strategy(self):
        raise NotImplementedError("Subclasses must implement the make_choice method")


class TitForTat(Strategy):
    """The strategy of do unto thee what was done unto me. Not really an eye-for-an because it is not vengeance
     that is sought, but more that this strategy is not a push-over.
     A 'NICE' strategy in that we start peacefully until provoked."""

    def __init__(self):
        super().__init__("TitForTat", C)

    @property
    def choice(self):
        return self._choice

    @choice.setter
    def choice(self, new_choice):
        self._choice = new_choice

    def history_data(self, opponent_choice, own_choice):
        self.history['own'].append(own_choice)
        self.history['opp'].append(opponent_choice)

    def strategy(self):
        self.choice = self.history['opp'][-1]


class AlwaysDefect(Strategy):
    """The strategy of the logical. This strategy is not a push-over and never will be. It is also unforgiving.
    The logical strategy concludes that the opponent will also choose to Defect. This is because of the risk
    involved with the selection of the cooperative choice. While not the most optimal, it will guarantee points.
    A 'NOT NICE' strategy in that we start and end with provocation."""

    def __init__(self):
        super().__init__("AlwaysDefect", D)

    @property
    def choice(self):
        return self._choice

    @choice.setter
    def choice(self, new_choice):
        self._choice = new_choice

    def history_data(self, opponent_choice, own_choice):
        self.history['own'].append(own_choice)
        self.history['opp'].append(opponent_choice)

    def strategy(self):
        self.choice = D


class AlwaysCooperate(Strategy):
    """The strategy of do only kindness unto all.This strategy is a push-over but has the potential to score the
    highest.
     A 'NICE' strategy in that we start and end peacefully."""

    def __init__(self):
        super().__init__("AlwaysCooperate", C)

    @property
    def choice(self):
        return self._choice

    @choice.setter
    def choice(self, new_choice):
        self._choice = new_choice

    def history_data(self, opponent_choice, own_choice):
        self.history['own'].append(own_choice)
        self.history['opp'].append(opponent_choice)

    def strategy(self):
        self.choice = C


class GenerousTitForTat(Strategy):
    """The strategy of do unto thee what was done unto me but let's not get ourselves tied up in a circular argument
    for all eternity. This strategy is not a push-over.
    A 'NICE' strategy in that we start peacefully until provoked but if we continue in a cycle of punishment, it will
    sacrifice a move for the greater good."""

    def __init__(self):
        super().__init__("GenerousTitForTat", C)
        # self.historic_choices = list()

    @property
    def choice(self):
        return self._choice

    @choice.setter
    def choice(self, new_choice):
        self._choice = new_choice

    def history_data(self, opponent_choice, own_choice):
        self.history['own'].append(own_choice)
        self.history['opp'].append(opponent_choice)

    def strategy(self):
        # Check own historical selections and make a choice
        try:
            if self.history['own'][-10:].count(D) >= 10:
                self.choice = C
            else:
                self.choice = self.history['opp'][-1]
        except IndexError:
            self.choice = self.history['opp'][-1]


class Grudger(Strategy):
    """The strategy of do nice unto others until betrayed. This strategy is not a push-over.
     A 'NICE' strategy in that we start peacefully until provoked. Once provoked it is unforgiving"""

    def __init__(self):
        super().__init__("Grudger", C)

    @property
    def choice(self):
        return self._choice

    @choice.setter
    def choice(self, new_choice):
        self._choice = new_choice

    def history_data(self, opponent_choice, own_choice):
        self.history['own'].append(own_choice)
        self.history['opp'].append(opponent_choice)

    def strategy(self):
        # print(D in self.history['opp'])
        if D in self.history['opp']:
            self.choice = D
        else:
            self.choice = C


class Joss(Strategy):
    """Similar to Tit-For-tat in that it will start out as Cooperative and will mimic the opponent.
    However, as a sneaky little side hustle, Joss will Defect around 10% of the time."""

    def __init__(self):
        super().__init__("Joss", C)

    @property
    def choice(self):
        return self._choice

    @choice.setter
    def choice(self, new_choice):
        self._choice = new_choice

    def history_data(self, opponent_choice, own_choice):
        self.history['own'].append(own_choice)
        self.history['opp'].append(opponent_choice)

    def strategy(self):
        if random.randint(1, 10) == 1:
            self.choice = D
        else:
            if self.history['opp']:
                self.choice = self.history['opp'][-1]


class Graaskamp(Strategy):
    """Similar to Joss in that it will start out as Cooperative and mimic the opponent.
    However, Graaskamp will defect every 50th round."""

    def __init__(self):
        super().__init__("Graaskamp", C)
        self.round = int()

    @property
    def choice(self):
        return self._choice

    @choice.setter
    def choice(self, new_choice):
        self._choice = new_choice

    def history_data(self, opponent_choice, own_choice):
        self.history['own'].append(own_choice)
        self.history['opp'].append(opponent_choice)

    def strategy(self):
        self.round += 1
        if self.round % 50 == 0:
            self.choice = D
        else:
            self.choice = self.history['opp'][-1]


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
        super().__init__("TidemanChieruzzi", C)
        self.retaliation_counter = 0
        self.retaliations = 0
        self.fresh_start = bool()
        self.fresh_start_counter = 0
        self.my_points = 0
        self.their_points = 0
        self.games_counter = 0
        self.own_defect_history = bool()

    @property
    def choice(self):
        return self._choice

    @choice.setter
    def choice(self, new_choice):
        self._choice = new_choice

    def history_data(self, opponent_choice, own_choice):
        self.history['own'].append(own_choice)
        self.history['opp'].append(opponent_choice)

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
        try:
            self.own_defect_history = self.history['own'][-2:].count(D) == 2
        except IndexError:
            self.own_defect_history = False

        return (
                self.my_points - self.their_points >= 10
                and self.own_defect_history
                and self.fresh_start_counter > 20
                and self.games_counter < 190
                and Tools.compare_samples(Tools.random_5050_sample(self.games_counter, 0.7), self.history['own']))

    def strategy(self):
        self.set_fresh_start_condition(self.choice, self.history['opp'][-1])

        if self.history['opp'][-1] == D:
            self.retaliations += 1
            self.retaliation_counter = self.retaliations  # start the retaliations counter again
        else:
            if self.retaliation_counter > 0:
                self.retaliation_counter -= 1

        if self.fresh_start:
            self.retaliation_counter = 0

        self.choice = (D if self.retaliation_counter else C)


class Nydegger(Strategy):
    """
        The Nydegger strategy is based on the following rules:

        The Nydegger strategy cooperates on the first round.
        After the first round, it analyzes the opponent's last five moves.
        If the opponent has defected in three or more of the last five moves, Nydegger will defect.
        Otherwise, it will cooperate."""

    def __init__(self):
        super().__init__("Nydegger", C)

    @property
    def choice(self):
        return self._choice

    @choice.setter
    def choice(self, new_choice):
        self._choice = new_choice

    def history_data(self, opponent_choice, own_choice):
        self.history['own'].append(own_choice)
        self.history['opp'].append(opponent_choice)

    def strategy(self):
        if len(self.history['opp']) >= 5:
            self.choice = statistics.mode(self.history['opp'][-5:])
        else:
            self.choice = C


class TitForTwoTats(Strategy):
    """
        The TitForTwoTats strategy is based on the following rules:

        The Sample strategy cooperates on the first round.
        After the first round, it analyzes the opponent's last two moves.
        If the opponent has defected both times, Sample will defect.
        Otherwise, it will cooperate."""

    def __init__(self):
        super().__init__("TitForTwoTats", C)

    @property
    def choice(self):
        return self._choice

    @choice.setter
    def choice(self, new_choice):
        self._choice = new_choice

    def history_data(self, opponent_choice, own_choice):
        self.history['own'].append(own_choice)
        self.history['opp'].append(opponent_choice)

    def strategy(self):
        if len(self.history['opp']) >= 2:
            if self.history['opp'][-2:].count(D) == 2:
                self.choice = D
            else:
                self.choice = C
        else:
            self.choice = C


class Random(Strategy):
    """Straight up random"""

    def __init__(self):
        super().__init__("Random", C)

    @property
    def choice(self):
        return self._choice

    @choice.setter
    def choice(self, new_choice):
        self._choice = new_choice

    def history_data(self, opponent_choice, own_choice):
        self.history['own'].append(own_choice)
        self.history['opp'].append(opponent_choice)

    def strategy(self):
        self.choice = random.choice([D, C])


class Grofman(Strategy):
    """
    Submitted to Axelrod’s first tournament by Bernard Grofman.

    The description written in [Axelrod1980] is:

    “If the players did different things on the previous move, this rule cooperates with probability 2/7.
    Otherwise, this rule always cooperates.”
    This strategy came 4th in Axelrod’s original tournament.
    """

    def __init__(self):
        super().__init__("Grofman", C)

    @property
    def choice(self):
        return self._choice

    @choice.setter
    def choice(self, new_choice):
        self._choice = new_choice

    def history_data(self, opponent_choice, own_choice):
        self.history['own'].append(own_choice)
        self.history['opp'].append(opponent_choice)

    def strategy(self):
        if len(self.history['opp']) > 1:
            if self.history['opp'][-1] != self.history['opp'][-2]:
                self.choice = random.choices([C, D], weights=[0.71, 0.29])[0]
            else:
                self.choice = C
        else:
            self.choice = C


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
        super().__init__("Shubik", C)
        self.retaliation_counter = 0
        self.retaliations = 0

    @property
    def choice(self):
        return self._choice

    @choice.setter
    def choice(self, new_choice):
        self._choice = new_choice

    def history_data(self, opponent_choice, own_choice):
        self.history['own'].append(own_choice)
        self.history['opp'].append(opponent_choice)

    def strategy(self):
        if self.history['opp'][-1] == D:
            self.retaliations += 1
            self.retaliation_counter = self.retaliations  # start the retaliations counter again
            self.choice = D
        else:
            if self.retaliation_counter > 0:
                self.retaliation_counter -= 1
            self.choice = (D if self.retaliation_counter else C)

        if self.retaliation_counter > 0:
            self.retaliation_counter -= 1


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
        super().__init__("WinStayLooseShift", C)
        self.payoff = 'R'

    @property
    def choice(self):
        return self._choice

    @choice.setter
    def choice(self, new_choice):
        self._choice = new_choice

    def history_data(self, opponent_choice, own_choice):
        self.history['own'].append(own_choice)
        self.history['opp'].append(opponent_choice)

    def strategy(self):
        if self.history['opp']:
            self.payoff = Tools.get_payoff_type(self.history['own'][-1], self.history['opp'][-1])
        self.choice = (C if self.payoff in ['R', 'P'] else D)


class Benjo(Strategy):
    """
    Tit-For-Two-Tat with a WSLS resolution in the case of a 'Cooperate'.
    It's interesting to see that this resolves to a Tit-For-Tat strategy. Or at least I think it does.
    I'm leaving it here to explore.
    """

    def __init__(self):
        super().__init__("Benjo", C)
        self.payoff = 'R'

    @property
    def choice(self):
        return self._choice

    @choice.setter
    def choice(self, new_choice):
        self._choice = new_choice

    def history_data(self, opponent_choice, own_choice):
        self.history['own'].append(own_choice)
        self.history['opp'].append(opponent_choice)

    def strategy(self):
        if len(self.history['opp']) >= 2:
            if self.history['opp'][-2:].count(D) == 2:
                self.choice = D
            else:
                self.choice = statistics.mode(self.history['opp'])
        else:
            self.choice = C


class ModalTFT(Strategy):
    """
    Benjo's Tit For Tat.
    Returns Cooperation with Cooperation. In the case of an opponent Defect, ModalTFT will return with the mode
    of opponent's history.
    """

    def __init__(self):
        super().__init__("ModalTFT", C)

    @property
    def choice(self):
        return self._choice

    @choice.setter
    def choice(self, new_choice):
        self._choice = new_choice

    def history_data(self, opponent_choice, own_choice):
        self.history['own'].append(own_choice)
        self.history['opp'].append(opponent_choice)

    def strategy(self):
        if self.history['opp']:
            if self.history['opp'][-1] == C:
                self.choice = C
            else:
                self.choice = statistics.mode(self.history['opp'])


class ModalDefector(Strategy):
    """
    Benjo's Defector.
    Will defect on a cooperative response and return the mode on a Defect response.
    """

    def __init__(self):
        super().__init__("ModalDefector", D)

    @property
    def choice(self):
        return self._choice

    @choice.setter
    def choice(self, new_choice):
        self._choice = new_choice

    def history_data(self, opponent_choice, own_choice):
        self.history['own'].append(own_choice)
        self.history['opp'].append(opponent_choice)

    def strategy(self):
        if self.history['opp']:
            if self.history['opp'][-1] == C:
                self.choice = D
            else:
                self.choice = statistics.mode(self.history['opp'])


class Downing(Strategy):
    """
    DOWNING is based on an “outcome maximization” principle originally developed as a possible interpretation of
    what human subjects do in the Prisoner's Dilemma lab experiments (Downing 1975).
    DOWNING's strategy: – It will try to understand its opponent and then make the choice to maximize its score
    in the long run.
    """

    def __init__(self):
        super().__init__("Downing", C)
        self.cooperate_threshold = 0.7  # Adjust as needed

    @property
    def choice(self):
        return self._choice

    @choice.setter
    def choice(self, new_choice):
        self._choice = new_choice

    def history_data(self, opponent_choice, own_choice):
        self.history['own'].append(own_choice)
        self.history['opp'].append(opponent_choice)

    def strategy(self):
        if len(self.history['opp']) >= 10:
            cooperate_ratio = self.history['opp'][-10:].count(C) / 10
            if cooperate_ratio >= self.cooperate_threshold:
                self.choice = C
            else:
                self.choice = D


# noinspection PyPep8Naming
class Feld(Strategy):
    """
    Submitted to Axelrod’s first tournament by Scott Feld.

    The description written in [Axelrod1980] is:

    “This rule starts with tit-for-tat and gradually lowers its probability of cooperation following the other’s
    cooperation to .5 by the two hundredth move. It always defects after a defection by the other.”

    This strategy plays Tit For Tat, always defecting if the opponent defects but cooperating when the opponent
    cooperates with a gradually decreasing probability until it is only .5. Note that the description does not
    clearly indicate how the cooperation probability should drop. This implements a linear decreasing function.

    This strategy came 11th in Axelrod’s original tournament.
    """

    def __init__(self):
        super().__init__("Feld", C)
        self.probability_of_Cooperation = 1

    @property
    def choice(self):
        return self._choice

    @choice.setter
    def choice(self, new_choice):
        self._choice = new_choice

    def history_data(self, opponent_choice, own_choice):
        self.history['own'].append(own_choice)
        self.history['opp'].append(opponent_choice)

    def strategy(self):
        if self.history['opp']:
            if self.history['opp'][-1] == D:
                self.choice = D
            else:
                weight_C = self.probability_of_Cooperation
                weight_D = 1 - weight_C
                self.choice = random.choices([C, D], weights=[weight_C, weight_D])[0]
        if self.probability_of_Cooperation >= 0.5:
            self.probability_of_Cooperation -= 0.0025


# noinspection PyPep8Naming
class Tullock(Strategy):
    """
    Submitted to Axelrod’s first tournament by Gordon Tullock.

    The description written in [Axelrod1980] is:

    “This rule cooperates on the first eleven moves. It then cooperates 10% less than the other player has
    cooperated on the preceding ten moves. This rule is based on an idea developed in Overcast and Tullock (1971).
    Professor Tullock was invited to specify how the idea could be implemented, and he did so out of scientific
    interest rather than an expectation that it would be a likely winner.”

    This is interpreted as:

    Cooperates for the first 11 rounds then randomly cooperates 10% less often than the opponent has in the
    previous 10 rounds.

    This strategy came 13th in Axelrod’s original tournament.
    """

    def __init__(self):
        super().__init__("Tullock", C)
        self.probability_of_Cooperation = 0.5

    @property
    def choice(self):
        return self._choice

    @choice.setter
    def choice(self, new_choice):
        self._choice = new_choice

    def history_data(self, opponent_choice, own_choice):
        self.history['own'].append(own_choice)
        self.history['opp'].append(opponent_choice)

    def strategy(self):
        if len(self.history['opp']) % 10 == 0 and self.history['opp']:
            count_opp_C = self.history['opp'][-10:].count(C)
            self.probability_of_Cooperation = count_opp_C - 1
            if self.probability_of_Cooperation > 0:
                self.probability_of_Cooperation /= 10
            else:
                self.probability_of_Cooperation = 0
            weight_C = self.probability_of_Cooperation
            weight_D = 1 - weight_C
            self.choice = random.choices([C, D], weights=[weight_C, weight_D])[0]
        else:
            self.choice = C


class NameWithheld(Strategy):
    """
    The description written in [Axelrod1980] is:
    “This rule has a probability of cooperating, P, which is initially 30% and > is updated every 10 moves.
    P is adjusted if the other player seems random, very cooperative, or very uncooperative. P is also adjusted
    after move 130 if the rule has a lower score than the other player. Unfortunately, the complex process of
    adjustment frequently left the probability of cooperation in the 30% to 70% range, and therefore the rule
    appeared random to many other players.”

    Given the lack of detail this strategy is implemented based on the final sentence of the description which is
    to have a cooperation probability that is uniformly random in the 30 to 70% range.
    """

    def __init__(self):
        super().__init__("NameWithheld", C)

    @property
    def choice(self):
        return self._choice

    @choice.setter
    def choice(self, new_choice):
        self._choice = new_choice

    def history_data(self, opponent_choice, own_choice):
        self.history['own'].append(own_choice)
        self.history['opp'].append(opponent_choice)

    def strategy(self):
        pass


class DefectOnce(Strategy):
    """Testing purposes only. Defects once then concedes."""

    def __init__(self):
        super().__init__("DefectOnce", D)

    @property
    def choice(self):
        return self._choice

    @choice.setter
    def choice(self, new_choice):
        self._choice = new_choice

    def history_data(self, opponent_choice, own_choice):
        self.history['own'].append(own_choice)
        self.history['opp'].append(opponent_choice)

    def strategy(self):
        self.choice = C


class CooperateOnce(Strategy):
    """Testing purposes only. Cooperates once then hates."""

    def __init__(self):
        super().__init__("CooperateOnce", C)

    @property
    def choice(self):
        return self._choice

    @choice.setter
    def choice(self, new_choice):
        self._choice = new_choice

    def history_data(self, opponent_choice, own_choice):
        self.history['own'].append(own_choice)
        self.history['opp'].append(opponent_choice)

    def strategy(self):
        self.choice = D


class Tester(Strategy):
    """
    Will probe the opponent on the first move with a Defect. If the opponent responds with a Defect, it will play
    TitForTat. If the opponent responds with a Cooperation, it will Defect every other move for the rest of the game.

    """

    def __init__(self):
        super().__init__("Tester", D)

    @property
    def choice(self):
        return self._choice

    @choice.setter
    def choice(self, new_choice):
        self._choice = new_choice

    def history_data(self, opponent_choice, own_choice):
        self.history['own'].append(own_choice)
        self.history['opp'].append(opponent_choice)

    def strategy(self):
        if self.history['opp']:
            if self.history['opp'][0] == D:
                self.choice = self.history['opp'][-1]
            else:
                self.choice = D if self.history['own'][-1] == C else C


class SteinAndRapoport(Strategy):
    """
    Submitted to Axelrod’s first tournament by William Stein and Amnon Rapoport.

    The description written in [Axelrod1980] is:

    “This rule plays tit-for-tat except that it cooperates on the first four moves, it defects on the last two
    moves, and every fifteen moves it checks to see if the opponent seems to be playing randomly. This check uses a
    chi-squared test of the other’s transition probabilities and also checks for alternating moves of CD and DC.

    This is implemented as follows:

    It cooperates for the first 4 moves.
    It defects on the last 2 moves.
    Every 15 moves it makes use of a chi-squared test to check if the opponent is playing randomly. If so it defects.
    This strategy came 6th in Axelrod’s original tournament.

    """

    def __init__(self):
        super().__init__("SteinAndRapoport", C)

    @property
    def choice(self):
        return self._choice

    @choice.setter
    def choice(self, new_choice):
        self._choice = new_choice

    def history_data(self, opponent_choice, own_choice):
        self.history['own'].append(own_choice)
        self.history['opp'].append(opponent_choice)

    def strategy(self):
        if len(self.history['own']) > 4:
            if len(self.history['own']) < 198:
                if len(self.history['own']) % 15 == 0:
                    if Tools.is_alternating_pattern(self.history['opp']) \
                            or Tools.check_randomness(self.history['opp']):
                        self.choice = D
                    elif Tools.check_randomness(self.history['opp']):
                        self.choice = D
            else:
                self.choice = D
        else:
            self.choice = C


class Davis(Strategy):
    """
    Submitted to Axelrod’s first tournament by Morton Davis.

    The description written in [Axelrod1980] is:

    “A player starts by cooperating for 10 rounds then plays Grudger, defecting if at any point the opponent
    has defected.”

    This strategy came 8th in Axelrod’s original tournament.
    """

    def __init__(self):
        super().__init__("Davis", C)

    @property
    def choice(self):
        return self._choice

    @choice.setter
    def choice(self, new_choice):
        self._choice = new_choice

    def history_data(self, opponent_choice, own_choice):
        self.history['own'].append(own_choice)
        self.history['opp'].append(opponent_choice)

    def strategy(self):
        if len(self.history['opp']) >= 10:
            self.choice = D if D in self.history['opp'] else C
        else:
            self.choice = C
