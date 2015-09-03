import pygame
import globals
from vector import *
import sprite
import copy

class Mario(sprite.Sprite):
        """This is the main player class"""
	def __init__(self, pos, vel, state, anim):
                """Constructor"""
		super(Mario,self).__init__(pos,vel,Vector((0, 0)),anim)
		self.animationstate = state
		self.actionstate = "on_ground"
		self.jumptime,self.hammer_time = 0,0
		self.ground,self.current_ground = globals.HEIGHT - 20,None
                self.val=1

	def move(self, dt):
            """Move horizontally"""
            #BUG:updates y also
            if self.val:
		self.pos += (self.vel * dt)
		
	def jump(self, time):
            """Jump vertically,set forces"""
	    if self.actionstate == "on_ground":
                if self.val:
                    self.actionstate,self.jumptime = "jumping",0

        def applyJump(self,dt):
                """Animates the forces for Jump"""
		
                if self.actionstate != "jumping":
			return
		self.ground,self.jumptime = globals.HEIGHT - 20,self.jumptime+dt
		if self.jumptime < 10:
			self.acc.x = self.acc.x+ self.vel.x * dt * 0.005
			self.acc.y = self.acc.y-dt * 2.5 * 0.1
			self.vel = self.acc * 2.5 * dt
		if self.val and self.jumptime > 10:
			self.actionstate = "falling"
	
	def climb(self, objects, arrow_pressed):
                """Applies necessary forces for Climb and sets animation"""

		if self.val and self.actionstate == "jumping" or self.actionstate == "falling":
			return

		if self.animation == globals.mario_with_hammer_left_an:
			return
		if self.animation == globals.mario_with_hammer_right_an:
			return

		for obj in objects:

			obj_x = obj[0][0]
			
			top_objy,bot_objy= obj[1][1],obj[0][1]

			if obj[0][1] < obj[1][1]:
				top_objy,bot_objy = obj[0][1],obj[1][1]

			y,yh = self.pos.y,self.pos.y + self.animation._rect.h

			x,xw = self.pos.x,self.pos.x +  self.animation._rect.w

			# bottom of ladder
		        if x < obj_x:
                            if xw > obj_x:
                                if y < bot_objy:
                                    if  yh > bot_objy:
			                if arrow_pressed == "up":
				            self.actionstate,self.animationstate="on_ladder","climb_up"
                                        elif arrow_pressed == "down":
                                            self.actionstate,self.animationstate = "off_ladder","face_back"

			# top of ladder
		        if x < obj_x:
                            if xw > obj_x:
                                if y < top_objy:
                                    if yh > top_objy:
                                        if arrow_pressed == "down":
				            self.actionstate,self.animationstate="on_ladder","climb_up"
                                        elif arrow_pressed == "up":
                                            self.actionstate,self.animationstate = "off_ladder","face_back"

		        if self.actionstate == "on_ladder":
                            if arrow_pressed == "down":
			        self.animationstate = "climb_down"
                            if arrow_pressed == "up":
			        self.animationstate = "climb_up"

	def reachPaulineWin(self, pauline):
                """Mario Pauline collision indicates win"""
		x,y = self.pos.x,self.pos.y
		w,h = self.animation._rect.w,self.animation._rect.h
		
		hx,hy = pauline.pos.x,pauline.pos.y
		hw,hh = pauline.animation._rect.w,pauline.animation._rect.h

                if x + w > hx:
                    if x < hx + hw:
                        if y + h > hy:
                            if y < hy + hh :
                                if (y + h <= globals.HEIGHT-450):
                                    return True

                return False

        def collectCoin(self, coin,surface):
		x,y = self.pos.x,self.pos.y
		w,h = self.animation._rect.w,self.animation._rect.h

		hx,hy = coin.pos.x,coin.pos.y
		hw,hh = coin.animation._rect.w,coin.animation._rect.h
                
		if x + w > hx:
                    if x < hx + hw:
                        if y + h > hy:
                            if y < hy + hh :
                                coin.picked_up,globals.score = True,globals.score + 10
                                return True
                return False


        def hammerCollision(self, hammer):
		"""Hammer Mario collision,starts hammer time"""
                x,y = self.pos.x,self.pos.y
		w,h = self.animation._rect.w,self.animation._rect.h

		hx,hy = hammer.pos.x,hammer.pos.y
		hw,hh = hammer.animation._rect.w,hammer.animation._rect.h

		if x + w > hx:
                    if x < hx + hw:
                        if y + h > hy:
                            if  y < hy + hh:
                                if hammer.picked_up == False:
                                        hammer.picked_up = True
                                        if self.animationstate in ["walk_left","face_left","face_back"]:
                                            self.animation = globals.mario_with_hammer_left_an
                                        elif self.animationstate in ["walk_right","face_right"]:
                                            self.animation = globals.mario_with_hammer_right_an


        def barrelCollision(self, barrels):
		"""Mario barrel collision, leads to loss of life"""
                x,y = self.pos.x,self.pos.y
		w,h = self.animation._rect.w,self.animation._rect.h
		did_die = 0

		cx,cy = x + w / 2.0,y + h / 2.0

		for barrel in barrels:
			if barrel.active == 1:

				bx,by = barrel.pos.x,barrel.pos.y
				bw,bh = barrel.animation._rect.w,barrel.animation._rect.h

				bcx,bcy = bx + bw / 2.0,by + bh / 2.0
				xdist,ydist = abs(cx - bcx), abs(cy - bcy)
                                if xdist < 10:
                                    if bcy - cy > 30:
                                        if bcy - cy < 50:
                                            if  (self.actionstate in["jumping","falling"]):
					            globals.score += 200
					            barrel.reset()
					            return 0

                                if xdist < (w/3.0 + bw/3.0):
                                    if ydist < (h/3.0 + bh/3.0):
					if self.animation == globals.mario_with_hammer_left_an:
					   	globals.score = globals.score+ 200
						barrel.reset()
						return 0

					if globals.mario_with_hammer_right_an== self.animation:
					   	globals.score = globals.score+ 200
						barrel.reset()
						return 0

					self.die()
					did_die,self.val =1, 1
	                                        	
		return did_die
	
        
        def checkTrailCollision(self, objects):
                """To make Mario move along the platform lines"""
                l=True
		for obj in objects:
                    if l:
                        if self.objectCollision(self.pos, obj) == 1:
				return

	
	def reset(self):
		"""Used when mario loses a life"""
		globals.mario_num_lives = 3
		self.pos.x,self.pos.y = 100,globals.HEIGHT-60
		self.vel,self.acc = Vector((0, 0)),Vector((0, 0))
		self.animationstate,self.animation = "face_right",globals.playerWalkingRightanim
		self.jumptime,self.actionstate = 0,"on_ground"
		self.ground, self.current_ground= globals.HEIGHT - 20,None
        
        def die(self):
                """Mario is dead,reset all"""
		self.pos.x,self.pos.y = 100,globals.HEIGHT-60
		globals.mario_num_lives -= 1
		self.vel,self.acc = Vector((0, 0)),Vector((0, 0))
		self.animationstate,self.animation = "face_right",globals.playerWalkingRightanim
		self.jumptime,self.actionstate = 0,"on_ground"
		self.ground, self.current_ground= globals.HEIGHT - 20,None


	

	def objectCollision(self, pos, obj):
		""" General function that returns collision between an object
                and Mario"""
		if self.actionstate == "on_ladder":
			return

		min_x,max_x = obj[0][0][0],obj[0][0][0]
		for line in obj:
			for point in line:
					min_x =min(point[0],min_x)
					max_x =max(point[0],max_x)
					
		for line in obj:

			do_collide = 0

			v1,v2 = Vector(line[0]),Vector(line[1])
			v3 = copy.deepcopy(pos)
                        v3.y,v3.x = v3.y + self.animation._rect.h,v3.x + self.animation._rect.w / 2
			t1,t2 = v2 - v1,v3 - v1
			t = (vecDot(t1,t2))
                        t/= (vecDot(t1, t1))
			v = v1 + t1 * t
			distance = vecDist(v3, v)
			left_obj,right_obj = line[1][0],line[0][0]

			if line[0][0] < line[1][0]:
				left_obj,right_obj = line[0][0],line[1][0]			
                        if distance < 5:
                            if v3.x >= left_obj:
                                if v3.x <= right_obj:
                                    if self.actionstate != "jumping":
				        do_collide = 1
				        self.pos.y = v.y - self.animation._rect.h
				        self.ground,self.current_ground= v.y,line

                        elif (v3.x < min_x or v3.x > max_x):
                            if line == self.current_ground:
				self.ground,self.actionstate = globals.HEIGHT -20,"falling"

		return do_collide

	def sideCollision(self):
                """Collisions along the sides of the frame"""
		if globals.WIDTH < self.pos.x + self.animation._rect.w:
			self.pos.x = globals.WIDTH - self.animation._rect.w
		self.pos.x = max(0,self.pos.x)
		
                if  globals.HEIGHT<self.pos.y + self.animation._rect.h:
			self.pos.y = globals.HEIGHT - self.animation._rect.h
		
                self.pos.y = max(0,self.pos.y)

	def floorCollision(self, ground):
                """Colllisions with the ground"""
		
		if self.actionstate != "on_ladder":
                    if ground <self.pos.y + self.animation._rect.h:
			self.pos.y = ground - self.animation._rect.h
			self.vel.x,self.vel.y = 0,0
                        self.acc.x,self.acc.y = 0,0
			self.jumptime,self.actionstate = 0,"on_ground"

	def applyGroundForce(self, force, dt):
            """Applies necessary force to move on ground"""
	    if self.actionstate == "on_ground":
		if force.x == 0:
			self.vel.x,self.acc.x = 0,0
			return

		self.acc = self.acc+force * dt
		max_accx = 1.5
		
		self.acc.x = min(max_accx,self.acc.x)
		self.acc.x = max(-max_accx,self.acc.x)

                if force.x > 0:
                    if self.vel.x < 0:
			self.acc.x = 0.0

                if force.x < 0:
                    if self.vel.x > 0:
			self.acc.x = 0.0
		        self.val=1
                self.vel = force + self.acc * dt


	def applyVerticalForce(self, force, dt):
            if "on_ladder"== self.actionstate:
		        self.vel = force * dt

	def setAnimationState(self, s):
            """Setter function for animation state"""
            k=True
            if k:
		self.animationstate = s

	def updateAnimation(self, dt):
                """Updates and sets animation"""
                states=["falling","face_left","face_right","jumping"]
		moves=["walk_left","walk_right","run_left","run_right"]
                ladpos=["on_ladder","climb_up","climb_down","face_back"]
                #Hammer animation
                if self.hammer_time > 0:
			if self.animationstate in ["walk_left",states[1]]:
				self.animation = globals.mario_with_hammer_left_an
			elif self.animationstate in ["walk_right", states[2]]:
				self.animation = globals.mario_with_hammer_right_an

		if self.hammer_time > 500:
			self.actionstate = states[0]
			if self.animation == globals.mario_with_hammer_right_an:
                            if self.actionstate == states[0]:
                                self.animation = globals.playerFacingRightanim
			
                        if self.animation == globals.mario_with_hammer_left_an:
                            if self.actionstate == states[0]:
				self.animation = globals.playerFacingLeftanim

			self.hammer_time = 0

                if self.animation == globals.mario_with_hammer_right_an:
                	self.hammer_time += dt
		   	return

		if self.animation == globals.mario_with_hammer_left_an:
		   	self.hammer_time += dt
		   	return
                #Jump animation
		if self.animationstate == states[1]:
			self.animation = globals.playerFacingLeftanim
			
                        if self.actionstate in [states[3],states[0]]:
				self.animation = globals.playerJumpFacingleftanim

		elif self.animationstate == states[2]:
			self.animation = globals.playerFacingRightanim

			if self.actionstate in [states[0],states[3]]:
				self.animation = globals.playerJumpFacingRightanim
		#Walk animation
		elif self.animationstate == moves[0]:
			self.animation = globals.playerWalkingLeftanim
			if self.vel.x == 0:
				self.animationstate = states[1]

                        if self.actionstate in [states[0],states[3]]:
				self.animation = globals.playerJumpFacingleftanim

		elif self.animationstate == moves[1]:
			self.animation = globals.playerWalkingRightanim
			if self.vel.x == 0:
				self.animationstate = states[2]

			if self.actionstate in [states[0],states[3]]:
				self.animation = globals.playerJumpFacingRightanim
                #Run animation
		elif self.animationstate == moves[2]:
			self.animation = globals.playerRunningRrightanim
			if self.vel.x == 0:
				self.animationstate = states[1]

			if self.actionstate in [states[0],states[3]]:
				self.animation = globals.playerJumpFacingleftanim

		elif self.animationstate == moves[3]:
			self.animation = globals.playerRunningRrightanim
			if self.vel.x == 0:
				self.animationstate = states[3]

                        if self.actionstate in [states[0],states[3]]:
				self.animation = globals.playerJumpFacingRightanim

	
                #CLimbing
                if self.actionstate == ladpos[0] and self.vel.y == 0.0:
			self.animation = globals.playerClimbstillanim

		elif self.animationstate == ladpos[1]:
			self.animation = globals.playerClimbupanim

		elif self.animationstate == ladpos[2]:
			self.animation = globals.playerClimbDownanim
		
		elif self.animationstate == ladpos[3]:
			self.animation = globals.playerFacingBackanim


	def applyGravity(self, dt):
                """ applies verticall downward force"""
		if self.actionstate in["on_ground","on_ladder"]:
			return
		self.vel.y += (0.5 * dt)

	def update(self, dt):
                """Calls all the other internal functions and updates Mario"""
                collide=True

		self.applyGravity(dt)
		
		self.applyJump(dt)
                if collide:
		    self.floorCollision(self.ground)
		    self.sideCollision()
		self.move(dt)
                if collide:
		    self.updateAnimation(dt)
		    self.animation.update(dt)

	def draw(self, surface):
                """Draw mario on surface"""
		self.animation.draw(surface, self.pos.x, self.pos.y)

