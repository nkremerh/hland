class Move():
    def __init__(self, hland, player1, player2):
        self.player1 = player1
        self.player2 = player2
        self.player1Move = player1.doMove(self.player2)
        self.player2Move = player2.doMove(self.player1)
        self.player1Score, self.player2Score = hland.getPayout(self.player1Move, self.player2Move)

    def __str__(self):
        string = f"Player 1 Strategy: {self.player1.strategyName}\nPlayer 2 Strategy: {self.player2.strategyName}\n"
        string += f"Player 1 Move: {self.player1Move:^9} -> {self.player1Score:^5}\n"
        string += f"Player 2 Move: {self.player2Move:^9} -> {self.player2Score:^5}"
        return string
