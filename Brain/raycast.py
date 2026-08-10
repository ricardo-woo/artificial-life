from Brain.Neuron import Neuron


class RaySensorLayer:
    def __init__(self, values_per_ray):
        self.values_per_ray = values_per_ray
        self.processor = Neuron(values_per_ray)

    def process(self, rays):
        return [self.processor.activate(ray) for ray in rays]

    def copy(self):
        new_layer = RaySensorLayer(self.values_per_ray)
        new_layer.kernel = self.processor.copy()
        return new_layer

    def mutate(self):
        self.processor.mutate()

    def get_data(self):
        return {
            "values_per_ray": self.values_per_ray,
            "processor": self.processor.get_data(),
        }

    @staticmethod
    def from_data(data):
        layer = RaySensorLayer(data["values_per_ray"])
        layer.processor = Neuron.from_data(data["processor"])
        return layer
