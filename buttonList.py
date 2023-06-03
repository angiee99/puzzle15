import pygame
pygame.init()
from gameSettings import *
from button import Button


class ButtonList: #mb button Container
    '''
    Container for buttons that handles them all together\n
    creates, shows and updates the buttons
    '''
    def __init__(self, game):
        self.__game = game 
        self.__ActiveBt = self.createActiveBt()  
        self.__NonActiveBt = self.createNonActiveBt()
    
    def createActiveBt(self):
        '''
        initialize buttons displayed when game is active
        '''
        self.btReshuffle = Button("Reshuffle", (505, 130), NLIGHT, NLIGHTBLUE)
        self.btAutosolve = Button("Autosolve", (505, 230), NBLUE, NLIGHT, "Click&Move", hover_color=NLIGHTBLUE)
        self.btSave  = Button("Save game", (505, 330), NLIGHT, NLIGHTBLUE)
        self.btRules = Button("info", (700, 470), NLIGHT)
        btSprites = pygame.sprite.Group()
        
        btSprites.add(self.btReshuffle)
        btSprites.add(self.btAutosolve)
        btSprites.add(self.btSave)
        btSprites.add(self.btRules)

        return btSprites
    
    def createNonActiveBt(self):
        '''
        initialize buttons displayed when game is non-active
        '''
        self.btResume = Button("Resume last game", (SCREEN_WIDTH//2- 125, SCREEN_HEIGHT//2 + 150),
                              NLIGHT, NLIGHTBLUE, hover_color=GREY)
        btWinSprites = pygame.sprite.Group()
        btWinSprites.add(self.btResume)
        btWinSprites.add(self.btResume)
        return btWinSprites
    
    def reset(self):
        '''
        turns all buttons to initial state
        '''
        for button in self.ActiveBt:
            button.backToInit()
        for button in self.NonActiveBt:
            button.backToInit()
    
    def update(self, pos=None):
        '''
        checks buttons and updates them
        '''
        if pos is None:
            return
        if self.game.active: 
            self.checkAButtons(pos)
        else: 
            self.checkNaButtons(pos)
        self.draw()
    
    def draw(self): #after update
        '''
        draws buttons depending on game state
        invokes hovered method for each button
        '''
        if self.game.active:
            for button in self.ActiveBt:
                button.showButton()
                button.hovered()
            self.ActiveBt.draw(self.game.screen)
        else: 
            for button in self.NonActiveBt:
                button.showButton()
                button.hovered()
            self.NonActiveBt.draw(self.game.screen)

    def checkNaButtons(self, pos=None):
        '''
        checks if non-active buttons were clicked and invokes their method 
        '''
        for button in self.NonActiveBt:
            if  button.rect.collidepoint(pos):
                button.clicked()
                if button == self.btResume:
                    saved_board = self.game.fileHandler.readBoard()
                    if saved_board: # if the board is read correctly
                        self.game.resumeSaved = True
                        self.game.board.setState(saved_board)
                        self.game.restartGame()
            button.backToInit()
    

    def checkAButtons(self, pos=None): 
        '''
        checks if active buttons were clicked and invokes their method 
        '''
        for button in self.ActiveBt:
            if  button.rect.collidepoint(pos):
                button.clicked()
                if button == self.btReshuffle:
                    self.game.board.shuffleMoves()
                    self.btAutosolve.backToInit()
                    self.game._resetScore()
                
                elif button == self.btAutosolve and  button.clickedState == 1: 
                    self.dirs = self.game.board.IDAstar()
                    self.game._resetScore()
        
                elif button == self.btAutosolve and self.dirs:     
                    d = self.dirs.pop(0)
                    self.game.moveTiles(dir = d)
                   
                elif button == self.btSave:
                    self.game.fileHandler.writeBoard(self.game.board.state)

                elif button == self.btRules and button.clickedState == 1:
                    self.game.showing_rules = True
                    self.game.rules_screen.draw()

            
            button.missionCompleted()
            if button.feedback == "": 
                button.backToInit()
   
    @property 
    def game(self):
        return self.__game
    @property 
    def ActiveBt(self):
        return self.__ActiveBt
    @property 
    def NonActiveBt(self):
        return self.__NonActiveBt
    
