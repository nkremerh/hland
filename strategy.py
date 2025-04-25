import player

import random

class Bentham(player.Player):
    def __init__(self, playerID, configuration, hland):
        super().__init__(playerID, configuration, hland)
        self.strategyName = "Bentham Utilitarian"

    def findBestMove(self, other):
        # TODO: Translate Bentham algorithm from Sugarscape to H*land
        return "cooperate"

class Grim(player.Player):
    def __init__(self, playerID, configuration, hland):
        super().__init__(playerID, configuration, hland)
        self.strategyName = "Grim"
        self.betrayed = False

    def findBestMove(self, other):
        if len(self.history) == 0:
            return "cooperate"
        elif self.betrayed == False:
            betrayalCheck = other.history[-1]
            if len(other.history) > len(self.history):
                # Other player went first this turn
                betrayalCheck = other.history[-2]
            if betrayalCheck == "defect":
                self.betrayed = True
                return "defect"
            return "cooperate"
        else:
            return "defect"

    def setupNewGame(self):
        self.betrayed = False
        self.history = []

class Random(player.Player):
    def __init__(self, playerID, configuration, hland):
        super().__init__(playerID, configuration, hland)
        self.strategyName = "Random"

    def findBestMove(self, other):
        choice = random.randint(0, 1)
        if choice == 0:
            return "cooperate"
        else:
            return "defect"

class TitForTat(player.Player):
    def __init__(self, playerID, configuration, hland):
        super().__init__(playerID, configuration, hland)
        self.strategyName = "Tit for Tat"

    def findBestMove(self, other):
        if len(self.history) == 0:
            return "cooperate"
        else:
            if len(other.history) > len(self.history):
                # Other player went first this turn
                return other.history[-2]
            return other.history[-1]

class Trigger(Grim):
    def __init__(self, playerID, configuration, hland):
        super().__init__(playerID, configuration, hland)
        # Alternate name for the Grim strategy
        self.strategyName = "Trigger"

class UnconditionalCooperator(player.Player):
    def __init__(self, playerID, configuration, hland):
        super().__init__(playerID, configuration, hland)
        self.strategyName = "Unconditional Cooperator"

    def findBestMove(self, other):
        return "cooperate"

class UnconditionalDefector(player.Player):
    def __init__(self, playerID, configuration, hland):
        super().__init__(playerID, configuration, hland)
        self.strategyName = "Unconditional Defector"

    def findBestMove(self, other):
        return "defect"
