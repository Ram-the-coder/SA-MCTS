from game import Game
from agents.agentsList import benchmarkList as agents
import agents.agentsList as agentsList
import params
from games.gamesList import benchmarkList as games
import os


#################### Global variables ####################
sp_online_params = {
    'tuning': [params.C, params.eps],
    'constant': [params.K_UCT, params.Ref, params.VO, params.T]
}

sp_offline_params = {
    'tuning': [],
    'constant': [params.C, params.eps, params.K_UCT, params.Ref, params.VO, params.T]
}

ap_online_2params = {
    'tuning': [params.K_GRAVE, params.Ref],
    'constant': [params.C, params.eps, params.VO, params.T]
}

ap_online_4params = {
    'tuning': [params.K_GRAVE, params.Ref, params.C, params.eps],
    'constant': [params.VO, params.T]
}

ap_online_6params = {
    'tuning': [params.K_GRAVE, params.Ref, params.C, params.eps, params.VO, params.T],
    'constant': []
}

ap_offline_params = {
    'tuning': [],
    'constant': [params.C, params.eps, params.K_GRAVE, params.Ref, params.VO, params.T]
}

#################### Methods ####################
def getParameters():
    print('Choose the agent type you want to benchmark:')
    print('1. SP Agent')
    print('2. AP Agent with 2 parameters')
    print('3. AP Agent with 4 parameters')
    print('4. AP Agent with 6 parameters')
    choice = int(input())
    if choice == 1:
        return sp_online_params, sp_offline_params
    if choice == 2:
        return ap_online_2params, ap_offline_params
    if choice == 3:
        return ap_online_4params, ap_offline_params
    if choice == 4:
        return ap_online_6params, ap_offline_params
    else
        print('invalid agent choice')

def benchmarkAgent(HALF_NUMBER_OF_GAMES_PER_PAIR, agent1params, agent2params):
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
                gameInstance = Game(agent1, agent1params, agent2, agent2params, game, displayPrefix)
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
                gameInstance = Game(agent2, agent2params, agent1, agent1params, game, displayPrefix)
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
    print('2. Linear Side Information (LSI)')
    print('3. Evolutionary Algorithm (EA)')
    print('4. N-Tuple Bandit Evolutionary Algorithm (NTBEA)')
    print('5. Covariance Matrix Adaptation Evolution Strategy (CMA-ES)')

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

    agent1params, agent2params = getParameters()
     
    for game in games:
        print('----------------------------------------\nGame:', game)

        wins1 = 0
        wins2 = 0
        draws = 0
        
        print('Running:', agent1, 'vs', agent2)
        for k in range(HALF_NUMBER_OF_GAMES_PER_PAIR):
            displayPrefix = 'Game {0}/{1}'.format(k+1, HALF_NUMBER_OF_GAMES_PER_PAIR)
            gameInstance = Game(agent1, agent1params, agent2, agent2params, game, displayPrefix)
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
            gameInstance = Game(agent2, agent2params, agent1, agent1params, game, displayPrefix)
            winner = gameInstance.playGame(displayState=False)
            if winner == 1:
                wins2 += 1
            elif winner == -1:
                wins1 += 1
            else:
                draws += 1
        print('Result: {0}: {1}/{5} {2}: {3}/{5} Draws: {4}/{5}\n'.format(agent1, wins1, agent2, wins2, draws, HALF_NUMBER_OF_GAMES_PER_PAIR*2))


def benchmarkAll(HALF_NUMBER_OF_GAMES_PER_PAIR):
    print('Benchmarking SP Agent')
    benchmarkAgent(HALF_NUMBER_OF_GAMES_PER_PAIR, sp_online_params, sp_offline_params)
    
    print('Benchmarking AP Agent tuning 2 parameters')
    benchmarkAgent(HALF_NUMBER_OF_GAMES_PER_PAIR, ap_online_2params, ap_offline_params)

    print('Benchmarking AP Agent tuning 4 parameters')
    benchmarkAgent(HALF_NUMBER_OF_GAMES_PER_PAIR, ap_online_4params, ap_offline_params)

    print('Benchmarking AP Agent tuning 6 parameters')
    benchmarkAgent(HALF_NUMBER_OF_GAMES_PER_PAIR, ap_online_6params, ap_offline_params)

#################### Main Method ####################
def main():
    os.system('cls')
    
    numberOfGames = int(input('Enter the number of games to benchmark against:'))
    HALF_NUMBER_OF_GAMES_PER_PAIR = numberOfGames // 2

    print('1. Benchmark all')
    print('2. Benchmark a single agent with all online allocation strategies')
    print('3. Benchmark a single agent type and allocation strategy')
    choice = int(input('Choose:'))
    
    if choice == 1:
        benchmarkAll(HALF_NUMBER_OF_GAMES_PER_PAIR)
    if choice == 2:
        agent1params, agent2params = getParameters()
        benchmarkAgent(HALF_NUMBER_OF_GAMES_PER_PAIR, agent1params, agent2params)
    else:
        singleTunerBenchmark(HALF_NUMBER_OF_GAMES_PER_PAIR)

#################### Call to Main Method ####################
if __name__ == '__main__':
    main()