import pygame, math, random, operator
from vector import *

class Unit:
    def __init__(self, x , y):
        self.height = 32
        self.width = 32
        self.pos = Vector(float(x),float(y))
        
        self.image = pygame.Surface((self.width, self.height), pygame.SRCALPHA, 32).convert_alpha()
        self.focus = pygame.Surface((self.width, self.height), pygame.SRCALPHA, 32).convert_alpha()
        self.rect = pygame.Rect(0,0,self.width,self.height)
        
        pygame.draw.circle(self.image, (255,0,0), (self.width / 2, self.height / 2), self.width /2)
        pygame.draw.circle(self.focus, (0,255,0), (self.width / 2, self.height / 2), self.width /2 + 5, 3)
        #self.rect.move_ip(float(x),float(y))
        self.rect.center = (self.pos.get()[0],self.pos.get()[1])
        #print "x is "
        #print x
        #raw_input('')
        
    def update(self, delta_seconds):
        pass
                
    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def drawfocus(self, screen):
        screen.blit(self.focus,self.rect)

    def keep_on_screen(self,width,height):
        pass
  
    def fire_at(self,target):
        pass