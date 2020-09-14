import cma
import mcts
from game_state import Board
import matplotlib.pyplot as plt
from copy import deepcopy

# TODO: Disable all termination criteria regarding
# the fitness function, so that the optimization continues
# even if the minimum tness is reached or if no signicant
# change in tness is observed. The motivation behind this
# choice is that the best parameter combination for MCTS
# might change over time, thus we want to keep exploring
# the search space. 

class CmaesParameterTuning:
    def __init__(self, initParameterValues, initStdDev, fitnessPenalty, parameterRanges):
        initParameterValues = deepcopy(initParameterValues)
        parameterRanges = deepcopy(parameterRanges)
        print(initParameterValues, initStdDev)
        self.es = cma.CMAEvolutionStrategy(initParameterValues, initStdDev)
        self.fitnessPenalty = fitnessPenalty
        self.board = Board()
        self.mcts = mcts.MonteCarlo(self.board)
        self.parameterRanges = parameterRanges

    def play(self):
        isAiTurn = False
        curStateNode = mcts.Node(self.board.start(), 0)

        while not self.board.isGameOver(curStateNode.state):

            self.board.display(curStateNode.state)
            print()
            isAiTurn = not isAiTurn

            if isAiTurn:
                if not self.es.stop():
                    # Minima not found yet
                    offsprings = self.es.ask()
                    offspringFitness = []
                    for parameterCombo in offsprings:
                        offspringFitness.append(self.computeFitness(parameterCombo, curStateNode))
                    self.es.tell(offsprings, offspringFitness)

                    
                    bestParams = self.es.result.xbest
                    self.repairIndividual(bestParams)
                    self.denormalizeIndividual(bestParams)
                    self.mcts.setParams(tuple(bestParams))

                curStateNode, reward = self.mcts.play(curStateNode)

            else:
                if len(curStateNode.children) == 0:
                    self.mcts.expand(curStateNode)
                inputMove = int(input('Your move: '))
                nextNode = None
                for child in curStateNode.children:
                    if child.move == inputMove:
                        nextNode = child
                        break
                curStateNode = nextNode

    
    def computeFitness(self, params, curStateNode):
        params = deepcopy(params)
        penalty = self.repairIndividual(params)
        self.denormalizeIndividual(params)
        self.mcts.setParams(tuple(params))
        curStateNode, reward = self.mcts.play(curStateNode)
        return (100 - reward + penalty)

    def repairIndividual(self, params):
        penalty = 0
        for i in range(0, len(params)):
            if params[i] < 0:
                penalty += params[i] ** 2
                params[i] = 0
            elif params[i] > 1:
                penalty += (params[i] - 1) ** 2
                params[i] = 1                
                
        penalty = self.fitnessPenalty * (penalty ** 0.5)
        return penalty

    def denormalizeIndividual(self, params):
        for i in range(0, len(params)):
            lb = self.parameterRanges[i]['min']
            ub = self.parameterRanges[i]['max']
            params[i] = lb + params[i] * (ub - lb)