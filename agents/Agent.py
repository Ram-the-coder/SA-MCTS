from agents.mcts import MonteCarlo
import agents.agentsList as agentsList
from agents.tuners.nmc import NMCParameterTuning
from agents.tuners.ea import EAParameterTuning
from agents.tuners.cmaes import cmaEsParameterTuning
from agents.tuners.ea import EAParameterTuning 
from agents.tuners.lsi import LSIParameterTuning
from agents.tuners.ntbea import NTBEAParameterTuning 
import datetime

TIME_PER_MOVE = 1

class Agent:
    def __init__(self, agentType, agentParameters, board, debug):
        self.agentType = agentType
        self.agentParameters = agentParameters
        self.board = board
        self.debug = debug

    def initGame(self):
        self.tuner = self.getTunerInstance(self.agentType, self.agentParameters['tuning'], self.board.averageNumberOfMoves())
        self.mcts = MonteCarlo(self.board)    
        self.mcts.setParams([{'name': param['name'], 'value': param['default']} for param in self.agentParameters['constant']])
        self.mcts.setParams([{'name': param['name'], 'value': param['default']} for param in self.agentParameters['tuning']])

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
                    if self.debug:
                        print('Chosen params:', params)
            
            # Do 1 MCTS Simulation
            reward = self.mcts.simulate(gameState)

            # Update tuner statistics
            if self.tuner != None:
                self.tuner.updateStatistics(reward)

        # Print Stats
        if self.debug:
            print('\nMove - Expected win percentage found by MCTS simulation')
            for x in sorted(((100 * child.wins/(child.plays+1), child.wins, child.plays, str(child.move)) for child in self.mcts.root.children), reverse = True):
                print('{3} - {0}% - {1}/{2}'.format(*x))
            print()
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

    def getTunerInstance(self, agentType, agentParameters, numMoves):
        if agentType == agentsList.nmc:
            return NMCParameterTuning(agentParameters)
        if agentType == agentsList.ea:
            return EAParameterTuning(agentParameters)
        if agentType == agentsList.cmaes:
            return cmaEsParameterTuning(agentParameters)
        if agentType == agentsList.lsi:
            N = numMoves * 10000
            ng = int(N * 0.75)
            ne = N - ng
            k = 20 if len(agentParameters) <= 2 else 600
            # print(ng, ne, k)
            return LSIParameterTuning(ng, ne, k, agentParameters)
        if agentType == agentsList.ntbea:
            return NTBEAParameterTuning(P=agentParameters)

        return None  
