# Game Theory - Axelrod Tournament

This Python program simulates a tournament in the vein of the Axelrod Tournament, where different strategies compete against each other in the game of the Prisoner's Dilemma. Strategies include TitForTat and AlwaysDefect for example. This Tournament is an attempt to replicate and help understand the works of "Strategies for the Iterated Prisoner’s Dilemma" (Anagh Malik, 2020), and is heavily influenced by the Youtube channel Veritasium and their presentation "What The Prisoner's Dilemma Reveals About Life, The Universe, and Everything". 

The key component to replicating the results presented in the Veritasium presentation is the random error generator. This is to simulate false positives/negatives to simulate real world situations. Veritasium use the example:
```"On 26 September 1983, during the Cold War, the Soviet nuclear early warning system Oko reported the launch of one intercontinental ballistic missile with four more missiles behind it, from the United States. Petrov, suspecting a false alarm, decided to wait for a confirmation that never came." ```

This is a work in progress and created out of curiosity. The end goal is to simply replicate the results of the Axelrod Tournament and setup some nice clean python code for others to expand on if that should tickle one's fancy. 

# Description

Classes
`GameRunner`
The `GameRunner` class runs a specified number of games between two strategies and calculates the scores.

`Strategy`
The `Strategy` class is the base class for different strategies. It includes common methods like `make_choice` and `update_opponent_choice`.

Subclasses
`TitForTat`: A strategy that cooperates initially and then mimics the opponent's last move.
`AlwaysDefect`: A strategy that always chooses to defect.

`Tournament`
The `Tournament` class orchestrates multiple `GameRunner` sessions for various pairs of strategies, keeping an overall tally of scores.

# Example usage:
I simply run this is a python shell to retrieve the output. Or something like PyCharm/VS-Code/Jupyter-Lab will all enable you to see the output to the screen. 

```
strategies = [TitForTat, AlwaysDefect, SoftTitForTat, AlwaysCooperate, Friedman]  # Add more strategies as needed
tournament = Tournament(strategies, num_games_per_match=200)
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


# References
Malik, A. (2020). Strategies for the Iterated Prisoner’s Dilemma. November 2020. Retrieved from https://arxiv.org/pdf/2111.11561.pdf

Muller, D. (2023, December 24). What The Prisoner's Dilemma Reveals About Life, The Universe, and Everything. Retrieved from https://www.youtube.com/watch?v=mScpHTIi-kM
