from agents.tuners.tunerMeta import TunerMeta
from itertools import product, combinations
from copy import deepcopy
from math import sqrt, log
from .ea import EA


class LModel:

    def __init__(self, L, P):

        self.maxL = len(P)
        self.L = L
        self.parameters = dict()
        P = deepcopy(P)
        for i, kv in enumerate(P):
            name = kv.pop('name')
            self.parameters[name] = kv
            self.parameters[name]['index'] = i

        self.LUT = dict()
        self.LUT_base_t = dict()
        for l in self.L:
            combination = combinations(sorted(self.parameters.keys()), l)
            for combi in combination:
                self.LUT_base_t[combi] = {'n': 1}

        self.totalSelections = 1

    def update(self, arm_key, reward):

        for l in self.L:
            required_param_names = combinations(
                sorted(self.parameters.keys()), l)

            for p_names in required_param_names:

                self.LUT_base_t[p_names]['n'] += 1
                key = [-1]*self.maxL

                for p_name in p_names:
                    index = self.parameters[p_name]['index']
                    key[index] = arm_key[index]
                if tuple(key) not in self.LUT:
                    self.LUT[tuple(key)] = {
                        'n': 1,
                        'expectedReward': reward
                    }
                else:
                    self.LUT[tuple(key)]['n'] += 1
                    self.LUT[tuple(key)]['expectedReward'] += reward

    def calcUCB(self, p_bar, c=1):
        UCB = 0
        count = 0

        for t in self.LUT_base_t.keys():
            key = [-1]*self.maxL
            for name in t:
                index = self.parameters[name]['index']
                key[index] = p_bar[index]

            entry = self.LUT.get(tuple(key), None)
            if entry == None:
                continue
            UCB += (entry['expectedReward']/entry['n']) + c * \
                sqrt(log(self.LUT_base_t[t]['n'])/entry['n'])
            count += 1

        if count > 0:
            return UCB/count
        return 0


class NTBEAParameterTuning(TunerMeta):

    def __init__(self, **kwargs):
        self.x = kwargs.get('x', 5)
        self.P = kwargs.get('P', list())
        self.L = kwargs.get('L', [1, len(self.P)])
        self.c = kwargs.get('c', 1)
        self.LModel = LModel(
            L=self.L,
            P=self.P
        )
        self.ea = EA(self.P)
        self.p_bar = None

    def getParams(self):
        if self.p_bar == None:
            selected_Genome = self.ea.generateRandomIndividual()
            self.p_bar = selected_Genome
        else:
            N = list()
            for _ in range(self.x):
                N.append(self.ea.singleRandomMutation(self.p_bar))
            selected_Genome = max(N, key=self.LModel.calcUCB)
            self.p_bar = selected_Genome

        individual = list()
        for i, param in enumerate(self.ea.parameters):
            individual.append(
                {'name': param['name'], 'value': selected_Genome[i]})

        return tuple(individual)

    def updateStatistics(self, reward):
        self.LModel.update(
            arm_key=self.p_bar,
            reward=reward
        )