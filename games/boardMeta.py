from abc import ABC, abstractmethod

# Game status
# TIE = -1
# ONGOING = 0
# Player numbers start from 1

class BoardMeta:

    # Returns a representation of the starting state of the game.
    @abstractmethod
    def start(self):
        pass

    # Takes the game state and returns the current player's number.
    @abstractmethod
    def current_player(self, state):
        pass
    
    # Takes the game state, and the move to be applied.
    # Returns the new game state.
    @abstractmethod
    def next_state(self, state, play):
        pass

    # Returns the full list of moves that
    # are legal plays for the current player.
    @abstractmethod
    def legal_plays(self, state):
        pass

    # If the game is now won, return the player
    # number.  If the game is still ongoing, return zero.  If
    # the game is tied, return a different distinct value, e.g. -1.
    @abstractmethod
    def winner(self, state):
        pass
    
    # Returns true if game is over
    @abstractmethod
    def isGameOver(self, state):
        pass

    # Used to display the board
    # Use pass if it can't be displayed
    @abstractmethod
    def display(self, state):
        pass
        
class BoardException(Exception): 
    def __init__(self, error_message, error_object):
        self.msg = error_message
        self.details = error_object
    
