from random import choice
import datetime
from math import log, sqrt

X_PLAYER = 1
O_PLAYER = 2
TIE = -1
ONGOING = 0

class Node:
    def __init__(self, state, depth, move=None):
        self.state = state
        self.children = []
        self.isTerminal = False
        self.plays = 0
        self.wins = 0
        self.depth = depth
        self.move = move


class MonteCarlo:
    def __init__(self, board, **kwargs):
        self.board = board
        self.C = kwargs.get('C', 0.7)
        self.timePerMove = kwargs.get('timePerMove', 1)
    
    def play(self, cur):        
        totalReward = 0
        totalPlays = 0
        if self.board.isGameOver(cur.state):
            return

        start = datetime.datetime.utcnow()
        while datetime.datetime.utcnow() - start < datetime.timedelta(seconds=self.timePerMove):
            # Selection
            path = self.select(cur)

            # Expansion
            leaf = path[0]
            self.expand(leaf)

            # Simulation
            player = self.board.current_player(cur.state)
            opponent = O_PLAYER if player == X_PLAYER else O_PLAYER
            reward = 0
            if not leaf.isTerminal:
                reward, terminalDepth = self.simulate(leaf, player)
                totalPlays += 1
                totalReward += reward
                # Backpropagation
                for node in path:
                    node.plays += 1
                    node.wins += reward
        
        # Print Stats
        for x in sorted(((100 * child.wins/(child.plays+1), child.wins, child.plays, child.move) for child in cur.children), reverse = True):
            print('{3} - {0}% - {1}/{2}'.format(*x))

        # Get best move
        bestChild = 0
        bestScore = cur.children[0].wins/(cur.children[0].plays+1)
        maxPlays = cur.children[0].plays

        for i in range(1, len(cur.children)):
            score = cur.children[i].wins/(cur.children[i].plays+1)
            if score > bestScore:
                bestScore = score
                bestChild = i
        
        # Return next state when best move is made
        return (cur.children[bestChild], totalReward / totalPlays if totalPlays != 0 else 0)       

    # Selection Logic
    # Select the unexplored leaf node
    # To make selection among a child's children, use UCT (Upper Confidence Tree) formula
    def select(self, node):
        if len(node.children) == 0:
            return [node]
        
        log_total = log(sum((child.plays + 1) for child in node.children)) / log(2.71828)

        if len(node.children) < 1:
            raise Exception('length less than one')

        selectedChild = None
        bestScore = -1000000

        for child in node.children:
            score = (child.wins / (child.plays + 1)) + (self.C * sqrt(log_total/(child.plays+1)))
            if score > bestScore:
                bestScore = score
                selectedChild = child

        if selectedChild == None:
            raise Exception("selected child none", bestScore, node.state, log_total, [(child.wins, child.plays, (child.wins / (child.plays + 1)) + (self.C * sqrt(log_total/(child.plays+1)))) for child in node.children])

        path = self.select(selectedChild)
        path.append(node)
        return path
    
    # Expansion Logic
    def expand(self, node):
        if self.board.winner(node.state) != 0:
            node.isTerminal = True
            return
        node.children = [Node(self.board.next_state(node.state, move), node.depth + 1, move) for move in self.board.legal_plays(node.state)]
            
    
    # Simulation Logic
    # Play random moves till game ends
    # Return a tuple (reward, terminalNodeDepth)
    # Reward = 1 for win, 0 otherwise
    def simulate(self, node, player):
        winner = self.board.winner(node.state)
        if winner != ONGOING:
            if winner == TIE:
                return (0, node.depth)
            
            return (1 if winner == player else 0, node.depth)

        selectedChild = None
        if len(node.children) > 0:
            selectedChild = choice(node.children)
        else:
            selectedChild = choice([Node(self.board.next_state(node.state, move), node.depth + 1, move) for move in self.board.legal_plays(node.state)])

        return self.simulate(selectedChild, player)