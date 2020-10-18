from agents.Agent import Agent
from games import games

class Game:
    def __init__(self, agent1, agent1parameters, agent2, agent2parameters, game, displayPrefix = None):
        self.board = games.getBoard(game)
        self.agent1 = Agent(agent1, agent1parameters, self.board)
        self.agent2 = Agent(agent2, agent2parameters, self.board)
        self.displayPrefix = displayPrefix

        # self.avgMoves = [0, 0]
        # self.avgSimulations = [0, 0]
        # self.n = 1
        # self.avgCnt = [0, 0, 0]

    # Return 1 if agent1 won
    # Return 0 if draw
    # Return -1 if agent2 won
    def playGame(self, displayState = True):
        gameState = self.board.start()
        agent1Turn = True
        turn = 0

        self.agent1.initGame()
        self.agent2.initGame()

        if displayState:
            self.board.display(gameState)

        while not self.board.isGameOver(gameState):
            if self.displayPrefix:
                print(self.displayPrefix + ' Turn {0}'.format(turn), end='\u001b[0K\r')
            turn += 1
            if displayState:
                print('{0}\'s turn'.format(self.agent1.agentType if agent1Turn else self.agent2.agentType))
            gameState = self.agent1.makeMove(gameState) if agent1Turn else self.agent2.makeMove(gameState)
            agent1Turn = not agent1Turn
            if displayState:
                self.board.display(gameState)
            
        if self.board.winner(gameState) == -1:
            return 0
        
        # self.updateStats()
        return -1 if agent1Turn else 1

    # def updateStats(self):
    #     self.avgMoves[0] += (self.agent1.moves - self.avgMoves[0])/self.n
    #     self.avgSimulations[0] += (self.agent1.simulations - self.avgSimulations[0])/self.n
    #     self.avgMoves[1] += (self.agent2.moves - self.avgMoves[1])/self.n
    #     self.avgSimulations[1] += (self.agent2.simulations - self.avgSimulations[1])/self.n
    #     self.avgCnt[0] += (self.agent1.tuner.gen - self.avgCnt[0])/self.n
    #     self.avgCnt[1] += (self.agent1.tuner.eval - self.avgCnt[1])/self.n
    #     self.avgCnt[2] += (self.agent1.tuner.exp - self.avgCnt[2])/self.n
    #     self.n += 1
