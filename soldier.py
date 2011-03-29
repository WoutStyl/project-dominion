import pygame, math, random, operator, unit
from vector import *

class Soldier(unit.Unit):
    def __init__(self, x = 0.0, y = 0.0):
        unit.Unit.__init__(self, x, y)
        
        self.speed = 45.0
        self.velocity = Vector(0.0,0.0)
        self.facing = Vector(0.0,1.0)
        self.health = 40
        
        self.refire_t = 2
        self.last_fire = 0
        self.fire_target = None
        
        self.anim = random.randint(0,200)
        self.anim_len = 100;
        
    def update(self, delta_seconds):
        self.anim += 1
        if self.anim > self.anim_len:
            self.anim = 0
        
        self.pos += self.velocity * self.speed * delta_seconds
        self.rect.center = self.pos.get()
        
        frame = self.anim * 4 / self.anim_len
        if frame == 0:
            self.move_direction("Right")
        elif frame == 1:
            self.move_direction("Down")
        elif frame == 2:
            self.move_direction("Left")
        else:
            self.move_direction("Up")
            
    def move_towards(self, other_unit):
        self.velocity = other_unit.pos - self.pos
        self.velocity.normalize()
        self.facing = Vector(self.velocity[0],self.velocity[1])
        
    def move_direction(self, direction):
        if direction == "Left":
            self.velocity = Vector(-1,0)
        elif direction == "Right":
            self.velocity = Vector(1,0)
        elif direction == "Up":
            self.velocity = Vector(0,-1)
        elif direction == "Down":
            self.velocity = Vector(0,1)
        elif direction == "UpLeft":
            self.velocity = Vector(-1,-1)
            self.velocity.normalize()
        elif direction == "UpRight":
            self.velocity = Vector(1,-1)
            self.velocity.normalize()
        elif direction == "DownLeft":
            self.velocity = Vector(-1,1)
            self.velocity.normalize()
        elif direction == "DownRight":
            self.velocity = Vector(1,1)
            self.velocity.normalize()
        self.facing = Vector(self.velocity[0],self.velocity[1])
        
    def stop(self):
        self.velocity = Vector(0.0,0.0)
        
    def fire_at(self, target):
        self.fire_target = target
            
    def is_within_distance(self, other_unit, distance):
        if self.rect.left > other_unit.rect.right:
            x1 = self.rect.left
            x2 = other_unit.rect.right
        elif self.rect.right < other_unit.rect.left:
            x1 = self.rect.right
            x2 = other_unit.rect.left
        else:
            x1 = self.pos[0]
            x2 = self.pos[0]
            
        if self.rect.top > other_unit.rect.bottom:
            y1 = self.rect.top
            y2 = other_unit.rect.bottom
        elif self.rect.bottom < other_unit.rect.top:
            y1 = self.rect.bottom
            y2 = other_unit.rect.top
        else:
            y1 = self.pos[1]
            y2 = self.pos[1]
            
        vec1 = Vector(x1,y1)
        vec2 = Vector(x2,y2)
        vec = vec1 - vec2
        
        return vec.length() <= distance
        
    def keep_on_screen(self, max_x, max_y):
        if self.rect.top <= 0 and self.velocity[1] < 0:
            self.velocity[1] = 0
        if self.rect.left <= 0 and self.velocity[0] < 0:
            self.velocity[0] = 0
        if self.rect.bottom >= max_y and self.velocity[1] > 0:
            self.velocity[1] = 0
        if self.rect.right >= max_x and self.velocity[0] > 0:
            self.velocity[0] = 0