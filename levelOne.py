from sprite import *
from globals import *

class LevelOne():

	def __init__(self):
		self.platforms,self.ladders,self.ladderlines = [],[],[]
		self.lines,self.aesthetic_lines= [],[]
		self.barrel = None
                self.k=True

        def platform_lines(self):

                p5 = (WIDTH - 70, HEIGHT-80)
		p1 = (0, HEIGHT-20)
		p7 = (70, HEIGHT-150)
		p3 = (WIDTH * 0.5, HEIGHT-20)
		p9 = (WIDTH - 70, HEIGHT-240)
		p13 = (WIDTH - 70, HEIGHT-390)
		p14 = (WIDTH * 0.5, HEIGHT-400)
		p2 = (WIDTH * 0.5, HEIGHT-20)
		p15 = (0, HEIGHT-400)
		p6 = (0, HEIGHT-100)
		p8 = (WIDTH, HEIGHT-180)
		p4 = (WIDTH, HEIGHT-30)
		p10 = (0, HEIGHT-260)
		p12 = (WIDTH, HEIGHT-340)
		p17 = (WIDTH * 0.5 - 110, HEIGHT-460)
		p18 = (WIDTH * 0.5 - 10, HEIGHT-460)
		p11 = (70, HEIGHT-310)
		p16 = (WIDTH * 0.50, HEIGHT-400)
		line_group = [(p1,p2),(p3,p4)]
		self.lines.append(line_group)
		line_group = [(p5,p6)]
		self.lines.append(line_group)
		line_group = [(p7,p8)]
		self.lines.append(line_group)
		line_group = [(p9,p10)]
		self.lines.append(line_group)
		line_group = [(p11,p12)]
		self.lines.append(line_group)
		line_group = [(p13,p14),(p15,p16)]
		self.lines.append(line_group)
		line_group_7 =[(p17,p18)]
		self.lines.append(line_group_7)

	def ladder_lines(self):

		p5,p7 = (WIDTH * 0.2, HEIGHT * 0.70),(WIDTH * 0.58, HEIGHT * 0.74)
		p1,p3 = (WIDTH * 0.8, HEIGHT * 0.815), (WIDTH * 0.5, HEIGHT * 0.69)
		p9,p11 = (WIDTH * 0.75, HEIGHT * 0.73), (WIDTH * 0.4, HEIGHT * 0.44)
		p16,p13 = (WIDTH * 0.80, HEIGHT * 0.475), (WIDTH * 0.2, HEIGHT * 0.455)
		p17,p4 = (WIDTH * 0.46, HEIGHT * 0.22),(WIDTH * 0.5, HEIGHT * 0.855)
		p2,p6= (WIDTH * 0.8, HEIGHT * 0.954),(WIDTH * 0.2, HEIGHT * 0.85)
		p8,p14 = (WIDTH * 0.58, HEIGHT * 0.56),(WIDTH * 0.2, HEIGHT * 0.595)
		p15,p18 = (WIDTH * 0.80, HEIGHT * 0.330),(WIDTH * 0.46, HEIGHT * 0.37)
		p10,p12 = (WIDTH * 0.75, HEIGHT * 0.565), (WIDTH * 0.4, HEIGHT * 0.605)
		self.ladderlines=[(p1,p2),(p3,p4),(p5,p6),(p7,p8),(p9,p10),(p11,p12),(p13,p14),(p15,p16),(p17,p18)]

	def create(self):
                if self.k:
                    self.ladder_lines()
		    self.platform_lines()
		for line_group in self.lines:

			for line in line_group:

				min_x,max_x = line[0][0],line[1][0]
				if line[1][0] < min_x:
					min_x = min(line[1][0],line[0][0])
					max_x = max(line[0][0],line[1][0])
				step_x = 20
                                l1,s1=line[1][1], line[1][0]
                                l2,s2=line[0][1], line[0][0]
				m=l1-l2
                                m/=float(s1-s2)
				y1,b=line[0][1],line[0][1]
                                b-= (m * line[0][0])

				while  max_x> min_x:
					y = (m * min_x)
                                        y+= b
					self.platforms.append(Sprite(Vector((min_x,y)),Vector((0,0)),Vector((0,0)),redPlatformanim))
					min_x =min_x+ step_x

		for line in self.ladderlines:
			min_y,max_y = line[0][1],line[1][1]
			x = line[1][0]
			step_y = 16
			if min_y > line[1][1] :
				min_y = min(line[1][1],line[0][1])
				max_y = max(line[0][1],line[1][1])
			max_y = max_y - 18
			while  min_y + 36 < max_y:
                                vec0=Vector((0,0))
				self.ladders.append(Sprite(Vector((x -8,max_y)),vec0, vec0, whiteLadderMiddleanim))
				max_y = max_y-step_y
        

	def draw_bonus_display(self, surface):
                col= (230,50,50)
		bonus = smallfont.render("EXTRA", 1,col)
		surface.blit(bonus, (WIDTH*0.755, 20))
		y2,y1 = 80,30
                bonus_rect = pygame.Rect((WIDTH*0.73, 45), (78, 32))
		bonus_score=smallfont.render(str(int(globals.tbonus)).zfill(4),1, MAGENTA)
		surface.blit(bonus_score, (WIDTH*0.77, 45))
                pygame.draw.line(surface, YELLOW, (WIDTH*0.72, y2), (WIDTH*0.90, y2), 2) 



	def draw_hud(self, surface):
		self.draw_bonus_display(surface)
		current_player_title = smallfont.render("SCORE", 1, YELLOW)
		surface.blit(current_player_title, (WIDTH*0.05, 2*10))
		current_score =smallfont.render(str(globals.score).zfill(6),1,MAGENTA)
		surface.blit(current_score, (WIDTH*0.05, 4*10))
		for i in range(globals.mario_num_lives):
			spacing = i*2*3*5
			surface.blit(playerLifes, pygame.Rect(20 + spacing, 70, 25, 25), playerLifes.get_rect())


	def draw(self, surface):

                map(lambda platform:platform.draw(surface),self.platforms)
                map(lambda ladder:ladder.draw(surface),self.ladders)
		self.draw_hud(surface)

	def destroy_platform(self, dt):
		pass
	def update(self):
		pass

