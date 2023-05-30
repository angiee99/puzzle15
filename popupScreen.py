import pygame
pygame.init()
from gameSettings import *

class PopupScreen:
    def __init__(self):
        self.screen = pygame.display.get_surface()
        #self.screen = pygame.Surface((SCREEN_WIDTH-100, SCREEN_WIDTH-100)) #possible only
        #                                                                 # if i pass the game as attr
        self.font = pygame.font.SysFont('Arial', 36)
        self.title_text = self.font.render("Puzzle 15", True, NLIGHT)
        self.title_rect = self.title_text.get_rect(center=self.screen.get_rect().center)


    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit(0)
            elif event.type == pygame.KEYDOWN:
                # if event.key == pygame.K_ESCAPE:
                    # Close the pop-up screen
                return False
        return True  


    def draw(self):
        # Draw the pop-up screen
        self.screen.fill(BLUE)  # Fill the screen with black color
        self.screen.blit(self.title_text, self.title_rect)  # Display the title text

        # Update the display
        pygame.display.flip()