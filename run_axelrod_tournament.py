from GameTools import Tournament
from Strategies import *

# No random elements # Add more strategies as needed
strategies_non_random = [TitForTat, AlwaysDefect, GenerousTitForTat, ModalTFT, AlwaysCooperate,
                         Friedman, Graaskamp, Nydegger, DefectOnce, TitForTwoTats, WinStayLooseShift,
                         Benjo, Shubik, Downing]

# Introduced random elements
strategies_random = [TitForTat, AlwaysDefect, GenerousTitForTat, Joss, TidemanChieruzzi, Random,
                     AlwaysCooperate, Friedman, Graaskamp, Nydegger, DefectOnce, Downing,
                     TitForTwoTats, WinStayLooseShift, Benjo, Shubik, ModalTFT]

strategies_all = [TitForTat, AlwaysDefect, AlwaysCooperate, GenerousTitForTat, Friedman,
                  Joss, Graaskamp, TidemanChieruzzi, Nydegger, TitForTwoTats, Random, Shubik,
                  WinStayLooseShift, Benjo, ModalTFT, ModalDefector, Downing]

# games = random.randint(200, 1000)
games = 2000

# Running games
tournament = Tournament(strategies_all, num_games_per_match=games, noise=True)  # Mess with the parameters if you want.
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

