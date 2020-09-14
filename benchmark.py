from game import Game
from agents.agentsList import benchmarkList as agents
from games.gamesList import benchmarkList as games
import progressbar
import os

NUMBER_OF_GAMES_PER_PAIR_OF_AGENTS = 5

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
    print('Game:', game)
    for agent1 in agents:
        for agent2 in agents:
            if agent1 == agent2:
                continue
            wins1 = 0
            wins2 = 0
            bar = progressbar.ProgressBar(maxval=5, widgets=[progressbar.Bar('=', '[', ']'), ' ', progressbar.Percentage()])
            print('Running:', agent1, 'vs', agent2)
            bar.start()
            for i in range(NUMBER_OF_GAMES_PER_PAIR_OF_AGENTS):
                gameInstance = Game(agent1, parameters, agent2, parameters, game)
                winner = gameInstance.playGame(displayState=False)
                if winner == 1:
                    wins1 += 1
                else:
                    wins2 += 1
                bar.update(i+1)
            bar.finish()
            print('Result: {0}: {1}% {2}: {3}%'.format(agent1, wins1*20, agent2, wins2*20))
