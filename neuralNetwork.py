import matplotlib.pyplot
import scipy.special
import numpy as np
import math

class NeuralNetwork:
	def __init__(self, inputNodes, hiddenNodes, outputNodes, learningRate):
		self.inputNodes = inputNodes
		self.hiddenNodes = hiddenNodes
		self.outputNodes = outputNodes

		# RANDOMIZE WEIGHTS (BETWEEN -0.5 AND 0.5)
		
		self.wih = np.random.rand(self.hiddenNodes, self.inputNodes) -0.5
		self.who = np.random.rand(self.outputNodes, self.hiddenNodes) - 0.5

		self.learningRate = learningRate

		pass

	
	def Train(self, inputList, outputList):
		# LIST TO NP ARRAY

		inputs = np.array(inputList, ndmin = 2).T
		outputs = np.array(outputList, ndmin = 2).T

		# FEEDFORWARD

		hiddenInputs = np.dot(self.wih, inputs)
		hiddenOutputs = self.ActivationFunction(hiddenInputs)

		finalInputs = np.dot(self.who, hiddenOutputs)
		finalOutputs = self.ActivationFunction(finalInputs)

		finalErrors = outputs - finalOutputs # target - acctual output

		hiddenErrors = np.dot(self.who.T, finalErrors)

		# BACKPROPAGATION

		self.who += self.learningRate * np.dot((finalErrors * finalOutputs * (1.0 - finalOutputs)), np.transpose(hiddenOutputs))

		self.wih += self.learningRate * np.dot((hiddenErrors * hiddenOutputs * (1.0 - hiddenOutputs)), np.transpose(inputs))

		pass

	def Query(self, inputList):
		inputs = np.array(inputList, ndmin = 2).T

		hiddenInputs = np.dot(self.wih, inputs)
		hiddenOutputs = self.ActivationFunction(hiddenInputs)

		finalInputs = np.dot(self.who, hiddenOutputs)
		finalOutputs = self.ActivationFunction(finalInputs)

		return finalOutputs

	# SIGMOID ACTIVATION
	def ActivationFunction(self, input):
		if (isinstance(input, (np.ndarray, np.generic))):
			for i in input:
				i = (1 / (1 + pow(math.e, -i)))

		return (1 / (1 + pow(math.e, -input)))
