from random import choice
from random import random
from math import log, sqrt, isnan, inf

X_PLAYER = 1
O_PLAYER = 2
TIE = -1
ONGOING = 0

class Node:
    def __init__(self, state, depth, move=None,parent=None):
        self.state = state
        self.children = []
        self.isTerminal = False
        self.plays = 0
        self.wins = 0
        self.depth = depth
        self.move = move
        self.parent = parent


class MonteCarlo:
    def __init__(self, board, **kwargs):
        self.board = board
        self.params = {}
        self.lookup={}
        self.AmafTable={}
        # self.f=open("output.txt","w")


    def setRootNodeState(self, state):
        self.root = Node(state, 0)
    
    def simulate(self, rootGameState):
        if self.board.isGameOver(self.root.state):
            return 0

        # Selection
        path = self.select(self.root)
        # print("Path   ",path[0].children)

        # Expansion
        leaf = path[0]
        self.expand(leaf)

        # Simulation
        player = self.board.current_player(self.root.state)
        opponent = O_PLAYER if player == X_PLAYER else X_PLAYER
        reward = 0
        # if not leaf.isTerminal:
        reward, terminalDepth,move = self.playout(leaf, player)

        # Backpropagation
        for node in path:
            node.plays += 1
            node.wins += reward
            if str(node) in self.AmafTable:
                if str(move) in self.AmafTable[str(node)]:
                    obj=self.AmafTable[str(node)][str(move)]
                    obj['plays']+=1
                    obj['wins']+=1 if reward==1 else 0
                    obj['average']=obj['wins']/obj['plays']
                else:
                    self.AmafTable[str(node)][str(move)]={"plays":0,"wins":0,"average":0.0}
            else:
                self.AmafTable[str(node)]={}
        
        return reward

    # Selection Logic
    # Select the unexplored leaf node
    # To make selection among a child's children, use UCT (Upper Confidence Tree) formula
    def select(self, node):
        if len(node.children) == 0 or node.plays < self.params['T']:
            return [node]
        total=max(sum(child.plays for child in node.children), 1)
        log_total = log(total)
        K=self.params['K']
        Beta=1 if K == inf else sqrt(K/(3*total+K))
        Ref=self.params['Ref']
        temp=node
        ancestor=node #closest ancestor that has atleast ref visits
        while temp!=None:
            visits=max(sum(child.plays for child in temp.children), 1)
            if visits>=Ref:
                ancestor=temp
                break
            temp=temp.parent
        
        

        if len(node.children) < 1:
            raise Exception('length less than one')

        selectedChild = None
        bestScore = -1000000

        for child in node.children:
            score=(1-Beta)*(child.wins / (child.plays + 1))+ (self.params['C'] * sqrt(log_total/(child.plays+1)))
            score+=Beta*self.AmafTable[ancestor][node.move] if ancestor in self.AmafTable else 0 
            if score > bestScore:
                bestScore = score

        goodChildren = []
        for child in node.children:
            score = (1-Beta)*(child.wins / (child.plays + 1))+(self.params['C'] * sqrt(log_total/(child.plays+1)))
            score+=Beta*self.AmafTable[ancestor][node.move] if ancestor in self.AmafTable else 0
            if bestScore - self.params['VO'] <= score:
                goodChildren.append(child)

        # self.f.write(str(len(goodChildren))+'\n')
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
        # print(node.state,self.board.legal_plays(node.state))
        node.children = [Node(self.board.next_state(node.state, move), node.depth + 1, move,node) for move in self.board.legal_plays(node.state)]
            
    
    # Simulation Logic
    # Play random moves till game ends
    # Return a tuple (reward, terminalNodeDepth)
    # Reward = 1 for win, 0 otherwise
    def playout(self, node, player):
        winner = self.board.winner(node.state)
        if winner != ONGOING:
            if winner == TIE:
                return (0.5, node.depth,node.move)
            
            return (1 if winner == player else 0, node.depth,node.move)

        # selectedChild = None
        if len(node.children) > 0:
            selectedChild = self.choose(node.children)   #select a node from a list of nodes
        else:
            selectedChild = self.choose([Node(self.board.next_state(node.state, move), node.depth + 1, move) for move in self.board.legal_plays(node.state)])
        selectedChild.move=repr(selectedChild.move)
        if selectedChild.move in self.lookup:    
            self.lookup[selectedChild.move]['plays']+=1
            self.lookup[selectedChild.move]['average']=self.lookup[selectedChild.move]['wins']/self.lookup[selectedChild.move]['plays']
        else:
            self.lookup[selectedChild.move]={'plays':0,'wins':0,'average':0.0}
        result,depth,move=self.playout(selectedChild, player)
        if result==1:
            self.lookup[selectedChild.move]['wins']+=1
        return result,depth,selectedChild.move

    def choose(self,options):
        if random()<self.params['eps'] or len(self.lookup)<2:
            return choice(options)
        else:
            #sort lookup table based on values
            self.lookup={k: v for k, v in sorted(self.lookup.items(), key=lambda item:item[1]['average'])}
            for i in self.lookup:
                for j in options:
                    if j.move==i:
                        return j
            return choice(options)





    def setParams(self, params):
        for param in params:
            self.params[param['name']] = param['value']