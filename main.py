from game import Game
from agents import agentsList
from games import gamesList
from games import games
import params
import sys

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

kwargs = dict()
for kwarg in sys.argv[1:]:
    k , v = kwarg.split("=")
    kwargs[k]=v

agent1 = kwargs.get('agent1','lsi')
agent2 = kwargs.get('agent2','mcts')
game = kwargs.get('game','tic-tac-toe')

gameplay = Game(agent1, parameters, agent2, parameters, game)
winner = gameplay.playGame()
print('winner: Agent', winner)

# checkers = Game(agentsList.ea, parameters, agentsList.mcts, parameters, gamesList.checkers)
# winner = checkers.playGame()
# print('winner: Agent', winner)

# reversi = Game(agentsList.nmc, parameters, agentsList.mcts, parameters, gamesList.reversi)
# winner = reversi.playGame()
# print('winner: ', agentsList.nmc if winner == 1 else agentsList.mcts if winner == -1 else 'draw')