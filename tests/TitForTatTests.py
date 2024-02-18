from Strategies import *
import copy


class GenericTests:
    @staticmethod
    def test_name(obj, name):
        return obj.name == name

    @staticmethod
    def test_choice(obj, choice):
        return obj.choice == choice


class TitForTatTest:
    def __init__(self):
        pass

    def test_two_strategies(self, player_obj1, player_obj2, expected_outcome, num_rounds=10):
        self.player1 = copy.copy(player_obj1)
        self.player2 = copy.copy(player_obj2)
        self.player1_name = player_obj1.name
        self.player2_name = player_obj2.name

        print(f"Pitting {self.player1_name} against {self.player2_name}")
        for _ in range(num_rounds):

            # Update the history for the test strategy
            self.player1.history_data(self.player2.choice, self.player1.choice)

            expected_result = expected_outcome[(len(self.player1.history['own']) - 1)]
            test_result = 'Pass' if self.player1.history['own'][-1] == expected_result else 'Fail'
            print(f"{self.player1_name} :: {self.player1.choice:<15} "
                  f"{self.player2_name} :: {self.player2.choice} \t{test_result:<20}")

            # Run the strategies to set the next decision
            self.player1.strategy(self.player2.choice)
            self.player2.strategy(self.player1.choice)

        print(f"{self.player1_name} test "
              f"{'Passed' if self.player1.history['own'] == expected_outcome else 'Failed'}\n")
        return self.player1.history['own'] == expected_outcome


# Run tests:
C = "Cooperate"
D = "Defect"

TFT_Tester = TitForTatTest()

TFT = TitForTat()
ADF = AlwaysDefect()
ACO = AlwaysCooperate()
GTFT = GenerousTitForTat()
FMAN = Friedman()
JOSS = Joss()
GK = Graaskamp()
TCH = TidemanChieruzzi()
NYD = Nydegger()
TFTT = TitForTwoTats()
RAN = Random()
GROF = Grofman()
SHU = Shubik()
WSLS = WinStayLooseShift()
BEN = Benjo()
MTFT = ModalTFT()
MADF = ModalDefector()
DOWN = Downing()
DEF1 = DefectOnce()

TFT_results = [C, D, D, D, D, D, D, D, D, D]
ADF_results = [D, D, D, D, D, D, D, D, D, D]
ACO_results = [C, C, C, C, C, C, C, C, C, C]
GTFT_results = [C, D, D, D, D, D, D, D, D, D, D, C, D, D, D, D, D, D, D, D]
FMAN_results = [C, D, D, D, D, D, D, D, D, D]
JOSS_results = []
GK_results = [C, C, C, C, C, C, C, C, C, C,
              C, C, C, C, C, C, C, C, C, C,
              C, C, C, C, C, C, C, C, C, C,
              C, C, C, C, C, C, C, C, C, C,
              C, C, C, C, C, C, C, C, C, C,
              D, C, C, C, C, C, C, C, C, C]
TCH_results = []
NYD_results = [C, C, C, C, C, D, D, D, D, D]
TFTT_results = [C, C, D, D, D, D, D, D, D, D]
RAN_results = []
GROF_results = []
SHU_results = [C, D, D, D, D, D, D, D, D, D]
WSLS_results = [C, D, C, D, C, D, C, D, C, D]
BEN_results = [C, C, D, D, D, D, D, D, D, D]
MTFT_results = [C, D, D, D, D, D, D, D, D, D]
MADF_results = [D, D, D, D, D, D, D, D, D, D]
DOWN_results = [C, C, C, C, C, C, C, C, C, C]  # Check these results. Not sure if it should cooperate 10 times.
DEF1_results = [D, C, C, C, C, C, C, C, C, C]

TFT_Tester.test_two_strategies(TFT, ADF, TFT_results, 10)
TFT_Tester.test_two_strategies(ADF, ADF, ADF_results, 10)
TFT_Tester.test_two_strategies(ACO, ADF, ACO_results, 10)
TFT_Tester.test_two_strategies(GTFT, ADF, GTFT_results, 20)
TFT_Tester.test_two_strategies(FMAN, ADF, FMAN_results, 10)
# TFT_Tester.test_two_strategies(JOSS, ADF, JOSS_results, 10)
TFT_Tester.test_two_strategies(GK, ACO, GK_results, 60)
# TFT_Tester.test_two_strategies(TCH, ADF, TCH_results, 10)
TFT_Tester.test_two_strategies(NYD, ADF, NYD_results, 10)
TFT_Tester.test_two_strategies(TFTT, ADF, TFTT_results, 10)
# TFT_Tester.test_two_strategies(RAN, ADF, RAN_results, 10)
# TFT_Tester.test_two_strategies(GROF, ADF, GROF_results, 10)
TFT_Tester.test_two_strategies(SHU, ADF, SHU_results, 10)
TFT_Tester.test_two_strategies(WSLS, ADF, WSLS_results, 10)
TFT_Tester.test_two_strategies(BEN, ADF, BEN_results, 10)
TFT_Tester.test_two_strategies(MTFT, ADF, MTFT_results, 10)
TFT_Tester.test_two_strategies(MADF, ADF, MADF_results, 10)
TFT_Tester.test_two_strategies(DOWN, ADF, DOWN_results, 10)
TFT_Tester.test_two_strategies(DEF1, ADF, DEF1_results, 10)
