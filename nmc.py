from game_state import Board
import mcts
from random import random
from copy import deepcopy


class MultiArmedBandit:
    # Uses optimistic initial values
    # Uses sample average method for update
    def __init__(self, **kwargs):
        self.arms = []

    def choose(self):
        bestExpectedReward, bestArmIndex = max([(self.arms[i]['expectedReward'], i) for i in range(0, len(self.arms))])
        return (deepcopy(self.arms[bestArmIndex]['armDetails']), bestArmIndex)

    # Expects a reward in the range [0, 1]
    # The optimistic initial value is set to 2 assuming reward range of [0, 1]
    def update(self, bestArmIndex, reward):
        if bestArmIndex >= len(self.arms):
            raise Exception('bestArmIndex out of bounds', bestArmIndex, len(self.arms))            
        self.arms[bestArmIndex]['n'] += 1 
        self.arms[bestArmIndex]['expectedReward'] += (reward - self.arms[bestArmIndex]['expectedReward']) / self.arms[bestArmIndex]['n']
        

    def addArm(self, armDetails):
        self.arms.append({
            'armDetails': armDetails,
            'expectedReward': 2,
            'n': 1
        })
        

EXPLORATION_PHASE = 'exploration'
EXPLOITATION_PHASE = 'exploitation'

class NMCParameterTuning:
    def __init__(self, numParams, **kwargs):
        self.board = Board()
        self.mcts = mcts.MonteCarlo(self.board)
        self.parametersMAB = [MultiArmedBandit() for i in range(0, numParams)]
        self.chosenParameterValueIndices = [None]*numParams
        self.comboMAB = MultiArmedBandit()
        self.chosenComboIndex = None
        self.phaseSelectionPolicy = kwargs.get('phaseSelectionPolicy', 0.1)

    def play(self):
        isAiTurn = False
        curStateNode = mcts.Node(self.board.start(), 0)

        while not self.board.isGameOver(curStateNode.state):
            self.board.display(curStateNode.state)
            isAiTurn = not isAiTurn

            if isAiTurn:
                parameters = self.chooseParameterValues()
                curStateNode, reward = self.mcts.play(curStateNode)
                self.updateStatistics(parameters, reward)
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
        
        print('Parameters at the end of play:', self.comboMAB.choose())

    def chooseParameterValues(self):
        phase = self.choosePhase() if len(self.comboMAB.arms) > 0 else EXPLORATION_PHASE
        parameters = [None]*len(self.parametersMAB) # Initialize
        if phase == EXPLORATION_PHASE:
            for i in range(0, len(self.parametersMAB)):
                parameters[i], self.chosenParameterValueIndices[i] = self.parametersMAB[i].choose()
            parameters = tuple(parameters)
            self.comboMAB.addArm((deepcopy(parameters), deepcopy(self.chosenParameterValueIndices)))
            self.chosenComboIndex = len(self.comboMAB.arms) - 1
        
        elif phase == EXPLOITATION_PHASE:
            (parameters, self.chosenParameterValueIndices), self.chosenComboIndex = self.comboMAB.choose()

        return parameters
    
    def choosePhase(self):
        val = random()
        return EXPLORATION_PHASE if val <= self.phaseSelectionPolicy else EXPLOITATION_PHASE

    def addArmsForParameters(self, i, *args):
        for val in args:
            self.parametersMAB[i].addArm(val)

    def updateStatistics(self, parameters, reward):
        self.comboMAB.update(self.chosenComboIndex, reward)
        self.chosenComboIndex = None
        for i in range(0, len(self.chosenParameterValueIndices)):
            self.parametersMAB[i].update(self.chosenParameterValueIndices[i], reward)
            self.chosenParameterValueIndices[i] = None