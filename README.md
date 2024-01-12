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

```
strategies = [TitForTat, AlwaysDefect, SoftTitForTat, AlwaysCooperate, Friedman]  # Add more strategies as needed
tournament = Tournament(strategies, num_games_per_match=200, noise=True)  # noise=False will remove random noise.
overall_scores = tournament.run_tournament()

sorted_scores = sorted(overall_scores.items(), key=lambda x: x[1], reverse=True)
print("")
print('*'*44)
print(" Overall Scores, sorted by highest ranking:")
print('*'*44)
for strategy, score in sorted_scores:
    print(f"{strategy}: {score}")
print('*'*44)
```

# Example output
```
********************************************
 Overall Scores, sorted by highest ranking:
********************************************
SoftTitForTat: 4475
TitForTat: 4067
Friedman: 4064
AlwaysDefect: 3837
AlwaysCooperate: 3832
********************************************
```
```
********************************************
 Overall Scores, sorted by highest ranking:
********************************************
Nydegger: 7852
AlwaysCooperate: 7201
SoftTitForTat: 7157
TitForTat: 6692
Graaskamp: 6421
Friedman: 6074
AlwaysDefect: 5139
Joss: 5090
********************************************
```
# References
Malik, A. (2020). Strategies for the Iterated Prisoner’s Dilemma. November 2020. Retrieved from https://arxiv.org/pdf/2111.11561.pdf

Muller, D. (2023, December 24). What The Prisoner's Dilemma Reveals About Life, The Universe, and Everything. Retrieved from https://www.youtube.com/watch?v=mScpHTIi-kM
