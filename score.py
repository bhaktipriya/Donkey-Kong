from globals import *
import pygame

class Score():

	def __init__(self):
		self.slide_duration,self.current_slide =100, 0
		self.highscores,self.slide_x =[], 500
		self.getScores()

	def getScores(self):
		scores_file = open("data/highscores.txt", 'r')
		
		for score in scores_file:
			h1, h2 = score.split(':')
			h1,h2 = h1.strip(),h2.strip()
			self.highscores.append((h1,h2))

		scores_file.close()

	def addScore(self, name, score):
                b=(name,score)
		self.highscores.append(b)

	def getHighScore(self):
                return (0,0)

	def saveScores(self):
		scores_file = open("data/highscores.txt", 'w')
		score_text,sorted_scores ="", []
                
                sorted_by_second = sorted(self.highscores,key=lambda tup:
                                          tup[1],reverse=True)
		for score in self.highscores:
                    ln= str(score[0])+":"+str(score[1])+"\n"
                    score_text+=ln

		scores_file.write(score_text)
		scores_file.close()

	def displayAllScores(self, surface, dt, score_index):
		x,y = 1,2
		x,y= x*100,y*100
            
                for hs in self.highscores:
		    thescore=globals.smallfont.render(str(hs[0])+"   "+str(hs[1]), 1,globals.PINK)
		    width = thescore.get_bounding_rect()
                    width=width[2]
		    surface.blit(thescore, (globals.WIDTH/2.0 - (width / 2.0), y))
		    y=y+50
