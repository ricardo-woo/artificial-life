import math

class SpatialGrid:
    def __init__(self, cell_size):
        self.cell_size = cell_size
        self.cells = {}

    def clear(self):
        self.cells.clear()

    def get_cell(self,x,y):
        return(int(x // self.cell_size), int(y // self.cell_size))

    def insert(self, target, x, y):
        cell = self.get_cell(x,y)

        if cell not in self.cells:
            self.cells[cell] = []

        self.cells[cell].append(target)

    def query(self, x, y, radius):
        min_cell_x = int((x-radius) // self.cell_size)
        max_cell_x = int((x+radius) // self.cell_size)

        min_cell_y = int((y-radius) // self.cell_size)
        max_cell_y = int((y+radius) // self.cell_size)

        results = []

        for cell_x in range(min_cell_x, max_cell_x + 1):
            for cell_y in range(min_cell_y, max_cell_y + 1):
                cell = (cell_x, cell_y)

                if cell in self.cells:
                    results.extend(self.cells[cell])
        return results