from Strategies import *

# No random elements # Add more strategies as needed
strategies_non_random = [TitForTat, AlwaysDefect, GenerousTitForTat, ModalTFT, AlwaysCooperate,
                         Grudger, Graaskamp, Nydegger, DefectOnce, TitForTwoTats, WinStayLooseShift,
                         Benjo, Shubik, Downing]

# Introduced random elements
strategies_random = [TitForTat, AlwaysDefect, GenerousTitForTat, Joss, TidemanChieruzzi, Random,
                     AlwaysCooperate, Grudger, Graaskamp, Nydegger, DefectOnce, Downing,
                     TitForTwoTats, WinStayLooseShift, Benjo, Shubik, ModalTFT]

# All the strategies
strategies_all = [TitForTat, AlwaysDefect, AlwaysCooperate, GenerousTitForTat, Grudger,
                  Joss, Graaskamp, TidemanChieruzzi, Nydegger, TitForTwoTats, Random, Shubik,
                  WinStayLooseShift, Benjo, ModalTFT, ModalDefector, Downing, Grofman, Feld, Tullock,
                  Tester, SteinAndRapoport, Davis]  # NameWithheld tba

# The original Axelrod tournament
axelrod_orig = [TitForTat, TidemanChieruzzi, Nydegger, Grofman, Shubik, SteinAndRapoport, Grudger,
                Davis, Graaskamp,  Downing, Feld, Joss, Tullock, Random]  # NameWithheld tba
# NameWithheld not yet implemented

# games = random.randint(200, 1000)
games = 2000

# Running games:
# tournament = Tournament(axelrod_orig, num_games_per_match=200, noise=False)
tournament = Tournament(strategies_all, num_games_per_match=games, noise=True)  # Mess with the parameters if you want.
overall_scores = tournament.round_robin()

sorted_scores = sorted(overall_scores.items(), key=lambda x: x[1], reverse=True)
print("")
print('*'*44)
print(" Overall Scores, sorted by highest ranking:")
print('*'*44)
print(f"Number of games: {games}\n")
for strategy, score in sorted_scores:
    print(f"{strategy:>20}: {score}")
print('*'*44)

