import games.tic_tac_toe as ticTacToe
import games.checkersBoard as checkers
import games.gamesList as gamesList

def getBoard(gameType):
    if(gameType == gamesList.ticTacToe):
        return ticTacToe.Board()
    return checkers.Board()