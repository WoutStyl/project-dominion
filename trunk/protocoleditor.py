import pygame, menu, button, math, protocolitem, function, variable, soldier

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
        self.bar_width = screen.get_width()/6
        
        self.createBar = pygame.Surface((self.bar_width, screen.get_height()), pygame.SRCALPHA, 32).convert_alpha()
        self.createBar.fill((100,100,100))
        self.selectBar = pygame.Surface((self.bar_width, screen.get_height()), pygame.SRCALPHA, 32).convert_alpha()
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
        
        self.selectedCreateType = ""
        self.selectedCreateIndex = 0
        self.createButtons = []
        text = font.render("Variable", 1, (0,0,0))
        self.createButtons.append(button.Button(0, 0, text, CreateSelectOnClick("variable", 0), "Blank"))
        text = font.render("Function", 1, (0,0,0))
        self.createButtons.append(button.Button(0, 75, text, CreateSelectOnClick("function", 1), "Blank"))
        text = font.render("If", 1, (0,0,0))
        self.createButtons.append(button.Button(0, 150, text, CreateSelectOnClick("if", 2), "Blank"))
        text = font.render("While", 1, (0,0,0))
        self.createButtons.append(button.Button(0, 225, text, CreateSelectOnClick("while", 3), "Blank"))
        text = font.render("Foreach", 1, (0,0,0))
        self.createButtons.append(button.Button(0, 300, text, CreateSelectOnClick("foreach", 4), "Blank"))
        text = font.render("Create", 1, (0,0,0))
        self.createButtons.append(button.Button(0, 525, text, CreateOnClick(), "Blank"))
        
        self.selectedOption = ""
        self.selectedOptionIndex = 0
        self.optionButtons = {}
        self.optionButtons["variable"] = []
        list = self.optionButtons["variable"]
        text = font.render("Boolean", 1, (0,0,0))
        list.append(button.Button(self.bar_width, 50, text, OptionSelectOnClick("Boolean", 0), "Blank"))
        text = font.render("Integer", 1, (0,0,0))
        list.append(button.Button(self.bar_width, 100, text, OptionSelectOnClick("Integer", 1), "Blank"))
        text = font.render("String", 1, (0,0,0))
        list.append(button.Button(self.bar_width, 150, text, OptionSelectOnClick("String", 2), "Blank"))
        self.optionButtons["function"] = []
        list = self.optionButtons["function"]
        i = 1
        for key in soldier.Soldier.commands.keys():
            text = font.render(key, 1, (0,0,0))
            list.append(button.Button(self.bar_width, i * 50, text, OptionSelectOnClick(key, i-1), "Blank"))
            i += 1
        
        self.buttons = self.regularButtons + self.createButtons + self.protocolItems
        for key in sorted(self.optionButtons.keys()):
            for aButton in self.optionButtons[key]:
                aButton.set_enabled(False)
            self.buttons += self.optionButtons[key]
        
    def update(self):
        self.buttons = self.regularButtons + self.createButtons + self.protocolItems
        for key in sorted(self.optionButtons.keys()):
            self.buttons += self.optionButtons[key]
        
        for b in self.buttons:
            b.update()
            
        if self.selectedCreateType != "":
            self.createButtons[self.selectedCreateIndex].focus()
            if self.selectedOption != "":
                self.optionButtons[self.selectedCreateType][self.selectedOptionIndex].focus()
        
        return super(ProtocolEditor, self).update()
        
    def draw(self, screen):
        screen.blit(self.createBar, self.createBarRect)
        screen.blit(self.selectBar, self.selectBarRect)
        
        super(ProtocolEditor, self).draw(screen)
        
        for b in self.buttons:
            b.draw(screen)
            
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
                
            
    def select_create_type(self, value, index):
        if self.selectedCreateType in self.optionButtons.keys():
            for aButton in self.optionButtons[self.selectedCreateType]:
                aButton.set_enabled(False)
                
        self.selectedCreateType = value
        self.createButtons[self.selectedCreateIndex].unfocus()
        self.selectedCreateIndex = index
        if self.selectedCreateType in self.optionButtons.keys():
            for aButton in self.optionButtons[self.selectedCreateType]:
                aButton.set_enabled(True)
        
    def select_option(self, option, index):
        self.selectedOption = option
        self.optionButtons[self.selectedCreateType][self.selectedOptionIndex].unfocus()
        self.selectedOptionIndex = index
        
    def save(self):
        pass
        
    def load(self):
        pass
        
    def exit(self):
        pass
        
    def create_selected(self):
        if self.selectedCreateType == "variable":
            if self.selectedOption == "":
                return
            self.protocolItems.append(protocolitem.ProtocolItem(variable.Variable(self.selectedOption)))
        if self.selectedCreateType == "function" and self.selectedOption != "":
            if self.selectedOption == "":
                return
            arguments = soldier.Soldier.commands[self.selectedOption]
            self.protocolItems.append(protocolitem.ProtocolItem(function.Function(arguments[0], self.selectedOption, arguments[1], arguments[2])))
        if self.selectedCreateType == "if":
            self.protocolItems.append(protocolitem.ProtocolItem(function.IfStatement()))
        if self.selectedCreateType == "while":
            self.protocolItems.append(protocolitem.ProtocolItem(function.WhileLoop()))
        if self.selectedCreateType == "foreach":
            self.protocolItems.append(protocolitem.ProtocolItem(function.ForeachLoop()))
            
        self.select_create_type("", 0)
        self.selectedOption = ""
        
    def set_start(self, name):
        self.startIndex = self.index
        self.startName = name
        
        if self.buttons[self.startIndex].set_link(self.startName, None):
            self.links[str(self.startIndex) + self.startName] = None
        
    def set_end(self, name):
        self.endIndex = self.index
        self.endName = name
        
        if self.startName == "" or (self.endName == "" and self.startName == "get") or \
           (self.startName == "get" and self.endName == "get") or \
           (self.startName != "get" and self.endName != "get"):
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
    def __init__(self, type = "", index = 0):
        super(CreateSelectOnClick, self).__init__()
        self.type = type
        self.index = index
        
    def unclicked(self, m):
        self.isClicked = False
        m.select_create_type(self.type, self.index)
        
class OptionSelectOnClick(button.OnClick):
    def __init__(self, option = "", index = 0):
        super(OptionSelectOnClick, self).__init__()
        self.option = option
        self.index = index
        
    def unclicked(self, m):
        self.isClicked = False
        m.select_option(self.option, self.index)