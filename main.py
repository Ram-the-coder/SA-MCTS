from game import Game
from agents import agentsList
from games import gamesList
from games import games
from math import inf

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

tictactoeGame = Game(agentsList.lsi, parameters, agentsList.mcts, parameters, gamesList.ticTacToe)
winner = tictactoeGame.playGame()
print('winner: Agent', winner)

# checkers = Game(agentsList.ea, parameters, agentsList.mcts, parameters, gamesList.checkers)
# winner = checkers.playGame()
# print('winner: Agent', winner)

# reversi = Game(agentsList.nmc, parameters, agentsList.mcts, parameters, gamesList.reversi)
# winner = reversi.playGame()
# print('winner: ', agentsList.nmc if winner == 1 else agentsList.mcts if winner == -1 else 'draw')