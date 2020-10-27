from agents.tuners.tunerMeta import TunerMeta
from random import choice, random
from heapq import nlargest
from copy import deepcopy


class EA:

    def __init__(self, parameters):
        self.Genomes = list()
        self.fitness = list()
        self.parameters = parameters

    def uniformCrossover(self, individual1, individual2):
        child = list()
        for i in range(len(individual1)):
            if random() < 0.5:
                child.append(individual1[i])
            else:
                child.append(individual2[i])
        return child

    def singleRandomMutation(self, individual):

        index = int(random()*len(self.parameters))
        child = list(individual)
        new_gene = choice(self.parameters[index]['domain'])
        child[index] = new_gene
        return child

    def generateRandomIndividual(self):

        individual = list()
        for param in self.parameters:
            individual.append(choice(param['domain']))
        key = tuple(individual)
        return key

    def generateIndividual(self, best_M_Genes, p_cross):

        if random() < p_cross:
            p1 = choice(best_M_Genes)
            p2 = choice(best_M_Genes)
            return self.uniformCrossover(p1, p2)
        else:
            p = choice(best_M_Genes)
            return self.singleRandomMutation(p)


class EAParameterTuning(TunerMeta):
    def __init__(self, parameters, **kwargs):

        max_population = 1
        for param in parameters:
            max_population *= len(param['domain'])
        self.populationSize = min(
            max_population, kwargs.get('populationSize', 5))
        self.p_cross = kwargs.get('p_cross', 0.5)
        self.mu = min(max_population, kwargs.get(
            'mu', int(self.populationSize/2)))
        self.current_individual_index = 0
        self.parameters = parameters
        self.ea = EA(self.parameters)
        
        for _ in range(self.populationSize):
            key = self.ea.generateRandomIndividual()
            self.ea.Genomes.append(key)
            self.ea.fitness.append(None)

    def getParams(self):
        selected_Genome = None
        # current generation
        if self.current_individual_index < self.populationSize:
            selected_Genome = self.ea.Genomes[self.current_individual_index]
        else:
            # next generation
            mu_best = nlargest(self.mu, zip(
                self.ea.Genomes, self.ea.fitness), key=lambda k: k[1])
            mu_best = [genome for genome, fitness in mu_best]
            self.ea.Genomes = mu_best
            for _ in range(self.populationSize-self.mu):
                self.ea.Genomes.append(
                    self.ea.generateIndividual(mu_best, self.p_cross))
            self.current_individual_index = 0
            selected_Genome = self.ea.Genomes[self.current_individual_index]
        individual = list()

        for i, param in enumerate(self.parameters):
            individual.append(
                {'name': param['name'], 'value': selected_Genome[i]})

        return tuple(individual)

    def updateStatistics(self, reward):
        self.ea.fitness[self.current_individual_index] = reward
        self.current_individual_index += 1