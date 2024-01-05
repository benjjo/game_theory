class Strategy:
    def __init__(self, name, init_choice):
        self.name = name
        self.choice = init_choice

    def set_choice(self, choice):
        self.choice = choice
        raise NotImplementedError("Subclasses must implement the set_choice method")

    def get_choice(self):
        raise NotImplementedError("Subclasses must implement the get_choice method")

    def make_choice(self, opp_choice):
        raise NotImplementedError("Subclasses must implement the make_choice method")


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
        if opp_choice == "Cooperate":
            self.set_choice("Cooperate")
        else:
            self.set_choice("Defect")


class AlwaysDefect(Strategy):
    """The strategy of the logical. This strategy is not a push-over and never will be. It is also unforgiving.
    The logical strategy concludes that the opponent will also choose to Defect. This is because of the risk
    involved with the selection of the cooperative choice. While not the most optimal, it will guarantee points.
    A 'NOT NICE' strategy in that we start and end with provocation."""

    def __init__(self):
        super().__init__("AlwaysDefect", "Defect")

    def get_choice(self):
        return self.choice

    def make_choice(self, opp_choice):
        pass


class AlwaysCooperate(Strategy):
    """The strategy of do only kindness unto all.This strategy is a push-over but has the potential to score the
    highest.
     A 'NICE' strategy in that we start and end peacefully."""

    def __init__(self):
        super().__init__("AlwaysCooperate", "Cooperate")

    def get_choice(self):
        return self.choice

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
        self.update_opp_choice(new_choice)
        self.choice = new_choice

    def update_opp_choice(self, recent_choice):
        self.historic_opponent_choices.append(recent_choice)

    def make_choice(self, opp_choice):
        if 'Defect' in self.historic_opponent_choices:
            self.set_choice("Defect")
        elif opp_choice == "Cooperate":
            self.set_choice("Cooperate")
        else:
            self.set_choice("Defect")

