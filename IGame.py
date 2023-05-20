import pygame
import sys
# from sys import exit
from board import Puzzle

pygame.init()
tileFont = pygame.font.SysFont('raleway', 72)

# WIDTH = 800
# HEIGHT = 541
WIDTH = 480
HEIGHT = 480
FPS = 30
TILESIZE = 128
GAME_SIZE = 4 # 4
TITLE = "Puzzle Game 15" # could be formatted so not only 15 is here

leftPadding = 10

class Game: 
    def __init__(self): 
        # pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption(TITLE)

    def play(self): 
        self.clock = pygame.time.Clock()
        self.board = Puzzle(size=GAME_SIZE)
        self.active = True
        self.start_time = 0 
        while True:
            if self.active:
                self.drawBoard()
                self.handleActiveEvents()
                # self.display_score()
                # print(self.clock.get_time())
                # print(self.board)
                if self.board.ifWon(): print('yes')
                if(self.board.ifWon() and self.clock.get_time() > 1): 
                    self.active = False
            else: 
                self.screen.fill("pink")
                self.handleNonActiveEvents()
            
            pygame.display.flip()
            self.clock.tick(FPS)

    def drawBoard(self):
        self.screen.fill("black")

        for i in range(self.board.size):
            for j in range(self.board.size):
                currentTileColor = "white"
                numberText = str(self.board[i][j])

                if self.board[i][j] == 0:
                    currentTileColor = "grey"
                    numberText = ''

                rect = pygame.Rect(j*WIDTH/self.board.size,
                                    i*HEIGHT/self.board.size,
                                    WIDTH/self.board.size,
                                    HEIGHT/self.board.size)

                pygame.draw.rect(self.screen, currentTileColor, rect)
                pygame.draw.rect(self.screen, "grey", rect, 1)

                fontImg = tileFont.render(numberText, 1, "black")
                self.screen.blit(fontImg,
                            (j*WIDTH/self.board.size+ (WIDTH/self.board.size - fontImg.get_width())/2,
                            i*HEIGHT/self.board.size + (HEIGHT/self.board.size - fontImg.get_height())/2))
        

    def handleActiveEvents(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit(0)
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r: 
                    self.board.shuffle()
                elif event.key == pygame.K_s:
                    self.board.get_solved_state()
            elif event.type == pygame.MOUSEBUTTONUP:
                pos = pygame.mouse.get_pos()
                puzzleCoord = (pos[1]//TILESIZE,
                                pos[0]//TILESIZE)
                dir = (puzzleCoord[0] - self.board.blankPos[0],
                        puzzleCoord[1] - self.board.blankPos[1])

                if dir == self.board.RIGHT:
                    self.board.move( self.board.RIGHT)
                elif dir ==  self.board.LEFT:
                     self.board.move( self.board.LEFT)
                elif dir ==  self.board.DOWN:
                    self.board.move( self.board.DOWN)
                elif dir ==  self.board.UP:
                     self.board.move( self.board.UP)

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
   
    def display_score(self):
        test_font = pygame.font.Font(None, 50)
        current_time = int ((pygame.time.get_ticks() - self.start_time) / 1000)
        score_surf = test_font.render(f'score: {current_time}', False, (64, 64, 64))
        score_rect = score_surf.get_rect(center = (400, 50))
        self.screen.blit(score_surf, score_rect)
        

start_time = 0 

            
if __name__ == "__main__": 
    game = Game()
    game.play()