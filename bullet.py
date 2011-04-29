import pygame, math, random, operator, unit
from vector import *
#Responsibilities
#Updates World Position
#Draws the bullet

#Collaborators
#Surface

class Bullet:
    def __init__(self, direction, x = 0.0, y = 0.0):
        self.speed = 720.0
        self.direction = direction
        self.height = 8
        self.width = 8
        self.pos = Vector(x,y)
        self.dead = False
        self.image = pygame.Surface((self.width, self.height), pygame.SRCALPHA, 32).convert_alpha()
        self.rect = pygame.Rect(0,0,self.width,self.height)
        self.timer = 0.0
        pygame.draw.circle(self.image, (255,255,255), (self.width / 2, self.height / 2), self.width /2)
        self.rect.center = self.pos.get()
        
    def update(self, delta_seconds):
        # Only update if we're not 'dead'
        if self.dead == False:
            self.timer += delta_seconds
            # Kill the bullet after 0.5 seconds
            if self.timer >= .5:
                self.dead = True
            self.pos += self.direction * self.speed * delta_seconds
            self.rect.center = self.pos.get()
            
    def die(self):
        self.dead = True
        del self.image
        del self.rect
        
    def draw(self, screen):
        print(self.dead)
        if self.dead == False:
            screen.blit(self.image, self.rect)
