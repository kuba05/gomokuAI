from src import MonteCarloTreeSearchNode, GomokuHelper
from collections.abc import Sequence
import collections, random, enum
import numpy as np

# model is one object in the EVA
LayerWeight = collections.namedtuple('LayerWeight', 'weights biases')





class Model():
    def __init__(self, inputs):
        self.layers = [LinearLayer(inputs, inputs//2), LinearLayer(inputs//2, 1)]
    
    def eval(self, data: np.array, weights: list) -> np.array:
        working = data.flatten()
        for layer, weight in zip(self.layers, weights):
            working = self.nonlinear(layer.predict(weight, working))
        return working
    
    def nonlinear(self, data):
        return np.vectorize(lambda value: np.tanh(value))(data)
  
    def getRandomWeights(self):
        return [layer.getRandomWeights() for layer in self.layers]

    
class LinearLayer():
    def __init__(self, inputs, outputs):
        self.inputs = inputs
        self.outputs = outputs
        
        
    def predict(self, layerWeight: LayerWeight, data):
        if len(layerWeight.weights) != self.outputs or len(layerWeight.biases) != self.outputs:
            raise ValueError("Invalid layerWeight in LinearLayer!")
            
        if len(data) != self.inputs:
            raise ValueError("Invalid number of inputs in LinearLayer!")
            
        #print("data:",data.shape)
        #print("data:", data.reshape(-1, 1).shape)
        #print("layerWeight:", layerWeight.weights.shape)
        #print(" layerWeight.biases:",  layerWeight.biases.shape)
        output = np.matmul(layerWeight.weights, data.reshape(-1, 1)) 
        #print("output:", output.shape)
        return output+ layerWeight.biases

    def getRandomWeights(self):
        return LayerWeight(np.random.rand(self.outputs, self.inputs), np.random.rand(self.outputs, 1))
        


class NeuralNetwork():
    def __init__(self, model, weights: list, mutateFactor=0.2):
        self.model = model
        self.weights = weights
        self.mutateFactor = mutateFactor
        #print(weights)
        
    def eval(self, state):
        eval = self.model.eval(state, self.weights)
        #print(state)
        #print(eval)
        return eval
        
    def createChild(self):
        return NeuralNetwork(self.model, np.copy(self.weights))
    
    def mutate(self):
        self.weights.weights += (np.random.rand(*self.weights.weights.shape) - 0.5) * self.mutateFactor * 2
        
        self.weights.biases += (np.random.rand(*self.weights.biases.shape) - 0.5) * self.mutateFactor * 2
                
                

def fight(players, search, gameHelper, simulations = 100, logging = False):
    """
    returns -1 if 1st player wins, 1 if second player wins, 0 if the game is a draw
    """
    initialState = np.full([5,5], 0)
    state = initialState
    if logging:
        print("state:\n", state)
        input()
        
    numberOfPlayers = len(players)
    activePlayer = -1
    while gameHelper.getOutcome(state) == None:
        activePlayer = (activePlayer + 1)%numberOfPlayers
        move = search(state, gameHelper, players[activePlayer], simulations=simulations)
        if logging:
            print("move:", move)
        state = gameHelper.getStateAfterMove(state, move)
        
        if logging:
            print("state:\n", state)
            input()
    if logging:
        print("Won by player ", activePlayer)
    return gameHelper.getOutcome(state) * (activePlayer * 2 - 1)


def evolve(model, populationSize = 100, cycles = 100):
    population = np.array([NeuralNetwork(model, model.getRandomWeights()) for i in range(populationSize)])
    
    mutation = np.vectorize(NeuralNetwork.mutate)
    
    
    for i in range(cycles):
        #print(population)
        print(i)
        population = np.random.permutation(population)
        
        for i in range(0, populationSize, 2):
            result = fight(population[i:i+2], MonteCarloTreeSearchNode.search, GomokuHelper)
            if result == 0:
                continue
            else:
                # this points to the index of the loser
                loser = i + (-result + 1)//2
                winner = i + (result + 1)//2
                population[loser] = population[winner].createChild()
        population = mutation(population)
        print(i)
        
    return population
    

       
if __name__ == "__main__":   
    sampleModel = Model(25)
    evolve(sampleModel) 
    nn1 = NeuralNetwork(sampleModel, sampleModel.getRandomWeights())
    nn2 = NeuralNetwork(sampleModel, sampleModel.getRandomWeights())
    fight([nn1, nn2], MonteCarloTreeSearchNode.search, GomokuHelper, simulations = 100, logging = True)