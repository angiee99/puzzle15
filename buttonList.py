import pygame
pygame.init()
from gameSettings import *
from button import Button


class ButtonList: #mb button Container
    def __init__(self, game):
        self.game = game 
        self.btSprites = self.createActiveBt()  
        self.btWinSprites = self.createWinBt()
    
    def createActiveBt(self):
        self.btReshuffle = Button("Reshuffle", (505, 130), NLIGHT, NLIGHTBLUE, hover_color=GREY)
        self.btAutosolve = Button("Autosolve", (505, 230), NBLUE, NLIGHT, "Click&Move")
        self.btSave = Button("Save game", (505, 330), NLIGHT, NLIGHTBLUE, hover_color=GREY)
        self.btRules    = Button("info", (700, 470), NLIGHT, hover_color=NLIGHTBLUE)
        btSprites = pygame.sprite.Group()
        
        btSprites.add(self.btReshuffle)
        btSprites.add(self.btAutosolve)
        btSprites.add(self.btSave)
        btSprites.add(self.btRules)

        return btSprites
    
    def createWinBt(self):
        self.btResume = Button("Resume last game", (SCREEN_WIDTH//2- 125, SCREEN_HEIGHT//2 + 150),
                              NLIGHT, NLIGHTBLUE, hover_color=GREY)
        btWinSprites = pygame.sprite.Group()
        btWinSprites.add(self.btResume)
        btWinSprites.add(self.btResume)
        return btWinSprites
    
    def reset(self):
        for button in self.btSprites:
            button.backToInit()
    
    def update(self, pos=None):
        if pos is None:
            return
        if self.game.active: 
            self.checkButtons(pos)
        else: 
            self.checkWinButtons(pos)
        self.draw()
    
    def draw(self): #after update
        if self.game.active:
            for button in self.btSprites:
                button.showButton()
                button.hovered()
            self.btSprites.draw(self.game.screen)
        else: 
            for button in self.btWinSprites:
                button.showButton()
                button.hovered()
            self.btWinSprites.draw(self.game.screen)

    def checkWinButtons(self, pos=None):
        for button in self.btWinSprites:
            if  button.rect.collidepoint(pos):
                button.clicked()
                if button == self.btResume:
                    self.resumeSaved = True
                    self.game.board.setState(self.game.fileHandler.readBoard())
                    self.game.restartGame()
            button.missionCompleted()
    

    def checkButtons(self, pos=None): 
        for button in self.btSprites:
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
                    self.game.popup_screen.draw()
                    button.backToInit()

                button.missionCompleted()
            