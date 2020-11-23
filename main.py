from game import Game
from agents import agentsList
from games import gamesList
from games import games
import params

parameters = {
    'constant': [params.K_GRAVE, params.Ref, params.T],
    'tuning': [params.C, params.eps, params.VO]
}

tictactoeGame = Game(agentsList.lsi, parameters, agentsList.mcts, parameters, gamesList.ticTacToe)
winner = tictactoeGame.playGame()
print('winner: Agent', winner)

# checkers = Game(agentsList.ea, parameters, agentsList.mcts, parameters, gamesList.checkers)
# winner = checkers.playGame()
# print('winner: Agent', winner)

# reversi = Game(agentsList.nmc, parameters, agentsList.mcts, parameters, gamesList.reversi)
# winner = reversi.playGame()
# print('winner: ', agentsList.nmc if winner == 1 else agentsList.mcts if winner == -1 else 'draw')