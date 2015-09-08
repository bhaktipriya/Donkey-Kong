class Vector():

	def __init__(self, tuple):
		self.x,self.y = tuple[0],tuple[1]
	
        def __add__(self, b):
                kx,ky=self.x + b.x, self.y + b.y
		return Vector((kx,ky))

	def __sub__(self, b):
                kx,ky=self.x - b.x, self.y - b.y
		return Vector((kx,ky))
	def __div__(self, i):
                kx,ky=self.x/i, self.y/i
                return Vector((kx, ky))
	def __mul__(self, i):
                kx,ky=self.x*i, self.y*i
		return Vector((kx, ky))

	def len(self):
                kx,ky=self.x*self.x, self.y*self.y
		return (kx+ky)**0.5

	def unit(self):
                l=self.len()
		return self / l

	def __repr__(self):
		return self.x, self.y
	
def vecDot(a, b):
        
        kx,ky=a.x*b.x, a.y*b.y
	return kx+ky

def vecDist(a, b):
        kx,ky=(a.x-b.x)**2, (a.y-b.y)**2
	return (kx+ky)**0.5

