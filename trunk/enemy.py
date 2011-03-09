import pygame, math, random, operator

class Enemy:
    def __init__(self, x = 0.0, y = 0.0):
        self.height = 32
        self.width = 32
        self.speed = 45.0
        self.pos = [x,y]
        self.velocity = [0.0,0.0]
        self.anim = random.randint(0,200)
        self.anim_len = 100;
        
        self.image = pygame.Surface((self.width, self.height), pygame.SRCALPHA, 32).convert_alpha()
        self.rect = pygame.Rect(0,0,self.width,self.height)
        
        pygame.draw.circle(self.image, (255,0,0), (self.width / 2, self.height / 2), self.width /2)
        self.rect.center = self.pos
        
    def update(self, delta_seconds):
        self.anim += 1
        if self.anim > self.anim_len:
            self.anim = 0
        
        self.pos[0] += self.speed * self.velocity[0] * delta_seconds
        self.pos[1] += self.speed * self.velocity[1] * delta_seconds
        self.rect.center = self.pos
        
        frame = self.anim * 4 / self.anim_len
        if frame == 0:
            self.velocity = [1.0,0.0]
        elif frame == 1:
            self.velocity = [0.0,1.0]
        elif frame == 2:
            self.velocity = [-1.0,0.0]
        else:
            self.velocity = [0.0,-1.0]
                
    def draw(self, screen):
        screen.blit(self.image, self.rect)
        
    def is_on_screen(self, max_x, max_y):
        if self.rect.top <= 0 and self.velocity[1] < 0:
            self.velocity[1] = 0
        if self.rect.left <= 0 and self.velocity[0] < 0:
            self.velocity[0] = 0
        if self.rect.bottom >= max_y and self.velocity[1] > 0:
            self.velocity[1] = 0
        if self.rect.right >= max_x and self.velocity[0] > 0:
            self.velocity[0] = 0