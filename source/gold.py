import random

class Gold:
    
    def __init__(self, cell_size):
        self.cell_size = cell_size
        
        self.x = random.randint(0, self.cell_size - 1)
        self.y = random.randint(0, self.cell_size - 1)

    def set_position(self, coordinate):
        self.x = coordinate[0]
        self.y = coordinate[1]
