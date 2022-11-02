import collections, random, enum
import numpy as np

# model is one object in the EVA
LayerWeights = collections.namedtuple('LayerWeights', 'weights biases')





class Model():
    def __init__(self, inputs):
        self.layers = [LinearLayer(inputs, inputs//2), LinearLayer(inputs//2, 1)]
    
    def eval(self, data):
        working = data.flatten()
        for layer in self.layers:
            working = layer.predict(working)
  
class LinearLayer():
    def __init__(self, inputs, outputs):
        self.inputs = inputs
        self.outputs = outputs
        
        
    def predict(self, layerWeights: LayerWeights, data):
        if len(layerWeights.weights) != self.outputs or layerWeights.biases != self.outputs:
            raise ValueError("Invalid layerWeights in LinearLayer!")
            
        if len(input) != self.inputs:
            raise ValueError("Invalid number of inputs in LinearLayer!")
            
        output = np.vectorize(lambda weights: numpy.dot(weights, data))(layerWeights.weights) + layerWeights.biases
        return output
        
        
def getAnswer(data, layerWeights: LayerWeights):
    layerWeights
    for layer in la