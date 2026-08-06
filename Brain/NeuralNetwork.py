from Brain.Neuron import Neuron


class NeuralNetwork:
    def __init__(self):
        inputs = 6
        # input[0] = energy
        # input[1] = food detected
        # input[2] = distance to closest food
        # input[3] = sin(angle to closest food)
        # input[4] = cos(angle to closest food)
        # input[5] = time since food visible

        hidden = 7

        outputs = 2
        # output[0] = angle change
        # output[1] = forward

        self.hidden_layer = [Neuron(inputs) for _ in range(hidden)]

        self.output_layer = [Neuron(hidden) for _ in range(outputs)]

    def predict(self, inputs):

        hidden_outputs = []

        for neuron in self.hidden_layer:
            neuron_output = neuron.activate(inputs)
            hidden_outputs.append(neuron_output)

        final_outputs = []

        for neuron in self.output_layer:
            neuron_output = neuron.activate(hidden_outputs)
            final_outputs.append(neuron_output)

        return final_outputs

    def copy(self):
        new_network = NeuralNetwork()
        new_network.hidden_layer = [neuron.copy() for neuron in self.hidden_layer]
        new_network.output_layer = [neuron.copy() for neuron in self.output_layer]
        return new_network

    def mutate(self):
        for neuron in self.hidden_layer:
            neuron.mutate()

        for neuron in self.output_layer:
            neuron.mutate()

    def get_data(self):

        return {
            "hidden": [neuron.get_data() for neuron in self.hidden_layer],
            "output": [neuron.get_data() for neuron in self.output_layer],
        }

    @staticmethod
    def from_data(data):

        network = NeuralNetwork()

        network.hidden_layer = [Neuron.from_data(n) for n in data["hidden"]]

        network.output_layer = [Neuron.from_data(n) for n in data["output"]]

        return network
