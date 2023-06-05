
from gameSettings import *
from puzzleStar import *
from fileModule import *
from rulesScreen import Screen

pygame.init()
from buttonList import ButtonList
tileFont = pygame.font.SysFont('Segoe UI', 56)
scoreFont = pygame.font.SysFont('Segoe UI', 40)
massageFont = pygame.font.SysFont('Segoe UI', 28)

class Game: 
    '''
    Puzzle 15 game with game board, buttons, rules screen and score tracking\n
    Enables self playing as well as autosolving with IDA*
    '''
    def __init__(self): 
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption(TITLE) 

        self.__board = PuzzleStar(size=GAME_SIZE)
        self.__active = False
        self.__start_time = 0 
        self.__winTime = 0
        self.__fileHandler = FileModule()
        self.__bestScore = self.__fileHandler.readScore()
        self.__buttons = ButtonList(self) # game is the attr of ButtonList
        self.__rules_screen = Screen()
        self.__showing_rules = False

    def play(self): 
        '''
        runs the main loop of the game,
        envokes other methods depending on game state
        '''
        self.clock = pygame.time.Clock()
        self.resumeSaved = False 
        
        while True:
            if self.__active:   
                if self.__showing_rules:
                    self.__rules_screen.draw()
                    self.__showing_rules = self.__rules_screen.handle_events()                    
                else:   #if not displaing rules        
                    self.drawBoard()
                    self.__buttons.draw() 
                    self.handleActiveEvents()
                    self.display_score()
                    self.checkIfWon()
            else: # if non-active
                self.drawWinScreen()
                self.__buttons.draw() 
                self.display_score()
                self.handleNonActiveEvents()
            
            pygame.display.flip()
            self.clock.tick(FPS)
   
    def drawBoard(self):
        '''
        draws the main game board and tiles
        '''
        self.screen.fill(NBLUE)

        for i in range(self.__board.size):
            for j in range(self.__board.size):
                currentTileColor = NLIGHT
                numberText = str(self.__board[i][j])

                if self.__board[i][j] == 0: # void tile
                    currentTileColor = NBLUE
                    numberText = ''
                # creates a rect object for a tile
                rect = pygame.Rect(j*BOARD_WIDTH/self.__board.size,
                                    i*BOARD_HEIGHT/self.__board.size + 20, # + 20 adds space above
                                    BOARD_WIDTH/self.__board.size,
                                    BOARD_HEIGHT/self.__board.size)

                pygame.draw.rect(self.screen, currentTileColor, rect)
                pygame.draw.rect(self.screen, NBLUE, rect, 1) #draws lines

                fontImg = tileFont.render(numberText, 1, NBLUE)
                self.screen.blit(fontImg,
                            (j*BOARD_WIDTH/self.__board.size+ (BOARD_WIDTH/self.__board.size - fontImg.get_width())/2,
                            i*BOARD_HEIGHT/self.__board.size + 20 + (BOARD_HEIGHT/self.__board.size - fontImg.get_height())/2))
    
    def checkIfWon(self):
        #checks if the game is won and updates the best score if so
        if(self.__board.ifWon() and self.clock.get_time() > 1): 
            self.__winTime = self._getCurrentTime()
            if(self.__winTime < self.__bestScore):
                self.__bestScore = self.__winTime 
                # self.__fileHandler.writeScore(self.__bestScore) 
            self.__active = False
    
    def drawWinScreen(self):
        '''
        displays the screen for non-active state
        '''
        self.screen.fill(NBLUE)
        click_surf = scoreFont.render("Press Space key to start", 1, NLIGHT)
        click_rect = click_surf.get_rect(midbottom = (SCREEN_WIDTH//2, SCREEN_HEIGHT//2))
       
        text1 = "Welcome to Puzzle 15"
        text2 = "You have won!"
        if self.__start_time == 0: win_surf = tileFont.render(text1, 1, NLIGHT)
        else: win_surf = tileFont.render(text2, 1, NLIGHT)
        win_rect = win_surf.get_rect(midbottom = (SCREEN_WIDTH//2, SCREEN_HEIGHT//2-60))
        
        self.screen.blit(win_surf, win_rect)
        self.screen.blit(click_surf, click_rect)

    def handleActiveEvents(self):
        '''
        goes through all events and delegates them 
        '''
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.__fileHandler.writeBoard(self.__board.state) # automatically saving board when exiting
                pygame.quit()
                quit(0)
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r: 
                    self.__board.shuffleMoves()
                    self._resetScore()
                elif event.key == pygame.K_ESCAPE: #to end the game for test purpose
                    self.__board.get_solved_state()
                elif event.key == pygame.K_a: 
                    self.dirs = self.__board.IDAstar()
                    print(self.dirs)
                    self._resetScore()
                elif event.key == pygame.K_m:
                    if self.dirs:
                        d = self.dirs.pop(0)
                        self.moveTiles(dir=d)                     
                self.__buttons.synchronizeKeys(event.key) # synchronize the buttons to pressed keys

            elif event.type == pygame.MOUSEBUTTONUP:
                pos = pygame.mouse.get_pos()
                self.__buttons.update(pos) #if a button is clicked
    
                self.moveTiles(pos=pos) #if a tile is clicked

    def handleNonActiveEvents(self):
        '''
        goes through all events and delegates them 
        '''
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit(0)
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE: 
                    self.restartGame()
            elif event.type == pygame.MOUSEBUTTONUP:
                pos = pygame.mouse.get_pos()
                try:
                    self.__buttons.update(pos)
                except TypeError as e: 
                    self.displayMassage([f"{e}","Cannot get the board, sorry"])
                    self.__buttons.reset()
                except ValueError as e: 
                    self.displayMassage([f"{e}","Cannot get the board, sorry"])
                    self.__buttons.reset()
                
    def displayMassage(self, text):
        '''
        displays massages for 2.5 seconds on the bottom of the screen
        '''
        start = self._getCurrentTime()
        while self._getCurrentTime() - start < 2.5: # the msg will be displaid for 2.5 seconds
            padding = 0
            for part in text:
                sms_surface = massageFont.render(part, True, NBLUE, NLIGHT)
                sms_rect = sms_surface.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2+ 100+padding))
                self.screen.blit(sms_surface, sms_rect)
                padding += 40
                pygame.display.flip()
        self.__buttons.reset()

    def restartGame(self):
        '''
        starting the game over, resets buttons, score,\n shuffles the tiles 
        or diplays the board read from file, sets active to True
        '''
        if not self.resumeSaved: 
            self.__board.shuffleMoves()

        self.__buttons.reset()
        self.__active = True
        self.resumeSaved = False
        self._resetScore()

    
    def display_score(self): 
        '''
        displayes regular score if game is active\n
        displays current and best score if game is non-active
        '''
        if self.__active:
            score_surf = scoreFont.render(f'score: {self._getCurrentTime()}', 1, NLIGHT)
            score_rect = score_surf.get_rect(bottomleft = (505, 70))

        else: 
            best_score_color = NLIGHTBLUE
            if self.__winTime == self.__bestScore:  best_score_color = OLIVE 
            score_surf = scoreFont.render(f'score: {self.__winTime}', 1, NLIGHTBLUE)
            score_rect = score_surf.get_rect(center = (SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + 30))
            best_score_surf = scoreFont.render(f'Best score: {self.__bestScore}', 1, best_score_color)
            best_score_rect = score_surf.get_rect(topleft = (SCREEN_WIDTH//2 - 115, SCREEN_HEIGHT//2 + 70))
            self.screen.blit(best_score_surf, best_score_rect)

        self.screen.blit(score_surf, score_rect)

    def moveTiles(self, pos: tuple =None, dir: tuple =None):
        ''' 
        moves the tile either by getting direction to move\n
        or by getting the mouse clicked position and counting the direction
        '''
        if pos:
            puzzleCoord = (pos[1]//TILESIZE,
                       pos[0]//TILESIZE) 
            dir = (puzzleCoord[0] - self.__board.blankPos[0],
                    puzzleCoord[1] - self.__board.blankPos[1])
        self.__board.move(dir)
    
    def _resetScore(self): 
        ''' resets the start time to current time'''
        self.__start_time = pygame.time.get_ticks()
    
    def _getCurrentTime(self): 
        return int ((pygame.time.get_ticks() - self.__start_time) / 1000)
    
    @property
    def board(self):
        return self.__board
    @property
    def active(self):
        return self.__active
    @property
    def start_time(self):
        return self.__start_time
    @property
    def win_time(self):
        return self.__win_time
    @property
    def fileHandler(self):
        return self.__fileHandler
    @property
    def bestScore(self):
        return self.__bestScore
    @property
    def buttons(self):
        return self.__buttons
    @property
    def rules_screen(self):
        return self.__rules_screen
    @property
    def showing_rules(self):
        return self.__showing_rules
    
    @showing_rules.setter
    def showing_rules(self, flag):
        self.__showing_rules = flag
    
