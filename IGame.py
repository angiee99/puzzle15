
from gameSettings import *
from board import Puzzle
from puzzleStar import *
from fileModule import *


pygame.init()
from button import Button
tileFont = pygame.font.SysFont('Viga', 72)
scoreFont = pygame.font.SysFont('Viga', 36)
# buttonFont = pygame.font.SysFont('Viga', 36)

class Game: 
    def __init__(self): 
        # pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption(TITLE)

    def play(self): 
        self.clock = pygame.time.Clock()
        self.board = PuzzleStar(size=GAME_SIZE) #could be PuzzleBoard with PuzzleStar inside but + GUI methods
        self.active = False
        self.start_time = 0 
        self.winTime = 0
        self.bestScore = INF
        self.buttons = self.createButtons()
        self.btWinSprites = self.createWinButtons()
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
        self.btReshuffle = Button("Reshuffle", (505, 120), BLACK, GREEN)
        self.btAutosolve = Button("Autosolve", (505, 220), YELLOW, DARKGREEN, "Click&Move")
        self.btSave = Button("Save game", (505, 320), BLACK, GREEN)
        
        btSprites = pygame.sprite.Group()
        
        btSprites.add(self.btReshuffle)
        btSprites.add(self.btAutosolve)
        btSprites.add(self.btSave)

        return btSprites
        # btSprites.update()
        
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
                    
                    elif button == self.btAutosolve and  button.clickedState == 1: 
                        self.dirs = self.board.IDAstar()
            
                    elif button == self.btAutosolve and self.dirs:     
                        d = self.dirs.pop(0)
                        self._moveTiles(d)
                        # button.missionCompleted() 
                        # if not self.dirs: button.backToInit() -- cause game will end 
                    elif button == self.btSave:
                        writeBoard(self.board)
                    button.missionCompleted()
            
        self.buttons.draw(self.screen)

    def drawBoard(self):
        self.screen.fill(YELLOW)

        for i in range(self.board.size):
            for j in range(self.board.size):
                currentTileColor = DARKGREEN
                numberText = str(self.board[i][j])

                if self.board[i][j] == 0:
                    currentTileColor = YELLOW
                    numberText = ''
#?
                rect = pygame.Rect(j*BOARD_WIDTH/self.board.size,
                                    i*BOARD_HEIGHT/self.board.size + 10, # + 5 adds space, but numbers are not centered 
                                    BOARD_WIDTH/self.board.size,
                                    BOARD_HEIGHT/self.board.size)
#?
                pygame.draw.rect(self.screen, currentTileColor, rect)
                pygame.draw.rect(self.screen, GREEN, rect, 1) #draws lines
#?
                fontImg = tileFont.render(numberText, 1, YELLOW)
                self.screen.blit(fontImg,
                            (j*BOARD_WIDTH/self.board.size+ (BOARD_WIDTH/self.board.size - fontImg.get_width())/2,
                            i*BOARD_HEIGHT/self.board.size + 10 + (BOARD_HEIGHT/self.board.size - fontImg.get_height())/2))
    
    def checkIfWon(self):
        if(self.board.ifWon() and self.clock.get_time() > 1): 
            self.winTime = self._getCurrentTime()
            if(self.winTime < self.bestScore):
                self.bestScore = self.winTime 
            self.active = False
    
    def drawWinScreen(self):
        self.screen.fill(BLUE)
        ''' sprite winText'''
        win_surf = tileFont.render(f'You won!', 1, GREY)
        win_rect = win_surf.get_rect(midbottom = (SCREEN_WIDTH//2, SCREEN_HEIGHT//2-20))
        self.screen.blit(win_surf, win_rect)

    def handleActiveEvents(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                writeBoard(self.board) # automatically saving board when exiting
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
                    self.dirs = self.board.IDAstar()
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
        self.start_time = pygame.time.get_ticks()
    
    def createWinButtons(self):
        self.btResume = Button("Resume last game", (SCREEN_WIDTH//2- 125, SCREEN_HEIGHT//2 + 150),
                              YELLOW, DARKGREEN, hover_color=GREY)
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
                        self.board.setState(readBoard()) 
                        self.restartGame()
                button.missionCompleted()
        self.btWinSprites.draw(self.screen)

    def _getCurrentTime(self): 
        return int ((pygame.time.get_ticks() - self.start_time) / 1000)
    
    def display_score(self): 
        test_font = pygame.font.Font(None, 50)
        if self.active:
            score_surf = scoreFont.render(f'score: {self._getCurrentTime()}', 1, BLUE)
            score_rect = score_surf.get_rect(bottomleft = (510, 50))

        else: 
            best_score_color = OLIVE 
            if self.winTime == self.bestScore:  best_score_color = GREEN 
            score_surf = test_font.render(f'score: {self.winTime}', 1, OLIVE)
            score_rect = score_surf.get_rect(center = (SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + 30))
            best_score_surf = test_font.render(f'Best score: {self.bestScore}', 1, best_score_color)
            best_score_rect = score_surf.get_rect(center = (SCREEN_WIDTH//2 - 35, SCREEN_HEIGHT//2 + 80))
            self.screen.blit(best_score_surf, best_score_rect)

        self.screen.blit(score_surf, score_rect)

    def _moveTiles(self, dir):
        self.board.move(dir)



    

            
if __name__ == "__main__": 
    game = Game()
    game.play()