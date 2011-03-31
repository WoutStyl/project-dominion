import pygame, math, random, operator, unit
from vector import *

class Bullet:
    def __init__(self, direction, x = 0.0, y = 0.0):
        self.speed = 720.0
        self.direction = direction
        self.height = 8
        self.width = 8
        self.pos = Vector(x,y)
        
        self.image = pygame.Surface((self.width, self.height), pygame.SRCALPHA, 32).convert_alpha()
        self.rect = pygame.Rect(0,0,self.width,self.height)
        
        pygame.draw.circle(self.image, (255,255,255), (self.width / 2, self.height / 2), self.width /2)
        self.rect.center = self.pos.get()
        
    def update(self, delta_seconds):
        self.pos += self.direction * self.speed * delta_seconds
        self.rect.center = self.pos.get()
    
    def draw(self, screen):
        screen.blit(self.image, self.rect)
