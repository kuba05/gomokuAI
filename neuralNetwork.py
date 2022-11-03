from src import MonteCarloTreeSearchNode
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
            working = self.RELU(working)
            working = layer.predict(weight, working)
        return working
    
    def RELU(self, data):
        return np.vectorize(lambda value: max(0, value))(data)
  
  
class LinearLayer():
    def __init__(self, inputs, outputs):
        self.inputs = inputs
        self.outputs = outputs
        
        
    def predict(self, layerWeight: LayerWeight, data):
        if len(layerWeight.weights) != self.outputs or layerWeight.biases != self.outputs:
            raise ValueError("Invalid layerWeight in LinearLayer!")
            
        if len(input) != self.inputs:
            raise ValueError("Invalid number of inputs in LinearLayer!")
            
        output = np.vectorize(lambda weights: numpy.dot(weights, data))(layerWeight.weights) + layerWeight.biases
        return output
        
sampleModel = Model(25)
