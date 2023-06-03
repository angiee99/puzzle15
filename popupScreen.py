import pygame
pygame.init()
from gameSettings import *


class Screen:
    '''
    Full window static screen with readable content
    '''
    def __init__(self):
        self.__screen = pygame.display.get_surface()
        self.font = pygame.font.SysFont('Segoe UI', 36) 
        self.rule_font = pygame.font.SysFont('Segoe UI', 24)
        self.__title = self._createTitle()
        self.__footer = self._createFooter()
        self._createRules()


    def _createRules(self): 
        '''
        write out the rules and calculate the line_height
        '''
        self.__rules_text = [
            "1. Move the tiles by clicking on them.",  
            "2. If you are stuck, use autosolve (press key 'a').",
            "3. To see the right moves, click&move them (press key 'm')." ,
            "4. If you wish, reshuffle the tiles (press key 'r').", 
            "5. You can save any game board for later." , 
            "6. Get the best score and win the game, dude." 
        ]       
        self.__line_height = self.rule_font.get_linesize()
        
    def _createTitle(self):
        '''
        create title surface and rect
        '''
        title_text = self.font.render("Puzzle 15", True, NLIGHT)
        title_rect = title_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2-170))
        return (title_text, title_rect)
    
    def _createFooter(self):
        '''
        create footer surface and rect
        '''
        footer_text = self.font.render("Press any key to get back to the game", True, NBLUE)
        footer_rect = footer_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT-70))
        return (footer_text, footer_rect)
    
    def draw(self):
        '''
        draw the title, footer and rules
        '''
        self.__screen.fill(NLIGHTBLUE)  # Fill the screen 
        self.__screen.blit(self.__title[0], self.__title[1])  # Display the title 
        self.__screen.blit(self.__footer[0], self.__footer[1])# Display the footer 
        
        total_height = len(self.__rules_text) * self.__line_height
        # Calculate the vertical position to center the rules text
        y = (SCREEN_HEIGHT - total_height) // 2 - 20

        # Display each rule with a number
        for i, rule in enumerate(self.__rules_text):
            rule_text_surface = self.rule_font.render(rule, True, NLIGHT)
            rule_text_rect = rule_text_surface.get_rect(topleft=(90, y))
            self.__screen.blit(rule_text_surface, rule_text_rect)

            y += self.__line_height + 10
        # Update the display
        pygame.display.flip()
    
    def handle_events(self):
        '''
        if close was pressed, quit\n
        if any key was pressed, close this screen by returning False
        '''
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit(0)
            elif event.type == pygame.KEYDOWN:
                #close the window if any key was pressed
                return False
        return True  
    @property
    def screen(self):
        return self.__screen
    @property
    def title(self):
        return self.__title
    @property
    def footer(self):
        return self.__footer
    @property
    def rules_text(self):
        return self.__rules_text 