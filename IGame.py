import pygame

from board import Puzzle
from astar import IDAstar

pygame.init()
tileFont = pygame.font.SysFont(' Viga', 72)
scoreFont = pygame.font.SysFont(' Viga', 36)
buttonFont = pygame.font.SysFont('Viga', 36)

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 500
BOARD_WIDTH = 480
BOARD_HEIGHT = 480
FPS = 30
TILESIZE = 128
GAME_SIZE = 4 # 4
TITLE = "Puzzle Game 15" # could be formatted so not only 15 is here

WHITE = "#FBF8F1"
BLACK = "#1A120B"
YELLOW = "#F5F0BB"
OLIVE = "#DBDFAA"
GREEN = "#B3C890"
DARKGREEN = "#7AA874"
BLUE = "#73A9AD"
SEABLUE = "#BCEAD5"
PINK = "#EF9F9F"
LIGHTPINK = "#F8C4B4"
leftPadding = 10



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
        while True:
            if self.active:             
                self.drawBoard()
                self.drawButtons()
                self.handleActiveEvents()
                # self.checkButtons()
                self.display_score()
                self.checkIfWon()
            else: 
                self.drawWinScreen()
                self.display_score()
                self.handleNonActiveEvents()
            
            pygame.display.flip()
            self.clock.tick(FPS)
   
    def drawButtons(self):
        self.btReshuffle = Button("Reshuffle", (500, 150), BLACK, BLUE)
        
        self.btSprites = pygame.sprite.Group()
        self.btSprites.add(self.btReshuffle)
        # btSprites.update()
        for sprite in self.btSprites:
            sprite.hovered()
        
        self.btSprites.draw(self.screen)

        # self.btReshuffle.hovered()


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
        win_surf = tileFont.render(f'You won!', False, YELLOW)
        win_rect = win_surf.get_rect(midbottom = (SCREEN_WIDTH//2, SCREEN_HEIGHT//2))
        self.screen.blit(win_surf, win_rect)

    def handleActiveEvents(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit(0)
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r: 
                    self.board.shuffle()
                #do not need this functionality with pygame.K_s
                # as it has no sense 
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
                    self.board.shuffle()
                    self.active = True
                    self.start_time = pygame.time.get_ticks()
    
    def _getCurrentTime(self): 
        return int ((pygame.time.get_ticks() - self.start_time) / 1000)
    
    def display_score(self): 
        test_font = pygame.font.Font(None, 50)
        if self.active:
            score_surf = scoreFont.render(f'score: {self._getCurrentTime()}', False, DARKGREEN)
            score_rect = score_surf.get_rect(bottomleft = (500, 50))

        else: 
            score_surf = test_font.render(f'score: {self.winTime}', False, OLIVE)
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

        self.showButton()

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
        
    def clicked(self):
        # probably will have to return true/false value
        pass
    def hovered(self):
        hover = self.rect.collidepoint(pygame.mouse.get_pos())
        if hover:
            self.image.fill(PINK)
            self.image.blit(self.text_surf, self.text_pos)
        # else:  self.image.fill(YELLOW)


            
if __name__ == "__main__": 
    game = Game()
    game.play()