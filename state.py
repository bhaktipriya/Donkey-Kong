import copy
from globals import *
import time
from timer import *
from levelOne import *
import pygame, sys

class StateMachine:
        """A game is a State Machine,which executes various states"""

	def __init__(self):
		self.next_state=0
                self.current_state = None

	def changeState(self, s):
		self.next_state=self.current_state
		self.current_state = s

	def getCurrentState(self):
		self.next_state=self.current_state
		return self.current_state

	def update(self):
		current_state.update()
		self.next_state=self.current_state
class State:
        """This class defines a State of a State Machine"""

	def __init__(self):
	        self.__prev=None
	        self.__cur=None
	        self.__next=None


	def enter(self, sm):
		self.__next,self.__prev =self.__cur,self.__cur
                self.__cur=sm


	def update(self, sm):
                self.__next=self.__cur
                self.__cur=sm


	def exit(self):
	        self.__next=None


class Game(StateMachine):
        """Game is a state machine,inherits properties from its parent"""

	def __init__(self):
                self.ret=1
		self.current_state = None
                self.next_state = None

	def changeState(self, s):
                self.current_state = s
                self.next_state = self.current_state

		if self.current_state and self.next_state:
			self.current_state.enter(self)

	def getCurrentState(self):
                if self.ret:
		    return self.current_state

	def update(self):
		if self.current_state:
                        self.ret=1
			self.current_state.update(self)
                        self.next_state = self.current_state

class Intro(State):
        """State Intro is the first state of Game"""
	def __init__(self):
		self.intro=1
                self.welc=True

	def enter(self, sm):
		self.intro=1


	def update(self, sm):
		menusound.play(-1)
                if self.welc==True:
                    ct=0
                    self.welc=False
                    while ct<14*50:
                        ct+=1
                        frameno=ct/50
                        surface.blit(welcome[frameno],(0,0))
                        pygame.display.flip()

		sm.changeState(StateMenu())



class StateMenu(State):
        """The second state of Game,with Menu options"""
	def __init__(self):
		self.inmenu=1
                self.welc=True

        def enter(self, sm):
		self.inmenu=1


	def update(self, sm):
                timer = Timer(pygame.time.get_ticks())
		intro_scores = Score()
		newgame = 1
                fr=0

                while 1:
			key = pygame.key.get_pressed()
			for event in pygame.event.get():
			    if event.type == pygame.QUIT:
                                sys.exit()

                        if key[pygame.K_UP] or key[pygame.K_w]:
                            newgame = 1
			elif key[pygame.K_DOWN] or key[pygame.K_s]:
                            newgame = 0
                        elif key[pygame.K_RETURN]:
                            if newgame:
				sm.changeState(StateLevelOne())
				break
                            else:
				sm.changeState(ViewHighScoreMenu())
				break
                        a=WIDTH/2 +50
                        if newgame:
                            pointerRect.center = (a+200, HEIGHT/3 + 100)
                        else:
			    pointerRect.center = (a+200, HEIGHT/3 + 200)
                        #Adjust the start,score and pointer buttons
			timer.update(pygame.time.get_ticks())
                        a=WIDTH/2 +50
                        scoresButtonRect = scoresButton.get_rect()
                        logoRect,startButtonRect = logoImage.get_rect(),startButton.get_rect()
                        authorRect, logoBarrelRect= authorImage.get_rect(),logoBarrel.get_rect()
                        startButtonRect.center = (a+300, HEIGHT/3 +100)
                        scoresButtonRect.center = (a+300, HEIGHT/3 +200)
                        logoRect.center,authorRect.center  = (a-50,HEIGHT/3-50),(a-50,HEIGHT-50)
                        logoBarrelRect.center = (WIDTH/5,HEIGHT/2)

                        fr+=1
                        fr%=140
                        kt=fr/10
                        surface.blit(lg[kt],(0,0))
                        #blit images
                        if self.inmenu:
			    surface.blit(authorImage,authorRect)
                        surface.blit(pointer,pointerRect)
                        surface.blit(startButton,startButtonRect)
                        surface.blit(scoresButton,scoresButtonRect)
			surface.blit(authorImage,authorRect)
			surface.blit(logoBarrel,logoBarrelRect)

                        pygame.display.flip()

	def exit(self):
		self.inmenu+=1


