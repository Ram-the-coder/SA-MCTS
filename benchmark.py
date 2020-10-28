from game import Game
from agents.agentsList import benchmarkList as agents
import agents.agentsList as agentsList
from games.gamesList import benchmarkList as games
from math import inf
import os

#################### CONSTANTS ####################
# HALF_NUMBER_OF_GAMES_PER_PAIR = 5

parameters = [{
    'name': 'C', # MCTS Exploration Constant
    'isDiscreteDomain': True,
    'lowerBound': 0, # For continuous domain
    'upperBound': 1, # For continuous domain
    'domain': [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9], # For discrete domain
    'default': 0.2
}, {
    'name': 'T', # Min number visits before selection and expansion is performed on a node
    'isDiscreteDomain': True,
    'lowerBound': 0, # For continuous domain
    'upperBound': 200, # For continuous domain
    'domain': [0, 5, 10, 20, 30, 40, 50, 100, 200, inf], # For discrete domain
    'default': 0
}, {
    'name': 'VO', # Used in mcts selection phase
    'isDiscreteDomain': True,
    'lowerBound': 0, # For continuous domain
    'upperBound': 0.025, # For continuous domain
    'domain': [0.001, 0.005, 0.01, 0.015, 0.02, 0.025], # For discrete domain
    'default': 0.01
}]

#################### Methods ####################
def benchmarkAll(HALF_NUMBER_OF_GAMES_PER_PAIR):
    for game in games:
        print('----------------------------------------\nGame:', game)
        for i in range(len(agents)):
            agent1 = agentsList.mcts
            agent2 = agents[i]
            if agent2 == agentsList.mcts:
                continue
            wins1 = 0
            wins2 = 0
            draws = 0
            print('Running:', agent1, 'vs', agent2)
            for k in range(HALF_NUMBER_OF_GAMES_PER_PAIR):
                displayPrefix = 'Game {0}/{1}'.format(k+1, HALF_NUMBER_OF_GAMES_PER_PAIR)
                gameInstance = Game(agent1, parameters, agent2, parameters, game, displayPrefix)
                winner = gameInstance.playGame(displayState=False)
                if winner == 1:
                    wins1 += 1
                elif winner == -1:
                    wins2 += 1
                else:
                    draws += 1

            print('Running:', agent2, 'vs', agent1)
            for k in range(HALF_NUMBER_OF_GAMES_PER_PAIR):
                displayPrefix = 'Game {0}/{1}'.format(k+1, HALF_NUMBER_OF_GAMES_PER_PAIR)
                gameInstance = Game(agent2, parameters, agent1, parameters, game, displayPrefix)
                winner = gameInstance.playGame(displayState=False)
                if winner == 1:
                    wins2 += 1
                elif winner == -1:
                    wins1 += 1
                else:
                    draws += 1
            print('Result: {0}: {1}/{5} {2}: {3}/{5} Draws: {4}/{5}\n'.format(agent1, wins1, agent2, wins2, draws, HALF_NUMBER_OF_GAMES_PER_PAIR*2))

def singleTunerBenchmark(HALF_NUMBER_OF_GAMES_PER_PAIR):
    print('Choose the allocation strategy that you want to benchmark:')
    print('1. Naive Monte Carlo (NMC)')
    print('2. Evolutionary Algorithm (EA)')
    print('3. Covariance Matrix Adaptation Evolution Strategy (CMA-ES)')
    print('4. N-Tuple Bandit Evolutionary Algorithm (NTBEA)')

    choice = int(input())
    agent1 = agentsList.mcts
    agent2 = agentsList.nmc

    if choice == 1:
        agent2 = agentsList.nmc
    elif choice == 2:
        agent2 = agentsList.ea
    elif choice == 3:
        agent2 = agentsList.cmaes
    elif choice == 4:
        agent2 = agentsList.ntbea

    print('Chosen allocation strategy:', agent2)
     
    for game in games:
        print('----------------------------------------\nGame:', game)

        wins1 = 0
        wins2 = 0
        draws = 0
        
        print('Running:', agent1, 'vs', agent2)
        for k in range(HALF_NUMBER_OF_GAMES_PER_PAIR):
            displayPrefix = 'Game {0}/{1}'.format(k+1, HALF_NUMBER_OF_GAMES_PER_PAIR)
            gameInstance = Game(agent1, parameters, agent2, parameters, game, displayPrefix)
            winner = gameInstance.playGame(displayState=False)
            if winner == 1:
                wins1 += 1
            elif winner == -1:
                wins2 += 1
            else:
                draws += 1

        print('Running:', agent2, 'vs', agent1)
        for k in range(HALF_NUMBER_OF_GAMES_PER_PAIR):
            displayPrefix = 'Game {0}/{1}'.format(k+1, HALF_NUMBER_OF_GAMES_PER_PAIR)
            gameInstance = Game(agent2, parameters, agent1, parameters, game, displayPrefix)
            winner = gameInstance.playGame(displayState=False)
            if winner == 1:
                wins2 += 1
            elif winner == -1:
                wins1 += 1
            else:
                draws += 1
        print('Result: {0}: {1}/{5} {2}: {3}/{5} Draws: {4}/{5}\n'.format(agent1, wins1, agent2, wins2, draws, HALF_NUMBER_OF_GAMES_PER_PAIR*2))



#################### Main Method ####################
def main():
    os.system('cls')
    
    numberOfGames = int(input('Enter the number of games to benchmark against:'))
    HALF_NUMBER_OF_GAMES_PER_PAIR = numberOfGames // 2

    print('1. Benchmark all online allocation strategies')
    print('2. Benchmark a single allocation strategies')
    choice = int(input('Choose:'))
    
    if(choice == 1):
        benchmarkAll(HALF_NUMBER_OF_GAMES_PER_PAIR)
    else:
        singleTunerBenchmark(HALF_NUMBER_OF_GAMES_PER_PAIR)

#################### Call to Main Method ####################
if __name__ == '__main__':
    main()