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
    def __init__(self, board, startState, **kwargs):
        self.board = board
        self.root = Node(startState, 0)
        self.C = kwargs.get('C', 0.7)
    
    def play(self):        
        cur = self.root
        getInput = True;

        # THE GAME
        while self.board.winner(cur.state) == 0:
            self.board.display(cur.state)
            getInput = not getInput

            # Player's Turn
            if getInput:
                if len(cur.children) == 0:
                    expand(cur)
                inputMove = int(input('Move:'))
                nextNode = None
                for child in cur.children:
                    if child.move == inputMove:
                        nextNode = child
                        break
                cur = nextNode
                continue

            # AI's Turn
            start = datetime.datetime.utcnow()
            while datetime.datetime.utcnow() - start < datetime.timedelta(seconds=2):
                # Selection
                path = self.select(cur)

                # Expansion
                leaf = path[0]
                self.expand(leaf)

                # Simulation
                player = X_PLAYER
                opponent = O_PLAYER
                reward = 0
                if not leaf.isTerminal:
                    reward, terminalDepth = self.simulate(leaf, player)
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
            
            # Make best move
            cur = cur.children[bestChild]
        

        self.board.display(cur.state)
        print('Winner', self.board.winner(cur.state))


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