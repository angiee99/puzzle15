
from gameSettings import *
from puzzleStar import *
from fileModule import *
from popupScreen import Screen

pygame.init()
from buttonList import ButtonList
tileFont = pygame.font.SysFont('Segoe UI', 56)
scoreFont = pygame.font.SysFont('Segoe UI', 40)

class Game: 
    def __init__(self): 
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption(TITLE) 

        self.board = PuzzleStar(size=GAME_SIZE) #could be PuzzleBoard with PuzzleStar inside but + GUI methods
        self.active = False
        self.start_time = 0 
        self.winTime = 0
        self.fileHandler = FileModule()
        self.bestScore = self.fileHandler.readScore()
        self.buttons = ButtonList(self) # game is the attr of ButtonList
        self.rules_screen = Screen()
        self.showing_rules = False

    def play(self): 
        self.clock = pygame.time.Clock()
        self.resumeSaved = False 
        
        while True:
            if self.active:   
                if self.showing_rules:
                    self.rules_screen.draw()
                    self.showing_rules = self.rules_screen.handle_events()                    
                else:           
                    self.drawBoard()
                    self.buttons.draw() 
                    self.handleActiveEvents()
                    self.display_score()
                    self.checkIfWon()
            else: 
                self.drawWinScreen()
                self.buttons.draw() 
                self.display_score()
                self.handleNonActiveEvents()
            
            pygame.display.flip()
            self.clock.tick(FPS)
   
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
        text1 = "Welcome to Puzzle 15"
        text2 = "You won!"
        if self.start_time == 0: win_surf = tileFont.render(text1, 1, NLIGHT)
        else: win_surf = tileFont.render(text2, 1, NLIGHT)
        win_rect = win_surf.get_rect(midbottom = (SCREEN_WIDTH//2, SCREEN_HEIGHT//2-60))
        
        self.screen.blit(win_surf, win_rect)
        self.screen.blit(click_surf, click_rect)

    def handleActiveEvents(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.fileHandler.writeBoard(self.board.state) # automatically saving board when exiting
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
                self.buttons.update(pos)
    
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
                self.buttons.update(pos)
    
    def restartGame(self):
        if not self.resumeSaved: 
            self.board.shuffleMoves()

        self.buttons.reset()
        self.active = True
        self.resumeSaved = False
        self._resetScore()

    
    def _getCurrentTime(self): 
        return int ((pygame.time.get_ticks() - self.start_time) / 1000)
    
    def display_score(self): 
        if self.active:
            score_surf = scoreFont.render(f'score: {self._getCurrentTime()}', 1, NLIGHT)
            score_rect = score_surf.get_rect(bottomleft = (505, 70))

        else: 
            best_score_color = NLIGHTBLUE
            if self.winTime == self.bestScore:  best_score_color = OLIVE 
            score_surf = scoreFont.render(f'score: {self.winTime}', 1, NLIGHTBLUE)
            score_rect = score_surf.get_rect(center = (SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + 30))
            best_score_surf = scoreFont.render(f'Best score: {self.bestScore}', 1, best_score_color)
            best_score_rect = score_surf.get_rect(topleft = (SCREEN_WIDTH//2 - 115, SCREEN_HEIGHT//2 + 70))
            self.screen.blit(best_score_surf, best_score_rect)

        self.screen.blit(score_surf, score_rect)

    def moveTiles(self, pos=None, dir=None):
        if pos:
            puzzleCoord = (pos[1]//TILESIZE,
                       pos[0]//TILESIZE) #?
            dir = (puzzleCoord[0] - self.board.blankPos[0],
                    puzzleCoord[1] - self.board.blankPos[1])
        self.board.move(dir)
    
    def _resetScore(self): 
        self.start_time = pygame.time.get_ticks()

    
  
if __name__ == "__main__": 

    game = Game()
    game.play()