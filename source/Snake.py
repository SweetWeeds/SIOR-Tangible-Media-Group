import random, pygame, sys
import numpy as np
from pygame.locals import *

from worm import Worm
from gold import Gold

UP = 'up'
DOWN = 'down'
LEFT = 'left'
RIGHT = 'right'

class Snake:
    def __init__(self, fps = 2, cell_size = 10):
    
        self.fps = fps
        self.cell_size = cell_size
        self.map = np.zeros((cell_size, cell_size), np.uint8)
            
        pygame.init()
        self.fps_clock = pygame.time.Clock()
        
    def get_key_event(self):
        #get only the first key event during a frame
        events = pygame.event.get()
        key_down_events = [event for event in events if event.type == KEYDOWN]
        if key_down_events:
            return key_down_events[0]
        else:
            None

    def start(self):
        self.worm = Worm(self.cell_size)
        self.gold = Gold(self.cell_size)

        #check object is overlapped
        if self.check_overlapped_object():
            self.gold.set_position(self.get_empty_position())

        while True:
            """
            self.worm.set_left()
            self.worm.set_right()
            self.worm.set_up()
            self.worm.set_down()
            """

            #if there is gold ahead the worm.
            if self.worm.check_ahead_gold(self.gold):
                #move forward and reposition gold
                self.worm.move_to_direction()
                self.gold.set_position(self.get_empty_position())
            #if there is nothing ahead the worm.
            else:
                #just move forward
                self.worm.move_to_direction()
            #if worm collides with the edge or worm body,
            if self.worm.check_collision():
                return
            
            self.draw_matrix()
            self.fps_clock.tick(self.fps)

    def draw_matrix(self):
        self.map = np.zeros((self.cell_size, self.cell_size), np.uint8)
        for wormBody in self.worm.coordinate:
            self.map[wormBody['y']][wormBody['x']] = 255 // 2
        self.map[self.gold.y][self.gold.x] = 255
        print(self.map)


    def check_worm_dead(self):
        if len(self.worm.coordinate) == 1:
            return True
        return False

    def check_overlapped_object(self):
        #check gold
        for wormBody in self.worm.coordinate:
            if wormBody['x'] == self.gold.x and wormBody['y'] == self.gold.y:
                return True

    def get_empty_position(self):
        positions = []
        for x in range(self.cell_size):
            for y in range(self.cell_size):
                positions.append([x,y])

        for wormBody in self.worm.coordinate:
            positions.remove([wormBody['x'], wormBody['y']])

        if [self.gold.x, self.gold.y] in positions:
            positions.remove([self.gold.x, self.gold.y])

        return positions[random.randint(0, len(positions) - 1 )]

    def terminate(self):
        pygame.quit()
        sys.exit()

    def checkForKeyPress(self):
        if len(pygame.event.get(QUIT)) > 0:
            self.terminate()

        keyUpEvents = pygame.event.get(KEYUP)
        if len(keyUpEvents) == 0:
            return None
        if keyUpEvents[0].key == K_ESCAPE:
            self.terminate()
        return keyUpEvents[0].key

if __name__ == '__main__':
    wormy = Snake()
    wormy.start()
    wormy.terminate()