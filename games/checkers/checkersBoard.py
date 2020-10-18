from games.boardMeta import BoardMeta, BoardException
from games.checkers.util.checkers import CheckerBoard
from random import choice

TIE = -1
ONGOING = 0

class Board(BoardMeta):

    def start(self):
        return CheckerBoard()

    def current_player(self, state):
        return 1 if state.active == 0 else 2

    def next_state(self, state, move_sequence):
        next_state_var = state;
        for move in move_sequence:
            next_state_var = next_state_var.peek_move(move)
        return next_state_var
    
    def legal_plays(self, state):
        moves = state.get_move_sequences()
        return moves

    def winner(self, state):
        if not state.is_over():
            return ONGOING
        if state.is_draw():
            return -1
        return 1 if state.passive == 0 else 2

    def isGameOver(self, state):
        return state.is_over()

    def display(self, state):
        print(state)

    def averageNumberOfMoves(self):
        return 76





