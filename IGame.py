
from gameSettings import *
from puzzleStar import *
from fileModule import *
 

pygame.init()
from button import Button
tileFont = pygame.font.SysFont('Viga', 72)
scoreFont = pygame.font.SysFont('Viga', 48)
# buttonFont = pygame.font.SysFont('Viga', 36)

class Game: 
    def __init__(self): 
        # pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption(TITLE) 

        self.board = PuzzleStar(size=GAME_SIZE) #could be PuzzleBoard with PuzzleStar inside but + GUI methods
        self.active = False
        self.start_time = 0 
        self.winTime = 0
        self.fileHandler = FileModule()
        self.bestScore = self.fileHandler.readScore()
        self.buttons = self.createButtons()
        self.btWinSprites = self.createWinButtons()

    def play(self): 
        self.clock = pygame.time.Clock()
        self.resumeSaved = False 
        
        while True:
            if self.active:             
                self.drawBoard()
                #separate 
                self.checkButtons() 
                self.handleActiveEvents()
                self.display_score()
                self.checkIfWon()
            else: 
                self.drawWinScreen()
                self.checkWinButtons()
                self.display_score()
                self.handleNonActiveEvents()
            
            pygame.display.flip()
            self.clock.tick(FPS)
   
    def createButtons(self):
        self.btReshuffle = Button("Reshuffle", (505, 130), NLIGHT, NLIGHTBLUE, hover_color=GREY)
        self.btAutosolve = Button("Autosolve", (505, 230), NBLUE, NLIGHT, "Click&Move")
        self.btSave = Button("Save game", (505, 330), NLIGHT, NLIGHTBLUE, hover_color=GREY)
        self.btI    = Button("info", (700, 470), NLIGHT, hover_color=NLIGHTBLUE)
        btSprites = pygame.sprite.Group()
        
        btSprites.add(self.btReshuffle)
        btSprites.add(self.btAutosolve)
        btSprites.add(self.btSave)
        btSprites.add(self.btI)

        return btSprites
        
    def checkButtons(self, pos=None): 
        for button in self.buttons:
            button.showButton()
            button.hovered()
            if pos is not None: # bt was clicked 
                if  button.rect.collidepoint(pos):
                    button.clicked()
                    if button == self.btReshuffle:
                        self.board.shuffleMoves()
                        self.btAutosolve.backToInit()
                        self._resetScore()
                    
                    elif button == self.btAutosolve and  button.clickedState == 1: 
                        self.dirs = self.board.IDAstar()
                        self._resetScore()
            
                    elif button == self.btAutosolve and self.dirs:     
                        d = self.dirs.pop(0)
                        self.moveTiles(dir = d)
                        # button.missionCompleted() 
                        # if not self.dirs: button.backToInit() -- cause game will end 
                    elif button == self.btSave:
                        self.fileHandler.writeBoard(self.board)
                    button.missionCompleted()
            
        self.buttons.draw(self.screen)

    def drawBoard(self):
        self.screen.fill(NBLUE)

        for i in range(self.board.size):
            for j in range(self.board.size):
                currentTileColor = NLIGHT
                numberText = str(self.board[i][j])

                if self.board[i][j] == 0:
                    currentTileColor = NBLUE
                    numberText = ''
#?
                rect = pygame.Rect(j*BOARD_WIDTH/self.board.size,
                                    i*BOARD_HEIGHT/self.board.size + 20, # + 5 adds space, but numbers are not centered 
                                    BOARD_WIDTH/self.board.size,
                                    BOARD_HEIGHT/self.board.size)
#?
                pygame.draw.rect(self.screen, currentTileColor, rect)
                pygame.draw.rect(self.screen, NBLUE, rect, 1) #draws lines
