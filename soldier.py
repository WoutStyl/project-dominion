import pygame, math, random, operator, unit, bullet, function, variable, map
from vector import *

class Soldier(unit.Unit):
    commands = {}
    
    def __init__(self, x = 0, y = 0, protocol = None, color = (255,0,0)):
        unit.Unit.__init__(self, x, y, protocol, color)
        
        self.speed = 45.0
        self.velocity = Vector(0.0,0.0)
        self.current_velocity = Vector(0.0,0.0)
        self.facing = Vector(0.0,1.0)
        self.health = 40
        self.waitTime = 0
        
        self.refireT = 5.0
        self.lastFire = 5.0
        self.fireTarget = None
        self.pDir = None
        self.fire = False
        
        self.anim = random.randint(0,200)
        self.animLen = 100;
        self.waitTime = 0
        
        
        
        
    def update(self, deltaSeconds):
        # Only fire at the given interval
        if self.lastFire >= self.refireT:
            self.lastFire = 0
        if self.lastFire >0:
            self.lastFire +=deltaSeconds
        
        # Move the player
        self.pos += self.current_velocity * self.speed * deltaSeconds
        self.update_position(self.pos.get())
        self.current_velocity = Vector(self.velocity[0],self.velocity[1])
        
        # Don't execute protocols while 'waiting'
        if self.waitTime > 0:
            self.waitTime -= deltaSeconds
        else:
            self.waitTime = 0

            if self.protocol !=None:
                    self.protocol = self.protocol.execute(self)
                
        # If it's time to fire
        if self.lastFire == 0 and self.fire == True:
            if self.fireTarget.is_dead():
                self.fire = False
                return None
            self.lastFire += deltaSeconds
            tPos = self.fireTarget.pos
            tVel = self.fireTarget.velocity * self.fireTarget.speed
            pPos = tPos + tVel   #projected position of the target
            self.pDir = pPos - self.pos
            self.pDir.normalize()       #direction to the projected position of the target
            self.fire = True
            #self.last_fire = 1
            return bullet.Bullet(self.pDir, self.pos[0], self.pos[1])
        return None
            
    def update_position(self, pos):
        self.pos[0] = pos[0]
        self.pos[1] = pos[1]
        self.rect.center = pos

    # Constrain the unit to the playable world
    def keep_on_screen(self, max_x, max_y):
        if self.rect.top <= 0 and self.velocity[1] < 0:
            self.velocity[1] = 0
        if self.rect.left <= 0 and self.velocity[0] < 0:
            self.velocity[0] = 0
        if self.rect.bottom >= max_y and self.velocity[1] > 0:
            self.velocity[1] = 0
        if self.rect.right >= max_x and self.velocity[0] > 0:
            self.velocity[0] = 0

    def draw(self, screen):
        super(Soldier, self).draw(screen)
        screen.blit(self.image, self.rect)
        if self.isSelected:
            #self.buildMenu.draw(screen)
            self.rect.center = self.pos.get()
            screen.blit(self.image, self.rect)
            
    def collide_rect(self, rect):
        if self.rect.colliderect(rect):
            if self.velocity[0] >= 0:
                diffX = self.rect.right - rect.left
            else:
                diffX = rect.right - self.rect.left
                
            if self.velocity[1] >= 0:
                diffY = self.rect.bottom - rect.top
            else:
                diffY = rect.bottom - self.rect.top
                
            if diffY >= diffX:
                self.current_velocity[0] = 0.0
            else:
                self.current_velocity[1] = 0.0
            return True
        return False
            
            
#Protocol Commands
    def move_towards(self, arguments):
        target = arguments["target"]
        if target == None:
            return
        self.velocity = target.pos - self.pos
        self.velocity.normalize()
        self.facing = Vector(self.velocity[0],self.velocity[1])
        
    def move_direction(self, arguments):
        direction = arguments["direction"]
        #print "Moving in direction ", direction
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
        
    def stop(self, arguments):
        #print "stopping"
        self.velocity = Vector(0.0,0.0)
        
    def fire_at(self, arguments):
        target = arguments["target"]
        if target is not None:
            self.fire = True
            self.fireTarget = target
        else:
            self.fire = False
            
    def stop_firing(self, arguments):
        self.fire_at({"target":None})

    def wait(self, arguments):
        #print "wait for me"
        self.waitTime = arguments["seconds"]
    def is_within_distance(self, arguments):
        target = arguments["target"]
        distance = arguments["distance"]
        if target == None:
            return False
            
        if self.rect.left > target.rect.right:
            x1 = self.rect.left
            x2 = target.rect.right
        elif self.rect.right < target.rect.left:
            x1 = self.rect.right
            x2 = target.rect.left
        else:
            x1 = self.pos[0]
            x2 = self.pos[0]
            
        if self.rect.top > target.rect.bottom:
            y1 = self.rect.top
            y2 = target.rect.bottom
        elif self.rect.bottom < target.rect.top:
            y1 = self.rect.bottom
            y2 = target.rect.top
        else:
            y1 = self.pos[1]
            y2 = self.pos[1]
            
        vec1 = Vector(x1,y1)
        vec2 = Vector(x2,y2)
        vec = vec1 - vec2
        return vec.length() <= distance
        
# A static list which defines the functions and arguments available
# for use in protocols. Parsed by the protocol editor
Soldier.commands = {"Move Towards":         ["",
                                             Soldier.move_towards,
                                             {"target": "Unit"}],
                    "Move Direction":       ["",
                                             Soldier.move_direction,
                                             {"direction": "String"}],
                    "Stop":                 ["",
                                             Soldier.stop,
                                             {}],
                    "Fire At":              ["",
                                             Soldier.fire_at,
                                             {"target": "Unit"}],
                    "Stop Firing":          ["",
                                             Soldier.stop_firing,
                                             {}],
                    "Wait":                 ["",
                                             Soldier.wait,
                                             {"seconds": "Integer"}],
                    "Is Within Distance":   ["Bool",
                                             Soldier.is_within_distance,
                                             {"target": "Unit", "distance": "Integer"}],
                    "Get An Enemy Unit":    ["Unit",
                                             map.Map.get().get_an_enemy_unit,
                                             {}]
                    }
