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
Number of games: 2000

   GenerousTitForTat: 97393
           TitForTat: 95386
              Tester: 93991
               Benjo: 93743
       TitForTwoTats: 91456
    SteinAndRapoport: 91237
              Shubik: 91046
       ModalDefector: 91023
             Grudger: 90872
    TidemanChieruzzi: 90792
               Davis: 90767
        AlwaysDefect: 90415
              Random: 90408
   WinStayLooseShift: 88762
             Tullock: 86818
            Nydegger: 85091
           Graaskamp: 84922
             Grofman: 84373
                Joss: 83582
     AlwaysCooperate: 83449
                Feld: 82698
             Downing: 82538
            ModalTFT: 81969
********************************************
```
```commandline
********************************************
 Overall Scores, sorted by highest ranking:
********************************************
Number of games: 200

           TitForTat: 6489
              Shubik: 5963
    TidemanChieruzzi: 5939
             Grofman: 5889
            Nydegger: 5454
    SteinAndRapoport: 5180
             Tullock: 4774
               Davis: 4765
             Grudger: 4747
              Random: 4588
                Feld: 4406
             Downing: 4317
           Graaskamp: 3936
                Joss: 3900
********************************************
```
# References
Malik, A. (2020). Strategies for the Iterated Prisoner’s Dilemma. November 2020. Retrieved from https://arxiv.org/pdf/2111.11561.pdf

Muller, D. (2023, December 24). What The Prisoner's Dilemma Reveals About Life, The Universe, and Everything. Retrieved from https://www.youtube.com/watch?v=mScpHTIi-kM