#?
                fontImg = tileFont.render(numberText, 1, NBLUE)
                self.screen.blit(fontImg,
                            (j*BOARD_WIDTH/self.board.size+ (BOARD_WIDTH/self.board.size - fontImg.get_width())/2,
                            i*BOARD_HEIGHT/self.board.size + 20 + (BOARD_HEIGHT/self.board.size - fontImg.get_height())/2))
    
    def checkIfWon(self):
        if(self.board.ifWon() and self.clock.get_time() > 1): 
            self.winTime = self._getCurrentTime()
            if(self.winTime < self.bestScore):
                self.bestScore = self.winTime 
                self.fileHandler.writeScore(self.bestScore)
            self.active = False
    
    def drawWinScreen(self):
        self.screen.fill(NBLUE)
        click_surf = scoreFont.render("Press Space key to start", 1, NLIGHT)
        click_rect = click_surf.get_rect(midbottom = (SCREEN_WIDTH//2, SCREEN_HEIGHT//2))
        ''' sprite winText ?'''
        text1 ="Welcome to Puzzle 15"
        text2 = "You won!"
        if self.start_time == 0: win_surf = tileFont.render(text1, 1, NLIGHT)
        else: win_surf = tileFont.render(text2, 1, NLIGHT)
        win_rect = win_surf.get_rect(midbottom = (SCREEN_WIDTH//2, SCREEN_HEIGHT//2-60))
        
        self.screen.blit(win_surf, win_rect)
        self.screen.blit(click_surf, click_rect)

    def handleActiveEvents(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.fileHandler.writeBoard(self.board) # automatically saving board when exiting
                pygame.quit()
                quit(0)
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r: 
                    self.board.shuffleMoves()
                    self._resetScore()
                #do not need this functionality with pygame.K_s
                # as it has no sense but good for tests
                elif event.key == pygame.K_s:
                    self.board.get_solved_state()
                elif event.key == pygame.K_a:
                    self.dirs = self.board.IDAstar()
                    print(self.dirs)
                    self._resetScore()
                elif event.key == pygame.K_m:
                    if self.dirs:
                        d = self.dirs.pop(0)
                        self.moveTiles(dir=d)

            elif event.type == pygame.MOUSEBUTTONUP:
                pos = pygame.mouse.get_pos()
                self.checkButtons(pos)
                
                # puzzleCoord = (pos[1]//TILESIZE,
                #                 pos[0]//TILESIZE) #?
                # dir = (puzzleCoord[0] - self.board.blankPos[0],
                #         puzzleCoord[1] - self.board.blankPos[1])
                self.moveTiles(pos=pos)


    def handleNonActiveEvents(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit(0)
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE: 
                    self.restartGame()
            elif event.type == pygame.MOUSEBUTTONUP:
                pos = pygame.mouse.get_pos()
                self.checkWinButtons(pos)
    
    def restartGame(self):
        if not self.resumeSaved: 
            self.board.shuffleMoves()
        for button in self.buttons:
            button.backToInit()
        self.active = True
        self.resumeSaved = False
        self._resetScore()
        # self.start_time = pygame.time.get_ticks()
    
    def createWinButtons(self):
        self.btResume = Button("Resume last game", (SCREEN_WIDTH//2- 125, SCREEN_HEIGHT//2 + 150),
                              NLIGHT, NLIGHTBLUE, hover_color=GREY)
        btWinSprites = pygame.sprite.Group()
        btWinSprites.add(self.btResume)
        return btWinSprites
        # in createButtons I return the sprite so the same will do here
    
    def checkWinButtons(self, pos=None):
        for button in self.btWinSprites:
            button.showButton()
            button.hovered()
            if pos is not None: # bt was clicked 
                if  button.rect.collidepoint(pos):
                    button.clicked()
                    if button == self.btResume:
                        self.resumeSaved = True
                        self.board.setState(self.fileHandler.readBoard()) 
                        self.restartGame()
                button.missionCompleted()
        self.btWinSprites.draw(self.screen)

    def _getCurrentTime(self): 
        return int ((pygame.time.get_ticks() - self.start_time) / 1000)
    
    def display_score(self): 
        if self.active:
            score_surf = scoreFont.render(f'score: {self._getCurrentTime()}', 1, BLUE)
            score_rect = score_surf.get_rect(bottomleft = (505, 60))

        else: 
            best_score_color = NLIGHTBLUE
            if self.winTime == self.bestScore:  best_score_color = OLIVE 
            score_surf = scoreFont.render(f'score: {self.winTime}', 1, NLIGHTBLUE)
            score_rect = score_surf.get_rect(center = (SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + 30))
            best_score_surf = scoreFont.render(f'Best score: {self.bestScore}', 1, best_score_color)
            best_score_rect = score_surf.get_rect(center = (SCREEN_WIDTH//2 - 35, SCREEN_HEIGHT//2 + 80))
            self.screen.blit(best_score_surf, best_score_rect)

        self.screen.blit(score_surf, score_rect)

    def moveTiles(self, pos=None, dir=None): #bug
        if pos:
            puzzleCoord = (pos[1]//TILESIZE,
                       pos[0]//TILESIZE) #?
            dir = (puzzleCoord[0] - self.board.blankPos[0],
                    puzzleCoord[1] - self.board.blankPos[1])
            # self.board.move(dir)
        self.board.move(dir)
    
    def _resetScore(self): 
        self.start_time = pygame.time.get_ticks()

    

            
if __name__ == "__main__": 
    game = Game()
    game.play()