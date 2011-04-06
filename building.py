import pygame, math, random, operator, unit, sys, menu, soldier, queueitem, button
from vector import *     
        
        

class Building(unit.Unit):
    def __init__(self, x = 0.0, y = 0.0):
        self.clock = pygame.time.Clock()
        self.height = 75
        self.width = 75
        self.pos = Vector(x,y)
        self.selected = False
        self.unitQueue = []
        self.image = pygame.Surface((self.width, self.height), pygame.SRCALPHA, 32).convert_alpha()
        self.rect = pygame.Rect(0,0,self.width,self.height)
        self.buildMenu = None
        self.seconds = 0
        pygame.draw.rect(self.image, (225,225,0), self.rect)
        self.rect.center = self.pos.get()
    def update(self, delta_seconds):
        self.seconds += delta_seconds
        i = 0
        for u in self.unitQueue:
            print i
            if u.update(self.seconds, i) :
                pass
            else:
                self.unitQueue.pop(0)
            i += 1
                    
    def draw(self, screen):
        if self.buildMenu is None:
            self.buildMenu = menu.Menu(screen)
            self.buildMenu.bTakeInput = True
            font = pygame.font.Font(None, 36)
            text = font.render("Add", 1, (0,0,0))
            Click = button.AddToQueueOnClick()
            Click.queue = self.unitQueue
            self.buildMenu.addButton(536, 536, text, Click)
        self.buildMenu.update()
        
        #print delta_seconds
        self.image = pygame.Surface((self.width, self.height), pygame.SRCALPHA, 32).convert_alpha()
        self.rect = pygame.Rect(0,0,self.width,self.height)
        pygame.draw.rect(self.image,(225,225,0), self.rect)
        self.rect.center = self.pos.get()
        screen.blit(self.image, self.rect)

    def drawfocus(self, screen):
        pygame.draw.rect(self.image,(0, 225,225), self.rect)
        self.buildMenu.draw(screen)
        for u in self.unitQueue:
            u.draw(screen)
        self.rect.center = self.pos.get()
        screen.blit(self.image, self.rect)
        
        
    def clicked(self):
        if self.selected:
            self.selected = False
        else:
            self.selected = True

    
