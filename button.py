from gameSettings import *
buttonFont = pygame.font.SysFont('Segoe UI', 28)

class Button(pygame.sprite.Sprite):
    '''
    represents a single button that is clickable and changable
    '''
    def __init__(self, text: str, pos: tuple, text_color=BLACK, bg_color=None, feedback="", hover_color=GREY):
        super().__init__()
        self.__pos = pos
        self._text = text
        self._initText = text
        self.__text_color = text_color
        self.__bg_color = bg_color
        self.__feedback = feedback
        self.__hover_color = hover_color
        self.__clickedState = None
    
    def _countCoord(self, text_size: tuple):
        '''
        counts the width and height of the button 
        differs if a button has a bg_color or not
        '''
        button_width  = text_size[0]
        button_height = text_size[1]
        if self.__bg_color is not None:
            button_width  = 250
            button_height *= 2
        return (button_width, button_height)
   
    def showButton(self):
        '''
        creates a surface and displays it
        '''
        self.text_surf = buttonFont.render(self._text, True, self.__text_color).convert_alpha()
        self._coordinates = self._countCoord( self.text_surf.get_size())

        self.__image = pygame.Surface(self._coordinates)
        self.__rect = self.__image.get_rect()
          
        if self.__bg_color is None:
            self.__image.fill(NBLUE)
        else:
            self.__image.fill(self.__bg_color)
            
            # text_pos is the center of surface        
        self.text_pos = self.text_surf.get_rect(center = self.__rect.center) 
        self.__image.blit(self.text_surf, self.text_pos)
        self.__rect.topleft = self.__pos 

    #прапорець wasClicked
    def clicked(self):
        ''' 
        changes the way button looks and changes the clickedState flag
        '''
        if self.__clickedState == 1: self.__clickedState += 1
        elif self.__clickedState == 2: return
        else: self.__clickedState = 1
        self.__image.fill(YELLOW)
   
    
    def missionCompleted(self):
        ''' 
        changes the way button looks and changes the clickedState flag\n
        if a button should change when the function terminates, 
        this methos is responsoble for that
        '''
        if self.__feedback == "" or self.__clickedState == False: 
            self.__clickedState == False
        else:  
            self._text = self.__feedback
            self.__clickedState = 2
            self.__image.blit(self.text_surf, self.text_pos)
   
    def backToInit(self): 
        '''
        changes the clickedState flag and turns the text back to initial
        '''
        self._text = self._initText 
        self.__clickedState = False

    def hovered(self):
        '''
        changes the color of the button if the mouse hovers
        '''
        hover = self.__rect.collidepoint(pygame.mouse.get_pos())
        if hover and not self.__clickedState:
            self.__image.fill(self.__hover_color)
            self.__image.blit(self.text_surf, self.text_pos)
    
    @property
    def pos(self):
        return self.__pos
    @property
    def text(self):
        return self._text
    @property
    def initText(self):
        return self._initText
    @property
    def text_color(self):
        return self.__text_color
    @property
    def bg_color(self):
        return self.__bg_color
    @property
    def feedback(self):
        return self.__feedback
    @property
    def feedback(self):
        return self.__feedback
    @property
    def hover_color(self):
        return self.__hover_color
    @property
    def clickedState(self):
        return self.__clickedState
    @property
    def image(self):
        return self.__image
    @property
    def rect(self):
        return self.__rect