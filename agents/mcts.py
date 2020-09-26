from random import choice
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
        self.root = None


class MonteCarlo:
    def __init__(self, board, **kwargs):
        self.board = board
        self.params = {}

    def setRootNodeState(self, state):
        self.root = Node(state, 0)
    
    def simulate(self, rootGameState):
        if self.board.isGameOver(self.root.state):
            return 0

        # Selection
        path = self.select(self.root)

        # Expansion
        leaf = path[0]
        self.expand(leaf)

        # Simulation
        player = self.board.current_player(self.root.state)
        opponent = O_PLAYER if player == X_PLAYER else O_PLAYER
        reward = 0
        # if not leaf.isTerminal:
        reward, terminalDepth = self.playout(leaf, player)

        # Backpropagation
        for node in path:
            node.plays += 1
            node.wins += reward
        
        return reward

    # Selection Logic
    # Select the unexplored leaf node
    # To make selection among a child's children, use UCT (Upper Confidence Tree) formula
    def select(self, node):
        if len(node.children) == 0 or node.plays < self.params['T']:
            return [node]
        
        log_total = log(max(sum(child.plays for child in node.children), 1))

        if len(node.children) < 1:
            raise Exception('length less than one')

        selectedChild = None
        bestScore = -1000000

        for child in node.children:
            score = (child.wins / (child.plays + 1)) + (self.params['C'] * sqrt(log_total/(child.plays+1)))
            if score > bestScore:
                bestScore = score

        goodChildren = []
        for child in node.children:
            score = (child.wins / (child.plays + 1)) + (self.params['C'] * sqrt(log_total/(child.plays+1)))
            if bestScore - self.params['VO'] <= score:
                goodChildren.append(child)

        selectedChild = choice(goodChildren)

        if selectedChild == None:
            raise Exception("selected child none", bestScore, node.state, log_total, [(child.wins, child.plays, (child.wins / (child.plays + 1)) + (self.params['C'] * sqrt(log_total/(child.plays+1)))) for child in node.children])

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
    def playout(self, node, player):
        winner = self.board.winner(node.state)
        if winner != ONGOING:
            if winner == TIE:
                return (0.5, node.depth)
            
            return (1 if winner == player else 0, node.depth)

        selectedChild = None
        if len(node.children) > 0:
            selectedChild = choice(node.children)
        else:
            selectedChild = choice([Node(self.board.next_state(node.state, move), node.depth + 1, move) for move in self.board.legal_plays(node.state)])

        return self.playout(selectedChild, player)

    def setParams(self, params):
        for param in params:
            self.params[param['name']] = param['value']