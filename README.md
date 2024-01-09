# Game Theory Tournament

This Python program simulates a tournament in game theory, where different strategies compete against each other in the Prisoner's Dilemma. Strategies include TitForTat and AlwaysDefect.
The key component is the random error generator. This is to simulate false positives/negatives to simulate real world situations. For example:
"On 26 September 1983, during the Cold War, the Soviet nuclear early warning system Oko reported the launch of one intercontinental ballistic missile with four more missiles behind it, from the United States. Petrov, suspecting a false alarm, decided to wait for a confirmation that never came."

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

