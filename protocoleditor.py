import pygame, menu, button, math, protocolitem, function, variable

class ProtocolEditor(menu.Menu):
    def __init__(self):
        super(ProtocolEditor, self).__init__()
        self.stealInput = True
        self.protocolItems = []
        
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
        self.createButtons.append(button.Button(0, 25, text, SelectVariableOnClick(), "Blank", True))
        text = font.render("Function", 1, (0,0,0))
        self.createButtons.append(button.Button(0, 125, text, SelectFunctionOnClick(), "Blank"))
        text = font.render("If", 1, (0,0,0))
        self.createButtons.append(button.Button(0, 225, text, SelectIfOnClick(), "Blank"))
        text = font.render("While", 1, (0,0,0))
        self.createButtons.append(button.Button(0, 325, text, SelectWhileOnClick(), "Blank"))
        text = font.render("Foreach", 1, (0,0,0))
        self.createButtons.append(button.Button(0, 425, text, SelectForeachOnClick(), "Blank"))
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
        
class SaveProtocolOnClick(button.OnClick):
    def unclicked(self, m):
        self.isClicked = True
        m.save()
        
class LoadProtocolOnClick(button.OnClick):
    def unclicked(self, m):
        self.isClicked = True
        m.save()
        
class ExitProtocolOnClick(button.OnClick):
    def unclicked(self, m):
        self.isClicked = True
        m.leave_menu()
        
class CreateOnClick(button.OnClick):
    def unclicked(self, m):
        self.isClicked = True
        m.create_selected()
        
class SelectVariableOnClick(button.OnClick):
    def unclicked(self, m):
        self.isClicked = True
        m.select_create_type("variable")
        
class SelectFunctionOnClick(button.OnClick):
    def unclicked(self, m):
        self.isClicked = True
        m.select_create_type("function")
        
class SelectIfOnClick(button.OnClick):
    def unclicked(self, m):
        self.isClicked = True
        m.select_create_type("if")
        
class SelectWhileOnClick(button.OnClick):
    def unclicked(self, m):
        self.isClicked = True
        m.select_create_type("while")
        
class SelectForeachOnClick(button.OnClick):
    def unclicked(self, m):
        self.isClicked = True
        m.select_create_type("foreach")
        
