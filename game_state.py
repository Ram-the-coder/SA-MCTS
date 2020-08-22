from copy import deepcopy

EMPTY = 0
X_PLAYER = 1
O_PLAYER = 2
TIE = -1
ONGOING = 0

class BoardException(Exception): 
    def __init__(self, error_message, error_object):
        self.msg = error_message
        self.details = error_object

class Board(object):

    def start(self):
        # Returns a representation of the starting state of the game.
        state = (EMPTY,)*9
        return state

    def current_player(self, state):
        # Takes the game state and returns the current player's number.
        numx = 0
        numo = 0
        for i in range(0, 9):
            if state[i] == X_PLAYER:
                numx += 1
            elif state[i] == O_PLAYER:
                numo += 1
        
        return X_PLAYER if numx == numo else O_PLAYER

    def next_state(self, state, play):
        # Takes the game state, and the move to be applied.
        # Returns the new game state.
        if state[play] != EMPTY:
            raise BoardException('Illegal move', {'state': state, 'move': play})
            return None

        nxt_state_list = list(state);
        nxt_state_list[play] = self.current_player(state)
        return tuple(nxt_state_list)

    def legal_plays(self, state):
        # Returns the full list of moves that
        # are legal plays for the current player.
        legal_moves = [i for i in range(0, 9) if state[i] == EMPTY]
        return legal_moves


    def winner(self, state):
        # If the game is now won, return the player
        # number.  If the game is still ongoing, return zero.  If
        # the game is tied, return a different distinct value, e.g. -1.

        # Check rows
        for i in range(0, 7, 3):
            if state[i] != EMPTY and state[i] == state[i+1] and state[i] == state[i+2]:
                return state[i]

        # Check columns
        for i in range(0, 3):
            if state[i] != EMPTY and state[i] == state[i+3] and state[i] == state[i+6]:
                return state[i]

        # Check Diagonals
        if state[0] != EMPTY and state[0] == state[4] and state[0] == state[8]:
            return state[i]
        if state[2] != EMPTY and state[2] == state[4] and state[2] == state[6]:
            return state[i]

        # Check Tie vs Ongoing
        for i in range(0, 9):
            if state[i] == EMPTY:
                return ONGOING
        
        return TIE

    def display(self, state):
        for i in range(0, 9):
            if state[i] == EMPTY:
                print('-', end=' ')
            elif state[i] == X_PLAYER:
                print('X', end=' ')
            else:
                print('O', end=' ')

            if i % 3 == 2:
                print('')


