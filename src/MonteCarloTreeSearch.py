import math, random
import numpy as np
try:
    from . import GomokuHelper
except ImportError:
    from game import GomokuHelper

    
LOGGING = False


class MonteCarloTreeSearchNode():
    @staticmethod
    def search(initialState, gameHelper, neuralNetwork, simulations = 1000):
        root = MonteCarloTreeSearchNode(initialState, gameHelper, neuralNetwork)
        for i in range(simulations):
            root.spread(i+1)
        
        if LOGGING:
            print(str(root))
        return min(root.children, key = lambda node: node.getRating(simulations)).move
    
    
    
    def __init__(self, state, gameHelper, neuralNetwork, move = None):
        self.move = move
        self.state = state
        self.visited = 0
        self.children = []
        self.gameHelper = gameHelper
        self.neuralNetwork = neuralNetwork
        self.completed = False
        self.rating = None
        self.root = move == None
    
    
    def representTree(self, depth=0):
        string = '\t' * depth + repr(self) + "\n"
        
        string += "\n".join(node.representTree(depth+1) for node in self.children)
        
        return string
        
        
        
    def __str__(self):
        return self.representTree()
    
    
    
    def __repr__(self):
        return f"Node {self.move}, rating {self.rating}, visited = {self.visited}, completed = {self.completed}"
    
    
      
    def initialize(self):
        # rating is +INF if player on move is winning
        outcome = self.gameHelper.getOutcome(self.state)
        if outcome != None:
            if outcome == 0:
                self.rating = 0
            else:
                self.rating = outcome * math.inf
            if LOGGING:
                print("outcome:", outcome)
                print("rating:", self.rating)
            self.completed = True
            return self.rating
            
        self.rating = self.neuralNetwork.eval(self.state)
        self.children = list(map(
            lambda move: MonteCarloTreeSearchNode(
                    state = self.gameHelper.getStateAfterMove(self.state, move),
                    gameHelper = self.gameHelper,
                    neuralNetwork = self.neuralNetwork,
                    move = move
            ),
            self.gameHelper.getAllMoves(self.state)
        ))
                    
        return self.rating
        
        
        
    def getRating(self, totalNumberOfSimulationsRun):
        # rating is +INF if player on move is winning
        if self.visited == 0:
            return -math.inf
        return self.rating/self.visited + 2 * np.sqrt(np.log(totalNumberOfSimulationsRun)/self.visited)
        
        
        
    def spread(self, totalNumberOfSimulationsRun):
        """
        returns the difference betwean new and old rating
        """
        if self.completed:
            return 0
        self.visited += 1
        if LOGGING:
            print("spreading to:", repr(self))
        # hasn't been visited before
        if self.visited == 1:           
            return -self.initialize()
        
        filtered = filter(lambda node: not node.completed, self.children)
        
        if self.root and LOGGING:
            print([node.getRating(totalNumberOfSimulationsRun) for node in self.children])
            
        # rating is +INF if player on move is winning
        try:
            ratingChange = min(filtered, key = lambda node: node.getRating(totalNumberOfSimulationsRun)).spread(totalNumberOfSimulationsRun)
        #this means there were no values left
        except ValueError:
            self.completed = True
            oldRating = self.rating
            self.rating = - min(self.children, key=lambda node: node.rating).rating
            return self.rating - oldRating
    
        
        self.rating += ratingChange
        
        return -ratingChange        
        


if __name__ == "__main__":
    SIDE = 3
    LOGGING = True
    evalTable = np.fromfunction(lambda i, j: SIDE**2 - abs(i-SIDE//2) - abs(j-SIDE//2), (SIDE, SIDE))
    
    class FakeNN:
        def eval(self, state):
            return np.sum(evalTable * state)
            
    print(
        MonteCarloTreeSearchNode.search(
            initialState = np.full([SIDE, SIDE], 0),
            gameHelper = GomokuHelper,
            neuralNetwork = FakeNN()
        )
    )