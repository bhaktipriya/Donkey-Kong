import pygame, sys
from state import *



if __name__=="__main__":
        application_state = 0
        game = Game()
        game.changeState(Intro())
	application_state = 0
	pygame.display.set_caption("Donkey Kong")
        while 1:

	    game.update()
