from mcts import MonteCarlo
from game_state import Board

ticTacToe = Board()
mctsInstance = MonteCarlo(ticTacToe, ticTacToe.start())
while True:
    cont = input('Play?')
    if cont != 'y':
        break
    mctsInstance.play()

