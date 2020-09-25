import games.ticTacToe.tic_tac_toe as ticTacToe
import games.checkers.checkersBoard as checkers
import games.reversi.reversiBoard as reversi
import games.gamesList as gamesList

def getBoard(gameType):
    if gameType == gamesList.reversi:
        return reversi.Board()
    if gameType == gamesList.ticTacToe:
        return ticTacToe.Board()
    return checkers.Board()