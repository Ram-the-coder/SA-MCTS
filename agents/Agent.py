from agents.mcts import MonteCarlo
import agents.agentsList as agentsList
from agents.tuners.nmc import NMCParameterTuning
import datetime

TIME_PER_MOVE = 1

class Agent:
    def __init__(self, agentType, agentParameters, board):
        self.agentType = agentType
        self.board = board
        self.tuner = self.getTunerInstance(agentType, agentParameters)
        self.mcts = MonteCarlo(self.board)    
        self.mcts.setParams([{'name': param['name'], 'value': param['default']} for param in agentParameters])


    def makeMove(self, gameState):
        if self.board.isGameOver(gameState):
            return gameState

        start = datetime.datetime.utcnow()
        self.mcts.setRootNodeState(gameState)

        # Simulate
        while datetime.datetime.utcnow() - start < datetime.timedelta(seconds = TIME_PER_MOVE):
            # Get params
            if self.tuner != None:
                params = self.tuner.getParams()
                if params and len(params) != 0:
                    self.mcts.setParams(params)
            
            # Do 1 MCTS Simulation
            reward = self.mcts.simulate(gameState)

            # Update tuner statistics
            if self.tuner != None:
                self.tuner.updateStatistics(reward)

        # Print Stats
        # for x in sorted(((100 * child.wins/(child.plays+1), child.wins, child.plays, child.move) for child in self.mcts.root.children), reverse = True):
        #     print('{3} - {0}% - {1}/{2}'.format(*x))

        # Get best move
        bestChild = 0
        bestScore = self.mcts.root.children[0].wins/(self.mcts.root.children[0].plays+1)
        maxPlays = self.mcts.root.children[0].plays

        for i in range(1, len(self.mcts.root.children)):
            score = self.mcts.root.children[i].wins/(self.mcts.root.children[i].plays+1)
            if score > bestScore:
                bestScore = score
                bestChild = i

        # Return next state
        return self.mcts.root.children[bestChild].state

    def getTunerInstance(self, agentType, agentParameters):
        if agentType == agentsList.nmc:
            return NMCParameterTuning(agentParameters)
    
        return None

        
        

