import pygame, menu, button, math, protocolitem, function, variable

class ProtocolEditor(menu.Menu):
    def __init__(self):
        super(ProtocolEditor, self).__init__()
        self.stealInput = True
        self.protocolItems = []
        self.links = {}
        
        self.startIndex = 0
        self.startName = ""
        self.endIndex = 0
        self.endName = ""
        
        screen = pygame.display.get_surface()
        self.createBar = pygame.Surface((screen.get_width()/8, screen.get_height()), pygame.SRCALPHA, 32).convert_alpha()
        self.createBar.fill((100,100,100))
        self.selectBar = pygame.Surface((screen.get_width()/8, screen.get_height()), pygame.SRCALPHA, 32).convert_alpha()
        self.selectBar.fill((200,200,200))
        
        self.createBarRect = self.createBar.get_rect()
        self.createBarRect.topleft = (0,0)
        self.selectBarRect = self.selectBar.get_rect()
        self.selectBarRect.topleft = self.createBarRect.topright
        
        font = pygame.font.Font(None, 36)
        
        self.regularButtons = []
        text = font.render("Save", 1, (0,0,0))
        self.regularButtons.append(button.Button(screen.get_width()-100, screen.get_height()-300, text, SaveProtocolOnClick(), "Blank", True))
        text = font.render("Load", 1, (0,0,0))
        self.regularButtons.append(button.Button(screen.get_width()-100, screen.get_height()-200, text, LoadProtocolOnClick(), "Blank"))
        text = font.render("Exit", 1, (0,0,0))
        self.regularButtons.append(button.Button(screen.get_width()-100, screen.get_height()-100, text, ExitProtocolOnClick(), "Blank"))
        
        self.createButtons = []
        text = font.render("Variable", 1, (0,0,0))
        self.createButtons.append(button.Button(0, 25, text, CreateSelectOnClick("variable"), "Blank", True))
        text = font.render("Function", 1, (0,0,0))
        self.createButtons.append(button.Button(0, 125, text, CreateSelectOnClick("function"), "Blank"))
        text = font.render("If", 1, (0,0,0))
        self.createButtons.append(button.Button(0, 225, text, CreateSelectOnClick("if"), "Blank"))
        text = font.render("While", 1, (0,0,0))
        self.createButtons.append(button.Button(0, 325, text, CreateSelectOnClick("while"), "Blank"))
        text = font.render("Foreach", 1, (0,0,0))
        self.createButtons.append(button.Button(0, 425, text, CreateSelectOnClick("foreach"), "Blank"))
        text = font.render("Create", 1, (0,0,0))
        self.createButtons.append(button.Button(0, 525, text, CreateOnClick(), "Blank"))
        
        self.selectedCreateType = ""
        
        self.buttons = self.regularButtons + self.createButtons + self.protocolItems
        
    def update(self):
        self.buttons = self.regularButtons + self.createButtons + self.protocolItems
        
        for b in self.buttons:
            b.update()
        return super(ProtocolEditor, self).update()
        
    def draw(self, screen):
        screen.blit(self.createBar, self.createBarRect)
        screen.blit(self.selectBar, self.selectBarRect)
        
        super(ProtocolEditor, self).draw(screen)
        
        for b in self.createButtons:
            b.draw(screen)
            
        for p in self.protocolItems:
            p.draw(screen)
            
        for l in self.links.values():
            if l != None:
                pygame.draw.line(screen, (255,255,255), l[0], l[1])
            
        if self.startName != "":
            position1 = self.buttons[self.startIndex].get_link_position(self.startName)
            position2 = pygame.mouse.get_pos()
            pygame.draw.line(screen, (255,255,255), position1, position2)
            
    def handle_event(self, event):
        returnValue = super(ProtocolEditor, self).handle_event(event)
        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                self.reset_link_drag()
        return returnValue
                
            
    def select_create_type(self, value):
        self.selectedCreateType = value
        
    def save(self):
        pass
        
    def load(self):
        pass
        
    def exit(self):
        pass
        
    def create_selected(self):
        if self.selectedCreateType == "variable":
            self.protocolItems.append(protocolitem.ProtocolItem(variable.Variable()))
            return
        if self.selectedCreateType == "function":
            self.protocolItems.append(protocolitem.ProtocolItem(function.Function()))
            return
        if self.selectedCreateType == "if":
            self.protocolItems.append(protocolitem.ProtocolItem(function.IfStatement()))
            return
        if self.selectedCreateType == "while":
            self.protocolItems.append(protocolitem.ProtocolItem(function.WhileLoop()))
            return
        if self.selectedCreateType == "foreach":
            self.protocolItems.append(protocolitem.ProtocolItem(function.ForeachLoop()))
            return
        
    def set_start(self, name):
        self.startIndex = self.index
        self.startName = name
        
        if self.buttons[self.startIndex].set_link(self.startName, None):
            self.links[str(self.startIndex) + self.startName] = None
        
    def set_end(self, name):
        self.endIndex = self.index
        self.endName = name
        
        if self.startName == "":
            self.reset_link_drag()
            return
        
        button1 = self.buttons[self.startIndex]
        button2 = self.buttons[self.endIndex]
            
        if button1.set_link(self.startName,button2):
            position1 = button1.get_link_position(self.startName)
            position2 = button2.get_link_position(self.endName)
            self.links[str(self.startIndex) + self.startName] = [position1, position2]
            self.reset_link_drag()
            return
            
        if button2.set_link(self.startName,button1):
            position1 = button2.get_link_position(self.endName)
            position2 = button1.get_link_position(self.startName)
            self.links[str(self.endIndex) + self.endName] = [position1, position2]
            self.reset_link_drag()
            return
        
        self.reset_link_drag()
        
    def reset_link_drag(self):
        self.startIndex = 0
        self.startName = ""
        self.endIndex = 0
        self.endName = ""
        
class SaveProtocolOnClick(button.OnClick):
    def unclicked(self, m):
        self.isClicked = False
        m.save()
        
class LoadProtocolOnClick(button.OnClick):
    def unclicked(self, m):
        self.isClicked = False
        m.save()
        
class ExitProtocolOnClick(button.OnClick):
    def unclicked(self, m):
        self.isClicked = False
        m.leave_menu()
        
class CreateOnClick(button.OnClick):
    def unclicked(self, m):
        self.isClicked = False
        m.create_selected()
        
class CreateSelectOnClick(button.OnClick):
    def __init__(self, type = ""):
        super(CreateSelectOnClick, self).__init__()
        self.type = type
        
    def unclicked(self, m):
        self.isClicked = False
        m.select_create_type(self.type)