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
        self.title_rect = self.title_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2-170))
        self.footer_text = self.font.render("Press any key to get back to the game", True, NBLUE)
        self.footer_rect = self.footer_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT-70))


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
        self.screen.fill(NLIGHTBLUE)  # Fill the screen with black color
        self.screen.blit(self.title_text, self.title_rect)  # Display the title text
        self.screen.blit(self.footer_text, self.footer_rect)
        # Display the rules text
        rules_text = [
            "1. Move the tiles by clicking on them.",  
            "2. If you are stuck, use autosolve (press key 'a').",
            "3. To see the right moves, click&move them (press key 'm')." ,
            "4. If you wish, reshuffle the tiles (press key 'r').", 
            "5. You can save any game board for later." , 
            "6. Get the best score and win the game, dude." 
        ]

        rule_font = pygame.font.SysFont('Arial', 24)
        line_height = rule_font.get_linesize()

        # Calculate the total height of the rules text
        total_height = len(rules_text) * line_height

        # Calculate the vertical position to center the rules text
        y = (SCREEN_HEIGHT - total_height) // 2 - 20

        # Display each rule with a number
        for i, rule in enumerate(rules_text):

            rule_text_surface = rule_font.render(rule, True, NLIGHT)
            rule_text_rect = rule_text_surface.get_rect(topleft=(90, y))
            self.screen.blit(rule_text_surface, rule_text_rect)

            y += line_height+10
        # Update the display
        pygame.display.flip()