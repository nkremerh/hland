import move

class Game():
    def __init__(self, hland, player1, player2, turns):
        self.hland = hland
        self.player1 = player1
        self.player2 = player2
        self.turns = turns

        self.gameOver = False
        self.moves = []
        self.player1Score = 0
        self.player2Score = 0
        self.tie = False
        self.winner = None
        self.winnerScore = None

    def doTurn(self):
        if self.turns > 0:
            newMove = move.Move(self.hland, self.player1, self.player2)
            self.player1Score += newMove.player1Score
            self.player2Score += newMove.player2Score
            self.moves.append(newMove)
            self.turns -= 1
        else:
            self.gameOver = True
            if self.player1Score > self.player2Score:
                self.winner = self.player1
                self.winnerScore = self.player1Score
            elif self.player1Score < self.player2Score:
                self.winner = self.player2
                self.winnerScore = self.player2Score
            else:
                self.tie = True
                self.winnerScore = self.player1Score

    def setupNewGame(self):
        self.player1.setupNewGame()
        self.player2.setupNewGame()

    def __str__(self):
        string = f"{self.player1.strategyName} ({self.player1Score})/{self.player2.strategyName} ({self.player2Score})\n"
        if self.tie == True:
            string += f"Winner: TIE {self.player1.strategyName}/{self.player2.strategyName} -> {self.winnerScore}"
        else:
            string += f"Winner: {self.winner.strategyName} -> {self.winnerScore}"
        return string
