import pygame

class Game(object):
    tileimage = 'tileset.PNG'
    screen_width = 8192
    screen_height = 8192
    width = 800
    height = 800

    def __init__(self):
        pygame.init()
        pygame.display.set_caption("lol")

        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode((self.width,self.height))
        self.bg = pygame.image.load(self.tileimage).convert()

    def update(self):
        self.clock.tick(50)

    def draw(self):

        for i in range(256):
            for j in range(256):
                self.screen.blit(self.bg,pygame.Rect(0,0,self.width,self.height),pygame.Rect(2*32,0,3*32-1,32))
		print "added a tile"
                
g = Game()
while True:
    g.update()
    g.draw()
    pygame.display.flip()
