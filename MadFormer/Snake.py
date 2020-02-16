from Actor import Actor
from Directions import Directions

class Snake(Actor):
    def __init__(self, x, y, direction, tile_size):
        self._dir = direction
        self.tile_size = tile_size
        #change to deque
        self.segments = [(x,y)]
        self.speed = 0.3 # tiles per tick (e.g 0.03 tpt*34 = 1 tps)

    def update(self):
        
        #To move the snake we pop the end piece of its tail
        #and add a new piece to its front
        new_head_x, new_head_y = self.segments[0][0], self.segments[0][1]
        new_head_x += self.dir_to_int()[0] * self.speed * self.tile_size
        new_head_y += self.dir_to_int()[1] * self.speed * self.tile_size
        
        self.segments.pop()
        self.segments.insert(0, (new_head_x, new_head_y))

        
    def eat(self):
        self.add_tail_piece()

    def add_tail_piece(self):
        x = self.segments[-1][0] * self.dir_to_int()[0]
        y = self.segments[-1][1] * self.dir_to_int()[1]

        self.segments.append((x,y))

    def dir_to_int(self):
        hor,ver = 0,0
        if(self._dir == Directions.up):
            ver = -1
        elif(self._dir == Directions.down):
            ver = 1
        elif(self._dir == Directions.right):
            hor = 1
        elif(self._dir == Directions.left):
            hor = -1

        return [hor,ver]

    @property
    def dir(self):
        return self._dir

    @dir.setter
    def dir(self, dir):
        if (self._dir == Directions.up and dir != Directions.down or 
            self._dir == Directions.down and dir != Directions.up or 
            self._dir == Directions.left and dir != Directions.right or 
            self._dir == Directions.right and dir != Directions.left):
           self._dir = dir

