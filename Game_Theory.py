import random


class GameRunner:
    def __init__(self, player1, player2, num_games):
        self.player1 = player1
        self.player2 = player2
        self.num_games = num_games

    def run_game(self):
        player1_score = 0
        player2_score = 0

        for _ in range(self.num_games):
            choice1 = self.player1.get_choice()
            choice2 = self.player2.get_choice()

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

            # Update the strategies with the opponent's choice
            self.player1.make_choice(choice2)
            self.player2.make_choice(choice1)
            print(f"{self.player1.name} = {choice1}\t\t {self.player2.name} = {choice2}")

        print(f"{self.player1.name}'s score: {player1_score}")
        print(f"{self.player2.name}'s score: {player2_score}")


class TitForTat:
    def __init__(self, name="TitForTat"):
        self.name = name
        self.choice = "Cooperate"

    def get_choice(self):
        return self.choice

    def set_choice(self, new_choice):
        self.choice = new_choice

    def make_choice(self, opp_choice):
        if opp_choice == "Cooperate":
            self.set_choice("Cooperate")
        else:
            self.set_choice("Defect")


class AlwaysDefect:
    def __init__(self, name="AlwaysDefect"):
        self.name = name
        self.choice = "Defect"

    def get_choice(self):
        return self.choice

    def make_choice(self, opp_choice):
        pass


class AlwaysCooperate:
    def __init__(self, name="AlwaysCooperate"):
        self.name = name
        self.choice = "Cooperate"

    def get_choice(self):
        return self.choice

    def make_choice(self, opp_choice):
        pass


class SoftTitForTat:
    def __init__(self, name="SoftTitForTat"):
        self.name = name
        self.choice = "Cooperate"
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


    def generate_choice_noise(self):
        choices = ['Cooperate', 'Defect']
        probabilities = [0.9, 0.1]

        # Generate a random choice based on the specified probabilities
        random_choice = random.choices(choices, probabilities)[0]

        return random_choice


# Example usage:
tit_for_tat_strategy = TitForTat()
soft_tit_for_tat_strategy = SoftTitForTat()
always_defect_strategy = AlwaysDefect()
always_cooperate_strategy = AlwaysCooperate()

# game_runner = GameRunner(tit_for_tat_strategy, always_defect_strategy, num_games=100)
game_runner = GameRunner(soft_tit_for_tat_strategy, always_defect_strategy, num_games=100)
# game_runner = GameRunner(tit_for_tat_strategy, always_cooperate_strategy, num_games=10)
# game_runner = GameRunner(tit_for_tat_strategy, tit_for_tat_strategy, num_games=10)
game_runner.run_game()
