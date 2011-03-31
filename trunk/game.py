import pygame, sys, string, random, math, operator, soldier, menu, button
        
class Game(object):
    screen_width=600
    screen_height=600  
    
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Project Dominion")
        cursor=pygame.cursors.compile(("   XX   ","   XX   ","   XX   ","XXXXXXXX","XXXXXXXX","   XX   ","   XX   ","   XX   "))
        pygame.mouse.set_cursor((8,8),(4,4),*cursor)

        
        
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        
        self.target = soldier.Soldier(0,0)
        self.target.image.fill((0,0,255))
        self.target.anim_len = 500
        
        self.enemies = []
        self.bullets = []
        for i in range(10):
            self.enemies.append(soldier.Soldier(random.randint(0,self.screen_width),random.randint(0,self.screen_height)))
        
    def update(self):
        self.clock.tick(50)
        delta_seconds = self.clock.get_time()/1000.0
        
        for event in pygame.event.get():
            self.handle_event(event)
        self.target.update(delta_seconds)
        self.target.keep_on_screen(self.screen_width,self.screen_height)
        for e in self.enemies:
            newbull = e.update(delta_seconds)
            if newbull is not None:
                self.bullets.append(newbull)
            e.keep_on_screen(self.screen_width,self.screen_height)
            e.fire_at(self.target, delta_seconds)
        for b in self.bullets:
            b.update(delta_seconds)
    def handle_event(self, event):
        if event.type == pygame.QUIT:
            sys.exit(0)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                sys.exit(0)
        
    def draw(self):
        self.screen.fill((0,0,0))
        self.target.draw(self.screen)
        for e in self.enemies:
            e.draw(self.screen)
        for b in self.bullets:
            b.draw(self.screen)
        
g = Game()

bInMenu = True
m = menu.Menu(g.screen)
oc = button.StartOnClick()
buttonlocx = g.screen_width/2
buttonlocx -= 128
buttonlocy = g.screen_height/2
buttonlocy -= 96
#print buttonlocx
#print buttonlocy
font = pygame.font.Font(None, 36)
text = font.render("", 1, (0,0,0))
m.addButton(buttonlocx, (buttonlocy -128), text, button.StartOnClick(), "StartCampaign")
m.addButton(buttonlocx,buttonlocy,text, button.MissionSelectOnClick(), "StartMission")
m.addButton(buttonlocx,(buttonlocy+128),text, button.SavedCampaignSelectOnClick(), "LoadCampaign")
m.addButton(buttonlocx,(buttonlocy+256),text, button.SavedMissionSelectOnClick(), "LoadMission")
print m.index
while m.bInMenu:
    m.update()
    g.screen.fill((0,0,0))
    m.draw(g.screen)
    pygame.display.flip()
    

while 1:
    g.update()
    g.draw()
    pygame.display.flip()
