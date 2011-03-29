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
    def handle_event(self,event):
        if(event.type == pygame.KEYDOWN):
            if(event.key == pygame.K_SPACE):
                print "Space bar pressed down."
            elif(event.key == pygame.K_ESCAPE):
                print "Escape key pressed down."
        elif(event.type == pygame.KEYUP):
            if(event.key == pygame.K_SPACE):
                print "Space bar released."
            elif(event.key == pygame.K_ESCAPE):
                print "Escape key released."
                pygame.quit()

    def update(self):
        self.clock.tick(50)
        for event in pygame.event.get():
            self.handle_event(event)

    def draw(self):
        self.screen.fill((0,0,0))
        for i in range(25):
            for j in range(25):
                self.screen.blit(self.bg,pygame.Rect(i*32,j*32,self.width,self.height),pygame.Rect(2*32,0,32,32))
g = Game()
while True:
    g.update()
    g.draw()
    pygame.display.flip()
