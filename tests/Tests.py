from Strategies import *
import unittest
from itertools import cycle

C = "Cooperate"
D = "Defect"


def test_game(strategy_obj, opponent_choice):
    strategy_obj.strategy()
    strategy_obj.history_data(own_choice=strategy_obj.choice, opponent_choice=opponent_choice)


class StrategyTester(unittest.TestCase):

    def test_TFT(self):
        # Instantiate the test strategy
        self.TFT = TitForTat()

        # Check the name
        self.assertTrue(self.TFT.name == "TitForTat")

        # Check first choice
        self.assertIs(C, self.TFT.choice)

        # Test against a specific set of actions
        self.TFT.history['own'] = [C, C, C, C, C, C, C, C, C, C]
        self.TFT.history['opp'] = [C, C, C, C, C, C, C, C, C, C]
        test_game(self.TFT, D)
        self.assertIs(C, self.TFT.choice)
        test_game(self.TFT, C)
        self.assertIs(D, self.TFT.choice)

    def test_ADF(self):
        # Instantiate the test strategy
        self.ADF = AlwaysDefect()

        # Check the name
        self.assertTrue(self.ADF.name == "AlwaysDefect")

        # Check first choice
        self.assertIs(D, self.ADF.choice)

        # Test against a specific set of actions
        self.ADF.history['own'] = [D, D, D, D, D, D, D, D, D, D]
        self.ADF.history['opp'] = [C, C, C, C, C, C, C, C, C, C]
        test_game(self.ADF, D)
        self.assertIs(D, self.ADF.choice)

    def test_ACO(self):
        # Instantiate the test strategy
        self.ACO = AlwaysCooperate()

        # Check the name
        self.assertTrue(self.ACO.name == "AlwaysCooperate")

        # Check first choice
        self.assertIs(C, self.ACO.choice)

        # Test against a specific set of actions
        self.ACO.history['own'] = [C, C, C, C, C, C, C, C, C, C]
        self.ACO.history['opp'] = [D, D, D, D, D, D, D, D, D, D]
        test_game(self.ACO, D)
        self.assertIs(C, self.ACO.choice)

    def test_GTFT(self):
        # Instantiate the test strategy
        self.GTFT = GenerousTitForTat()

        # Check the name
        self.assertTrue(self.GTFT.name == "GenerousTitForTat")

        # Check first choice
        self.assertIs(C, self.GTFT.choice)

        # Test against a specific set of actions
        self.GTFT.history['own'] = [D] * 9
        self.GTFT.history['opp'] = [D] * 9
        test_game(self.GTFT, D)
        self.assertIs(D, self.GTFT.choice)

        self.GTFT.history['own'] = [D] * 10
        self.GTFT.history['opp'] = [D] * 10
        test_game(self.GTFT, D)
        self.assertIs(C, self.GTFT.choice)

    def test_GRUD(self):
        # Instantiate the test strategy
        self.GRUD = Grudger()

        # Check the name
        self.assertTrue(self.GRUD.name == "Grudger")

        # Check first choice
        self.assertIs(C, self.GRUD.choice)

        # Test against a Defective move
        test_game(self.GRUD, D)
        self.assertIs(C, self.GRUD.choice)

        # Defect is now in the history data
        test_game(self.GRUD, C)
        self.assertIs(D, self.GRUD.choice)

        # Test against a specific set of actions
        self.GRUD.history['own'] = [C, C, C, C, C, C, C, C, C, C]
        self.GRUD.history['opp'] = [C, C, C, C, C, C, C, C, C, D]
        test_game(self.GRUD, C)
        self.assertIs(D, self.GRUD.choice)

    def test_JOSS(self):
        # Instantiate the test strategy
        self.JOSS = Joss()

        # Check the name
        self.assertTrue(self.JOSS.name == "Joss")

        # Check first choice
        self.assertIs(C, self.JOSS.choice)

        # Test against a specific set of actions
        for _ in range(100):
            test_game(self.JOSS, C)
        self.assertIn(D, self.JOSS.history['own'], 'Did not generate a Defect in 100 iterations.')

    def test_GK(self):
        # Instantiate the test strategy
        self.GK = Graaskamp()

        # Check the name
        self.assertTrue(self.GK.name == "Graaskamp")

        # Check first choice
        self.assertIs(C, self.GK.choice)

        # Test against a specific set of actions
        self.GK.history['own'] = [D] * 49
        self.GK.history['opp'] = [D] * 49
        test_game(self.GK, D)
        self.assertIs(D, self.GK.choice)

        self.GK.history['own'] = [D] * 50
        self.GK.history['opp'] = [D] * 49 + [C]
        test_game(self.GK, C)
        self.assertIs(C, self.GK.choice)

    def test_TCH(self):
        # Instantiate the test strategy
        self.TCH = TidemanChieruzzi()

        # Check the name
        self.assertTrue(self.TCH.name == "TidemanChieruzzi")

        # Check first choice
        self.assertIs(C, self.TCH.choice)

        # Test against a specific set of actions
        self.TCH.history['own'] = [C, C, C, C, C, C, C, C, C, C]
        self.TCH.history['opp'] = [C, C, C, C, C, C, C, C, C, C]
        test_game(self.TCH, D)
        self.assertIs(C, self.TCH.choice)

    def test_NYD(self):
        # Instantiate the test strategy
        self.NYD = Nydegger()

        # Check the name
        self.assertTrue(self.NYD.name == "Nydegger")

        # Check first choice
        self.assertIs(C, self.NYD.choice)

        # Test against a specific set of actions
        self.NYD.history['own'] = [C, C, C, C, C, C]
        self.NYD.history['opp'] = [C, C, D, C, D, C]
        test_game(self.NYD, D)
        self.assertIs(C, self.NYD.choice)
        test_game(self.NYD, C)
        self.assertIs(D, self.NYD.choice)

    def test_TFTT(self):
        # Instantiate the test strategy
        self.TFTT = TitForTwoTats()

        # Check the name
        self.assertTrue(self.TFTT.name == "TitForTwoTats")

        # Check first choice
        self.assertIs(C, self.TFTT.choice)

        # Test against a specific set of actions
        self.TFTT.history['own'] = [C, C, C, C, C]
        self.TFTT.history['opp'] = [C, C, D, C, D]
        test_game(self.TFTT, D)
        self.assertIs(C, self.TFTT.choice)
        test_game(self.TFTT, C)
        self.assertIs(D, self.TFTT.choice)

    def test_RAN(self):
        # Instantiate the test strategy
        self.RAN = Random()

        # Check the name
        self.assertTrue(self.RAN.name == "Random")

        # Check first choice
        self.assertIs(C, self.RAN.choice)

    def test_GROF(self):
        # Instantiate the test strategy
        self.GROF = Grofman()

        # Check the name
        self.assertTrue(self.GROF.name == "Grofman")

        # Check first choice
        self.assertIs(C, self.GROF.choice)
        for _ in range(10):
            test_game(self.GROF, C)
        self.assertEqual(self.GROF.history['own'], [C, C, C, C, C, C, C, C, C, C], 'Mismatched historical data')

        self.GROF = Grofman()
        cycle_choice = cycle([C, D])
        for _ in range(10000):
            iter_choice = next(cycle_choice)
            test_game(self.GROF, iter_choice)
        counts = {element: self.GROF.history['own'].count(element) for element in set(self.GROF.history['own'])}
        self.assertTrue(counts[D] / counts[C] < 0.42, 'Unweighted distribution detected.')

    def test_SHU(self):
        # Instantiate the test strategy
        self.SHU = Shubik()

        # Check the name
        self.assertTrue(self.SHU.name == "Shubik")

        # Check first choice
        self.assertIs(C, self.SHU.choice)

        # Test against a specific set of actions
        self.SHU.history['own'] = [C]
        self.SHU.history['opp'] = [C]
        test_game(self.SHU, D)
        self.assertIs(C, self.SHU.choice)
        self.assertEqual(self.SHU.retaliation_counter, 0)
        self.assertEqual(self.SHU.history['own'], [C, C])

        # The next choice should be a Cooperate if the Opponent chooses Cooperate, and the counter should decrement.
        test_game(self.SHU, C)
        self.assertIs(D, self.SHU.choice)
        self.assertEqual(self.SHU.retaliation_counter, 0)
        self.assertEqual(self.SHU.retaliations, 1)
        self.assertEqual(self.SHU.history['own'], [C, C, D], 'Mismatched historical data')

        # The next two choices from the opponent will be Defect. This should trigger two defects.
        test_game(self.SHU, D)
        # Retaliations should reset to 2
        self.assertEqual(self.SHU.retaliation_counter, 0)
        self.assertEqual(self.SHU.retaliations, 1)
        test_game(self.SHU, D)
        # Retaliations should reset to 3
        self.assertEqual(self.SHU.retaliation_counter, 1)
        self.assertEqual(self.SHU.retaliations, 2)
        test_game(self.SHU, C)
        test_game(self.SHU, C)
        test_game(self.SHU, C)
        # self.assertIs(D, self.SHU.choice)
        self.assertEqual(self.SHU.retaliation_counter, 0)
        self.assertEqual(self.SHU.retaliations, 3)
        self.assertEqual(self.SHU.history['own'], [C, C, D, C, D, D, D, C], 'Mismatched historical data')

    def test_WSLS(self):
        # Instantiate the test strategy
        self.WSLS = WinStayLooseShift()

        # Check the name
        self.assertTrue(self.WSLS.name == "WinStayLooseShift")

        # Check first choice
        self.assertIs(C, self.WSLS.choice)

        # Both Cooperate, then opponent Defects
        self.WSLS.history['own'] = [C]
        self.WSLS.history['opp'] = [C]
        test_game(self.WSLS, D)
        self.assertIs(C, self.WSLS.choice)
        test_game(self.WSLS, D)
        self.assertIs(D, self.WSLS.choice)

        # Both Defect, then opponent Cooperates
        self.WSLS.history['own'] = [D]
        self.WSLS.history['opp'] = [D]
        test_game(self.WSLS, C)
        self.assertIs(C, self.WSLS.choice)
        test_game(self.WSLS, C)
        self.assertIs(C, self.WSLS.choice)

        # Opponent Defects, then Cooperates
        self.WSLS.history['own'] = [D, C]
        self.WSLS.history['opp'] = [D, D]
        test_game(self.WSLS, C)
        self.assertIs(D, self.WSLS.choice)
        test_game(self.WSLS, C)
        self.assertIs(D, self.WSLS.choice)

    def test_BEN(self):
        # Instantiate the test strategy
        self.BEN = Benjo()

        # Check the name
        self.assertTrue(self.BEN.name == "Benjo")

        # Check first choice
        self.assertIs(C, self.BEN.choice)

        # Test against a specific set of actions
        self.BEN.history['own'] = [C, C, C, C, C]
        self.BEN.history['opp'] = [C, C, D, C, D]
        test_game(self.BEN, D)
        self.assertIs(C, self.BEN.choice)
        test_game(self.BEN, C)
        self.assertIs(D, self.BEN.choice)

    def test_MTFT(self):
        # Instantiate the test strategy
        self.MTFT = ModalTFT()

        # Check the name
        self.assertTrue(self.MTFT.name == "ModalTFT")

        # Check first choice
        self.assertIs(C, self.MTFT.choice)

        # Test against a specific set of actions
        self.MTFT.history['own'] = [C, C, C, C, C]
        self.MTFT.history['opp'] = [C, C, C, C, C]
        test_game(self.MTFT, D)
        self.assertIs(C, self.MTFT.choice)

        # Test against a specific set of actions
        self.MTFT.history['own'] = [C, C, C, C, C]
        self.MTFT.history['opp'] = [C, C, C, D, D]
        test_game(self.MTFT, D)
        self.assertIs(C, self.MTFT.choice)

        # Tipping point for Defection
        self.MTFT.history['own'] = [C, C, C, C, C]
        self.MTFT.history['opp'] = [C, C, D, D, D]
        test_game(self.MTFT, D)
        self.assertIs(D, self.MTFT.choice)

    def test_MADF(self):
        # Instantiate the test strategy
        self.MADF = ModalDefector()

        # Check the name
        self.assertTrue(self.MADF.name == "ModalDefector")

        # Check first choice
        self.assertIs(D, self.MADF.choice)

        # Test against a specific set of actions
        self.MADF.history['own'] = [C]
        self.MADF.history['opp'] = [C]
        test_game(self.MADF, D)
        self.assertIs(D, self.MADF.choice)
        test_game(self.MADF, C)
        self.assertIs(C, self.MADF.choice)

    def test_DOWN(self):
        # Instantiate the test strategy
        self.DOWN = Downing()

        # Check the name
        self.assertTrue(self.DOWN.name == "Downing")

        # Check first choice
        self.assertIs(C, self.DOWN.choice)

        # Test against 100% compliance
        self.DOWN.history['own'] = [C, C, C, C, C, C, C, C, C, C]
        self.DOWN.history['opp'] = [C, C, C, C, C, C, C, C, C, C]
        test_game(self.DOWN, C)
        self.assertIs(C, self.DOWN.choice)

        # Test against 80% compliance
        self.DOWN.history['own'] = [C, C, C, C, C, C, C, C, C, C]
        self.DOWN.history['opp'] = [C, C, C, C, C, C, C, C, D, D]
        test_game(self.DOWN, C)
        self.assertIs(C, self.DOWN.choice)

        # Test against 70% compliance
        self.DOWN.history['own'] = [C, C, C, C, C, C, C, C, C, C]
        self.DOWN.history['opp'] = [C, C, C, C, C, C, C, D, D, D]
        test_game(self.DOWN, C)
        self.assertIs(C, self.DOWN.choice)

        # Test against 60% compliance
        self.DOWN.history['own'] = [C, C, C, C, C, C, C, C, C, C]
        self.DOWN.history['opp'] = [C, C, C, C, C, C, D, D, D, D]
        test_game(self.DOWN, C)
        self.assertIs(D, self.DOWN.choice)

    def test_FELD(self):
        # Instantiate the test strategy
        self.FEL = Feld()

        # Check the name
        self.assertTrue(self.FEL.name == "Feld")
        # The following is used to calculate the prob. of cooperation. Used to test later.
        self.assertTrue(self.FEL.probability_of_Cooperation)

        # Check first choice
        self.assertIs(C, self.FEL.choice)

        # Test for the probability of Tit-for-tat behaviour as games increase
        cycle_choice = cycle([C, D])
        for _ in range(100):
            iter_choice = next(cycle_choice)
            test_game(self.FEL, iter_choice)
        # At 100 games, the probability of TFT behaviour should be at 0.75
        self.assertEqual(round(self.FEL.probability_of_Cooperation, 2), 0.75)

        # Test for the probability of Tit-for-tat behaviour as games increases to 0.5.
        for _ in range(100):
            iter_choice = next(cycle_choice)
            test_game(self.FEL, iter_choice)
        # At 200 games, the probability of TFT behaviour should be at 0.5
        self.assertEqual(round(self.FEL.probability_of_Cooperation, 1), 0.5)

    def test_TUL(self):
        # Instantiate the test strategy
        self.TUL = Tullock()

        # Check the name
        self.assertTrue(self.TUL.name == "Tullock")

        # Check first choice
        self.assertIs(C, self.TUL.choice)

        # Test for the probability of Tit-for-tat behaviour as games increase
        cycle_choice = cycle([C, D])
        for _ in range(10):
            iter_choice = next(cycle_choice)
            test_game(self.TUL, iter_choice)
        self.assertEqual(self.TUL.history['own'], [C, C, C, C, C, C, C, C, C, C])
        test_game(self.TUL, D)
        self.assertTrue(self.TUL.probability_of_Cooperation == 0.4)
        for _ in range(6):
            test_game(self.TUL, D)
        for _ in range(4):
            test_game(self.TUL, C)
        self.assertTrue(self.TUL.probability_of_Cooperation == 0.2)

    def test_DEF1(self):
        # Instantiate the test strategy
        self.DEF1 = DefectOnce()

        # Check the name
        self.assertTrue(self.DEF1.name == "DefectOnce")

        # Check first choice
        self.assertIs(D, self.DEF1.choice)

        # Test against a specific set of actions
        self.DEF1.history['own'] = [C, C, C, C, C, C, C, C, C, C]
        self.DEF1.history['opp'] = [C, C, C, C, C, C, C, C, C, C]
        test_game(self.DEF1, D)
        self.assertIs(C, self.DEF1.choice)
        test_game(self.DEF1, D)
        self.assertIs(C, self.DEF1.choice)

    def test_COOP1(self):
        # Instantiate the test strategy
        self.COOP1 = CooperateOnce()

        # Check the name
        self.assertTrue(self.COOP1.name == "CooperateOnce")

        # Check first choice
        self.assertIs(C, self.COOP1.choice)

        # Test against a specific set of actions
        self.COOP1.history['own'] = [C, C, C, C, C, C, C, C, C, C]
        self.COOP1.history['opp'] = [C, C, C, C, C, C, C, C, C, C]
        test_game(self.COOP1, C)
        self.assertIs(D, self.COOP1.choice)
        test_game(self.COOP1, C)
        self.assertIs(D, self.COOP1.choice)

    def test_TST(self):
        # Instantiate the test strategy
        self.TST = Tester()

        # Check the name
        self.assertTrue(self.TST.name == "Tester")

        # Check first choice
        self.assertIs(D, self.TST.choice)

        # Test against Defection on the first response from opponent (1st choice being C, response being D)
        test_game(self.TST, D)
        # Test choice
        self.assertIs(D, self.TST.choice)  # C matching first choice of opponent
        # Test history
        self.assertEqual([D], self.TST.history['own'])
        self.assertEqual([D], self.TST.history['opp'])

        self.TST = Tester()
        # Test that TitForTat continues
        for _ in range(5):
            test_game(self.TST, D)
        for _ in range(5):
            test_game(self.TST, C)

        # Test history
        self.assertEqual([D, D, D, D, D, D, C, C, C, C], self.TST.history['own'])
        self.assertEqual([D, D, D, D, D, C, C, C, C, C], self.TST.history['opp'])

        # Fresh start
        self.TST = Tester()
        # Test against Cooperation on the first response from opponent
        test_game(self.TST, C)
        self.assertIs(D, self.TST.choice)

        # Test that TitForTat continues
        for _ in range(4):
            test_game(self.TST, D)
        for _ in range(5):
            test_game(self.TST, C)

        # Test history
        self.assertEqual([D, C, D, C, D, C, D, C, D, C], self.TST.history['own'])
        self.assertEqual([C, D, D, D, D, C, C, C, C, C], self.TST.history['opp'])

    def test_SAP(self):
        # Instantiate the test strategy
        self.SAP = SteinAndRapoport()

        # Check the name
        self.assertTrue(self.SAP.name == "SteinAndRapoport")

        # Check first choice
        self.assertIs(C, self.SAP.choice)

        # Check first 4 are C
        for _ in range(4):
            test_game(self.SAP, D)
        self.assertEqual(self.SAP.history['own'], [C, C, C, C])

        # Check 15th move chooses C following a slew of C
        self.SAP = SteinAndRapoport()
        self.assertIs(C, self.SAP.choice)
        for _ in range(16):
            test_game(self.SAP, C)
        self.assertIs(self.SAP.choice, C)

        # Check 15th Move Defects after a random sample
        self.SAP = SteinAndRapoport()
        for _ in range(16):
            test_game(self.SAP, random.choice([C, D]))
        self.assertIs(self.SAP.choice, D)

        # Check 15th Move Defects after a random sample
        self.SAP = SteinAndRapoport()
        for _ in range(16):
            test_game(self.SAP, random.choice([C, D]))
        self.assertIs(self.SAP.choice, D)

        # Check 199th and 200th Moves Defect
        self.SAP = SteinAndRapoport()
        for _ in range(200):
            test_game(self.SAP, C)
        self.assertEqual(self.SAP.history['own'][-2:], [D, D])

        # Check 15th Move Defects after an alternating pattern is detected
        self.SAP = SteinAndRapoport()
        cycle_choice = cycle([C, D])
        for _ in range(16):
            iter_choice = next(cycle_choice)
            test_game(self.SAP, iter_choice)
        self.assertIs(self.SAP.history['own'][-1], D)

    def test_DAV(self):
        # Instantiate the test strategy
        self.DAV = Davis()

        # Check the name
        self.assertTrue(self.DAV.name == "Davis")

        # Check first choice
        self.assertIs(C, self.DAV.choice)

        # Test against a specific set of actions
        for _ in range(10):
            test_game(self.DAV, D)
        self.assertIs(self.DAV.choice, C)
        test_game(self.DAV, C)
        self.assertIs(D, self.DAV.choice)
        for _ in range(100):
            test_game(self.DAV, C)
        self.assertIs(self.DAV.choice, D)



