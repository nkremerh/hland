import math
import random

class Player:
    def __init__(self, agentID, configuration, hland):
        self.ID = agentID
        self.configuration = configuration
        self.hland = hland

        self.history = []
        self.strategyName = "Hobbes, Hume, or Hyde"

    def addMoveToHistory(self, move):
        self.history.append(move)

    def doMove(self, other):
        move = self.findBestMove(other)
        self.addMoveToHistory(move)
        return move

    def findBestMove(self, other):
        move = random.randint(0, 2) if len(self.history) > 0 else random.randint(0, 1)
        if move == 0:
            # Act as Hobbes and adhere to the social contract
            return "cooperate"
        elif move == 1:
            # Act as Hume and be a slave to the passions
            return "defect"
        else:
            # Act as Hyde and do the opposite of last move
            previousMove = self.history[-1]
            if previousMove.player1 == self:
                previousMove = previousMove.player1Move
            else:
                previousMove = previousMove.player2Move
            if previousMove == "cooperate":
                return "defect"
            else:
                return "cooperate"

    def setupNewGame(self):
        self.history = []

    def __str__(self):
        return f"{self.ID}"
