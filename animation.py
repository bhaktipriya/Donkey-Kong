import pygame

class Animation:

	def __init__(self, spr, beg, end, step,velocity = 1):
            self._tm = pygame.time.get_ticks()
	    self._spr,self._step=spr,step
	    self._beg,self._end = beg,end
            #get Rect of Pygame image
    	    imgRect = spr.get_rect()
	    self._velocity,self._rect = velocity,pygame.Rect(beg,0,step,imgRect.h)

	def update(self, dt):

		if self._velocity == 0:
                    #velocity is 0, reset values and return
			self._rect.x,self._rect.top = self._beg,0
			self._tm = 0.0
			return

		self._tm = self._tm+ self._velocity * dt
		if self._tm > 58.0:
			self._tm = 0.0
                        #checking boundary condition,adjusting image rectangle
			if not self._rect.x + self._step != self._end:
				self._rect.x = self._beg - self._step
			
                        self._rect.x += self._step


		
	def draw(self, surface, x, y):
		surface.blit(self._spr, pygame.Rect(x, y, self._step,self._rect.h), self._rect)
