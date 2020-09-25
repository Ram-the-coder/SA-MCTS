from game import Game
from agents.agentsList import benchmarkList as agents
from games.gamesList import benchmarkList as games
import os

NUMBER_OF_GAMES = 5

parameters = [{
    'name': 'C',
    'isDiscreteDomain': True,
    'lowerBound': None, # For continuous domain
    'upperBound': None, # For continuous domain
    'domain': [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9], # For discrete domain
    'default': 0.7
}]

os.system('cls')

for game in games:
    print('\nGame:', game)
    for i in range(len(agents)):
        for j in range(i+1, len(agents)):
            agent1 = agents[i]
            agent2 = agents[j]
            wins1 = 0
            wins2 = 0
            draws = 0
            print('Running:', agent1, 'vs', agent2)
            for i in range(NUMBER_OF_GAMES):
                displayPrefix = 'Game {0}/{1}'.format(i+1, NUMBER_OF_GAMES)
                gameInstance = Game(agent1, parameters, agent2, parameters, game, displayPrefix)
                winner = gameInstance.playGame(displayState=False)
                if winner == 1:
                    wins1 += 1
                elif winner == -1:
                    wins2 += 1
                else:
                    draws += 1

            print('Running:', agent2, 'vs', agent1)
            for i in range(NUMBER_OF_GAMES):
                displayPrefix = 'Game {0}/{1}'.format(i+1, NUMBER_OF_GAMES)
                gameInstance = Game(agent2, parameters, agent1, parameters, game, displayPrefix)
                winner = gameInstance.playGame(displayState=False)
                if winner == 1:
                    wins2 += 1
                elif winner == -1:
                    wins1 += 1
                else:
                    draws += 1
            print('Result: {0}: {1}% {2}: {3}% Draws: {4}%'.format(agent1, (wins1*50)/NUMBER_OF_GAMES, agent2, (wins2*50)/NUMBER_OF_GAMES, (draws*50)/NUMBER_OF_GAMES))