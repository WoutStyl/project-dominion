import pygame, math, random, operator
from vector import *

class Unit:
    def __init__(self, x = 0.0, y = 0.0):
        self.height = 32
        self.width = 32
        self.pos = Vector(x,y)
        
        self.image = pygame.Surface((self.width, self.height), pygame.SRCALPHA, 32).convert_alpha()
        self.rect = pygame.Rect(0,0,self.width,self.height)
        
        pygame.draw.circle(self.image, (255,0,0), (self.width / 2, self.height / 2), self.width /2)
        self.rect.center = self.pos.get()
        
    def update(self, delta_seconds):
        pass
                
    def draw(self, screen):
        screen.blit(self.image, self.rect)