class RaySensorLayer:
    def __init__(self, values_per_ray):
        self.values_per_ray = values_per_ray

    def process(self, rays):
        return rays

    def copy(self):
        return RaySensorLayer(self.values_per_ray)

    def mutate(self):
        pass

    def get_data(self):
        return {"values_per_ray": self.values_per_ray}

    @staticmethod
    def from_data(data):
        return RaySensorLayer(data["values_per_ray"])
