import random, time, sys
import numpy as np

from worm import Worm
from gold import Gold

UP = 'up'
DOWN = 'down'
LEFT = 'left'
RIGHT = 'right'

class Snake:
    def __init__(self, cell_size = 9):
    
        self.cell_size = cell_size
        self.map = np.zeros((cell_size, cell_size), np.uint8)
        self.worm = Worm(self.cell_size)
        self.gold = Gold(self.cell_size)

        #check object is overlapped
        if self.check_overlapped_object():
            self.gold.set_position(self.get_empty_position())

    def draw_matrix(self):
        self.map = np.zeros((self.cell_size, self.cell_size), np.uint8)
        for wormBody in self.worm.coordinate:
            self.map[wormBody['y']][wormBody['x']] = 255 // 2
        self.map[self.gold.y][self.gold.x] = 255
        print(self.map)

    def check_overlapped_object(self):
        #check gold
        for wormBody in self.worm.coordinate:
            if wormBody['x'] == self.gold.x and wormBody['y'] == self.gold.y:
                return True

    def get_empty_position(self):
        positions = []
        for x in range(self.cell_size):
            for y in range(self.cell_size):
                positions.append([y, x])

        for wormBody in self.worm.coordinate:
            positions.remove([wormBody['y'], wormBody['x']])

        if [self.gold.y, self.gold.x] in positions:
            positions.remove([self.gold.y, self.gold.x])

        return positions[random.randint(0, len(positions) - 1)]

if __name__ == '__main__':
    wormy = Snake()
    wormy.terminate()