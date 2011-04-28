import pygame, math, random, operator, unit, sys, menu, soldier, queueitem, button
from vector import *     
        
        
#Responsibilities
#Keep track of building related data (mainly queue)
#Update the queue
#Draw the building
#Spawn the units

#Collaborators
#Units
#Surface
#Map

class Building(unit.Unit):
    def __init__(self, x = 0.0, y = 0.0, color = (225,0,0)):
        super(Building, self).__init__(x,y,color)
        self.height = 75
        self.width = 75
        self.type = "Building"
        
        self.image = pygame.Surface((self.width, self.height), pygame.SRCALPHA, 32).convert_alpha()
        self.rect = pygame.Rect(0,0,self.width,self.height)
        pygame.draw.rect(self.image,color, self.rect)
        self.rect.center = self.pos.get()
        
        self.unitQueue = []
        
        self.buildMenu = menu.Menu()
        font = pygame.font.Font(None, 36)
        text = font.render("Add", 1, (0,0,0))
        Click = button.AddToQueueOnClick(self)
        self.buildMenu.add_button(536, 536, text, Click)
        
        self.seconds = 0
        
    def update(self, delta_seconds):
        self.seconds += delta_seconds
        i = 0
        for u in self.unitQueue:
            if not u.update(self.seconds, i) :
                self.unitQueue.pop(0)
            i += 1
            
        if self.isSelected:
            self.buildMenu.update()
                    
    def draw(self, screen):
        super(Building, self).draw(screen)
        if self.isSelected:
            pygame.draw.rect(self.image,(0, 225,225), self.rect)
            #for u in self.unitQueue:
                #u.draw(screen)
            self.rect.center = self.pos.get()
            screen.blit(self.image, self.rect)
        
        
    def clicked(self):
        if self.selected:
            self.selected = False
        else:
            self.selected = True
    
    def add_to_queue(self):
        self.unitQueue.append(queueitem.QueueItem(len(self.unitQueue)))
    
