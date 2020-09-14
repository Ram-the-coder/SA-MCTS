from agents.Agent import Agent
from games import games

class Game:
    def __init__(self, agent1, agent1parameters, agent2, agent2parameters, game):
        self.board = games.getBoard(game)
        self.agent1 = Agent(agent1, agent1parameters, self.board)
        self.agent2 = Agent(agent2, agent2parameters, self.board)


    # Return 1 if agent1 won
    # Return 0 if draw
    # Return -1 if agent2 won
    def playGame(self, displayState = True):
        gameState = self.board.start()
        agent1Turn = True

        if displayState:
            self.board.display(gameState)

        while not self.board.isGameOver(gameState):
            if displayState:
                print('{0}\'s turn'.format(self.agent1.agentType if agent1Turn else self.agent2.agentType))
            gameState = self.agent1.makeMove(gameState) if agent1Turn else self.agent2.makeMove(gameState)
            agent1Turn = not agent1Turn
            if displayState:
                self.board.display(gameState)
            
        if self.board.winner(gameState) == -1:
            return 0
        
        return -1 if agent1Turn else 1
