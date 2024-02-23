# Game Theory - Axelrod Tournament

This Python program simulates a tournament in the vein of the Axelrod Tournament, where different strategies compete against each other in the game of the Prisoner's Dilemma. Strategies include TitForTat and AlwaysDefect for example. This Tournament is an attempt to replicate and help understand the works of "Strategies for the Iterated Prisoner’s Dilemma" (Anagh Malik, 2020), and is heavily influenced by the Youtube channel Veritasium and their presentation "What The Prisoner's Dilemma Reveals About Life, The Universe, and Everything". 

The key component to replicating the results presented in the Veritasium presentation is the random error generator. This is to simulate false positives/negatives to simulate real world situations. Veritasium use the example:
```"On 26 September 1983, during the Cold War, the Soviet nuclear early warning system Oko reported the launch of one intercontinental ballistic missile with four more missiles behind it, from the United States. Petrov, suspecting a false alarm, decided to wait for a confirmation that never came." ```

This is a work in progress and created out of curiosity. The end goal is to simply replicate the results of the Axelrod Tournament and setup some simple python code for others to expand on if that should tickle one's fancy. 

# Description

Classes
`GameRunner`
The `GameRunner` class runs a specified number of games between two strategies and calculates the scores.

The `Tournament` class orchestrates multiple `GameRunner` sessions for various pairs of strategies, keeping an overall tally of scores.

The `Strategy` class is the base class for different strategies. It includes common methods like `make_choice`, `set_choice` and `get_choice`. It includes common attributes including `name` and `init_choice`.

Subclass examples: `TitForTat` is a strategy that cooperates initially and then mimics the opponent's last move.
`AlwaysDefect` is a strategy that always chooses to defect.

# Example usage:
I simply run the `prisoners_dilema.py` script in a python shell to retrieve the output. Or something like PyCharm/VS-Code/Jupyter-Lab will enable you to see the output printed to the screen. The below shows the code that is tacked onto the end of the script. Update to modify the output.  

```commandline
from Strategies import *

# No random elements # Add more strategies as needed
strategies_non_random = [TitForTat, AlwaysDefect, GenerousTitForTat, ModalTFT, AlwaysCooperate,
                         Friedman, Graaskamp, Nydegger, DefectOnce, TitForTwoTats, WinStayLooseShift,
                         Benjo, Shubik, Downing]

# Introduced random elements
strategies_random = [TitForTat, AlwaysDefect, GenerousTitForTat, Joss, TidemanChieruzzi, Random,
                     AlwaysCooperate, Friedman, Graaskamp, Nydegger, DefectOnce, Downing,
                     TitForTwoTats, WinStayLooseShift, Benjo, Shubik, ModalTFT]

# All the strategies
strategies_all = [TitForTat, AlwaysDefect, AlwaysCooperate, GenerousTitForTat, Friedman,
                  Joss, Graaskamp, TidemanChieruzzi, Nydegger, TitForTwoTats, Random, Shubik,
                  WinStayLooseShift, Benjo, ModalTFT, ModalDefector, Downing]

# games = random.randint(200, 1000)
games = 2000

# Running games
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
```

# Example output
```commandline
********************************************
 Overall Scores, sorted by highest ranking:
********************************************
GenerousTitForTat: 4475
TitForTat: 4067
Friedman: 4064
AlwaysDefect: 3837
AlwaysCooperate: 3832
********************************************
```
```commandline
********************************************
 Overall Scores, sorted by highest ranking:
********************************************
Nydegger: 7852
AlwaysCooperate: 7201
GenerousTitForTat: 7157
TitForTat: 6692
Graaskamp: 6421
Friedman: 6074
AlwaysDefect: 5139
Joss: 5090
********************************************
```
```commandline
********************************************
 Overall Scores, sorted by highest ranking:
********************************************
Number of games: 303

TitForTwoTats: 15191
Nydegger: 14571
GenerousTitForTat: 14360
AlwaysCooperate: 13977
TitForTat: 13168
Random: 13130
Graaskamp: 12810
Joss: 11382
Friedman: 11051
AlwaysDefect: 10284
********************************************
```
```commandline
********************************************
 Overall Scores, sorted by highest ranking:
********************************************
Number of games: 2000

   GenerousTitForTat: 74207
           TitForTat: 72877
       TitForTwoTats: 72112
               Benjo: 71256
              Random: 66892
            ModalTFT: 65699
     AlwaysCooperate: 64952
   WinStayLooseShift: 64364
            Nydegger: 62681
           Graaskamp: 61749
                Joss: 60123
            Friedman: 59906
    TidemanChieruzzi: 59730
              Shubik: 59649
        AlwaysDefect: 59537
       ModalDefector: 59421
             Downing: 58230
********************************************
```
# References
Malik, A. (2020). Strategies for the Iterated Prisoner’s Dilemma. November 2020. Retrieved from https://arxiv.org/pdf/2111.11561.pdf

Muller, D. (2023, December 24). What The Prisoner's Dilemma Reveals About Life, The Universe, and Everything. Retrieved from https://www.youtube.com/watch?v=mScpHTIi-kM