class StateLevelOne(State):
        """This class forms the real game,runs the game loop"""
	def __init__(self):
		pass

	def enter(self, sm):
		globals.score,globals.bonus_timer = 0,0
		_ , globals.highscore = GameScore.getHighScore()
		globals.tbonus = 5000
		regular_barrels.reset(1)
		blue_barrels.reset(1)
                regular_barrels.reset(1)
		hammer1.reset()
		hammer2.reset()

                mario.reset()
		menusound.stop()
		Lev1Music.play(-1)



	def update(self, sm):
                k=True
		coin_step_count = 0
		coin_step = 0
                frame=0
                jmpsound=0
		levelOne = LevelOne()
		levelOne.create()
		timer = Timer(pygame.time.get_ticks())
		clock_time,insert_flag = 0,0
		playing_hammer_music=0
                l=0
		while 1:
		        menusound.stop()
			key = pygame.key.get_pressed()
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
                                    sys.exit()
                        if key[pygame.K_ESCAPE] or key[pygame.K_q]:
                            if k==True:
				    menusound.play(-1)
				    Lev1Music.stop()
				    sm.changeState(StateMenu())
				    break

			timer.update(pygame.time.get_ticks())
			clock_time = clock_time+timer.dt2
                        fact=100
                        rst=0
                        #set bonus timer
			globals.bonus_timer = globals.bonus_timer+(timer.dt2 / 1000.0)
			if globals.bonus_timer > 2:
				globals.tbonus -= fact
                                globals.bonus_timer = rst

			globals.tbonus = max(0,globals.tbonus)
			key = pygame.key.get_pressed()

                        #assess input
                        keypressed = 0
                        states=["on_ladder","off_ladder"]
                        animstates=["walk_left","walk_right"]
			if mario.actionstate != states[0]:
				if key[pygame.K_LEFT] or key[pygame.K_a]:
					keypressed = 1
					mario.setAnimationState(animstates[0])
					x,y=-1.5,0
	                                mario.applyGroundForce(Vector((x,y)), timer.dt)

                                if key[pygame.K_RIGHT] or key[pygame.K_d]:
					keypressed = 1
					mario.setAnimationState(animstates[1])
					x,y=1.5,0
	                                mario.applyGroundForce(Vector((x,y)), timer.dt)

				if key[pygame.K_SPACE]:
					keypressed = 1
					mario.jump(timer.time)
                                        jmpsound=1
                                if jmpsound:
                                    jmpsound=0
                                    globals.JumpMusic.play(0, fade_ms=500)


			if key[pygame.K_UP] or key[pygame.K_w]:
                                actn="up"
				keypressed = 1
				mario.climb(levelOne.ladderlines, actn)
				x,y=0,-1.5
	                        mario.applyVerticalForce(Vector((x,y)), timer.dt)

			if key[pygame.K_DOWN]or key[pygame.K_s]:
                                actn="down"
				keypressed = 1
				mario.climb(levelOne.ladderlines,actn)
				x,y= 0,1.5
	                        mario.applyVerticalForce(Vector((x,y)), timer.dt)

			if keypressed == 0:
				x,y=0,0
	                        mario.applyVerticalForce(Vector((x,y)), timer.dt)
	                        mario.applyGroundForce(Vector((x,y)), timer.dt)

                        #check mario coin collisions
			for i in xrange(len(globals.coinlist)):
                            mario.collectCoin(globals.coinlist[i],surface)

                        mario.checkTrailCollision(levelOne.lines)
			reset1 = mario.barrelCollision(regular_barrels.barrels)
			reset2 = mario.barrelCollision(blue_barrels.barrels)
			# Coin animation
                        if coin_step_count % 20 == 0:
				coin_step += 1

                        coin_step = coin_step % 4
			coin_step_count += 1
			coin_step = coin_step % 100


                        gnd,bg=True,True

                        #check mario hammer collisions
			mario.hammerCollision(hammer1)
			mario.hammerCollision(hammer2)

			if mario.animation == globals.mario_with_hammer_right_an:
			         if not playing_hammer_music:
					playing_hammer_music = 1
					HammerMusic.play()
                        if mario.animation == globals.mario_with_hammer_left_an:
				 if not playing_hammer_music:
					playing_hammer_music = 1
					HammerMusic.play()

			else:
				playing_hammer_music = 0



                        win = mario.reachPaulineWin(pauline)
                        #update all barrels
                        oilDrum.update(timer.dt)
			oilDrumFire.update(timer.dt)
			mario.update(timer.dt)
                        if gnd :
			    pauline.update(timer.dt)
			    donkeykong.update(timer.dt)
			barrel_activate_flag = random.randrange(2)

                        if barrel_activate_flag == 1:
                            if gnd and regular_barrels.insert_flag == 0:
					blue_barrels.activate()
			else:
				if gnd and blue_barrels.insert_flag == 0:
					regular_barrels.activate()

                        if gnd:
                            regular_barrels.update(timer, reset1 or reset2)
			    blue_barrels.update(timer, reset1 or reset2)
			    regular_barrels.checkCollisions(levelOne)
			    blue_barrels.checkCollisions(levelOne)


                        for x in xrange(WIDTH/wid+1):
                             for y in xrange(HEIGHT/heig+1):
                                             surface.blit(grass,(x*100,y*100))

                        #Donkey kong logo animation
                        frame+=1
                        if frame <=5:
                            surface.blit(globals.frame1,(WIDTH/2-250,0))
                        elif frame <= 10:
                            surface.blit(globals.frame2,(WIDTH/2-250,0))
                        elif frame <= 15:
                            surface.blit(globals.frame3,(WIDTH/2-250,0))
                        elif frame <= 20:
                            surface.blit(globals.frame4,(WIDTH/2-250,0))
                        elif frame <= 25:
                            frame=0
                            surface.blit(globals.frame5,(WIDTH/2-250,0))
                        if gnd:
                            levelOne.update()
                            if bg:
			        levelOne.draw(surface)


                        #draw all objects
			map(lambda barrel:barrel.draw(surface),stBarrels)

			oilDrum.draw(surface)
			oilDrumFire.draw(surface)

			donkeykong.draw(surface)
			pauline.draw(surface)

                        if gnd:
			    hammer1.draw(surface)
			    hammer2.draw(surface)


                        for i in xrange(len(globals.coinlist)):
                            coinlist[i].draw(surface,coin_step)

			mario.draw(surface)

                        #Mario Win

			regular_barrels.draw(surface)
			blue_barrels.draw(surface)
			if gnd and win == True:
				Lev1Music.stop()
				WinMusic.play()
				ct=0

                                while ct<24*20:
                                        ct+=1
                                        frameno=ct/20
                                        game_over_win_title=bigfont.render("CONGRATULATIONS!",1, YELLOW)
				        surface.fill(BLUE)
                                        surface.blit(game_over_win_title,(WIDTH/2-150,0))
                                        surface.blit(mariodance[frameno],(WIDTH/2,HEIGHT/2-150))
                                        pygame.display.flip()

				WinMusic.stop()
		                menusound.play(-1)
                                sm.changeState(StateMenu())
				return

                        #Mario DEAD
			if gnd and 0>=globals.mario_num_lives :
				Lev1Music.stop()
				playerDeadMusic.play()
				pygame.time.delay(3001)
                                ct=0
                                cryMusic.play(maxtime=1000)
                                for i in xrange(5):
                                    while ct<4*50:
                                        ct+=1
                                        frameno=ct/50
				        game_over_lose_title = bigfont.render("TRY AGAIN!", 1, YELLOW)
                                        surface.blit(princesscry[frameno],(0,0))
				        ct+=1
                                        surface.blit(game_over_lose_title,(WIDTH/2-150,0))
                                        pygame.display.flip()
                                        ct-=1

				for i in range(1001):
                                        pygame.time.delay(5)
					gnd=1

				menusound.play(-1)
                                gnd=1
				sm.changeState(StateMenu())
				return

                        #Mario lost a life
                        if reset1 or reset2:
                                l+=1
				playerDeadMusic.play()
				Lev1Music.stop()
				pygame.time.delay(3001)


                        if reset1 or reset2:
                                if l==1:
                                    lives="LIFE"
                                else:
                                    lives="LIVES"
                                cryMusic.play(maxtime=1000)
                                for i in xrange(5):
			            ct=0
                                    while ct<4*50:
                                        ct+=1
                                        frameno=ct/50
				        msg=bigfont.render(str(l)+" "+lives+" DOWN!",1, YELLOW)
                                        surface.blit(princesscry[frameno],(0,0))
				        surface.blit(msg, (WIDTH/2-150,0))
                                        pygame.display.flip()


				pygame.time.delay(1000)
				Lev1Music.play(-1)
                        else:
                            pygame.display.flip()


	def exit(self):
		self.done=1

