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
            otherMove = self.history[-1].player1Move if self.history[-1].player1 == other else self.history[-1].player2Move
            betrayalCheck = other.history[-1]
            if otherMove == "defect":
                self.betrayed = True
                return "defect"
            return "cooperate"
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
        return "defect"

class SuspiciousTitForTat(player.Player):
    def __init__(self, playerID, configuration, hland):
        super().__init__(playerID, configuration, hland)
        self.strategyName = "Suspicious Tit for Tat"

    def findBestMove(self, other):
        if len(self.history) == 0:
            return "defect"
        otherMove = self.history[-1].player1Move if self.history[-1].player1 == other else self.history[-1].player2Move
        return otherMove

class TitForTat(player.Player):
    def __init__(self, playerID, configuration, hland):
        super().__init__(playerID, configuration, hland)
        self.strategyName = "Tit for Tat"

    def findBestMove(self, other):
        if len(self.history) == 0:
            return "cooperate"
        otherMove = self.history[-1].player1Move if self.history[-1].player1 == other else self.history[-1].player2Move
        return otherMove

class TitForTwoTats(player.Player):
    def __init__(self, playerID, configuration, hland):
        super().__init__(playerID, configuration, hland)
        self.strategyName = "Tit for Two Tats"
        self.tats = 0

    def findBestMove(self, other):
        if len(self.history) == 0:
            return "cooperate"
        otherMove = self.history[-1].player1Move if self.history[-1].player1 == other else self.history[-1].player2Move
        if otherMove == "defect":
            self.tats += 1
        if self.tats % 2 == 0 and self.tats > 0:
            return "defect"
        return "cooperate"

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
