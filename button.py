from gameSettings import *
buttonFont = pygame.font.SysFont('Viga', 36)

class Button(pygame.sprite.Sprite):
    def __init__(self, text, pos, text_color=BLACK, bg_color=None, feedback="", hover_color=BLUE):
        super().__init__()
        self.pos = pos
        self.text = text
        self.initText = text
        self.text_color = text_color
        self.bg_color = bg_color
        self.feedback = feedback
        self.hover_color = hover_color
        self.clickedState = None


    def showButton(self):
        self.text_surf = buttonFont.render(self.text, True, self.text_color).convert_alpha()
        text_size = self.text_surf.get_size()

        button_width  = text_size[0]
        button_height = text_size[1]
        if self.bg_color is not None:
            button_width  = 250
            button_height *= 2

        self.image = pygame.Surface((button_width, button_height))
        self.rect = self.image.get_rect()
          
        if self.bg_color is None:
            self.image.fill(OLIVE)
        else:
            self.image.fill(self.bg_color)
            
            # text_pos is the center of surface        
        self.text_pos = self.text_surf.get_rect(center = self.rect.center) 
        self.image.blit(self.text_surf, self.text_pos)
        self.rect.topleft = self.pos 

    #прапорець wasClicked  = ін проусес
    def clicked(self):
        if self.clickedState == 1: self.clickedState += 1
        elif self.clickedState == 2:  self.clickedState = 2
        else: self.clickedState = 1
        self.image.fill(YELLOW)
   
    #змінить прапорець wasClicked на реді 
    def missionCompleted(self):
        if self.feedback == "" or self.clickedState == False: 
            self.clickedState = False
        else:  
            self.text = self.feedback
            self.clickedState = 2
            self.image.blit(self.text_surf, self.text_pos)

    
    def backToInit(self): 
        self.text = self.initText 
        self.clickedState = False

    def hovered(self):
        hover = self.rect.collidepoint(pygame.mouse.get_pos())
        if hover and not self.clickedState:
            self.image.fill(self.hover_color)
            self.image.blit(self.text_surf, self.text_pos)