class ToolsTester(unittest.TestCase):

    def test_calculate_payoff(self):
        self.assertEqual(Tools.calculate_payoff(C, C), 3)
        self.assertEqual(Tools.calculate_payoff(C, D), 0)
        self.assertEqual(Tools.calculate_payoff(D, C), 5)
        self.assertEqual(Tools.calculate_payoff(D, D), 1)

    def test_calculate_payoff_type(self):
        self.assertEqual(Tools.get_payoff_type(C, C), 'R')
        self.assertEqual(Tools.get_payoff_type(C, D), 'S')
        self.assertEqual(Tools.get_payoff_type(D, C), 'T')
        self.assertEqual(Tools.get_payoff_type(D, D), 'P')

    def test_random_5050_sample(self):
        test_list = Tools.random_5050_sample(100, 0.7)
        # Test that list only contains C and D
        test_result = (test_list.count(C) + test_list.count(D) == len(test_list))
        self.assertTrue(test_result)
        # Test that the list contains both C and D
        self.assertTrue(C and D in test_list, 'Unified data in test list')

    def test_compare_samples(self):
        test_case = Tools.compare_samples([C, C, D, D], [D, D, C, C])
        self.assertFalse(test_case)
        test_case = Tools.compare_samples([D, D, D, C], [C, C, D, D])
        self.assertFalse(test_case)
        test_case = Tools.compare_samples([C, C, C, C], [D, D, D, D])
        self.assertTrue(test_case)

    def test_score_board(self):
        tournament = Tournament([AlwaysDefect, AlwaysCooperate], num_games_per_match=1, noise=False)
        overall_scores = tournament.round_robin()
        self.assertEqual(overall_scores['AlwaysDefect'], 6)
        self.assertEqual(overall_scores['AlwaysCooperate'], 3)

    def test_object_spawner(self):
        test_list = [AlwaysDefect, TitForTat]
        test_output = Tools.object_spawner(test_list)
        self.assertEqual(len(test_output), 2)

    def test_check_randomness(self):
        test_list = [C]*1000
        test_output = Tools.check_randomness(test_list)
        self.assertFalse(test_output)
        test_list = list()
        for _ in range(100):
            test_list.append(random.choice([C, D]))
        test_output = Tools.check_randomness(test_list)
        self.assertTrue(test_output)
        test_list = list()
        cycle_list = cycle([C, D])
        for _ in range(1000):
            test_list.append(next(cycle_list))
        test_output = Tools.check_randomness(test_list)
        self.assertFalse(test_output)

    def test_is_alternating_pattern(self):
        test_list = list()
        cycle_list = cycle([C, D])
        for _ in range(1000):
            test_list.append(next(cycle_list))
        test_result = Tools.is_alternating_pattern(test_list)
        self.assertTrue(test_result)
        test_list.append(C)
        test_list.append(C)
        test_result = Tools.is_alternating_pattern(test_list)
        self.assertFalse(test_result)


# Run tests:
if __name__ == '__main__':
    unittest.main()
