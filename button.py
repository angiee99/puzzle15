from gameSettings import *
buttonFont = pygame.font.SysFont('Viga', 36)

class Button(pygame.sprite.Sprite):
    def __init__(self, text, pos, text_color=BLACK, bg_color=None, feedback="", hover_color=BLUE):
        super().__init__()
        self._pos = pos
        self._text = text
        self._initText = text
        self._text_color = text_color
        self._bg_color = bg_color
        self._feedback = feedback
        self._hover_color = hover_color
        self._clickedState = None
   

    def showButton(self):
    #could be separate
        self.text_surf = buttonFont.render(self._text, True, self._text_color).convert_alpha()
        text_size = self.text_surf.get_size()

        button_width  = text_size[0]
        button_height = text_size[1]
        if self._bg_color is not None:
            button_width  = 250
            button_height *= 2
    #could be separate
        self._image = pygame.Surface((button_width, button_height))
        self._rect = self._image.get_rect()
          
        if self._bg_color is None:
            self._image.fill(NBLUE)
        else:
            self._image.fill(self._bg_color)
            
            # text_pos is the center of surface        
        self.text_pos = self.text_surf.get_rect(center = self._rect.center) 
        self._image.blit(self.text_surf, self.text_pos)
        self._rect.topleft = self._pos 

    #прапорець wasClicked  = ін проусес
    def clicked(self):
        if self._clickedState == 1: self._clickedState += 1
        elif self._clickedState == 2: return
        else: self._clickedState = 1
        self._image.fill(YELLOW)
   
    #змінить прапорець wasClicked на реді 
    def missionCompleted(self):
        if self._feedback == "" or self._clickedState == False: 
            return
        else:  
            self._text = self._feedback
            self._clickedState = 2
            self._image.blit(self.text_surf, self.text_pos)
   
    def backToInit(self): 
        self._text = self._initText 
        self._clickedState = False

    def hovered(self):
        hover = self._rect.collidepoint(pygame.mouse.get_pos())
        if hover and not self._clickedState:
            self._image.fill(self._hover_color)
            self._image.blit(self.text_surf, self.text_pos)
    
    @property
    def pos(self):
        return self._pos
    @property
    def text(self):
        return self._text
    @property
    def initText(self):
        return self._initText
    @property
    def text_color(self):
        return self._text_color
    @property
    def bg_color(self):
        return self._bg_color
    @property
    def feedback(self):
        return self._feedback
    @property
    def feedback(self):
        return self._feedback
    @property
    def hover_color(self):
        return self._hover_color
    @property
    def clickedState(self):
        return self._clickedState
    @property
    def image(self):
        return self._image
    @property
    def rect(self):
        return self._rect