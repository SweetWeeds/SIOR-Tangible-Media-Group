import random

from gold import Gold

UP = 'up'
DOWN = 'down'
LEFT = 'left'
RIGHT = 'right'

HEAD = 0 

class Worm:
    def __init__(self, cell_size):
        self.cell_size = cell_size

        self.startx = cell_size // 2
        self.starty = cell_size // 2

        self.coordinate = [{'x': self.startx, 'y': self.starty}, {'x': self.startx - 1, 'y': self.starty}]
        self.direction = RIGHT

    def check_collision(self):
        if self.coordinate[HEAD]['x'] < 0 or self.coordinate[HEAD]['x'] >= self.cell_size:
            return True
        if self.coordinate[HEAD]['y'] < 0 or self.coordinate[HEAD]['y'] >= self.cell_size:
            return True

        for wormBody in self.coordinate[1 :]:
            if self.coordinate[HEAD]['x'] == wormBody['x'] and self.coordinate[HEAD]['y'] == wormBody['y']:
                return True
        return False

    def check_ahead_gold(self, gold):
        if self.direction == LEFT:
            if gold.x == (self.coordinate[HEAD]['x'] - 1) and gold.y == self.coordinate[HEAD]['y']:
                return True
        elif self.direction == RIGHT:
            if gold.x == (self.coordinate[HEAD]['x'] + 1) and gold.y == self.coordinate[HEAD]['y']:
                return True
        elif self.direction == UP:
            if gold.x == self.coordinate[HEAD]['x'] and gold.y == (self.coordinate[HEAD]['y'] - 1):
                return True
        elif self.direction == DOWN:
            if gold.x == self.coordinate[HEAD]['x'] and gold.y == (self.coordinate[HEAD]['y'] + 1):
                return True

    def set_left(self):
        if  self.direction != RIGHT:
            self.direction = LEFT

    def set_right(self):
        if  self.direction != LEFT:
            self.direction = RIGHT

    def set_up(self):
        if self.direction != DOWN:
            self.direction = UP

    def set_down(self):
        if self.direction != UP:
            self.direction = DOWN

    def move_to_direction(self, add):
        if not add:
            for i in range(1, len(self.coordinate)):
                bodyNow = self.coordinate[len(self.coordinate) - i]
                bodyBack = self.coordinate[len(self.coordinate) - (i + 1)]
                bodyNow['x'] = bodyBack['x']
                bodyNow['y'] = bodyBack['y']
        else:
            self.coordinate.insert(1, {'x': self.coordinate[HEAD]['x'], 'y': self.coordinate[HEAD]['y']})

        if self.direction == LEFT:
            self.coordinate[HEAD]['x'] -= 1
        elif self.direction == RIGHT:
            self.coordinate[HEAD]['x'] += 1
        elif self.direction == UP:
            self.coordinate[HEAD]['y'] -= 1
        elif self.direction == DOWN:
            self.coordinate[HEAD]['y'] += 1