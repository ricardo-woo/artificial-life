import random
import math

from settings import WEIGHT, BIAS


class Neuron:
    def __init__(self, number_of_inputs):
        limit = 1 / math.sqrt(number_of_inputs) if number_of_inputs > 0 else 1
        self.weights = [random.uniform(-limit, limit) for _ in range(number_of_inputs)]
        self.bias = random.uniform(-limit, limit)

    def activate(self, inputs):

        value = self.bias

        for i in range(len(inputs)):
            value += inputs[i] * self.weights[i]
        return math.tanh(value)

    def copy(self):
        new_neuron = Neuron(len(self.weights))
        new_neuron.weights = self.weights[:]
        new_neuron.bias = self.bias
        return new_neuron

    def mutate(self, mutation_rate=0.1, mutation_strength=0.05):
        for i in range(len(self.weights)):
            if random.random() < mutation_rate:
                self.weights[i] += random.uniform(-mutation_strength, mutation_strength)
                self.weights[i] = max(-WEIGHT, min(WEIGHT, self.weights[i]))
        if random.random() < mutation_rate:
            self.bias += random.uniform(-mutation_strength, mutation_strength)
            self.bias = max(-BIAS, min(BIAS, self.bias))

    def get_data(self):
        return {"weights": self.weights, "bias": self.bias}

    @staticmethod
    def from_data(data):

        neuron = Neuron(len(data["weights"]))

        neuron.weights = data["weights"]
        neuron.bias = data["bias"]

        return neuron
