from agents.tuners.tunerMeta import TunerMeta
from random import random
from copy import deepcopy
from math import sqrt, log


class MultiArmedBandit:
    # Uses UCB for choosing
    # Uses sample average method for update

    def __init__(self, **kwargs):
        self.arms = []
        self.c = 1 # Exploration constant
        self.totalSelections = 1

    def choose(self):
        # bestExpectedReward, bestArmIndex = max([(self.arms[i]['expectedReward'], i) for i in range(len(self.arms))])
        bestScore, bestArmIndex = max([(self.calcUCB(self.arms[i]), i) for i in range(len(self.arms))])
        self.totalSelections += 1
        return (deepcopy(self.arms[bestArmIndex]['armDetails']), bestArmIndex)

    # Expects a reward in the range [0, 1]
    def update(self, armIndex, reward):
        if armIndex >= len(self.arms):
            raise Exception('bestArmIndex out of bounds', {'armIndex': armIndex, 'num arms': len(self.arms)})            
        self.arms[armIndex]['n'] += 1 
        self.arms[armIndex]['expectedReward'] += (reward - self.arms[armIndex]['expectedReward']) / self.arms[armIndex]['n']
        

    def addArm(self, armDetails):
        self.arms.append({
            'armDetails': armDetails,
            'expectedReward': 0,
            'n': 1
        })

    def calcUCB(self, arm):
        return arm['expectedReward'] + self.c * sqrt(log(self.totalSelections) / arm['n'])
        

EXPLORATION_PHASE = 'exploration'
EXPLOITATION_PHASE = 'exploitation'

class NMCParameterTuning(TunerMeta):
    def __init__(self, parameters, **kwargs):
        numParams = len(parameters)
        self.parametersMAB = [MultiArmedBandit() for i in range(0, numParams)]
        self.chosenParameterValueIndices = [None]*numParams
        self.comboMAB = MultiArmedBandit()
        self.chosenComboIndex = None
        self.phaseSelectionPolicy = kwargs.get('phaseSelectionPolicy', 0.75)
        
        for i in range(numParams):
            if not parameters[i]['isDiscreteDomain']:
                raise Exception(parameters[i], 'this parameter passes to NMC does not have a discrete domain')
            for val in parameters[i]['domain']:
                self.parametersMAB[i].addArm({'name': parameters[i]['name'], 'value': val})
            
            
    def getParams(self):
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

    # def addArmsForParameters(self, i, *args):
    #     for val in args:
    #         self.parametersMAB[i].addArm(val)

    def updateStatistics(self, reward):
        self.comboMAB.update(self.chosenComboIndex, reward)
        self.chosenComboIndex = None
        for i in range(0, len(self.chosenParameterValueIndices)):
            self.parametersMAB[i].update(self.chosenParameterValueIndices[i], reward)
            self.chosenParameterValueIndices[i] = None