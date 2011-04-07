import pygame, math, random, operator, unit, sys, menu, soldier, queueitem, button
from vector import *     
        
        

class Building(unit.Unit):
    def __init__(self, x = 0.0, y = 0.0, color = (225,0,0)):
        super(Building, self).__init__(x,y,color)
        self.height = 75
        self.width = 75
        
        self.image = pygame.Surface((self.width, self.height), pygame.SRCALPHA, 32).convert_alpha()
        self.rect = pygame.Rect(0,0,self.width,self.height)
        pygame.draw.rect(self.image,color, self.rect)
        self.rect.center = self.pos.get()
        
        self.unitQueue = []
        self.buildMenu = None
        self.seconds = 0
        
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
            Click.set_queue(self.unitQueue)
            self.buildMenu.add_button(536, 536, text, Click)
        self.buildMenu.update()
        
        #print delta_seconds
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
    

    
