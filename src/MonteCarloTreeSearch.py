import math, random
import numpy as np
from game import GomokuHelper

class MonteCarloTreeSearchNode():
    @staticmethod
    def search(initialState, gameHelper, neuralNetwork, simulations = 1000):
        root = MonteCarloTreeSearchNode(initialState, gameHelper, neuralNetwork)
        for i in range(simulations):
            root.spread(i+1)

        return max(root.childs, key = lambda node: node.getRating(simulations)).move
    
    
    
    def __init__(self, state, gameHelper, neuralNetwork, move = None):
        self.move = move
        self.state = state
        self.visited = 0
        self.childs = []
        self.gameHelper = gameHelper
        self.neuralNetwork = neuralNetwork
        self.completed = False
    
      
      
    def initialize(self):
        outcome = self.gameHelper.getOutcome(self.state)
        if outcome != None:
            self.rating = outcome * math.inf
            self.completed = True
            
        self.rating = self.neuralNetwork.eval(self.state)
        self.childs = list(map(
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
        if self.visited == 0:
            return math.inf
        return self.rating/self.visited + np.sqrt(2 * np.log(totalNumberOfSimulationsRun)/self.visited)
        
        
        
    def spread(self, totalNumberOfSimulationsRun):
        """
        returns the difference betwean new and old rating
        """
        self.visited += 1
        
        # hasn't been visited before
        if self.visited == 1:           
            return -self.initialize()
        
        filtered = filter(lambda node: not node.completed, self.childs)
    
        try:    
            ratingChange = max(filtered, key = lambda node: node.getRating(totalNumberOfSimulationsRun)).spread(totalNumberOfSimulationsRun)
        #this means there were no values left
        except ValueError:
            self.completed = True
            return 0
    
        
        self.rating += ratingChange
        
        return -ratingChange        
        


if __name__ == "__main__":
    class FakeNN:
        def eval(self, state):
            return random.random()*2 - 1
            
    print(
        MonteCarloTreeSearchNode.search(
            initialState = np.full([15,15], 0),
            gameHelper = GomokuHelper(),
            neuralNetwork = FakeNN()
        )
    )