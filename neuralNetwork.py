import collections, random, enum
import numpy as np

# creature is one object in the EVA
Creature = collections.namedtuple('Creature', 'weights biases')





class Engine():
    def __init__(self, neuralNetwork):
        self.neuralNetwork = neuralNetwork
        
        self.evalutionOfBoardStates = {}
        self.visitedBoardStates = []
        
    # monte carlo search (https://gist.github.com/MaxKho/dde027d3ca64173491b465c8dfef36b0#file-mcts-policy)
    def search(self, boardState):
        finished = outcome(boardState)
        if finished != None:
            return finished
    
        if boardState not in self.visitedBoardStates:
            visitedBoardStates.append(boardState)
            evalutionOfBoardStates[boardState], v = self.neuralNetwork.predict(boardState)
            return -v
      
        maxEvalution, bestMove = -float("inf"), random.choice(legalMoves(boardState))
        for move in legalMoves(s):
            # magic!
            evalution = Q[boardState][move] + c*P[boardState][move]*sqrt(sum(N[s]))/(1+N[boardState][move])
            if evalution > maxEvalution:
                maxEvalution = evalution
                bestMove = move
        move = bestMove
        
        boardStateAfterMove = makeMove(boardState, move)
        v = search(boardStateAfterMove, nnet)
    
        Q[boardState][move] = (N[boardState][move]*Q[boardState][move] + v)/(N[boardState][move]+1)
        global N[boardState][move]
        N[boardState][move] += 1
        return -v

    def policy(s, nnet):
        for i in range(number_of_simulations):
            search(s, nnet)
        return [N[s][a] for a in legalMoves(s)]
  
  
class LinearLayer():
    def __init__(self, inputs, outputs):
        self.inputs = inputs
        self.outputs = outputs
        
        
    def predict(self, creature: Creature, data):
        if len(creature.weights) != self.outputs or creature.biases != self.outputs:
            raise ValueError("Invalid creature in LinearLayer!")
            
        if len(input) != self.inputs:
            raise ValueError("Invalid number of inputs in LinearLayer!")
            
        output = np.vectorize(lambda weights: numpy.dot(weights, data))(creature.weights) + creature.biases
        return output
        

def getAnswer(data, creature: Creature):
    creature
    for layer in la