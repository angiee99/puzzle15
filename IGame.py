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
        # self.active = True
        while True: 

            self.drawBoard()
            self.handleEvents()

            # if(self.board.ifWon): 
            #     self.screen.fill("pink")
            
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
        

    def handleEvents(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit(0)
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r: 
                    self.board.shuffle()
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


if __name__ == "__main__": 
    game = Game()
    game.play()