class ViewHighScoreMenu(State):
        """This class shows the High scores of the game"""

	def __init__(self):
		self.menu=1
                self.done=0

	def enter(self, sm):
		self.menu=1

        def checkesc(self,ent):
            if ent.type == pygame.QUIT:
                sys.exit()
                if event.type == pygame.KEYUP and pygame.key.name(ent.key) == "escape":
                        return True

            return False



	def update(self, sm):
		timer = Timer(pygame.time.get_ticks())
		score_index = 0
		while 1 and not score_index:
			for event in pygame.event.get():
                            if event.type == pygame.QUIT:
                                score_index=0
                                sys.exit()
                            elif event.type==pygame.KEYUP:
                                if pygame.key.name(event.key) =="escape" or pygame.key.name(event.key) =="q" :
					sm.changeState(StateMenu())
					return
			high_score_title = bigfont.render("High Score", 1,RED)
			width = high_score_title.get_bounding_rect()[2]
			surface.fill(YELLOW)
			surface.blit(high_score_title, (globals.WIDTH/2.0 - (width / 2.0), 90))

                        timer.update(pygame.time.get_ticks())
                        #display all scores
                        if self.menu:
			    GameScore.displayAllScores(surface, timer.dt, score_index)
			    pygame.display.flip()

	def exit(self):
		self.done=1



