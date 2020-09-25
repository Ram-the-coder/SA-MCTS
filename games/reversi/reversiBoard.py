from games.boardMeta import BoardMeta, BoardException
import games.reversi.util.reversi as util
from copy import deepcopy

PLAYER_1 = 'X'
PLAYER_2 = 'O'
TIE = -1
ONGOING = 0

class BoardState:
    def __init__(self):
        self.board = util.getNewBoard()
        util.resetBoard(self.board)

        self.turn = PLAYER_1
        self.gameOver = False
        self.winner = ONGOING

    def makeMove(self, move):
        util.makeMove(self.board, self.turn, move[0], move[1])
        self.turn = PLAYER_2 if self.turn == PLAYER_1 else PLAYER_1
        if util.getValidMoves(self.board, self.turn) == []:
            self.gameOver = True
            scores = util.getScoreOfBoard(self.board)
            if scores[PLAYER_1] > scores[PLAYER_2]:
                self.winner = PLAYER_1
            elif scores[PLAYER_1] < scores[PLAYER_2]:
                self.winner = PLAYER_2
            else: 
                self.winner = TIE



class Board(BoardMeta):

    def start(self):
        return BoardState()

    def current_player(self, state):
        return 1 if state.turn == PLAYER_1 else 2

    def next_state(self, state, move):
        newState = deepcopy(state)
        newState.makeMove(move)
        return newState

    def legal_plays(self, state):
        return util.getValidMoves(state.board, state.turn)

    def winner(self, state):
        return state.winner

    def isGameOver(self, state):
        return state.gameOver

    def display(self, state):
        util.drawBoard(state.board)