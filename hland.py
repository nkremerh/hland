#! /usr/bin/python

import player
import game
import move
import strategy

import getopt
import json
import random
import sys

class Hland:
    def __init__(self, configuration):
        self.configuration = configuration
        self.nextPlayerID = 0
        self.seed = configuration["seed"]
        self.payoutMatrix = configuration["payoutMatrix"]

        self.players = self.configurePlayers()
        self.games = self.configureGames()
        self.runtimeStats = {"meanTurnsPerGame": 0, "gamesPlayed": 0, "bestStrategy": None, "bestStrategyScore": 0}
        self.log = open(configuration["logfile"], 'a') if configuration["logfile"] != None else None
        self.logFormat = configuration["logfileFormat"]

        self.scores = {}
        self.winner = None
        self.winnerScore = None

    def configurePlayers(self):
        players = []
        numPlayers = self.configuration["startingPlayers"]
        playerConfigurations = self.randomizePlayerConfigurations(numPlayers)
        for i in range(numPlayers):
            playerConfiguration = playerConfigurations[i]
            playerID = self.generatePlayerID()
            a = player.Player(playerID, playerConfiguration, self)
            # If using a different decision model, replace new player with instance of child class
            if "bentham" in playerConfiguration["strategy"]:
                a = strategy.Bentham(playerID, playerConfiguration, self)
            elif "grim" in playerConfiguration["strategy"]:
                a = strategy.Grim(playerID, playerConfiguration, self)
            elif "random" in playerConfiguration["strategy"]:
                a = strategy.Random(playerID, playerConfiguration, self)
            elif "titForTat" in playerConfiguration["strategy"]:
                a = strategy.TitForTat(playerID, playerConfiguration, self)
            elif "trigger" in playerConfiguration["strategy"]:
                a = strategy.Trigger(playerID, playerConfiguration, self)
            elif "unconditionalCooperator" in playerConfiguration["strategy"]:
                a = strategy.UnconditionalCooperator(playerID, playerConfiguration, self)
            elif "unconditionalDefector" in playerConfiguration["strategy"]:
                a = strategy.UnconditionalDefector(playerID, playerConfiguration, self)
            players.append(a)
        return players

    def configureGames(self):
        if self.players == None:
            self.players = self.configurePlayers()
        turns = self.configureTurnsPerGame()
        games = []
        i = 0
        for player1 in self.players:
            for player2 in self.players:
                newGame = game.Game(self, player1, player2, turns[i])
                i += 1
                games.append(newGame)
        return games

    def configureTurnsPerGame(self):
        if self.players == None:
            self.players = self.configurePlayers()
        turns = []
        minTurns = self.configuration["turnsPerGame"][0]
        maxTurns = self.configuration["turnsPerGame"][1]
        currTurns = minTurns
        for i in range(len(self.players) ** 2):
            if currTurns > maxTurns:
                currTurns = minTurns
            turns.append(currTurns)
            currTurns += 1
        random.shuffle(turns)
        return turns

    def doTournament(self):
        if self.games == None:
            self.games = self.configureGames()
        for game in self.games:
            self.playGame(game)
            self.updateRuntimeStats()
        print(self)

    def endLog(self):
        if self.log == None:
            return
        logString = '\t' + json.dumps(self.runtimeStats) + "\n]"
        if self.logFormat == "csv":
            logString = ""
            # Ensure consistent ordering for CSV format
            for stat in sorted(self.runtimeStats):
                if logString == "":
                    logString += f"{self.runtimeStats[stat]}"
                else:
                    logString += f",{self.runtimeStats[stat]}"
            logString += "\n"
        self.log.write(logString)
        self.log.flush()
        self.log.close()

    def endSimulation(self):
        exit(0)

    def generatePlayerID(self):
        playerID = self.nextPlayerID
        self.nextPlayerID += 1
        return playerID

    def getPayout(self, player1Move, player2Move):
        if player1Move == "cooperate" and player2Move == "cooperate":
            return self.payoutMatrix[0]
        elif player1Move == "cooperate" and player2Move == "defect":
            return self.payoutMatrix[1]
        elif player1Move == "defect" and player2Move == "cooperate":
            return self.payoutMatrix[2]
        elif player1Move == "defect" and player2Move == "defect":
            return self.payoutMatrix[3]

    def playGame(self, game):
        game.setupNewGame()
        for t in range(game.turns + 1):
            game.doTurn()
        game.endGame()
        print(game)

    def randomizePlayerConfigurations(self, numPlayers):
        configs = self.configuration
        strategies = []
        configurations = []
        if configs["strategies"] == None:
            configs["strategies"] = ["default"]
        for i in range(numPlayers):
            strategy = configs["strategies"][i % len(configs["strategies"])]
            strategies.append(strategy)
        random.shuffle(strategies)
        for i in range(numPlayers):
            playerConfiguration = {"seed": self.seed, "strategy": strategies.pop()}
            configurations.append(playerConfiguration)
        return configurations

    def runSimulation(self):
        self.startLog()
        self.doTournament()
        self.endLog()
        self.endSimulation()

    def startLog(self):
        if self.log == None:
            return
        if self.logFormat == "csv":
            header = ""
            # Ensure consistent ordering for CSV format
            for stat in sorted(self.runtimeStats):
                if header == "":
                    header += f"{stat}"
                else:
                    header += f",{stat}"
            header += "\n"
            self.log.write(header)
        else:
            self.log.write("[\n")
        self.updateRuntimeStats()
        self.writeToLog()

    def updateRuntimeStats(self):
        runtimeStats = {"meanTurnsPerGame": 0, "gamesPlayed": 0, "bestStrategy": None, "bestStrategyScore": 0}
        for key in runtimeStats.keys():
            self.runtimeStats[key] = runtimeStats[key]
        strategies = {}
        for player in self.players:
            if player.strategyName not in strategies:
                strategies[player.strategyName] = player.tournamentScore
            else:
                strategies[player.strategyName] += player.tournamentScore
        self.winner = max(strategies, key=strategies.get)
        self.winnerScore = strategies[self.winner]
        self.scores = strategies

    def writeToLog(self):
        if self.log == None:
            return
        logString = '\t' + json.dumps(self.runtimeStats) + ",\n"
        if self.logFormat == "csv":
            logString = ""
            # Ensure consistent ordering for CSV format
            for stat in sorted(self.runtimeStats):
                if logString == "":
                    logString += f"{self.runtimeStats[stat]}"
                else:
                    logString += f",{self.runtimeStats[stat]}"
            logString += "\n"
        self.log.write(logString)

    def __str__(self):
        string = f"Tournament Seed: {self.seed}\nWinner: {self.winner} ({self.winnerScore})\nPlayers: {self.scores}"
        return string

