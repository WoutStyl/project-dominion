import pygame, math, random, operator, unit, sys, soldier
from vector import *

class QueueItem():
    def __init__(self, queue):
        self.buildComplete = False
        self.x = 16 + (32 * (len(queue)-1))
        self.y = 552
        #self.unit = unit
        self.pos = Vector(self.x,self.y)
        self.loadbarPos = Vector(self.x-16,self.y+21)
        self.startTime = -1
        self.currentTime = 0
        self.timeDiff = ((self.currentTime - self.startTime)*3.2)
        #self.endTime = delta_seconds + 10
        #Image for Unit Icon
        self.image = pygame.Surface((32,32),pygame.SRCALPHA, 32).convert_alpha()
        self.rect = pygame.Rect(0,0,32,32)
        pygame.draw.rect(self.image, (225,0,0), self.rect)
        self.rect.center = self.pos.get()
        self.listIndex = len(queue)-1

        #Image for Load Bar
        #self.loadbarImage = pygame.Surface((self.timeDiff, 5), pygame.SRCALPHA, 32).convert_alpha()
        #self.loadbarRect = pygame.Rect(0,0,self.timeDiff, 5)
        self.loadbarImage = pygame.Surface((self.timeDiff+1, 10), pygame.SRCALPHA, 32).convert_alpha()
        self.loadbarRect = pygame.Rect(0,0,self.timeDiff+1, 10)
        pygame.draw.rect(self.loadbarImage, (225,225,0), self.loadbarRect)
        self.loadbarRect.topleft = self.loadbarPos.get()
        
    def update(self, delta_seconds, i):
        self.listIndex = i
        self.x = 16 + (32 * i)
        self.pos = Vector(self.x,self.y)
        self.rect.center = self.pos.get()
        if i is 0:
            if self.startTime is -1:
                self.startTime = delta_seconds
            self.loadbarPos = Vector(self.x-16,self.y+21)
            self.currentTime = delta_seconds
            self.timeDiff = (self.currentTime - self.startTime) *3.2
            if self.timeDiff <= 32:
                self.loadbarImage = pygame.Surface((self.timeDiff+1, 10), pygame.SRCALPHA, 32).convert_alpha()
                self.loadbarRect = pygame.Rect(0,0,self.timeDiff+1, 10)
                pygame.draw.rect(self.loadbarImage, (225,225,0), self.loadbarRect)
                self.loadbarRect.topleft = self.loadbarPos.get()
                return True
            else:
                self.buildComplete = True
                return False
        else:
            return True
        
        
    def draw(self, screen): 
        screen.blit(self.image, self.rect)
        if self.listIndex is 0:
            screen.blit(self.loadbarImage, self.loadbarRect)
