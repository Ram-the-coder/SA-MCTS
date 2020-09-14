from game import Game
from agents import agentsList
from games import gamesList

parameters = [{
    'name': 'C',
    'isDiscreteDomain': True,
    'lowerBound': None, # For continuous domain
    'upperBound': None, # For continuous domain
    'domain': [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9], # For discrete domain
    'default': 0.7
}]

tictactoeGame = Game(agentsList.nmc, parameters, agentsList.mcts, parameters, gamesList.ticTacToe)
winner = tictactoeGame.playGame()
print('winner: Agent', winner)

