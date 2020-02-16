import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame
import sys
from Actor import Actor
from random import randint
from Directions import Directions
from Snake import Snake

class AppleGenerator():
    #Find better spawning algorithm that makes sure it spawns away from the
    #snake, and that it spawns snapped to a grid
    @staticmethod
    def generate():
        (x,y) = (int(randint(0,320)),int(randint(0,320)))
        return (x,y)

class Game:
    def __init__(self, screen_size ,fps, tile_size):
        self.win = self.createDisplay(screen_size,screen_size,"Cobra")
        self.w, self.h = screen_size, screen_size
        self.clock = pygame.time.Clock()
        self.tile_size = tile_size
        self.snake = Snake(0, self.h//2, Directions.right, tile_size)
        self.actors = [self.snake]
        self.bg_color = (0,0,0)
        self.base_fps = fps
        self.fast_fps = fps * 2
        self.fps = self.base_fps
        self.score = 0
        self.apple = (self.h//2, self.w//2)
        self.padding = tile_size // 2
        self.paused = False

    def createDisplay(self,height, width, title=None):
        win = pygame.display.set_mode((width,height), pygame.RESIZABLE)
        if title != None:
            pygame.display.set_caption(title)
        return win

    def init(self):
        """intializes pygame code"""
        pygame.init()

    def close(self):
        pygame.quit()
        pygame.display.quit()


    def reset(self):
        "Resets all data and places the player at starting pos"
        self.snake = Snake(0, self.h//2, Directions.right, self.tile_size)
        self.actors[0] = self.snake
        self.score = 0
        self.apple = (self.h//2, self.w//2)
        self.fps = self.base_fps

    def mainLoop(self):
        #initialization
        self.init()
       
        keys = []
        runLoop = True

        self.paused = False
        apple = AppleGenerator.generate()
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
                if(self.fps == self.base_fps):
                    self.fps = self.fast_fps
                else:
                    self.fps = self.base_fps
            elif keys[pygame.K_r]:
                self.reset()
            
            if not self.paused:

                if(self.apple[0] >= (self.snake.segments[0][0] - self.padding) and 
                   self.apple[0] <= (self.snake.segments[0][0] + self.padding) and 
                   self.apple[1] >= (self.snake.segments[0][1] - self.padding) and 
                   self.apple[1] <= (self.snake.segments[0][1] + self.padding)):
                    self.snake.eat()
                    self.apple = AppleGenerator.generate()

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
                pygame.draw.rect(self.win,(0,255,0),(self.apple[0],self.apple[1],10,10))
                for s in self.snake.segments:
                    pygame.draw.rect(self.win, (0, 0, 255), 
                                     (s[0], s[1], self.tile_size,self.tile_size))
                pygame.display.update()

        self.close()
 
