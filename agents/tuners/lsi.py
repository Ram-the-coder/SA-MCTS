from agents.tuners.tunerMeta import TunerMeta
from random import choice, choices
from copy import deepcopy
from math import log2, ceil
from heapq import nlargest
from numpy import zeros

BUILD_SIDE_INFO_PHASE = 0
GENERATE_PHASE = 1
EVALUATE_INIT_PHASE = 2
EVALUATE_PHASE = 3
EXPLOIT_PHASE = 4

class LSIParameterTuning(TunerMeta):

    def __init__(self, ng, ne, k, parameters):
        if ne < (k * log2(k)):
            print('ne', ne, 'k', k)
            raise Exception('High value of k compared to ne')
        self.ng = ng
        self.ne = ne
        self.candidatesToEval = k
        self.phase = BUILD_SIDE_INFO_PHASE
        
        self.parameters = parameters
        
        self.R = [[0]*len(param['domain']) for param in parameters] # Distribution function
        self.Rn = [[1]*len(param['domain']) for param in parameters] # number of times R[i][j] has been updated
        self.domainSize = sum([len(param['domain']) for param in parameters])

        self.itr = 0

        # INITIALISE VARS FOR SIDE INFO PHASE
        self.x = ng // self.domainSize
        self.i = 0
        self.j = 0

        # INITIALIZE VARS FOR GENERATE PHASE
        self.C = []

        # Remove later
        # self.gen = 0
        # self.eval = 0
        # self.exp = 0


    def getParams(self):
        if self.phase == BUILD_SIDE_INFO_PHASE:
            return self.randomlyExtend(self.parameters[self.i]['domain'][self.j], self.i)

        if self.phase == GENERATE_PHASE:
            self.generate() 

        if self.phase == EVALUATE_INIT_PHASE:
            self.Ci = self.C
            self.ri = [0]*len(self.Ci)
            self.ni = [1]*len(self.Ci)
            self.i = 0
            self.n = ceil(log2(len(self.C)))
            self.itr = 0
            self.x = int(self.ne // (len(self.Ci) * ceil(log2(len(self.C)))))
            self.paramComboIdx = 0
            self.phase += 1

        if self.phase == EVALUATE_PHASE:
            return self.Ci[self.paramComboIdx]

        if self.phase == EXPLOIT_PHASE:
            # self.exp += 1 # Remove later
            return self.Ci[0]
    
    def updateStatistics(self, reward):
        if self.phase == BUILD_SIDE_INFO_PHASE:
            # self.gen += 1 # Remove later
            self.R[self.i][self.j] += (reward - self.R[self.i][self.j]) / self.Rn[self.i][self.j]
            self.Rn[self.i][self.j] += 1

            self.j += 1

            if self.j == len(self.parameters[self.i]['domain']):
                self.j = 0
                self.i += 1

                if self.i == len(self.parameters):
                    self.i = 0
                    self.itr += 1

                    if self.itr == self.x:
                        self.itr = 0
                        self.phase += 1
        
        elif self.phase == EVALUATE_PHASE:
            # self.eval += 1 # Remove later
            self.ri[self.paramComboIdx] += (reward - self.ri[self.paramComboIdx]) / self.ni[self.paramComboIdx]
            self.ni[self.paramComboIdx] += 1

            self.paramComboIdx += 1

            if self.paramComboIdx == len(self.Ci):
                self.paramComboIdx = 0
                self.itr += 1

                if self.itr == self.x:
                    self.itr = 0
                    self.Ci = nlargest(ceil(len(self.Ci)/2),  zip(self.Ci, self.ri), key=lambda k: k[1])
                    self.Ci = [paramCombo for paramCombo, expectedReward in self.Ci]
                    self.i += 1
                    if self.i == self.n:
                        self.phase += 1
                        if len(self.Ci) != 1:
                            raise Exception('Length of self.Ci should be 1', self.Ci)
                    else:
                        self.x = self.ne // (len(self.Ci) * log2(len(self.C)))


    # Return a parameter combination tuple
    def randomlyExtend(self, paramVal, paramIdx):
        params = []
        for i in range(len(self.parameters)):
            if i == paramIdx:
                params.append({
                    'name': self.parameters[i]['name'],
                    'value': paramVal
                })
            else:
                params.append({
                    'name': self.parameters[i]['name'],
                    'value': choice(self.parameters[i]['domain'])
                })

        return tuple(params)


    def generate(self):
        shape = [len(param['domain']) for param in self.parameters]
        exisistenceDP = zeros(shape, dtype='b')
        for _ in range(self.candidatesToEval):
            params = []
            indexes = []
            for i in range(len(self.parameters)):
                idx = choices(list(range(len(self.parameters[i]['domain']))), weights=self.R[i], k=1)[0]
                indexes.append(idx)
                params.append({
                    'name': self.parameters[i]['name'],
                    'value': self.parameters[i]['domain'][idx]
                })

            if exisistenceDP[tuple(indexes)]:
                continue
            exisistenceDP[tuple(indexes)] = 1
            params = tuple(params)
            self.C.append(params)
        self.phase += 1
        