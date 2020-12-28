from game import Game
from agents import agentsList
from games import gamesList
from games import games
import params
import sys

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

agent1 = kwargs.get('agent1','ntbea')
agent2 = kwargs.get('agent2','mcts')
game = kwargs.get('game','tic-tac-toe')
debug = kwargs.get('debug', False)

gameplay = Game(agent1, sp_online_params, agent2, sp_offline_params, game, debug=debug)
winner = gameplay.playGame()
if winner == 0:
    print('Game Drawn')
elif winner == 1:
    print(agent1 + ' wins')
else:
    print(agent2 + ' wins')