import pygame, math, random, operator, unit, sys, menu, soldier, queueitem, button, map
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
    width = 75
    height = 75
    type = "Building"
    def __init__(self,player, x = 0.0, y = 0.0, color = (225,0,0)):
        super(Building, self).__init__(x,y,None,color)
        self.player = player
        self.height = 75
        self.width = 75
        self.type = "Building"
        self.health = 40
        self.image = pygame.Surface((self.width, self.height), pygame.SRCALPHA, 32).convert_alpha()
        self.focus = pygame.Surface((self.width, self.height), pygame.SRCALPHA, 32).convert_alpha()
        self.rect = pygame.Rect(0,0,self.width,self.height)
        pygame.draw.rect(self.image,color, self.rect)
        pygame.draw.circle(self.focus, (0,255,0), (self.width / 2, self.height / 2), self.width / 2 + 12, 5)
        
        self.rect.center = self.pos.get()
        
        self.unitQueue = []
        
        self.unitMenu = "Build"
        
        self.seconds = 0
        
    # Update the time passed on the unitQueue and pop when
    # necessary
    def update(self, delta_seconds):
        self.seconds += delta_seconds
        i = 0
        for u in self.unitQueue:
            if not u.update(self.seconds, i) :
                self.spawn_unit()
                self.unitQueue.pop(0)
            i += 1
                    
    def draw(self, screen):
        super(Building, self).draw(screen)
        if self.isSelected:
            screen.blit(self.focus, self.rect)
            #for u in self.unitQueue:
                #u.draw(screen)
            
    def spawn_unit(self):
        width,height = soldier.Soldier.get_size()
        rect = pygame.Rect(0,0,width,height)
        pos = self.pos.get()
        newUnit = soldier.Soldier(pos[0],pos[1],self.protocol)
        
        theMap = map.Map.get()
        screen = pygame.display.get_surface()
        i = 0
        total = 8
        while theMap.collision(newUnit):
            if i == 0:
                print "first one"
                pos[0] += width
                pos[1] -= height
            if int(i * 4 / total) == 0:
                print "go down"
                pos[1] += height
            elif int(i * 4 / total) == 1:
                print "go left"
                pos[0] -= width
            elif int(i * 4 / total) == 2:
                print "go up"
                pos[1] -= height
            elif int(i * 4 / total) == 3:
                print "go right"
                pos[0] += width
            rect.center = pos
            if screen.get_rect().contains(rect):
                print "update"
                newUnit.update_position(pos)
            if i == total:
                i = 0
                total += 8
            else:
                i += 1
        map.Map.get().spawn_unit(self.player, newUnit)
        
    def clicked(self):
        if self.selected:
            self.selected = False
        else:
            self.selected = True
    
    def add_to_queue(self):
        self.unitQueue.append(queueitem.QueueItem(len(self.unitQueue)))
    
    def get_unit_queue(self):
        return self.unitQueue