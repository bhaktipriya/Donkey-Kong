class Timer():

	def __init__(self, t):
		self.time = t
		self.dt,self.dt2 = 0,0

	def update(self, time):
		self.dt2 = time - self.time
		self.dt,self.time = 0.75,time

