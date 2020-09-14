import games.tic_tac_toe as ticTacToe
import games.gamesList as gamesList

def getBoard(gameType):
    if(gameType == gamesList.ticTacToe):
        return ticTacToe.Board()