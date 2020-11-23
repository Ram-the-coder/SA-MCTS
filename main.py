from game import Game
from agents import agentsList
from games import gamesList
from games import games
import params

parameters = {
    'constant': [params.K_GRAVE, params.Ref, params.T],
    'tuning': [params.C, params.eps, params.VO]
}

sp_online_params = {
    'tuning': [params.C, params.eps],
    'constant': [params.K_UCT, params.Ref, params.VO, params.T]
}

sp_offline_params = {
    'tuning': [],
    'constant': [params.C, params.eps, params.K_UCT, params.Ref, params.VO, params.T]
}

tictactoeGame = Game(agentsList.lsi, sp_online_params, agentsList.mcts, sp_offline_params, gamesList.ticTacToe)
winner = tictactoeGame.playGame()
print('winner: Agent', winner)

# checkers = Game(agentsList.ea, parameters, agentsList.mcts, parameters, gamesList.checkers)
# winner = checkers.playGame()
# print('winner: Agent', winner)

# reversi = Game(agentsList.nmc, parameters, agentsList.mcts, parameters, gamesList.reversi)
# winner = reversi.playGame()
# print('winner: ', agentsList.nmc if winner == 1 else agentsList.mcts if winner == -1 else 'draw')