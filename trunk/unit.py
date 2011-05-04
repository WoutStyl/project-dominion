import pygame, math, random, operator
from vector import *

# Collaborators:
#   none
# Responsibilities:
#   governs an individual units status

class Unit(object):
    width = 32
    height = 32
    type = "Unit"
    
    @staticmethod
    def get_size():
        return Unit.width, Unit.height
    
    def __init__(self, x = 0, y = 0, protocol = None, color = (255,0,0)):
        self.pos = Vector(float(x),float(y))
        self.health = 5
        self.image = pygame.Surface((self.width, self.height), pygame.SRCALPHA, 32).convert_alpha()
        # The image overlayed on the unit when it's selected
        self.focus = pygame.Surface((self.width, self.height), pygame.SRCALPHA, 32).convert_alpha()
        self.rect = pygame.Rect(0,0,self.width,self.height)
        
        # Images are just circles for now
        pygame.draw.circle(self.image, color, (self.width / 2, self.height / 2), self.width /2)
        pygame.draw.circle(self.focus, (0,255,0), (self.width / 2, self.height / 2), self.width /2 + 5, 3)
        #self.rect.move_ip(float(x),float(y))
        self.rect.center = (self.pos.get()[0],self.pos.get()[1])
        
        self.isSelected = False
        #print "x is "
        #print x
        #raw_input('')
        self.unitMenu = "Standard"
        self.protocol = protocol
    def take_damage(self, damage):
        self.health -= damage;
        if self.health <= 0:
            self.die();
    def die(self):
        del self.image
        del self.rect
    def is_dead(self):
        if self.health <=0:
            return True
        return False
    def update(self, delta_seconds):
        pass
                
    def draw(self, screen):
        screen.blit(self.image, self.rect)
        
        if self.isSelected:
            screen.blit(self.focus,self.rect)
        
    # Whether or not the unit has been selected by the player
    def set_selected(self, value):
        self.isSelected = value

    def keep_on_screen(self,width,height):
        pass
        
    def get_type(self):
        return self.type
  
    def fire_at(self,target):
        pass
        
    def get_pos(self):
        return self.pos.get()
        
    def set_protocol(self, p):
        self.protocol = p
        
    def set_color(self, color):
        pygame.draw.circle(self.image, color, (self.width / 2, self.height / 2), self.width /2)
        
    def collide_terrain(self, rect, value):
        if not value:
            return self.collide_rect(rect)
        return False
    
    def collide_unit(self, unit):
        if self == unit:
            return False
        return self.collide_rect(unit.rect)
        
    def collide_rect(self, rect):
        return self.rect.colliderect(rect)