import pygame, math, random, operator
from vector import *

class Unit(object):
    def __init__(self, x = 0, y = 0, color = (255,0,0)):
        self.height = 32
        self.type = "Unit"
        self.width = 32
        self.pos = Vector(float(x),float(y))
        
        self.image = pygame.Surface((self.width, self.height), pygame.SRCALPHA, 32).convert_alpha()
        self.focus = pygame.Surface((self.width, self.height), pygame.SRCALPHA, 32).convert_alpha()
        self.rect = pygame.Rect(0,0,self.width,self.height)
        
        pygame.draw.circle(self.image, color, (self.width / 2, self.height / 2), self.width /2)
        pygame.draw.circle(self.focus, (0,255,0), (self.width / 2, self.height / 2), self.width /2 + 5, 3)
        #self.rect.move_ip(float(x),float(y))
        self.rect.center = (self.pos.get()[0],self.pos.get()[1])
        
        self.isSelected = False
        #print "x is "
        #print x
        #raw_input('')
        self.buildMenu = None
        
    def update(self, delta_seconds):
        pass
                
    def draw(self, screen):
        screen.blit(self.image, self.rect)
        
        if self.isSelected:
            screen.blit(self.focus,self.rect)
        
    def set_selected(self, value):
        self.isSelected = value

    def keep_on_screen(self,width,height):
        pass
  
    def fire_at(self,target):
        pass