def parseConfiguration(configFile, configuration):
    file = open(configFile)
    options = json.loads(file.read())
    options = options["hlandOptions"]

    for opt in configuration:
        if opt in options:
            configuration[opt] = options[opt]
    return configuration

def parseOptions(configuration):
    commandLineArgs = sys.argv[1:]
    shortOptions = "c:h:"
    longOptions = ["conf=", "help"]
    try:
        args, vals = getopt.getopt(commandLineArgs, shortOptions, longOptions)
    except getopt.GetoptError as err:
        print(err)
        printHelp()
    nextArg = 0
    for currArg, currVal in args:
        nextArg += 1
        if currArg in("-c", "--conf"):
            if currVal == "":
                print("No config file provided.")
                printHelp()
            parseConfiguration(currVal, configuration)
        elif currArg in ("-h", "--help"):
            printHelp()
    return configuration

def printHelp():
    print("Usage:\n\tpython hland.py --conf config.json\n\nOptions:\n\t-c,--conf\tUse specified config file for simulation settings.\n\t-h,--help\tDisplay this message.")
    exit(0)

def verifyConfiguration(configuration):
    ranges = ["turnsPerGame"]
    negativeFlag = 0
    for configName in ranges:
        configValue = configuration[configName]
        if isinstance(configValue, list):
            if len(configValue) == 0:
                continue
            configValue.sort()
            for i in range(len(configValue)):
                if configValue[i] < 0:
                    configValue[i] = 0
                    negativeFlag += 1
    if negativeFlag > 0:
        print(f"Detected negative values provided for {negativeFlag} option(s). Setting these values to zero.")
    if configuration["logfile"] == "":
        configuration["logfile"] = None
    if configuration["seed"] == -1:
        configuration["seed"] = random.randrange(sys.maxsize)
    return configuration

if __name__ == "__main__":
    # Set default values for simulation configuration
    configuration = {"logfile": None,
                     "logfileFormat": "json",
                     "payoutMatrix": [(4, 4), (1, 5), (5, 1), (2, 2)],
                     "profileMode": False,
                     "seed": -1,
                     "strategies": None,
                     "startingPlayers": 2,
                     "turnsPerGame": [1, 1]
                     }
    configuration = parseOptions(configuration)
    configuration = verifyConfiguration(configuration)
    random.seed(configuration["seed"])
    H = Hland(configuration)
    if configuration["profileMode"] == True:
        import cProfile
        import tracemalloc
        tracemalloc.start()
        cProfile.run("H.runSimulation()")
        snapshot = tracemalloc.take_snapshot()
        memoryStats = snapshot.statistics("lineno", True)
        for stat in memoryStats[:100]:
            print(stat)
    else:
        H.runSimulation()
    exit(0)
