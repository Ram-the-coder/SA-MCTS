import cma
from copy import deepcopy
from agents.tuners.tunerMeta import TunerMeta
import random

class cmaEs:
    def __init__(self,initParameterValues,initMean=[0.179]*5,initStdDev=0.3,fitnesPenalty=100):
       
        self.initParameterValues = deepcopy(initParameterValues)
        self.fitnessPenalty=fitnesPenalty
        self.es=cma.CMAEvolutionStrategy(initMean,initStdDev)
        


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

    def denormalizeIndividual(self,individual, params):
        for i in range(0, len(params)):
            lb = params[i]['lowerBound']
            ub = params[i]['upperBound']
            individual[i] = lb + individual[i] * (ub - lb)
        # print(individual)


class cmaEsParameterTuning(TunerMeta):
    def __init__(self, parameters, **kwargs):
        self.parameters=parameters
        # print(parameters)
        self.fitness=[]
        self.current_index=0
        initmean=[random.random() for i in range(len(self.parameters))]
        # print("initmean",initmean)
        self.cmaes=cmaEs(parameters,initmean)
        self.penalty=100
        self.es=self.cmaes.es
        self.generatedPopulation=self.es.ask()
        self.populationSize=len(self.generatedPopulation)
        self.fitness=[0]*self.populationSize
        self.stopped=False
        # print(self.generatedPopulation)
        
        
    def getParams(self):
        # selectedIndividual=None
        #### Current Generation
        if self.es.stop():
            selectedIndividual=self.es.result.xbest
            # print("xbest..........................")
            # print(selectedIndividual)
            self.stopped=True
        else:
            if self.current_index<self.populationSize:
                selectedIndividual=self.generatedPopulation[self.current_index]
                
            else:
                #### New Generation
                self.es.tell(self.generatedPopulation,self.fitness) #update fitness values to the distribution
                self.generatedPopulation=self.es.ask() #generate new population
                self.current_index=0
                selectedIndividual=self.generatedPopulation[self.current_index]
                self.populationSize=len(self.generatedPopulation)
                self.fitness=[0]*self.populationSize
                # selectedIndividual=self.es.result.xbest


        individual=[]
        self.cmaes.repairIndividual(selectedIndividual)
        self.cmaes.denormalizeIndividual(selectedIndividual,self.parameters)
        for i, param in enumerate(self.parameters): 
            individual.append(
                {'name': param['name'], 'value':selectedIndividual[i]})
        # print(individual)
        return tuple(individual)
        
    def updateStatistics(self,reward):
        if not self.stopped:
            self.fitness[self.current_index]=100-reward+self.cmaes.repairIndividual(self.generatedPopulation[self.current_index])
            self.current_index+=1
        return

        


