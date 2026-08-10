import math


class SpatialGrid:
    def __init__(self, cell_size):
        self.cell_size = cell_size
        self.cells = {}
        self.object_cells = {}

    def clear(self):
        self.cells.clear()
        self.object_cells.clear()

    def get_cell(self, x, y):
        return (int(x // self.cell_size), int(y // self.cell_size))

    def insert(self, target, x, y):
        # Don't insert the same object twice
        if target in self.object_cells:
            return

        cell = self.get_cell(x, y)

        if cell not in self.cells:
            self.cells[cell] = []

        self.cells[cell].append(target)
        self.object_cells[target] = cell

    def remove(self, target):
        cell = self.object_cells.get(target)

        if cell is None:
            return

        if cell in self.cells:
            self.cells[cell].remove(target)

            if not self.cells[cell]:
                del self.cells[cell]

        del self.object_cells[target]

    def update(self, target, x, y):
        old_cell = self.object_cells.get(target)
        new_cell = self.get_cell(x, y)

        if old_cell == new_cell:
            return

        self.remove(target)
        self.insert(target, x, y)

    def query(self, x, y, radius):
        min_cell_x = int((x - radius) // self.cell_size)
        max_cell_x = int((x + radius) // self.cell_size)

        min_cell_y = int((y - radius) // self.cell_size)
        max_cell_y = int((y + radius) // self.cell_size)

        results = []

        for cell_x in range(min_cell_x, max_cell_x + 1):
            for cell_y in range(min_cell_y, max_cell_y + 1):
                cell = (cell_x, cell_y)

                if cell in self.cells:
                    results.extend(self.cells[cell])
        return results
