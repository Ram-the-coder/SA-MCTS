from game import Game
import agents.agentsList as agentsList
from games.gamesList import benchmarkList as games
from math import inf
import os
import threading

# Return 1 if agent1 wins, 0 if draw, -1 if agent2 wins
def runGame(agent1, agent2, game, parameters, displayPrefix):
    gameInstance = Game(agent1, parameters, agent2, parameters, game, displayPrefix)
    winner = gameInstance.playGame(displayState=False)
    return winner

threadLock = threading.Lock()

class myThread(threading.Thread):
    def __init__(self, agent1, agent2, game, parameters, displayPrefix, stats):
        threading.Thread.__init__(self)
        self.agent1 = agent1
        self.agent2 = agent2
        self.parameters = parameters
        self.game = game
        self.displayPrefix = displayPrefix
        self.stats = stats

    def run(self):
        winner = runGame(self.agent1, self.agent2, self.game, self. parameters, self.displayPrefix)    
        threadLock.acquire()
        if winner == 1:
            self.stats[0] += 1
        elif winner == -1:
            self.stats[1] += 1
        else:
            self.stats[2] += 1
        threadLock.release()

NUMBER_OF_GAMES = 10

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

os.system('cls')
agents = agentsList.benchmarkList

for game in games:
    print('\nGame:', game)
    for i in range(len(agents)):
        agent1 = agentsList.mcts
        agent2 = agents[i]
        if agent2 == agentsList.mcts:
            continue

        print('Running:', agent1, 'vs', agent2)
        threads = []
        stats = [0, 0, 0] #[agent1Wins, agent2Wins, draws]
        for k in range(NUMBER_OF_GAMES):
            displayPrefix = 'Game {0}/{1}'.format(k+1, NUMBER_OF_GAMES)
            thread = myThread(agent1, agent2, game, parameters, displayPrefix, stats)
            thread.start()
            threads.append(thread)

        for k in range(NUMBER_OF_GAMES):
            displayPrefix = 'Game {0}/{1}'.format(k+1, NUMBER_OF_GAMES)
            thread = myThread(agent2, agent1, game, parameters, displayPrefix, stats)
            thread.start()
            threads.append(thread)
        
        for thread in threads:
            thread.join()

        print('Result: {0}: {1}% {2}: {3}% Draws: {4}%'.format(agent1, (stats[0]*50)/NUMBER_OF_GAMES, agent2, (stats[1]*50)/NUMBER_OF_GAMES, (stats[2]*50)/NUMBER_OF_GAMES))