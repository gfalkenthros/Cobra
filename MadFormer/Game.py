import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame
import sys
from Actor import Actor
from random import randint
from Directions import Directions
from Snake import Snake

class AppleGenerator():
    def __init__(self, map_size, tile_size):
        self.map_size = map_size
        self.tile_size = tile_size
        self.num_tiles = map_size // tile_size

    def generate(self):
        (x,y) = (randint(0,self.num_tiles-1)*self.tile_size,
                 randint(0,self.num_tiles-1)*self.tile_size)
        return (x,y)

class Game:
    def __init__(self, screen_size , tile_size, fps=30):
        self.win = self.createDisplay(screen_size,screen_size,"Cobra")
        self.w, self.h = screen_size, screen_size
        self.clock = pygame.time.Clock()
        self.tile_size = tile_size
        self.snake = Snake(0, self.h//2, Directions.right, tile_size)
        self.actors = [self.snake]
        self.bg_color = (0,0,0)
        self.base_speed = 0.2
        self.fast_speed = self.base_speed * 2
        self.fps = fps
        self.score = 0
        self.apple = (self.h//2, self.w//2)
        self.padding = tile_size // 2
        self.paused = False
        self.apple_gen = AppleGenerator(self.h, self.tile_size)

    def create_text(self, text):
        textsurface = self.font.render(text, False, (255, 255, 255))
        return textsurface

    def createDisplay(self,height, width, title=None):
        win = pygame.display.set_mode((width,height), pygame.RESIZABLE)
        if title != None:
            pygame.display.set_caption(title)
        return win

    def init(self):
        """intializes pygame code"""
        pygame.init()
        self.font = pygame.font.SysFont('Comic Sans MS', 15)


    def close(self):
        pygame.quit()
        pygame.display.quit()


    def reset(self):
        "Resets all data and places the player at starting pos"
        self.snake = Snake(0, self.h//2, Directions.right, self.tile_size)
        self.actors[0] = self.snake
        self.score = 0
        self.apple = (self.h//2, self.w//2)
        self.fps = self.fps

    def mainLoop(self):
        #initialization
        self.init()
       
        keys = []
        runLoop = True

        self.paused = False
        apple = self.apple_gen.generate()
        apple_scale = 0.8
        #add scene object

        while runLoop:
            self.clock.tick(self.fps)
            events = pygame.event.get()
            keys = pygame.key.get_pressed()

            #Check for events
            for event in events:
                if event.type == pygame.QUIT:
                    runLoop = False

            #User input
            if keys[pygame.K_ESCAPE]:
                pygame.event.post(pygame.event.Event(pygame.QUIT))
            if keys[pygame.K_w]:
                self.snake.dir = Directions.up 
            elif keys[pygame.K_s]:
                self.snake.dir = Directions.down
            elif keys[pygame.K_a]:
                self.snake.dir = Directions.left
            elif keys[pygame.K_d]:
                self.snake.dir = Directions.right
            elif keys[pygame.K_SPACE]:
                self.paused = not self.paused
            elif keys[pygame.K_TAB]:
                if(self.snake.speed == self.base_speed):
                    self.snake.speed = self.fast_speed
                else:
                    self.snake.speed = self.base_speed
            elif keys[pygame.K_r]:
                self.reset()
            
            if not self.paused:

                if(self.apple[0] >= (self.snake.segments[0][0] - self.padding) and 
                   self.apple[0] <= (self.snake.segments[0][0] + self.padding) and 
                   self.apple[1] >= (self.snake.segments[0][1] - self.padding) and 
                   self.apple[1] <= (self.snake.segments[0][1] + self.padding)):
                    self.snake.eat()
                    self.score += 1
                    self.apple = self.apple_gen.generate()

                #Logic
                for actor in self.actors:
                    actor.update()

            
                #If snake has tail check for collision
                if len(self.snake.segments) > 1:
                    for i in range(1,len(self.snake.segments)):
                        if (self.snake.segments[0][0] == self.snake.segments[i][0] and 
                            self.snake.segments[0][1] == self.snake.segments[i][1]): 
                                runLoop = False

                #Grahpics
                self.win.fill(self.bg_color)
                pygame.draw.rect(self.win,(0,255,0),(self.apple[0],self.apple[1],
                                                     self.tile_size*apple_scale,self.tile_size*apple_scale))
                for s in self.snake.segments:
                    pygame.draw.rect(self.win, (0, 0, 255), 
                                     (s[0], s[1], self.tile_size,self.tile_size))
                self.win.blit(self.create_text("Score: " + str(self.score)),(0,0))
                
                pygame.display.update()

        self.close()
 
