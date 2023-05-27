# import pygame
from gameSettings import *
from board import Puzzle
from astar import IDAstar

pygame.init()
tileFont = pygame.font.SysFont('Viga', 72)
scoreFont = pygame.font.SysFont('Viga', 36)
buttonFont = pygame.font.SysFont('Viga', 36)

class Game: 
    def __init__(self): 
        # pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption(TITLE)

    def play(self): 
        self.clock = pygame.time.Clock()
        self.board = Puzzle(size=GAME_SIZE)
        self.active = True
        self.start_time = 0 
        self.buttons = self.createButtons() 
        while True:
            if self.active:             
                self.drawBoard()
                #separate 
                self.checkButtons() 
                self.handleActiveEvents()
               #separate
                # self.reactToButtons()
                self.display_score()
                self.checkIfWon()
            else: 
                self.drawWinScreen()
                self.display_score()
                self.handleNonActiveEvents()
            
            pygame.display.flip()
            self.clock.tick(FPS)
   
    def createButtons(self):
        self.btReshuffle = Button("Reshuffle", (510, 120), BLACK, BLUE, "Shuffleddd")
        self.btAutosolve = Button("Autosolve", (505, 220), BLACK, BLUE, "Click&Move")
        self.btSave = Button("Save game", (505, 320), BLACK, BLUE)
        
        btSprites = pygame.sprite.Group()
        
        btSprites.add(self.btReshuffle)
        btSprites.add(self.btAutosolve)
        btSprites.add(self.btSave)

        return btSprites
        # btSprites.update()
        
    def checkButtons(self, pos=None): 
        for sprite in self.buttons:
            sprite.showButton()
            sprite.hovered()
            if pos is not None: # bt was clicked 
                if  sprite.rect.collidepoint(pos):
                    sprite.clicked()
                    if sprite == self.btReshuffle:
                        self.board.shuffleMoves()
                    elif sprite == self.btAutosolve: 
                        self.dirs = IDAstar(self.board)
                    sprite.missionCompleted()    
            
            # sprite.clicked()
        self.buttons.draw(self.screen)

    def drawBoard(self):
        self.screen.fill(OLIVE)

        for i in range(self.board.size):
            for j in range(self.board.size):
                currentTileColor = DARKGREEN
                numberText = str(self.board[i][j])

                if self.board[i][j] == 0:
                    currentTileColor = YELLOW
                    numberText = ''
#?
                rect = pygame.Rect(j*BOARD_WIDTH/self.board.size,
                                    i*BOARD_HEIGHT/self.board.size + 5, # + 5 adds space, but numbers are not centered 
                                    BOARD_WIDTH/self.board.size,
                                    BOARD_HEIGHT/self.board.size)
#?
                pygame.draw.rect(self.screen, currentTileColor, rect)
                pygame.draw.rect(self.screen, OLIVE, rect, 1) #draws lines
#?
                fontImg = tileFont.render(numberText, 1, YELLOW)
                self.screen.blit(fontImg,
                            (j*BOARD_WIDTH/self.board.size+ (BOARD_WIDTH/self.board.size - fontImg.get_width())/2,
                            i*BOARD_HEIGHT/self.board.size + (BOARD_HEIGHT/self.board.size - fontImg.get_height())/2))
    
    def checkIfWon(self):
        if(self.board.ifWon() and self.clock.get_time() > 1): 
                    self.winTime = self._getCurrentTime()
                    self.active = False
    
    def drawWinScreen(self):
        self.screen.fill(BLUE)
        ''' sprite winText'''
        win_surf = tileFont.render(f'You won!', 1, YELLOW)
        win_rect = win_surf.get_rect(midbottom = (SCREEN_WIDTH//2, SCREEN_HEIGHT//2))
        self.screen.blit(win_surf, win_rect)

    def handleActiveEvents(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit(0)
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r: 
                    self.board.shuffleMoves()
                #do not need this functionality with pygame.K_s
                # as it has no sense but good for tests
                elif event.key == pygame.K_s:
                    self.board.get_solved_state()
                elif event.key == pygame.K_a:
                    self.dirs = IDAstar(self.board)
                    print(self.dirs)
                elif event.key == pygame.K_m:
                    if self.dirs:
                        d = self.dirs.pop(0)
                        self._moveTiles(d)

            elif event.type == pygame.MOUSEBUTTONUP:
                pos = pygame.mouse.get_pos()
                self.checkButtons(pos)
                
                puzzleCoord = (pos[1]//TILESIZE,
                                pos[0]//TILESIZE) #?
                dir = (puzzleCoord[0] - self.board.blankPos[0],
                        puzzleCoord[1] - self.board.blankPos[1])
                self._moveTiles(dir)

    def handleNonActiveEvents(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit(0)
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE: 
                    self.board.shuffleMoves()
                    self.active = True
                    self.start_time = pygame.time.get_ticks()
    
    def _getCurrentTime(self): 
        return int ((pygame.time.get_ticks() - self.start_time) / 1000)
    
    def display_score(self): 
        test_font = pygame.font.Font(None, 50)
        if self.active:
            score_surf = scoreFont.render(f'score: {self._getCurrentTime()}', 1, DARKGREEN)
            score_rect = score_surf.get_rect(bottomleft = (510, 50))

        else: 
            score_surf = test_font.render(f'score: {self.winTime}', 1, OLIVE)
            score_rect = score_surf.get_rect(center = (SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + 50))
        self.screen.blit(score_surf, score_rect)

    def _moveTiles(self, dir):
        self.board.move(dir)


class Button(pygame.sprite.Sprite):
    def __init__(self, text, pos, text_color=BLACK, bg_color=None, feedback=""):
        super().__init__()
        self.pos = pos
        self.text = text
        self.text_color = text_color
        self.bg_color = bg_color
        self.feedback = feedback

        self.clickedState = None
        # self.showButton()

    def showButton(self):
        self.text_surf = buttonFont.render(self.text, True, self.text_color).convert_alpha()
        text_size = self.text_surf.get_size()

        button_width  = text_size[0]
        button_height = text_size[1]
        if self.bg_color is not None:
            button_width  *= 2
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
        print("clicked")
        self.clickedState = 1
        self.image.fill(YELLOW)
   
    #змінить прапорець wasClicked на реді 
    def missionCompleted(self):
        if self.feedback == "": 
            self.clickedState = False
        else: 
            self.text = self.feedback
            # self.text_surf = buttonFont.render(
            #         self.feedback, True, self.text_color).convert_alpha()
            self.clickedState = 2
            self.image.blit(self.text_surf, self.text_pos)
    
    def hovered(self):
        hover = self.rect.collidepoint(pygame.mouse.get_pos())
        if hover and not self.clickedState:
            self.image.fill(PINK)
            self.image.blit(self.text_surf, self.text_pos)
        # else:  self.image.fill(YELLOW)
    

            
if __name__ == "__main__": 
    game = Game()
    game.play()